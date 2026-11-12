import os
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

h = open('cache/scratch/index_backup.html', encoding='utf-8').read()
for nombre in ['const HIST=', 'const IDXINFO=', 'const CAJ=']:
    i = h.find(nombre)
    if i < 0:
        print(f"{nombre}: no encontrado"); continue
    eq = h.find('=', i)
    pb = h.find('[', eq); pl = h.find('{', eq)
    if pb < 0: pb = len(h)
    if pl < 0: pl = len(h)
    op = min(pb, pl)
    ei = find_end(h, op)
    print(f"=== {nombre} ===")
    print(f"  inicio: {i}  fin: {ei}")
    print(f"  contexto despues: {repr(h[ei:ei+80])}")
    print()
