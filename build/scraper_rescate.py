#!/usr/bin/env python3
"""
Scraper de rescate para HW Collector.
Busca un código de Hot Wheels en múltiples fuentes de internet
cuando no existe en la base local.

Uso:
    python build/scraper_rescate.py <codigo>
    python build/scraper_rescate.py L2593
    python build/scraper_rescate.py FRN78

Fuentes (en orden de prioridad):
    1. SmartWheelers — base de conocimiento de Hot Wheels
    2. Hot Wheels Wiki (Fandom) — enciclopedia comunitaria
    3. HW Price Guide — valores de mercado
    4. Reddit r/HotWheels — discusiones y fotos
    5. eBay — ventas recientes
    6. Mercado Libre — precios en CLP
"""

import sys
import json
import re
import time
import hashlib
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime

# Configuración
TIMEOUT = 15  # segundos por request
DELAY_BETWEEN_SOURCES = 2  # segundos entre fuentes
USER_AGENT = 'HWCollector/1.0 (Proyecto personal de coleccionismo; contacto: [REDACTED])'
CACHE_DIR = Path(__file__).parent.parent / 'data' / 'scraper_cache'
CACHE_DIR.mkdir(parents=True, exist_ok=True)

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
    req.add_header('Accept-Encoding', 'gzip, deflate, br')
    req.add_header('Connection', 'keep-alive')
    req.add_header('Upgrade-Insecure-Requests', '1')
    req.add_header('Sec-Fetch-Dest', 'document')
    req.add_header('Sec-Fetch-Mode', 'navigate')
    req.add_header('Sec-Fetch-Site', 'none')
    req.add_header('Sec-Fetch-User', '?1')
    req.add_header('Cache-Control', 'max-age=0')
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            import gzip
            data = resp.read()
            if resp.headers.get('Content-Encoding') == 'gzip':
                data = gzip.decompress(data)
            return data.decode('utf-8', errors='ignore')
    except Exception as e:
        return None

def parse_html(html):
    """Parsea HTML con BeautifulSoup si está disponible, si no con regex."""
    try:
        from bs4 import BeautifulSoup
        return BeautifulSoup(html, 'html.parser')
    except ImportError:
        return None

def extraer_de_smartwheelers(codigo):
    """Busca en SmartWheelers (base de conocimiento de Hot Wheels)."""
    log(f"  Buscando en SmartWheelers...", C.INFO)
    url = f"https://www.smartwheelers.com/search?q={urllib.parse.quote(codigo)}"
    html = fetch_url(url)
    if not html:
        log(f"  SmartWheelers: sin respuesta", C.WARN)
        return None
    
    # Buscar cualquier texto que contenga el código
    import re
    # Patrón: buscar texto que contenga el código
    patron = re.compile(rf'[^<>]*{re.escape(codigo)}[^<>]*', re.IGNORECASE)
    matches = patron.findall(html)
    if matches:
        nombre = matches[0].strip()
        if len(nombre) > 5:
            log(f"  SmartWheelers: encontrado", C.OK)
            return {
                'nombre': nombre[:100],
                'fuente': 'SmartWheelers',
                'url': url
            }
    
    # Buscar en títulos y encabezados
    soup = parse_html(html)
    if soup:
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'span', 'div']):
            texto = tag.get_text(strip=True)
            if codigo.lower() in texto.lower() and len(texto) > 5 and len(texto) < 200:
                log(f"  SmartWheelers: encontrado en <{tag.name}>", C.OK)
                return {
                    'nombre': texto,
                    'fuente': 'SmartWheelers',
                    'url': url
                }
    
    log(f"  SmartWheelers: no encontrado", C.WARN)
    return None

def extraer_de_hw_wiki(codigo):
    """Busca en Hot Wheels Wiki (Fandom)."""
    log(f"  Buscando en Hot Wheels Wiki...", C.INFO)
    url = f"https://hotwheels.fandom.com/es/wiki/Especial:Buscar?query={urllib.parse.quote(codigo)}"
    html = fetch_url(url)
    if not html:
        log(f"  HW Wiki: sin respuesta", C.WARN)
        return None
    
    soup = parse_html(html)
    if not soup:
        return None
    
    # Buscar enlaces a artículos
    resultados = []
    for link in soup.select('a[href*="/es/wiki/"]'):
        nombre = link.get_text(strip=True)
        if nombre and len(nombre) > 3 and codigo.lower() in nombre.lower():
            resultados.append({
                'nombre': nombre,
                'fuente': 'Hot Wheels Wiki',
                'url': f"https://hotwheels.fandom.com{link.get('href', '')}"
            })
    
    if resultados:
        log(f"  HW Wiki: {len(resultados)} resultado(s)", C.OK)
        return resultados[0]
    
    log(f"  HW Wiki: no encontrado", C.WARN)
    return None

def extraer_de_hwpriceguide(codigo):
    """Busca en HW Price Guide (valores de mercado)."""
    log(f"  Buscando en HW Price Guide...", C.INFO)
    url = f"https://www.hwpriceguide.com/search?query={urllib.parse.quote(codigo)}"
    html = fetch_url(url)
    if not html:
        log(f"  HW Price Guide: sin respuesta", C.WARN)
        return None
    
    soup = parse_html(html)
    if not soup:
        return None
    
    # Buscar resultados
    resultados = []
    for item in soup.select('.car-result, .search-result, tr'):
        nombre = item.select_one('.car-name, .name, td:first-child')
        if nombre:
            resultados.append({
                'nombre': nombre.get_text(strip=True),
                'fuente': 'HW Price Guide',
                'url': url
            })
    
    if resultados:
        log(f"  HW Price Guide: {len(resultados)} resultado(s)", C.OK)
        return resultados[0]
    
    log(f"  HW Price Guide: no encontrado", C.WARN)
    return None

def extraer_de_reddit(codigo):
    """Busca en Reddit r/HotWheels usando la API JSON."""
    log(f"  Buscando en Reddit r/HotWheels...", C.INFO)
    url = f"https://www.reddit.com/r/HotWheels/search.json?q={urllib.parse.quote(codigo)}&restrict_sr=1&limit=5"
    html = fetch_url(url, headers={'Accept': 'application/json'})
    if not html:
        log(f"  Reddit: sin respuesta", C.WARN)
        return None
    
    try:
        data = json.loads(html)
        posts = data.get('data', {}).get('children', [])
        if posts:
            post = posts[0].get('data', {})
            log(f"  Reddit: encontrado '{post.get('title', '')[:50]}'", C.OK)
            return {
                'nombre': post.get('title', ''),
                'fuente': 'Reddit r/HotWheels',
                'url': f"https://www.reddit.com{post.get('permalink', '')}"
            }
    except json.JSONDecodeError:
        pass
    
    log(f"  Reddit: no encontrado", C.WARN)
    return None

def extraer_de_ebay(codigo):
    """Busca en eBay (ventas recientes)."""
    log(f"  Buscando en eBay...", C.INFO)
    url = f"https://www.ebay.com/sch/i.html?_nkw={urllib.parse.quote(codigo + ' hot wheels')}&_sop=15"
    html = fetch_url(url)
    if not html:
        log(f"  eBay: sin respuesta", C.WARN)
        return None
    
    soup = parse_html(html)
    if not soup:
        return None
    
    # Buscar items
    resultados = []
    for item in soup.select('.s-item, .srp-results .s-item'):
        nombre = item.select_one('.s-item__title, .s-item__title span')
        if nombre:
            resultados.append({
                'nombre': nombre.get_text(strip=True),
                'fuente': 'eBay',
                'url': url
            })
    
    if resultados:
        log(f"  eBay: {len(resultados)} resultado(s)", C.OK)
        return resultados[0]
    
    log(f"  eBay: no encontrado", C.WARN)
    return None

def extraer_de_mercadolibre(codigo):
    """Busca en Mercado Libre (precios en CLP)."""
    log(f"  Buscando en Mercado Libre...", C.INFO)
    url = f"https://listado.mercadolibre.cl/{urllib.parse.quote(codigo + ' hot wheels')}"
    html = fetch_url(url)
    if not html:
        log(f"  Mercado Libre: sin respuesta", C.WARN)
        return None
    
    soup = parse_html(html)
    if not soup:
        return None
    
    # Buscar items
    resultados = []
    for item in soup.select('.ui-search-result, .andes-card'):
        nombre = item.select_one('.ui-search-result__title, .ui-search-item__title')
        if nombre:
            resultados.append({
                'nombre': nombre.get_text(strip=True),
                'fuente': 'Mercado Libre',
                'url': url
            })
    
    if resultados:
        log(f"  Mercado Libre: {len(resultados)} resultado(s)", C.OK)
        return resultados[0]
    
    log(f"  Mercado Libre: no encontrado", C.WARN)
    return None

def guardar_en_cache(codigo, datos):
    """Guarda el resultado en caché para no repetir requests."""
    cache_file = CACHE_DIR / f"{hashlib.md5(codigo.encode()).hexdigest()}.json"
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump({
            'codigo': codigo,
            'datos': datos,
            'fecha': datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)

def leer_cache(codigo):
    """Lee el resultado de caché si existe y no tiene más de 7 días."""
    cache_file = CACHE_DIR / f"{hashlib.md5(codigo.encode()).hexdigest()}.json"
    if not cache_file.exists():
        return None
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Verificar que no tenga más de 7 días
        fecha = datetime.fromisoformat(data.get('fecha', '2000-01-01'))
        if (datetime.now() - fecha).days > 7:
            return None
        return data.get('datos')
    except (json.JSONDecodeError, KeyError):
        return None

def buscar_en_internet(codigo):
    """Busca un código en todas las fuentes disponibles."""
    log(f"\n{'='*50}")
    log(f"Scraping de rescate para: {codigo}")
    log(f"{'='*50}\n")
    
    # Primero verificar caché
    cache = leer_cache(codigo)
    if cache:
        log(f"Resultado encontrado en caché (válido por 7 días)", C.OK)
        return cache
    
    # Buscar en cada fuente
    fuentes = [
        extraer_de_smartwheelers,
        extraer_de_hw_wiki,
        extraer_de_hwpriceguide,
        extraer_de_reddit,
        extraer_de_ebay,
        extraer_de_mercadolibre,
    ]
    
    for fuente in fuentes:
        try:
            resultado = fuente(codigo)
            if resultado:
                guardar_en_cache(codigo, resultado)
                return resultado
        except Exception as e:
            log(f"  Error: {e}", C.ERR)
        time.sleep(DELAY_BETWEEN_SOURCES)
    
    log(f"\nNo se encontró '{codigo}' en ninguna fuente.", C.ERR)
    return None

def main():
    if len(sys.argv) < 2:
        print("Uso: python build/scraper_rescate.py <codigo>")
        print("Ejemplo: python build/scraper_rescate.py L2593")
        sys.exit(1)
    
    codigo = sys.argv[1].upper()
    resultado = buscar_en_internet(codigo)
    
    if resultado:
        log(f"\n{'='*50}")
        log(f"RESULTADO ENCONTRADO", C.OK)
        log(f"{'='*50}")
        log(f"Nombre: {resultado.get('nombre', 'N/A')}")
        log(f"Fuente: {resultado.get('fuente', 'N/A')}")
        log(f"URL: {resultado.get('url', 'N/A')}")
        log(f"\nPara agregar a la app, usá estos datos en 'Agregar manualmente'.")
    else:
        log(f"\nNo se encontró información para '{codigo}'.", C.ERR)
        log(f"Sugerencias:")
        log(f"  1. Verificá que el código esté completo")
        log(f"  2. Intentá buscar por nombre del modelo")
        log(f"  3. Agregalo manualmente desde la app")
        sys.exit(1)

if __name__ == '__main__':
    main()
