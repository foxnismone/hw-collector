#!/usr/bin/env python3
"""Calcula el desglose del índice de coleccionabilidad (R, D, C, A, M)
y lo añade a cada modelo como 'indice_detalle'. Recalcula 'indice_coleccionabilidad'.

Fórmula: Índice = 0,30·R + 0,25·D + 0,20·C + 0,15·A + 0,10·M
  R rareza (0-100)  D demanda (0-100)  C condición (0-100)  A antigüedad (0-60)  M mercado (0-100)
"""
import json, re

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def rareza(m):
    k = (m.get('k') or '').lower()
    s = (m.get('s') or '').lower()
    texto = k + ' ' + s
    if 'super treasure' in texto or k == 'sth': return 95
    if 'treasure hunt' in texto or k == 'th': return 80
    if any(x in texto for x in ('red line club','rlc','elite 64','convention','collectors national')): return 85
    if 'car culture' in texto: return 70
    if 'boulevard' in texto: return 68
    if 'premium' in texto: return 65
    if m.get('conmemorativo') or 'anniversary' in texto: return 72
    # re-ediciones: si el modelo tiene muchas apariciones, menos raro
    return 45

def demanda(m, apariciones):
    # proxy: más apariciones = más demanda pero también más común
    if apariciones >= 10: return 85
    if apariciones >= 5: return 70
    if apariciones >= 3: return 58
    if apariciones >= 2: return 48
    return 40

def condicion(m):
    # base: nuevo en tarjeta
    return 100

def antiguedad(m):
    y = m.get('y')
    if not y: return 30
    try: y = int(y)
    except Exception: return 30
    if y >= 2026: return 0
    if y < 2016: return 60
    return min(60, round((2026 - y) * 5.5))

def mercado(m):
    k = (m.get('k') or '').lower()
    s = (m.get('s') or '').lower()
    texto = k + ' ' + s
    if 'super treasure' in texto: return 95
    if 'treasure hunt' in texto: return 88
    if any(x in texto for x in ('red line club','rlc','convention')): return 80
    if 'car culture' in texto: return 72
    return 55

def main():
    cat = json.load(open(BASE + 'catalog_web.json', encoding='utf-8'))
    print(f"Modelos: {len(cat)}")

    # contar apariciones por nombre de casting (normalizado)
    def norm(s):
        s = (s or '').lower()
        s = re.sub(r"\s*\(\d+(st|nd|rd|th) color[^)]*\)", '', s)
        s = re.sub(r"[^a-z0-9]", '', s)
        return s
    apariciones = {}
    for m in cat:
        n = norm(m.get('m'))
        if n: apariciones[n] = apariciones.get(n, 0) + 1

    for m in cat:
        R = rareza(m)
        D = demanda(m, apariciones.get(norm(m.get('m')), 1))
        C = condicion(m)
        A = antiguedad(m)
        M = mercado(m)
        indice = round(0.30*R + 0.25*D + 0.20*C + 0.15*A + 0.10*M, 1)
        m['indice_detalle'] = {
            'R': {'v': R, 'l': 'Rareza', 'peso': 0.30},
            'D': {'v': D, 'l': 'Demanda', 'peso': 0.25},
            'C': {'v': C, 'l': 'Condición', 'peso': 0.20},
            'A': {'v': A, 'l': 'Antigüedad', 'peso': 0.15},
            'M': {'v': M, 'l': 'Mercado', 'peso': 0.10},
        }
        m['indice_coleccionabilidad'] = indice

    json.dump(cat, open(BASE + 'catalog_web.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
    print("indice_detalle añadido a todos los modelos")

    # Regenerar cat.js
    txt = json.dumps(cat, ensure_ascii=False, separators=(',',':'))
    open('C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/cat.js','w',encoding='utf-8').write('const CAT=' + txt + ';\n')
    print(f"cat.js regenerado ({len(txt)/1024/1024:.1f} MB)")

    # estadisticas
    import statistics
    idx = [m['indice_coleccionabilidad'] for m in cat]
    print(f"Índice: min {min(idx)} | mediana {statistics.median(idx)} | max {max(idx)}")

if __name__ == '__main__':
    main()
