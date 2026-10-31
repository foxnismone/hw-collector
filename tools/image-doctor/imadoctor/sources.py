#!/usr/bin/env python3
"""Fuentes de candidatos para el flujo 3.

Orden de preferencia (de mas fiel a menos fiel):
  1. cache local img/        -> coincidencia de nombre de archivo
  2. API de Fandom           -> File: namespace + pageimages del casting
  3. busqueda web            -> DuckDuckGo HTML (sin API key)

Cada fuente es independiente: si una no responde, las demas siguen funcionando.
"""
from __future__ import annotations
import json, os, re, time, urllib.parse, urllib.request, urllib.error, hashlib
from typing import Callable

from .config import Config, DEFAULT
from .context import _limpiar

UA_BROWSER = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')


# ---------------------------------------------------------------- cache local
def _cache_index(img_dir: str) -> dict[str, str]:
    """nombre_limpio -> ruta absoluta, para busquedas instantaneas."""
    idx: dict[str, str] = {}
    if not os.path.isdir(img_dir):
        return idx
    for root, _d, files in os.walk(img_dir):
        for fn in files:
            base = os.path.splitext(fn)[0]
            clave = _limpiar(base).lower()
            if clave and clave not in idx:
                idx[clave] = os.path.join(root, fn)
    return idx


def desde_cache_local(query: str, cfg: Config) -> list[str]:
    """Busca en img/ un archivo cuyo nombre coincida con la consulta."""
    idx = _cache_index(cfg.img_dir)
    if not idx:
        return []
    q = _limpiar(query).lower()
    if not q:
        return []
    out = []
    # coincidencia exacta primero
    if q in idx:
        out.append('file:///' + idx[q].replace('\\', '/'))
    # luego contencion
    for clave, ruta in idx.items():
        if q in clave or clave in q:
            u = 'file:///' + ruta.replace('\\', '/')
            if u not in out:
                out.append(u)
    return out[:5]


# ---------------------------------------------------------------- Fandom
def _fandom(params: dict, cfg: Config, intentos: int = 3) -> dict:
    """Llama a la API de Fandom con reintentos y manejo de errores."""
    url = cfg.fandom_api + '?' + urllib.parse.urlencode(params)
    for i in range(intentos):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', cfg.ua)
            req.add_header('Referer', 'https://hotwheels.fandom.com/')
            with urllib.request.urlopen(req, timeout=cfg.timeout) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 429:                     # rate limit: esperar y reintentar
                time.sleep(2.0 * (i + 1))
                continue
            if i == intentos - 1:
                return {'_error': f'HTTP {e.code}'}
        except Exception as e:
            if i == intentos - 1:
                return {'_error': str(e)[:80]}
            time.sleep(1.0)
    return {'_error': 'sin respuesta'}


def _norm_ext(u: str) -> str:
    """Fandom devuelve a veces URLs sin extension; infiere la correcta."""
    if re.search(r'\.(jpe?g|png|webp|gif|svg)(\?|$)', u, re.I):
        return u
    return u + '.jpg'


def desde_fandom(query: str, cfg: Config, limite: int = 8) -> list[str]:
    """Busca archivos en el namespace File: de la wiki."""
    resultados: list[str] = []

    # 1) busqueda directa en File:
    d = _fandom({
        'action': 'query', 'format': 'json',
        'generator': 'search', 'gsrsearch': f'File:{query}', 'gsrnamespace': 6,
        'gsrlimit': 12,
        'prop': 'imageinfo', 'iiprop': 'url|size|mime', 'iilimit': 1,
    }, cfg)
    for p in (d.get('query') or {}).get('pages') or {}:
        pagina = ((d.get('query') or {}).get('pages') or {})[p]
        for ii in pagina.get('imageinfo') or []:
            if ii.get('mime', '').startswith('image/') and ii.get('url'):
                resultados.append(_norm_ext(ii['url']))

    # 2) solo si File: no devolvio nada (ahorra 2 llamadas API por query; el
    #    rate limit de Fandom es 200/5min, asi que cada llamada cuenta)
    if not resultados:
        d2 = _fandom({
            'action': 'query', 'format': 'json', 'redirects': 1,
            'titles': query, 'prop': 'pageimages', 'piprop': 'original|thumbnail',
            'pithumbsize': 600,
        }, cfg)
        for p in ((d2.get('query') or {}).get('pages') or {}).values():
            pi = p.get('pageimage') or p.get('thumbnail') or {}
            u = pi.get('original') if isinstance(pi, dict) else None
            u = u or (p.get('thumbnail') or {}).get('source')
            if u and u not in resultados:
                resultados.append(_norm_ext(u))

    # 3) solo si File: no devolvio nada
    if not resultados:
        d3 = _fandom({
            'action': 'query', 'format': 'json', 'redirects': 1,
            'titles': query, 'prop': 'images', 'imlimit': 20,
        }, cfg)
        for p in ((d3.get('query') or {}).get('pages') or {}).values():
            for img in p.get('images') or []:
                t = (img.get('title') or '').lower()
                if any(k in t for k in ('loose', 'card', 'blister', 'base', 'hw')):
                    u = (d3.get('query') or {}).get('pages')
                # resolver la URL del archivo listado
                d4 = _fandom({'action': 'query', 'format': 'json',
                              'titles': img.get('title'),
                              'prop': 'imageinfo', 'iiprop': 'url'}, cfg)
                for p4 in ((d4.get('query') or {}).get('pages') or {}).values():
                    for ii in p4.get('imageinfo') or []:
                        if ii.get('url'):
                            resultados.append(_norm_ext(ii['url']))

    # deduplicar y limitar
    vistos, out = set(), []
    for u in resultados:
        clave = u.split('?')[0]
        if clave in vistos:
            continue
        vistos.add(clave)
        out.append(u)
    return out[:limite]


# ---------------------------------------------------------------- web
DDG_RE = re.compile(r'uddg=([^&"]+)')


def desde_web(query: str, cfg: Config, limite: int = 8) -> list[str]:
    """Busca imagenes por web usando DuckDuckGo HTML (sin API key)."""
    out: list[str] = []
    try:
        url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(
            f'{query} hot wheels diecast')
        req = urllib.request.Request(url)
        req.add_header('User-Agent', UA_BROWSER)
        req.add_header('Accept', 'text/html')
        with urllib.request.urlopen(req, timeout=cfg.timeout) as r:
            html = r.read(400000).decode('utf-8', 'ignore')
        for m in DDG_RE.finditer(html):
            try:
                u = urllib.parse.unquote(m.group(1))
            except Exception:
                continue
            if not u.startswith('http'):
                continue
            low = u.lower().split('?')[0]
            if not low.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                continue
            if any(d in u for d in ('wikimedia', 'wikipedia.org/wiki')):
                continue
            if u not in out:
                out.append(u)
            if len(out) >= limite * 2:
                break
    except Exception:
        pass
    return out[:limite]


# ---------------------------------------------------------------- orquestador
def buscar_candidatos(query: str, cfg: Config = DEFAULT) -> list[str]:
    """Une todas las fuentes para una consulta, en orden de fiabilidad."""
    if not query or len(query.strip()) < 3:
        return []
    candidatos: list[str] = []
    vistos = set()

    def add(urls):
        for u in urls:
            clave = u.split('?')[0]
            if clave in vistos:
                continue
            vistos.add(clave)
            candidatos.append(u)

    add(desde_cache_local(query, cfg))
    add(desde_fandom(query, cfg))
    if len(candidatos) < 4:
        add(desde_web(query, cfg))
    return candidatos


def buscar_multiples(queries: list[str], cfg: Config = DEFAULT) -> list[str]:
    """Recorre las consultas del plan hasta juntar candidatos suficientes."""
    todos: list[str] = []
    vistos = set()
    for q in queries:
        for u in buscar_candidatos(q, cfg):
            clave = u.split('?')[0]
            if clave in vistos:
                continue
            vistos.add(clave)
            todos.append(u)
        if len(todos) >= 12:
            break
    return todos
