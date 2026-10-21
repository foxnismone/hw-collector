#!/usr/bin/env python3
"""Parsea las páginas 'List of XXXX Hot Wheels' del árbol cronológico.
Extrae por fila: Toy#, Col.#, Modelo, Serie, Serie#, Foto.
Salida: data/modelos_por_anio.json  (año -> [modelos])
"""
import json, urllib.request, urllib.parse, re, time, os

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def api(params, intentos=3):
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (hotwheels-research)')
    req.add_header('Referer','https://hotwheels.fandom.com/')
    for i in range(intentos):
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception:
            time.sleep(1.5*(i+1))
    return None

def limpiar_modelo(t):
    """De [[Mazda MX-5 Miata (2025)|Mazda MX-5 Miata]] (2nd Color) -> Mazda MX-5 Miata (2nd Color)"""
    t = t.strip()
    # quitar templates
    t = re.sub(r'\{\{[^{}]*\}\}', '', t)
    # wikilinks con display
    t = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[\[([^\]]*)\]\]', r'\1', t)
    t = re.sub(r"''+", '', t)
    t = re.sub(r'<br\s*/?>', ' ', t)
    t = re.sub(r'<[^>]+>', '', t)
    return re.sub(r'\s{2,}', ' ', t).strip()

def limpiar_serie(t):
    t = t.strip()
    t = re.sub(r'\{\{[^{}]*\}\}', '', t)
    t = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[\[([^\]]*)\]\]', r'\1', t)
    t = re.sub(r"<font[^>]*>|</font>", '', t)
    t = re.sub(r"''+", '', t)
    t = re.sub(r'<br\s*/?>', ' ', t)
    return re.sub(r'\s{2,}', ' ', t).strip()

def parsear_pagina_anio(titulo, anio):
    d = api({'action':'parse','page':titulo,'prop':'wikitext','format':'json'})
    if not d or 'parse' not in d: return []
    wt = d['parse'].get('wikitext',{}).get('*','')
    if not wt: return []

    modelos = []
    # Dividir en filas por '|-\n'
    filas = re.split(r'\n\|-\s*\n', wt)
    for fila in filas:
        # Extraer celdas: líneas que empiezan con '|'
        celdas = []
        for linea in fila.split('\n'):
            linea = linea.strip()
            if linea.startswith('|'):
                celda = linea[1:]
                celdas.append(celda)
        if len(celdas) < 4: continue
        toy = celdas[0].strip()
        if not re.match(r'^[A-Z]{2,4}\d{2}$', toy): continue  # formato tipo JJJ02
        col = limpiar_modelo(celdas[1])
        modelo = limpiar_modelo(celdas[2])
        serie = limpiar_serie(celdas[3]) if len(celdas) > 3 else ''
        serie_num = limpiar_modelo(celdas[4]) if len(celdas) > 4 else ''
        foto = ''
        for c in celdas[5:]:
            m = re.search(r'\[\[File:([^\]|]+)', c)
            if m:
                foto = m.group(1).strip(); break
        if not modelo: continue
        modelos.append({'toy':toy,'col':col,'m':modelo,'s':serie,'n':serie_num,'foto':foto})
    return modelos

def main():
    mapa = json.load(open(BASE + 'mapa_fandom.json', encoding='utf-8'))
    paginas = mapa['cronologico']
    print(f"Páginas por parsear: {len(paginas)}")

    salida = {}
    if os.path.exists(BASE + 'modelos_por_anio.json'):
        salida = json.load(open(BASE + 'modelos_por_anio.json', encoding='utf-8'))

    total = 0
    for titulo in paginas:
        m = re.match(r'List of (\d{4}) Hot Wheels$', titulo)
        if not m: continue
        anio = int(m.group(1))
        if str(anio) in salida:
            total += len(salida[str(anio)])
            continue
        modelos = parsear_pagina_anio(titulo, anio)
        salida[str(anio)] = modelos
        total += len(modelos)
        print(f"  {anio}: {len(modelos)} modelos")
        json.dump(salida, open(BASE + 'modelos_por_anio.json','w',encoding='utf-8'), ensure_ascii=False)
        time.sleep(0.25)

    print(f"\nTOTAL modelos por año: {total}")
    json.dump(salida, open(BASE + 'modelos_por_anio.json','w',encoding='utf-8'), ensure_ascii=False)
    print("Guardado: data/modelos_por_anio.json")

if __name__ == '__main__':
    main()
