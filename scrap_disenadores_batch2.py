#!/usr/bin/env python3
"""Extrae diseñadores faltantes del catálogo Hot Wheels desde Fandom.

Técnica: name-matching. Para cada diseñador pendiente, se obtiene su página
de Fandom, se extraen los nombres de modelos (wikilinks relevantes) y se
asignan al catálogo por coincidencia exacta de nombre.
"""

import json, re, time, urllib.request, urllib.parse, sys, os
from bs4 import BeautifulSoup

BASE = r"C:\Users\GODZILLA24H2\Desktop\hotwheels_collector"
CATALOGO_PATH = os.path.join(BASE, "data", "catalog_web.json")
RESTANTES_PATH = os.path.join(BASE, "data", "disenadores_restantes.json")
SALIDA_PATH = os.path.join(BASE, "data", "disenadores_batch2.json")

UA = "Mozilla/5.0 (hotwheels-research)"
REFERER = "https://hotwheels.fandom.com/"

def api_fandom(params):
    """Llamada a la API MediaWiki de Fandom."""
    url = "https://hotwheels.fandom.com/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Referer", REFERER)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw)
    except Exception as e:
        return {"error": str(e)}

def obtener_wikitext(titulo):
    """Obtiene el wikitext de una página de Fandom."""
    data = api_fandom({
        "action": "query",
        "prop": "revisions",
        "titles": titulo,
        "rvslots": "*",
        "rvprop": "content",
        "format": "json",
        "formatversion": 2
    })
    if "error" in data:
        return None, data["error"]
    pages = data.get("query", {}).get("pages", [])
    if not pages:
        return None, "Página no encontrada"
    revisions = pages[0].get("revisions", [])
    if not revisions:
        return None, "Sin revisiones"
    content = revisions[0].get("slots", {}).get("main", {}).get("content", "")
    return content, None

def extraer_modelos_tabla(wikitext):
    """Extrae nombres de modelos de la tabla de proyectos en wikitext.
    
    Busca tablas con columna 'Casting Name' y extrae los wikilinks de esa columna.
    También extrae todos los wikilinks relevantes como fallback.
    """
    modelos = []
    
    # Buscar tablas que contengan "Casting Name"
    tabla_pattern = r'\{\|[^}]*?Casting Name.*?\|\}'
    tablas = re.findall(tabla_pattern, wikitext, re.DOTALL | re.IGNORECASE)
    
    if tablas:
        for tabla in tablas:
            # Extraer filas de la tabla
            filas = re.findall(r'\|-(.*?)(?=\|-|\|\})', tabla, re.DOTALL)
            for fila in filas:
                # Buscar wikilinks en la fila
                enlaces = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', fila)
                for enlace in enlaces:
                    # Limpiar nombre
                    nombre = enlace.strip()
                    # Filtros
                    if not nombre or len(nombre) < 3:
                        continue
                    if nombre.startswith(("Image:", "Category:", "File:")):
                        continue
                    if re.match(r'^\d{4}$', nombre):  # años
                        continue
                    if nombre.startswith("20") and "Hot Wheels" in nombre:
                        continue
                    # Excluir nombres de series comunes
                    series_skip = [
                        "New Models", "Treasure Hunt", "Super Treasure Hunt",
                        "First Editions", "Sweet Sixteen", "Street Beasts",
                        "HW Racers", "HW Imagination", "HW Graphics",
                        "AcceleRacers", "Speed Graphics", "Track Stars",
                        "HW Workshop", "City Works", "HW Rescue",
                        "HW Speed", "HW Stunt", "HW Trucks", "HW Racers",
                        "Basic Cars", "Track Sets", "Play Sets",
                    ]
                    if nombre in series_skip:
                        continue
                    modelos.append(nombre)
    
    # Fallback: extraer todos los wikilinks relevantes del wikitext
    if not modelos:
        todos_enlaces = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', wikitext)
        for enlace in todos_enlaces:
            nombre = enlace.strip()
            if not nombre or len(nombre) < 3:
                continue
            if nombre.startswith(("Image:", "Category:", "File:", "Template:", "User:")):
                continue
            if re.match(r'^\d{4}$', nombre):
                continue
            if nombre.startswith("20") and "Hot Wheels" in nombre:
                continue
            modelos.append(nombre)
    
    return list(set(modelos))

def normalizar_nombre(n):
    """Normaliza nombre de modelo para matching."""
    n = n.strip().lower()
    n = re.sub(r"\s+", " ", n)
    return n

def main():
    print("=" * 60)
    print("SCRAPING DE DISEÑADORES FALTANTES - BATCH 2")
    print("=" * 60)
    
    # Cargar datos
    with open(CATALOGO_PATH, encoding="utf-8") as f:
        catalogo = json.load(f)
    with open(RESTANTES_PATH, encoding="utf-8") as f:
        disenadores_restantes = json.load(f)
    
    print(f"Catálogo: {len(catalogo)} modelos")
    print(f"Diseñadores restantes a procesar: {len(disenadores_restantes)}")
    
    # Índice de modelos sin diseñador
    sin_diseñador = {}
    for modelo in catalogo:
        nombre = modelo.get("m", "").strip()
        if nombre and not modelo.get("diseñador") and not modelo.get("disenador"):
            sin_diseñador[normalizar_nombre(nombre)] = modelo
    
    print(f"Modelos sin diseñador en catálogo: {len(sin_diseñador)}")
    
    # Procesar cada diseñador
    resultados = {}
    errores = []
    asignaciones = {}
    total_asignados = 0
    
    disenadores_lista = list(disenadores_restantes.items())
    total = len(disenadores_lista)
    
    for idx, (nombre_disenador, info) in enumerate(disenadores_lista, 1):
        print(f"\n[{idx}/{total}] Procesando: {nombre_disenador}")
        
        # Construir título de página
        titulo = nombre_disenador.replace(" ", "_")
        
        # Obtener wikitext de la página
        wikitext, err = obtener_wikitext(titulo)
        if err or not wikitext:
            error_msg = f"{nombre_disenador}: error al obtener wikitext - {err or 'wikitext vacío'}"
            print(f"  ERROR: {error_msg}")
            errores.append(error_msg)
            resultados[nombre_disenador] = {
                "bio": info.get("bio", ""),
                "tools": [],
                "asignados": [],
                "error": err or "wikitext vacío"
            }
            time.sleep(0.5)
            continue
        
        # Extraer nombres de modelos de la tabla
        nombres = extraer_modelos_tabla(wikitext)
        print(f"  Modelos extraídos: {len(nombres)}")
        
        # Hacer matching con el catálogo
        asignados = []
        for nom in nombres:
            nom_norm = normalizar_nombre(nom)
            if nom_norm in sin_diseñador:
                modelo = sin_diseñador[nom_norm]
                # Verificar que no tenga ya diseñador
                if not modelo.get("diseñador") and not modelo.get("disenador"):
                    modelo["diseñador"] = nombre_disenador
                    asignados.append(modelo.get("m", nom))
                    total_asignados += 1
        
        print(f"  Modelos asignados: {len(asignados)}")
        if asignados:
            for a in asignados[:5]:
                print(f"    - {a}")
            if len(asignados) > 5:
                print(f"    ... y {len(asignados) - 5} más")
        
        resultados[nombre_disenador] = {
            "bio": info.get("bio", ""),
            "tools": info.get("tools", []),
            "nombres_extraidos": len(nombres),
            "asignados": asignados
        }
        
        # Petición cada 1.5s para no saturar
        time.sleep(1.5)
    
    # Guardar resultados
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    print(f"Diseñadores procesados: {len(resultados)}")
    print(f"Total asignaciones: {total_asignados}")
    print(f"Errores: {len(errores)}")
    
    with open(SALIDA_PATH, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    # Guardar catálogo actualizado
    with open(CATALOGO_PATH, "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, separators=(",", ":"))
    
    print(f"\nGuardado: {SALIDA_PATH}")
    print(f"Catálogo actualizado: {CATALOGO_PATH}")
    
    return {
        "diseñadores_encontrados": len(resultados),
        "total_asignados": total_asignados,
        "errores": errores,
        "success": True
    }

if __name__ == "__main__":
    resultado = main()
    print(f"\n{json.dumps(resultado, ensure_ascii=False, indent=2)}")