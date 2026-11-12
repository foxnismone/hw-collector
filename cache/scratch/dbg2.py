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
i = h.find('HIST=')
eq = h.find('=', i)
pl = h.find('{', eq)
ei = find_end(h, pl)
print(f"HIST: inicio {i}, fin {ei}")
print(f"despues: {repr(h[ei:ei+100])}")
print()
# ver qué declaración sigue
print(f"buscar CASEBY: {h.find('CASEBY', ei)}")
j = h.find('CASEBY', ei)
print(f"contexto: {repr(h[j-60:j+40])}")
