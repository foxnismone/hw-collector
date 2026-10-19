#!/usr/bin/env python3
"""Traduce los nombres y descripciones de las ruedas al español."""
import json, urllib.request, urllib.parse, time

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

def traducir(texto, sl='en', tl='es'):
    if not texto or len(texto.strip()) < 2:
        return texto
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=' + sl + '&tl=' + tl + '&dt=t&q=' + urllib.parse.quote(texto[:1500])
    for intento in range(3):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return ''.join(x[0] for x in data[0] if x[0])
        except Exception:
            time.sleep(1.5 * (intento + 1))
    return texto

def main():
    with open(BASE + 'wheeltypes_reales.json', encoding='utf-8') as f:
        wheels = json.load(f)

    traducidos = 0
    for w in wheels:
        nombre = w.get('n', '')
        # Traducir el nombre si tiene palabras inglesas comunes
        if nombre and any(p in nombre.lower() for p in ['wheel', 'spoke', 'redline', 'black wall', 'white wall', 'real rider', 'hot one', 'basic', 'deep dish', 'off-road', 'construction', 'truck', 'motorcycle', 'star', 'skull', 'split', 'lace', 'turbine', 'pickup', 'street', 'race', 'steelie', 'chrome', 'gold', 'micro', 'mini']):
            n_es = traducir(nombre, 'en', 'es')
            w['n_es'] = n_es
            # Actualizar descripción
            d = w.get('d', {})
            anios = w.get('y', '')
            d['es'] = f"{n_es}. Tipo de rueda Hot Wheels usado entre {anios}."
            d['pt'] = traducir(nombre, 'en', 'pt') + f". Tipo de roda Hot Wheels usado entre {anios}."
            d['fr'] = traducir(nombre, 'en', 'fr') + f". Type de roue Hot Wheels utilisé entre {anios}."
            w['d'] = d
            traducidos += 1
            if traducidos % 20 == 0:
                print(f"  {traducidos} traducidos...")
                with open(BASE + 'wheeltypes_reales.json', 'w', encoding='utf-8') as f:
                    json.dump(wheels, f, ensure_ascii=False, indent=2)

    with open(BASE + 'wheeltypes_reales.json', 'w', encoding='utf-8') as f:
        json.dump(wheels, f, ensure_ascii=False, indent=2)
    print(f"Ruedas traducidas: {traducidos}/{len(wheels)}")

if __name__ == '__main__':
    main()
