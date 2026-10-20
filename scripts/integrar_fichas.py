#!/usr/bin/env python3
"""Integra las fichas reales + traducciones + galería en el catálogo.
Entrada: data/fichas_traducidas.json
Salida:  data/catalog_web.json (actualizado) e index.html (reconstruido)
"""
import json, re, os, sys

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/'
DATA = BASE + 'data/'

def weserv(u):
    if not u: return u
    if 'weserv' in u: return u
    if u.startswith('http'): return 'https://images.weserv.nl/?url=' + u.replace('https://','')
    return 'https://images.weserv.nl/?url=' + u

def main():
    fichas = json.load(open(DATA + 'fichas_traducidas.json', encoding='utf-8'))
    print(f"Fichas traducidas: {len(fichas)}")

    cat = json.load(open(DATA + 'catalog_web.json', encoding='utf-8'))
    print(f"Catálogo: {len(cat)}")

    aplicadas = 0
    con_galeria = 0
    for m in cat:
        nombre = m.get('m', '').strip()
        if nombre in fichas:
            f = fichas[nombre]
            # Construir ficha enriquecida con idiomas
            ficha = dict(m.get('ficha', {}))
            # Guardar los textos base (inglés) si vienen
            es = f.get('es', {}); pt = f.get('pt', {}); fr = f.get('fr', {})
            # Base: usar la versión en español si existe (la app default es 'es')
            ficha['es'] = es
            ficha['pt'] = pt
            ficha['fr'] = fr
            # Campos planos: poner el español como default (o el original si no hay traducción)
            ficha['descripcion'] = es.get('descripcion') or ficha.get('descripcion', '')
            ficha['historia'] = es.get('historia') or ficha.get('historia', '')
            ficha['curiosidades'] = es.get('curiosidades') or ficha.get('curiosidades', '')
            ficha['dato_clave'] = es.get('dato_clave') or ficha.get('dato_clave', '')
            # Galería
            gal = f.get('galeria', [])
            if gal:
                m['galeria'] = [weserv(u) for u in gal[:8]]
                con_galeria += 1
            if f.get('disenador'):
                m['disenador'] = f['disenador']
            m['ficha'] = ficha
            aplicadas += 1

    print(f"Fichas aplicadas: {aplicadas}")
    print(f"Con galería: {con_galeria}")

    json.dump(cat, open(DATA + 'catalog_web.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

    # Reconstruir el CAT en el HTML
    def find_end(s, oi):
        depth = 0; in_str = False; esc = False
        for j in range(oi, len(s)):
            ch = s[j]
            if in_str:
                if esc: esc = False
                elif ch == '\\': esc = True
                elif ch == '"': in_str = False
                continue
            if ch == '"': in_str = True
            elif ch in '[{': depth += 1
            elif ch in ']}':
                depth -= 1
                if depth == 0: return j + 1
        return -1

    html = open(BASE + 'index.html', encoding='utf-8').read()
    i = html.find('const CAT=[')
    if i < 0:
        print("✗ no se encontró const CAT="); return 1
    oi = html.find('[', i); ei = find_end(html, oi)
    html = html[:oi] + json.dumps(cat, ensure_ascii=False, separators=(',', ':')) + html[ei:]
    open(BASE + 'index.html', 'w', encoding='utf-8').write(html)
    print(f"HTML reconstruido: {len(html):,} chars")
    return 0

if __name__ == '__main__':
    sys.exit(main())
