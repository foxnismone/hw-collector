#!/usr/bin/env python3
"""
Herramienta de extracción masiva de datos de Fandom Wiki por año.
Accede a cada página List_of_YYYY_Hot_Wheels (1968-2027),
extrae tablas con datos de modelos (nombre, tool, serie, diseñador, país),
extraer URLs de imágenes de cada modelo, integra al catálogo existente
y completa modelos faltantes.
"""

import json
import re
import os
import sys
import time
import requests
from pathlib import Path
from typing import Optional

# Paths
BASE = Path(__file__).resolve().parent.parent
CATALOG_PATH = BASE / "data" / "catalog_web.json"
OUTPUT_PATH = BASE / "data" / "catalog_extended.json"
LOG_PATH = BASE / "scripts" / "extraccion_log.json"
RAW_DIR = BASE / "data" / "raw" / "por_anio"

RAW_DIR.mkdir(parents=True, exist_ok=True)

# Session para reutilizar conexión
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
})

FANDOM_API = "https://hotwheels.fandom.com/api.php"
FANDOM_WIKI = "https://hotwheels.fandom.com/wiki"


def fetch_wiki_page(title: str, max_retries: int = 3) -> Optional[str]:
    """Obtiene el contenido wikitext de una página de Fandom via API."""
    for attempt in range(max_retries):
        try:
            params = {
                "action": "parse",
                "page": title,
                "prop": "wikitext",
                "format": "json",
                "formatversion": 2,
            }
            resp = session.get(FANDOM_API, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            if "error" in data:
                print(f"  API error for {title}: {data['error'].get('info', 'unknown')}")
                return None
            return data["parse"]["wikitext"]
        except Exception as e:
            wait = 2 ** attempt
            print(f"  Retry {attempt+1}/{max_retries} for {title}: {e}")
            time.sleep(wait)
    return None


def fetch_page_html(url: str, max_retries: int = 3) -> Optional[str]:
    """Obtiene el HTML de una página de Fandom."""
    for attempt in range(max_retries):
        try:
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            wait = 2 ** attempt
            print(f"  Retry {attempt+1}/{max_retries} for {url}: {e}")
            time.sleep(wait)
    return None


def clean_wiki_markup(text: str) -> str:
    """Limpia markup wiki para obtener texto plano."""
    # Convertir links: [[Page|Display]] -> Display
    text = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', text)
    # Convertir links: [[Page]] -> Page
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
    # Remover templates {{...}}
    text = re.sub(r'\{\{[^}]+\}\}', '', text)
    # Remover tags HTML
    text = re.sub(r'<[^>]+>', '', text)
    # Remover bold/italic
    text = re.sub(r"'''?", '', text)
    # Limpiar espacios extra
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_image_url(text: str) -> str:
    """Extrae URL de imagen de un texto wikitext."""
    # Buscar [[File:...]] o [[Image:...]]
    match = re.search(r'\[\[(?:File|Image):([^|\]]+)', text)
    if match:
        fname = match.group(1).strip()
        # Convertir a URL de Fandom
        return f"https://static.wikia.nocookie.net/hotwheels/images/{fname}"
    return ''


def parse_modern_format(wikitext: str, year: int) -> list:
    """
    Parsea el formato moderno de List_of (2020+).
    Formato: |Toy # | Col.# | Model Name | Series | Series # | Photo |
    """
    models = []
    lines = wikitext.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Detectar tool code (patrón: letras mayúsculas + números)
        tool_match = re.match(r'^\|([A-Z]{3}\d{2,4})\s*$', line)
        if not tool_match:
            tool_match = re.match(r'^([A-Z]{3}\d{2,4})\s*$', line)
        if tool_match:
            tool_code = tool_match.group(1)
            model = {
                'tool': tool_code,
                'year': year,
                'name': '',
                'series': '',
                'position': '',
                'image_url': '',
                'image_name': '',
                'notes': '',
                'source': 'List_of_{}'.format(year),
            }
            # Leer las siguientes líneas hasta el próximo tool code o fin de fila
            j = i + 1
            while j < len(lines) and j < i + 20:
                next_line = lines[j].strip()
                # Si es otro tool code, terminar
                if re.match(r'^\|?[A-Z]{3}\d{2,4}\s*$', next_line):
                    break
                # Número de color (ej: 001)
                num_match = re.match(r'^\|(\d{3,4})\s*$', next_line)
                if num_match and not model.get('number'):
                    model['number'] = num_match.group(1)
                # Nombre con link: [[Name]] o [[Page|Name]]
                name_match = re.match(r'^\|\[\[([^\]|]+)\|([^\]]+)\]\]', next_line)
                if name_match:
                    model['name'] = name_match.group(2)
                    model['wiki_page'] = name_match.group(1)
                else:
                    name_match = re.match(r'^\|\[\[([^\]]+)\]\]', next_line)
                    if name_match:
                        model['name'] = name_match.group(1)
                        model['wiki_page'] = name_match.group(1)
                # Serie con bgcolor
                series_match = re.search(r'\[\[([^\]|]+)\|([^\]]+)\]\]', next_line)
                if series_match and not model.get('series'):
                    # Evitar confundir con el nombre
                    if 'bgcolor' in next_line or 'Mini Collection' in next_line or 'New for' in next_line:
                        model['series'] = series_match.group(2)
                # Posición (ej: 3/5)
                pos_match = re.match(r'^\|(\d+/\d+)', next_line)
                if pos_match:
                    model['position'] = pos_match.group(1)
                # Imagen
                img_match = re.search(r'\[\[(?:File|Image):([^|\]]+)', next_line)
                if img_match:
                    fname = img_match.group(1).strip()
                    model['image_url'] = f"https://static.wikia.nocookie.net/hotwheels/images/{fname}"
                    model['image_name'] = fname.replace('.jpg', '').replace('.png', '').replace('.jpeg', '').replace('.JPG', '').replace('.PNG', '')
                j += 1
            if model['name']:
                models.append(model)
            i = j
        else:
            i += 1
    return models


def parse_classic_table(wikitext: str, year: int) -> list:
    """Parsea tablas clásicas (1968-1990s). Formato: | Toy # | Model Name | Photo |"""
    models = []
    lines = wikitext.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Detectar número de toy (4-5 dígitos)
        toy_match = re.match(r'^\|(\d{4,5})\s*$', line)
        if toy_match:
            toy_num = toy_match.group(1)
            model = {
                'tool': toy_num,
                'number': toy_num,
                'name': '',
                'year': year,
                'series': '',
                'position': '',
                'image_url': '',
                'image_name': '',
                'notes': '',
                'source': 'List_of_{}'.format(year),
            }
            # Leer las siguientes líneas
            j = i + 1
            while j < len(lines) and j < i + 10:
                next_line = lines[j].strip()
                # Si es otro número de toy, terminar
                if re.match(r'^\|\d{4,5}\s*$', next_line):
                    break
                # Nombre con link
                if '[[' in next_line and not model['name']:
                    name_match = re.search(r'\[\[([^\]|]+)\|([^\]]+)\]\]', next_line)
                    if name_match:
                        model['name'] = name_match.group(2)
                        model['wiki_page'] = name_match.group(1)
                    else:
                        name_match = re.search(r'\[\[([^\]]+)\]\]', next_line)
                        if name_match:
                            model['name'] = name_match.group(1)
                            model['wiki_page'] = name_match.group(1)
                # Imagen
                if '[[' in next_line and ('File:' in next_line or 'Image:' in next_line):
                    img_match = re.search(r'\[\[(?:File|Image):([^|\]]+)', next_line)
                    if img_match:
                        fname = img_match.group(1).strip()
                        model['image_url'] = f"https://static.wikia.nocookie.net/hotwheels/images/{fname}"
                        model['image_name'] = fname.replace('.jpg', '').replace('.png', '').replace('.jpeg', '').replace('.JPG', '').replace('.PNG', '')
                j += 1
            if model['name']:
                models.append(model)
            i = j
        else:
            i += 1
    return models


def parse_table_format(wikitext: str, year: int) -> list:
    """Parsea tablas con formato extendido (1990s-2010s)."""
    models = []
    lines = wikitext.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Detectar número de toy o código de tool
        toy_match = re.match(r'^\|([A-Z0-9]{3,6})\s*$', line)
        if toy_match:
            tool_code = toy_match.group(1)
            model = {
                'tool': tool_code,
                'number': '',
                'name': '',
                'year': year,
                'series': '',
                'position': '',
                'image_url': '',
                'image_name': '',
                'notes': '',
                'source': 'List_of_{}'.format(year),
            }
            j = i + 1
            while j < len(lines) and j < i + 15:
                next_line = lines[j].strip()
                if re.match(r'^\|[A-Z0-9]{3,6}\s*$', next_line):
                    break
                # Número de color
                num_match = re.match(r'^\|(\d{3,4})\s*$', next_line)
                if num_match and not model['number']:
                    model['number'] = num_match.group(1)
                # Nombre con link
                if '[[' in next_line and not model['name']:
                    name_match = re.search(r'\[\[([^\]|]+)\|([^\]]+)\]\]', next_line)
                    if name_match:
                        model['name'] = name_match.group(2)
                        model['wiki_page'] = name_match.group(1)
                    else:
                        name_match = re.search(r'\[\[([^\]]+)\]\]', next_line)
                        if name_match:
                            model['name'] = name_match.group(1)
                            model['wiki_page'] = name_match.group(1)
                # Imagen
                if '[[' in next_line and ('File:' in next_line or 'Image:' in next_line):
                    img_match = re.search(r'\[\[(?:File|Image):([^|\]]+)', next_line)
                    if img_match:
                        fname = img_match.group(1).strip()
                        model['image_url'] = f"https://static.wikia.nocookie.net/hotwheels/images/{fname}"
                        model['image_name'] = fname.replace('.jpg', '').replace('.png', '').replace('.jpeg', '').replace('.JPG', '').replace('.PNG', '')
                j += 1
            if model['name']:
                models.append(model)
            i = j
        else:
            i += 1
    return models


def fetch_model_details(wiki_page: str) -> dict:
    """Obtiene diseñador, país y serie desde la página individual del modelo."""
    details = {'designer': '', 'country': '', 'series': '', 'year': ''}
    if not wiki_page:
        return details
    from urllib.parse import unquote
    wiki_page = unquote(wiki_page).replace('_', ' ')
    wikitext = fetch_wiki_page(wiki_page)
    if not wikitext:
        return details
    designer_match = re.search(r'(?:Designer|designer|Design by|Designed by)[:\s]*([^\n\|]+)', wikitext)
    if designer_match:
        details['designer'] = designer_match.group(1).strip()
    version_table = re.findall(
        r'\|\s*\d+/\d+\s*\|\s*(\d{4})\s*\|\s*([^|]+)\|\s*[^|]*\|\s*[^|]*\|\s*[^|]*\|\s*[^|]*\|\s*[^|]*\|\s*[^|]*\|\s*([A-Z]{3}\d{2,4})\s*\|\s*([^|]+)\|',
        wikitext
    )
    if version_table:
        for vt in version_table:
            if not details['year']:
                details['year'] = vt[0]
            if not details['series']:
                s = vt[1].strip()
                s = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', s)
                s = re.sub(r'\[\[([^\]]+)\]\]', r'\1', s)
                details['series'] = s
            if not details['country']:
                c = vt[3].strip()
                c = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', c)
                c = re.sub(r'\[\[([^\]]+)\]\]', r'\1', c)
                if c and len(c) < 30:
                    details['country'] = c
    desc_designer = re.search(r'(?:According to designer|designer is|designed by)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', wikitext)
    if desc_designer and not details['designer']:
        details['designer'] = desc_designer.group(1)
    return details


def process_year(year: int, existing_by_tool: dict, existing_by_name: dict) -> tuple:
    """Procesa un año completo."""
    title = f"List_of_{year}_Hot_Wheels"
    print(f"\n{'='*60}")
    print(f"Procesando {title}...")
    print(f"{'='*60}")
    stats = {'year': year, 'found': 0, 'new_models': 0, 'updated': 0, 'images_found': 0, 'details_fetched': 0, 'errors': []}
    wikitext = fetch_wiki_page(title)
    if not wikitext:
        print(f"  No wikitext, intentando HTML...")
        html = fetch_page_html(f"{FANDOM_WIKI}/{title}")
        if html:
            wikitext = html
        else:
            stats['errors'].append(f"No se pudo obtener {title}")
            return stats, []
    raw_file = RAW_DIR / f"List_of_{year}_Hot_Wheels.txt"
    raw_file.write_text(wikitext, encoding='utf-8')
    if re.search(r'\{\|\s*class="wikitable"', wikitext) and year < 2010:
        models = parse_classic_table(wikitext, year)
        print(f"  Formato clásico: {len(models)} modelos")
    elif re.search(r'\{\|.*\|\}', wikitext) and year < 2015:
        models = parse_table_format(wikitext, year)
        print(f"  Formato tabla: {len(models)} modelos")
    else:
        models = parse_modern_format(wikitext, year)
        print(f"  Formato moderno: {len(models)} modelos")
    stats['found'] = len(models)
    new_models = []
    for model in models:
        tool = model.get('tool', '')
        name = model.get('name', '')
        if not tool or not name:
            continue
        existing = existing_by_tool.get(tool) or existing_by_name.get(name.lower())
        if model.get('image_url'):
            stats['images_found'] += 1
        if not existing:
            wiki_page = model.get('wiki_page', '')
            if wiki_page:
                details = fetch_model_details(wiki_page)
                model.update(details)
                stats['details_fetched'] += 1
            new_models.append(model)
            stats['new_models'] += 1
        else:
            if model.get('image_url') and not existing.get('im'):
                existing['im'] = model.get('image_name', '')
                existing['imr'] = model.get('image_url', '')
                stats['updated'] += 1
    print(f"  Nuevos: {stats['new_models']}, Actualizados: {stats['updated']}, Imágenes: {stats['images_found']}")
    return stats, new_models


def main():
    """Función principal: procesa todos los años 1968-2027."""
    print("="*60)
    print("EXTRACCIÓN MASIVA DE FANDOM WIKI POR AÑO")
    print("="*60)
    if CATALOG_PATH.exists():
        with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
    else:
        catalog = []
    print(f"Catálogo actual: {len(catalog)} modelos")
    existing_by_tool = {}
    existing_by_name = {}
    for item in catalog:
        if 't' in item:
            existing_by_tool[item['t']] = item
        if 'm' in item:
            existing_by_name[item['m'].lower()] = item
    all_stats = []
    all_new_models = []
    for year in range(1968, 2028):
        try:
            stats, new_models = process_year(year, existing_by_tool, existing_by_name)
            all_stats.append(stats)
            all_new_models.extend(new_models)
        except Exception as e:
            print(f"  ERROR procesando {year}: {e}")
            all_stats.append({'year': year, 'found': 0, 'new_models': 0, 'updated': 0, 'images_found': 0, 'details_fetched': 0, 'errors': [str(e)]})
        time.sleep(0.3)
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_stats, f, indent=2, ensure_ascii=False)
    print(f"\n{'='*60}")
    print(f"INTEGRANDO AL CATÁLOGO...")
    print(f"{'='*60}")
    for model in all_new_models:
        tool = model.get('tool', '')
        name = model.get('name', '')
        year = model.get('year', 0)
        model_id = f"{year}-{tool}"
        entry = {
            'i': model_id,
            'm': name,
            'y': year,
            't': tool,
            'c': model.get('number', ''),
            's': model.get('series', ''),
            'n': model.get('position', ''),
            'k': 'Mainline',
            'im': model.get('image_name', ''),
            'imr': model.get('image_url', ''),
            'pais': model.get('country', ''),
            'diseñador': model.get('designer', ''),
            'ficha': {
                'descripcion': f"{name} de {year}. Serie: {model.get('series', 'N/A')}.",
                'historia': f"Modelo de {year} extraído de {model.get('source', 'Fandom Wiki')}.",
                'curiosidades': f"Tool #{tool}. Parte de la colección de {year}.",
                'conmemorativo': False,
                'dato_clave': f"Tool #{tool} de {year}",
            },
        }
        if not existing_by_tool.get(tool) and not existing_by_name.get(name.lower()):
            catalog.append(entry)
            existing_by_tool[tool] = entry
            existing_by_name[name.lower()] = entry
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    total_found = sum(s.get('found', 0) for s in all_stats)
    total_new = sum(s.get('new_models', 0) for s in all_stats)
    total_updated = sum(s.get('updated', 0) for s in all_stats)
    total_images = sum(s.get('images_found', 0) for s in all_stats)
    total_details = sum(s.get('details_fetched', 0) for s in all_stats)
    total_errors = sum(len(s.get('errors', [])) for s in all_stats)
    print(f"\n{'='*60}")
    print(f"RESUMEN FINAL")
    print(f"{'='*60}")
    print(f"Años procesados: 1968-2027 (59 años)")
    print(f"Modelos encontrados: {total_found}")
    print(f"Nuevos modelos: {total_new}")
    print(f"Modelos actualizados: {total_updated}")
    print(f"Imágenes encontradas: {total_images}")
    print(f"Detalles obtenidos: {total_details}")
    print(f"Errores: {total_errors}")
    print(f"Catálogo final: {len(catalog)} modelos")
    print(f"\nArchivo guardado: {OUTPUT_PATH}")
    print(f"Log guardado: {LOG_PATH}")
    return {
        'success': total_errors < 50,
        'modelos_procesados': total_found,
        'imagenes_encontradas': total_images,
        'nuevos_modelos': total_new,
        'actualizados': total_updated,
        'detalles_obtenidos': total_details,
        'errores': total_errors,
    }


if __name__ == '__main__':
    result = main()
    print(f"\n{'='*60}")
    print("RESULTADO JSON:")
    print(json.dumps(result, indent=2))
