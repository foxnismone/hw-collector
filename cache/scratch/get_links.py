import re
html = open('index.html', encoding='utf-8').read()
print("=== <a> externos ===")
for m in re.finditer(r'<a[^>]*href="https?://[^"]*"[^>]*>', html):
    print(f"  {m.start():>7}  {m.group(0)[:150]}")
print("\n=== onclick con interpolacion (sin escJ) ===")
for m in re.finditer(r'onclick="[^"]*\'\$\{[^}]+\}\'', html):
    seg = m.group(0)
    if 'escJ' not in seg:
        print(f"  {m.start():>7}  {seg[:110]}")
