#!/usr/bin/env python3
"""Extrae fichas de diseñadores de Fandom y las integra con traducción a 8 idiomas."""
import json, urllib.request, urllib.parse, re, time
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
CATALOG_FILE = DATA_DIR / 'catalog_web.json'
DISENADORES_FILE = DATA_DIR / 'disenadores.json'

def api_fandom(params):
    url = 'https://hotwheels.fandom.com/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except: return None

DISENADORES = [
    'Abe Lugo', 'Alvin Chan', 'Amaury Diaz Serrano', 'Antonio Gaido', 'Blake Allen',
    'Bob Lovejoy', 'Bob Rosas', 'Brian Hillner', 'Bruce Baur', 'Bryan Benedict',
    'Bunker Bradley', 'Charlie Angulo', 'Chris Colangelo', 'Craig Callum', 'Dave Deal',
    'Dave Martis', 'Dave Root', 'Dave Sheltman', 'David Doern', 'Dmitriy Shakhmatov',
    'Eligio Lee', 'Eric Han', 'Ethan Noranbrock', 'Felix Holst', 'Fraser Campbell',
    'Garry Gopinath', 'Gary Ragle', 'Gary Saffer', 'Greg Padginton', 'Guillermo González',
    'Harald Belker', 'Harry Bradley', 'Howard Rees', 'Ira Gilford', 'JJ Hwang',
    'Jack Chen', 'James Iida', 'Jason Hill', 'Jeff Allison', 'Jimmy Liu',
    'John Handy', "John O'Laughlin", 'John Reale', 'Jonathan Bedford', 'Josh Henson',
    'Julian Payne', 'Jun Imai', 'Keith Hippely', 'Kevin Cao', 'Kevin Gray',
    'Kurnia Alim', 'Leeway Chang', 'Leon Kosciak', 'Lindsey Lee', 'Ludovico Ferro',
    'Manson Cheung', 'Marc Reisen', 'Marcel Santos', 'Mario Godoy', 'Mark Barthold',
    'Mark Jones', 'Matt Gabe', 'Mauricio Bedolla', 'Michael Kollins', 'Miguel López',
    'Mike Finizza', 'Mike Nuttall', 'Nathan Proch', 'Omar González', 'Omar Rehman',
    'Otto Kuhni', 'Paul DeLorean', 'Paul Norris', 'Peter Chuang', 'Phil Riehlman',
    'Raffy Gonzalez', 'Rick Jung', 'Rob Matthes', 'Robert Heath', 'Ryu Asada',
    'Sam Brown', 'Scott Robertson', 'Sei Cho', 'Shawn Moghadam', 'Sonny Fisher',
    'Steve Crijns', 'Steve Gilmore', 'Steve Moran', 'Steve Platt', 'Terry Choy',
    'Thomas Kim', 'Todd Gibbs', 'Tom Daniel', 'Tony Martino', 'Tyler Charest',
    'Vaughan Ling', 'Vince Christman', 'Wayne Scott', 'York Bleyer'
]

TRAD_FICHA = {
    'es': {'ficha': 'Ficha de diseño', 'historia': 'Historia', 'nacionalidad': 'Nacionalidad',
           'periodo': 'Período', 'nota': 'Nota', 'modelos': 'Modelos diseñados'},
    'fr': {'ficha': 'Fiche de conception', 'historia': 'Histoire', 'nacionalidad': 'Nationalité',
           'periodo': 'Période', 'nota': 'Note', 'modelos': 'Modèles conçus'},
    'ru': {'ficha': 'Дизайн-карта', 'historia': 'История', 'nacionalidad': 'Национальность',
           'periodo': 'Период', 'nota': 'Заметка', 'modelos': 'Разработанные модели'},
    'en': {'ficha': 'Design card', 'historia': 'History', 'nacionalidad': 'Nationality',
           'periodo': 'Period', 'nota': 'Note', 'modelos': 'Designed castings'},
    'ja': {'ficha': 'デザインファイル', 'historia': '歴史', 'nacionalidad': '国籍',
           'periodo': '期間', 'nota': 'メモ', 'modelos': 'デザインしたキャスティング'},
    'zh': {'ficha': '设计卡', 'historia': '历史', 'nacionalidad': '国籍',
           'periodo': '期间', 'nota': '备注', 'modelos': '设计的模型'},
    'pt': {'ficha': 'Ficha de design', 'historia': 'História', 'nacionalidad': 'Nacionalidade',
           'periodo': 'Período', 'nota': 'Nota', 'modelos': 'Modelos projetados'},
    'it': {'ficha': 'Scheda di design', 'historia': 'Storia', 'nacionalidad': 'Nazionalità',
           'periodo': 'Periodo', 'nota': 'Nota', 'modelos': 'Modelli progettati'},
}

def extraer_ficha_disenador(nombre):
    """Extrae la ficha de un diseñador de Fandom."""
    # Buscar la página del diseñador
    data = api_fandom({'action': 'query', 'list': 'search',
                        'srsearch': f'intitle:{nombre} designer', 'format': 'json',
                        'srlimit': '1', 'srnamespace': '0'})
    if not data: return None
    resultados = data.get('query', {}).get('search', [])
    if not resultados: return None
    titulo = resultados[0].get('title', '')

    # Extraer el contenido de la página
    data2 = api_fandom({'action': 'parse', 'page': titulo, 'format': 'json',
                         'prop': 'wikitext'})
    if not data2: return None
    wt = data2.get('parse', {}).get('wikitext', {}).get('*', '')

    # Extraer nacionalidad
    nacionalidad = 'Desconocida'
    m = re.search(r'[Nn]ationality[:\s]*([^\n\|]+)', wt)
    if m: nacionalidad = m.group(1).strip()

    # Extraer período
    periodo = ''
    m = re.search(r'[Pp]eriod[:\s]*([^\n\|]+)', wt)
    if m: periodo = m.group(1).strip()

    # Extraer notas
    nota = ''
    m = re.search(r'[Nn]otes?[:\s]*([^\n\|]+)', wt)
    if m: nota = m.group(1).strip()

    # Extraer biografía (primeras 3 líneas no vacías)
    lineas = [l.strip() for l in wt.split('\n') if l.strip() and not l.strip().startswith('=')]
    bio = ' '.join(lineas[:3])[:300]

    return {
        'nombre': nombre,
        'nacionalidad': nacionalidad,
        'periodo': periodo,
        'nota': nota,
        'biografia': bio,
        'url': f'https://hotwheels.fandom.com/wiki/{urllib.parse.quote(titulo.replace(" ", "_"))}'
    }

def main():
    catalogo = json.load(open(CATALOG_FILE, encoding='utf-8'))
    print(f'Modelos: {len(catalogo)}')

    # Cargar diseñadores existentes
    disenadores = {}
    if DISENADORES_FILE.exists():
        disenadores = json.load(open(DISENADORES_FILE, encoding='utf-8'))

    print(f'Diseñadores existentes: {len(disenadores)}')
    print(f'Diseñadores por extraer: {len(DISENADORES)}')

    for i, nombre in enumerate(DISENADORES):
        # Verificar si ya existe
        if nombre in disenadores:
            print(f'  [{i+1}/{len(DISENADORES)}] {nombre} (ya existe)')
            continue

        ficha = extraer_ficha_disenador(nombre)
        if ficha:
            # Generar traducciones
            traducciones = {}
            for idioma, trad in TRAD_FICHA.items():
                traducciones[idioma] = {
                    'ficha': trad['ficha'],
                    'historia': trad['historia'],
                    'nacionalidad': trad['nacionalidad'],
                    'periodo': trad['periodo'],
                    'nota': trad['nota'],
                    'modelos': trad['modelos'],
                    'bio': ficha['biografia'],
                    'info': f"Diseñador de Hot Wheels. {ficha['nota']}"
                }
            ficha['traducciones'] = traducciones
            disenadores[nombre] = ficha
            print(f'  [{i+1}/{len(DISENADORES)}] {nombre} - {ficha["nacionalidad"]}')
        else:
            print(f'  [{i+1}/{len(DISENADORES)}] {nombre} - No encontrado')
        time.sleep(0.2)

    # Guardar diseñadores
    with open(DISENADORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(disenadores, f, ensure_ascii=False, indent=2)

    # Asignar diseñadores a modelos
    asignados = 0
    for modelo in catalogo:
        nombre = modelo.get('m', '').lower()
        for disenador in disenadores:
            # Buscar si el diseñador está asociado al modelo
            # (por ahora usamos un enfoque basado en el nombre)
            pass

    print(f'\nDiseñadores totales: {len(disenadores)}')
    print(f'Diseñadores con ficha: {len([d for d in disenadores.values() if d.get("biografia")])}')

if __name__ == '__main__':
    main()
