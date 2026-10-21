#!/usr/bin/env python3
"""Integra las fichas REALES de Fandom (descripcion, curiosidades, disenador, galeria)
al catalogo, reemplazando las fichas genericas. Usa traducciones cuando existan."""
import json, re

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def norm(s):
    s = (s or '').lower()
    s = re.sub(r"\s*\(\d+(st|nd|rd|th) color[^)]*\)", '', s)
    s = re.sub(r"\s*\(color variant[^)]*\)", '', s)
    s = re.sub(r"\s*\(treasure hunt\)", '', s)
    s = re.sub(r"\s*\(\d{4}\)", '', s)
    s = re.sub(r"[^a-z0-9]", '', s)
    return s

def weserv(u):
    if not u: return ''
    if 'weserv' in u: return u
    if u.startswith('http'): u = u.replace('https://','')
    return 'https://images.weserv.nl/?url=' + u

def main():
    cat = json.load(open(BASE + 'catalog_web.json', encoding='utf-8'))
    fr = json.load(open(BASE + 'fichas_reales.json', encoding='utf-8'))
    ft = json.load(open(BASE + 'fichas_traducidas.json', encoding='utf-8'))

    # indice por nombre normalizado
    idx = {}
    for nombre, ficha in fr.items():
        if ficha:
            idx[norm(nombre)] = (nombre, ficha)

    aplicadas = 0
    con_galeria = 0
    con_traduccion = 0
    con_disenador = 0

    for m in cat:
        clave = norm(m.get('m'))
        if clave not in idx: continue
        nombre, ficha = idx[clave]

        # texto base (ingles de la wiki) o traduccion
        trad = ft.get(nombre, {})
        es = trad.get('es', {})
        pt = trad.get('pt', {})
        fr_l = trad.get('fr', {})

        desc = es.get('descripcion') or ficha.get('descripcion') or ''
        hist = es.get('historia') or desc
        cur = es.get('curiosidades') or ficha.get('curiosidades') or ''
        dk = es.get('dato_clave') or ficha.get('disenador') or m.get('t','')

        m['ficha'] = {
            'descripcion': desc,
            'historia': hist,
            'curiosidades': cur,
            'conmemorativo': bool(m.get('ficha',{}).get('conmemorativo', False)),
            'dato_clave': dk,
        }
        if es: m['ficha']['es'] = es
        if pt: m['ficha']['pt'] = pt
        if fr_l: m['ficha']['fr'] = fr_l
        if es: con_traduccion += 1

        # galeria
        gal = ficha.get('galeria', [])
        if gal:
            urls = [weserv(u) for u in gal[:8] if u]
            if urls:
                m['galeria'] = urls
                con_galeria += 1

        # disenador
        if ficha.get('disenador') and not m.get('disenador'):
            m['disenador'] = ficha['disenador']
            con_disenador += 1

        aplicadas += 1

    print(f"Fichas reales aplicadas: {aplicadas}")
    print(f"Con galeria: {con_galeria}")
    print(f"Con traduccion es/pt/fr: {con_traduccion}")
    print(f"Disenadores asignados: {con_disenador}")

    json.dump(cat, open(BASE + 'catalog_web.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
    txt = json.dumps(cat, ensure_ascii=False, separators=(',',':'))
    open('C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/cat.js','w',encoding='utf-8').write('const CAT=' + txt + ';\n')
    print(f"cat.js regenerado ({len(txt)/1024/1024:.1f} MB)")

if __name__ == '__main__':
    main()
