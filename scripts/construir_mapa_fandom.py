#!/usr/bin/env python3
"""Construye el MAPA DE ÍNDICES de Fandom:
  - todas las páginas 'List of XXXX Hot Wheels' (árbol cronológico)
  - todas las páginas de 'Category:Hot Wheels by Series' (árbol categórico)
Guarda data/mapa_fandom.json con las listas para scraping incremental.
"""
import json, urllib.request, urllib.parse, time, re

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def api(params, intentos=3):
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (hotwheels-research)')
    req.add_header('Referer','https://hotwheels.fandom.com/')
    for i in range(intentos):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception:
            time.sleep(1.5*(i+1))
    return None

def todos_los_miembros(titulo_categoria):
    """Pagina todos los miembros de una categoría."""
    out = []
    cmcontinue = None
    while True:
        p = {'action':'query','list':'categorymembers','cmtitle':titulo_categoria,
             'cmlimit':'500','cmtype':'page','format':'json'}
        if cmcontinue: p['cmcontinue'] = cmcontinue
        r = api(p)
        if not r or 'query' not in r: break
        out.extend(m['title'] for m in r['query']['categorymembers'])
        cmcontinue = r.get('continue',{}).get('cmcontinue')
        if not cmcontinue: break
        time.sleep(0.3)
    return out

def main():
    print("=== Árbol cronológico ===")
    lista_anios = todos_los_miembros('Category:Lists of Hot Wheels by year')
    print(f"  {len(lista_anios)} páginas")

    print("=== Árbol categórico (series) ===")
    series = todos_los_miembros('Category:Hot Wheels by Series')
    print(f"  {len(series)} páginas")

    # Subcategorías de series (Mainline Segment, Premium, etc.)
    r = api({'action':'query','list':'categorymembers','cmtitle':'Category:Hot Wheels by Series',
             'cmlimit':'500','cmtype':'subcat','format':'json'})
    subcats = [m['title'] for m in r['query']['categorymembers']] if r and 'query' in r else []
    print(f"\n  Subcategorías: {len(subcats)}")
    for s in subcats[:20]:
        print(f"    {s}")

    # Expandir subcategorías
    sub_paginas = {}
    for sc in subcats:
        miembros = todos_los_miembros(sc)
        sub_paginas[sc] = miembros
        print(f"    {sc}: {len(miembros)}")

    mapa = {
        'cronologico': sorted(lista_anios),
        'series_directas': sorted(series),
        'subcategorias': {k: sorted(v) for k, v in sub_paginas.items()},
        'fecha': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    json.dump(mapa, open(BASE + 'mapa_fandom.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
    total = len(lista_anios) + len(series) + sum(len(v) for v in sub_paginas.values())
    print(f"\nTotal páginas en mapa: {total}")
    print(f"Guardado: data/mapa_fandom.json")

if __name__ == '__main__':
    main()
