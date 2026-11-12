html = open('cache/scratch/index_backup.html', encoding='utf-8').read()
import re
print("=== data-open en backup ===")
for m in list(re.finditer(r'data-open', html))[:10]:
    print("  ", html[max(0,m.start()-180):m.start()+80].replace('\n',' '))
