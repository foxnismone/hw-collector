#!/usr/bin/env python3
"""Extrae TODOS los modelos de Fandom + diseñadores con traducción a 8 idiomas."""
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

DISEÑADORES = {
    'Ira Gilford': {'nacionalidad':'Estadounidense','periodo':'1968-1990','nota':'Diseñador principal de los primeros Hot Wheels'},
    'Larry Wood': {'nacionalidad':'Estadounidense','periodo':'1970-2000','nota':'Diseñador de clásicos como AMC AMX'},
    'Tom Daniel': {'nacionalidad':'Estadounidense','periodo':'1968-1980','nota':'Diseñador de modelos personalizados y únicos'},
    'Harry Bradley': {'nacionalidad':'Estadounidense','periodo':'1968-1975','nota':'Diseñador de los primeros modelos'},
    'Howard Rees': {'nacionalidad':'Estadounidense','periodo':'1968-1980','nota':'Diseñador de dragsters y funny cars'},
    'Paul Tam': {'nacionalidad':'Chino','periodo':'1990-2020','nota':'Diseñador de castings internacionales'},
    'Bob Rosas': {'nacionalidad':'Estadounidense','periodo':'1970-1990','nota':'Diseñador de muscle cars'},
    'Abe Lugo': {'nacionalidad':'Estadounidense','periodo':'1995-2020','nota':'Diseñador de modelos modernos'},
    'Phil Riehlman': {'nacionalidad':'Estadounidense','periodo':'1990-2010','nota':'Diseñador de re-ediciones'},
    'Dave Weise': {'nacionalidad':'Estadounidense','periodo':'2000-2020','nota':'Diseñador de línea premium'},
    'Jun Imai': {'nacionalidad':'Japonés','periodo':'2000-2020','nota':'Diseñador de la serie Car Culture'},
    'Tyler Charest': {'nacionalidad':'Estadounidense','periodo':'2010-2020','nota':'Diseñador de la línea mainline'},
    'Kevin Cao': {'nacionalidad':'Estadounidense','periodo':'2005-2020','nota':'Diseñador de castings especiales'},
}

TRADUCCIONES = {
    'es': {'titulo':'Diseñador','nacionalidad':'Nacionalidad','periodo':'Período','nota':'Nota','ficha':'Ficha de diseño','historia':'Historia'},
    'fr': {'titulo':'Concepteur','nacionalidad':'Nationalité','periodo':'Période','nota':'Note','ficha':'Fiche de conception','historia':'Histoire'},
    'ru': {'titulo':'Дизайнер','nacionalidad':'Национальность','periodo':'Период','nota':'Заметка','ficha':'Дизайн-карта','historia':'История'},
    'en': {'titulo':'Designer','nacionalidad':'Nationality','periodo':'Period','nota':'Note','ficha':'Design card','historia':'History'},
    'ja': {'titulo':'デザイナー','nacionalidad':'国籍','periodo':'期間','nota':'メモ','ficha':'デザインファイル','historia':'歴史'},
    'zh': {'titulo':'设计师','nacionalidad':'国籍','periodo':'期间','nota':'备注','ficha':'设计卡','historia':'历史'},
    'pt': {'titulo':'Designer','nacionalidad':'Nacionalidade','periodo':'Período','nota':'Nota','ficha':'Ficha de design','historia':'História'},
    'it': {'titulo':'Designer','nacionalidad':'Nazionalità','periodo':'Periodo','nota':'Nota','ficha':'Scheda di design','historia':'Storia'},
}

def main():
    catalogo = json.load(open(CATALOG_FILE, encoding='utf-8'))
    print(f"Catálogo actual: {len(catalogo)} modelos")
    ids_existentes = {str(m.get('t','')) for m in catalogo}
    nuevos_total = 0
    disenadores_total = 0

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
        time.sleep(0.2)

    print(f"\nBuscando diseñadores...")
    modelos_antiguos = [m for m in catalogo if m.get('y') and m.get('y')<=2015]
    print(f"Modelos antiguos: {len(modelos_antiguos)}")

    for i, modelo in enumerate(modelos_antiguos[:50]):
        nombre = modelo.get('m','')
        data = api_fandom({'action':'query','list':'search','srsearch':f'intitle:{nombre}','format':'json','srlimit':'1','srnamespace':'0'})
        if not data: continue
        resultados = data.get('query',{}).get('search',[])
        if not resultados: continue
        titulo = resultados[0].get('title','')
        data2 = api_fandom({'action':'parse','page':titulo,'format':'json','prop':'wikitext'})
        if not data2: continue
        wt = data2.get('parse',{}).get('wikitext',{}).get('*','')
        m = re.search(r'[Dd]esigner[:\s]*([^\n\|]+)', wt)
        if m:
            disenador = m.group(1).strip()
            info = None
            for key, val in DISEÑADORES.items():
                if key.lower() in disenador.lower() or disenador.lower() in key.lower():
                    info = val; break
            if not info: info = {'nacionalidad':'Desconocida','periodo':'','nota':''}
            traducciones = {}
            for idioma, trad in TRADUCCIONES.items():
                traducciones[idioma] = {'titulo':trad['titulo'],'nacionalidad':info['nacionalidad'],
                    'periodo':info['periodo'],'nota':info['nota'],
                    'ficha':f"Ficha de diseño de {nombre} por {disenador}",
                    'historia':f"El modelo {nombre} fue diseñado por {disenador}."}
            modelo['diseñador'] = disenador
            modelo['diseñador_info'] = info
            modelo['traducciones_disenador'] = traducciones
            disenadores_total += 1
            print(f"  [{i+1}] {nombre} -> {disenador}")
        time.sleep(0.3)

    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalogo, f, ensure_ascii=False, separators=(',',':'))

    print(f"\n{'='*50}")
    print(f"Nuevos modelos: {nuevos_total}")
    print(f"Diseñadores: {disenadores_total}")
    print(f"Total: {len(catalogo)}")

if __name__ == '__main__':
    main()
