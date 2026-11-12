import re
html = open('index.html', encoding='utf-8').read()
# el script de galeria es el que empieza despues de vendor/supabase.js
m = re.search(r'<script src="vendor/supabase\.js"></script>\s*<script>([\s\S]*?)</script>', html)
if m:
    print("ENCONTRADO, longitud:", len(m.group(1)))
    # guardar el contenido
    open('cache/scratch/galeria_block.js','w',encoding='utf-8').write(m.group(1))
    print("guardado en cache/scratch/galeria_block.js")
else:
    print("no encontrado")
