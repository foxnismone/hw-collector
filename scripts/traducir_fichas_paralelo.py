#!/usr/bin/env python3
"""Traduce fichas a ES/PT/FR en PARALELO (ThreadPool).
Reanuda desde lo ya traducido. Entrada: data/fichas_reales.json
"""
import json, urllib.request, urllib.parse, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'
SALIDA = BASE + 'fichas_traducidas.json'

def traducir(texto, tl='es', intentos=4):
    if not texto or len(texto.strip()) < 5:
        return texto
    url = ('https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl='
           + tl + '&dt=t&q=' + urllib.parse.quote(texto[:4500]))
    for i in range(intentos):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return ''.join(x[0] for x in data[0] if x[0])
        except Exception:
            time.sleep(0.8 * (i + 1))
    return texto

def tarea(nombre, f):
    textos = {k: f.get(k, '') for k in ('descripcion', 'historia', 'curiosidades', 'dato_clave')}
    ent = {'galeria': f.get('galeria', []), 'disenador': f.get('disenador', '')}
    for tl in ('es', 'pt', 'fr'):
        ent[tl] = {k: traducir(v, tl) for k, v in textos.items() if v}
    return nombre, ent

def main():
    fichas = json.load(open(BASE + 'fichas_reales.json', encoding='utf-8'))
    resultado = {}
    if os.path.exists(SALIDA):
        resultado = json.load(open(SALIDA, encoding='utf-8'))
    print(f"Fichas reales: {len(fichas)} | ya traducidas: {len(resultado)}")

    pend = [(n, f) for n, f in fichas.items() if n not in resultado]
    print(f"Pendientes: {len(pend)}")

    ok = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(tarea, n, f): n for n, f in pend}
        for fut in as_completed(futures):
            try:
                n, ent = fut.result()
                resultado[n] = ent
                ok += 1
            except Exception:
                ok += 1
            if ok % 25 == 0:
                json.dump(resultado, open(SALIDA, 'w', encoding='utf-8'), ensure_ascii=False)
                print(f"  {ok}/{len(pend)}...")

    json.dump(resultado, open(SALIDA, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"\nTraducidas ahora: {len(resultado)}/{len(fichas)}")

if __name__ == '__main__':
    main()
