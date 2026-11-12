import re
h = open('index.html', encoding='utf-8').read()
for sel in ['.dh ', '.mt ', '.catlogo', '.thumb ', 'grid-template', '.grid ', '.dem', '.idx ']:
    ms = list(re.finditer(re.escape(sel), h))
    if not ms: 
        continue
    m = ms[0]
    # buscar la regla CSS completa
    i = m.start()
    # buscar el cierre }
    end = h.find('}', i)
    if end == -1: end = i+300
    fragmento = h[i:end+1]
    # print solo si parece CSS (contiene { )
    if '{' in fragmento[:60]:
        print(f"--- '{sel}' ---")
        print("  ", fragmento[:260].replace('\n',' '))
        print()
