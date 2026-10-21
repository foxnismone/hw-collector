#!/usr/bin/env python3
"""Integra los datos de las páginas de CASTING al catálogo:
  - Enriquece fichas existentes con descripción real, curiosidades, diseñador
  - Añade versiones (cada una con todos sus metadatos) como entradas nuevas
  - Asigna la imagen real del casting
"""
import json, hashlib, urllib.parse, re, os

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/'
DATA = BASE + 'data/'

def norm(s):
    s = (s or '').lower()
    s = re.sub(r"\s*\(\d+(st|nd|rd|th) color[^)]*\)", '', s)
    s = re.sub(r"\s*\(treasure hunt\)", '', s)
    s = re.sub(r"\s*\(\d{4}\)", '', s)
    s = re.sub(r"[^a-z0-9]", '', s)
    return s

def url_fandom(nombre):
    if not nombre: return ''
    n = nombre.strip().replace(' ', '_')
    n = re.sub(r'/revision/latest.*$', '', n)
    h = hashlib.md5(n.encode('utf-8')).hexdigest()
    return f"https://static.wikia.nocookie.net/hotwheels/images/{h[0]}/{h[0:2]}/{urllib.parse.quote(n)}"

def main():
    cat = json.load(open(DATA + 'catalog_web.json', encoding='utf-8'))
    castings = json.load(open(DATA + 'castings.json', encoding='utf-8'))

    # Índice por nombre normalizado
    por_nom = {}
    for i, m in enumerate(cat):
        n = norm(m.get('m'))
        if n: por_nom.setdefault(n, []).append(i)

    enriquecidos = 0
    nuevas = 0
    ids = {str(m['i']) for m in cat}

    for titulo, c in castings.items():
        if not c or not c.get('versiones'): continue
        nombre = c.get('name') or titulo
        n = norm(nombre)
        idxs = por_nom.get(n, [])

        # Enriquecer existentes
        if idxs:
            for i in idxs:
                m = cat[i]
                f = m.get('ficha')
                if not isinstance(f, dict): continue
                cambiado = False
                if c.get('descripcion') and not f.get('es'):
                    f['descripcion'] = c['descripcion']
                    f['historia'] = c['descripcion']
                    f['es'] = {
                        'descripcion': c['descripcion'],
                        'historia': c['descripcion'],
                        'curiosidades': c.get('curiosidades',''),
                        'dato_clave': c.get('number','')
                    }
                    cambiado = True
                elif c.get('descripcion') and f.get('es'):
                    f['es']['descripcion'] = c['descripcion']
                    f['es']['historia'] = c['descripcion']
                    cambiado = True
                if c.get('curiosidades'):
                    if not f.get('curiosidades'): f['curiosidades'] = c['curiosidades']
                    if f.get('es') and not f['es'].get('curiosidades'): f['es']['curiosidades'] = c['curiosidades']
                    cambiado = True
                if c.get('designer') and not m.get('diseñador'):
                    m['diseñador'] = c['designer']; cambiado = True
                if cambiado: enriquecidos += 1
            continue

        # Nueva entrada por casting (primera versión)
        v = c['versiones'][0]
        toy = v.get('toy') or c.get('number','')
        anio = v.get('anio') or ''
        try: anio_i = int(re.search(r'\d{4}', str(anio)).group())
        except Exception: anio_i = 0
        pid = f"{anio_i}-{toy}" if toy else f"c-{hashlib.md5(titulo.encode()).hexdigest()[:8]}"
        if pid in ids: continue
        img = url_fandom(v.get('foto') or c.get('image',''))
        desc = c.get('descripcion','') or f"{nombre}"
        ficha = {
            'descripcion': desc,
            'historia': desc,
            'curiosidades': c.get('curiosidades',''),
            'conmemorativo': False,
            'dato_clave': toy,
            'es': {'descripcion': desc, 'historia': desc,
                   'curiosidades': c.get('curiosidades',''), 'dato_clave': toy}
        }
        entrada = {
            'i': pid, 'm': nombre, 'y': anio_i if anio_i else None,
            't': toy, 'c': v.get('col',''), 's': v.get('serie') or c.get('series',''),
            'n': v.get('serie_num',''), 'k': c.get('_categoria','Mainline'),
            'x': 12.99, 'im': img, 'v': 12.99, 'V': 24.99, 'px': 12,
            'f': [12.99, 12.99, 15.0, 0.0, 20.0], 'dm': 0, 'ap': 4,
            'ficha': ficha, 'indice_coleccionabilidad': 45.0,
            'pais': v.get('pais',''),
            'categorias_fandom': [c.get('_categoria','')],
        }
        if c.get('designer'): entrada['disenador'] = c['designer']
        if img: entrada['galeria'] = [img]
        cat.append(entrada); ids.add(pid); nuevas += 1

    print(f"Fichas enriquecidas: {enriquecidos}")
    print(f"Nuevas entradas: {nuevas}")
    print(f"Catálogo total: {len(cat)}")

    json.dump(cat, open(DATA + 'catalog_web.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))

    # Reconstruir HTML
    def find_end(s, oi):
        d=0; ins=False; esc=False
        for j in range(oi, len(s)):
            ch=s[j]
            if ins:
                if esc: esc=False
                elif ch=='\\': esc=True
                elif ch=='"': ins=False
                continue
            if ch=='"': ins=True
            elif ch in '[{': d+=1
            elif ch in ']}':
                d-=1
                if d==0: return j+1
        return -1
    html = open(BASE + 'index.html', encoding='utf-8').read()
    i = html.find('const CAT=['); oi = html.find('[', i); ei = find_end(html, oi)
    html = html[:oi] + json.dumps(cat, ensure_ascii=False, separators=(',',':')) + html[ei:]
    open(BASE + 'index.html', 'w', encoding='utf-8').write(html)
    print(f"HTML: {len(html):,} chars ({len(html)/1024/1024:.1f} MB)")

if __name__ == '__main__':
    main()
