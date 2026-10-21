#!/usr/bin/env python3
"""Normaliza y amplia las categorias (c.k) del catalogo.
Mapea por c.k actual y por la serie (c.s) para cubrir todas las lineas."""
import json, re

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

# Mapeo por serie (c.s) -> categoria normalizada
MAPA_SERIE = [
    (r'super treasure', 'SUPER TREASURE HUNT'),
    (r'treasure hunt', 'TREASURE HUNT'),
    (r'car culture', 'CAR CULTURE'),
    (r'boulevard', 'BOULEVARD'),
    (r'pop culture', 'POP CULTURE'),
    (r'team transport', 'TEAM TRANSPORT'),
    (r'retro entertainment', 'RETRO ENTERTAINMENT'),
    (r'red line club|\brlc\b', 'RLC · RED LINE CLUB'),
    (r'elite 64', 'ELITE 64'),
    (r'convention', 'CONVENTION'),
    (r'first edition', 'FIRST EDITIONS'),
    (r'new model', 'NEW MODELS'),
    (r'mystery', 'MYSTERY MODELS'),
    (r'crack.?up', 'CRACK-UPS'),
    (r'ultra hot', 'ULTRA HOTS'),
    (r'real rider', 'REAL RIDERS'),
    (r'color shifter', 'COLOR SHIFTERS'),
    (r'color reveal|color changer', 'COLOR SHIFTERS'),
    (r'redline', 'REDLINE'),
    (r'100% hot wheels', '100% HOT WHEELS'),
    (r'monster truck', 'MONSTER TRUCKS'),
    (r'sizzler', 'SIZZLERS'),
    (r'starship', 'STARSHIPS'),
    (r'flying colors', 'FLYING COLORS'),
    (r' Zamac', 'ZAMAC'),
]

def categoria_de(m):
    s = (m.get('s') or '') + ' ' + (m.get('k') or '')
    sl = s.lower()
    for patron, cat in MAPA_SERIE:
        if re.search(patron, sl, re.I):
            return cat
    # por c.k
    k = (m.get('k') or '').lower()
    if 'gran escala' in k: return 'GRAN ESCALA'
    if 'vintage' in k or 'clasica' in k: return 'VINTAGE'
    if 'special' in k: return 'SPECIAL & EARLY'
    if 'collector' in k: return 'COLLECTOR EXCLUSIVES'
    if 'mystery' in k: return 'MYSTERY MODELS'
    return 'MAINLINE'

def main():
    cat = json.load(open(BASE + 'catalog_web.json', encoding='utf-8'))
    from collections import Counter
    antes = Counter(m.get('k','') for m in cat)

    for m in cat:
        m['k'] = categoria_de(m)

    despues = Counter(m.get('k','') for m in cat)
    print(f"Categorias antes: {len(antes)} -> despues: {len(despues)}")
    print("\nCategorias (top 30):")
    for k,v in despues.most_common(30):
        print(f"  {v:6d}  {k}")

    json.dump(cat, open(BASE + 'catalog_web.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
    txt = json.dumps(cat, ensure_ascii=False, separators=(',',':'))
    open('C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/cat.js','w',encoding='utf-8').write('const CAT=' + txt + ';\n')
    print(f"\ncat.js regenerado ({len(txt)/1024/1024:.1f} MB)")

if __name__ == '__main__':
    main()
