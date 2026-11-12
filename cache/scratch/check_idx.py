import json
cat = json.load(open('data/catalog_web.json', encoding='utf-8'))
# ejemplo con indice_detalle
ej = [m for m in cat if m.get('indice_detalle')]
print("Con indice_detalle:", len(ej))
if ej:
    print(json.dumps(ej[0].get('indice_detalle'), ensure_ascii=False, indent=2)[:600])
    print("indice_coleccionabilidad:", ej[0].get('indice_coleccionabilidad'))
# ¿cuantos tienen indice?
print("Con indice_coleccionabilidad:", sum(1 for m in cat if m.get('indice_coleccionabilidad') is not None))
