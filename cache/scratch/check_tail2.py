html = open('index.html', encoding='utf-8').read()
import re
# todas las ocurrencias de ftrend
pos = [m.start() for m in re.finditer(r'ftrend', html)]
print("ocurrencias de ftrend:", pos)
# la ultima (en el script)
ult = pos[-1]
j = html.find('function initRuedas', ult)
print(f"\n=== desde ultima ftrend ({ult}) hasta initRuedas ({j}) ===")
print(html[ult:j][:3500])
