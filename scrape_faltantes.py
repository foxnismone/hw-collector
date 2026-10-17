#!/usr/bin/env python3
"""
Scrapear imágenes y diseñadores faltantes para Hot Wheels Collector.
Usa la API de Fandom (api.php) con User-Agent Mozilla y Referer.
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
DISENADORES_FILE = os.path.join(BASE_DIR, 'data', 'disenadores.json')
IMAGENES_OUTPUT = os.path.join(BASE_DIR, 'data', 'imagenes_faltantes.json')
PROYECTOS_OUTPUT = os.path.join(BASE_DIR, 'data', 'proyectos_disenadores.json')

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
    # Remover paréntesis y sufijos comunes
    name = re.sub(r'\s*\([^)]*\)', '', name)
    # Remover caracteres especiales
    name = re.sub(r'["\'&]', '', name)
    # Limpiar espacios
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
    
    # Buscar en namespace de archivos (namespace=6)
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
            # Obtener URL real de la imagen
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
                        # Usar miniatura escalada
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
    print(f"SCRAPING DE IMÁGENES FALTANTES: {len(sin_imagen)} modelos")
    print(f"{'='*60}")
    
    # Preparar títulos para búsqueda en batch
    # En Fandom, los títulos de páginas de modelos pueden tener sufijos
    titulos_busqueda = []
    modelo_por_titulo = {}
    
    for modelo in sin_imagen:
        nombre = clean_model_name(modelo.get('m', ''))
        anio = modelo.get('y')
        
        # Título principal: nombre del modelo
        titulo_principal = nombre
        titulos_busqueda.append(titulo_principal)
        modelo_por_titulo[titulo_principal] = modelo
        
        # Variante con año
        if anio:
            titulo_anio = f"{nombre} ({anio})"
            titulos_busqueda.append(titulo_anio)
            modelo_por_titulo[titulo_anio] = modelo
        
        # Variante solo nombre (sin año) ya está arriba
    
    # Eliminar duplicados manteniendo orden
    titulos_unicos = list(dict.fromkeys(titulos_busqueda))
    print(f"Títulos únicos a buscar: {len(titulos_unicos)}")
    
    # Procesar en batches
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
        
        # Rate limiting suave
        if (i + 1) % 10 == 0:
            time.sleep(0.5)
    
    print(f"Imágenes encontradas (pageimages): {len(imagenes_encontradas)}")
    
    # Para los que no encontraron, búsqueda individual
    faltantes = [m for m in sin_imagen if m.get('i') not in imagenes_encontradas]
    print(f"Faltantes tras pageimages: {len(faltantes)}")
    
    if faltantes:
        print("Búsqueda individual en namespace de archivos...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {}
            for modelo in faltantes[:200]:  # Limitar a 200 para no sobrecargar
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

# ── Parte 2: Proyectos de diseñadores ───────────────────────────
def extraer_proyectos_disenador(nombre_disenador):
    """Extraer nombres de modelos de la página de un diseñador."""
    titulo = nombre_disenador.replace(' ', '_')
    params = {
        'action': 'parse',
        'page': titulo,
        'prop': 'text',
        'format': 'json',
        'formatversion': '2',
    }
    data = api_fandom(params)
    if not data or 'parse' not in data:
        return None
    
    parse_data = data['parse']
    if isinstance(parse_data, str):
        return None
    
    # Con formatversion=2, 'text' es un string directamente
    html = parse_data.get('text', '')
    if not html or not isinstance(html, str):
        return None
    
    # Extraer nombres de modelos desde enlaces wiki
    # Buscar patrones [[Nombre]] o [[Nombre|texto]]
    nombres = set()
    
    # Enlaces wiki [[Nombre]] o [[Nombre|texto]]
    for match in re.finditer(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', html):
        nombre = match.group(1).strip()
        if nombre and len(nombre) > 2 and not nombre.startswith('Category:') and not nombre.startswith('File:') and not nombre.startswith('Image:'):
            nombres.add(nombre)
    
    # También buscar en tablas HTML (<td><a href="/wiki/Nombre">)
    for match in re.finditer(r'<a[^>]*href="/wiki/([^"]+)"[^>]*>([^<]+)</a>', html):
        href = match.group(1)
        texto = match.group(2).strip()
        # Usar el texto del enlace si es significativo
        if texto and len(texto) > 2 and not texto.startswith('Category:'):
            nombres.add(texto)
    
    return list(nombres)

def scrape_proyectos_disenadores(disenadores, sin_disenador):
    """Extraer proyectos de diseñadores y asignar a modelos sin diseñador."""
    print(f"\n{'='*60}")
    print(f"SCRAPING DE PROYECTOS DE DISEÑADORES")
    print(f"Diseñadores: {len(disenadores)}")
    print(f"Modelos sin diseñador: {len(sin_disenador)}")
    print(f"{'='*60}")
    
    # Extraer nombres de modelos de cada diseñador
    proyectos_disenador = {}
    nombres_por_disenador = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for nombre_disenador in disenadores.keys():
            future = executor.submit(extraer_proyectos_disenador, nombre_disenador)
            futures[future] = nombre_disenador
        
        for future in concurrent.futures.as_completed(futures):
            nombre = futures[future]
            try:
                nombres = future.result()
                if nombres:
                    nombres_por_disenador[nombre] = nombres
                    proyectos_disenador[nombre] = nombres
                    print(f"  {nombre}: {len(nombres)} proyectos")
                else:
                    print(f"  {nombre}: sin proyectos")
            except Exception as e:
                print(f"  ERROR {nombre}: {e}")
    
    print(f"\nDiseñadores con proyectos: {len(proyectos_disenador)}")
    print(f"Total proyectos extraídos: {sum(len(v) for v in proyectos_disenador.values())}")
    
    # Hacer matching: asignar diseñador a modelos sin diseñador
    print(f"\nAsignando diseñadores a modelos sin diseñador...")
    asignaciones = {}
    modelos_asignados = set()
    
    # Crear índice de nombres de modelos del catálogo
    modelo_por_nombre = {}
    for modelo in sin_disenador:
        nombre = modelo.get('m', '').strip()
        if nombre:
            modelo_por_nombre[normalize_name(nombre)] = modelo
    
    # Para cada diseñador, buscar coincidencias
    for nombre_disenador, proyectos in nombres_por_disenador.items():
        for proyecto in proyectos:
            nombre_norm = normalize_name(proyecto)
            if nombre_norm in modelo_por_nombre:
                modelo = modelo_por_nombre[nombre_norm]
                model_id = modelo.get('i')
                if model_id and model_id not in modelos_asignados:
                    asignaciones[model_id] = {
                        'modelo': modelo.get('m'),
                        'diseñador': nombre_disenador,
                        'proyecto_fandom': proyecto,
                    }
                    modelos_asignados.add(model_id)
    
    print(f"Modelos con diseñador asignado: {len(asignaciones)}")
    return proyectos_disenador, asignaciones

# ── Main ────────────────────────────────────────────────────────
def main():
    print("="*60)
    print("HOT WHEELS COLLECTOR - SCRAPE FALTANTES")
    print("="*60)
    
    # Cargar datos
    with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
    
    with open(DISENADORES_FILE, 'r', encoding='utf-8') as f:
        disenadores = json.load(f)
    
    sin_imagen = [m for m in catalog if not m.get('im')]
    sin_disenador = [m for m in catalog if not m.get('diseñador')]
    
    # Parte 1: Imágenes
    imagenes = scrape_imagenes_faltantes(sin_imagen)
    
    # Parte 2: Proyectos de diseñadores
    proyectos, asignaciones = scrape_proyectos_disenadores(disenadores, sin_disenador)
    
    # Guardar resultados
    with open(IMAGENES_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(imagenes, f, ensure_ascii=False, indent=2)
    print(f"\nGuardado: {IMAGENES_OUTPUT}")
    
    with open(PROYECTOS_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump({
            'proyectos_por_disenador': proyectos,
            'asignaciones_modelos': asignaciones,
        }, f, ensure_ascii=False, indent=2)
    print(f"Guardado: {PROYECTOS_OUTPUT}")
    
    # Resumen final
    print(f"\n{'='*60}")
    print("RESUMEN FINAL")
    print(f"{'='*60}")
    print(f"Imágenes encontradas: {len(imagenes)}")
    print(f"Proyectos de diseñadores: {sum(len(v) for v in proyectos.values())}")
    print(f"Modelos con diseñador asignado: {len(asignaciones)}")
    print(f"Modelos sin imagen restantes: {len(sin_imagen) - len(imagenes)}")
    print(f"Modelos sin diseñador restantes: {len(sin_disenador) - len(asignaciones)}")

if __name__ == '__main__':
    main()
