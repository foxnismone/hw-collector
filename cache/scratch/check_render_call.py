html = open('index.html', encoding='utf-8').read()
import re
i = html.find('function initPage()')
# buscar render( despues de initPage
for m in list(re.finditer(r'render\((true|false)\)', html[i:i+25000]))[:10]:
    pos = i + m.start()
    print(f"  [{m.group(0)}] en {pos}:", html[max(0,pos-150):pos+50].replace('\n',' ')[:200])
