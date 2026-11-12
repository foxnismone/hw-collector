html = open('index.html', encoding='utf-8').read()
for f in ['radar','barrasFactores','histo','donut','valorRef','bestChannels','_hist','galeriaHTML','abrirGaleria']:
    ok = ('function '+f) in html or (f+'=') in html or (f+' =') in html
    print(f"  {f}: {'OK' if ok else '*** FALTA ***'}")
print()
for v in ['IDXINFO','HIST','IDXI','MKT','CASEBY','DEM']:
    ok = ('const '+v) in html or ('var '+v) in html or (v+'=') in html
    print(f"  var {v}: {'OK' if ok else '*** FALTA ***'}")
