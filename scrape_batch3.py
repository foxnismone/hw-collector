#!/usr/bin/env python3
import json
import urllib.parse
import urllib.request
import time
import sys
import os

DATA_DIR = r'C:\Users\GODZILLA24H2\Desktop\hotwheels_collector\data'
PROGRESS_FILE = os.path.join(DATA_DIR, 'imagenes_batch3.json')
PENDINGS_FILE = os.path.join(DATA_DIR, 'pendientes_batch3.json')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def search_fandom(title, year=None):
    query = f"Hot Wheels {title}"
    if year:
        query += f" {year}"
    
    url = f"https://hotwheels.fandom.com/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json&srlimit=1"
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        results = data.get('query', {}).get('search', [])
        if results:
            page_title = results[0]['title']
            return get_page_image(page_title)
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
    
    return None

def get_page_image(page_title):
    url = f"https://hotwheels.fandom.com/api.php?action=query&titles={urllib.parse.quote(page_title)}&prop=pageimages&format=json&pithumbsize=300"
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if 'thumbnail' in page_data:
                return page_data['thumbnail']['source']
    except Exception as e:
        print(f"  Error img: {e}", file=sys.stderr)
    
    return None

with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
    progreso = json.load(f)

with open(PENDINGS_FILE, 'r', encoding='utf-8') as f:
    pendientes = json.load(f)

print(f"Pendientes a procesar: {len(pendientes)}", flush=True)

encontradas_nuevas = 0
for i, modelo in enumerate(pendientes):
    nombre = modelo['m']
    anio = modelo.get('y')
    codigo = modelo['i']
    
    print(f"[{i+1}/{len(pendientes)}] {nombre} ({anio})...", end=' ', flush=True)
    
    img_url = search_fandom(nombre, anio)
    
    if img_url:
        progreso[codigo] = {
            'nombre': nombre,
            'anio': anio,
            'imagen_url': img_url
        }
        encontradas_nuevas += 1
        print(f"OK", flush=True)
    else:
        print("no", flush=True)
    
    if (i + 1) % 10 == 0:
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progreso, f, ensure_ascii=False, indent=2)
        print(f"  [Guardado: {i+1}/{len(pendientes)}]", flush=True)
    
    time.sleep(0.3)

with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
    json.dump(progreso, f, ensure_ascii=False, indent=2)

print(f"\nDONE: {encontradas_nuevas} nuevas encontradas. Total: {len(progreso)}")
