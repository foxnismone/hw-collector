#!/usr/bin/env python3
"""Quita el placeholder 'Image_Not_Available.jpg' de galerias e 'im',
y resuelve la foto real consultando la pagina del casting en Fandom."""
import json, urllib.request, urllib.parse, re, time, os

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'
PLACEHOLDER = 'image_not_available'

def api(params, intentos=3):
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (hotwheels-research)')
    req.add_header('Referer','https://hotwheels.fandom.com/')
    for i in range(intentos):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception:
            time.sleep(1.2*(i+1))
    return None

def casting_base(nombre):
    n = re.sub(r"\s*\(\d+(st|nd|rd|th) color[^)]*\)", '', nombre, flags=re.I)
    n = re.sub(r"\s*\(color variant[^)]*\)", '', n, flags=re.I)
    n = re.sub(r"\s*\(treasure hunt\)", '', n, flags=re.I)
    return n.strip()

def buscar_foto_real(nombre):
    """Busca la imagen principal de la pagina del casting."""
    for cand in (nombre, casting_base(nombre)):
        if not cand: continue
        d = api({'action':'parse','page':cand,'prop':'images','format':'json'})
        if not d or 'parse' not in d: continue
        imgs = d['parse'].get('images', [])
        for im in imgs:
            if im.lower().endswith(('.jpg','.jpeg','.png','.webp','.gif')):
                if 'not_available' in im.lower(): continue
                if im.lower().startswith(('site-','icon-','avatar')): continue
                return im
    return ''

def main():
    cat = json.load(open(BASE + 'catalog_web.json', encoding='utf-8'))

    # 1. limpiar galerias del placeholder
    limpias = 0
    for m in cat:
        gal = m.get('galeria')
        if gal:
            ng = [u for u in gal if PLACEHOLDER not in str(u).lower()]
            if len(ng) != len(gal):
                if ng: m['galeria'] = ng
                else: m.pop('galeria', None)
                limpias += 1
    print(f"Galerias limpiadas: {limpias}")

    # 2. modelos cuyo 'im' es el placeholder
    pend = [m for m in cat if PLACEHOLDER in str(m.get('im','')).lower()]
    print(f"Modelos con im placeholder: {len(pend)}")

    # agrupar por casting base (para no repetir consultas)
    por_casting = {}
    for m in pend:
        b = casting_base(m['m'])
        por_casting.setdefault(b, []).append(m)
    print(f"Castings unicos a resolver: {len(por_casting)}")

    resueltos = 0
    fallos = []
    for i, (base, modelos) in enumerate(por_casting.items()):
        foto = buscar_foto_real(base)
        if foto:
            url = 'https://static.wikia.nocookie.net/hotwheels/images/' + foto.replace(' ','_') if not foto.startswith('http') else foto
            # normalizar: Special:FilePath no es imagen directa
            for m in modelos:
                m['im'] = 'https://images.weserv.nl/?url=' + re.sub(r'/revision/latest.*$','',url).replace('https://','')
                if not m.get('galeria'):
                    m['galeria'] = [m['im']]
            resueltos += len(modelos)
        else:
            for m in modelos:
                m.pop('im', None)
                if PLACEHOLDER in str((m.get('galeria') or [''])[0]).lower():
                    m.pop('galeria', None)
            fallos.append(base)
        if (i+1) % 25 == 0:
            print(f"  {i+1}/{len(por_casting)} ... resueltos={resueltos}")
            json.dump(cat, open(BASE + 'catalog_web.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
        time.sleep(0.25)

    print(f"\nResueltos: {resueltos}")
    print(f"Sin foto real (se dejan sin imagen): {len(fallos)}")
    if fallos[:10]: print(f"  {fallos[:10]}")

    # verificar
    quedar = sum(1 for m in cat if PLACEHOLDER in str(m.get('im','')).lower())
    print(f"im placeholder restantes: {quedar}")

    json.dump(cat, open(BASE + 'catalog_web.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
    txt = json.dumps(cat, ensure_ascii=False, separators=(',',':'))
    open('C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/cat.js','w',encoding='utf-8').write('const CAT=' + txt + ';\n')
    print(f"cat.js regenerado ({len(txt)/1024/1024:.1f} MB)")

if __name__ == '__main__':
    main()
