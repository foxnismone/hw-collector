import json
fr = json.load(open('data/fichas_reales.json', encoding='utf-8'))
ft = json.load(open('data/fichas_traducidas.json', encoding='utf-8'))
print(f"fichas_reales: {len(fr)}")
print(f"fichas_traducidas: {len(ft)}")

con_datos = {k:v for k,v in fr.items() if v}
print(f"Con datos: {len(con_datos)}")

# ejemplo
ej = list(con_datos.items())[0]
print(f"\nEjemplo: {ej[0]}")
print(json.dumps(ej[1], ensure_ascii=False, indent=2)[:800])

# campos disponibles
campos = set()
for v in con_datos.values(): campos.update(v.keys())
print(f"\nCampos: {campos}")
