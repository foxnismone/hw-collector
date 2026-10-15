#!/usr/bin/env python3
"""
Descarga todas las imágenes externas (Wikia) al servidor local.
Actualiza el catálogo con URLs locales.

Uso:
    python build/descargar_imagenes.py
"""

import json
import urllib.request
import hashlib
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
CATALOG_FILE = DATA_DIR / 'catalog_web.json'
IMG_CACHE = DATA_DIR / 'img_cache'
IMG_CACHE.mkdir(parents=True, exist_ok=True)

def descargar_imagen(url):
    """Descarga una imagen y devuelve la ruta local."""
    key = hashlib.md5(url.encode()).hexdigest()
    ext = url.split('.')[-1].split('?')[0]
    if len(ext) > 4:
        ext = 'jpg'
    cache_path = IMG_CACHE / f"{key}.{ext}"
    
    if not cache_path.exists():
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            with urllib.request.urlopen(req, timeout=15) as resp:
                with open(cache_path, 'wb') as f:
                    f.write(resp.read())
            return str(cache_path.relative_to(DATA_DIR.parent))
        except Exception as e:
            return None
    else:
        return str(cache_path.relative_to(DATA_DIR.parent))

def main():
    # Cargar catálogo
    with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
        catalogo = json.load(f)
    
    print(f"Total modelos: {len(catalogo)}")
    
    # Buscar imágenes externas
    urls_externas = [c for c in catalogo if c.get('im', '').startswith('http')]
    print(f"Imágenes externas: {len(urls_externas)}")
    
    # Descargar imágenes
    descargadas = 0
    fallidas = 0
    for i, modelo in enumerate(urls_externas):
        url = modelo['im']
        print(f"  [{i+1}/{len(urls_externas)}] {modelo['m']}...")
        
        ruta_local = descargar_imagen(url)
        if ruta_local:
            modelo['im'] = ruta_local
            descargadas += 1
        else:
            fallidas += 1
            print(f"    ❌ Falló")
        
        time.sleep(0.2)
    
    # Guardar catálogo actualizado
    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalogo, f, ensure_ascii=False, separators=(',', ':'))
    
    print(f"\n{'='*50}")
    print(f"✅ Descargadas: {descargadas}")
    print(f"❌ Fallidas: {fallidas}")
    print(f"Total con imagen local: {len([c for c in catalogo if c.get('im')])}")

if __name__ == '__main__':
    main()
