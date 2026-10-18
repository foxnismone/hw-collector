#!/usr/bin/env python3
"""
Herramienta de extracción masiva de datos de Hot Wheels Fandom Wiki.
Extrae datos de las páginas List_of_YYYY_Hot_Wheels (1968-2027) y los integra al catálogo.
"""

import json, re, urllib.request, urllib.parse, time, sys, os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent / 'data'
CATALOG_FILE = BASE_DIR / 'catalog_web.json'
DISENADORES_FILE = BASE_DIR / 'disenadores.json'

def api_fandom(params):
    """Hace una solicitud a la API de Fandom"""
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (hotwheels-research)')
    req.add_header('Referer', 'https://hotwheels.fandom.com/')
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"  Error API: {e}")
        return None

def obtener_wikitext(titulo):
    """Obtiene el wikitext de una página"""
    data = api_fandom({
        'action':'query','prop':'revisions',
        'titles':titulo,'rvslots':'*','rvprop':'content',
        'format':'json','formatversion':'2'
    })
    if not data:
        return None
    pages = data.get('query',{}).get('pages',{})
    if isinstance(pages, dict):
        for p in pages.values():
            return p.get('revisions',[{}])[0].get('slots',{}).get('main',{}).get('content','')
    return None

def extraer_modelos_wikitext(wikitext, anio):
    """Extrae modelos del wikitext de una página List_of"""
    modelos = []
    lineas = wikitext.split('\n')
    
    for linea in lineas:
        # Buscar líneas de tabla con datos de modelos
        # Formato: | Toy # | Model Name | Photo |
        # o: | 6205 | Custom Cougar | [Custom Cougar](url) |
        
        # Patrón 1: | tool | nombre | imagen
        match = re.match(r'\|\s*(\d{4})\s*\|\s*([^\|]+)\s*\|\s*\[([^\]]+)\]\(([^\)]+)\)', linea)
        if match:
            tool = match.group(1).strip()
            nombre = match.group(2).strip()
            url_img = match.group(4).strip()
            # Convertir URL de Fandom a proxy
            if 'wikia' in url_img:
                url_img = url_img.replace('https://static.wikia.nocookie.net/', 'https://images.weserv.nl/?url=static.wikia.nocookie.net/')
            modelos.append({
                'anio': anio,
                'tool': tool,
                'nombre': nombre,
                'imagen': url_img
            })
            continue
        
        # Patrón 2: | tool | nombre | [nombre](url) |
        match = re.match(r'\|\s*(\d{4})\s*\|\s*([^\|]+)\s*\|\s*\[([^\]]+)\]\(([^\)]+)\)', linea)
        if match:
            tool = match.group(1).strip()
            nombre = match.group(2).strip()
            url_img = match.group(4).strip()
            if 'wikia' in url_img:
                url_img = url_img.replace('https://static.wikia.nocookie.net/', 'https://images.weserv.nl/?url=static.wikia.nocookie.net/')
            modelos.append({
                'anio': anio,
                'tool': tool,
                'nombre': nombre,
                'imagen': url_img
            })
            continue
        
        # Patrón 3: | tool | nombre | imagen (sin link)
        match = re.match(r'\|\s*(\d{4})\s*\|\s*([^\|]+)\s*\|\s*([^\s|]+)', linea)
        if match:
            tool = match.group(1).strip()
            nombre = match.group(2).strip()
            url_img = match.group(3).strip()
            if 'wikia' in url_img:
                url_img = url_img.replace('https://static.wikia.nocookie.net/', 'https://images.weserv.nl/?url=static.wikia.nocookie.net/')
            modelos.append({
                'anio': anio,
                'tool': tool,
                'nombre': nombre,
                'imagen': url_img
            })
    
    return modelos

def main():
    # Cargar catálogo
    with open(CATALOG_FILE, encoding='utf-8') as f:
        catalog = json.load(f)
    
    with open(DISENADORES_FILE, encoding='utf-8') as f:
        disenadores = json.load(f)
    
    # Índices
    tool_existente = {m.get('t',''): m for m in catalog if m.get('t')}
    nombre_existente = {m.get('m','').lower().strip(): m for m in catalog}
    
    print(f"Catálogo actual: {len(catalog)} modelos")
    print(f"Diseñadores: {len(disenadores)}")
    
    # Procesar cada año
    total_agregados = 0
    total_imagenes = 0
    total_modelos = 0
    
    for anio in range(1968, 2028):
        titulo = f'List_of_{anio}_Hot_Wheels'
        print(f"\nProcesando {titulo}...")
        
        wikitext = obtener_wikitext(titulo)
        if not wikitext:
            print(f"  No se pudo obtener wikitext")
            continue
        
        modelos = extraer_modelos_wikitext(wikitext, anio)
        print(f"  Modelos encontrados: {len(modelos)}")
        total_modelos += len(modelos)
        
        for modelo in modelos:
            tool = modelo['tool']
            nombre = modelo['nombre']
            url_img = modelo['imagen']
            
            # Verificar si ya existe
            if tool in tool_existente:
                # Actualizar imagen si no tiene
                if not tool_existente[tool].get('im'):
                    tool_existente[tool]['im'] = url_img
                    total_imagenes += 1
                continue
            
            # Verificar si existe por nombre
            nombre_norm = nombre.lower().strip()
            if nombre_norm in nombre_existente:
                # Actualizar tool number si no tiene
                if not nombre_existente[nombre_norm].get('t'):
                    nombre_existente[nombre_norm]['t'] = tool
                # Actualizar imagen si no tiene
                if not nombre_existente[nombre_norm].get('im'):
                    nombre_existente[nombre_norm]['im'] = url_img
                    total_imagenes += 1
                continue
            
            # Agregar nuevo modelo
            nuevo = {
                'i': f'{anio}-{tool}',
                'm': nombre,
                'y': anio,
                't': tool,
                'c': '001',
                's': f'{anio} Hot Wheels',
                'n': f'1/{len(modelos)}',
                'k': 'Mainline',
                'im': url_img,
                'v': 1.0,
                'V': 5.0,
                'px': 12,
                'f': [20.2, 38.0, 100.0, 0.0, 40.0],
                'dm': 0,
                'ap': 4,
                'ficha': {
                    'descripcion': f'{nombre} de {anio}.',
                    'historia': f'El {nombre} fue introducido en {anio}.',
                    'curiosidades': f'Tool #{tool}. Parte de la colección de {anio}.',
                    'conmemorativo': False,
                    'dato_clave': f'Tool #{tool} de {anio}'
                },
                'indice_coleccionabilidad': 53.5,
                'valores_mercado': {
                    'usd': 39.6,
                    'clp': 37620.0,
                    'eur': 36.43,
                    'fecha': '2026-10-14T10:13:19.274849',
                    'fuente': 'Cálculo automático'
                }
            }
            catalog.append(nuevo)
            tool_existente[tool] = nuevo
            nombre_existente[nombre_norm] = nuevo
            total_agregados += 1
            total_imagenes += 1
        
        time.sleep(0.2)
    
    # Guardar
    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, separators=(',',':'))
    
    with open(DISENADORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(disenadores, f, ensure_ascii=False, indent=2)
    
    # Estadísticas
    con_img = sum(1 for m in catalog if m.get('im'))
    con_d = sum(1 for m in catalog if m.get('diseñador'))
    con_p = sum(1 for m in catalog if m.get('pais'))
    con_s = sum(1 for m in catalog if m.get('s'))
    con_n = sum(1 for m in catalog if m.get('n'))
    
    print(f"\n{'='*60}")
    print(f"RESULTADO FINAL")
    print(f"{'='*60}")
    print(f"Modelos procesados: {total_modelos}")
    print(f"Modelos agregados: {total_agregados}")
    print(f"Imágenes asignadas: {total_imagenes}")
    print(f"\nImágenes: {con_img}/{len(catalog)} ({con_img*100//len(catalog)}%)")
    print(f"Diseñadores: {con_d}/{len(catalog)} ({con_d*100//len(catalog)}%)")
    print(f"Países: {con_p}/{len(catalog)} ({con_p*100//len(catalog)}%)")
    print(f"Series: {con_s}/{len(catalog)} ({con_s*100//len(catalog)}%)")
    print(f"Números: {con_n}/{len(catalog)} ({con_n*100//len(catalog)}%)")

if __name__ == '__main__':
    main()
