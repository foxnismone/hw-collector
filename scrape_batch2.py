#!/usr/bin/env python3
"""
Buscar imágenes faltantes en Fandom (batch2) para modelos sin imagen.
Reutiliza la lógica probada de scrape_faltantes.py.
Guarda resultados en data/imagenes_batch2.json.
"""

import json
import urllib.request
import urllib.parse
import concurrent.futures
import re
import time
import os
from collections import defaultdict

# ── Configuración ──────────────────────────────────────────────
BASE_DIR = r'C:\Users\GODZILLA24H2\Desktop\hotwheels_collector'
CATALOG_FILE = os.path.join(BASE_DIR, 'data', 'catalog_web.json')
IMAGENES_OUTPUT = os.path.join(BASE_DIR, 'data', 'imagenes_batch2.json')

API_URL = 'https://hotwheels.fandom.com/api.php'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (hotwheels-research)',
    'Referer': 'https://hotwheels.fandom.com/',
}

MAX_WORKERS = 8
BATCH_SIZE = 45  # títulos por request para pageimages

# ── Helpers API ─────────────────────────────────────────────────
def api_fandom(params, retries=3):
    """Llamada a la API de Fandom con reintentos."""
    url = API_URL + '?' + urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            if attempt == retries - 1:
                print(f"  ERROR API tras {retries} intentos: {e}")
                return None
            time.sleep(1 + attempt)

def normalize_name(name):
    """Normalizar nombre para comparar."""
    return re.sub(r'\s+', ' ', name.strip().lower())

def clean_model_name(name):
    """Limpiar nombre de modelo para búsqueda en Fandom."""
    name = re.sub(r'\s*\([^)]*\)', '', name)
    name = re.sub(r'["\'&]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

# ── Parte 1: Imágenes faltantes ─────────────────────────────────
def buscar_imagenes_batch(titles_batch):
    """Buscar imágenes para un batch de títulos usando pageimages."""
    titles_str = '|'.join(titles_batch)
    params = {
        'action': 'query',
        'prop': 'pageimages',
        'titles': titles_str,
        'piprop': 'thumbnail',
        'pithumbsize': '200',
        'redirects': '1',
        'format': 'json',
        'formatversion': '2',
    }
    data = api_fandom(params)
    if not data or 'query' not in data:
        return {}
    
    resultados = {}
    pages = data['query'].get('pages', [])
    for page in pages:
        title = page.get('title', '')
        thumbnail = page.get('thumbnail', {})
        if thumbnail and thumbnail.get('source'):
            resultados[title] = {
                'image_url': thumbnail['source'],
                'width': thumbnail.get('width', 200),
                'height': thumbnail.get('height', 200),
                'source': 'pageimages',
            }
    return resultados

def buscar_imagen_por_nombre(nombre_modelo, anio):
    """Buscar imagen de un modelo individual por búsqueda en namespace de archivo."""
    nombre_clean = clean_model_name(nombre_modelo)
    if not nombre_clean:
        return None
    
    search_term = f"{nombre_clean} {anio}" if anio else nombre_clean
    params = {
        'action': 'query',
        'list': 'search',
        'srnamespace': '6',
        'srsearch': search_term,
        'srlimit': '3',
        'format': 'json',
        'formatversion': '2',
    }
    data = api_fandom(params)
    if not data or 'query' not in data:
        return None
    
    searches = data['query'].get('search', [])
    for result in searches:
        file_title = result.get('title', '')
        if file_title.startswith('File:'):
            params2 = {
                'action': 'query',
                'titles': file_title,
                'prop': 'imageinfo',
                'iiprop': 'url',
                'format': 'json',
                'formatversion': '2',
            }
            data2 = api_fandom(params2)
            if data2 and 'query' in data2:
                pages = data2['query'].get('pages', [])
                for page in pages:
                    imageinfo = page.get('imageinfo', [])
                    if imageinfo and imageinfo[0].get('url'):
                        url = imageinfo[0]['url']
                        if '/revision/latest' not in url:
                            url = url.rsplit('/', 1)[0] + '/revision/latest/scale-to-width-down/200'
                        return {
                            'image_url': url,
                            'source': 'search+imageinfo',
                            'file': file_title,
                        }
    return None

def scrape_imagenes_faltantes(sin_imagen):
    """Scrapear imágenes para todos los modelos sin imagen."""
    print(f"\n{'='*60}")
    print(f"SCRAPING DE IMÁGENES FALTANTES (BATCH2): {len(sin_imagen)} modelos")
    print(f"{'='*60}")
    
    titulos_busqueda = []
    modelo_por_titulo = {}
    
    for modelo in sin_imagen:
        nombre = clean_model_name(modelo.get('m', ''))
        anio = modelo.get('y')
        
        titulo_principal = nombre
        titulos_busqueda.append(titulo_principal)
        modelo_por_titulo[titulo_principal] = modelo
        
        if anio:
            titulo_anio = f"{nombre} ({anio})"
            titulos_busqueda.append(titulo_anio)
            modelo_por_titulo[titulo_anio] = modelo
    
    titulos_unicos = list(dict.fromkeys(titulos_busqueda))
    print(f"Títulos únicos a buscar: {len(titulos_unicos)}")
    
    imagenes_encontradas = {}
    batches = [titulos_unicos[i:i+BATCH_SIZE] for i in range(0, len(titulos_unicos), BATCH_SIZE)]
    print(f"Batches de {BATCH_SIZE}: {len(batches)}")
    
    for i, batch in enumerate(batches):
        print(f"  Batch {i+1}/{len(batches)} ({len(batch)} títulos)...")
        resultados = buscar_imagenes_batch(batch)
        
        for titulo, info in resultados.items():
            if titulo in modelo_por_titulo:
                modelo = modelo_por_titulo[titulo]
                model_id = modelo.get('i')
                if model_id and model_id not in imagenes_encontradas:
                    imagenes_encontradas[model_id] = {
                        'modelo': modelo.get('m'),
                        'anio': modelo.get('y'),
                        'titulo_fandom': titulo,
                        **info,
                    }
        
        if (i + 1) % 10 == 0:
            time.sleep(0.5)
    
    print(f"Imágenes encontradas (pageimages): {len(imagenes_encontradas)}")
    
    # Búsqueda individual para los faltantes
    faltantes = [m for m in sin_imagen if m.get('i') not in imagenes_encontradas]
    print(f"Faltantes tras pageimages: {len(faltantes)}")
    
    if faltantes:
        print("Búsqueda individual en namespace de archivos...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {}
            for modelo in faltantes:
                future = executor.submit(
                    buscar_imagen_por_nombre,
                    modelo.get('m', ''),
                    modelo.get('y')
                )
                futures[future] = modelo
            
            for future in concurrent.futures.as_completed(futures):
                modelo = futures[future]
                try:
                    resultado = future.result()
                    if resultado:
                        model_id = modelo.get('i')
                        imagenes_encontradas[model_id] = {
                            'modelo': modelo.get('m'),
                            'anio': modelo.get('y'),
                            'titulo_fandom': modelo.get('m'),
                            **resultado,
                        }
                except Exception as e:
                    print(f"  Error en búsqueda individual: {e}")
    
    print(f"Imágenes totales encontradas: {len(imagenes_encontradas)}")
    return imagenes_encontradas

# ── Main ────────────────────────────────────────────────────────
def main():
    print("="*60)
    print("HOT WHEELS COLLECTOR - BATCH2 IMÁGENES FALTANTES")
    print("="*60)
    
    with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
    
    sin_imagen = [m for m in catalog if not m.get('im')]
    print(f"Total modelos en catálogo: {len(catalog)}")
    print(f"Modelos sin imagen: {len(sin_imagen)}")
    
    imagenes = scrape_imagenes_faltantes(sin_imagen)
    
    with open(IMAGENES_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(imagenes, f, ensure_ascii=False, indent=2)
    print(f"\nGuardado: {IMAGENES_OUTPUT}")
    
    print(f"\n{'='*60}")
    print("RESUMEN FINAL")
    print(f"{'='*60}")
    print(f"Imágenes encontradas: {len(imagenes)}")
    print(f"Modelos sin imagen restantes: {len(sin_imagen) - len(imagenes)}")
    
    # Estadísticas por fuente
    fuentes = defaultdict(int)
    for info in imagenes.values():
        fuentes[info.get('source', 'unknown')] += 1
    print(f"Por fuente: {dict(fuentes)}")

if __name__ == '__main__':
    main()
