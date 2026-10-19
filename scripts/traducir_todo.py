#!/usr/bin/env python3
"""Traduce TODO el contenido de Hot Wheels Collector a ES/PT/FR usando Google Translate free."""
import json, urllib.request, urllib.parse, time, os, sys

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def traducir(texto, sl='en', tl='es', reintentos=3):
    if not texto or len(texto.strip()) < 3:
        return texto
    # Truncar a 4500 chars (límite del endpoint)
    texto = texto[:4500]
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=' + sl + '&tl=' + tl + '&dt=t&q=' + urllib.parse.quote(texto)
    for intento in range(reintentos):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return ''.join(x[0] for x in data[0] if x[0])
        except Exception as e:
            time.sleep(1.5 * (intento + 1))
    return texto  # devolver original si falla

def es_ingles(texto):
    """Detecta si el texto está en inglés"""
    if not texto:
        return False
    PAL_EN = [' the ', ' was ', ' were ', ' from ', ' and ', ' with ', ' has ', ' his ', ' who ', ' worked ', ' designer ']
    n = sum(1 for p in PAL_EN if p in texto.lower())
    return n >= 2

def es_espanol(texto):
    if not texto:
        return False
    PAL_ES = [' diseñador', ' trabajó', ' fue ', ' durante', ' también', ' desde ', ' hasta ', ' mientras', ' más ', ' según', ' actualmente', ' equipo', ' empresa']
    n = sum(1 for p in PAL_ES if p in texto.lower())
    return n >= 2

def procesar_disenadores():
    print("=== TRADUCIENDO DISEÑADORES ===")
    with open(BASE + 'disenadores.json', encoding='utf-8') as f:
        dis = json.load(f)
    traducidos = 0
    for nombre, d in dis.items():
        bio = d.get('biografia_limpia') or d.get('bio_es') or ''
        if not bio or es_espanol(bio):
            continue
        if es_ingles(bio):
            es = traducir(bio, 'en', 'es')
            pt = traducir(bio, 'en', 'pt')
            fr = traducir(bio, 'en', 'fr')
            d['biografia_limpia'] = es
            d['bio_es'] = es
            d['bio_en'] = bio
            d['bio_pt'] = pt
            d['bio_fr'] = fr
            traducidos += 1
            if traducidos % 10 == 0:
                print(f"  {traducidos} traducidos...")
                with open(BASE + 'disenadores.json', 'w', encoding='utf-8') as f:
                    json.dump(dis, f, ensure_ascii=False, indent=2)
    with open(BASE + 'disenadores.json', 'w', encoding='utf-8') as f:
        json.dump(dis, f, ensure_ascii=False, indent=2)
    print(f"Diseñadores traducidos: {traducidos}")

def procesar_series():
    print("=== TRADUCIENDO SERIES ===")
    with open(BASE + 'series_ui.json', encoding='utf-8') as f:
        series = json.load(f)
    traducidos = 0
    for s in series:
        desc = s.get('d', '')
        if not desc or es_espanol(desc):
            continue
        if es_ingles(desc):
            es = traducir(desc, 'en', 'es')
            s['d'] = es
            s['d_en'] = desc
            traducidos += 1
            if traducidos % 25 == 0:
                print(f"  {traducidos} traducidos...")
                with open(BASE + 'series_ui.json', 'w', encoding='utf-8') as f:
                    json.dump(series, f, ensure_ascii=False, indent=2)
    with open(BASE + 'series_ui.json', 'w', encoding='utf-8') as f:
        json.dump(series, f, ensure_ascii=False, indent=2)
    print(f"Series traducidas: {traducidos}")

def procesar_ruedas():
    print("=== TRADUCIENDO RUEDAS ===")
    with open(BASE + 'wheeltypes_reales.json', encoding='utf-8') as f:
        wheels = json.load(f)
    traducidos = 0
    for w in wheels:
        d = w.get('d', {})
        es = d.get('es', '')
        # Si la descripción es solo la plantilla genérica, traducir el nombre
        nombre = w.get('n', '')
        if es_ingles(nombre):
            nombre_es = traducir(nombre, 'en', 'es')
            w['n_es'] = nombre_es
            traducidos += 1
    with open(BASE + 'wheeltypes_reales.json', 'w', encoding='utf-8') as f:
        json.dump(wheels, f, ensure_ascii=False, indent=2)
    print(f"Ruedas con nombre traducido: {traducidos}")

if __name__ == '__main__':
    procesar_disenadores()
    procesar_series()
    procesar_ruedas()
    print("COMPLETADO")
