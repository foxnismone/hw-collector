import json
base = '.'
cat = json.load(open('data/catalog_web.json', encoding='utf-8'))

# Todos los recursos graficos que YA existen (img local o URL valida)
existe_imagen = [m for m in cat if m.get('im') or m.get('galeria')]
sin_imagen = [m for m in cat if not m.get('im') and not m.get('galeria')]

print(f"=== TOTAL: {len(cat)} modelos ===")
print(f"Con imagen  (im o galeria): {len(existe_imagen)}")
print(f"Sin imagen: {len(sin_imagen)}")
print()

# ¿hay alguna imagen ya descargada localmente que coincida en nombre?
import os
archivos_locales = set()
if os.path.isdir('img'):
    for root, dirs, files in os.walk('img'):
        for f in files:
            nombre_base = os.path.splitext(f)[0]
            archivos_locales.add(nombre_base.lower())

# Chequear si los archivos .webp referenciados existen
refs_webp = 0
refs_webp_ok = 0
for m in cat:
    if m.get('im') and str(m['im']).endswith('.webp'):
        refs_webp += 1
        path = os.path.join('img', str(m['im']))
        if os.path.exists(path):
            refs_webp_ok += 1

print(f"Refs .webp en catalogo: {refs_webp}, de las cuales {refs_webp_ok} existen en img/")
print()

# Modelos sin imagen pero con galeria parcial
print("=== sin im pero con galeria ===")
parcial = [m for m in cat if not m.get('im') and m.get('galeria')]
print(f"  {len(parcial)} modelos")
for m in parcial[:5]:
    print(f"  {m.get('m')[:40]}  galeria: {len(m.get('galeria') or [])}")
print()

# Modelos sin imagen ni galeria - por categoria
from collections import Counter
print("=== sin im ni galeria (las 137) ===")
sin_nada = [m for m in cat if not m.get('im') and not m.get('galeria')]
c = Counter(m.get('k','?') for m in sin_nada)
for k, n in c.most_common():
    print(f"  {k:25} {n}")

# Modelos JRP (2027) sin imagen - los de la captura
print()
print("=== modelos JRP sin imagen (los de la captura) ===")
jrp = [m for m in sin_imagen if str(m.get('t','')).startswith('JRP')]
print(f"  {len(jrp)} modelos JRP")
for m in jrp[:8]:
    print(f"  {m.get('m')[:40]:42} {m.get('k','')[:16]}  y={m.get('y')} Toy#{m.get('t')}")
