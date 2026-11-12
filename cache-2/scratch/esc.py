h = open('index.html', encoding='utf-8').read()
import re
for fn in ['escA', 'escT', 'escJ']:
    m = re.search(r'function '+fn+r'\([^)]*\)\{[^}]*\}', h)
    if not m:
        m = re.search(r'const '+fn+r'\s*=', h)
    if m:
        i = m.start()
        end = h.find('}', i)
        print(f"=== {fn} ===")
        print(h[i:h.find(';',end)+1] if ';' in h[i:h.find(';',end)+1] else h[i:end+1])
        print()
    else:
        # maybe arrow const ending with =>...;
        idx = h.find('const '+fn+'=')
        if idx!=-1:
            print(f"--- {fn} @ {idx} (arrow)")
            print(h[idx:idx+160])
            print()
