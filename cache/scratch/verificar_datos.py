import json, os
os.chdir(r'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector')

def find_end(s, oi):
    d=0; ins=False; esc=False
    for j in range(oi, len(s)):
        c=s[j]
        if ins:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c=='"': ins=False
            continue
        if c=='"': ins=True
        elif c in '[{': d+=1
        elif c in ']}':
            d-=1
            if d==0: return j+1
    return -1

def cargar(archivo):
    txt = open(archivo, encoding='utf-8').read()
    i = txt.find('=')
    pb = txt.find('[', i); pl = txt.find('{', i)
    if pb < 0: pb = len(txt)
    if pl < 0: pl = len(txt)
    op = min(pb, pl)
    ei = find_end(txt, op)
    return json.loads(txt[op:ei])

CAT = cargar('data/cat.js')
DIS = cargar('data/disenadores.js')
RUE = cargar('data/ruedas.js')
SER = cargar('data/series.js')

print(f'CAT: {len(CAT)}')
print(f'DISENADORES: {len(DIS)}')
print(f'WHEELTYPES: {len(RUE)}')
print(f'SERIES: {len(SER)}')
print(f'Con ficha ES: {sum(1 for m in CAT if isinstance(m.get("ficha"),dict) and m["ficha"].get("es"))}')
print(f'Con galeria: {sum(1 for m in CAT if m.get("galeria"))}')
print(f'Con imagen: {sum(1 for m in CAT if m.get("im"))}')
print(f'Con disenador: {sum(1 for m in CAT if m.get("disenador"))}')
anos = [m["y"] for m in CAT if m.get("y")]
print(f'Anios: {min(anos)} - {max(anos)}')
from collections import Counter
c = Counter(anos)
print(f'Modelos por decada:')
for dec in range(1960, 2030, 10):
    print(f'  {dec}s: {sum(v for k,v in c.items() if dec<=k<dec+10)}')

# Ejemplo de ficha real
ej = [m for m in CAT if isinstance(m.get("ficha"),dict) and m["ficha"].get("es") and len(m["ficha"]["es"].get("descripcion",""))>200]
if ej:
    print(f'\nEjemplo ficha real: {ej[0]["m"]}')
    print(f'  {ej[0]["ficha"]["es"]["descripcion"][:150]}')
