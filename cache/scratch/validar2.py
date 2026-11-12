import re, subprocess, json, os
os.chdir(r'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector')
html = open('index.html', encoding='utf-8').read()
scripts = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.DOTALL)
open('cache/scratch/app.js','w',encoding='utf-8').write('\n;\n'.join(scripts))
r = subprocess.run(['node','--check','cache/scratch/app.js'], capture_output=True, text=True, shell=True)
print(f'JS app valido: {r.returncode==0}')
if r.returncode: print(r.stderr[:400])

print(f"'const CAT=' en HTML: {'SI (problema)' if 'const CAT=' in html else 'no (correcto)'}")
print(f"'data/cat.js' en HTML: {'si' if 'data/cat.js' in html else 'NO (problema)'}")

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

for f in ['data/cat.js','data/disenadores.js','data/ruedas.js','data/series.js']:
    txt = open(f, encoding='utf-8').read()
    i = txt.find('=')
    pb = txt.find('[', i); pl = txt.find('{', i)
    if pb < 0: pb = len(txt)
    if pl < 0: pl = len(txt)
    op = min(pb, pl)
    ei = find_end(txt, op)
    try:
        data = json.loads(txt[op:ei])
        print(f'  {f}: {len(data)} elementos OK ({len(txt)/1024/1024:.1f} MB)')
    except Exception as e:
        print(f'  {f}: ERROR {str(e)[:60]}')
