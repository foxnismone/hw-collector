#!/usr/bin/env python3
"""Separa el CAT (y los demás arrays grandes) del HTML a archivos JS externos.
Reduce el HTML base y permite caché/compression independientes.
"""
import json, re, os

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/'
DATA = BASE + 'data/'

def find_end(s, oi):
    d=0; ins=False; esc=False
    for j in range(oi, len(s)):
        ch=s[j]
        if ins:
            if esc: esc=False
            elif ch=='\\': esc=True
            elif ch=='"': ins=False
            continue
        if ch=='"': ins=True
        elif ch in '[{': d+=1
        elif ch in ']}':
            d-=1
            if d==0: return j+1
    return -1

def extraer_array(html, nombre):
    i = html.find(nombre)
    if i < 0: return None, None, None, None
    eq = html.find('=', i)
    pb = html.find('[', eq)
    pl = html.find('{', eq)
    if pb == -1: pb = len(html)
    if pl == -1: pl = len(html)
    op = min(pb, pl)
    ei = find_end(html, op)
    return i, ei, op, html[op:ei]

def main():
    html = open(BASE + 'index.html', encoding='utf-8').read()
    print(f"HTML original: {len(html):,} chars")

    os.makedirs(DATA, exist_ok=True)
    reemplazos = []

    for nombre, archivo in [('const CAT=', 'data/cat.js'),
                             ('DISENADORES=', 'data/disenadores.js'),
                             ('const WHEELTYPES=', 'data/ruedas.js'),
                             ('const SERIES=', 'data/series.js')]:
        i, ei, oi, datos = extraer_array(html, nombre)
        if i is None:
            print(f"  {nombre}: no encontrado")
            continue
        # escribir archivo externo
        ruta = BASE + archivo
        open(ruta, 'w', encoding='utf-8').write(nombre + datos + ';\n')
        # reemplazar en el HTML TODO el bloque (desde el nombre hasta el final del array)
        resto = html[ei:]
        # si lo que sigue es ", OTRA=" (declaración concatenada), pasar a ";const OTRA="
        if resto.lstrip().startswith(','):
            resto = resto.lstrip()
            resto = ';const ' + resto[1:].lstrip()
        html = html[:i] + resto
        # insertar el script justo antes del script principal
        reemplazos.append((nombre, archivo, len(datos)))

    print(f"\nArrays extraídos:")
    for n, a, t in reemplazos:
        print(f"  {n} -> {a} ({t:,} chars)")

    # limpiar separadores sobrantes: al extraer un array quedan ", ;" (coma + punto y coma original)
    html = re.sub(r'\s*,\s*;\s*', ';', html)
    # insertar los <script src> antes del último </body> o antes del primer <script>
    tags = ''.join(f'<script src="{a}"></script>\n' for _, a, _ in reemplazos)
    # insertar después de <head> o al inicio
    if '</head>' in html:
        html = html.replace('</head>', tags + '</head>', 1)
    else:
        html = tags + html
    print(f"\nHTML resultante: {len(html):,} chars ({len(html)/1024/1024:.1f} MB)")
    open(BASE + 'index.html', 'w', encoding='utf-8').write(html)
    print(f"Tags insertados:\n{tags}")

if __name__ == '__main__':
    main()
