#!/usr/bin/env python3
"""Extrae fichas reales de los modelos que faltan (lista faltan_extraer.json).
Acepta nombres con variantes de color: si no hay página propia, busca el base.
"""
import json, urllib.request, urllib.parse, re, time, os

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'
SALIDA = BASE + 'fichas_reales.json'

def api(params, intentos=3):
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (hotwheels-research)')
    req.add_header('Referer', 'https://hotwheels.fandom.com/')
    for i in range(intentos):
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception:
            time.sleep(1.5 * (i + 1))
    return None

def limpiar(t):
    if not t: return ''
    t = str(t)
    prev = None
    while prev != t:
        prev = t
        t = re.sub(r'\{\{[^{}]*\}\}', ' ', t)
    t = re.sub(r'\[\[(?:File|Image|Archivo):[^\]]*\]\]', ' ', t, flags=re.I)
    t = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[\[([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[https?://\S+\]', ' ', t)
    t = re.sub(r"'{2,}", '', t)
    t = re.sub(r'\[\[Category:[^\]]*\]\]', ' ', t, flags=re.I)
    t = re.sub(r'<ref[^>]*>.*?</ref>', ' ', t, flags=re.DOTALL | re.I)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = t.replace('&ndash;','-').replace('&mdash;','—').replace('&nbsp;',' ')
    t = t.replace('&amp;','&').replace('&quot;','"').replace('&#39;',"'")
    t = re.sub(r'\s{2,}', ' ', t)
    return t.strip()

def base_de(nombre):
    """Quita sufijos de variante de color para buscar la página base."""
    n = re.sub(r"\s*\(\d+(st|nd|rd|th) Color[^)]*\)\s*$", '', nombre, flags=re.I)
    n = re.sub(r"\s*\(Color Variant[^)]*\)\s*$", '', n, flags=re.I)
    n = re.sub(r"\s*\(Treasure Hunt\)\s*$", '', n, flags=re.I)
    return n.strip()

def extraer_ficha(nombre):
    for candidato in (nombre, base_de(nombre)):
        if not candidato: continue
        d = api({'action':'parse','page':candidato,'prop':'text|wikitext','format':'json'})
        if not d or 'parse' not in d: continue
        html = d['parse'].get('text',{}).get('*','')
        wt = d['parse'].get('wikitext',{}).get('*','')
        if not wt: continue

        ficha = {}
        # Galería
        imgs = []
        for m in re.finditer(r'<img[^>]*src="(https://static\.wikia[^"]*)"', html):
            u = re.sub(r'/revision/latest/.*$', '', m.group(1)).replace('https://','')
            if u not in imgs: imgs.append(u)
        if imgs: ficha['galeria'] = imgs[:8]

        # Descripción (intro antes de ==)
        corte = re.search(r'^==', wt, re.MULTILINE)
        intro = limpiar(wt[:corte.start()] if corte else wt)
        intro = re.sub(r'^\s*\[\[(?:Image|File):[^\]]*\]\]\s*', '', intro, flags=re.I)
        intro = re.sub(r'^[\'\'\'\s]+', '', intro)
        intro = limpiar(intro)
        if len(intro) > 60:
            ficha['descripcion'] = intro[:600]

        # Notas/curiosidades
        notas = re.search(r'==\s*(Notes|Curiosities|Notas|Trivia)\s*==(.*?)(?===|$)', wt, re.DOTALL | re.I)
        if notas:
            txt = limpiar(notas.group(2))
            if len(txt) > 40: ficha['curiosidades'] = txt[:400]

        # Diseñador
        for source in ('designer','disenador'):
            m = re.search(rf'data-source="{source}"[^>]*>.*?<div class="pi-data-value[^"]*">(.*?)</div>', html, re.DOTALL)
            if m:
                ficha['disenador'] = limpiar(m.group(1)); break

        if ficha.get('descripcion') or ficha.get('curiosidades') or ficha.get('galeria'):
            return ficha
    return None

def main():
    faltan = json.load(open(BASE + 'faltan_extraer.json', encoding='utf-8'))
    fichas = json.load(open(SALIDA, encoding='utf-8')) if os.path.exists(SALIDA) else {}
    print(f"Por procesar: {len(faltan)} | ya en salida: {len(fichas)}")

    pend = [n for n in faltan if n not in fichas]
    print(f"Pendientes: {len(pend)}")

    from concurrent.futures import ThreadPoolExecutor, as_completed
    ok = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(extraer_ficha, n): n for n in pend}
        for fut in as_completed(futs):
            n = futs[fut]
            try:
                f = fut.result()
                fichas[n] = f if f else {}
                ok += 1
            except Exception:
                fichas[n] = {}
                ok += 1
            if ok % 100 == 0:
                json.dump(fichas, open(SALIDA,'w',encoding='utf-8'), ensure_ascii=False)
                print(f"  {ok}/{len(pend)}")

    json.dump(fichas, open(SALIDA,'w',encoding='utf-8'), ensure_ascii=False)
    con_datos = sum(1 for f in fichas.values() if f)
    print(f"\nTotal: {len(fichas)} | con datos: {con_datos}")

if __name__ == '__main__':
    main()
