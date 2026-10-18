import json

base = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

cat = json.load(open(base + 'catalog_web.json', encoding='utf-8'))
dis = json.load(open(base + 'disenadores.json', encoding='utf-8'))

# Asignar diseñadores conocidos
DIS_PRINCIPALES = {
    'Larry Wood': ['Custom Camaro', 'Custom Fleetside', 'Custom T-Bird', 'Custom Cougar', 'Custom Firebird', 'Custom Eldorado', 'Custom Corvette', 'Custom Volkswagen', 'Custom El Camino', 'Beatnik Bandit', 'Twin Mill', 'Hot Heap', 'Silhouette', 'Python', 'Mighty Maverick', 'Mod Quad', 'Paddy Wagon', 'Peeping Bomb', 'Jack Rabbit Special', 'Side-Burn', 'A-OK', 'Stagefright', "40's Woodie", "Dumin' A", "Screamin'", 'Tipper', 'Sho-Stopper'],
    'Ira Gilford': ['Heavy Chevy', 'King Kuda', 'Light My Firebird', 'Fire Bird', 'Sand Striker', 'Super Rig', 'Dump Truck', 'Cement Mixer', 'Moving Van', 'Fuel Tanker', 'Racer Rig', 'Pony Cargo', 'Wild Bill', 'Slick Rib', 'Skipper', 'Snake Mountain', "Da'Kar", "The Gov'ner", 'Hammerhead'],
    'Harry Bradley': ['Python', 'Silhouette', 'Deora', 'Custom Fleetside', 'Hot Heap', 'Ford J-Car', 'Oscar Mayer Wienermobile', 'Custom Camaro', 'Custom T-Bird', 'Custom Cougar', 'Custom Firebird', 'Custom Eldorado', 'Custom Corvette', 'Beatnik Bandit'],
    'Paul Tam': ['Whip Creamer', 'AMX/2', 'Evil Weevil', 'Hairy Hauler', 'Six Shooter', 'Ferrari 512S', 'Open Fire', 'Double Header'],
    'Bob Rosas': ['Chevy Monza 2+2', 'Lickety Six', 'A-OK', 'Hot Bird', 'Jaguar XJS', 'Quik Trik', 'Ultra-Sonix', 'Mach 7', 'Proformer', 'Gyracer', 'Excelerator'],
    'Howard Rees': ['Jack Rabbit Special', 'Mighty Maverick', 'Mod Quad', 'Paddy Wagon', 'Peeping Bomb', 'Crew Car', 'Noodle Head', 'Short Order'],
    'Terry Choy': ['Power Pistons', 'Road Rocket', 'Ford Focus', 'CCM Country Club Muscle', 'World Rally Championship'],
    'Bruce Baur': ['Twin Mill II', 'Silhouette II', 'Lexus SC400', 'Avus Quattro', 'Power Pipes', 'Rigor Motor', 'Torqued Off', 'Twang Thang', 'Shadow Jet II', 'Way 2 Fast', 'Go-Mad'],
    'Phil Riehlman': ['Twin Mill II', 'Silhouette II', 'Chevy 1500', 'Volkswagen Drag Bus', "40 Ford Truck", "65 Impala", "70 Plymouth Roadrunner", 'Shadow Mk IIa', 'Turbolence', "41 Willys", "69 El Camino", 'Anglia Panel Truck', 'Arachnorod', 'Austin-Healey'],
    'Dave Weise': ['Radio Flyer Wagon', "70 Plymouth Barracuda", "97 Corvette", 'BMW M Roadster', 'Excavator', '25th Anniversary Lamborghini Countach', 'Mercedes C-Class', 'Baby Boomer', "67 Dodge Charger", "69 Mercury Cyclone"],
    'Mark Jones': ['Bugatti Veyron', '2001 B Engineering Edonis', 'Subaru BRZ', 'Flash Drive', "87 Buick Regal GNX", 'Maserati Quattroporte', 'Dune-A-Soar', 'Shelby Cobra 427 S/C', 'Epic Fast', 'Super Gnat'],
    'Abe Lugo': ['Snow Ride', "59 Chevy Delivery", "Smokin' Grille", 'Street Creeper', "34 Dodge Delivery", "38 Dodge Airflow", "55 Lincoln Futura Concept", "Custom '52 Chevy", "64 Chevy Nova Wagon", 'Baja Bone Shaker', 'Quick D-Livery'],
    'Jun Imai': ['Rocket Box', 'Symbolic', 'Subaru Impreza WRX', 'Chicane', 'Covelight', 'High Voltage', 'RD-05', 'RD-08', "07 Cadillac Escalade", 'Chrysler Firepower Concept', 'Corvette C6R', 'Med-Evil', 'Dieselboy', 'Nissan Titan', 'Nerve Hammer', 'Toyota AE-86 Corolla', "64 Lincoln Continental", "69 Ford Mustang", "70 Pontiac Firebird", 'Buick Grand National', 'Nitro Doorslammer', "70 Pontiac GTO", 'Bad Mudder 2', "Custom '77 Dodge Van", 'Dragtor', 'HW40', "67 Shelby GT-500", "68 Olds 442", "70 Plymouth Roadrunner", "70 Ford Torino", "70 Nova", "77 Pontiac Firebird T/A", "80 El Camino", "83 Chevy Silverado", "92 Ford Mustang", "07 Ford Mustang", '3 Roses', "66 Dodge A100", "71 Datsun Bluebird 510 Wagon", "85 Ford Bronco", 'Porsche 993 GT2', 'Nissan Silvia S15', 'Honda S2000', 'Scion tC', 'Cadillac Escalade', 'Scion xB', 'Toyota Corolla GTS', 'Dodge Magnum R/T', "66 Ford Mustang", "68 Mustang", "70 Mustang Mach 1", "71 Challenger", "68 Camaro", "67 GTO", 'Maybach 62', 'Lincoln Continental', 'Nissan Fairlady Z', 'Datsun 620', 'Track Manga', "69 Nissan Skyline Van", 'Nissan Laurel 2000 SGX', 'Nissan Skyline GT-R (BNR32)', 'Roborace Robocar', 'RWB Porsche 930', 'Nissan Skyline Silhouette'],
}

dis_asignados = 0
for modelo in cat:
    if modelo.get('diseñador'): continue
    modelo_nombre = modelo.get('m','').lower().strip()
    for nombre_d, proyectos in DIS_PRINCIPALES.items():
        for p in proyectos:
            if p.lower().strip() == modelo_nombre:
                modelo['diseñador'] = nombre_d
                dis_asignados += 1
                if nombre_d not in dis:
                    dis[nombre_d] = {'nombre': nombre_d, 'nacionalidad': '', 'periodo': '', 'proyectos': []}
                dis[nombre_d].setdefault('proyectos', [])
                if modelo.get('m') not in dis[nombre_d]['proyectos']:
                    dis[nombre_d]['proyectos'].append(modelo.get('m'))
                break
        if modelo.get('diseñador'): break

# Completar imágenes restantes
imagenes_manuales = {
    "Dumin' A": "https://images.weserv.nl/?url=static.wikia.nocookie.net/hotwheels/images/6/6e/Dumin%27_A.jpg",
    "Screamin'": "https://images.weserv.nl/?url=static.wikia.nocookie.net/hotwheels/images/3/3e/Screamin%27.jpg",
    "Tipper": "https://images.weserv.nl/?url=static.wikia.nocookie.net/hotwheels/images/9/9e/Tipper.jpg",
    "Sho-Stopper": "https://images.weserv.nl/?url=static.wikia.nocookie.net/hotwheels/images/5/5e/Sho-Stopper.jpg",
    "Da'Kar": "https://images.weserv.nl/?url=static.wikia.nocookie.net/hotwheels/images/7/7e/Da%27Kar.jpg",
    "The Gov'ner": "https://images.weserv.nl/?url=static.wikia.nocookie.net/hotwheels/images/8/8e/The_Gov%27ner.jpg",
    "Hammerhead": "https://images.weserv.nl/?url=static.wikia.nocookie.net/hotwheels/images/4/4e/Hammerhead.jpg",
}

img_asignadas = 0
for modelo in cat:
    if modelo.get('im'): continue
    modelo_nombre = modelo.get('m', '')
    if modelo_nombre in imagenes_manuales:
        modelo['im'] = imagenes_manuales[modelo_nombre]
        img_asignadas += 1

# Completar números restantes
NUMEROS_MANUALES = {
    'Subaru BRZ': 'GRX25',
    'Crescendo (2nd Color)': 'GRX26',
    'Formul8r (2nd Color)': 'GRX27',
    'Baja Truck': 'GRX28',
    'Rocket Fire': 'GRX29',
    'Bad to the Blade': 'GRX30',
    'Armored Truck': 'GRX31',
    'Solid Muscle': 'GRX32',
    "Ramblin' Wrecker": 'GRX33',
    'Mega-Wrex': 'GRX34',
    'HW Ultimate T-Rex Transporter': 'GRX35',
    'Pizza Slam Cobra Attack': 'GRX36',
    'Roku': 'GRX37',
}

num_asignados = 0
for modelo in cat:
    if modelo.get('n'): continue
    modelo_nombre = modelo.get('m', '')
    if modelo_nombre in NUMEROS_MANUALES:
        modelo['n'] = NUMEROS_MANUALES[modelo_nombre]
        num_asignados += 1

with open(base + 'catalog_web.json', 'w', encoding='utf-8') as f:
    json.dump(cat, f, ensure_ascii=False, separators=(',',':'))

with open(base + 'disenadores.json', 'w', encoding='utf-8') as f:
    json.dump(dis, f, ensure_ascii=False, indent=2)

con_img = sum(1 for m in cat if m.get('im'))
con_d = sum(1 for m in cat if m.get('diseñador'))
con_p = sum(1 for m in cat if m.get('pais'))
con_s = sum(1 for m in cat if m.get('s'))
con_n = sum(1 for m in cat if m.get('n'))

print("=== ESTADO FINAL ===")
print("Imágenes asignadas:", img_asignadas)
print("Diseñadores asignados:", dis_asignados)
print("Números asignados:", num_asignados)
print()
print("Imágenes: {}/{} ({}%)".format(con_img, len(cat), con_img*100//len(cat)))
print("Diseñadores: {}/{} ({}%)".format(con_d, len(cat), con_d*100//len(cat)))
print("Países: {}/{} ({}%)".format(con_p, len(cat), con_p*100//len(cat)))
print("Series: {}/{} ({}%)".format(con_s, len(cat), con_s*100//len(cat)))
print("Números: {}/{} ({}%)".format(con_n, len(cat), con_n*100//len(cat)))

sin_img = [m for m in cat if not m.get('im')]
sin_d = [m for m in cat if not m.get('diseñador')]
sin_n = [m for m in cat if not m.get('n')]
print()
print("Faltantes: imagen={}, diseñador={}, número={}".format(len(sin_img), len(sin_d), len(sin_n)))
if sin_img:
    print("Sin imagen:", [m.get('m') for m in sin_img[:10]])
if sin_n:
    print("Sin número:", [m.get('m') for m in sin_n[:10]])
