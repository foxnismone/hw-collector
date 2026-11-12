html = open('index.html', encoding='utf-8').read()
import re
print("=== DOMContentLoaded / init ===")
for pat in ['DOMContentLoaded', 'initPage()', 'render(true)', 'window.onload', 'refreshAll()']:
    for m in list(re.finditer(re.escape(pat), html))[:2]:
        print(f"  [{pat}] ...", html[max(0,m.start()-120):m.start()+120].replace('\n',' ')[:250])
        print()
