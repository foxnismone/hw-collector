import json, re
cat = json.load(open('data/catalog_web.json', encoding='utf-8'))

# 1. cuantos tienen "Not Available" en la imagen
ina = [m for m in cat if 'not available' in str(m.get('im','')).lower() or 'no_image' in str(m.get('im','')).lower() or 'imagen_no' in str(m.get('im','')).lower()]
print(f"Modelos con imagen 'Not Available': {len(ina)}")
for m in ina[:8]:
    print(f"  {m['m'][:40]:42s} im={m['im'][:75]}")

# 2. Ver el formato exacto
print("\n=== Formatos de 'not available' ===")
import collections
pats = collections.Counter()
for m in ina:
    u = str(m.get('im',''))
    if 'hotwheels.fandom.com/wiki/Special:FilePath' in u: pats['fandom FilePath'] += 1
    elif 'static.wikia' in u: pats['static.wikia'] += 1
    elif u.startswith('http'): pats['otra http'] += 1
    else: pats['otro'] += 1
print(pats)

# 3. Ejemplos de URL
print("\n=== URLs de ejemplo ===")
for m in ina[:5]:
    print(f"  {m['im']}")
