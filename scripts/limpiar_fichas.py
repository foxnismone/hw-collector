#!/usr/bin/env python3
"""Limpia el wikitext residual de las fichas (descripcion/curiosidades/dato_clave)
y repara las traducciones con el mismo criterio.
Entradas:  data/fichas_reales.json, data/fichas_traducidas.json
"""
import json, re, os

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def limpiar_wiki(t):
    if not t: return ''
    t = str(t)
    # Plantillas {{...}} (anidadas simples)
    prev = None
    while prev != t:
        prev = t
        t = re.sub(r'\{\{[^{}]*\}\}', ' ', t)
    # Archivos e imágenes
    t = re.sub(r'\[\[(?:File|Image|Archivo):[^\]]*\]\]', ' ', t, flags=re.I)
    # Wikilinks
    t = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[\[([^\]]*)\]\]', r'\1', t)
    # Enlaces externos con texto
    t = re.sub(r'\[https?://\S+\s+([^\]]*)\]', r'\1', t)
    t = re.sub(r'\[https?://\S+\]', ' ', t)
    # Negritas / cursivas wiki
    t = re.sub(r"'{2,}", '', t)
    # Categorías y marcadores
    t = re.sub(r'\[\[Category:[^\]]*\]\]', ' ', t, flags=re.I)
    t = re.sub(r'^\s*[:*#;].*$', ' ', t, flags=re.MULTILINE)
    # HTML
    t = re.sub(r'<ref[^>]*>.*?</ref>', ' ', t, flags=re.DOTALL|re.I)
    t = re.sub(r'<ref[^>]*/>', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    # Entidades
    t = t.replace('&ndash;','-').replace('&mdash;','—').replace('&nbsp;',' ')
    t = t.replace('&amp;','&').replace('&quot;','"').replace('&#39;',"'")
    # Colapsar
    t = re.sub(r'\s{2,}', ' ', t)
    return t.strip()

def limpiar_diccionario(obj):
    """Limpia todos los valores de texto de un dict (recursivo 1 nivel)."""
    if not isinstance(obj, dict): return obj
    out = {}
    for k, v in obj.items():
        if isinstance(v, str):
            out[k] = limpiar_wiki(v)
        elif isinstance(v, dict):
            out[k] = {kk: limpiar_wiki(vv) if isinstance(vv, str) else vv for kk, vv in v.items()}
        elif isinstance(v, list):
            out[k] = [limpiar_wiki(x) if isinstance(x, str) else x for x in v]
        else:
            out[k] = v
    return out

def main():
    for nombre_archivo in ('fichas_reales.json', 'fichas_traducidas.json'):
        p = BASE + nombre_archivo
        if not os.path.exists(p):
            print(f"{nombre_archivo}: no existe, se omite")
            continue
        datos = json.load(open(p, encoding='utf-8'))
        limpios = {k: limpiar_diccionario(v) for k, v in datos.items()}
        json.dump(limpios, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print(f"{nombre_archivo}: {len(limpios)} limpiadas")

    # Verificación
    datos = json.load(open(BASE + 'fichas_reales.json', encoding='utf-8'))
    basura = sum(1 for f in datos.values() if any(c in str(f.get('descripcion','')) for c in ['[[', ']]', '{{', "'''", 'category:']))
    print(f"\nFichas con basura residual: {basura}/{len(datos)}")
    # Ejemplo
    ej = datos.get('Batmobile') or list(datos.values())[0]
    print(f"Ejemplo: {ej.get('descripcion','')[:200]}")

if __name__ == '__main__':
    main()
