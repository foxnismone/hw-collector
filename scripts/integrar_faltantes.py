#!/usr/bin/env python3
"""Integra los modelos faltantes del árbol cronológico al catálogo.
Las imágenes se sirven vía proxy weserv (URL construida con el hash MD5 de MediaWiki).
"""
import json, hashlib, urllib.parse, re

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/'
DATA = BASE + 'data/'

def url_fandom(nombre):
    """Construye la URL de static.wikia.nocookie.net para un archivo de Fandom."""
    if not nombre: return ''
    n = nombre.strip().replace(' ', '_')
    # quitar prefijo revision si vino
    n = re.sub(r'/revision/latest.*$', '', n)
    h = hashlib.md5(n.encode('utf-8')).hexdigest()
    return f"https://static.wikia.nocookie.net/hotwheels/images/{h[0]}/{h[0:2]}/{urllib.parse.quote(n)}"

def categoria_de(serie, anio):
    s = (serie or '').lower()
    if not serie:
        return 'Mainline'
    if any(k in s for k in ('treasure hunt','super treasure')):
        return 'Treasure Hunt'
    if 'first edition' in s: return 'First Editions'
    if 'car culture' in s: return 'Car Culture'
    if 'boulevard' in s: return 'Boulevard'
    if 'pop culture' in s: return 'Pop Culture'
    if 'team transport' in s: return 'Team Transport'
    if 'premium' in s: return 'Premium'
    if anio and int(anio) <= 1978:
        return 'Vintage'
    return 'Mainline'

def main():
    cat = json.load(open(DATA + 'catalog_web.json', encoding='utf-8'))
    faltan = json.load(open(DATA + 'faltantes.json', encoding='utf-8'))
    existentes = {m['i'] for m in cat}

    nuevas = []
    sin_foto = 0
    for f in faltan:
        toy = f.get('toy','')
        anio = f['anio']
        pid = f"{anio}-{toy}" if toy else f"{anio}-{hashlib.md5((f.get('modelo','')).encode()).hexdigest()[:6]}"
        if pid in existentes: continue
        modelo = f.get('modelo','')
        serie = f.get('serie','')
        foto = f.get('foto','')
        im = url_fandom(foto) if foto else ''
        if not im: sin_foto += 1

        cat_k = categoria_de(serie, anio)
        ficha = {
            'descripcion': f"{modelo} de {anio}" + (f". Serie: {serie}." if serie else "."),
            'historia': f"El {modelo} fue lanzado en {anio}" + (f" como parte de la serie {serie}." if serie else "."),
            'curiosidades': (f"Toy # {toy}. " if toy else "") + (f"Serie {serie}." if serie else ""),
            'conmemorativo': False,
            'dato_clave': toy or modelo,
            'es': {'descripcion': f"{modelo} de {anio}" + (f". Serie: {serie}." if serie else "."),
                   'historia': f"El {modelo} fue lanzado en {anio}" + (f" como parte de la serie {serie}." if serie else "."),
                   'curiosidades': (f"Toy # {toy}. " if toy else "") + (f"Serie {serie}." if serie else ""),
                   'dato_clave': toy or modelo}
        }

        entrada = {
            'i': pid, 'm': modelo, 'y': anio, 't': toy,
            'c': f.get('col',''), 's': serie, 'n': f.get('serie_num',''),
            'k': cat_k, 'x': 9.99,
            'im': im, 'v': 9.99, 'V': 19.99, 'px': 12,
            'f': [9.99, 9.99, 12.0, 0.0, 15.0],
            'dm': 0, 'ap': 4,
            'ficha': ficha,
            'indice_coleccionabilidad': 35.0,
        }
        if foto:
            entrada['galeria'] = [im]
        nuevas.append(entrada)
        existentes.add(pid)

    print(f"Nuevas entradas: {len(nuevas)}")
    print(f"Sin foto: {sin_foto}")
    cat.extend(nuevas)
    json.dump(cat, open(DATA + 'catalog_web.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
    print(f"Catálogo total: {len(cat)}")

    # Reconstruir HTML
    def find_end(s, oi):
        depth=0; in_str=False; esc=False
        for j in range(oi, len(s)):
            ch=s[j]
            if in_str:
                if esc: esc=False
                elif ch=='\\': esc=True
                elif ch=='"': in_str=False
                continue
            if ch=='"': in_str=True
            elif ch in '[{': depth+=1
            elif ch in ']}':
                depth-=1
                if depth==0: return j+1
        return -1

    html = open(BASE + 'index.html', encoding='utf-8').read()
    i = html.find('const CAT=['); oi = html.find('[', i); ei = find_end(html, oi)
    html = html[:oi] + json.dumps(cat, ensure_ascii=False, separators=(',',':')) + html[ei:]
    open(BASE + 'index.html', 'w', encoding='utf-8').write(html)
    print(f"HTML: {len(html):,} chars ({len(html)/1024/1024:.1f} MB)")

if __name__ == '__main__':
    main()
