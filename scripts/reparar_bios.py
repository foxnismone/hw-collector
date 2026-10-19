#!/usr/bin/env python3
"""Re-extrae las biografías rotas de diseñadores desde Fandom (API parse)."""
import json, urllib.request, urllib.parse, re, time

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def api(params):
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (hotwheels-research)')
    req.add_header('Referer', 'https://hotwheels.fandom.com/')
    for intento in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception:
            time.sleep(1.5 * (intento + 1))
    return None

def traducir(texto, tl='es'):
    if not texto or len(texto.strip()) < 3:
        return texto
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=' + tl + '&dt=t&q=' + urllib.parse.quote(texto[:4500])
    for intento in range(3):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return ''.join(x[0] for x in data[0] if x[0])
        except Exception:
            time.sleep(1.5 * (intento + 1))
    return texto

def extraer_bio(titulo):
    """Extrae el texto biográfico de una página de diseñador."""
    # Obtener el wikitext
    data = api({
        'action': 'query', 'prop': 'revisions', 'titles': titulo,
        'rvslots': '*', 'rvprop': 'content', 'format': 'json', 'formatversion': '2'
    })
    if not data:
        return None
    pages = data.get('query', {}).get('pages', [])
    if not pages:
        return None
    content = ''
    for p in pages:
        revs = p.get('revisions', [])
        if revs:
            content = revs[0].get('slots', {}).get('main', {}).get('content', '')
    if not content:
        return None

    # Limpiar wikitext
    text = content
    # Quitar templates {{...}}
    text = re.sub(r'\{\{[^{}]*\}\}', ' ', text)
    # Quitar tablas {| ... |}
    text = re.sub(r'\{\|.*?\|\}', ' ', text, flags=re.DOTALL)
    # Quitar headings
    text = re.sub(r'^=+.*?=+\s*$', ' ', text, flags=re.MULTILINE)
    # Quitar File/Image
    text = re.sub(r'\[\[File:[^\]]*\]\]', ' ', text)
    text = re.sub(r'\[\[Image:[^\]]*\]\]', ' ', text)
    # Quitar wikilinks manteniendo texto
    text = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', text)
    text = re.sub(r'\[\[([^\]]*)\]\]', r'\1', text)
    # Quitar HTML
    text = re.sub(r'<[^>]+>', ' ', text)
    # Quitar listas
    text = re.sub(r'^[\*#:;]+.*$', ' ', text, flags=re.MULTILINE)
    # Entidades
    text = text.replace('&ndash;', '-').replace('&nbsp;', ' ').replace('&amp;', '&')
    # Colapsar espacios
    text = re.sub(r'\s{2,}', ' ', text).strip()
    # Tomar el primer párrafo sustancial
    for parrafo in text.split('. '):
        if len(parrafo) > 60:
            # Buscar el inicio real (después del nombre)
            return parrafo.strip() + '.'
    return text[:400] if len(text) > 50 else None

def main():
    with open(BASE + 'disenadores.json', encoding='utf-8') as f:
        dis = json.load(f)

    # Identificar bios rotas
    JUNK = ['Skip to content', 'Advertisement', 'URL: https://', 'Sign In', 'Casting Designers', 'Title | Year']
    rotas = [n for n, d in dis.items() if any(j in d.get('bio_es','') for j in JUNK)]
    print(f"Bios rotas: {len(rotas)}")

    arregladas = 0
    for nombre in rotas:
        titulo = nombre.replace(' ', '_')
        bio_en = extraer_bio(titulo)
        if bio_en and len(bio_en) > 60:
            es = traducir(bio_en, 'es')
            pt = traducir(bio_en, 'pt')
            fr = traducir(bio_en, 'fr')
            dis[nombre]['biografia_limpia'] = es
            dis[nombre]['bio_es'] = es
            dis[nombre]['bio_en'] = bio_en
            dis[nombre]['bio_pt'] = pt
            dis[nombre]['bio_fr'] = fr
            arregladas += 1
            print(f"  {nombre}: OK ({len(es)} chars)")
        else:
            print(f"  {nombre}: sin bio encontrada")
        time.sleep(0.3)
        if arregladas % 5 == 0:
            with open(BASE + 'disenadores.json', 'w', encoding='utf-8') as f:
                json.dump(dis, f, ensure_ascii=False, indent=2)

    with open(BASE + 'disenadores.json', 'w', encoding='utf-8') as f:
        json.dump(dis, f, ensure_ascii=False, indent=2)
    print(f"\nBios arregladas: {arregladas}/{len(rotas)}")

if __name__ == '__main__':
    main()
