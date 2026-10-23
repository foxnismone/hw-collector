#!/usr/bin/env python3
"""Repara URLs de Fandom malformadas: les falta el hash MD5 de MediaWiki.
Correcto: /images/{md5[0]}/{md5[0:2]}/{archivo}
"""
import json, hashlib, re, urllib.parse

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'
HASH_RE = re.compile(r'/images/([a-f0-9])/([a-f0-9]{2})/')

def reparar(u):
    if not u or 'static.wikia' not in u or 'weserv' not in u:
        return u, False
    if HASH_RE.search(u):
        return u, False
    # extraer el nombre de archivo
    m = re.search(r'/images/(.+)$', u)
    if not m: return u, False
    resto = m.group(1)
    # el resto puede traer query de weserv
    resto = resto.split('&v=')[0]
    nombre = resto.strip()
    if '/' in nombre:  # ya tiene alguna estructura
        return u, False
    nombre = urllib.parse.unquote(nombre)
    nombre = nombre.replace(' ', '_')
    h = hashlib.md5(nombre.encode('utf-8')).hexdigest()
    ruta = f"{h[0]}/{h[0:2]}/{urllib.parse.quote(nombre)}"
    nuevo = re.sub(r'(static\.wikia\.nocookie\.net/hotwheels/images/)[^&]*',
                   r'\g<1>' + ruta, u)
    return nuevo, nuevo != u

def main():
    cat = json.load(open(BASE + 'catalog_web.json', encoding='utf-8'))
    fix_im = fix_gal = 0

    for m in cat:
        if m.get('im'):
            n, cambiado = reparar(m['im'])
            if cambiado:
                m['im'] = n; fix_im += 1
        gal = m.get('galeria')
        if gal:
            ng = []
            cambio = False
            for u in gal:
                n, c = reparar(u)
                if c: cambio = True
                ng.append(n)
            if cambio:
                m['galeria'] = ng; fix_gal += 1

    print(f"im reparadas: {fix_im}")
    print(f"galerias reparadas: {fix_gal}")

    # verificar
    mal = 0
    for m in cat:
        urls = []
        if m.get('im'): urls.append(m['im'])
        urls.extend(m.get('galeria') or [])
        for u in urls:
            if 'weserv' in u and not HASH_RE.search(u):
                mal += 1
    print(f"URLs malformadas restantes: {mal}")

    json.dump(cat, open(BASE + 'catalog_web.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
    txt = json.dumps(cat, ensure_ascii=False, separators=(',',':'))
    open('C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/cat.js','w',encoding='utf-8').write('const CAT=' + txt + ';\n')
    print(f"cat.js regenerado ({len(txt)/1024/1024:.1f} MB)")

if __name__ == '__main__':
    main()
