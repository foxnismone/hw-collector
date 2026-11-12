import re
html = open('index.html', encoding='utf-8').read()
m = re.search(r'http-equiv="Content-Security-Policy" content="([^"]+)"', html)
print("CSP:", m.group(1))
print()
print("frame-ancestors presente:", "frame-ancestors" in m.group(1))
print("qrcode.min.js ocurrencias:", [html[max(0,i.start()-60):i.start()+30] for i in re.finditer('qrcode.min.js', html)])
