#!/usr/bin/env python3
"""
Sistema de integración de datos para HW Collector.
Integra los datos de Fandom Wiki con el catálogo actual,
agregando ficha, índice de coleccionabilidad, valores y categorías.

Uso:
    python build/integrar_datos.py data/new_models_batch1.json data/new_models_batch2.json

El sistema:
1. Carga el catálogo actual (catalog_web.json)
2. Carga los modelos parseados de Fandom
3. Para cada modelo nuevo, genera:
   - Ficha completa (descripción, historia, curiosidades, conmemorativo)
   - Índice de coleccionabilidad (0-100) con factores
   - Valores de mercado (CLP, USD, EUR)
   - Categoría con descripción
4. Guarda el catálogo actualizado
"""

import sys
import json
import math
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent / 'data'
CATALOG_FILE = DATA_DIR / 'catalog_web.json'
CATEGORIES_FILE = DATA_DIR / 'categorias.json'

# ============================================================================
# CATEGORÍAS CON DESCRIPCIÓN
# ============================================================================
CATEGORIAS = {
    'mainline': {
        'nombre': 'Mainline',
        'descripcion': 'Modelos estándar de Hot Wheels disponibles en tiendas minoristas. Son la línea principal con blister card individual. Incluye todos los años desde 1968.',
        'color': '#3b82f6',
        'icon': '🚗'
    },
    'treasure_hunt': {
        'nombre': 'Treasure Hunt',
        'descripcion': 'Modelos raros con acabado especial (Spectraflame o edición especial). Solo 1 de cada 72 cajas aproximadamente. Muy buscados por coleccionistas.',
        'color': '#f59e0b',
        'icon': '🏆'
    },
    'super_treasure_hunt': {
        'nombre': 'Super Treasure Hunt',
        'descripcion': 'Modelos extremadamente raros con acabado premium (ruedas rubber, pintura especial). Solo 1 de cada 144 cajas. Los más valiosos de la línea mainline.',
        'color': '#ef4444',
        'icon': '⭐'
    },
    'car_culture': {
        'nombre': 'Car Culture',
        'descripcion': 'Línea premium con detalles realistas, ruedas rubber y acabados de alta calidad. Incluye series como Muscle Mania, Euro Style, Japan Historics.',
        'color': '#8b5cf6',
        'icon': '🏁'
    },
    'team_transport': {
        'nombre': 'Team Transport',
        'descripcion': 'Camiones premium con remolque. Cada camión tiene un remolque específico que representa su equipo. Línea de alta calidad.',
        'color': '#10b981',
        'icon': '🚛'
    },
    'exclusivo': {
        'nombre': 'Exclusivo',
        'descripcion': 'Modelos exclusivos de tiendas específicas (Target, Walmart, Toys R Us, etc.). No disponibles en todas las regiones.',
        'color': '#f97316',
        'icon': '🏪'
    },
    'vintage': {
        'nombre': 'Vintage',
        'descripcion': 'Modelos antiguos de los años 60-80. Incluye las primeras ediciones (Redline) y clásicos muy buscados.',
        'color': '#78716c',
        'icon': '📜'
    },
    'modern': {
        'nombre': 'Modern',
        'descripcion': 'Modelos recientes de 2015 en adelante. Incluye las líneas actuales con blister card moderno.',
        'color': '#06b6d4',
        'icon': '🆕'
    },
    'rlc': {
        'nombre': 'Red Line Club',
        'descripcion': 'Modelos exclusivos para miembros del Red Line Club (RLC). Suscripción anual, modelos limitados con acabados premium.',
        'color': '#dc2626',
        'icon': '🔴'
    }
}

# ============================================================================
# ÍNDICE DE COLECCIONABILIDAD
# ============================================================================
def calcular_indice_coleccionabilidad(modelo):
    """
    Calcula el índice de coleccionabilidad (0-100) basado en:
    - Rareza (0-100): basado en producción y disponibilidad
    - Demanda (0-100): basado en búsquedas y ventas
    - Valoración (0-100): basado en precios de mercado
    - Tendencia (0-100): basado en crecimiento de valor
    - Completitud (0-100): basado en importancia para la colección
    """
    año = modelo.get('y') or 2024
    año_actual = datetime.now().year
    edad = max(0, año_actual - año)
    
    # Rareza: modelos más antiguos = más raros
    if edad >= 50:
        rareza = 95
    elif edad >= 40:
        rareza = 85
    elif edad >= 30:
        rareza = 75
    elif edad >= 20:
        rareza = 65
    elif edad >= 10:
        rareza = 55
    else:
        rareza = 40
    
    # Demanda: base (se actualiza con datos de mercado)
    demanda = 50
    
    # Valoración: basada en el valor base
    valor_base = modelo.get('x', 5.0)
    if valor_base >= 50:
        valoracion = 95
    elif valor_base >= 20:
        valoracion = 80
    elif valor_base >= 10:
        valoracion = 65
    elif valor_base >= 5:
        valoracion = 50
    else:
        valoracion = 35
    
    # Tendencia: modelos antiguos tienden a subir más
    tendencia = min(100, 50 + edad * 2)
    
    # Completitud: importancia para la colección
    completitud = 50
    
    # Índice ponderado
    indice = (
        rareza * 0.25 +
        demanda * 0.25 +
        valoracion * 0.20 +
        tendencia * 0.15 +
        completitud * 0.15
    )
    
    return round(min(100, max(0, indice)), 1)

# ============================================================================
# VALORES DE MERCADO
# ============================================================================
def calcular_valores_mercado(modelo):
    """
    Calcula valores de mercado en CLP, USD y EUR.
    Basado en el valor base y factores de mercado.
    """
    valor_base = modelo.get('x', 5.0)
    año = modelo.get('y') or 2024
    año_actual = datetime.now().year
    edad = max(0, año_actual - año)
    
    # Factor de apreciación por antigüedad
    factor_edad = 1 + (edad * 0.03)
    
    # Valor en USD
    usd = round(valor_base * factor_edad, 2)
    
    # Valor en CLP (tipo de cambio aproximado)
    clp = round(usd * 950, 0)
    
    # Valor en EUR
    eur = round(usd * 0.92, 2)
    
    return {
        'usd': usd,
        'clp': clp,
        'eur': eur,
        'fecha': datetime.now().isoformat(),
        'fuente': 'Cálculo automático'
    }

# ============================================================================
# FICHA COMPLETA
# ============================================================================
def generar_ficha(modelo):
    """
    Genera la ficha completa del modelo:
    - Descripción
    - Historia
    - Curiosidades
    - Conmemorativo
    - Dato clave
    """
    nombre = modelo.get('m', 'Desconocido')
    año = modelo.get('y', 2024)
    serie = modelo.get('s', 'Desconocida')
    categoria = modelo.get('k', 'Mainline')
    tool = modelo.get('t', modelo.get('i', ''))
    
    descripcion = f"{nombre} de {año}. Serie: {serie}. Categoría: {categoria}."
    
    historia = f"El {nombre} fue introducido en {año} como parte de la línea {serie}."
    
    curiosidades = f"Tool #{tool}. Parte de la colección de {año}."
    
    conmemorativo = False
    dato_clave = f"Tool #{tool} de {año}"
    
    return {
        'descripcion': descripcion,
        'historia': historia,
        'curiosidades': curiosidades,
        'conmemorativo': conmemorativo,
        'dato_clave': dato_clave
    }

# ============================================================================
# INTEGRACIÓN DE DATOS
# ============================================================================
def integrar_modelo(dato_fandom, catalogo_existente):
    """
    Integra un dato de Fandom con el formato completo del catálogo.
    Si el modelo ya existe, lo actualiza con los datos de Fandom.
    Si no existe, crea una entrada nueva con todos los campos.
    """
    tool = dato_fandom.get('tool_number', '')
    nombre = dato_fandom.get('name', '')
    año = dato_fandom.get('year', 2024)
    
    # Verificar si ya existe
    existente = None
    for modelo in catalogo_existente:
        if modelo.get('i') == tool or modelo.get('t') == tool:
            existente = modelo
            break
    
    if existente:
        # Actualizar con datos de Fandom
        existente['m'] = nombre
        existente['y'] = año
        # Agregar ficha, índice y valores
        existente['ficha'] = generar_ficha(existente)
        existente['indice_coleccionabilidad'] = calcular_indice_coleccionabilidad(existente)
        existente['valores_mercado'] = calcular_valores_mercado(existente)
        return existente
    else:
        # Crear nueva entrada
        nuevo = {
            'i': tool,
            'm': nombre,
            'y': año,
            't': tool,
            'c': '000',
            's': 'Desconocida',
            'n': '1/1',
            'k': 'Mainline',
            'x': 5.0,
            'im': '',
            'v': 1.0,
            'V': 10.0,
            'px': 1,
            'f': [50.0, 50.0, 50.0, 50.0, 50.0],
            'dm': 0,
            'ap': 0,
            'ficha': generar_ficha({'m': nombre, 'y': año, 's': 'Desconocida', 'k': 'Mainline', 't': tool, 'x': 5.0}),
            'indice_coleccionabilidad': calcular_indice_coleccionabilidad({'x': 5.0, 'y': año}),
            'valores_mercado': calcular_valores_mercado({'x': 5.0, 'y': año}),
            'categoria_descripcion': CATEGORIAS.get('mainline', {}).get('descripcion', '')
        }
        return nuevo

def guardar_categorias():
    """Guarda las categorías con su descripción."""
    CATEGORIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(CATEGORIAS, f, ensure_ascii=False, indent=2)
    print(f"✅ Categorías guardadas: {len(CATEGORIAS)} categorías")

def integrar_datos(archivos_fandom):
    """Integra los datos de Fandom con el catálogo actual."""
    # Cargar catálogo actual
    catalogo = []
    if CATALOG_FILE.exists():
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalogo = json.load(f)
    print(f"📊 Catálogo actual: {len(catalogo)} modelos")
    
    # Guardar categorías
    guardar_categorias()
    
    # Procesar archivos de Fandom
    ids_existentes = {m.get('i', '') for m in catalogo}
    ids_tool = {m.get('t', '') for m in catalogo}
    
    nuevos = 0
    actualizados = 0
    
    for archivo in archivos_fandom:
        ruta = Path(archivo)
        if not ruta.exists():
            print(f"  ⚠️  No existe: {archivo}")
            continue
        
        with open(ruta, 'r', encoding='utf-8') as f:
            datos_fandom = json.load(f)
        
        for dato in datos_fandom:
            tool = dato.get('tool_number', '')
            if not tool:
                continue
            
            # Verificar si ya existe por ID o tool
            if tool in ids_existentes or tool in ids_tool:
                # Actualizar existente
                for modelo in catalogo:
                    if modelo.get('i') == tool or modelo.get('t') == tool:
                        modelo['m'] = dato.get('name', modelo.get('m'))
                        modelo['y'] = dato.get('year', modelo.get('y'))
                        modelo['ficha'] = generar_ficha(modelo)
                        modelo['indice_coleccionabilidad'] = calcular_indice_coleccionabilidad(modelo)
                        modelo['valores_mercado'] = calcular_valores_mercado(modelo)
                        actualizados += 1
                        break
            else:
                # Crear nuevo
                nuevo = integrar_modelo(dato, catalogo)
                catalogo.append(nuevo)
                ids_existentes.add(nuevo['i'])
                ids_tool.add(nuevo['t'])
                nuevos += 1
        
        print(f"  ✓ {ruta.name}: {len(datos_fandom)} modelos procesados")
    
    # Guardar catálogo actualizado
    CATALOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalogo, f, ensure_ascii=False, separators=(',', ':'))
    
    print(f"\n{'='*50}")
    print(f"✅ Integración completada")
    print(f"{'='*50}")
    print(f"  Nuevos: {nuevos}")
    print(f"  Actualizados: {actualizados}")
    print(f"  Total: {len(catalogo)}")
    
    return nuevos, actualizados

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python build/integrar_datos.py <archivo1.json> [archivo2.json] ...")
        sys.exit(1)
    integrar_datos(sys.argv[1:])
