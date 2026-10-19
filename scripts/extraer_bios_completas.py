#!/usr/bin/env python3
"""Extrae biografías COMPLETAS de diseñadores desde Fandom: intro limpia + todos sus castings.

Reemplaza las bios cortas/desalineadas por:
  - bio_es / bio_en / bio_pt / bio_fr  (narrativa limpia, sin wikitext)
  - castings: [{anio, nombre, serie, edicion, toy}]  (lista COMPLETA)
  - n_castings
  - fuente: URL de la página de Fandom
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

def wikitext(titulo):
    d = api({'action': 'query', 'prop': 'revisions', 'titles': titulo,
             'rvslots': '*', 'rvprop': 'content', 'redirects': '1',
             'format': 'json', 'formatversion': '2'})
    if not d:
        return None
    pages = d.get('query', {}).get('pages', [])
    for p in pages:
        if 'missing' in p:
            return None
        revs = p.get('revisions', [])
        if revs:
            return revs[0].get('slots', {}).get('main', {}).get('content', '')
    return None

# ---------- limpieza ----------
NAV = re.compile(r'(Men[uú] Explorar|Skip to content|Saltar al contenido|Iniciar sesi[oó]n|Sign In|'
                 r'Publicidad|Advertisement|Don\'t have an account|Hot Wheels Wiki\s*\||'
                 r'URL (del fandom|de [A-Za-z]+):|Fandom\b|Register|Categor[ií]as?:)', re.I)

def limpiar(t):
    if not t:
        return ''
    t = re.sub(r'<ref[^>]*>.*?</ref>', ' ', t, flags=re.DOTALL | re.I)
    t = re.sub(r'<ref[^>]*/>', ' ', t)
    t = re.sub(r'\{\{[^{}]*\}\}', ' ', t)
    t = re.sub(r'\{\{[^{}]*\}\}', ' ', t)
    t = re.sub(r'\{\|.*?\|\}', ' ', t, flags=re.DOTALL)          # tablas
    t = re.sub(r'\[\[(?:File|Image|Archivo):[^\]]*\]\]', ' ', t, flags=re.I)
    t = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', t)           # [[x|y]] -> y
    t = re.sub(r'\[\[([^\]]*)\]\]', r'\1', t)                    # [[x]] -> x
    t = re.sub(r'\[https?://\S+\s+([^\]]*)\]', r'\1', t)         # [url texto] -> texto
    t = re.sub(r'\[https?://\S+\]', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r"'{2,}", '', t)                                  # ''' y ''
    t = t.replace('&ndash;', '–').replace('&mdash;', '—').replace('&nbsp;', ' ')
    t = t.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    t = re.sub(r'^\s*[*#:;].*$', ' ', t, flags=re.MULTILINE)     # listas wiki
    t = re.sub(r'\s{2,}', ' ', t)
    return t.strip()

def limpiar_nombre(t):
    """Limpia un nombre de casting/serie de una celda de tabla."""
    t = re.sub(r'\[\[(?:File|Image):[^\]]*\]\]', '', t, flags=re.I)
    t = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[\[([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r"'{2,}", '', t)
    t = t.replace('&ndash;', '–').replace('&nbsp;', ' ')
    t = re.sub(r'^\|+', '', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def extraer_intro(txt):
    """Intro: párrafos antes de la primera sección ==."""
    # quitar plantillas iniciales y cabeceras de imagen
    t = re.sub(r'^\s*\[\[(?:Image|File):[^\]]*\]\]\s*', '', txt, flags=re.I)
    t = re.sub(r'^\s*\{\{designer.*?\}\}\s*', '', t, flags=re.DOTALL | re.I)
    t = re.sub(r'^\s*\{\{[^{}]*\}\}\s*', '', t)
    # cortar en la primera sección
    corte = re.search(r'^\s*==', t, re.MULTILINE)
    if corte:
        t = t[:corte.start()]
    t = limpiar(t)
    # quedarnos con los primeros párrafos sustanciales
    parrafos = [p.strip() for p in re.split(r'(?<=[.!?])\s{2,}', t) if len(p.strip()) > 40]
    if not parrafos:
        parrafos = [p.strip() for p in t.split('\n') if len(p.strip()) > 40]
    intro = ' '.join(parrafos[:4]).strip()
    return intro

def extraer_castings(txt):
    """Parsea TODAS las tablas wikitable con Year/Casting/Series."""
    castings = []
    for tabla in re.findall(r'\{\|.*?\n\|\}', txt, re.DOTALL):
        # saltar cabecera (líneas que empiezan con ! )
        filas = re.split(r'\n\|-+', tabla)
        for fila in filas[1:]:
            celdas = []
            for ln in fila.split('\n'):
                ln = ln.strip()
                if not ln or ln.startswith('!') or ln.startswith('{|') or ln.startswith('|}'):
                    continue
                if ln.startswith('|'):
                    celdas.append(ln[1:])
                elif celdas:
                    celdas[-1] += ' ' + ln
            # separar celdas con || también
            expandido = []
            for c in celdas:
                expandido.extend(c.split('||'))
            vals = [limpiar_nombre(c) for c in expandido]
            vals = [v for v in vals if v != '' or True]
            if len(vals) < 3:
                continue
            anio = vals[0]
            if not re.match(r'^(19|20)\d{2}', anio):
                continue
            nombre = vals[1] if len(vals) > 1 else ''
            serie = vals[2] if len(vals) > 2 else ''
            edicion = vals[3] if len(vals) > 3 else ''
            toy = vals[4] if len(vals) > 4 else ''
            # limpiar "n/d" y basura
            for campo in (edicion, toy):
                pass
            if nombre and len(nombre) > 1 and nombre.lower() not in ('casting name', 'photo', 'name'):
                castings.append({
                    'anio': anio.strip(),
                    'nombre': nombre.strip(),
                    'serie': serie.strip(),
                    'edicion': edicion.strip(),
                    'toy': toy.strip(),
                })
    # dedupe conservando orden
    vistos = set(); out = []
    for c in castings:
        k = (c['anio'], c['nombre'], c['serie'])
        if k in vistos:
            continue
        vistos.add(k); out.append(c)
    return out

def extraer_datos(titulo):
    txt = wikitext(titulo)
    if not txt:
        return None
    intro_en = extraer_intro(txt)
    castings = extraer_castings(txt)
    # metadatos de la plantilla {{designer|...}}
    meta = {}
    m = re.search(r'\{\{designer(.*?)\}\}', txt, re.DOTALL | re.I)
    if m:
        for campo in ('name', 'years', 'title', 'image'):
            mm = re.search(campo + r'\s*=\s*([^\n|}]*)', m.group(1))
            if mm:
                meta[campo] = limpiar_nombre(mm.group(1))
    return {'intro_en': intro_en, 'castings': castings, 'meta': meta, 'raw_len': len(txt)}

if __name__ == '__main__':
    with open(BASE + 'disenadores.json', encoding='utf-8') as f:
        dis = json.load(f)

    nombres = list(dis.keys())
    solo = sys.argv[1] if len(sys.argv) > 1 else None
    if solo:
        nombres = [n for n in nombres if solo.lower() in n.lower()]

    ok = 0; sin_intro = 0; sin_cast = 0
    for i, nombre in enumerate(nombres):
        datos = extraer_datos(nombre)
        if not datos:
            print(f"  [{i+1}/{len(nombres)}] {nombre}: SIN PÁGINA")
            continue
        intro = datos['intro_en']
        castings = datos['castings']
        d = dis[nombre]
        d['bio_en_raw'] = intro
        d['castings'] = castings
        d['n_castings'] = len(castings)
        d['meta'] = datos['meta']
        d['fuente'] = 'https://hotwheels.fandom.com/wiki/' + urllib.parse.quote(nombre.replace(' ', '_'))
        if not intro:
            sin_intro += 1
        if not castings:
            sin_cast += 1
        ok += 1
        if (i + 1) % 10 == 0 or i == len(nombres) - 1:
            with open(BASE + 'disenadores.json', 'w', encoding='utf-8') as f:
                json.dump(dis, f, ensure_ascii=False, indent=2)
            print(f"  [{i+1}/{len(nombres)}] guardado (ok={ok} sin_intro={sin_intro} sin_castings={sin_cast})")
        time.sleep(0.25)

    with open(BASE + 'disenadores.json', 'w', encoding='utf-8') as f:
        json.dump(dis, f, ensure_ascii=False, indent=2)
    print(f"\nCOMPLETADO: {ok} extraídos | sin intro: {sin_intro} | sin castings: {sin_cast}")
