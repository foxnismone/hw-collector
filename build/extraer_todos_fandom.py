#!/usr/bin/env python3
"""Extrae TODOS los modelos de Hot Wheels de Fandom Wiki usando la API y BeautifulSoup."""
import json, urllib.request, urllib.parse, re, time
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
CATALOG_FILE = DATA_DIR / 'catalog_web.json'

def api_fandom(params):
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except: return None

def extraer_pagina(titulo, anio):
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return []
    data = api_fandom({'action':'parse','page':titulo,'format':'json','prop':'text'})
    if not data: return []
    html = data.get('parse',{}).get('text',{}).get('*','')
    if not html: return []
    soup = BeautifulSoup(html, 'html.parser')
    modelos = []
    for tabla in soup.find_all('table'):
        for fila in tabla.find_all('tr'):
            celdas = fila.find_all(['td','th'])
            if len(celdas) >= 3:
                tool = celdas[0].get_text(strip=True)
                if not re.match(r'^[A-Z]?\d+$', tool): continue
                nombre = celdas[2].get_text(strip=True)
                nombre = re.sub(r'\[\[|\]\]','',nombre)
                nombre = re.sub(r'\|.*','',nombre).strip()
                if nombre and len(nombre)>2 and not nombre.isdigit():
                    modelos.append({'tool_number':tool,'name':nombre,'year':anio})
    return modelos

def main():
    catalogo = json.load(open(CATALOG_FILE, encoding='utf-8'))
    print(f"Catálogo actual: {len(catalogo)} modelos")
    ids_existentes = {str(m.get('t','')) for m in catalogo}
    nuevos_total = 0
    for anio in range(1968, 2028):
        titulo = f"List_of_{anio}_Hot_Wheels_new_castings"
        modelos = extraer_pagina(titulo, anio)
        nuevos = [m for m in modelos if m['tool_number'] not in ids_existentes]
        for m in nuevos:
            catalogo.append({'i':m['tool_number'],'m':m['name'],'y':anio,'t':m['tool_number'],
                'c':'000','s':'Desconocida','n':'1/1','k':'Mainline','x':5.0,'im':'',
                'v':1.0,'V':10.0,'px':1,'f':[50.0,50.0,50.0,50.0,50.0],'dm':0,'ap':0})
            ids_existentes.add(m['tool_number'])
            nuevos_total += 1
        print(f"[{anio}] {len(modelos)} encontrados, {len(nuevos)} nuevos")
        time.sleep(0.3)
    with open(CATALOG_FILE,'w',encoding='utf-8') as f:
        json.dump(catalogo, f, ensure_ascii=False, separators=(',',':'))
    print(f"\n✅ Nuevos: {nuevos_total} | Total: {len(catalogo)}")

if __name__=='__main__':
    main()
