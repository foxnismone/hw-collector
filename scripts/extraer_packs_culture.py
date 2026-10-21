#!/usr/bin/env python3
"""Extrae los Car Culture 2-Packs completos desde Fandom:
  - toy#, año, mix, theme, 2 castings, color, ruedas, foto del pack (Photo Carded)
Salida: data/packs_culture.json
"""
import json, urllib.request, urllib.parse, re, time

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

def limpiar(t):
    if not t: return ''
    t = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[\[([^\]]*)\]\]', r'\1', t)
    t = re.sub(r"''+", '', t)
    t = re.sub(r'<br\s*/?>', ' ', t)
    t = re.sub(r'\s{2,}', ' ', t)
    return t.strip()

def main():
    d = api({'action':'parse','page':'Car Culture 2-Packs','prop':'wikitext','format':'json'})
    wt = d['parse']['wikitext']['*']

    # Dividir por año (==YYYY==)
    partes = re.split(r'^==(\d{4})==\s*$', wt, flags=re.MULTILINE)
    # partes[0] = intro, luego [año, contenido, año, contenido...]
    packs = []
    for i in range(1, len(partes), 2):
        anio = int(partes[i])
        contenido = partes[i+1]
        # Dividir por mix (===Mix N===)
        mixes = re.split(r'^===Mix (\d+)===\s*$', contenido, flags=re.MULTILINE)
        for j in range(1, len(mixes), 2):
            num_mix = int(mixes[j])
            tabla = mixes[j+1]
            # Buscar cada pack: rowspan="2" |TOY#  seguido de rowspan="2" |THEME
            # Patrón: | rowspan="2" |HBL97\n| rowspan="2" |Larry Chen
            for m in re.finditer(r'\|\s*rowspan="2"\s*\|\s*([A-Z0-9]+)\s*\n\|\s*rowspan="2"\s*\|\s*([^\n]+)', tabla):
                toy = m.group(1).strip()
                theme = limpiar(m.group(2))
                # Bloque del pack (hasta el siguiente rowspan o fin de tabla)
                inicio = m.end()
                sig = re.search(r'\|\s*rowspan="2"\s*\|\s*[A-Z0-9]+\s*\n', tabla[inicio:])
                bloque = tabla[inicio:inicio+sig.start()] if sig else tabla[inicio:]

                # Castings del bloque
                castings = []
                for cm in re.finditer(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', bloque):
                    c = cm.group(1).strip()
                    if c and not c.startswith('File:') and not c.startswith('RR') and not c.startswith('RRA') and not c.startswith('RRE') and not c.startswith('RRL') and not c.startswith('C4') and not c.startswith('MC') and not c.startswith('PR') and not c.startswith('OH') and not c.startswith('SK') and not c.startswith('DD') and not c.startswith('RT') and not c.startswith('J5') and not c.startswith('ID') and not c.startswith('MK') and not c.startswith('APP') and not c.startswith('S5') and not c.startswith('P4') and not c.startswith('5H') and not c.startswith('WTC') and not c.startswith('BTT') and not c.startswith('OR') and not c.startswith('NS') and not c.startswith('MM') and not c.startswith('SKB') and not c.startswith('AT') and not c.startswith('MT') and not c.startswith('BF') and not c.startswith('SS') and not c.startswith('GMP') and not c.startswith('RU') and not c.startswith('RS') and not c.startswith('Y5') and not c.startswith('L4') and not c.startswith('FC') and not c.startswith('E10') and not c.startswith('10S') and not c.startswith('3SP') and not c.startswith('5SP') and not c.startswith('7SP') and not c.startswith('MC5') and not c.startswith('MC8') and not c.startswith('MCP') and not c.startswith('MC3') and not c.startswith('MCR') and not c.startswith('RPR') and not c.startswith('R10') and not c.startswith('R5S') and not c.startswith('RBL') and not c.startswith('RU') and not c.startswith('SK5') and not c.startswith('TRR'):
                        castings.append(c)
                castings = list(dict.fromkeys(castings))

                # Foto del pack (Photo Carded) = último [[File:...2-Car Set...]]
                fotos_pack = re.findall(r'\[\[File:([^\]|]*2-Car Set[^\]|]*)\|', bloque, re.I)
                if not fotos_pack:
                    fotos_pack = re.findall(r'\[\[File:([^\]|]+)\|[^\]]*\]\]\s*\n\s*\|\s*$', bloque, re.M)
                foto_pack = fotos_pack[0] if fotos_pack else ''

                packs.append({
                    'toy': toy, 'anio': anio, 'mix': num_mix,
                    'theme': theme, 'castings': castings[:2],
                    'foto_pack': foto_pack
                })

    print(f"Packs encontrados: {len(packs)}")
    for p in packs[:8]:
        print(f"  {p['anio']} Mix{p['mix']} | {p['toy']} | {p['theme'][:30]} | {p['castings']}")
    print(f"  ...")
    for p in packs[-3:]:
        print(f"  {p['anio']} Mix{p['mix']} | {p['toy']} | {p['theme'][:30]} | {p['castings']}")

    # Fotos de pack únicas
    fotos = list(dict.fromkeys(p['foto_pack'] for p in packs if p['foto_pack']))
    print(f"\nFotos de pack únicas: {len(fotos)}")

    json.dump({'packs': packs, 'fotos': fotos}, open(BASE+'packs_culture.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
    print("Guardado en data/packs_culture.json")

if __name__ == '__main__':
    main()
