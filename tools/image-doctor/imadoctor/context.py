#!/usr/bin/env python3
"""Flujo 2 — Extraccion de contexto y estrategia de busqueda semantica.

Para cada imagen rota junta: alt, title, nombre de archivo original, campos del
modelo (nombre/serie/categoria) y el parrafo adyacente. Con eso construye
consultas de busqueda ordenadas por especificidad.
"""
from __future__ import annotations
import os, re
from urllib.parse import unquote
from dataclasses import dataclass, field
from .scanner import ImageRef

STOP = {'de', 'la', 'el', 'en', 'y', 'del', 'los', 'las', 'un', 'una', 'con',
        'por', 'para', 'the', 'of', 'and', 'hot', 'wheels', 'scale', '1:64',
        'imagen', 'image', 'foto', 'photo', 'file', 'archivo'}

PLACEHOLDER_RE = re.compile(r'(not[_\s]?available|no[_\s]?image|imagen[_\s]?no|'
                            r'placeholder|sin[_\s]?foto|image[_\s]?not|default)', re.I)


@dataclass
class SearchPlan:
    ref: ImageRef
    queries: list[str] = field(default_factory=list)  # de mas a menos especifica
    motivo: str = ''
    filename_hint: str = ''

    def __post_init__(self):
        if self.queries is None:
            self.queries = []


def _limpiar(s: str) -> str:
    s = (s or '')
    # deshacer doble encoding: '100%25' -> '100%' (las URLs de Fandom vienen asÃ-)
    for _ in range(2):
        if '%' not in s:
            break
        dec = unquote(s)
        if dec == s:
            break
        s = dec
    s = s.replace('_', ' ')
    s = re.sub(r'\.(jpe?g|png|webp|gif|svg|avif)$', '', s, flags=re.I)
    s = re.sub(r'\[[^\]]*\]|\([^)]*\)', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def _keywords(texto: str, top: int = 6) -> list[str]:
    palabras = re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ0-9][A-Za-zÁÉÍÓÚÑáéíóúñ0-9'\-]{2,}", texto or '')
    seen, out = set(), []
    for p in palabras:
        pl = p.lower()
        if pl in STOP or pl in seen:
            continue
        seen.add(pl)
        out.append(p)
        if len(out) >= top:
            break
    return out


def es_placeholder(ref: ImageRef) -> bool:
    """True si la referencia apunta a un placeholder generico de la wiki."""
    return bool(PLACEHOLDER_RE.search(ref.raw_value) or PLACEHOLDER_RE.search(ref.resolved))


def planificar(ref: ImageRef) -> SearchPlan:
    """Construye las consultas candidatas para resolver una imagen rota."""
    plan = SearchPlan(ref=ref)
    motivo = []

    if es_placeholder(ref):
        motivo.append('placeholder generico')
    if ref.status == 'missing_file':
        motivo.append('archivo local inexistente')
    if ref.http_status and ref.http_status >= 400:
        motivo.append(f'HTTP {ref.http_status}')
    if ref.error:
        motivo.append(ref.error[:60])
    plan.motivo = '; '.join(dict.fromkeys(motivo)) or 'sin diagnostico'

    # --- metadata exacta del vehiculo: marca + modelo + anio + version + color ---
    # Esta es la query mas fiel: separa los campos en vez de usar el nombre suelto.
    marca = _limpiar(ref.marca)
    modelo = _limpiar(ref.modelo or ref.model_name)
    anio = ref.anio
    version = _limpiar(ref.version)
    color = _limpiar(ref.color)
    serie = _limpiar(ref.serie)

    if marca or modelo:
        base = ' '.join(x for x in (marca, modelo) if x)
        # 1) query principal: marca + modelo + anio (+ version/color si aplica)
        q = base
        if anio:
            q += f' {anio}'
        if version:
            q += f' {version}'
        plan.queries.append(q)
        # 2) con 'Hot Wheels' para mejorar el recall en la wiki/buscadores
        plan.queries.append(f'{base} Hot Wheels')
        # 3) version/color explicitos: la foto de esa variante exacta
        if version or color:
            qv = base
            if anio:
                qv += f' {anio}'
            for extra in (version, color):
                if extra:
                    qv += f' {extra}'
            plan.queries.append(f'{qv} Hot Wheels diecast')
        # 4) toy number / casting code: identifican el molde sin ambiguedad
        if ref.toy_number:
            plan.queries.append(f'Hot Wheels {ref.toy_number} {base}')
        if ref.casting_code:
            plan.queries.append(f'{base} {ref.casting_code} Hot Wheels')
        # 5) serie / categoria como refuerzo
        if serie:
            plan.queries.append(f'{base} {serie} Hot Wheels'.strip())
    elif modelo:
        # sin marca detectada: caer al nombre completo
        plan.queries.append(modelo)
        plan.queries.append(f'{modelo} Hot Wheels')
        if anio:
            plan.queries.append(f'{modelo} {anio} Hot Wheels')

    # --- nombre de archivo como pista (mas especifico que el modelo) ---
    fname = os.path.basename(ref.resolved or ref.raw_value or '')
    fname_limpio = _limpiar(fname)
    if fname_limpio and fname_limpio.lower() != modelo.lower():
        plan.filename_hint = fname_limpio
        plan.queries.insert(0, fname_limpio)

    # --- alt y title ---
    for extra in (ref.alt, ref.title):
        e = _limpiar(extra)
        if e and e.lower() not in ('imagen', 'image', 'foto'):
            plan.queries.append(e)

    # --- keywords del contexto adyacente ---
    kw = _keywords(ref.surrounding)
    if kw:
        plan.queries.append(' '.join(kw[:5]))

    # --- deduplicar preservando orden y preferir los mas largos primero ---
    vistos, final = set(), []
    for q in plan.queries:
        q = q.strip()
        if len(q) < 3:
            continue
        clave = q.lower()
        if clave in vistos:
            continue
        vistos.add(clave)
        final.append(q)
    # mas especifico (mas palabras) primero
    final.sort(key=lambda q: -len(q.split()))
    plan.queries = final[:6]
    return plan


def planificar_todos(refs: list[ImageRef]) -> list[SearchPlan]:
    return [planificar(r) for r in refs]


# ---------------------------------------------------------------- metadata
def planificar_metadata(ref: 'ImageRef', md=None) -> SearchPlan:
    """Plan de busqueda usando los metadatos EXACTOS del vehiculo.

    'Lamborghini Centenario Roadster 2016 2nd Color' encuentra la foto correcta;
    el nombre crudo del catalogo casi nunca lo hace.
    """
    plan = SearchPlan(ref=ref)

    if md is None:
        return planificar(ref)

    diag = []
    if ref.status == 'missing_file':
        diag.append('archivo local inexistente')
    if ref.http_status and ref.http_status >= 400:
        diag.append(f'HTTP {ref.http_status}')
    if ref.error:
        diag.append(ref.error[:60])
    plan.motivo = '; '.join(dict.fromkeys(diag)) or 'sin diagnostico'

    plan.filename_hint = _limpiar(os.path.basename(ref.resolved or ref.raw_value or ''))

    # 1) query principal con marca/modelo/anio/version
    q = md.query_principal()
    if q:
        plan.queries.append(q)

    # 2) alternativas enriquecidas
    for alt in md.query_alternativas():
        plan.queries.append(alt)

    # 3) nombre original completo (por si la metadata fallo)
    nom = _limpiar(ref.model_name or md.nombre_original)
    if nom and nom.lower() not in q.lower():
        plan.queries.append(nom)

    # 4) pista del nombre de archivo
    if plan.filename_hint and len(plan.filename_hint) > 5:
        plan.queries.append(plan.filename_hint)

    # deduplicar y ordenar por especificidad
    vistos, final = set(), []
    for x in plan.queries:
        x = x.strip()
        if len(x) < 4:
            continue
        clave = x.lower()
        if clave in vistos:
            continue
        vistos.add(clave)
        final.append(x)
    final.sort(key=lambda x: -len(x.split()))
    plan.queries = final[:7]
    return plan
