#!/usr/bin/env python3
"""Deduplica IDs (IDX[id] se sobrescribia y el clic abria el equivocado),
arregla modelos sin nombre y normaliza campos de texto."""
import json
from collections import Counter

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def main():
    cat = json.load(open(BASE + 'catalog_web.json', encoding='utf-8'))
    antes = len(cat)

    # 1. deduplicar IDs
    vistos = {}
    dup = 0
    for m in cat:
        pid = str(m.get('i'))
        if pid in vistos:
            vistos[pid] += 1
            m['i'] = f"{pid}-{vistos[pid]}"
            dup += 1
        else:
            vistos[pid] = 1
    print(f"IDs deduplicados: {dup}")

    # 2. modelos sin nombre
    sin_nombre = 0
    for m in cat:
        if not m.get('m') or not str(m.get('m')).strip():
            # usar toy o serie como nombre
            nombre = str(m.get('t') or m.get('s') or m['i'])
            m['m'] = nombre
            sin_nombre += 1
        # limpiar espacios
        m['m'] = str(m.get('m','')).strip()
    print(f"Nombres arreglados: {sin_nombre}")

    # 3. normalizar campos de texto (nunca None)
    for m in cat:
        for k in ('t','c','s','n','k','pais','im'):
            if m.get(k) is None: m[k] = ''
        # im: si esta vacio, quitar la clave para que no muestre roto
        if m.get('im') == '': m.pop('im', None)

    # verificar
    ids = Counter(str(m.get('i')) for m in cat)
    dup2 = {k:v for k,v in ids.items() if v>1}
    print(f"IDs duplicados restantes: {len(dup2)}")
    sin_nom = sum(1 for m in cat if not str(m.get('m','')).strip())
    print(f"Sin nombre restantes: {sin_nom}")
    sin_im = sum(1 for m in cat if not m.get('im'))
    print(f"Sin imagen: {sin_im}")

    json.dump(cat, open(BASE + 'catalog_web.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
    txt = json.dumps(cat, ensure_ascii=False, separators=(',',':'))
    open('C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/cat.js','w',encoding='utf-8').write('const CAT=' + txt + ';\n')
    print(f"cat.js regenerado ({len(txt)/1024/1024:.1f} MB)")
    print(f"Modelos: {antes} -> {len(cat)}")

if __name__ == '__main__':
    main()
