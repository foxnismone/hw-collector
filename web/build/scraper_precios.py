#!/usr/bin/env python3
"""
Scraper de precios para HW Collector.
Busca precios de Hot Wheels en eBay y Mercado Libre
y actualiza el archivo precios_referencia.json.

Uso:
    python build/scraper_precios.py --sync

Fuentes:
    1. eBay — ventas recientes
    2. Mercado Libre — precios en CLP
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
PRICES_FILE = DATA_DIR / 'precios_referencia.json'

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

def cargar_precios():
    """Carga los precios actuales."""
    if PRICES_FILE.exists():
        with open(PRICES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_precios(precios):
    """Guarda los precios actualizados."""
    PRICES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PRICES_FILE, 'w', encoding='utf-8') as f:
        json.dump(precios, f, ensure_ascii=False, separators=(',', ':'))
    log(f"Precios guardados: {len(precios)} modelos", C.OK)

def scrapear_ebay(codigo):
    """Busca precios en eBay."""
    log(f"  Buscando en eBay ({codigo})...", C.INFO)
    
    url = f"https://www.ebay.com/sch/i.html?_nkw={urllib.parse.quote(codigo + ' hot wheels')}&_sop=15&_ipg=25"
    html = fetch_url(url)
    if not html:
        log(f"  eBay: sin respuesta", C.WARN)
        return None
    
    # Buscar precios en el HTML
    # Patrón común: "$XX.XX" o "USD XX.XX"
    precios = re.findall(r'\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', html)
    
    # Filtrar precios razonables (entre 1 y 500 USD)
    precios_validos = []
    for p in precios:
        try:
            valor = float(p.replace(',', ''))
            if 1 <= valor <= 500:
                precios_validos.append(valor)
        except ValueError:
            continue
    
    if precios_validos:
        precio_promedio = sum(precios_validos) / len(precios_validos)
        log(f"  eBay: ${precio_promedio:.2f} USD (promedio de {len(precios_validos)} precios)", C.OK)
        return {
            'usd': round(precio_promedio, 2),
            'fuente': 'eBay',
            'fecha': datetime.now().isoformat()
        }
    
    log(f"  eBay: no encontrado", C.WARN)
    return None

def scrapear_mercadolibre(codigo):
    """Busca precios en Mercado Libre."""
    log(f"  Buscando en Mercado Libre ({codigo})...", C.INFO)
    
    url = f"https://listado.mercadolibre.cl/{urllib.parse.quote(codigo + ' hot wheels')}"
    html = fetch_url(url)
    if not html:
        log(f"  Mercado Libre: sin respuesta", C.WARN)
        return None
    
    # Buscar precios en el HTML
    # Patrón común: "$XX.XXX" o "$X.XXX.XXX" (formato CLP)
    precios = re.findall(r'\$\s*(\d{1,3}(?:\.\d{3})+)', html)
    
    # Filtrar precios razonables (entre 500 y 500000 CLP)
    precios_validos = []
    for p in precios:
        try:
            valor = int(p.replace('.', ''))
            if 500 <= valor <= 500000:
                precios_validos.append(valor)
        except ValueError:
            continue
    
    if precios_validos:
        precio_promedio = sum(precios_validos) / len(precios_validos)
        log(f"  Mercado Libre: ${int(precio_promedio):,} CLP (promedio de {len(precios_validos)} precios)", C.OK)
        return {
            'clp': int(precio_promedio),
            'fuente': 'Mercado Libre',
            'fecha': datetime.now().isoformat()
        }
    
    log(f"  Mercado Libre: no encontrado", C.WARN)
    return None

def sync_precios(catalogo):
    """Sincroniza los precios con todas las fuentes."""
    log(f"\n{'='*50}")
    log(f"Sincronización de precios")
    log(f"{'='*50}\n")
    
    # Cargar precios actuales
    precios = cargar_precios()
    log(f"Precios actuales: {len(precios)} modelos", C.INFO)
    
    # Buscar precios para cada modelo (limitado a 50 para no sobrecargar)
    modelos_a_actualizar = catalogo[:50]  # Limitar para no sobrecargar
    
    nuevos_precios = 0
    for modelo in modelos_a_actualizar:
        codigo = modelo.get('i', '')
        if not codigo:
            continue
        
        # Verificar si ya tiene precio reciente (menos de 7 días)
        if codigo in precios:
            fecha = precios[codigo].get('fecha', '')
            if fecha:
                try:
                    fecha_dt = datetime.fromisoformat(fecha)
                    if (datetime.now() - fecha_dt).days < 7:
                        continue
                except ValueError:
                    pass
        
        # Buscar en cada fuente
        nuevas_fuentes = [
            scrapear_ebay,
            scrapear_mercadolibre,
        ]
        
        for fuente in nuevas_fuentes:
            try:
                resultado = fuente(codigo)
                if resultado:
                    precios[codigo] = resultado
                    nuevos_precios += 1
                    break
            except Exception as e:
                log(f"  Error: {e}", C.ERR)
            time.sleep(DELAY_BETWEEN_SOURCES)
    
    # Guardar precios
    if nuevos_precios > 0:
        guardar_precios(precios)
        log(f"\n{nuevos_precios} precios actualizados", C.OK)
    else:
        log(f"\nNo se actualizaron precios", C.WARN)
    
    return nuevos_precios

def main():
    if '--sync' in sys.argv:
        # Cargar catálogo
        catalog_file = DATA_DIR / 'catalog_web.json'
        if catalog_file.exists():
            with open(catalog_file, 'r', encoding='utf-8') as f:
                catalogo = json.load(f)
        else:
            log("No se encontró el catálogo. Ejecutá primero scraper_catalogo.py", C.ERR)
            sys.exit(1)
        
        sync_precios(catalogo)
    else:
        print("Uso: python build/scraper_precios.py --sync")
        print("Busca precios de Hot Wheels y actualiza los valores de referencia.")

if __name__ == '__main__':
    main()
