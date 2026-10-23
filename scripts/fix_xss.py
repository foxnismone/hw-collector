#!/usr/bin/env python3
"""Refactor de SEGURIDAD (XSS) del index.html de HW Collector.
Escapa cada interpolacion segun su contexto: texto, string JS, atributo/URL.
"""
import re, sys

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/'
RUTA = BASE + 'index.html'

html = open(RUTA, encoding='utf-8').read()
original = html
cambios = 0

# ---------- 1. Helpers de escape (junto a esc) ----------
HELPERS = """function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}
/* --- Escape por contexto (defensa en profundidad XSS) --- */
const escT=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const escA=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
const escJ=s=>String(s??'').replace(/\\\\/g,'\\\\\\\\').replace(/'/g,"\\\\'").replace(/"/g,'\\\\"').replace(/\\n/g,'\\\\n').replace(/\\r/g,'');
const escU=s=>String(s??'').replace(/[^a-zA-Z0-9._~:/?#\\[\\]@!$&'()*+,;=%-]/g,'');
const safeAttr=(v)=>escA(v);"""

if 'escT=' not in html:
    html = html.replace("function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\"/g,'&quot;').replace(/'/g,'&#39;');}", HELPERS, 1)
    print("✓ Helpers de escape anadidos")

# ---------- 2. Campos de TEXTO (envolver en escT) ----------
CAMPOS_TEXTO = [
    'c.m','c.s','c.t','c.c','c.n','c.k','c.pais','c.y',
    'fSel.descripcion','fSel.historia','fSel.curiosidades','fSel.dato_clave',
    'vm.fuente','vm.fecha','c.diseñador','c.categoria_descripcion',
    'd.nombre','d.nacionalidad','d.periodo','d.biografia_limpia','d.biografia',
    'w.s','w.col','w.c','w.n','w.nombre','w.n_es',
    'r.canal','r.tipo','b.canal','match.m','encontrado.m','disenador.nacionalidad',
    'o.u','o.subcoleccion','codigo','txt','query','q',
]
for campo in CAMPOS_TEXTO:
    # ${campo} simple -> ${escT(campo)}
    patron = r'\$\{' + re.escape(campo) + r'\}'
    nuevo = '${escT(' + campo + ')}'
    if patron != nuevo:
        html, n = re.subn(patron, nuevo, html)
        if n: cambios += n

# casos compuestos frecuentes
COMPUESTOS = [
    (r'\$\{c\.n\?\("\(\+" \+ c\.n \+ "\)"\):""\}', '${c.n?"("+escT(c.n)+")":""}'),
    (r'\$\{c\.n\?"\("\+\$\{c\.n\}\}\+\)"\:""\}', '${c.n?"("+escT(c.n)+")":""}'),
    (r'\$\{c\.m\.replace\(\/\'\/g,""\)\}', '${escJ(c.m)}'),
    (r'\$\{_hist\(c\.m\)\?\.historia\}', '${escT(_hist(c.m)?.historia)}'),
    (r'\$\{_hist\(c\.m\)\?\.dato_clave\}', '${escT(_hist(c.m)?.dato_clave)}'),
    (r'\$\{_hist\(c\.m\)\?\.curiosidades\}', '${escT(_hist(c.m)?.curiosidades)}'),
    (r'\$\{String\(c\.k\|\|""\)\.toUpperCase\(\)\}', '${String(c.k||"").toUpperCase()}'),
]
for patron, nuevo in COMPUESTOS:
    html, n = re.subn(patron, nuevo, html)
    if n: cambios += n

print(f"✓ Escape de texto aplicado ({cambios} cambios)")

# ---------- 3. Strings JS en onclick (escJ) ----------
# onclick="fn('${X}')"
patron_onclick = re.compile(r"(onclick=\"[a-zA-Z_]+\(\s*(?:event,\s*)?')(\$\{[^}]+\})(')")
def repl_onclick(m):
    return m.group(1) + '${escJ(' + m.group(2)[2:-1] + ')}' + m.group(3)
html, n = patron_onclick.subn(repl_onclick, html)
print(f"✓ onclick con id escapado: {n}")

# setCond('${id}'), setLoc('${id}'), etc.
for fn in ['setCond','setLoc','speak','bump','editQty','saveEdit','delCar','addById','editCar','flipCar','verFicha','agregarManual','onboardAgregar','agregarEscaneado','agregarFoto']:
    patron = re.compile(r"(onclick=\"[a-zA-Z_]+\(\s*(?:event,\s*)?')(\$\{[^}]+\})(')")
    html, n2 = patron.subn(repl_onclick, html)
    if n2: cambios += n2

print(f"✓ Total cambios: {cambios}")

open(RUTA, 'w', encoding='utf-8').write(html)
print(f"Guardado. {len(original):,} -> {len(html):,} chars")
