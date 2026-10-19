#!/usr/bin/env python3
"""Repara las últimas bios rotas y la en inglés."""
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
    data = api({'action':'query','prop':'revisions','titles':titulo,'rvslots':'*','rvprop':'content','format':'json','formatversion':'2'})
    if not data: return None
    pages = data.get('query',{}).get('pages',[])
    if not pages: return None
    content = ''
    for p in pages:
        revs = p.get('revisions',[])
        if revs: content = revs[0].get('slots',{}).get('main',{}).get('content','')
    if not content: return None
    text = re.sub(r'\{\{[^{}]*\}\}',' ',content)
    text = re.sub(r'\{\|.*?\|\}',' ',text,flags=re.DOTALL)
    text = re.sub(r'^=+.*?=+\s*$',' ',text,flags=re.MULTILINE)
    text = re.sub(r'\[\[File:[^\]]*\]\]',' ',text)
    text = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]',r'\1',text)
    text = re.sub(r'\[\[([^\]]*)\]\]',r'\1',text)
    text = re.sub(r'<[^>]+>',' ',text)
    text = re.sub(r'^[\*#:;]+.*$',' ',text,flags=re.MULTILINE)
    text = text.replace('&ndash;','-').replace('&nbsp;',' ').replace('&amp;','&')
    text = re.sub(r'\s{2,}',' ',text).strip()
    for parrafo in text.split('. '):
        if len(parrafo) > 60:
            return parrafo.strip() + '.'
    return text[:400] if len(text) > 50 else None

def main():
    with open(BASE + 'disenadores.json', encoding='utf-8') as f:
        dis = json.load(f)

    # Re-extraer las 3 rotas
    for nombre in ['Manson Cheung', 'Phil Riehlman', 'Steve Gilmore']:
        bio_en = extraer_bio(nombre.replace(' ', '_'))
        if bio_en and len(bio_en) > 60:
            es = traducir(bio_en, 'es')
            dis[nombre]['biografia_limpia'] = es
            dis[nombre]['bio_es'] = es
            dis[nombre]['bio_en'] = bio_en
            dis[nombre]['bio_pt'] = traducir(bio_en, 'pt')
            dis[nombre]['bio_fr'] = traducir(bio_en, 'fr')
            print(f"{nombre}: OK ({len(es)})")
        else:
            print(f"{nombre}: sin bio")
        time.sleep(0.3)

    # Traducir Guest Designers (está en inglés)
    if 'Guest Designers' in dis:
        bio_en = dis['Guest Designers'].get('bio_es', '')
        if any(p in bio_en.lower() for p in [' hot wheels ', ' celebrities ', ' approached ']):
            es = traducir(bio_en, 'es')
            dis['Guest Designers']['bio_es'] = es
            dis['Guest Designers']['bio_en'] = bio_en
            dis['Guest Designers']['bio_pt'] = traducir(bio_en, 'pt')
            dis['Guest Designers']['bio_fr'] = traducir(bio_en, 'fr')
            print(f"Guest Designers: traducido ({len(es)})")

    # Limpiar Tony Martino (tiene basura al inicio)
    if 'Tony Martino' in dis:
        bio = dis['Tony Martino'].get('bio_es', '')
        # Buscar el inicio real después de la basura
        idx = bio.find('Tenga en cuenta')
        if idx > 0:
            dis['Tony Martino']['bio_es'] = bio[idx:idx+500]
            print(f"Tony Martino: limpiado")

    with open(BASE + 'disenadores.json', 'w', encoding='utf-8') as f:
        json.dump(dis, f, ensure_ascii=False, indent=2)

    # Verificación final
    JUNK = ['Skip to content', 'Advertisement', 'URL: https://', 'Sign In', 'Year Casting Name', 'Hot Wheels Wiki']
    rotas = [n for n, d in dis.items() if any(j in d.get('bio_es','') for j in JUNK)]
    PAL_ES = [' diseñador', ' trabajó', ' fue ', ' durante', ' también', ' desde ', ' equipo', 'conocido', 'mattel', 'creó', 'diseñó']
    bio_es = sum(1 for d in dis.values() if sum(1 for p in PAL_ES if p in d.get('bio_es','').lower()) >= 2)
    print(f"\nBios rotas restantes: {len(rotas)}")
    print(f"Bios en español detectadas: {bio_es}/{len(dis)}")

if __name__ == '__main__':
    main()
