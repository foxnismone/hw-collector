#!/usr/bin/env python3
"""El campo 'x' (indice mostrado) habia sido usado como valor en los modelos nuevos.
Si x < 20 (imposible como indice 0-100) se toma de indice_coleccionabilidad.
Ttabla de componentes f (R,D,C,A,M) tambien estaba como valores."""
import json

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def main():
    cat = json.load(open(BASE + 'catalog_web.json', encoding='utf-8'))
    fix_x = fix_f = 0

    for m in cat:
        ind = m.get('indice_coleccionabilidad')
        # x debe ser un indice 0-100
        if not isinstance(m.get('x'), (int,float)) or m['x'] < 20:
            if isinstance(ind, (int,float)):
                m['x'] = round(float(ind), 1); fix_x += 1
            else:
                m['x'] = 45.0; fix_x += 1
        # f son los 5 componentes del indice (0-100 cada uno, A hasta 60)
        f = m.get('f')
        if not isinstance(f, list) or len(f) != 5 or any(not isinstance(v,(int,float)) for v in f):
            d = m.get('indice_detalle') or {}
            m['f'] = [d.get('R',{}).get('v',0), d.get('D',{}).get('v',0),
                      d.get('C',{}).get('v',0), d.get('A',{}).get('v',0), d.get('M',{}).get('v',0)]
            fix_f += 1

    print(f"x reparados: {fix_x}")
    print(f"f reparados: {fix_f}")

    # verificar
    mal_x = sum(1 for m in cat if not isinstance(m.get('x'),(int,float)) or m['x']<20)
    mal_f = sum(1 for m in cat if not isinstance(m.get('f'),list) or len(m['f'])!=5)
    print(f"\nVerificacion: x<20: {mal_x} | f mal: {mal_f}")

    # rango de x
    xs = [m['x'] for m in cat]
    print(f"x: min {min(xs)} | max {max(xs)} | mediana {sorted(xs)[len(xs)//2]}")

    json.dump(cat, open(BASE + 'catalog_web.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
    txt = json.dumps(cat, ensure_ascii=False, separators=(',',':'))
    open('C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/cat.js','w',encoding='utf-8').write('const CAT=' + txt + ';\n')
    print(f"cat.js regenerado ({len(txt)/1024/1024:.1f} MB)")

if __name__ == '__main__':
    main()
