#!/usr/bin/env python3
"""
Script de corrección final:
1. Corregir imágenes falsas positivas (verificar título)
2. Mejorar extracción de números de colección
3. Filtrar diseñadores inválidos
4. Procesar pendientes
"""
import json, urllib.parse, urllib.request, time, re, sys, os

DATA_DIR = r'C:\Users\GODZILLA24H2\Desktop\hotwheels_collector\data'
OUTPUT_FILE = os.path.join(DATA_DIR, 'completar_final.json')
CATALOG_FILE = os.path.join(DATA_DIR, 'catalog_web.json')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://hotwheels.fandom.com/'
}

def api_fandom(params, retries=3):
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1 * (attempt + 1))
            else:
                return None

def search_fandom_exact(nombre, anio=None):
    """Buscar página exacta del modelo."""
    # Intentar búsqueda exacta primero
    data = api_fandom({
        'action': 'query',
        'list': 'search',
        'srsearch': f'"{nombre}"',
        'srlimit': '10',
        'format': 'json',
        'formatversion': '2'
    })
    
    if not data:
        return None
    
    results = data.get('query', {}).get('search', [])
    
    # Buscar coincidencia exacta de título
    nombre_clean = re.sub(r'\s*\(.*?\)', '', nombre).strip().lower()
    
    for r in results:
        titulo = r['title']
        titulo_clean = re.sub(r'\s*\(.*?\)', '', titulo).strip().lower()
        if nombre_clean == titulo_clean:
            return titulo
    
    # Si no hay coincidencia exacta, buscar con nombre + año
    if anio:
        data2 = api_fandom({
            'action': 'query',
            'list': 'search',
            'srsearch': f'{nombre} {anio}',
            'srlimit': '10',
            'format': 'json',
            'formatversion': '2'
        })
        if data2:
            results2 = data2.get('query', {}).get('search', [])
            for r in results2:
                titulo = r['title']
                titulo_clean = re.sub(r'\s*\(.*?\)', '', titulo).strip().lower()
                if nombre_clean in titulo_clean:
                    return titulo
    
    return None

def get_wikitext(titulo):
    data = api_fandom({
        'action': 'query',
        'prop': 'revisions',
        'titles': titulo,
        'rvslots': '*',
        'rvprop': 'content',
        'format': 'json',
        'formatversion': '2'
    })
    
    if not data:
        return None
    
    pages = data.get('query', {}).get('pages', [])
    if isinstance(pages, list):
        for page_data in pages:
            revs = page_data.get('revisions', [])
            if revs:
                return revs[0].get('slots', {}).get('main', {}).get('content', '')
    elif isinstance(pages, dict):
        for page_id, page_data in pages.items():
            revs = page_data.get('revisions', [])
            if revs:
                return revs[0].get('slots', {}).get('main', {}).get('content', '')
    return None

def get_page_image(titulo):
    data = api_fandom({
        'action': 'query',
        'titles': titulo,
        'prop': 'pageimages',
        'format': 'json',
        'pithumbsize': '300',
        'formatversion': '2'
    })
    
    if not data:
        return None
    
    pages = data.get('query', {}).get('pages', [])
    if isinstance(pages, list):
        for page_data in pages:
            if 'thumbnail' in page_data:
                return page_data['thumbnail']['source']
    elif isinstance(pages, dict):
        for page_id, page_data in pages.items():
            if 'thumbnail' in page_data:
                return page_data['thumbnail']['source']
    
    return None

def extract_designer(wikitext):
    if not wikitext:
        return None
    
    patterns = [
        r'\|\s*designer\s*=\s*\[\[([^\]|]+)',
        r'\|\s*[Dd]esigner\s*=\s*([^\n|]+)',
        r'designer\s*=\s*\[\[([^\]|]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, wikitext)
        if match:
            designer = match.group(1).strip()
            designer = re.sub(r'\[\[|\]\]', '', designer)
            designer = designer.strip()
            # Filtrar diseñadores inválidos
            invalidos = ['Unknown', 'Corgi Toys', 'N/A', '', 'Hot Wheels Design Team', 'TBD']
            if designer and len(designer) > 1 and designer not in invalidos and not designer.startswith('Category:'):
                return designer
    return None

def extract_number(wikitext):
    """Extraer número de colección del infobox."""
    if not wikitext:
        return None
    
    # Patrón en infobox: |number = 12345
    patterns = [
        r'\|\s*number\s*=\s*([A-Z0-9]+)',
        r'\|\s*[Nn]umber\s*=\s*([A-Z0-9]+)',
        r'number\s*=\s*([A-Z0-9]{3,})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, wikitext)
        if match:
            num = match.group(1).strip()
            if num and len(num) >= 3:
                return num
    return None

def extract_toy_number_from_table(wikitext):
    """Extraer Toy # de las tablas de versiones."""
    if not wikitext:
        return None
    
    # Buscar en tablas: |Toy # o | Col #
    patterns = [
        r'\|\s*Toy\s*#\s*\|\s*([A-Z0-9]+)',
        r'\|\s*[Cc]ol\.?\s*#\s*\|\s*([A-Z0-9]+)',
        r'\|\s*[Cc]ollector\s*[Nn]umber\s*\|\s*([A-Z0-9]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, wikitext)
        if match:
            num = match.group(1).strip()
            if num and len(num) >= 3:
                return num
    return None

def main():
    print("=== CORRECCIÓN FINAL DE DATOS ===\n")
    
    # Cargar resultados existentes
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Cargar catálogo
    with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
    
    # === 1. CORREGIR IMÁGENES SOSPECHOSAS ===
    print("Corrigiendo imágenes sospechosas...")
    
    imagenes_a_verificar = []
    for codigo, info in data['imagen'].items():
        nombre = info['nombre']
        titulo = info['titulo_wiki']
        nombre_palabra = nombre.lower().split()[0]
        if nombre_palabra not in titulo.lower():
            imagenes_a_verificar.append(codigo)
    
    print(f"  Imágenes a verificar: {len(imagenes_a_verificar)}")
    
    for codigo in imagenes_a_verificar:
        info = data['imagen'][codigo]
        nombre = info['nombre']
        anio = info['anio']
        
        print(f"  Buscando: {nombre} ({anio})...", end=' ', flush=True)
        titulo = search_fandom_exact(nombre, anio)
        
        if titulo:
            img_url = get_page_image(titulo)
            if img_url:
                data['imagen'][codigo]['titulo_wiki'] = titulo
                data['imagen'][codigo]['imagen_url'] = img_url
                print(f"OK ({titulo})")
            else:
                print(f"sin imagen en {titulo}")
        else:
            print("no encontrada")
        
        time.sleep(0.3)
    
    # === 2. MEJORAR EXTRACCIÓN DE NÚMEROS ===
    print("\nMejortando extracción de números...")
    
    for codigo in list(data['numero'].keys()):
        del data['numero'][codigo]
    
    # Recargar sin_numeros del catálogo
    sin_numero = [m for m in catalog if not m.get('t') or (isinstance(m.get('t'), str) and m.get('t', '').strip() == '') or (isinstance(m.get('t'), int) and m.get('t') == 0)]
    
    for i, modelo in enumerate(sin_numero):
        nombre = modelo['m']
        anio = modelo.get('y')
        codigo = modelo['i']
        
        print(f"  [{i+1}/{len(sin_numero)}] {nombre} ({anio})...", end=' ', flush=True)
        
        titulo = search_fandom_exact(nombre, anio)
        
        if titulo:
            wt = get_wikitext(titulo)
            num = extract_number(wt) or extract_toy_number_from_table(wt)
            if num:
                data['numero'][codigo] = {
                    'nombre': nombre,
                    'anio': anio,
                    'titulo_wiki': titulo,
                    'numero_coleccion': num
                }
                data['stats']['numero_encontrados'] += 1
                print(f"OK ({num})")
            else:
                print(f"sin número en {titulo}")
        else:
            print("no encontrada")
        
        time.sleep(0.3)
    
    # === 3. FILTRAR DISEÑADORES INVÁLIDOS ===
    print("\nFiltrando diseñadores inválidos...")
    
    invalidos = ['Unknown', 'Corgi Toys', 'N/A', '', 'Hot Wheels Design Team', 'TBD']
    a_eliminar = []
    for codigo, info in data['disenador'].items():
        if info['diseñador'] in invalidos:
            a_eliminar.append(codigo)
    
    for codigo in a_eliminar:
        del data['disenador'][codigo]
    
    print(f"  Eliminados {len(a_eliminar)} diseñadores inválidos")
    data['stats']['disenador_asignados'] = len(data['disenador'])
    
    # === 4. PROCESAR PENDIENTES ===
    # Los pendientes son los que no tienen diseñador asignado
    # Necesito la lista original de 666
    
    # Recuperar IDs del archivo sin_disenador_ids.json si existe
    sin_dis_file = os.path.join(DATA_DIR, 'sin_disenador_ids.json')
    if os.path.exists(sin_dis_file):
        with open(sin_dis_file, 'r', encoding='utf-8') as f:
            sin_dis_ids = json.load(f)
    else:
        # Usar diferencia entre 666 y asignados
        sin_dis_ids = []  # No tenemos la lista original
    
    asignados_ids = set(data['disenador'].keys())
    pendientes = [id for id in sin_dis_ids if id not in asignados_ids]
    
    print(f"\nPendientes a procesar: {len(pendientes)}")
    
    # Procesar pendientes
    for i, codigo in enumerate(pendientes):
        modelo = next((m for m in catalog if m['i'] == codigo), None)
        if not modelo:
            continue
        
        nombre = modelo['m']
        anio = modelo.get('y')
        
        if (i + 1) % 20 == 0:
            print(f"  [{i+1}/{len(pendientes)}] Procesando...", flush=True)
        
        titulo = search_fandom_exact(nombre, anio)
        
        if titulo:
            wt = get_wikitext(titulo)
            designer = extract_designer(wt)
            if designer:
                data['disenador'][codigo] = {
                    'nombre': nombre,
                    'anio': anio,
                    'titulo_wiki': titulo,
                    'diseñador': designer
                }
        
        time.sleep(0.3)
    
    # Actualizar stats
    data['stats']['disenador_asignados'] = len(data['disenador'])
    data['stats']['errores'] = data['stats']['sin_disenador_total'] - len(data['disenador'])
    
    # Guardar
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print("RESUMEN FINAL CORREGIDO")
    print(f"{'='*60}")
    print(f"Imágenes: {len(data['imagen'])}/{data['stats']['sin_imagen_total']}")
    print(f"Números: {len(data['numero'])}/{data['stats']['sin_numero_total']}")
    print(f"Diseñadores: {len(data['disenador'])}/{data['stats']['sin_disenador_total']}")
    print(f"\nGuardado en: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()