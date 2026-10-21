#!/usr/bin/env python3
"""Asigna pais de origen a los modelos que no lo tienen, segun epoca y linea."""
import json, re

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

# Paises reales de fabricacion de Hot Wheels por epoca
def pais_de(m):
    y = m.get('y')
    try: y = int(y)
    except Exception: y = 0
    k = (m.get('k') or '').lower()
    s = (m.get('s') or '').lower()
    texto = k + ' ' + s

    # lineas premium modernas: Tailandia
    if any(x in texto for x in ('car culture','boulevard','team transport','pop culture')):
        return 'Thailand'
    if any(x in texto for x in ('red line club','rlc','elite 64','convention')):
        return 'Malaysia'
    if 'super treasure' in texto or 'treasure hunt' in texto:
        return 'Malaysia'

    if y == 0: return 'USA'
    if 1968 <= y <= 1975: return 'USA'
    if 1976 <= y <= 1980: return 'Hong Kong'
    if 1981 <= y <= 1989: return 'Malaysia'
    if 1990 <= y <= 1999: return 'Malaysia'
    if 2000 <= y <= 2004: return 'China'
    if 2005 <= y <= 2010: return 'Malaysia'
    if 2011 <= y <= 2013: return 'Malaysia'
    return 'Malaysia'

def main():
    cat = json.load(open(BASE + 'catalog_web.json', encoding='utf-8'))
    sin = 0
    for m in cat:
        if not m.get('pais'):
            m['pais'] = pais_de(m)
            sin += 1
    print(f"Paises asignados: {sin}")
    print(f"Con pais ahora: {sum(1 for m in cat if m.get('pais'))}/{len(cat)}")

    json.dump(cat, open(BASE + 'catalog_web.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
    txt = json.dumps(cat, ensure_ascii=False, separators=(',',':'))
    open('C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/cat.js','w',encoding='utf-8').write('const CAT=' + txt + ';\n')
    print(f"cat.js regenerado ({len(txt)/1024/1024:.1f} MB)")

if __name__ == '__main__':
    main()
