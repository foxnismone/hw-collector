#!/usr/bin/env python3
"""Genera las entradas de Car Culture 2-Packs y las añade al catálogo."""
import json, os, glob

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/'
DATA = BASE + 'data/'

def main():
    packs = json.load(open(DATA + 'packs_culture.json', encoding='utf-8'))
    cat = json.load(open(DATA + 'catalog_web.json', encoding='utf-8'))
    existentes = {m['i'] for m in cat}

    nuevas = []
    for p in packs:
        archivo = p.get('foto_pack','')
        if not archivo: continue
        fn = archivo.replace('/','_').replace(' ','_')
        # normalizar a .jpg si era webp
        if not os.path.exists(BASE + 'img/packs_culture/' + fn):
            fn = fn.rsplit('.',1)[0] + '.jpg'
        if not os.path.exists(BASE + 'img/packs_culture/' + fn): continue

        toy = p['toy']
        pid = f"{p['anio']}-{toy}"
        if pid in existentes: continue

        cast1 = p['castings'][0] if len(p['castings']) > 0 else ''
        cast2 = p['castings'][1] if len(p['castings']) > 1 else ''

        ficha_es = (f"Pack premium de 2 autos de la línea Car Culture ({p['anio']}), "
                    f"tema «{p['theme']}». Contiene: {cast1}" +
                    (f" y {cast2}." if cast2 else "."))
        ficha = {
            'descripcion': ficha_es,
            'historia': f"Car Culture es la línea premium de Hot Wheels presentada en 2021; "
                        f"cada pack reúne dos modelos con tema común y acabado premium (carrocería "
                        f"esculpida, ruedas Real Riders y base metálica). Este pack, número {toy}, "
                        f"pertenece a {p['anio']} Mix {p['mix']} con el tema «{p['theme']}».",
            'curiosidades': f"Toy # {toy} · Serie Car Culture {p['anio']} · Mix {p['mix']}. "
                            f"Contiene 2 castings premium fabricados en Tailandia.",
            'conmemorativo': True,
            'dato_clave': f"{toy} · {p['theme']}",
            'es': {'descripcion': ficha_es,
                   'historia': f"Car Culture es la línea premium de Hot Wheels presentada en 2021; "
                               f"cada pack reúne dos modelos con tema común y acabado premium.",
                   'curiosidades': f"Toy # {toy} · Serie Car Culture {p['anio']} · Mix {p['mix']}.",
                   'dato_clave': f"{toy} · {p['theme']}"},
            'pt': {'descripcion': ficha_es.replace('línea', 'linha').replace('tema', 'tema'),
                   'historia': "Car Culture é a linha premium da Hot Wheels apresentada em 2021; "
                               "cada pack reúne dois modelos com tema comum e acabamento premium.",
                   'curiosidades': f"Toy # {toy} · Série Car Culture {p['anio']} · Mix {p['mix']}.",
                   'dato_clave': f"{toy} · {p['theme']}"},
            'fr': {'descripcion': ficha_es,
                   'historia': "Car Culture est la gamme premium de Hot Wheels lancée en 2021 ; "
                               "chaque pack réunit deux modèles à thème commun.",
                   'curiosidades': f"Toy # {toy} · Série Car Culture {p['anio']} · Mix {p['mix']}.",
                   'dato_clave': f"{toy} · {p['theme']}"}
        }

        entrada = {
            'i': pid,
            'm': f"Car Culture 2-Pack — {p['theme']}",
            'y': p['anio'],
            't': toy,
            'c': f"{toy}",
            's': 'Car Culture',
            'n': f"{p['mix']}/10",
            'k': 'Car Culture',
            'x': 24.99,
            'im': f"packs_culture/{fn}",
            'v': 24.99, 'V': 39.99, 'px': 12,
            'f': [25.0, 25.0, 30.0, 0.0, 40.0],
            'dm': 0, 'ap': 4,
            'ficha': ficha,
            'indice_coleccionabilidad': 62.0,
            'pais': 'Thailand',
            'categorias_fandom': ['Car Culture', '2-Packs'],
            'galeria': [f"https://images.weserv.nl/?url=static.wikia.nocookie.net/hotwheels/images/{archivo.split('/')[0]}/{archivo.split('/')[1] if '/' in archivo else ''}"] if '/' in archivo else []
        }
        nuevas.append(entrada)
        existentes.add(pid)

    print(f"Nuevas entradas de packs: {len(nuevas)}")
    cat.extend(nuevas)
    json.dump(cat, open(DATA + 'catalog_web.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
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
    print(f"HTML reconstruido: {len(html):,} chars")

if __name__ == '__main__':
    main()
