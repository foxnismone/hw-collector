#!/usr/bin/env python3
"""
Busca imágenes de los modelos antiguos en Fandom Wiki usando la API.
Actualiza el catálogo con las URLs de las imágenes.

Uso:
    python build/buscar_imagenes.py
"""

import json
import time
import urllib.request
import urllib.parse
import urllib.error
import re
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent / 'data'
CATALOG_FILE = DATA_DIR / 'catalog_web.json'

TIMEOUT = 15
DELAY = 0.5  # segundos entre requests

def api_fandom(params):
    """Hace un request a la API de Fandom."""
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None

def obtener_imagen_de_pagina(nombre_modelo):
    """Busca la imagen de un modelo en su página de Fandom."""
    # Buscar la página del modelo
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': f'intitle:{nombre_modelo} casting',
        'srnamespace': '0',
        'format': 'json',
        'srlimit': '1'
    }
    data = api_fandom(params)
    if not data:
        return None
    
    resultados = data.get('query', {}).get('search', [])
    if not resultados:
        return None
    
    titulo = resultados[0].get('title', '')
    if not titulo:
        return None
    
    # Obtener imágenes de la página
    params = {
        'action': 'parse',
        'page': titulo,
        'format': 'json',
        'prop': 'images'
    }
    data = api_fandom(params)
    if not data:
        return None
    
    imagenes = data.get('parse', {}).get('images', [])
    if not imagenes:
        return None
    
    # Buscar la primera imagen que no sea un logo o icono
    for img in imagenes:
        if img and not any(x in img.lower() for x in ['logo', 'icon', 'button', 'sprite']):
            # Obtener la URL de la imagen
            params = {
                'action': 'query',
                'titles': f'File:{img}',
                'prop': 'imageinfo',
                'iiprop': 'url',
                'format': 'json'
            }
            data = api_fandom(params)
            if not data:
                continue
            
            pages = data.get('query', {}).get('pages', {})
            for p in pages.values():
                ii = p.get('imageinfo', [{}])[0]
                url = ii.get('url', '')
                if url:
                    return url.split('/revision/')[0]  # Quitar parámetros de revisión
    
    return None

def main():
    # Cargar catálogo
    with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
        catalogo = json.load(f)
    
    print(f"Total modelos: {len(catalogo)}")
    
    # Buscar imágenes para modelos que no tienen imagen
    modelos_sin_imagen = [c for c in catalogo if not c.get('im')]
    print(f"Modelos sin imagen: {len(modelos_sin_imagen)}")
    
    # Limitar a los primeros 50 para no sobrecargar
    modelos_a_buscar = modelos_sin_imagen[:50]
    
    encontradas = 0
    for i, modelo in enumerate(modelos_a_buscar):
        nombre = modelo.get('m', '')
        print(f"  [{i+1}/{len(modelos_a_buscar)}] Buscando imagen de {nombre}...")
        
        url = obtener_imagen_de_pagina(nombre)
        if url:
            modelo['im'] = url
            encontradas += 1
            print(f"    ✅ {url[:60]}")
        else:
            print(f"    ❌ No encontrada")
        
        time.sleep(DELAY)
    
    # Guardar catálogo actualizado
    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalogo, f, ensure_ascii=False, separators=(',', ':'))
    
    print(f"\n{'='*50}")
    print(f"✅ Imágenes encontradas: {encontradas}")
    print(f"✅ Total con imagen: {len([c for c in catalogo if c.get('im')])}")

if __name__ == '__main__':
    main()
