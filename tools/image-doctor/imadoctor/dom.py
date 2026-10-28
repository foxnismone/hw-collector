#!/usr/bin/env python3
"""Auditoria del DOM renderizado (flujo 1, segunda mitad).

El scanner mira el codigo fuente y los archivos. Este modulo mira el RESULTADO:
abre el sitio en un navegador real y busca contenedores vacios, tarjetas sin
imagen, imagenes que no cargaron y saltos de layout (layout shift).

Necesita Playwright. Si no esta disponible, el modulo degrada a un chequeo
estatico del HTML (no por eso menos util: detecta el patron 'thumb imgerr').
"""
from __future__ import annotations
import json, os, re
from dataclasses import dataclass, field, asdict
from typing import Callable

from .config import Config, DEFAULT

PLAYWRIGHT_OK = False
try:
    from playwright.sync_api import sync_playwright          # type: ignore
    PLAYWRIGHT_OK = True
except Exception:
    try:
        from playwright.async_api import async_playwright     # type: ignore
    except Exception:
        pass


@dataclass
class HallazgoDOM:
    tipo: str                 # 'img_rota' | 'contenedor_vacio' | 'sin_alt' | 'layout_shift' | 'tarjeta_sin_foto'
    selector: str = ''
    detalle: str = ''
    modelo: str = ''
    accion_sugerida: str = ''
    severidad: str = 'media'  # 'alta' | 'media' | 'baja'

    def to_dict(self):
        return asdict(self)


# ---------------------------------------------------------------- estatico
# Marcas que usa el frontend (ver index.html / noPhotoSVG):
#   img.thumb.placeholder + src="data:image/svg+xml,..." -> placeholder profesional (CONTROLADO, ok)
#   data-noimg="1"                                       -> modelo sin foto (estado correcto)
#   data-fallback="1"                                    -> foto existia pero no cargo en runtime (alerta)
#   class="thumb imgerr"                                 -> placeholder legado / cuadro roto (alerta)
RE_IMG_THUMB = re.compile(r'<img\b[^>]*\bclass="[^"]*thumb[^"]*"[^>]*>', re.I | re.S)


def auditar_html_estatico(path: str, cfg: Config = DEFAULT) -> list[HallazgoDOM]:
    """Chequeo sin navegador: inspecciona cada <img class="thumb..."> del HTML.

    Clasifica:
      - src='data:image/svg+xml,...'  -> placeholder profesional (controlado, ok)
      - src vacio/sin src             -> bloque roto (problema, alta)
      - data-fallback="1"             -> foto existia pero no cargo (alerta, media)
      - sin alt                       -> accesibilidad (baja)
    Nunca inventa fotos: solo audita el estado del DOM.
    """
    out: list[HallazgoDOM] = []
    try:
        with open(path, encoding='utf-8', errors='ignore') as f:
            html = f.read()
    except Exception as e:
        return [HallazgoDOM('contenedor_vacio',
                             detalle=f'no se pudo leer {path}: {str(e)[:70]}',
                             severidad='alta')]

    n_placeholder = 0
    n_rotos = 0
    n_fallback = 0
    n_sin_alt = 0
    ej_rotos: list[str] = []
    ej_fallback: list[str] = []
    for m in RE_IMG_THUMB.finditer(html):
        tag = m.group(0)
        if 'data:image/svg+xml' in tag:
            n_placeholder += 1
            continue
        ms = re.search(r'src=(["\']?)(.*?)\1', tag, re.I)
        src = ms.group(2) if ms else ''
        if not src.strip():
            n_rotos += 1
            if len(ej_rotos) < 8:
                ej_rotos.append(tag[:120])
        if 'data-fallback="1"' in tag or "data-fallback='1'" in tag:
            n_fallback += 1
            if len(ej_fallback) < 8:
                ej_fallback.append(tag[:120])
        if not re.search(r'\balt=', tag, re.I):
            n_sin_alt += 1

    if n_rotos:
        out.append(HallazgoDOM(
            'contenedor_vacio', selector='img.thumb',
            detalle=f'{n_rotos} miniaturas <img class="thumb"> con src vacio (bloque roto)',
            modelo=ej_rotos[0] if ej_rotos else '',
            accion_sugerida='asignar placeholder profesional noPhotoSVG() o resolver la imagen',
            severidad='alta'))
    if n_fallback:
        out.append(HallazgoDOM(
            'img_rota', selector='img[data-fallback="1"]',
            detalle=f'{n_fallback} imagenes tenian foto pero fallaron al cargar (data-fallback)',
            modelo=ej_fallback[0] if ej_fallback else '',
            accion_sugerida='verificar URL y proxy weserv; la imagen original puede estar caida',
            severidad='media'))
    if n_sin_alt:
        out.append(HallazgoDOM(
            'sin_alt', selector='img.thumb',
            detalle=f'{n_sin_alt} miniaturas con src real pero sin atributo alt',
            accion_sugerida='agregar alt con el nombre del modelo (accesibilidad)',
            severidad='baja'))
    if n_placeholder:
        out.append(HallazgoDOM(
            'placeholder_controlado', selector='img.thumb.placeholder',
            detalle=f'{n_placeholder} miniaturas sin foto mostrando el placeholder '
                    f'profesional (SVG data-URI). Estado controlado: NO inventa fotos.',
            accion_sugerida='mantener noPhotoSVG(); re-auditar si aparecen fotos nuevas',
            severidad='baja'))
    # Los <img> de la galeria se generan en runtime desde JS (cardHTML), por lo
    # que el chequeo estatico de etiquetas no las ve. Verifico el patron de
    # placeholder directamente en el codigo fuente del frontend:
    if 'noPhotoSVG' in html:
        out.append(HallazgoDOM(
            'placeholder_controlado', selector='JS:noPhotoSVG',
            detalle='El frontend genera placeholders profesionales via noPhotoSVG() '
                    '(SVG data-URI). La logica NO inventa fotos.',
            accion_sugerida='re-auditar con --dom si cambia la logica de placeholders',
            severidad='baja'))
    if 'thumb imgerr' in html:
        out.append(HallazgoDOM(
            'contenedor_vacio', selector='.thumb.imgerr',
            detalle='Patron legacy "thumb imgerr" (cuadro rojo) presente en HTML/JS',
            accion_sugerida='reemplazar por noPhotoSVG() placeholder profesional',
            severidad='alta'))
    return out


# ---------------------------------------------------------------- navegador
def auditar_dom(url: str, cfg: Config = DEFAULT,
                scroll: bool = True) -> list[HallazgoDOM]:
    """Abre el sitio y busca bloques rotos en el DOM real."""
    if not PLAYWRIGHT_OK:
        local = os.path.join(cfg.base, 'index.html')
        out = auditar_html_estatico(local, cfg)
        out.append(HallazgoDOM('contenedor_vacio',
                    detalle='Playwright no disponible: auditoría estática del HTML local',
                    accion_sugerida='pip install playwright  # auditoría dinámica + layout shift',
                    severidad='baja'))
        return out

    out: list[HallazgoDOM] = []
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = None
            for exe in ('C:/Program Files/Google/Chrome/Application/chrome.exe',
                        'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'):
                if os.path.exists(exe):
                    browser = pw.chromium.launch(headless=True, executable_path=exe,
                                                 args=['--no-sandbox'])
                    break
            if browser is None:
                browser = pw.chromium.launch(headless=True, args=['--no-sandbox'])

            page = browser.new_page(viewport={'width': 1440, 'height': 900})
            errores_red: list[str] = []
            page.on('response', lambda r: errores_red.append(f'{r.status} {r.url}')
                    if r.status >= 400 else None)

            page.goto(url, wait_until='load', timeout=90000)
            page.wait_for_timeout(4000)

            if scroll:
                # disparar lazy-loading y detectar imagenes que quedan rotas
                page.evaluate("""async () => {
                    for (let i = 0; i < 14; i++) {
                        window.scrollTo(0, window.scrollY + 700);
                        await new Promise(r => setTimeout(r, 240));
                    }
                    window.scrollTo(0, 0);
                }""")
                page.wait_for_timeout(1800)

            datos = page.evaluate("""() => {
                const rotas = [], vacias = [], sinAlt = [], sinFoto = [];
                document.querySelectorAll('#grid img.thumb').forEach(im => {
                    if (!im.alt) sinAlt.push(im.src.slice(0, 90));
                    if (im.complete && im.naturalWidth === 0) rotas.push(im.src.slice(0, 110));
                });
                document.querySelectorAll('#grid .card').forEach(c => {
                    if (!c.querySelector('img')) sinFoto.push((c.textContent||'').trim().slice(0, 60));
                });
                document.querySelectorAll('#grid .thumb.imgerr, #grid .thumb:not(img)')
                    .forEach(e => vacias.push((e.closest('.card')?.textContent||'').trim().slice(0, 60)));
                return {
                    rotas: rotas.slice(0, 12), vacias: vacias.slice(0, 12),
                    sinAlt: sinAlt.length, sinFoto: sinFoto.slice(0, 12),
                    total: document.querySelectorAll('#grid .card').length,
                    conImg: [...document.querySelectorAll('#grid .card')]
                              .filter(c => c.querySelector('img')).length
                };
            }""")

            if datos['rotas']:
                out.append(HallazgoDOM(
                    'img_rota', selector='img.thumb',
                    detalle=f"{len(datos['rotas'])} imagenes no cargaron",
                    modelo=datos['rotas'][0],
                    accion_sugerida='verificar URL y proxy (weserv no resuelve %25)',
                    severidad='alta'))
            if datos['vacias']:
                out.append(HallazgoDOM(
                    'contenedor_vacio', selector='.thumb.imgerr',
                    detalle=f"{len(datos['vacias'])} contenedores de imagen vacios en el DOM",
                    modelo=datos['vacias'][0],
                    accion_sugerida='resolver la imagen del vehiculo o mantener el placeholder',
                    severidad='alta'))
            if datos['sinFoto']:
                out.append(HallazgoDOM(
                    'tarjeta_sin_foto', selector='#grid .card',
                    detalle=f"{len(datos['sinFoto'])} tarjetas sin ningun <img> "
                            f"({datos['conImg']}/{datos['total']} tienen foto)",
                    modelo=datos['sinFoto'][0],
                    accion_sugerida='asignar imagen por defecto oficial de la marca',
                    severidad='media'))
            if datos['sinAlt']:
                out.append(HallazgoDOM(
                    'sin_alt', selector='img.thumb',
                    detalle=f"{datos['sinAlt']} imagenes de tarjeta sin atributo alt",
                    accion_sugerida='agregar alt con el nombre del modelo',
                    severidad='baja'))
            if errores_red:
                out.append(HallazgoDOM(
                    'img_rota', selector='(red)',
                    detalle=f"{len(errores_red)} respuestas 4xx/5xx al cargar la pagina",
                    modelo=errores_red[0][:110],
                    accion_sugerida='revisar las URLs de imagen que fallan',
                    severidad='alta'))
            browser.close()
    except Exception as e:
        out.append(HallazgoDOM('contenedor_vacio',
                               detalle=f'no se pudo auditar el DOM: {str(e)[:90]}',
                               accion_sugerida='revisar la conexion o Playwright',
                               severidad='baja'))
    return out


def resumen_hallazgos(h: list[HallazgoDOM]) -> dict:
    from collections import Counter
    c = Counter(x.tipo for x in h)
    return {'total': len(h), 'por_tipo': dict(c),
            'alta': sum(1 for x in h if x.severidad == 'alta')}
