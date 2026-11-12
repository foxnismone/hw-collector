#!/usr/bin/env python3
"""Chequeo exhaustivo: recorre el HTML y extrae c.\* usados en templates,
y verifica que NINGUNO sea null/undefined en el catalogo.
"""
import json, re, os

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/'
html = open(BASE + 'index.html', encoding='utf-8').read()
cat = json.load(open(BASE + 'data/catalog_web.json', encoding='utf-8'))

# Campos usados como c.algo en el HTML
campos = set(re.findall(r'\bc\.([a-zA-Z_][a-zA-Z0-9_]*)', html))
print(f"Campos 'c.*' usados en el HTML: {len(campos)}")
print(" ", sorted(campos))

# Verificar null/None por campo
print("\n=== NULL POR CAMPO ===")
problemas = {}
for campo in sorted(campos):
    nulos = sum(1 for m in cat if m.get(campo) is None)
    vacios = sum(1 for m in cat if m.get(campo) == '')
    if nulos or vacios:
        problemas[campo] = (nulos, vacios)
        print(f"  {campo}: null={nulos} vacios={vacios}")

if not problemas:
    print("  (ninguno)")

# Tipos de cada campo
print("\n=== TIPOS ===")
for campo in sorted(campos):
    tipos = set(type(m.get(campo)).__name__ for m in cat[:2000])
    print(f"  {campo}: {tipos}")

# Especificamente: campos numericos usados con toFixed/aritmetica
print("\n=== CAMPOS NUMERICOS (toFixed/op matematica) ===")
for campo in ['x','v','V','px']:
    malos = [m['i'] for m in cat if not isinstance(m.get(campo), (int,float))]
    print(f"  {campo}: {len(malos)} no-numericos")
    if malos: print(f"    ej: {malos[:3]}")

# Imagenes
print("\n=== IMAGENES ===")
sin_im = sum(1 for m in cat if not m.get('im'))
print(f"  Sin im: {sin_im}")
tipos_im = {}
for m in cat:
    i = str(m.get('im',''))
    if i.startswith('packs_culture/'): t='local'
    elif 'images.weserv.nl' in i: t='weserv'
    elif 'static.wikia' in i: t='fandom-url'
    elif i.startswith('http'): t='otra-url'
    elif i: t='otro'
    else: t='vacio'
    tipos_im[t] = tipos_im.get(t,0)+1
print(f"  Tipos: {tipos_im}")

# Fichas
print("\n=== FICHAS ===")
malas = sum(1 for m in cat if not isinstance(m.get('ficha'), dict))
print(f"  ficha no-dict: {malas}")
sin_es = sum(1 for m in cat if isinstance(m.get('ficha'),dict) and not m['ficha'].get('es'))
print(f"  sin ficha.es: {sin_es}")
print(f"  con galeria: {sum(1 for m in cat if m.get('galeria'))}")
print(f"  con indice_detalle: {sum(1 for m in cat if m.get('indice_detalle'))}")
print(f"  con pais: {sum(1 for m in cat if m.get('pais'))}")
print(f"  con disenador: {sum(1 for m in cat if m.get('disenador'))}")

# ids duplicados
print("\n=== IDS ===")
from collections import Counter
ids = Counter(str(m.get('i')) for m in cat)
dup = {k:v for k,v in ids.items() if v>1}
print(f"  total ids: {len(ids)} | duplicados: {len(dup)}")
if dup:
    for k,v in list(dup.items())[:5]: print(f"    {k}: {v}")
