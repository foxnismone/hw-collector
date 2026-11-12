h = open('index.html', encoding='utf-8').read()

start = h.find("const sv='<svg")
end_marker = "'</svg>';"
end = h.find(end_marker, start) + len(end_marker)
old_sv = h[start:end]

new_sv = (
  'const sv=\'<svg xmlns="http://www.w3.org/2000/svg" width="\'+w+\'" height="\'+h+\'" viewBox="0 0 \'+w+\' \'+h+\'">\''
  '+\'<rect width="\'+w+\'" height="\'+h+\'" rx="\'+_r(w*0.042)+\'" fill="\'+c.bg+\'"/>\''
  '+\'<rect x="\'+m+\'" y="\'+m+\'" width="\'+_r(w-2*m)+\'" height="\'+_r(innerH)+\'" rx="\'+_r(rx)+\'" fill="\'+c.ev+\'" stroke="\'+c.ln+\'" stroke-width="1"/>\''
  '+\'<ellipse cx="\'+_r(cx)+\'" cy="\'+_r(fy)+\'" rx="\'+_r((wr-wl)/2+12)+\'" ry="\'+_r(r*0.42)+\'" fill="\'+c.ac+\'" opacity=".55"/>\''
  '+\'<circle cx="\'+_r(wl)+\'" cy="\'+_r(fy)+\'" r="\'+_r(r)+\'" fill="\'+c.br+\'" opacity=".45"/>\''
  '+\'<circle cx="\'+_r(wr)+\'" cy="\'+_r(fy)+\'" r="\'+_r(r)+\'" fill="\'+c.br+\'" opacity=".45"/>\''
  '+\'<circle cx="\'+_r(wl)+\'" cy="\'+_r(fy)+\'" r="\'+_r(r*0.4)+\'" fill="\'+c.bg+\'"/>\''
  '+\'<circle cx="\'+_r(wr)+\'" cy="\'+_r(fy)+\'" r="\'+_r(r*0.4)+\'" fill="\'+c.bg+\'"/>\''
  '+\'<path d="M\'+_r(cx-13)+\' \'+_r(fy-r*1.6)+\' L\'+_r(cx)+\' \'+_r(fy-r*2.4)+\' L\'+_r(cx+14)+\' \'+_r(fy-r*1.6)+\' Z" fill="#ffffff" opacity=".75"/>\''
  '+\'<text x="\'+_r(cx)+\'" y="\'+_r(h-8)+\'" font-size="11" fill="\'+c.mu+\'" text-anchor="middle" font-family="system-ui,monospace">Imagen pr\u00F3ximamente</text>\''
  '+\'</svg>\';'
)
# agrego helper _r para redondear y limpiar decimales (evita 7.476000000000001)
helper_anchor = "const c=noPhotoSVG._c, m=w*0.106;"
helper = "const _r=v=>+(Math.round(v*1000)/1000).toFixed(3); const c=noPhotoSVG._c, m=w*0.106;"
assert h.count(helper_anchor) == 1, "helper anchor count"
assert h.count(old_sv) == 1, "old_sv count"
h = h.replace(helper_anchor, helper, 1)
h = h.replace(old_sv, new_sv, 1)

open('index.html','w',encoding='utf-8').write(h)
print("sv reescrito. noPhotoSVG count:", h.count('noPhotoSVG'))
print("auto-cierre /> en svg:", h.count('/>'))
# verificar que la funcion esta bien balanceada
import subprocess
print("chequeo sintaxis JS...", )
