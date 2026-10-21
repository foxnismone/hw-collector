#!/usr/bin/env python3
"""Scraper de PÁGINAS DE CASTING de Fandom.
Extrae de cada página:
  - template {{casting|name=|series=|number=|years=|designer=|image=}}
  - descripción real (sección Description)
  - tabla de Versiones (Col #, Year, Series, Color, Tampo, Base, Window, Interior, Wheel, Toy #, Country, Photo)
Salida: data/castings.json
"""
import json, urllib.request, urllib.parse, re, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    t = t.replace('&ndash;','-').replace('&mdash;','—').replace('&nbsp;',' ')
    t = re.sub(r'\s{2,}', ' ', t)
    return t.strip()

MAPA = [
    (r'col\.?\s*#', 'col'),
    (r'^year$|\byear\b', 'anio'),
    (r'series\s*#', 'serie_num'),
    (r'series', 'serie'),
    (r'^color$|body color', 'color'),
    (r'tampo', 'tampo'),
    (r'base color|base\s*/', 'base'),
    (r'window', 'ventana'),
    (r'interior', 'interior'),
    (r'wheel type|wheel', 'rueda'),
    (r'toy\s*#', 'toy'),
    (r'country', 'pais'),
    (r'photo', 'foto'),
]

def mapear(enc):
    out = []
    for e in enc:
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
        if l.startswith('!'): enc.append(l[1:].strip())
    if not enc: return []
    campos = mapear(enc)
    filas = re.split(r'\n\|-\s*\n', tabla)
    out = []
    for fila in filas:
        celdas = [l[1:] for l in fila.split('\n') if l.strip().startswith('|')]
        if len(celdas) < 2: continue
        reg = {}
        for i, c in enumerate(celdas):
            if i >= len(campos): break
            campo = campos[i]
            if campo == 'foto':
                im = re.search(r'\[\[(?:File|Image):([^\]|]+)', c)
                if im and not im.group(1).startswith(('Site-','Icon-')): reg['foto'] = im.group(1).strip()
            elif campo != 'otro':
                if campo not in reg or not reg[campo]:
                    reg[campo] = limpiar(c)
        if reg: out.append(reg)
    return out

def extraer_tablas(wt):
    tabs = []; depth = 0; ini = -1
    for i in range(len(wt)-1):
        if wt[i:i+2] == '{|':
            if depth == 0: ini = i
            depth += 1
        elif wt[i:i+2] == '|}':
            depth -= 1
            if depth == 0 and ini >= 0:
                tabs.append(wt[ini:i+2]); ini = -1
    return tabs

def parsear_casting(titulo):
    d = api({'action':'parse','page':titulo,'prop':'text|wikitext','format':'json'})
    if not d or 'parse' not in d: return None
    wt = d['parse'].get('wikitext',{}).get('*','')
    if not wt: return None

    meta = {'titulo': titulo}
    # template {{casting|...}}
    m = re.search(r'\{\{casting\|([^}]*)\}\}', wt, re.I)
    if m:
        for campo in ('name','series','number','years','designer','image'):
            cm = re.search(rf'\|\s*{campo}\s*=\s*([^|}}]+)', m.group(1))
            if cm: meta[campo] = limpiar(cm.group(1))
    # descripción
    dm = re.search(r'==\s*Description\s*==(.*?)(?===|$)', wt, re.DOTALL | re.I)
    if dm:
        desc = limpiar(dm.group(1))
        if len(desc) > 40: meta['descripcion'] = desc[:800]
    # versiones
    versiones = []
    for t in extraer_tablas(wt):
        vs = parsear_tabla(t)
        if vs: versiones.extend(vs)
    if versiones: meta['versiones'] = versiones
    # curiosidades (Notes)
    nm = re.search(r'==\s*(Notes|Curiosities|Notas|Trivia)\s*==(.*?)(?===|$)', wt, re.DOTALL | re.I)
    if nm:
        txt = limpiar(nm.group(2))
        if len(txt) > 30: meta['curiosidades'] = txt[:500]
    return meta if ('versiones' in meta or 'descripcion' in meta) else None

def main():
    mapa = json.load(open(BASE + 'mapa_fandom.json', encoding='utf-8'))
    sub = mapa['subcategorias']

    # Categorías prioritarias del usuario
    import re as _re
    prioridades = [
        (r'car culture', 'Car Culture'),
        (r'team transport', 'Team Transport'),
        (r'boulevard', 'Boulevard'),
        (r'pop culture', 'Pop Culture'),
        (r'retro entertainment', 'Retro Entertainment'),
        (r'first edition|new model', 'First Editions/New Models'),
        (r'mystery', 'Mystery Models'),
        (r'red line club|\bhwc\b|elite 64|convention|collectors national', 'Collector Exclusives'),
        (r'redline|flying colors|ultra hot|real rider|crack.?up|color shifter', 'Special & Early'),
        (r'100% hot wheels|monster truck|sizzler|starship', 'Gran Escala'),
    ]
    paginas = []
    for patron, etiqueta in prioridades:
        for cat, miembros in sub.items():
            if _re.search(patron, cat, _re.I):
                for m in miembros:
                    paginas.append((m, etiqueta))
    # quitar duplicados
    vistos = set(); unicas = []
    for t, e in paginas:
        if t not in vistos:
            unicas.append((t, e)); vistos.add(t)
    paginas = unicas
    print(f"Páginas de casting a parsear: {len(paginas)}")

    salida = {}
    if os.path.exists(BASE + 'castings.json'):
        salida = json.load(open(BASE + 'castings.json', encoding='utf-8'))
    pend = [(t, e) for t, e in paginas if t not in salida]
    print(f"Ya parseadas: {len(salida)} | pendientes: {len(pend)}")

    ok = 0
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(parsear_casting, t): (t, e) for t, e in pend}
        for fut in as_completed(futs):
            t, e = futs[fut]
            try:
                r = fut.result()
                salida[t] = r if r else {}
                salida[t]['_categoria'] = e
                ok += 1
            except Exception:
                salida[t] = {}; salida[t]['_categoria'] = e
                ok += 1
            if ok % 200 == 0:
                json.dump(salida, open(BASE + 'castings.json','w',encoding='utf-8'), ensure_ascii=False)
                print(f"  {ok}/{len(pend)}")

    json.dump(salida, open(BASE + 'castings.json','w',encoding='utf-8'), ensure_ascii=False)
    con_datos = sum(1 for v in salida.values() if v.get('versiones'))
    print(f"\nTotal: {len(salida)} | con versiones: {con_datos}")

if __name__ == '__main__':
    main()
