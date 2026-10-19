#!/usr/bin/env python3
"""Resuelve las imágenes rotas restantes buscando en el namespace de archivos de Fandom."""
import json, urllib.request, urllib.parse, time, os, re

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/'

def api(params):
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (hotwheels-research)')
    req.add_header('Referer', 'https://hotwheels.fandom.com/')
    for intento in range(2):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception:
            time.sleep(1)
    return None

def resolver_por_archivo(fname):
    """Busca un archivo por nombre en Fandom y devuelve su URL"""
    # Limpiar nombre
    base_name = re.sub(r'\.(jpg|jpeg|png|webp|gif)$', '', fname, flags=re.I)
    base_name = base_name.replace('_', ' ')
    # Buscar en namespace 6 (File)
    data = api({
        'action': 'query', 'list': 'search', 'srnamespace': '6',
        'srsearch': base_name, 'srlimit': '3', 'format': 'json', 'formatversion': '2'
    })
    if not data:
        return None
    results = data.get('query', {}).get('search', [])
    for r in results:
        titulo = r.get('title', '')  # "File:Nombre.jpg"
        # Obtener URL
        info = api({
            'action': 'query', 'titles': titulo, 'prop': 'imageinfo',
            'iiprop': 'url', 'format': 'json', 'formatversion': '2'
        })
        if info:
            pages = info.get('query', {}).get('pages', [])
            for p in pages:
                ii = p.get('imageinfo', [])
                if ii and ii[0].get('url'):
                    return ii[0]['url']
    return None

def main():
    with open(BASE + 'data/catalog_web.json', encoding='utf-8') as f:
        cat = json.load(f)

    rotas = [m for m in cat if m.get('im') and not m['im'].startswith('http') and not os.path.exists(BASE + 'img/' + m['im'])]
    print(f"Rotas a resolver: {len(rotas)}")

    resueltas = 0
    for m in rotas:
        fname = m['im']
        url = resolver_por_archivo(fname)
        if url:
            m['im'] = 'https://images.weserv.nl/?url=' + url.replace('https://', '')
            m['imr'] = 1
            resueltas += 1
        else:
            m['im'] = ''  # Marcar como sin imagen
        if resueltas % 10 == 0 and resueltas > 0:
            with open(BASE + 'data/catalog_web.json', 'w', encoding='utf-8') as f:
                json.dump(cat, f, ensure_ascii=False, separators=(',', ':'))
        time.sleep(0.15)

    with open(BASE + 'data/catalog_web.json', 'w', encoding='utf-8') as f:
        json.dump(cat, f, ensure_ascii=False, separators=(',', ':'))

    faltan = sum(1 for m in cat if m.get('im') and not m['im'].startswith('http') and not os.path.exists(BASE + 'img/' + m['im']))
    con_img = sum(1 for m in cat if m.get('im'))
    print(f"\nResueltas por búsqueda: {resueltas}")
    print(f"Rotas restantes: {faltan}")
    print(f"Con imagen: {con_img}/{len(cat)}")

if __name__ == '__main__':
    main()
