import re, subprocess, json, os
os.chdir(r'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector')
html = open('index.html', encoding='utf-8').read()
scripts = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.DOTALL)
open('cache/scratch/final.js','w',encoding='utf-8').write('\n;\n'.join(scripts))
r = subprocess.run(['node','--check','cache/scratch/final.js'], capture_output=True, text=True, shell=True)
print(f'JS valido: {r.returncode==0}')
if r.returncode: print(r.stderr[:400])

def find_end(s,oi):
    d=0;ins=False;esc=False
    for j in range(oi,len(s)):
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

i=html.find('const CAT=['); o=html.find('[',i); e=find_end(html,o)
cat=json.loads(html[o:e])
print(f'CAT: {len(cat)}')
print(f'Packs Car Culture: {sum(1 for m in cat if m.get("k")=="Car Culture")}')
print(f'Con ficha ES/PT/FR: {sum(1 for m in cat if isinstance(m.get("ficha"),dict) and m["ficha"].get("es"))}')
print(f'Con galeria: {sum(1 for m in cat if m.get("galeria"))}')
print(f'HTML: {len(html):,} chars ({len(html)/1024/1024:.1f} MB)')
