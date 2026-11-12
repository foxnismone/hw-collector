#!/usr/bin/env python3
"""Busca fotos reales en Fandom para los modelos sin imagen.

Estrategia: para cada modelo sin im, buscar:
  1) su pagina de casting por nombre (pageimages + imágenes)
  2) su toy number (JRPxx) como título alternativo
  3) archivos File: que coincidan con el nombre
Descarta el placeholder 'Image_Not_Available' y reporta solo URLs reales.
"""
import json, urllib.request, urllib.parse, time, sys, os

sys.path.insert(0, 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/tools/image-doctor')
from imadoctor.config import Config

cfg = Config()
UAS = cfg.ua

def fandom(params, retries=2, delay=1.0):
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    for i in range(retries):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', UAS)
            req.add_header('Referer', 'https://hotwheels.fandom.com/')
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            if i == retries - 1:
                return {'_error': str(e)[:80]}
            time.sleep(delay * (i + 1))
    return {'_error': 'timeout'}

def obtener_imagen_real(nombre, toy_num):
    """Devuelve (url, fuente) si encuentra una foto real, o (None, razon)."""
    titulo = nombre

    # 1) pageimages del casting (foto principal de la pagina)
    d = fandom({'action': 'query', 'format': 'json', 'redirects': 1, 'titles': titulo,
                'prop': 'pageimages', 'piprop': 'original'})
    pages = (d.get('query') or {}).get('pages') or {}
    for p in pages.values():
        orig = p.get('original') or {}
        src = orig.get('source', '')
        if src and 'Image_Not_Available' not in src.upper() and orig.get('width', 0) > 100:
            return src, 'pageimages del casting'
        # tambien revisar si existen imágenes listadas
        pid = p.get('pageid')
        if pid:
            d2 = fandom({'action': 'query', 'format': 'json', 'pageids': pid,
                         'prop': 'images', 'imlimit': 30})
            for p2 in (d2.get('query') or {}).get('pages', {}).values():
                for img in p2.get('images') or []:
                    t = img.get('title', '')
                    if 'Not_Available' in t or 'Image_Not' in t:
                        continue
                    # resolver la URL real del archivo
                    d3 = fandom({'action': 'query', 'format': 'json', 'titles': t,
                                 'prop': 'imageinfo', 'iiprop': 'url|mime|size'})
                    for p3 in (d3.get('query') or {}).get('pages', {}).values():
                        for ii in p3.get('imageinfo') or []:
                            u = ii.get('url', '')
                            if u and ii.get('mime', '').startswith('image/'):
                                return u, 'imagen de la pagina (' + os.path.basename(t) + ')'

    # 2) buscar archivo File: con el nombre del modelo
    d4 = fandom({'action': 'query', 'format': 'json', 'list': 'search', 'srnamespace': 6,
                 'srsearch': titulo, 'srlimit': 10})
    for h in (d4.get('query') or {}).get('search') or []:
        t = h.get('title', '')
        if 'Not_Available' in t:
            continue
        d5 = fandom({'action': 'query', 'format': 'json', 'titles': t,
                     'prop': 'imageinfo', 'iiprop': 'url|mime|size'})
        for p5 in (d5.get('query') or {}).get('pages', {}).values():
            for ii in p5.get('imageinfo') or []:
                u = ii.get('url', '')
                if u and (ii.get('mime', '').startswith('image/') or u.lower().endswith(('.jpg', '.png'))):
                    return u, 'File: ' + os.path.basename(t)

    # 3) por toy number
    if toy_num:
        d6 = fandom({'action': 'query', 'format': 'json', 'titles': toy_num,
                     'prop': 'pageimages', 'piprop': 'original'})
        pages = (d6.get('query') or {}).get('pages') or {}
        for p6 in pages.values():
            if p6.get('missing') is not False and not p6.get('pageid'):
                continue
            src = (p6.get('original') or {}).get('source', '')
            if src and 'Image_Not_Available' not in src.upper():
                return src, 'pageimages por toy number ' + toy_num

    return None, 'no hay foto en Fandom'

# --- los modelos JRP de la captura ---
cat = json.load(open(os.path.join(cfg.data, 'catalog_web.json'), encoding='utf-8'))
jrp = [m for m in cat if str(m.get('t', '')).startswith('JRP') and not m.get('im')]
print(f"Modelos JRP sin imagen: {len(jrp)}")
print()

resultados = []
for m in jrp:
    nombre = m.get('m', '')
    toy = m.get('t', '')
    url, fuente = obtener_imagen_real(nombre, toy)
    estado = 'ENCONTRADA' if url else 'FALTA'
    print(f"  [{estado}] {nombre[:38]:40} {toy:8} {fuente[:50] if url else ''}")
    if url:
        print(f"          {url[:110]}")
        resultados.append({'nombre': nombre, 'toy': toy, 'url': url, 'fuente': fuente})
    time.sleep(0.3)

print(f"\n>>> Total fotos encontradas: {len(resultados)}/{len(jrp)}")
# guardar para usar luego
with open(os.path.join(cfg.cache_dir, 'jrp_fotos_encontradas.json'), 'w', encoding='utf-8') as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)
print("guardado en cache/jrp_fotos_encontradas.json")
