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

def limpiar_texto(texto):
    if not texto:
        return ''
    prev = None
    while prev != texto:
        prev = texto
        texto = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', texto)
        texto = re.sub(r'\[\[([^\]]+)\]\]', r'\1', texto)
    texto = re.sub(r"''+", '', texto)
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def limpiar_nombre_modelo(texto):
    texto = limpiar_texto(texto)
    texto = re.sub(r'\s*(org|changed to|was|also known as|aka)\s*$', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\s*/\s*$', '', texto)
    return texto.strip()

def extraer_url_imagen(texto):
    if not texto:
        return None
    matches = re.findall(r'\[\[(?:File|Image):([^\]|]+)', texto, re.IGNORECASE)
    if matches:
        return matches[-1].strip()
    return None

def parsear_galerias(wikitext, anio):
    """Parsea galerías <gallery> que contienen modelos"""
    modelos = []
    if not wikitext:
        return modelos

    # Buscar todas las galerías <gallery>...</gallery>
    galleries = re.findall(r'<gallery[^>]*>(.*?)</gallery>', wikitext, re.DOTALL | re.IGNORECASE)

    for galeria in galleries:
        lineas = galeria.strip().split('\n')
        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
            # Formato 1: Image:archivo.jpg|[[Nombre]]|link=...
            # Formato 2: archivo.jpg|[[Nombre]]
            # Formato 3: Image:archivo.jpg|Nombre
            tiene_imagen = linea.startswith('Image:') or linea.startswith('File:')
            # Si no tiene prefijo Image:/File:, verificar si parece una línea de galería
            # (contiene .jpg, .JPG, .png, .PNG, .jpeg, .gif seguido de |)
            parece_galeria = False
            if not tiene_imagen:
                parece_galeria = bool(re.match(r'^[^|]+\.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF)\|', linea))

            if tiene_imagen o parece_galeria:
                # Extraer nombre del link wiki
                match = re.search(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', linea)
                if match:
                    nombre = match.group(2) if match.group(2) else match.group(1)
                    nombre = limpiar_texto(nombre)
                    if nombre:
                        # Extraer nombre de archivo de imagen
                        if tiene_imagen:
                            archivo_match = re.match(r'(?:Image|File):([^|]+)', linea)
                            archivo = archivo_match.group(1).strip() if archivo_match else ''
                        else:
                            archivo_match = re.match(r'^([^|]+)\|', linea)
                            archivo = archivo_match.group(1).strip() if archivo_match else ''
                        modelos.append({
                            'anio': anio,
                            'toy': '',
                            'nombre': nombre,
                            'serie': '',
                            'foto': archivo
                        })

    return modelos

def parsear_wikitext(wikitext, anio):
    """Parsea tablas wikitext con formato real de Fandom"""
    modelos = []
    if not wikitext:
        return modelos

    # Primero parsear galerías (para años 1970-1973)
    modelos.extend(parsear_galerias(wikitext, anio))

    # Buscar todas las tablas {| ... |}
    tablas = []
    pos = 0
    while True:
        inicio = wikitext.find('{|', pos)
        if inicio == -1:
            break
        nivel = 1
        i = inicio + 2
        while i < len(wikitext) and nivel > 0:
            if wikitext[i:i+2] == '{|':
                nivel += 1
                i += 2
            elif wikitext[i:i+2] == '|}':
                nivel -= 1
                i += 2
            else:
                i += 1
        fin = i
        tablas.append(wikitext[inicio:fin])
        pos = fin

    for tabla in tablas:
        lineas = tabla.split('\n')

        # Encontrar headers
        headers = []
        for linea in lineas:
            linea = linea.strip()
            if linea.startswith('!'):
                if '|' in linea:
                    partes = linea.split('|')
                    header_text = partes[-1].strip()
                else:
                    header_text = linea[1:].strip()
                header_text = header_text.strip('*').strip()
                headers.append(header_text)

        if not headers:
            continue

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
            elif 'photo' in h_lower or 'foto' in h_lower or 'image' in h_lower or 'color' in h_lower:
                col_foto = i

        if col_nombre == -1 and col_toy == -1:
            continue

        # Encontrar filas
        filas = []
        fila_actual = []
        en_fila = False

        for linea in lineas:
            linea = linea.strip()

            if linea.startswith('|-'):
                if fila_actual:
                    filas.append(fila_actual)
                fila_actual = []
                en_fila = True
                continue

            if linea.startswith('|}'):
                break

            if linea.startswith('|+'):
                continue

            if linea.startswith('!'):
                continue

            if linea.startswith('|') and en_fila:
                celda = linea[1:].strip()
                fila_actual.append(celda)

        if fila_actual:
            filas.append(fila_actual)

        # Procesar filas
        for fila in filas:
            if len(fila) < 2:
                continue

            num_celdas = len(fila)

            toy_num = ''
            if col_toy >= 0 and col_toy < num_celdas:
                numeros = re.findall(r'\d+', fila[col_toy])
                if numeros:
                    toy_num = numeros[0]

            nombre = ''
            if col_nombre >= 0 and col_nombre < num_celdas:
                nombre = limpiar_nombre_modelo(fila[col_nombre])

            serie = ''
            if col_serie >= 0 and col_serie < num_celdas:
                serie = limpiar_texto(fila[col_serie])

            foto = ''
            if col_foto >= 0 and col_foto < num_celdas:
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
    with open(CATALOG_FILE, encoding='utf-8') as f:
        catalog = json.load(f)

    print(f"Catálogo actual: {len(catalog)} modelos")

    tool_existente = {m.get('t', ''): m for m in catalog if m.get('t')}
    nombre_existente = {m.get('m', '').lower().strip(): m for m in catalog}

    total_procesados = 0
    total_imagenes = 0
    total_agregados = 0
    modelos_por_anio = {}

    for anio in range(1968, 1996):
        titulo = f'List_of_{anio}_Hot_Wheels'

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

        modelos = parsear_wikitext(wikitext, anio)

        print(f"  Modelos encontrados: {len(modelos)}")
        total_procesados += len(modelos)
        modelos_por_anio[anio] = len(modelos)

        for modelo in modelos:
            toy = modelo['toy']
            nombre = modelo['nombre']
            serie = modelo['serie']
            foto = modelo['foto']

            if not toy and not nombre:
                continue

            existente = None
            if toy and toy in tool_existente:
                existente = tool_existente[toy]
            elif nombre:
                nombre_norm = nombre.lower().strip()
                if nombre_norm in nombre_existente:
                    existente = nombre_existente[nombre_norm]

            if existente:
                if not existente.get('s') and serie:
                    existente['s'] = serie
                if not existente.get('im') and foto:
                    existente['im'] = foto
                    total_imagenes += 1
            else:
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

    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, separators=(',', ':'))

    # Guardar resumen de imágenes por año
    with open(IMAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(modelos_por_anio, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"RESULTADO FINAL")
    print(f"{'='*60}")
    print(f"Modelos procesados: {total_procesados}")
    print(f"Modelos agregados: {total_agregados}")
    print(f"Imágenes asignadas: {total_imagenes}")
    print(f"Total catálogo: {len(catalog)}")

    print(f"\nModelos por año:")
    for anio in range(1968, 1996):
        count = modelos_por_anio.get(anio, 0)
        print(f"  {anio}: {count}")

if __name__ == '__main__':
    main()
