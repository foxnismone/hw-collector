#!/usr/bin/env python3
"""Parsea las páginas 'List of XXXX Hot Wheels' (v3) soportando:
  - tablas con encabezados variables (Car Name, Casting Name, Model Name, Col #, Toy #)
  - toy numérico (1980s-2000s) y alfanumérico (2014+)
  - [[Image:...]] y [[File:...]]
  - <gallery> (años 1968-1982)
Salida: data/modelos_por_anio.json
"""
import json, urllib.request, urllib.parse, re, time

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

def quitar_templates(t):
    prev = None
    while prev != t:
        prev = t
        t = re.sub(r'\{\{[^{}]*\}\}', ' ', t)
    return t

def limpiar(t):
    if not t: return ''
    t = quitar_templates(t)
    t = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[\[([^\]]*)\]\]', r'\1', t)
    t = re.sub(r"<font[^>]*>|</font>", '', t)
    t = re.sub(r"''+", '', t)
    t = re.sub(r'<br\s*/?>', ' ', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'\s{2,}', ' ', t)
    return t.strip()

def nombre_imagen(t):
    for m in re.finditer(r'\[\[(?:File|Image):([^\]|]+)', t):
        f = m.group(1).strip()
        if f.startswith('Site-') or f.startswith('Icon-'): continue
        return f
    return ''

MAPA = [
    (r'toy\s*#', 'toy'),
    (r'col\.?\s*#', 'col'),
    (r'series\s*#', 'serie_num'),
    (r'series', 'serie'),
    (r'car\s*name|casting\s*name|model\s*name|casting|model|^name$|\bname\b', 'modelo'),
    (r'photo', 'foto'),
]

def mapear(encabezados):
    out = []
    for e in encabezados:
        el = quitar_templates(e).lower().replace("'''", '').strip()
        campo = 'otro'
        for patron, nombre in MAPA:
            if re.search(patron, el):
                campo = nombre; break
        out.append(campo)
    return out

def parsear_tabla(tabla):
    enc = []
    for linea in tabla.split('\n'):
        l = linea.strip()
        if l.startswith('!'):
            enc.append(l[1:].strip())
    if not enc: return []
    campos = mapear(enc)
    if 'modelo' not in campos: return []

    filas = re.split(r'\n\|-\s*\n', tabla)
    out = []
    for fila in filas:
        celdas = []
        for linea in fila.split('\n'):
            l = linea.strip()
            if l.startswith('|'):
                celdas.append(l[1:])
        if len(celdas) < 2: continue
        reg = {}
        for i, c in enumerate(celdas):
            if i >= len(campos): break
            campo = campos[i]
            if campo == 'foto':
                img = nombre_imagen(c)
                if img: reg['foto'] = img
            elif campo != 'otro':
                if campo not in reg or not reg[campo]:
                    reg[campo] = limpiar(c)
        if not reg.get('modelo'): continue
        out.append(reg)
    return out

def parsear_gallery(gal):
    """Formatos en <gallery>:
       - Image:x.jpg|[[Modelo]]|link=Modelo
       - x.jpg|[[Modelo]]              (1973, sin prefijo)
    """
    out = []
    # con prefijo Image:/File:
    for m in re.finditer(r'(?:Image|File):([^|\n]+)\|\s*\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', gal):
        img = m.group(1).strip()
        modelo = limpiar(m.group(2))
        if modelo: out.append({'modelo': modelo, 'foto': img, 'serie': ''})
    # sin prefijo (solo nombre.ext)
    if not out:
        for m in re.finditer(r'([A-Za-z0-9_%\- ]+\.(?:jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF))\s*\|\s*\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', gal):
            img = m.group(1).strip()
            modelo = limpiar(m.group(2))
            if modelo: out.append({'modelo': modelo, 'foto': img, 'serie': ''})
    return out

def parsear_templates(wt):
    """{{List0000White|TOY|COL|[[Modelo|Display]]|Serie|SerieNum|}} + imagen siguiente"""
    out = []
    for m in re.finditer(r'\{\{List0000White\|([^|}]*)\|([^|}]*)\|\[\[([^\]|]+)(?:\|([^\]]*))?\]\]\|([^|}]*)\|([^|}]*)\|?\}\}', wt):
        toy = limpiar(m.group(1)); col = limpiar(m.group(2))
        modelo = limpiar(m.group(4) or m.group(3)); serie = limpiar(m.group(5)); serie_num = limpiar(m.group(6))
        # imagen asociada: el [[Image:...]] que sigue al template
        resto = wt[m.end():m.end()+200]
        img = ''
        im = re.search(r'\[\[(?:Image|File):([^\]|]+)', resto)
        if im: img = im.group(1).strip()
        if modelo:
            out.append({'toy':toy,'col':col,'modelo':modelo,'serie':serie,'serie_num':serie_num,'foto':img})
    return out

def extraer_tablas(wt):
    tablas = []
    depth = 0; ini = -1
    for i in range(len(wt)-1):
        if wt[i:i+2] == '{|':
            if depth == 0: ini = i
            depth += 1
        elif wt[i:i+2] == '|}':
            depth -= 1
            if depth == 0 and ini >= 0:
                tablas.append(wt[ini:i+2]); ini = -1
    return tablas

def extraer_galerias(wt):
    out = []
    for m in re.finditer(r'<gallery[^>]*>(.*?)</gallery>', wt, re.DOTALL | re.I):
        out.append(m.group(1))
    return out

def parsear_pagina(titulo):
    d = api({'action':'parse','page':titulo,'prop':'wikitext','format':'json'})
    if not d or 'parse' not in d: return []
    wt = d['parse'].get('wikitext',{}).get('*','')
    if not wt: return []
    modelos = []
    for t in extraer_tablas(wt):
        modelos.extend(parsear_tabla(t))
    for g in extraer_galerias(wt):
        modelos.extend(parsear_gallery(g))
    modelos.extend(parsear_templates(wt))
    return modelos

def main():
    mapa = json.load(open(BASE + 'mapa_fandom.json', encoding='utf-8'))
    salida = {}
    total = 0
    for titulo in mapa['cronologico']:
        m = re.match(r'List of (\d{4}) Hot Wheels$', titulo)
        if not m: continue
        anio = int(m.group(1))
        modelos = parsear_pagina(titulo)
        for mo in modelos: mo['y'] = anio
        salida[str(anio)] = modelos
        total += len(modelos)
        print(f"  {anio}: {len(modelos)}")
        json.dump(salida, open(BASE + 'modelos_por_anio.json','w',encoding='utf-8'), ensure_ascii=False)
        time.sleep(0.3)
    print(f"\nTOTAL: {total}")

if __name__ == '__main__':
    main()
