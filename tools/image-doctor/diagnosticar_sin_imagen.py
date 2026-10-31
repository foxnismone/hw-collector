#!/usr/bin/env python3
"""Diagnostico: de los modelos sin imagen, cuantos NO existen en la fuente
y cuantos si se pueden resolver. Responde 'por que no sale la imagen'."""
from __future__ import annotations
import json, os, sys, time, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imadoctor.config import Config
from imadoctor.scanner import scan_catalog_json, MISSING, OK, EMPTY, CORRUPT, BROKEN
from imadoctor.context import planificar, es_placeholder
from imadoctor.sources import buscar_multiples
from imadoctor.validate import validar, elegir_mejor
from imadoctor.visual import disponible as clip_ok, score_visual

cfg = Config()
cat_path = os.path.join(cfg.data, 'catalog_web.json')

# 1. los que no tienen imagen
sin_img = []
with open(cat_path, encoding='utf-8') as f:
    cat = json.load(f)
for i, m in enumerate(cat):
    v = m.get('im')
    if not v or (isinstance(v, str) and v.strip().lower() in ('none', '')):
        sin_img.append((i, m))

print(f"=== MODELOS SIN IMAGEN: {len(sin_img)} de {len(cat)} ===\n")

# 2. para una muestra, ver que dice Fandom
def fandom_pageimage(titulo):
    try:
        url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode({
            'action': 'query', 'format': 'json', 'redirects': 1,
            'titles': titulo, 'prop': 'pageimages', 'piprop': 'original|thumbnail',
            'pithumbsize': 400})
        req = urllib.request.Request(url)
        req.add_header('User-Agent', cfg.ua)
        req.add_header('Referer', 'https://hotwheels.fandom.com/')
        with urllib.request.urlopen(req, timeout=25) as r:
            d = json.loads(r.read().decode())
        for p in (d.get('query', {}).get('pages', {}) or {}).values():
            pi = p.get('pageimage')
            if not pi:
                # MediaWiki devuelve original/thumbnail a NIVEL DE PAGINA (sin la
                # clave 'pageimage') cuando la imagen es el placeholder generico.
                orig = p.get('original') or {}
                src = str(orig.get('source') or '')
                if 'not_available' in src.lower() or 'no_image' in src.lower():
                    return None, 'Image_Not_Available'
                if src:
                    return {'source': src, 'width': orig.get('width', 0),
                            'height': orig.get('height', 0)}, 'ok'
                return None, 'sin pageimage'
            if 'not_available' in str(pi).lower() or 'no_image' in str(pi).lower():
                return None, 'Image_Not_Available'
            return pi, 'ok'
    except Exception as e:
        return None, f'error {str(e)[:40]}'
    return None, '?'

MUESTRA = 40
print(f"--- muestra de {MUESTRA} (que dice Fandom) ---")
con_foto = 0
sin_foto = 0
no_existe = 0
for i, m in sin_img[:MUESTRA]:
    titulo = str(m.get('m') or '')
    pi, estado = fandom_pageimage(titulo)
    marca = {'ok': 'FOTO REAL', 'Image_Not_Available': 'NO EXISTE (placeholder)',
             'sin pageimage': 'sin pagina'}.get(estado, estado)
    if estado == 'ok':
        con_foto += 1
    elif estado == 'Image_Not_Available':
        sin_foto += 1
    else:
        no_existe += 1
    print(f"  {titulo[:42]:<44} {marca}")
    time.sleep(0.35)

print(f"\n  => con foto real: {con_foto} | NO existe en Fandom: {sin_foto} | sin pagina: {no_existe}")

# 3. intentar resolver con el buscador
print(f"\n--- intentando resolver {min(25, len(sin_img))} con image-doctor ---")
usos = clip_ok()
resueltos = 0
for i, m in sin_img[:25]:
    from imadoctor.scanner import ImageRef
    ref = ImageRef(source_file=cat_path, field_name=f'im[{i}]',
                   raw_value='', model_name=str(m.get('m') or ''),
                   serie=str(m.get('s') or ''), status=MISSING)
    # metadata
    from imadoctor import metadata as md
    meta = md.metadata_de(m)
    ref.marca, ref.modelo, ref.anio = meta.marca, meta.modelo, meta.anio
    ref.version, ref.color, ref.serie = meta.version, meta.color, meta.serie
    plan = planificar(ref)
    if not plan.queries:
        print(f"  {ref.model_name[:34]:<36} sin pistas")
        continue
    cands = buscar_multiples(plan.queries, cfg)
    if not cands:
        print(f"  {ref.model_name[:34]:<36} sin candidatos")
        continue
    mejor = elegir_mejor(cands[:6], cfg, consulta_visual=plan.queries[0],
                         score_fn=score_visual if usos else None)
    if mejor:
        resueltos += 1
        print(f"  {ref.model_name[:34]:<36} OK {mejor.width}x{mejor.height} score={mejor.score:.3f}")
    else:
        print(f"  {ref.model_name[:34]:<36} candidatos descartados")

print(f"\n  => resueltos: {resueltos}/25")
