#!/usr/bin/env python3
"""Flujo 4 — Correccion y actualizacion automatica.

Reemplaza la referencia rota por el recurso validado, descargandolo localmente
en img/ (o actualizando el enlace absoluto segun corresponda). Escribe en
data/catalog_web.json y regenera data/cat.js, siempre de forma atomica.
"""
from __future__ import annotations
import json, os, re, shutil, tempfile, hashlib
from dataclasses import dataclass
from typing import Callable

from .config import Config, DEFAULT, headers_imagen
from .scanner import ImageRef, REF_LOCAL, REF_HTTP
from .validate import Verdict


@dataclass
class Reparacion:
    ref: ImageRef
    accion: str                 # 'descargada_local' | 'url_actualizada' | 'omitida'
    nuevo_valor: str = ''
    motivo: str = ''
    respaldo: str = ''

    def to_dict(self):
        return {
            'source_file': self.ref.source_file,
            'field_name': self.ref.field_name,
            'modelo': self.ref.model_name,
            'serie': self.ref.serie,
            'valor_anterior': self.ref.raw_value,
            'valor_nuevo': self.nuevo_valor,
            'accion': self.accion,
            'motivo': self.motivo,
            'http_status_anterior': self.ref.http_status,
            'anterior_error': self.ref.error,
            'respaldo': self.respaldo,
        }


# ---------------------------------------------------------------- descarga
def _nombre_local(query: str, ext: str = '.jpg') -> str:
    base = re.sub(r'[^A-Za-z0-9]+', '_', (query or 'imagen')).strip('_')[:70]
    return (base or 'imagen') + ext


def descargar(url: str, destino: str, cfg: Config) -> tuple[bool, str]:
    """Descarga una imagen validada. Devuelve (ok, error).

    Valida magic-bytes y dimensiones sobre los bytes en memoria (no confia en
    la extension de la URL ni del '.part') y usa mkstemp con la extension
    correcta, de modo que _probe_local no rechace el archivo temporal.
    """
    import urllib.request
    from .scanner import _probe_local, _dims_from_bytes, _ext_de_magic
    try:
        req = urllib.request.Request(url)
        for k, v in headers_imagen(cfg).items():
            req.add_header(k, v)
        with urllib.request.urlopen(req, timeout=cfg.timeout) as r:
            datos = r.read(cfg.max_bytes)
    except Exception as e:
        return False, str(e)[:100]

    if len(datos) < cfg.min_bytes:
        return False, f'{len(datos)} bytes < minimo {cfg.min_bytes}'
    ext = _ext_de_magic(datos)
    if ext is None:
        return False, 'magic bytes no reconocidos (no es imagen)'
    w, h = _dims_from_bytes(datos)
    if w and (w < cfg.min_dim or h < cfg.min_dim):
        return False, f'dimensiones degeneradas {w}x{h}'
    if w and w > cfg.max_dim:
        return False, f'imagen gigante {w}x{h}'

    # forzar extension segun contenido; evita el bug del '.part' rechazado
    destino = os.path.splitext(destino)[0] + ext
    ddir = os.path.dirname(destino) or '.'
    os.makedirs(ddir, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=ddir, suffix=ext)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(datos)
    except Exception:
        os.remove(tmp)
        raise
    st, info = _probe_local(tmp, cfg)
    if st != 'ok':
        os.remove(tmp)
        return False, info.get('error', 'no decodifica')
    os.replace(tmp, destino)
    return True, ''


# ---------------------------------------------------------------- escritura atomica
def _escribir_json_atomico(path: str, data, cfg: Config) -> str:
    """Escribe JSON de forma atomica y devuelve la ruta del respaldo."""
    cfg.ensure_dirs()
    respaldo = ''
    if os.path.exists(path):
        respaldo = path + '.bak'
        shutil.copy2(path, respaldo)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
    return respaldo


def _escribir_texto_atomico(path: str, contenido: str) -> None:
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(contenido)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


# ---------------------------------------------------------------- regeneracion
def regenerar_cat_js(cfg: Config, script: str = 'scripts/regenerar_datos.py') -> bool:
    """Regenera data/cat.js desde catalog_web.json (mantiene el pipeline existente)."""
    try:
        import subprocess, sys
        py = sys.executable
        r = subprocess.run([py, os.path.join(cfg.base, script)],
                           cwd=cfg.base, capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            return False
        return os.path.exists(os.path.join(cfg.data, 'cat.js'))
    except Exception:
        return False


def _regenerar_cat_js_manual(cfg: Config) -> bool:
    """Fallback: regenera cat.js sin depender del script externo."""
    try:
        src = os.path.join(cfg.data, 'catalog_web.json')
        with open(src, encoding='utf-8') as f:
            data = json.load(f)
        txt = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        _escribir_texto_atomico(os.path.join(cfg.data, 'cat.js'),
                                'const CAT=' + txt + ';\n')
        return True
    except Exception:
        return False


# ---------------------------------------------------------------- reparacion
def reparar_catalogo(refs: list[ImageRef], veredictos: dict[str, Verdict],
                     cfg: Config = DEFAULT) -> list[Reparacion]:
    """Aplica los veredictos al catalogo. Si cfg.dry_run, solo simula."""
    reparaciones: list[Reparacion] = []
    cambios: dict[str, dict] = {}

    for ref in refs:
        v = veredictos.get(ref.raw_value)
        if not v or not v.valid:
            reparaciones.append(Reparacion(ref=ref, accion='omitida',
                                           motivo='sin candidato valido'))
            continue

        nuevo = v.local_path or v.url
        if v.local_path and os.path.exists(v.local_path):
            nuevo = v.local_path.replace(cfg.base, '').replace('\\', '/').lstrip('/')
            accion = 'descargada_local'
        else:
            accion = 'url_actualizada'

        if cfg.dry_run:
            reparaciones.append(Reparacion(ref=ref, accion=accion + ' (simulado)',
                                           nuevo_valor=nuevo,
                                           motivo=f'score {v.score:.3f}'))
            continue

        # acumular el cambio por archivo+campo
        key = (ref.source_file, ref.field_name)
        cambios.setdefault(ref.source_file, {}).setdefault(ref.field_name, nuevo)
        reparaciones.append(Reparacion(ref=ref, accion=accion,
                                       nuevo_valor=nuevo,
                                       motivo=f'{v.width}x{v.height} {v.size}b score {v.score:.3f}'))

    if cfg.dry_run or not cambios:
        return reparaciones

    # --- aplicar sobre catalog_web.json ---
    for path, campos in cambios.items():
        if not path.endswith('catalog_web.json'):
            continue
        try:
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            for r in reparaciones:
                if r.ref.source_file == path:
                    r.accion = 'omitida'
                    r.motivo = f'no se pudo leer el catalogo: {str(e)[:60]}'
            continue

        items = data if isinstance(data, list) else [data]
        aplicados = 0
        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            for campo, nuevo in campos.items():
                m = re.match(r'^(\w+)\[(\d+)\]$', campo)
                if m and m.group(1) == 'galeria':
                    j = int(m.group(2))
                    gal = item.get('galeria')
                    if isinstance(gal, list) and j < len(gal):
                        gal[j] = nuevo
                        aplicados += 1
                elif campo in ('im', 'imagen', 'image', 'foto'):
                    if item.get(campo):
                        item[campo] = nuevo
                        aplicados += 1
        if aplicados:
            respaldo = _escribir_json_atomico(path, data, cfg)
            for r in reparaciones:
                if r.ref.source_file == path and r.accion != 'omitida':
                    r.respaldo = respaldo

    # --- regenerar cat.js ---
    if not regenerar_cat_js(cfg):
        _regenerar_cat_js_manual(cfg)

    return reparaciones
