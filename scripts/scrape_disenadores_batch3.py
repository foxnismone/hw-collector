#!/usr/bin/env python3
"""
Deep scraping de diseñadores para los 670 modelos sin asignar.
Corregido: el contenido está en slots.main.content (no '*'),
y el diseñador está en el template {{casting|designer=[[Nombre]]|...}}.
"""
import json, re, urllib.request, urllib.parse, time, sys

API = 'https://hotwheels.fandom.com/api.php'
UA = 'Mozilla/5.0 (hotwheels-research)'

def api_fandom(params):
    url = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', UA)
    req.add_header('Referer', 'https://hotwheels.fandom.com/')
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))

def extraer_disenador(wikitext):
    if not wikitext:
        return None
    # Template casting: designer=[[Nombre Apellido]]
    # El template es {{casting|name=...|designer=[[Nombre]]|...}}
    # Después del diseñador viene un | o }}
    patron = r'\{\{casting\b[^}]*\|\s*designer\s*=\s*(.+?)(?:\}\}|\|)'
    m = re.search(patron, wikitext, re.IGNORECASE | re.DOTALL)
    if not m:
        patron2 = r'\|\s*designer\s*=\s*(.+?)(?:\n|\||\}\})'
        m = re.search(patron2, wikitext, re.IGNORECASE)
    if not m:
        return None
    
    valor = m.group(1).strip()
    links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', valor)
    if links:
        nombres = [l.strip() for l in links if not l.startswith(('Category:', 'File:', 'Image:'))]
        if nombres:
            return nombres[0]
    
    valor = re.sub(r'\{\{[^}]*\}\}', '', valor)
    valor = re.sub(r'<[^>]+>', '', valor)
    valor = valor.strip('[]')
    valor = valor.strip()
    if valor and len(valor) > 2 and not valor.startswith('Category:'):
        return valor
    return None

def main():
    with open('data/catalog_web.json', encoding='utf-8') as f:
        catalog = json.load(f)
    
    sin_dis = [m for m in catalog if not m.get('diseñador')]
    print(f'Modelos sin diseñador: {len(sin_dis)}')
    
    resultados = {}
    no_encontrados = []
    
    batch_size = 50
    total = len(sin_dis)
    
    for i in range(0, total, batch_size):
        batch = sin_dis[i:i+batch_size]
        titulos = []
        mapa_titulo_a_id = {}
        
        for m in batch:
            nombre = m.get('m', '').strip()
            titulo = nombre.replace(' ', '_')
            titulos.append(titulo)
            mapa_titulo_a_id[titulo] = m.get('i')
            mapa_titulo_a_id[nombre] = m.get('i')
        
        num_batch = i//batch_size + 1
        total_batches = (total + batch_size - 1)//batch_size
        print(f'\nBatch {num_batch}/{total_batches} ({i+1}-{min(i+batch_size, total)} de {total})...')
        
        try:
            data = api_fandom({
                'action': 'query',
                'prop': 'revisions',
                'titles': '|'.join(titulos),
                'rvslots': '*',
                'rvprop': 'content',
                'format': 'json',
                'formatversion': '2',
                'redirects': '1'
            })
            
            paginas = data.get('query', {}).get('pages', [])
            for pagina in paginas:
                titulo = pagina.get('title', '')
                id_modelo = mapa_titulo_a_id.get(titulo)
                
                if pagina.get('missing'):
                    if id_modelo:
                        no_encontrados.append(id_modelo)
                    continue
                
                revisiones = pagina.get('revisions', [])
                if not revisiones:
                    if id_modelo:
                        no_encontrados.append(id_modelo)
                    continue
                
                wikitext = revisiones[0].get('slots', {}).get('main', {}).get('content', '')
                disenador = extraer_disenador(wikitext)
                
                if disenador and id_modelo:
                    resultados[id_modelo] = disenador
                    print(f'  OK {titulo} -> {disenador}')
                elif id_modelo:
                    no_encontrados.append(id_modelo)
                    if wikitext:
                        for linea in wikitext.split('\n'):
                            if 'design' in linea.lower():
                                print(f'    FALLO {titulo} -> {linea.strip()[:100]}')
                                break
                        else:
                            print(f'  FALLO {titulo} -> sin campo designer')
                    else:
                        print(f'  FALLO {titulo} -> sin contenido')
            
            with open('data/disenadores_batch3.json', 'w', encoding='utf-8') as f:
                json.dump(resultados, f, ensure_ascii=False, indent=2)
            print(f'  Progreso: {len(resultados)}/{total} asignados, {len(no_encontrados)} sin encontrar')
            
        except Exception as e:
            print(f'  ERROR en batch: {e}')
            time.sleep(3)
            for m in batch:
                nombre = m.get('m', '').strip()
                titulo = nombre.replace(' ', '_')
                try:
                    data = api_fandom({
                        'action': 'query',
                        'prop': 'revisions',
                        'titles': titulo,
                        'rvslots': '*',
                        'rvprop': 'content',
                        'format': 'json',
                        'formatversion': '2'
                    })
                    paginas = data.get('query', {}).get('pages', [])
                    for pagina in paginas:
                        if pagina.get('missing'):
                            no_encontrados.append(m.get('i'))
                            continue
                        revisiones = pagina.get('revisions', [])
                        if not revisiones:
                            no_encontrados.append(m.get('i'))
                            continue
                        wikitext = revisiones[0].get('slots', {}).get('main', {}).get('content', '')
                        disenador = extraer_disenador(wikitext)
                        if disenador:
                            resultados[m.get('i')] = disenador
                            print(f'  OK {titulo} -> {disenador}')
                        else:
                            no_encontrados.append(m.get('i'))
                except Exception as e2:
                    print(f'    ERROR individual: {e2}')
                    no_encontrados.append(m.get('i'))
        
        time.sleep(0.5)
    
    print(f'\n=== RESUMEN FINAL ===')
    print(f'Total sin diseñador: {total}')
    print(f'Asignados: {len(resultados)}')
    print(f'No encontrados: {len(no_encontrados)}')
    
    with open('data/disenadores_batch3.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f'\nResultados guardados en data/disenadores_batch3.json')
    
    return len(resultados)

if __name__ == '__main__':
    asignados = main()
    sys.exit(0 if asignados > 0 else 1)
