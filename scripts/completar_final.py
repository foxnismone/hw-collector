#!/usr/bin/env python3
"""
Script final para completar datos faltantes del catálogo Hot Wheels:
- 7 modelos sin imagen
- 13 modelos sin número de colección (tool number)
- 666 modelos sin diseñador

Usa la API de Fandom (hotwheels.fandom.com/api.php)
Guarda resultados en data/completar_final.json
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
    """Llamada a la API de Fandom con reintentos."""
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
                print(f"    ERROR API: {e}", file=sys.stderr)
                return None

def search_fandom_page(nombre, anio=None):
    """Buscar una página en Fandom por nombre de modelo."""
    query = f"Hot Wheels {nombre}"
    if anio:
        query += f" {anio}"
    
    data = api_fandom({
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'srlimit': '5',
        'format': 'json',
        'formatversion': '2'
    })
    
    if not data:
        return None
    
    results = data.get('query', {}).get('search', [])
    return results

def get_wikitext(titulo):
    """Obtener el wikitext de una página."""
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

def extract_designer(wikitext):
    """Extraer diseñador del wikitext."""
    if not wikitext:
        return None
    
    # Patrones comunes en infobox de Fandom
    patterns = [
        r'[|]\s*[Dd]esigner\s*=\s*\[\[([^\]|]+)',
        r'[|]\s*[Dd]esigner\s*=\s*([^\n|]+)',
        r'\|\s*[Dd]esigner\s*=\s*\[\[([^\]|]+)',
        r'[Dd]esigner\s*=\s*\[\[([^\]|]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, wikitext)
        if match:
            designer = match.group(1).strip()
            # Limpiar markup wiki
            designer = re.sub(r'\[\[|\]\]', '', designer)
            designer = designer.strip()
            if designer and len(designer) > 1 and not designer.startswith('Category:'):
                return designer
    
    return None

def extract_toy_number(wikitext):
    """Extraer número de colección del wikitext."""
    if not wikitext:
        return None
    
    # Buscar en tablas o infobox
    patterns = [
        r'[|]\s*[Tt]oy\s*#\s*=\s*([A-Z0-9]+)',
        r'[|]\s*[Cc]ol\.?#\s*=\s*([A-Z0-9]+)',
        r'[|]\s*[Cc]ollector\s*[Nn]umber\s*=\s*([A-Z0-9]+)',
        r'Toy\s*#\s*([A-Z0-9]{3,})',
        r'Col\.?#\s*([A-Z0-9]{3,})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, wikitext)
        if match:
            num = match.group(1).strip()
            if num and len(num) >= 3:
                return num
    
    return None

def get_page_image(titulo):
    """Obtener la imagen principal de una página."""
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
    # Con formatversion=2, pages es una lista
    if isinstance(pages, list):
        for page_data in pages:
            if 'thumbnail' in page_data:
                return page_data['thumbnail']['source']
    elif isinstance(pages, dict):
        for page_id, page_data in pages.items():
            if 'thumbnail' in page_data:
                return page_data['thumbnail']['source']
    
    return None

def find_best_match(results, nombre_modelo, anio=None):
    """Encontrar la mejor coincidencia entre los resultados de búsqueda."""
    if not results:
        return None
    
    nombre_lower = nombre_modelo.lower().strip()
    # Quitar sufijos como "(2nd Color)"
    nombre_base = re.sub(r'\s*\(.*?\)', '', nombre_lower).strip()
    
    for r in results:
        titulo = r['title']
        titulo_lower = titulo.lower()
        
        # Coincidencia exacta
        if nombre_lower == titulo_lower:
            return titulo
        
        # Coincidencia por nombre base
        if nombre_base and nombre_base in titulo_lower:
            return titulo
    
    # Si no hay coincidencia, devolver el primero si parece relevante
    if results:
        first_title = results[0]['title']
        # Verificar que no sea una lista
        if 'List of' not in first_title:
            return first_title
    
    return None

def main():
    print("=== COMPLETAR DATOS FALTANTES DEL CATÁLOGO ===\n")
    
    # Cargar catálogo
    with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
    print(f"Catálogo cargado: {len(catalog)} modelos")
    
    # Identificar faltantes
    sin_imagen = [m for m in catalog if not m.get('im')]
    sin_numero = [m for m in catalog if not m.get('t') or (isinstance(m.get('t'), str) and m.get('t', '').strip() == '') or (isinstance(m.get('t'), (int, float)) and m.get('t') == 0)]
    sin_disenador = [m for m in catalog if not m.get('diseñador') or (isinstance(m.get('diseñador'), str) and m.get('diseñador', '').strip() == '')]
    
    print(f"Sin imagen: {len(sin_imagen)}")
    print(f"Sin número (tool #): {len(sin_numero)}")
    print(f"Sin diseñador: {len(sin_disenador)}")
    
    resultado = {
        'imagen': {},
        'numero': {},
        'disenador': {},
        'stats': {
            'sin_imagen_total': len(sin_imagen),
            'sin_numero_total': len(sin_numero),
            'sin_disenador_total': len(sin_disenador),
            'imagen_encontradas': 0,
            'numero_encontrados': 0,
            'disenador_asignados': 0,
            'errores': 0
        }
    }
    
    # === 1. COMPLETAR IMÁGENES (7 modelos) ===
    print(f"\n{'='*60}")
    print("FASE 1: Buscando imágenes faltantes...")
    print(f"{'='*60}")
    
    for i, modelo in enumerate(sin_imagen):
        nombre = modelo['m']
        anio = modelo.get('y')
        codigo = modelo['i']
        
        print(f"[{i+1}/{len(sin_imagen)}] {nombre} ({anio})...", end=' ', flush=True)
        
        results = search_fandom_page(nombre, anio)
        titulo = find_best_match(results, nombre, anio)
        
        if titulo:
            img_url = get_page_image(titulo)
            if img_url:
                resultado['imagen'][codigo] = {
                    'nombre': nombre,
                    'anio': anio,
                    'titulo_wiki': titulo,
                    'imagen_url': img_url
                }
                resultado['stats']['imagen_encontradas'] += 1
                print(f"OK ({titulo})")
            else:
                print(f"sin imagen en {titulo}")
                resultado['stats']['errores'] += 1
        else:
            print("no encontrada")
            resultado['stats']['errores'] += 1
        
        time.sleep(0.3)
    
    # === 2. COMPLETAR NÚMEROS (13 modelos) ===
    print(f"\n{'='*60}")
    print("FASE 2: Buscando números de colección faltantes...")
    print(f"{'='*60}")
    
    for i, modelo in enumerate(sin_numero):
        nombre = modelo['m']
        anio = modelo.get('y')
        codigo = modelo['i']
        
        print(f"[{i+1}/{len(sin_numero)}] {nombre} ({anio})...", end=' ', flush=True)
        
        results = search_fandom_page(nombre, anio)
        titulo = find_best_match(results, nombre, anio)
        
        if titulo:
            wt = get_wikitext(titulo)
            num = extract_toy_number(wt)
            if num:
                resultado['numero'][codigo] = {
                    'nombre': nombre,
                    'anio': anio,
                    'titulo_wiki': titulo,
                    'numero_coleccion': num
                }
                resultado['stats']['numero_encontrados'] += 1
                print(f"OK ({num})")
            else:
                print(f"sin número en {titulo}")
                resultado['stats']['errores'] += 1
        else:
            print("no encontrada")
            resultado['stats']['errores'] += 1
        
        time.sleep(0.3)
    
    # === 3. ASIGNAR DISEÑADORES (666 modelos) ===
    print(f"\n{'='*60}")
    print("FASE 3: Asignando diseñadores faltantes...")
    print(f"{'='*60}")
    
    total = len(sin_disenador)
    for i, modelo in enumerate(sin_disenador):
        nombre = modelo['m']
        anio = modelo.get('y')
        codigo = modelo['i']
        
        if (i + 1) % 50 == 0 or i == 0:
            print(f"[{i+1}/{total}] Procesando...", flush=True)
        
        results = search_fandom_page(nombre, anio)
        titulo = find_best_match(results, nombre, anio)
        
        if titulo:
            wt = get_wikitext(titulo)
            designer = extract_designer(wt)
            if designer:
                resultado['disenador'][codigo] = {
                    'nombre': nombre,
                    'anio': anio,
                    'titulo_wiki': titulo,
                    'diseñador': designer
                }
                resultado['stats']['disenador_asignados'] += 1
        
        time.sleep(0.3)
        
        # Guardar progreso cada 100
        if (i + 1) % 100 == 0:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(resultado, f, ensure_ascii=False, indent=2)
            print(f"  [Guardado progreso: {i+1}/{total}]")
    
    # Guardar resultado final
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print("RESUMEN FINAL")
    print(f"{'='*60}")
    print(f"Imágenes encontradas: {resultado['stats']['imagen_encontradas']}/{len(sin_imagen)}")
    print(f"Números encontrados: {resultado['stats']['numero_encontrados']}/{len(sin_numero)}")
    print(f"Diseñadores asignados: {resultado['stats']['disenador_asignados']}/{len(sin_disenador)}")
    print(f"Errores: {resultado['stats']['errores']}")
    print(f"\nResultados guardados en: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()