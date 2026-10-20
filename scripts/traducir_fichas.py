#!/usr/bin/env python3
"""Traduce las fichas reales (descripcion/historia/curiosidades/dato_clave) a ES/PT/FR.
Entrada: data/fichas_reales.json
Salida:  data/fichas_traducidas.json  ->  {nombre: {es:{...}, pt:{...}, fr:{...}, galeria:[...]}}
"""
import json, urllib.request, urllib.parse, time, os

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'
SALIDA = BASE + 'fichas_traducidas.json'

def traducir(texto, tl='es', intentos=3):
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
            time.sleep(1.5 * (i + 1))
    return texto

def main():
    fichas = json.load(open(BASE + 'fichas_reales.json', encoding='utf-8'))
    print(f"Fichas reales: {len(fichas)}")

    resultado = {}
    if os.path.exists(SALIDA):
        resultado = json.load(open(SALIDA, encoding='utf-8'))

    pend = [n for n in fichas if n not in resultado]
    print(f"Pendientes de traducir: {len(pend)}")

    ok = 0
    for i, nombre in enumerate(pend):
        f = fichas[nombre]
        # Textos a traducir
        textos = {
            'descripcion': f.get('descripcion', ''),
            'historia': f.get('historia', ''),
            'curiosidades': f.get('curiosidades', ''),
            'dato_clave': f.get('dato_clave', '')
        }
        ent = {'galeria': f.get('galeria', []), 'disenador': f.get('disenador', '')}
        for tl in ('es', 'pt', 'fr'):
            ent[tl] = {k: traducir(v, tl) for k, v in textos.items() if v}
        resultado[nombre] = ent
        ok += 1
        if ok % 20 == 0:
            json.dump(resultado, open(SALIDA, 'w', encoding='utf-8'), ensure_ascii=False)
            print(f"  {ok}/{len(pend)} traducidos...")

    json.dump(resultado, open(SALIDA, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"\nTraducidas: {ok} | total: {len(resultado)}")

if __name__ == '__main__':
    main()
