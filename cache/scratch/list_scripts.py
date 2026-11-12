import re
html = open('index.html', encoding='utf-8').read()
print("=== TODOS los tags <script> ===")
for m in re.finditer(r'<script([^>]*)>', html):
    attrs = m.group(1).strip()
    es_src = 'src=' in attrs
    print(f"  {m.start():>8}  {'SRC' if es_src else 'INLINE'}  {attrs[:60]}")
print("\n=== TODOS los </script> ===")
for m in re.finditer(r'</script>', html):
    print(f"  {m.start():>8}")
