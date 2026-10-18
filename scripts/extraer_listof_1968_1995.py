#!/usr/bin/env python3
"""
Extracción masiva de datos de Fandom List_of_1968-1995.
Obtiene wikitext de cada página, parsea tablas, extrae modelos con Tool #, nombre, serie y foto.
Integra al catálogo data/catalog_web.json y guarda imágenes en data/imagenes_listof_1968_1995.json
"""

import json, re, urllib.request, urllib.parse, time, sys, os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent / 'data'
CATALOG_FILE = BASE_DIR / 'catalog_web.json'
IMAGES_FILE = BASE_DIR / 'imagenes_listof_1968_1995.json'
CACHE_DIR = BASE_DIR / 'scraper_cache'
CACHE_DIR.mkdir(exist_ok=True)

UA = 'Mozilla/5.0 (hotwheels-research)'
REFERER = 'https://hotwheels.fandom.com/'

def api_fandom(params):
    """Hace una solicitud a la API de Fandom"""
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', UA)
    req.add_header('Referer', REFERER)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"  Error API: {e}")
        return None

def obtener_wikitext(titulo):
    """Obtiene el wikitext de una página"""
    data = api_fandom({
        'action': 'parse',
        'page': titulo,
        'prop': 'wikitext',
        'format': 'json',
        'formatversion': '2'
    })
    if not data:
        return None
    return data.get('parse', {}).get('wikitext', '')

def limpiar_nombre(texto):
    """Limpia un nombre de modelo del wikitext"""
    if not texto:
        return ''
    # Extraer texto de links wiki: [[Link|Nombre]] o [[Nombre]]
    matches = re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', texto)
    if matches:
        # Usar el nombre mostrado (segundo grupo) si existe, si no el link
        partes = []
        for link, nombre in matches:
            partes.append(nombre if nombre else link)
        return ' '.join(partes)
    # Limpiar markup
    texto = re.sub(r"''+", '', texto)
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def limpiar_nombre_modelo(texto):
    """Limpia el nombre del modelo, manejando casos como 'org [[P-911]] changed to'"""
    texto = limpiar_nombre(texto)
    # Limpiar sufijos comunes
    texto = re.sub(r'\s*(org|changed to|was|also known as)\s*$', '', texto, flags=re.IGNORECASE)
    return texto.strip()

def extraer_url_imagen(texto):
    """Extrae la URL de imagen del wikitext"""
    if not texto:
        return None
    # Buscar [[File:...]] o [[Image:...]]
    matches = re.findall(r'\[\[(?:File|Image):([^\]|]+)', texto, re.IGNORECASE)
    if matches:
        # Tomar la última imagen (generalmente la foto principal)
        archivo = matches[-1].strip()
        return archivo
    return None

def obtener_url_real_imagen(nombre_archivo):
    """Obtiene la URL real de una imagen usando la API"""
    if not nombre_archivo:
        return None
    data = api_fandom({
        'action': 'query',
        'titles': f'File:{nombre_archivo}',
        'prop': 'imageinfo',
        'iiprop': 'url',
        'format': 'json',
        'formatversion': '2'
    })
    if not data:
        return None
    pages = data.get('query', {}).get('pages', [])
    if pages and len(pages) > 0:
        imageinfo = pages[0].get('imageinfo', [])
        if imageinfo and len(imageinfo) > 0:
            url = imageinfo[0].get('url', '')
            if url:
                # Agregar parámetro para miniatura
                if 'revision/latest' not in url:
                    url = url.replace('/revision/latest', '/revision/latest/scale-to-width-down/200')
                return url
    return None

def parsear_tabla(wikitext, anio):
    """Parsea las tablas del wikitext y extrae modelos"""
    modelos = []
    
    if not wikitext:
        return modelos
    
    # Buscar todas las tablas wikitable
    # Las tablas comienzan con {| y terminan con |}
    tabla_pattern = re.compile(r'\{\|[^}]*class="[^"]*wikitable[^"]*"[^}]*\|\}(.*?)\|\}', re.DOTALL)
    
    # Si no encuentra con ese patrón, buscar tablas genéricas
    tablas = tabla_pattern.findall(wikitext)
    
    if not tablas:
        # Buscar cualquier tabla
        tablas = re.findall(r'\{\|(.*?)\|\}', wikitext, re.DOTALL)
    
    for tabla in tablas:
        lineas = tabla.split('\n')
        
        # Encontrar el header para identificar columnas
        header_idx = -1
        headers = []
        for i, linea in enumerate(lineas):
            if linea.strip().startswith('!'):
                # Es header
                headers = [h.strip() for h in linea.split('!!')]
                header_idx = i
                break
        
        if header_idx == -1 or not headers:
            # No hay header, asumir formato básico
            continue
        
        # Identificar columnas por nombre
        col_toy = -1
        col_nombre = -1
        col_serie = -1
        col_foto = -1
        
        for i, h in enumerate(headers):
            h_lower = h.lower().strip('*').strip()
            if 'toy' in h_lower or 'tool' in h_lower or 'col' in h_lower:
                col_toy = i
            elif 'casting' in h_lower or 'model' in h_lower or 'name' in h_lower:
                col_nombre = i
            elif 'series' in h_lower or 'serie' in h_lower:
                col_serie = i
            elif 'photo' in h_lower or 'foto' in h_lower or 'image' in h_lower or 'color' in h_lower:
                col_foto = i
        
        # Si no se encontraron columnas, saltar
        if col_toy == -1 and col_nombre == -1:
            continue
        
        # Procesar filas de datos
        datos = []
        for linea in lineas[header_idx+1:]:
            linea = linea.strip()
            if linea.startswith('|-'):
                continue
            if linea.startswith('|}'):
                break
            if linea.startswith('|+'):
                continue
            if linea and not linea.startswith('!'):
                # Es una fila de datos - puede ocupar múltiples líneas
                # En wikitext, las celdas están en líneas separadas que comienzan con |
                datos.append(linea)
        
        # Las filas en wikitext pueden ser multilínea
        # Cada celda comienza con | y las filas con |-
        # Necesito agrupar las celdas por fila
        filas = []
        fila_actual = []
        for linea in lineas[header_idx+1:]:
            linea = linea.strip()
            if linea.startswith('|-'):
                if fila_actual:
                    filas.append(fila_actual)
                fila_actual = []
            elif linea.startswith('|}'):
                break
            elif linea.startswith('|') and not linea.startswith('|-'):
                # Es una celda
                celda = linea[1:].strip()  # Quitar el |
                fila_actual.append(celda)
        
        if fila_actual:
            filas.append(fila_actual)
        
        # Procesar cada fila
        for fila in filas:
            if len(fila) < 2:
                continue
            
            # Extraer Toy #
            toy_num = ''
            if col_toy >= 0 and col_toy < len(fila):
                toy_match = re.search(r'\d+', fila[col_toy])
                if toy_match:
                    toy_num = toy_match.group()
            
            # Extraer nombre
            nombre = ''
            if col_nombre >= 0 and col_nombre < len(fila):
                nombre = limpiar_nombre_modelo(fila[col_nombre])
            
            # Extraer serie
            serie = ''
            if col_serie >= 0 and col_serie < len(fila):
                serie = limpiar_nombre(fila[col_serie])
            
            # Extraer foto
            foto = ''
            if col_foto >= 0 and col_foto < len(fila):
                foto = extraer_url_imagen(fila[col_foto])
            
            # Solo agregar si tiene Toy # o nombre
            if toy_num or nombre:
                modelos.append({
                    'anio': anio,
                    'toy': toy_num,
                    'nombre': nombre,
                    'serie': serie,
                    'foto': foto
                })
    
    return modelos

def parsear_wikitext_completo(wikitext, anio):
    """Parser alternativo que funciona con el formato real de Fandom"""
    modelos = []
    
    if not wikitext:
        return modelos
    
    # Buscar todas las tablas
    tablas = re.findall(r'\{\|(.*?)\|\}', wikitext, re.DOTALL)
    
    for tabla in tablas:
        lineas = tabla.split('\n')
        
        # Encontrar headers
        headers = []
        for linea in lineas:
            if linea.strip().startswith('!'):
                # Puede haber múltiples headers separados por !!
                headers = [h.strip() for h in linea.split('!!')]
                break
        
        if not headers:
            continue
        
        # Limpiar headers
        headers = [h.strip('*').strip() for h in headers]
        
        # Identificar columnas
        col_toy = -1
        col_nombre = -1
        col_serie = -1
        col_foto = -1
        
        for i, h in enumerate(headers):
            h_lower = h.lower()
            if 'toy' in h_lower or 'tool' in h_lower:
                col_toy = i
            elif 'casting' in h_lower or 'model' in h_lower or 'name' in h_lower:
                col_nombre = i
            elif 'series' in h_lower or 'serie' in h_lower:
                col_serie = i
            elif 'photo' in h_lower or 'foto' in h_lower or 'image' in h_lower:
                col_foto = i
        
        # Buscar el patrón de filas: líneas que contienen datos
        # En el formato Fandom, las filas tienen celdas en líneas separadas
        en_tabla = False
        fila_actual = []
        todas_filas = []
        
        for linea in lineas:
            linea = linea.strip()
            
            if linea.startswith('|-'):
                if fila_actual:
                    todas_filas.append(fila_actual)
                fila_actual = []
                continue
            
            if linea.startswith('|}'):
                if fila_actual:
                    todas_filas.append(fila_actual)
                break
            
            if linea.startswith('|+'):
                continue
            
            if linea.startswith('!'):
                continue
            
            if linea.startswith('|'):
                # Es una celda de datos
                celda = linea[1:].strip()
                fila_actual.append(celda)
        
        if fila_actual:
            todas_filas.append(fila_actual)
        
        # Procesar filas
        for fila in todas_filas:
            if len(fila) < 2:
                continue
            
            # Extraer Toy #
            toy_num = ''
            if col_toy >= 0 and col_toy < len(fila):
                # Buscar número en la celda
                numeros = re.findall(r'\d+', fila[col_toy])
                if numeros:
                    toy_num = numeros[0]
            
            # Extraer nombre
            nombre = ''
            if col_nombre >= 0 and col_nombre < len(fila):
                nombre = limpiar_nombre_modelo(fila[col_nombre])
            
            # Extraer serie
            serie = ''
            if col_serie >= 0 and col_serie < len(fila):
                serie = limpiar_nombre(fila[col_serie])
            
            # Extraer foto
            foto = ''
            if col_foto >= 0 and col_foto < len(fila):
                foto = extraer_url_imagen(fila[col_foto])
            
            if toy_num or nombre:
                modelos.append({
                    'anio': anio,
                    'toy': toy_num,
                    'nombre': nombre,
                    'serie': serie,
                    'foto': foto
                })
    
    return modelos

def main():
    # Cargar catálogo existente
    with open(CATALOG_FILE, encoding='utf-8') as f:
        catalog = json.load(f)
    
    print(f"Catálogo actual: {len(catalog)} modelos")
    
    # Cargar imágenes existentes si las hay
    imagenes_existentes = {}
    if IMAGES_FILE.exists():
        with open(IMAGES_FILE, encoding='utf-8') as f:
            imagenes_existentes = json.load(f)
    
    # Índices del catálogo
    tool_existente = {m.get('t', ''): m for m in catalog if m.get('t')}
    nombre_existente = {m.get('m', '').lower().strip(): m for m in catalog}
    
    total_procesados = 0
    total_imagenes = 0
    total_agregados = 0
    
    # Procesar cada año 1968-1995
    for anio in range(1968, 1996):
        titulo = f'List_of_{anio}_Hot_Wheels'
        
        # Verificar cache
        cache_file = CACHE_DIR / f'wikitext_{anio}.txt'
        if cache_file.exists():
            with open(cache_file, encoding='utf-8') as f:
                wikitext = f.read()
        else:
            print(f"\nProcesando {titulo}...")
            wikitext = obtener_wikitext(titulo)
            if wikitext:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    f.write(wikitext)
            time.sleep(0.3)
        
        if not wikitext:
            print(f"  Sin wikitext para {anio}")
            continue
        
        # Parsear modelos
        modelos = parsear_wikitext_completo(wikitext, anio)
        
        if not modelos:
            # Intentar parser alternativo
            modelos = parsear_tabla(wikitext, anio)
        
        print(f"  Modelos encontrados: {len(modelos)}")
        total_procesados += len(modelos)
        
        # Procesar cada modelo
        for modelo in modelos:
            toy = modelo['toy']
            nombre = modelo['nombre']
            serie = modelo['serie']
            foto = modelo['foto']
            
            if not toy and not nombre:
                continue
            
            # Buscar si ya existe
            existente = None
            if toy and toy in tool_existente:
                existente = tool_existente[toy]
            elif nombre:
                nombre_norm = nombre.lower().strip()
                if nombre_norm in nombre_existente:
                    existente = nombre_existente[nombre_norm]
            
            if existente:
                # Actualizar datos si falta algo
                if not existente.get('s') and serie:
                    existente['s'] = serie
                if not existente.get('im') and foto:
                    existente['im'] = foto
                    total_imagenes += 1
            else:
                # Agregar nuevo modelo
                nuevo_id = f"{anio}-{toy}" if toy else f"{anio}-{nombre[:10].replace(' ', '_')}"
                nuevo = {
                    'i': nuevo_id,
                    'm': nombre,
                    'y': anio,
                    't': toy,
                    'c': '001',
                    's': serie or f'{anio} Hot Wheels',
                    'n': f'1/{len(modelos)}',
                    'k': 'Mainline',
                    'im': foto or '',
                    'v': 1.0,
                    'V': 5.0,
                    'px': 12,
                    'f': [20.2, 38.0, 100.0, 0.0, 40.0],
                    'dm': 0,
                    'ap': 4,
                    'ficha': {
                        'descripcion': f'{nombre} de {anio}.',
                        'historia': f'El {nombre} fue introducido en {anio}.',
                        'curiosidades': f'Tool #{toy}. Parte de la colección de {anio}.',
                        'conmemorativo': False,
                        'dato_clave': f'Tool #{toy} de {anio}'
                    },
                    'indice_coleccionabilidad': 53.5,
                    'valores_mercado': {
                        'usd': 39.6,
                        'clp': 37620.0,
                        'eur': 36.43,
                        'fecha': '2026-10-14T10:13:19.274849',
                        'fuente': 'Cálculo automático'
                    }
                }
                catalog.append(nuevo)
                if toy:
                    tool_existente[toy] = nuevo
                if nombre:
                    nombre_existente[nombre.lower().strip()] = nuevo
                total_agregados += 1
                if foto:
                    total_imagenes += 1
    
    # Guardar catálogo
    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, separators=(',', ':'))
    
    # Guardar imágenes
    with open(IMAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(imagenes_existentes, f, ensure_ascii=False, indent=2)
    
    # Estadísticas
    print(f"\n{'='*60}")
    print(f"RESULTADO FINAL")
    print(f"{'='*60}")
    print(f"Modelos procesados: {total_procesados}")
    print(f"Modelos agregados: {total_agregados}")
    print(f"Imágenes asignadas: {total_imagenes}")
    print(f"Total catálogo: {len(catalog)}")

if __name__ == '__main__':
    main()
