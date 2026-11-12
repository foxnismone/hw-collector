html = open('index.html', encoding='utf-8').read()

# nivelColor
i = html.find('function nivelColor')
print("=== nivelColor ===")
print(html[i:i+350] if i>=0 else "NO DEFINIDA")

# CSS .idx
import re
for pat in ['.idx{', '.idx ', '.fbar{', '.fbar ']:
    j = html.find(pat)
    print(f"\n=== {pat} ===")
    print(html[j:j+250].replace('\n',' ') if j>=0 else "NO EN CSS")

# .card CSS
k = html.find('.card{')
print("\n=== .card ===")
print(html[k:k+400].replace('\n',' ') if k>=0 else "NO")
