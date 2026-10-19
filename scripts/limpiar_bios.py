#!/usr/bin/env python3
"""Limpia los prefijos de URL de Fandom de las bios y repara las rotas."""
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

def limpiar_bio(bio):
    """Elimina prefijos de navegación y URLs de fandom."""
    # Quitar "Nombre | Wiki Hot Wheels | URL del fandom: https://...wiki/Nombre "
    bio = re.sub(r'^.*?URL (?:del fandom|de [A-Za-z]+):\s*https://hotwheels\.fandom\.com/wiki/\S+\s*', '', bio, flags=re.I)
    bio = re.sub(r'^\S+\s*\|\s*Wiki Hot Wheels\s*\|\s*', '', bio)
    # Quitar "Hot Wheels Wiki ..." inicial
    bio = re.sub(r'^Hot Wheels Wiki\s*', '', bio)
    # Quitar "Tenga en cuenta que el Wiki..." 
    bio = re.sub(r'^Tenga en cuenta que el Wiki de Hot Wheels.*?prohibido\.\s*', '', bio)
    # Quitar "Menu Explore..." 
    bio = re.sub(r'^Menu Explore More History.*?Skip to content.*?\.?\s*', '', bio)
    return bio.strip()

def main():
    with open(BASE + 'disenadores.json', encoding='utf-8') as f:
        dis = json.load(f)

    limpiadas = 0
    for nombre, d in dis.items():
        bio = d.get('bio_es', '')
        nuevo = limpiar_bio(bio)
        if nuevo != bio:
            dis[nombre]['bio_es'] = nuevo
            dis[nombre]['biografia_limpia'] = nuevo
            limpiadas += 1

    # Re-extraer Guillermo González y Tony Martino
    for nombre in ['Guillermo González', 'Tony Martino']:
        bio_en = extraer_bio(nombre.replace(' ', '_'))
        if bio_en and len(bio_en) > 60:
            es = traducir(bio_en, 'es')
            dis[nombre]['biografia_limpia'] = es
            dis[nombre]['bio_es'] = es
            dis[nombre]['bio_en'] = bio_en
            dis[nombre]['bio_pt'] = traducir(bio_en, 'pt')
            dis[nombre]['bio_fr'] = traducir(bio_en, 'fr')
            print(f"{nombre}: re-extraida")

    with open(BASE + 'disenadores.json', 'w', encoding='utf-8') as f:
        json.dump(dis, f, ensure_ascii=False, indent=2)
    print(f"\nBios limpiadas: {limpiadas}")

    # Verificación
    JUNK = ['Skip to content', 'Advertisement', 'URL del fandom', 'URL de ', 'Sign In', 'Year Casting Name', 'Hot Wheels Wiki', 'Menu Explore']
    rotas = [n for n, d in dis.items() if any(j in d.get('bio_es','') for j in JUNK)]
    PAL_ES = [' diseñador', ' trabajó', ' fue ', ' durante', ' también', ' desde ', ' equipo', 'conocido', 'mattel', 'creó', 'diseñó']
    bio_es = sum(1 for d in dis.values() if sum(1 for p in PAL_ES if p in d.get('bio_es','').lower()) >= 2)
    print(f"Con basura: {len(rotas)}")
    print(f"En español: {bio_es}/{len(dis)}")
    foto_real = sum(1 for d in dis.values() if d.get('foto') and '/0/0c/' not in d.get('foto','') and 'weserv' in d.get('foto',''))
    print(f"Fotos reales: {foto_real}/{len(dis)}")

if __name__ == '__main__':
    main()
