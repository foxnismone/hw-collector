#!/usr/bin/env python3
"""Extrae URLs REALES de fotos de diseñadores usando la API de Fandom (pageimages)."""
import json, urllib.request, urllib.parse, time

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def api(params):
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (hotwheels-research)')
    req.add_header('Referer', 'https://hotwheels.fandom.com/')
    for intento in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            time.sleep(1.5 * (intento + 1))
    return None

def main():
    with open(BASE + 'disenadores.json', encoding='utf-8') as f:
        dis = json.load(f)

    nombres = list(dis.keys())
    print(f"Extrayendo fotos reales de {len(nombres)} diseñadores...")

    fotos_reales = {}
    # Batches de 50 títulos
    for i in range(0, len(nombres), 50):
        batch = nombres[i:i+50]
        data = api({
            'action': 'query',
            'titles': '|'.join(batch),
            'prop': 'pageimages',
            'piprop': 'thumbnail',
            'pithumbsize': '300',
            'redirects': '1',
            'format': 'json',
            'formatversion': '2'
        })
        if not data:
            print(f"  Batch {i//50+1}: ERROR")
            continue
        pages = data.get('query', {}).get('pages', [])
        for p in pages:
            titulo = p.get('title', '')
            thumb = p.get('thumbnail', {}).get('source', '')
            if thumb and titulo:
                fotos_reales[titulo] = thumb
        print(f"  Batch {i//50+1}: {len(pages)} páginas, {len(fotos_reales)} fotos acumuladas")
        time.sleep(0.3)

    # Aplicar fotos reales
    aplicadas = 0
    for nombre, d in dis.items():
        if nombre in fotos_reales:
            url = fotos_reales[nombre]
            d['foto'] = 'https://images.weserv.nl/?url=' + url.replace('https://', '')
            aplicadas += 1

    with open(BASE + 'disenadores.json', 'w', encoding='utf-8') as f:
        json.dump(dis, f, ensure_ascii=False, indent=2)

    print(f"\nFotos reales aplicadas: {aplicadas}/{len(dis)}")

    # Guardar mapa
    with open(BASE + 'fotos_reales_api.json', 'w', encoding='utf-8') as f:
        json.dump(fotos_reales, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
