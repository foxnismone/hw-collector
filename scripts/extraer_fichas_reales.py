#!/usr/bin/env python3
"""Extrae fichas REALES de cada modelo desde Fandom:
  - descripcion / historia / curiosidades / dato_clave
  - galeria: imágenes adicionales de la página
  - disenador (si está)
"""
import json, urllib.request, urllib.parse, re, time, sys

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

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
    t = re.sub(r'<ref[^>]*>.*?</ref>', ' ', t, flags=re.DOTALL|re.I)
    t = re.sub(r'<ref[^>]*/>', ' ', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[\[([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[https?://\S+\]', ' ', t)
    t = t.replace('&ndash;','-').replace('&mdash;','—').replace('&nbsp;',' ')
    t = t.replace('&amp;','&').replace('&quot;','"').replace('&#39;',"'")
    t = re.sub(r'\s{2,}', ' ', t)
    return t.strip()

def extraer_ficha(nombre):
    d = api({'action':'parse','page':nombre,'prop':'text|wikitext','format':'json'})
    if not d or 'parse' not in d:
        return None
    html = d['parse'].get('text',{}).get('*','')
    wt = d['parse'].get('wikitext',{}).get('*','')
    
    ficha = {}
    
    # Imágenes de la galería (todas las de la página)
    imgs = []
    for m in re.finditer(r'<img[^>]*src="(https://static\.wikia[^"]*)"', html):
        u = m.group(1)
        # Quitar el parámetro de escala para obtener la original
        u = re.sub(r'/revision/latest/.*$', '', u)
        u = u.replace('https://', '')
        if u not in imgs:
            imgs.append(u)
    ficha['galeria'] = imgs[:8]
    
    # Extraer primer párrafo de la descripción (antes de las secciones)
    # Cortar en la primera cabecera ==
    corte = re.search(r'^==', wt, re.MULTILINE)
    intro = wt[:corte.start()] if corte else wt
    intro = limpiar(intro)
    # Quitar plantillas
    intro = re.sub(r'\{\{[^{}]*\}\}', ' ', intro)
    intro = re.sub(r'\{\{[^{}]*\}\}', ' ', intro)
    intro = re.sub(r'^\s*\[\[(?:Image|File):[^\]]*\]\]\s*', '', intro, flags=re.I)
    intro = re.sub(r'^[\'\'\'\s]+', '', intro)
    intro = limpiar(intro)
    if len(intro) > 60:
        ficha['descripcion'] = intro[:600]
    
    # Curiosidades / datos: buscar secciones
    if '==Gallery==' in wt or '== Galería ==' in wt or 'Gallery' in wt:
        ficha['curiosidades'] = 'Tiene galería de fotos en la wiki.'
    
    # Diseñador
    for source in ('designer','disenador'):
        m = re.search(rf'data-source="{source}"[^>]*>.*?<div class="pi-data-value[^"]*">(.*?)</div>', html, re.DOTALL)
        if m:
            ficha['disenador'] = limpiar(m.group(1))
            break
    
    # Buscar curiosidades específicas en el wikitext (sección == Notes == o similar)
    notas = re.search(r'==\s*(Notes|Curiosities|Notas|Trivia)\s*==(.*?)(?===|$)', wt, re.DOTALL | re.I)
    if notas:
        txt = limpiar(notas.group(2))
        if len(txt) > 40:
            ficha['curiosidades'] = txt[:400]
    
    return ficha

def main():
    cat = json.load(open(BASE + 'catalog_web.json', encoding='utf-8'))
    # Modelos con ficha genérica (los nuevos)
    gen = [m for m in cat if str(m.get('ficha',{}).get('historia','')).startswith('El ') and len(str(m.get('ficha',{}).get('historia',''))) < 80]
    print(f"Modelos con ficha genérica: {len(gen)}")
    
    # Solo procesar los que tengan más de 1 campo faltante
    pend = [m for m in gen if not m.get('ficha_galeria')]
    print(f"Pendientes de enriquecer: {len(pend)}")
    
    salida = BASE + 'fichas_reales.json'
    fichas = {}
    if __import__('os').path.exists(salida):
        fichas = json.load(open(salida, encoding='utf-8'))
    
    ok = err = 0
    for i, m in enumerate(pend):
        nombre = m.get('m','').strip()
        if nombre in fichas:
            continue
        f = extraer_ficha(nombre)
        if f:
            fichas[nombre] = f
            ok += 1
        else:
            err += 1
        if (i+1) % 20 == 0:
            json.dump(fichas, open(salida,'w',encoding='utf-8'), ensure_ascii=False)
            print(f"  {i+1}/{len(pend)} ok={ok} err={err}")
        time.sleep(0.2)
    
    json.dump(fichas, open(salida,'w',encoding='utf-8'), ensure_ascii=False)
    print(f"\nFichas reales: {ok} | errores: {err} | total guardadas: {len(fichas)}")

if __name__ == '__main__':
    main()
