import re
h = open('index.html', encoding='utf-8').read()
# extraer todo el contenido de <script>...</script>
scripts = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', h, re.S)
print("scripts encontrados:", len(scripts))
big = max(scripts, key=len)
open('cache-2/scratch/inline.js','w',encoding='utf-8').write(big)
print("inline.js bytes:", len(big))
