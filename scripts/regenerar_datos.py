#!/usr/bin/env python3
"""Regenera los archivos JS externos (data/*.js) desde los JSON fuente.
Uso: despues de modificar catalog_web.json / disenadores.json / series_ui.json,
ejecutar este script y hacer commit.
"""
import json, os

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/'
DATA = BASE + 'data/'

PARES = [
    ('catalog_web.json', 'cat.js', 'const CAT='),
    ('disenadores.json', 'disenadores.js', 'DISENADORES='),
    ('series_ui.json', 'series.js', 'const SERIES='),
]

def main():
    for origen, destino, prefijo in PARES:
        p = DATA + origen
        if not os.path.exists(p):
            print(f"  {origen}: NO EXISTE (se omite)")
            continue
        datos = json.load(open(p, encoding='utf-8'))
        if isinstance(datos, dict) and 'items' in datos and origen == 'series_ui.json':
            datos = datos['items']
        txt = prefijo + json.dumps(datos, ensure_ascii=False, separators=(',',':')) + ';\n'
        open(DATA + destino, 'w', encoding='utf-8').write(txt)
        print(f"  {destino}: {len(datos)} elementos ({len(txt)/1024/1024:.1f} MB)")

    # ruedas
    for cand in ['wheeltypes_reales.json', 'ruedas.json', 'wheeltypes.json', 'tipos_ruedas.json']:
        p = DATA + cand
        if os.path.exists(p):
            datos = json.load(open(p, encoding='utf-8'))
            txt = 'const WHEELTYPES=' + json.dumps(datos, ensure_ascii=False, separators=(',',':')) + ';\n'
            open(DATA + 'ruedas.js', 'w', encoding='utf-8').write(txt)
            print(f"  ruedas.js: {len(datos)} elementos ({len(txt)/1024/1024:.1f} MB)  <- {cand}")
            break
    else:
        print("  ruedas.js: no se encontro fuente (se conserva el existente)")

if __name__ == '__main__':
    main()
