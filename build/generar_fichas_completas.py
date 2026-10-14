#!/usr/bin/env python3
"""
Genera ficha, índice de coleccionabilidad y valores de mercado
para TODOS los modelos del catálogo (incluyendo los originales 2016-2026).

Uso:
    python build/generar_fichas_completas.py
"""

import json
import math
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent / 'data'
CATALOG_FILE = DATA_DIR / 'catalog_web.json'

def calcular_indice_coleccionabilidad(modelo):
    """Calcula el índice de coleccionabilidad (0-100)."""
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
    
    # Demanda: base
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

def calcular_valores_mercado(modelo):
    """Calcula valores de mercado en CLP, USD y EUR."""
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

def generar_ficha(modelo):
    """Genera la ficha completa del modelo."""
    nombre = modelo.get('m', 'Desconocido')
    año = modelo.get('y') or 2024
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

def main():
    # Cargar catálogo
    with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
        catalogo = json.load(f)
    
    print(f"Total modelos: {len(catalogo)}")
    
    # Generar ficha, índice y valores para TODOS los modelos
    actualizados = 0
    for modelo in catalogo:
        if 'ficha' not in modelo:
            modelo['ficha'] = generar_ficha(modelo)
            actualizados += 1
        if 'indice_coleccionabilidad' not in modelo:
            modelo['indice_coleccionabilidad'] = calcular_indice_coleccionabilidad(modelo)
        if 'valores_mercado' not in modelo:
            modelo['valores_mercado'] = calcular_valores_mercado(modelo)
    
    # Guardar catálogo actualizado
    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalogo, f, ensure_ascii=False, separators=(',', ':'))
    
    print(f"✅ Fichas generadas: {actualizados}")
    print(f"✅ Índices calculados: {len([x for x in catalogo if 'indice_coleccionabilidad' in x])}")
    print(f"✅ Valores calculados: {len([x for x in catalogo if 'valores_mercado' in x])}")

if __name__ == '__main__':
    main()
