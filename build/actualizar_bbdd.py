#!/usr/bin/env python3
"""
Actualiza catalog_web.json con los nuevos modelos parseados de Hot Wheels Wiki.

Uso:
    python build/actualizar_bbdd.py data/new_models_batch1.json
    python build/actualizar_bbdd.py data/new_models_batch1.json data/new_models_batch2.json
"""

import sys
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
CATALOG_FILE = DATA_DIR / 'catalog_web.json'

def cargar_catalogo():
    if CATALOG_FILE.exists():
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_catalogo(catalogo):
    CATALOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalogo, f, ensure_ascii=False, separators=(',', ':'))
    print(f"Catálogo guardado: {len(catalogo)} modelos totales")

def actualizar_catalogo(archivos_nuevos):
    catalogo = cargar_catalogo()
    ids_existentes = {m.get('i', '') for m in catalogo}
    print(f"Modelos actuales: {len(catalogo)}")

    nuevos = 0
    for archivo in archivos_nuevos:
        ruta = Path(archivo)
        if not ruta.exists():
            print(f"  ⚠️  No existe: {archivo}")
            continue
        with open(ruta, 'r', encoding='utf-8') as f:
            modelos = json.load(f)
        for m in modelos:
            tool = m.get('tool_number', '').strip()
            if not tool:
                continue
            if tool not in ids_existentes:
                # Agregar al catálogo con formato compatible
                catalogo.append({
                    'i': tool,
                    'm': m.get('name', '').strip(),
                    'k': 'Mainline',
                    'y': m.get('year', 0),
                    'img': ''
                })
                ids_existentes.add(tool)
                nuevos += 1
        print(f"  ✓ {ruta.name}: {len(modelos)} modelos procesados")

    if nuevos:
        guardar_catalogo(catalogo)
        print(f"\n✅ {nuevos} nuevos modelos agregados al catálogo")
    else:
        print(f"\n⚠️  No se agregaron nuevos modelos")
    return nuevos

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python build/actualizar_bbdd.py <archivo1.json> [archivo2.json] ...")
        sys.exit(1)
    actualizar_catalogo(sys.argv[1:])
