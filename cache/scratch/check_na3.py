import json, glob, os

archivos = ['data/modelos_por_anio.json','data/fichas_reales.json','data/castings.json','data/catalog_web.json']
for a in archivos:
    if not os.path.exists(a): continue
    txt = open(a, encoding='utf-8').read()
    n = txt.lower().count('not available')
    n2 = txt.lower().count('image_not_available')
    n3 = txt.lower().count('imagen_no_disponible')
    print(f"{a}: 'not available'={n}  image_not_available={n2}  imagen_no_disponible={n3}")

# en el catalogo: cuantos NO tienen im
cat = json.load(open('data/catalog_web.json', encoding='utf-8'))
sin_im = [m for m in cat if not m.get('im')]
print(f"\nModelos sin imagen (muestran 🚫): {len(sin_im)}")
for m in sin_im[:10]:
    print(f"  {m['m'][:45]:47s} {m['y']}")
