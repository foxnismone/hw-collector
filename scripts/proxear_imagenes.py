#!/usr/bin/env python3
"""Todas las imagenes de Fandom deben ir por el proxy images.weserv.nl.
Fandom bloquea el hotlinking directo (403) -> por eso se veian rotas.
Normaliza 'im' y 'galeria'."""
import json, re

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def prox(u):
    if not u: return ''
    u = str(u).strip()
    if not u: return ''
    if 'images.weserv.nl' in u: return u
    # quitar revision/latest para la original
    u = re.sub(r'/revision/latest/.*$', '', u)
    if u.startswith('https://static.wikia.nocookie.net') or u.startswith('http://static.wikia.nocookie.net'):
        return 'https://images.weserv.nl/?url=' + u.replace('https://','').replace('http://','')
    return u

def main():
    cat = json.load(open(BASE + 'catalog_web.json', encoding='utf-8'))
    fix_im = fix_gal = 0

    for m in cat:
        if m.get('im'):
            n = prox(m['im'])
            if n != m['im']:
                m['im'] = n; fix_im += 1
        gal = m.get('galeria')
        if gal:
            ng = [prox(u) for u in gal]
            if ng != gal:
                m['galeria'] = ng; fix_gal += 1

    print(f"im proxeados: {fix_im}")
    print(f"galerias proxeadas: {fix_gal}")

    # verificar: ninguna URL de Fandom sin proxy
    mal = 0
    for m in cat:
        urls = []
        if m.get('im'): urls.append(m['im'])
        urls.extend(m.get('galeria') or [])
        for u in urls:
            if 'static.wikia' in u and 'weserv' not in u: mal += 1
    print(f"URLs de Fandom SIN proxy restantes: {mal}")

    json.dump(cat, open(BASE + 'catalog_web.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
    txt = json.dumps(cat, ensure_ascii=False, separators=(',',':'))
    open('C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/cat.js','w',encoding='utf-8').write('const CAT=' + txt + ';\n')
    print(f"cat.js regenerado ({len(txt)/1024/1024:.1f} MB)")

if __name__ == '__main__':
    main()
