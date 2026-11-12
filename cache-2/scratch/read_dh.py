h = open('index.html', encoding='utf-8').read()
import re
# disHTML
i = h.find('disHTML'); 
print("disHTML @", i)
# drawerHTML function
for name in ['function drawerHTML','function fichaHTML','const dh=','div class="dh"','<img class="mirror"']:
    j = h.find(name)
    print(f"--- {name} @ {j}")
    if j != -1:
        print("  ", h[j:j+260].replace('\n',' '))
    print()
