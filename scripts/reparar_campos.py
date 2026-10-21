#!/usr/bin/env python3
"""Repara campos null del catalogo que rompen el JS (toFixed sobre null, etc).
- v/V/x/px nunca null (toFixed los usa)
- y nunca null (se muestra directo)
- c/t/s/n nunca vacios que rompan
"""
import json

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def main():
    cat = json.load(open(BASE + 'catalog_web.json', encoding='utf-8'))
    fix_v = fix_y = fix_x = fix_px = 0

    for m in cat:
        # v y V deben ser numeros
        if m.get('v') is None or not isinstance(m.get('v'), (int, float)):
            m['v'] = 9.99; fix_v += 1
        if m.get('V') is None or not isinstance(m.get('V'), (int, float)):
            m['V'] = round(float(m['v']) * 2, 2)
            fix_v += 1
        if m['V'] < m['v']:
            m['V'] = round(float(m['v']) * 2, 2)
        # x debe ser numero
        if m.get('x') is None or not isinstance(m.get('x'), (int, float)):
            m['x'] = 45.0; fix_x += 1
        # px
        if m.get('px') is None or not isinstance(m.get('px'), (int, float)):
            m['px'] = 12; fix_px += 1
        # y nunca null
        if m.get('y') is None:
            m['y'] = 2020; fix_y += 1
        # campos de texto
        for k in ('m','t','c','s','n','k'):
            if m.get(k) is None: m[k] = ''
        # ficha siempre objeto
        if not isinstance(m.get('ficha'), dict):
            m['ficha'] = {'descripcion': '', 'historia': '', 'curiosidades': '', 'conmemorativo': False, 'dato_clave': ''}

    print(f"v/V reparados: {fix_v}")
    print(f"x reparados: {fix_x}")
    print(f"px reparados: {fix_px}")
    print(f"y reparados: {fix_y}")

    # Verificar
    mal_v = sum(1 for m in cat if not isinstance(m.get('v'), (int,float)))
    mal_V = sum(1 for m in cat if not isinstance(m.get('V'), (int,float)))
    mal_x = sum(1 for m in cat if not isinstance(m.get('x'), (int,float)))
    mal_y = sum(1 for m in cat if m.get('y') is None)
    print(f"\nVerificacion: v={mal_v} V={mal_V} x={mal_x} y={mal_y}")

    json.dump(cat, open(BASE + 'catalog_web.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
    txt = json.dumps(cat, ensure_ascii=False, separators=(',',':'))
    open('C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/cat.js','w',encoding='utf-8').write('const CAT=' + txt + ';\n')
    print(f"cat.js regenerado ({len(txt)/1024/1024:.1f} MB)")

if __name__ == '__main__':
    main()
