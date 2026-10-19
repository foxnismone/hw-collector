#!/usr/bin/env python3
"""Traduce las biografías completas (bio_en_raw) a ES/PT/FR y arma la narrativa final."""
import json, urllib.request, urllib.parse, time, re

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def traducir(texto, tl='es'):
    if not texto or len(texto.strip()) < 3:
        return texto
    url = ('https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl='
           + tl + '&dt=t&q=' + urllib.parse.quote(texto[:4800]))
    for i in range(3):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return ''.join(x[0] for x in data[0] if x[0])
        except Exception:
            time.sleep(1.5 * (i + 1))
    return texto

def resumen_castings(castings, idioma='es'):
    """Frase que resume los castings para insertar en la narrativa."""
    if not castings:
        return ''
    n = len(castings)
    anios = sorted({c['anio'] for c in castings if c.get('anio')})
    rango = f"{anios[0]}–{anios[-1]}" if len(anios) > 1 else (anios[0] if anios else '')
    series = {}
    for c in castings:
        s = (c.get('serie') or '').strip()
        if s:
            series[s] = series.get(s, 0) + 1
    top_series = sorted(series.items(), key=lambda kv: -kv[1])[:5]
    modelos = []
    vistos = set()
    for c in castings:
        nm = (c.get('nombre') or '').strip()
        if nm and nm.lower() not in vistos:
            vistos.add(nm.lower()); modelos.append(nm)
    muestra = ', '.join(modelos[:12])

    if idioma == 'es':
        partes = [f"Tiene {n} castings documentados"]
        if rango:
            partes.append(f"en el período {rango}")
        txt = ' '.join(partes) + '.'
        if muestra:
            txt += f" Entre sus diseños figuran {muestra}"
            txt += f" y {len(modelos)-12} modelos más." if len(modelos) > 12 else '.'
        if top_series:
            txt += " Sus series más frecuentes son " + ', '.join(f"{s} ({k})" for s, k in top_series) + '.'
        return txt
    if idioma == 'pt':
        txt = f"Tem {n} castings documentados" + (f" no período {rango}" if rango else '') + '.'
        if muestra:
            txt += f" Entre seus projetos estão {muestra}"
            txt += f" e mais {len(modelos)-12} modelos." if len(modelos) > 12 else '.'
        return txt
    if idioma == 'fr':
        txt = f"Il compte {n} castings documentés" + (f" sur la période {rango}" if rango else '') + '.'
        if muestra:
            txt += f" Parmi ses créations figurent {muestra}"
            txt += f" et {len(modelos)-12} autres modèles." if len(modelos) > 12 else '.'
        return txt
    return ''

def main():
    with open(BASE + 'disenadores.json', encoding='utf-8') as f:
        dis = json.load(f)

    pendientes = [n for n, d in dis.items() if d.get('bio_en_raw') and not d.get('bio_es_v2')]
    print(f"Pendientes de traducir: {len(pendientes)}")

    hechos = 0
    for nombre in pendientes:
        d = dis[nombre]
        en = d['bio_en_raw']
        castings = d.get('castings', [])

        es = traducir(en, 'es')
        pt = traducir(en, 'pt')
        fr = traducir(en, 'fr')

        # narrativa final = intro traducida + resumen de castings
        res_es = resumen_castings(castings, 'es')
        res_pt = resumen_castings(castings, 'pt')
        res_fr = resumen_castings(castings, 'fr')

        d['bio_es_v2'] = (es + (' ' + res_es if res_es else '')).strip()
        d['bio_pt_v2'] = (pt + (' ' + res_pt if res_pt else '')).strip()
        d['bio_fr_v2'] = (fr + (' ' + res_fr if res_fr else '')).strip()
        d['bio_en_v2'] = (en + (' ' + resumen_castings(castings, 'es') if res_es else '')).strip()

        # compatibilidad: sobrescribir los campos que usa la app
        d['bio_es'] = d['bio_es_v2']
        d['bio_pt'] = d['bio_pt_v2']
        d['bio_fr'] = d['bio_fr_v2']
        d['bio_en'] = en
        d['biografia_limpia'] = d['bio_es_v2']

        hechos += 1
        if hechos % 5 == 0:
            with open(BASE + 'disenadores.json', 'w', encoding='utf-8') as f:
                json.dump(dis, f, ensure_ascii=False, indent=2)
            print(f"  {hechos}/{len(pendientes)} traducidos...")
        time.sleep(0.2)

    with open(BASE + 'disenadores.json', 'w', encoding='utf-8') as f:
        json.dump(dis, f, ensure_ascii=False, indent=2)
    print(f"\nTraducidos: {hechos}")

    # Verificación
    con_v2 = sum(1 for d in dis.values() if d.get('bio_es_v2'))
    largo_prom = sum(len(d.get('bio_es_v2','')) for d in dis.values()) // max(con_v2,1)
    print(f"Con bio v2: {con_v2}/{len(dis)} | largo promedio: {largo_prom} chars")

if __name__ == '__main__':
    main()
