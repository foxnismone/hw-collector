import json

# Categorías de coleka.com (colecciones temáticas)
CATEGORIAS_COLEKA = [
    {"id": "spider_man", "nombre": "Spider-Man", "año": "2022-2026", "modelos": 10, "tipo": "personajes"},
    {"id": "pull_back", "nombre": "Pull-Back Speeders", "año": "2024-2025", "modelos": 2, "tipo": "linea"},
    {"id": "clasicos", "nombre": "Clásicos", "año": "1976-2026", "modelos": 4189, "tipo": "linea"},
    {"id": "rlc", "nombre": "Collectors / RLC & NFT Garage", "año": "2024-2025", "modelos": 23, "tipo": "club"},
    {"id": "x_men", "nombre": "X-Men", "año": "2023", "modelos": 5, "tipo": "personajes"},
    {"id": "cool_classics", "nombre": "Cool Classics", "año": "2014", "modelos": 7, "tipo": "linea"},
    {"id": "daniel_arsham", "nombre": "Daniel Arsham", "año": "2023-2024", "modelos": 8, "tipo": "colaboracion"},
    {"id": "acceleracers", "nombre": "Acceleracers", "año": "", "modelos": 22, "tipo": "serie"},
    {"id": "action_pack", "nombre": "Action Pack", "año": "", "modelos": 7, "tipo": "serie"},
    {"id": "split_speeders", "nombre": "Split Speeders", "año": "", "modelos": 4, "tipo": "serie"},
    {"id": "racerverse", "nombre": "Racerverse", "año": "2023-2025", "modelos": 39, "tipo": "serie"},
    {"id": "captain_marvel", "nombre": "Captain Marvel", "año": "2023", "modelos": 2, "tipo": "personajes"},
    {"id": "black_panther", "nombre": "Black Panther", "año": "2022", "modelos": 3, "tipo": "personajes"},
    {"id": "car_tridge", "nombre": "Car-tridge", "año": "", "modelos": 5, "tipo": "serie"},
    {"id": "racing", "nombre": "Racing", "año": "2003", "modelos": 29, "tipo": "serie"},
    {"id": "racing_metal", "nombre": "Racing Metal Series", "año": "1995", "modelos": 4, "tipo": "serie"},
    {"id": "mainline_themed", "nombre": "Mainline Themed Collections", "año": "2018-2025", "modelos": 217, "tipo": "serie"},
    {"id": "track_fleet", "nombre": "Track Fleet", "año": "2024-2025", "modelos": 2, "tipo": "serie"},
    {"id": "garage", "nombre": "Garage", "año": "2011", "modelos": 15, "tipo": "serie"},
    {"id": "fast_food", "nombre": "Fast Food Series", "año": "1996", "modelos": 4, "tipo": "serie"},
    {"id": "detroit_muscle", "nombre": "Detroit Muscle", "año": "2019", "modelos": 6, "tipo": "serie"},
    {"id": "despicable_me", "nombre": "Despicable Me", "año": "2017", "modelos": 6, "tipo": "personajes"},
    {"id": "spring_19", "nombre": "Spring '19", "año": "2019", "modelos": 6, "tipo": "serie"},
    {"id": "holiday_hot_rod", "nombre": "Holiday Hot Rod", "año": "2019", "modelos": 6, "tipo": "serie"},
    {"id": "porsche", "nombre": "Porsche", "año": "2019-2020", "modelos": 5, "tipo": "serie"},
    {"id": "hw_turbo", "nombre": "HW Turbo", "año": "2020", "modelos": 6, "tipo": "serie"},
    {"id": "tooned", "nombre": "Tooned", "año": "2020", "modelos": 10, "tipo": "serie"},
    {"id": "mario_kart", "nombre": "Mario Kart", "año": "2019-2025", "modelos": 112, "tipo": "colaboracion"},
    {"id": "marvel", "nombre": "Marvel", "año": "2015-2021", "modelos": 30, "tipo": "personajes"},
    {"id": "star_trek", "nombre": "Star Trek 50", "año": "2015-2016", "modelos": 6, "tipo": "colaboracion"},
]

# Guía de identificación de códigos
GUIA_CODIGOS = {
    "titulo": "Guía de Identificación de Códigos Hot Wheels",
    "secciones": [
        {
            "nombre": "Código de Asortación (Case Assortment)",
            "descripcion": "Código que identifica la caja/case de 72 autos",
            "formato": "3-4 letras + 4 números",
            "ejemplos": ["L2593", "C4982", "5785"],
            "donde_aparece": "En el lateral de la caja, código de barras"
        },
        {
            "nombre": "Código de Modelo/Tool Number",
            "descripcion": "Código único del modelo (casting)",
            "formato": "3 letras + 2 números",
            "ejemplos": ["FRN78", "JKX06", "JJJ02"],
            "donde_aparece": "En la base del auto, junto al número de serie"
        },
        {
            "nombre": "Número de Serie (Toy Number)",
            "descripcion": "Número de producción del modelo",
            "formato": "4-5 números",
            "ejemplos": ["6451", "56388", "2020"],
            "donde_aparece": "En la base del auto, grabado o impreso"
        },
        {
            "nombre": "Código de Country (País de Manufactura)",
            "descripcion": "Código que indica dónde fue fabricado",
            "formato": "Texto",
            "ejemplos": ["USA", "Hong Kong", "Malaysia", "Thailand", "China", "Mexico"],
            "donde_aparece": "En la base del auto, junto al tool number"
        },
        {
            "nombre": "Código de Color",
            "descripcion": "Algunas variantes tienen código de color",
            "formato": "1-2 letras + 1-2 números",
            "ejemplos": ["C10", "G37", "A52"],
            "donde_aparece": "En la base del auto, código de color"
        },
        {
            "nombre": "Código de Ruedas (Wheel Type)",
            "descripcion": "Tipo de ruedas del modelo",
            "formato": "Abreviatura",
            "ejemplos": ["RL (Redline)", "BW (Butterfly Wheels)", "5SP (5 Spoke)", "RR (Real Riders)", "DD8 (Deep Dish)"],
            "donde_aparece": "En la base del auto, indica el tipo de ruedas"
        },
        {
            "nombre": "Código de Base (Base Type)",
            "descripcion": "Tipo de base (chasis)",
            "formato": "Texto",
            "ejemplos": ["Metal", "Plastic", "ZAMAC"],
            "donde_aparece": "En la base del auto, material del chasis"
        }
    ]
}

# Anatomía de la caja
ANATOMIA_CAJA = {
    "titulo": "Anatomía de la Caja Hot Wheels",
    "partes": [
        {"nombre": "Frontal", "elementos": ["Logo Hot Wheels", "Imagen del auto", "Nombre del modelo", "Número de serie", "Edad recomendada"]},
        {"nombre": "Lateral izquierdo", "elementos": ["Código de asortación", "Código de barras", "Precio", "País de origen"]},
        {"nombre": "Lateral derecho", "elementos": ["Código de asortación", "Lista de autos del case", "Información de seguridad"]},
        {"nombre": "Superior", "elementos": ["Logo Hot Wheels", "Tipo (Mainline/TH/STH)", "Año de producción"]},
        {"nombre": "Inferior", "elementos": ["Código de asortación", "Dirección del fabricante", "Código de reciclaje"]},
        {"nombre": "Interior (blister)", "elementos": ["El auto en sí", "Tarjeta de colección (TH/STH)", "Sticker sheet (algunos modelos)"]}
    ]
}

# Guardar datos
with open('data/categorias_coleka.json', 'w', encoding='utf-8') as f:
    json.dump(CATEGORIAS_COLEKA, f, ensure_ascii=False, indent=2)

with open('data/guia_codigos.json', 'w', encoding='utf-8') as f:
    json.dump(GUIA_CODIGOS, f, ensure_ascii=False, indent=2)

with open('data/anatomia_caja.json', 'w', encoding='utf-8') as f:
    json.dump(ANATOMIA_CAJA, f, ensure_ascii=False, indent=2)

print("✅ Datos de coleka.com y 164custom.com integrados")
print(f"   - {len(CATEGORIAS_COLEKA)} categorías temáticas")
print(f"   - {len(GUIA_CODIGOS['secciones'])} secciones de guía de códigos")
print(f"   - {len(ANATOMIA_CAJA['partes'])} partes de anatomía de caja")
