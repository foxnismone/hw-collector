#!/usr/bin/env python3
"""Resuelve las imágenes locales rotas del catálogo usando la API de Fandom."""
import json, urllib.request, urllib.parse, time, os

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

def main():
    with open(BASE + 'data/catalog_web.json', encoding='utf-8') as f:
        cat = json.load(f)

    # Identificar rotas
    rotas = []
    for m in cat:
        im = m.get('im', '')
        if im and not im.startswith('http') and not os.path.exists(BASE + 'img/' + im):
            rotas.append(m)

    print(f"Imágenes rotas: {len(rotas)}")

    # Resolver por nombre de modelo (pageimages)
    resueltas = 0
    for i in range(0, len(rotas), 50):
        batch = rotas[i:i+50]
        titulos = [m.get('m', '').strip() for m in batch]
        data = api({
            'action': 'query', 'titles': '|'.join(titulos),
            'prop': 'pageimages', 'piprop': 'thumbnail', 'pithumbsize': '300',
            'redirects': '1', 'format': 'json', 'formatversion': '2'
        })
        if not data:
            continue
        pages = data.get('query', {}).get('pages', [])
        # Mapear título -> thumbnail
        thumbs = {}
        for p in pages:
            t = p.get('title', '')
            th = p.get('thumbnail', {}).get('source', '')
            if th:
                thumbs[t.lower()] = th
        for m in batch:
            nombre = m.get('m', '').strip().lower()
            if nombre in thumbs:
                url = thumbs[nombre]
                m['im'] = 'https://images.weserv.nl/?url=' + url.replace('https://', '')
                m['imr'] = 1  # referencia del casting
                resueltas += 1
        print(f"  Batch {i//50+1}: {resueltas} resueltas acumuladas")
        time.sleep(0.3)

    with open(BASE + 'data/catalog_web.json', 'w', encoding='utf-8') as f:
        json.dump(cat, f, ensure_ascii=False, separators=(',', ':'))

    # Verificar
    faltan = sum(1 for m in cat if m.get('im') and not m['im'].startswith('http') and not os.path.exists(BASE + 'img/' + m['im']))
    print(f"\nResueltas: {resueltas}")
    print(f"Rotas restantes: {faltan}")

if __name__ == '__main__':
    main()
