import json, re
p = 'data/cat.js'
raw = open(p, encoding='utf-8').read()
print('size:', len(raw), 'bytes')
m = re.search(r"^const\s+CAT\s*=\s*(\[.*\]);\s*$", raw, re.S | re.M)
if not m:
    print('FALLO: no se reconoce const CAT=[...]')
    print('primeros 120:', raw[:120])
else:
    print('OK: encabezado const CAT=[ reconocido')
    try:
        d = json.loads(m.group(1))
        print('OK: JSON valido, longitud =', len(d))
        print('con im:', sum(1 for x in d if x.get('im')))
        print('sin im:', sum(1 for x in d if not x.get('im')))
        print('primer modelo:', d[0]['m'], '|', d[0]['k'], '|', d[0]['y'])
        # verificar que los .webp referenciados existen
        import os
        missing = sum(1 for x in d if x.get('im','').endswith('.webp')
                      and not os.path.exists(os.path.join('img', x['im'])))
        print('webp referenciados pero faltantes en img/:', missing)
    except Exception as e:
        print('FALLO parse:', str(e)[:200])
