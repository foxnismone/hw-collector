#!/usr/bin/env python3
"""
Scraper de catálogo para HW Collector.
Busca nuevos modelos de Hot Wheels en múltiples fuentes
y actualiza el archivo catalog_web.json.

Uso:
    python build/scraper_catalogo.py --sync

Fuentes:
    1. Hot Wheels Wiki (Fandom) — lista de modelos por año
    2. SmartWheelers — base de conocimiento
    3. HW Price Guide — catálogo con valores
    4. Reddit r/HotWheels — lanzamientos nuevos
"""

import sys
import json
import re
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime

# Configuración
TIMEOUT = 15
DELAY_BETWEEN_SOURCES = 2
DATA_DIR = Path(__file__).parent.parent / 'data'
CATALOG_FILE = DATA_DIR / 'catalog_web.json'

# Colores para output
class C:
    OK = '\033[92m'
    WARN = '\033[93m'
    ERR = '\033[91m'
    INFO = '\033[94m'
    END = '\033[0m'

def log(msg, color=C.INFO):
    print(f"{color}{msg}{C.END}")

def fetch_url(url, headers=None):
    """Hace un request HTTP con timeout y headers completos de navegador."""
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    req.add_header('Accept-Language', 'es-ES,es;q=0.9,en;q=0.8')
    req.add_header('Accept-Encoding', 'identity')
    req.add_header('Connection', 'keep-alive')
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None

def cargar_catalogo():
    """Carga el catálogo actual."""
    if CATALOG_FILE.exists():
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_catalogo(catalogo):
    """Guarda el catálogo actualizado."""
    CATALOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalogo, f, ensure_ascii=False, separators=(',', ':'))
    log(f"Catálogo guardado: {len(catalogo)} modelos", C.OK)

def scrapear_hw_wiki(ano):
    """Busca modelos de un año específico en Hot Wheels Wiki."""
    log(f"  Buscando en Hot Wheels Wiki ({ano})...", C.INFO)
    
    # URLs de listas por año
    urls = [
        f"https://hotwheels.fandom.com/wiki/List_of_{ano}_Hot_Wheels",
        f"https://hotwheels.fandom.com/wiki/{ano}_New_Models",
    ]
    
    modelos = []
    for url in urls:
        html = fetch_url(url)
        if not html:
            continue
        
        # Buscar patrones de modelos
        # Formato común: "FRN78 - '18 Dodge Challenger"
        patron = re.compile(r'([A-Z]{3}\d{2})\s*[-–]\s*([^<\n]+)', re.IGNORECASE)
        matches = patron.findall(html)
        
        for codigo, nombre in matches:
            nombre = nombre.strip()
            if len(nombre) > 3 and len(nombre) < 100:
                modelos.append({
                    'i': codigo.upper(),
                    'm': nombre,
                    'k': 'Desconocido',
                    'y': ano,
                    'fuente': 'Hot Wheels Wiki'
                })
        
        if modelos:
            log(f"  HW Wiki: {len(modelos)} modelos encontrados", C.OK)
            return modelos
    
    log(f"  HW Wiki: no encontrado", C.WARN)
    return []

def scrapear_smartwheelers():
    """Busca modelos nuevos en SmartWheelers."""
    log(f"  Buscando en SmartWheelers...", C.INFO)
    
    url = "https://www.smartwheelers.com/new-releases"
    html = fetch_url(url)
    if not html:
        log(f"  SmartWheelers: sin respuesta", C.WARN)
        return []
    
    # Buscar patrones de modelos
    patron = re.compile(r'([A-Z]{3}\d{2})\s*[-–]\s*([^<\n]+)', re.IGNORECASE)
    matches = patron.findall(html)
    
    modelos = []
    for codigo, nombre in matches:
        nombre = nombre.strip()
        if len(nombre) > 3 and len(nombre) < 100:
            modelos.append({
                'i': codigo.upper(),
                'm': nombre,
                'k': 'Desconocido',
                'y': datetime.now().year,
                'fuente': 'SmartWheelers'
            })
    
    if modelos:
        log(f"  SmartWheelers: {len(modelos)} modelos encontrados", C.OK)
    
    return modelos

def scrapear_reddit():
    """Busca discusiones de nuevos modelos en Reddit."""
    log(f"  Buscando en Reddit r/HotWheels...", C.INFO)
    
    url = "https://www.reddit.com/r/HotWheels/new.json?limit=25"
    html = fetch_url(url, headers={'Accept': 'application/json'})
    if not html:
        log(f"  Reddit: sin respuesta", C.WARN)
        return []
    
    try:
        data = json.loads(html)
        posts = data.get('data', {}).get('children', [])
        
        modelos = []
        for post in posts:
            title = post.get('data', {}).get('title', '')
            # Buscar códigos en títulos
            codigos = re.findall(r'\b([A-Z]{3}\d{2})\b', title)
            for codigo in codigos:
                modelos.append({
                    'i': codigo.upper(),
                    'm': title[:100],
                    'k': 'Desconocido',
                    'y': datetime.now().year,
                    'fuente': 'Reddit'
                })
        
        if modelos:
            log(f"  Reddit: {len(modelos)} modelos encontrados", C.OK)
        return modelos
    except json.JSONDecodeError:
        pass
    
    log(f"  Reddit: no encontrado", C.WARN)
    return []

def sync_catalogo():
    """Sincroniza el catálogo con todas las fuentes."""
    log(f"\n{'='*50}")
    log(f"Sincronización de catálogo")
    log(f"{'='*50}\n")
    
    # Cargar catálogo actual
    catalogo = cargar_catalogo()
    ids_existentes = {m.get('i', '') for m in catalogo}
    log(f"Modelos actuales: {len(catalogo)}", C.INFO)
    
    # Buscar en cada fuente
    nuevas_fuentes = [
        scrapear_smartwheelers,
        scrapear_reddit,
    ]
    
    # Buscar por año actual y anterior
    ano_actual = datetime.now().year
    for ano in [ano_actual, ano_actual - 1]:
        nuevas_fuentes.append(lambda a=ano: scrapear_hw_wiki(a))
    
    nuevos_modelos = []
    for fuente in nuevas_fuentes:
        try:
            modelos = fuente()
            for modelo in modelos:
                if modelo['i'] not in ids_existentes:
                    nuevos_modelos.append(modelo)
                    ids_existentes.add(modelo['i'])
        except Exception as e:
            log(f"  Error: {e}", C.ERR)
        time.sleep(DELAY_BETWEEN_SOURCES)
    
    # Agregar nuevos modelos al catálogo
    if nuevos_modelos:
        catalogo.extend(nuevos_modelos)
        guardar_catalogo(catalogo)
        log(f"\n{len(nuevos_modelos)} nuevos modelos agregados", C.OK)
    else:
        log(f"\nNo se encontraron nuevos modelos", C.WARN)
    
    return len(nuevos_modelos)

def main():
    if '--sync' in sys.argv:
        sync_catalogo()
    else:
        print("Uso: python build/scraper_catalogo.py --sync")
        print("Busca nuevos modelos de Hot Wheels y actualiza el catálogo.")

if __name__ == '__main__':
    main()
