h = open('index.html', encoding='utf-8').read()
i = h.find('brandlogo')  # first usage in HTML body (after the CSS)
# find usage after the <style> block / in body
j = h.find('brandlogo', 100)
print("=== brandlogo usage @", j)
print(h[j-260:j+120].replace('\n',' '))
print()
# el header bar / brand h1
k = h.find('<header class="top"')
if k==-1: k = h.find('class="top"')
print("=== header @", k)
print(h[k:k+400].replace('\n',' '))
