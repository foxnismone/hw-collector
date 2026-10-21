#!/usr/bin/env python3
"""Compara los modelos del árbol cronológico con el catálogo actual
y reporta cuántos faltan. Usa toy# y nombre normalizado."""
import json, re

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def norm(s):
    s = (s or '').lower()
    s = re.sub(r"\s*\(\d+(st|nd|rd|th) color[^)]*\)", '', s)
    s = re.sub(r"\s*\(treasure hunt\)", '', s)
    s = re.sub(r"[^a-z0-9]", '', s)
    return s

def main():
    cat = json.load(open(BASE + 'catalog_web.json', encoding='utf-8'))
    por_anio = json.load(open(BASE + 'modelos_por_anio.json', encoding='utf-8'))

    # Índices del catálogo
    ids = {m['i'] for m in cat}
    por_nom = {}
    for m in cat:
        y = m.get('y')
        n = norm(m.get('m'))
        if y and n: por_nom.setdefault((y, n), []).append(m)

    faltan = []
    ya = 0
    for anio, modelos in por_anio.items():
        for mo in modelos:
            toy = mo.get('toy','')
            pid = f"{anio}-{toy}"
            if pid in ids:
                ya += 1; continue
            n = norm(mo.get('modelo'))
            if (int(anio), n) in por_nom:
                ya += 1; continue
            faltan.append({**mo, 'anio': int(anio)})

    print(f"Modelos del árbol: {sum(len(v) for v in por_anio.values())}")
    print(f"Ya en catálogo: {ya}")
    print(f"FALTAN: {len(faltan)}")

    # Por año
    from collections import Counter
    c = Counter(f['anio'] for f in faltan)
    print(f"\nFaltantes por año:")
    for a in sorted(c):
        print(f"  {a}: {c[a]}")

    # Sin imagen
    sin_foto = sum(1 for f in faltan if not f.get('foto'))
    print(f"\nSin foto: {sin_foto}")

    json.dump(faltan, open(BASE + 'faltantes.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"Guardado: data/faltantes.json")

if __name__ == '__main__':
    main()
