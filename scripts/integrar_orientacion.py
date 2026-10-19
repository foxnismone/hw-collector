#!/usr/bin/env python3
"""Integra data/orientacion.json en index.html como el array ORIENT.

Uso:  python scripts/integrar_orientacion.py
"""
import json, os, re, sys

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/'
ORI = BASE + 'data/orientacion.json'
HTML = BASE + 'index.html'

def main():
    if not os.path.exists(ORI):
        print("Falta data/orientacion.json"); return 1
    o = json.load(open(ORI, encoding='utf-8'))
    izq = sum(1 for v in o.values() if v.get('dir') == 'IZQ')
    der = sum(1 for v in o.values() if v.get('dir') == 'DER')
    print(f"Orientaciones: {len(o)} | IZQ={izq} DER={der} sin_dato={len(o)-izq-der}")

    # Solo guardar lo necesario: dir + conf (redondear conf a 2 decimales)
    compacto = {k: {'d': v['dir'], 'c': round(float(v.get('conf', 0)), 2)}
                for k, v in o.items() if v.get('dir')}

    html = open(HTML, encoding='utf-8').read()

    # El código lee ORIENT[id].dir y ORIENT[id].conf -> mapear d->dir, c->conf
    # Para no duplicar claves largas, guardamos {d,c} y adaptamos la función FLIP.
    nueva = 'const ORIENT=' + json.dumps(compacto, ensure_ascii=False, separators=(',', ':')) + ';'

    if 'const ORIENT=' in html:
        i = html.find('const ORIENT=')
        j = html.find('\n', i)
        html = html[:i] + nueva + html[j:]
    else:
        # insertar antes de la definición de ORI
        anchor = '/* Orientación: aplica efecto espejo'
        i = html.find(anchor)
        if i < 0:
            print("No se encontró el ancla de ORI"); return 1
        html = html[:i] + nueva + '\n' + html[i:]

    # FLIP debe leer las claves cortas
    viejo_flip = "const FLIP=c=>{ const o=c&&ORI[c.i]; if(!o||!o.dir||(o.conf||0)<0.55) return false; return o.dir!==state.dir; };"
    nuevo_flip = "const FLIP=c=>{ const o=c&&ORIENT[c.i]; if(!o||!o.d||(o.c||0)<0.55) return false; return o.d!==state.dir; };"
    if viejo_flip in html:
        html = html.replace(viejo_flip, nuevo_flip)
    else:
        # ya adaptado
        html = re.sub(r"const FLIP=c=>\{[^}]*\};", nuevo_flip, html, count=1)

    open(HTML, 'w', encoding='utf-8').write(html)
    print(f"ORIENT integrado: {len(compacto)} entradas")
    print(f"  FLIP usa ORIENT: {'ORIENT[c.i]' in html}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
