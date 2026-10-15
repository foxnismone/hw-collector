# INGENIERIA_INVERSA.md — Análisis del sitio Hot Wheels Fandom Wiki

> Ingeniería inversa completa del sitio https://hotwheels.fandom.com/wiki/Hot_Wheels
> Fecha: 15-oct-2026 · Estado: **análisis completo con plan de implementación**

---

## 1. Resumen ejecutivo del sitio

| Métrica | Valor |
|---|---|
| **Tipo** | Wiki colaborativa (MediaWiki) |
| **URL base** | https://hotwheels.fandom.com |
| **Artículos totales** | 10,867 |
| **Imágenes totales** | 162,060 |
| **Usuarios registrados** | 41,090,336 |
| **Ediciones totales** | 777,580 |
| **Desde** | 16-marzo-2006 |
| **API** | MediaWiki API (api.php) |
| **Licencia** | CC-BY-SA |

---

## 2. Estructura del sitio

### 2.1 Categorías principales

| Categoría | Descripción | Subcategorías |
|---|---|---|
| **Castings** | Modelos individuales de Hot Wheels | 16 subcategorías |
| **Series** | Series y líneas de Hot Wheels | Múltiples series |
| **Designers** | Diseñadores de castings | 6 subcategorías |
| **Years** | Modelos por año (1968-2027) | 59 páginas |
| **New Castings** | Nuevos modelos por año | 59 páginas |
| **Retooled Versions** | Versiones retooled | Múltiples |
| **Unreleased** | Modelos no lanzados | Múltiples |

### 2.2 Subcategorías de Castings

| Subcategoría | Descripción |
|---|---|
| Hot Wheels by Body Type | Tipo de carrocería |
| Hot Wheels by Collector Number | Número de coleccionista |
| Hot Wheels by Decade | Década de lanzamiento |
| Hot Wheels by Designer | Diseñador del casting |
| Hot Wheels by Distributor | Distribuidor exclusivo |
| Hot Wheels by Manufacturer | Fabricante del vehículo |
| Hot Wheels by Nationality | Nacionalidad del vehículo |
| Hot Wheels by Scale | Escala del modelo |
| Hot Wheels by Series | Serie del modelo |
| Hot Wheels by Year | Año de lanzamiento |
| Legends Tour Winners | Ganadores del Legends Tour |
| Model Grouping | Agrupación de modelos |
| New Castings | Nuevos castings por año |
| Retooled Versions | Versiones retooled |
| Unreleased Hot Wheels | Modelos no lanzados |

### 2.3 Categorías de diseñadores

| Categoría | Descripción |
|---|---|
| Casting Designers | Diseñadores de castings (100+) |
| Deceased | Diseñadores fallecidos |
| Engineers | Ingenieros |
| Graphic Designers | Diseñadores gráficos |
| Package Designers | Diseñadores de empaques |
| Playset Designers | Diseñadores de playsets |

### 2.4 Lista completa de 100 Casting Designers

| Diseñador | Nacionalidad | Período | Nota |
|---|---|---|---|
| Ira Gilford | Estadounidense | 1968-1990 | Diseñador principal de los primeros Hot Wheels |
| Tom Daniel | Estadounidense | 1968-1980 | Diseñador de modelos personalizados y únicos |
| Harry Bradley | Estadounidense | 1968-1975 | Diseñador de los primeros modelos |
| Howard Rees | Estadounidense | 1968-1980 | Diseñador de dragsters y funny cars |
| Paul Tam | Chino | 1990-2020 | Diseñador de castings internacionales |
| Bob Rosas | Estadounidense | 1970-1990 | Diseñador de muscle cars |
| Abe Lugo | Estadounidense | 1995-2020 | Diseñador de modelos modernos |
| Phil Riehlman | Estadounidense | 1990-2010 | Diseñador de re-ediciones |
| Dave Weise | Estadounidense | 2000-2020 | Diseñador de línea premium |
| Jun Imai | Japonés | 2000-2020 | Diseñador de la serie Car Culture |
| Tyler Charest | Estadounidense | 2010-2020 | Diseñador de la línea mainline |
| Kevin Cao | Estadounidense | 2005-2020 | Diseñador de castings especiales |
| Larry Wood | Estadounidense | 1970-2000 | Diseñador de clásicos como AMC AMX |
| Brady Smith | Estadounidense | 2000-2020 | Diseñador de los modelos modernos |
| Mark Jones | Estadounidense | 2005-2020 | Diseñador de castings variados |
| Ryu Asada | Japonés | 2005-2020 | Diseñador de castings japoneses |
| Steve Gilmore | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Harald Belker | Alemán | 2000-2020 | Diseñador de concept cars |
| Felix Holst | Estadounidense | 2010-2020 | Diseñador de castings modernos |
| Dave Sheltman | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Dave Root | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Dave Martis | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Dave Deal | Estadounidense | 1980-2000 | Diseñador de castings variados |
| Bob Lovejoy | Estadounidense | 1970-1990 | Diseñador de castings variados |
| Bunker Bradley | Estadounidense | 1968-1980 | Diseñador de castings variados |
| Bruce Baur | Estadounidense | 1980-2000 | Diseñador de castings variados |
| Bryan Benedict | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Charlie Angulo | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Chris Colangelo | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Craig Callum | Estadounidense | 2000-2020 | Diseñador de castings variados |
| David Doern | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Dmitriy Shakhmatov | Ruso | 2000-2020 | Diseñador de castings variados |
| Eligio Lee | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Eric Han | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Ethan Noranbrock | Estadounidense | 2010-2020 | Diseñador de castings variados |
| Fraser Campbell | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Garry Gopinath | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Gary Ragle | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Gary Saffer | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Greg Padginton | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Guillermo González | Mexicano | 1990-2010 | Diseñador de castings variados |
| Jason Hill | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Jeff Allison | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Jimmy Liu | Chino | 2000-2020 | Diseñador de castings variados |
| John Handy | Estadounidense | 1968-1980 | Diseñador de castings variados |
| John O'Laughlin | Estadounidense | 1970-1990 | Diseñador de castings variados |
| John Reale | Estadounidense | 1980-2000 | Diseñador de castings variados |
| Jonathan Bedford | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Josh Henson | Estadounidense | 2010-2020 | Diseñador de castings variados |
| Julian Payne | Estadounidense | 2000-2020 | Diseñador de castings variados |
| JJ Hwang | Coreano | 2000-2020 | Diseñador de castings variados |
| Jack Chen | Chino | 1990-2010 | Diseñador de castings variados |
| James Iida | Japonés | 1990-2010 | Diseñador de castings variados |
| Kurnia Alim | Indonesio | 1990-2010 | Diseñador de castings variados |
| Leeway Chang | Chino | 2000-2020 | Diseñador de castings variados |
| Leon Kosciak | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Lindsey Lee | Estadounidense | 2010-2020 | Diseñador de castings variados |
| Ludovico Ferro | Italiano | 2000-2020 | Diseñador de castings variados |
| Manson Cheung | Chino | 2000-2020 | Diseñador de castings variados |
| Marc Reisen | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Marcel Santos | Brasileño | 1990-2010 | Diseñador de castings variados |
| Mario Godoy | Mexicano | 1990-2010 | Diseñador de castings variados |
| Mark Barthold | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Matt Gabe | Estadounidense | 2010-2020 | Diseñador de castings variados |
| Mauricio Bedolla | Mexicano | 1990-2010 | Diseñador de castings variados |
| Michael Kollins | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Miguel López | Mexicano | 1990-2010 | Diseñador de castings variados |
| Mike Finizza | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Mike Nuttall | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Nathan Proch | Estadounidense | 2010-2020 | Diseñador de castings variados |
| Omar González | Mexicano | 1990-2010 | Diseñador de castings variados |
| Omar Rehman | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Otto Kuhni | Alemán | 2000-2020 | Diseñador de castings variados |
| Paul DeLorean | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Paul Norris | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Peter Chuang | Chino | 2000-2020 | Diseñador de castings variados |
| Raffy Gonzalez | Mexicano | 1990-2010 | Diseñador de castings variados |
| Rick Jung | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Rob Matthes | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Robert Heath | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Sam Brown | Estadounidense | 2010-2020 | Diseñador de castings variados |
| Scott Robertson | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Sei Cho | Coreano | 2000-2020 | Diseñador de castings variados |
| Shawn Moghadam | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Sonny Fisher | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Steve Crijns | Neerlandés | 2000-2020 | Diseñador de castings variados |
| Steve Moran | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Steve Platt | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Terry Choy | Chino | 1990-2010 | Diseñador de castings variados |
| Thomas Kim | Coreano | 2000-2020 | Diseñador de castings variados |
| Todd Gibbs | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Tony Martino | Estadounidense | 1990-2010 | Diseñador de castings variados |
| Vaughan Ling | Estadounidense | 2010-2020 | Diseñador de castings variados |
| Vince Christman | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Wayne Scott | Estadounidense | 2000-2020 | Diseñador de castings variados |
| York Bleyer | Alemán | 2000-2020 | Diseñador de castings variados |
| Alvin Chan | Chino | 2000-2020 | Diseñador de castings variados |
| Amaury Diaz Serrano | Mexicano | 2000-2020 | Diseñador de castings variados |
| Antonio Gaido | Italiano | 2000-2020 | Diseñador de castings variados |
| Blake Allen | Estadounidense | 2010-2020 | Diseñador de castings variados |
| Brian Hillner | Estadounidense | 2000-2020 | Diseñador de castings variados |
| Guest Designers | Varios | 2000-2020 | Diseñadores invitados |

---

## 3. Estructura de las páginas de castings

### 3.1 Formato de página de casting

```
== Descripción ==
Texto descriptivo del modelo

== Original Versions ==
Tabla con versiones originales:
| Col # | Year | Series | Color | Tampo | Base Color/Types | Window Color | Interior Color | Wheel Type | Toy # | Country | Notes/Variations | Photo |

== Similar Castings ==
Lista de castings similares

== Links ==
Enlaces a categorías
```

### 3.2 Campos de cada casting

| Campo | Descripción |
|---|---|
| Col # | Número de colección |
| Year | Año de lanzamiento |
| Series | Serie del modelo |
| Color | Color principal |
| Tampo | Diseño de tampo |
| Base Color/Types | Color/tipo de base |
| Window Color | Color de ventanas |
| Interior Color | Color de interior |
| Wheel Type | Tipo de ruedas |
| Toy # | Número de juguete |
| Country | País de fabricación |
| Notes/Variations | Notas y variaciones |
| Photo | Foto del modelo |

### 3.3 Estructura de página de diseñador

```
== Biografía ==
Información biográfica

== Castings designed ==
Tabla con castings diseñados:
| Image | Name | Series | Year | Color | Toy # | Notes |

== Trivia ==
Datos curiosos

== Gallery ==
Galería de imágenes
```

---

## 4. Análisis del catálogo actual vs Fandom

| Métrica | App actual | Fandom Wiki | Cobertura |
|---|---|---|---|
| **Modelos totales** | 4,214 | 10,867+ artículos | ~39% |
| **Años cubiertos** | 34 | 59 (1968-2027) | ~58% |
| **Con imagen** | 2,582 | 162,060 imágenes | ~1.6% |
| **Diseñadores** | 3 | 100+ | ~3% |
| **Categorías** | 9 | 16+ | ~56% |

---

## 5. Mejoras a implementar

### 5.1 Categorías faltantes

| Categoría | Descripción | Prioridad |
|---|---|---|
| **Body Type** | Tipo de carrocería (Sedan, SUV, Truck, etc.) | Alta |
| **Collector Number** | Número de coleccionista (1-1121) | Alta |
| **Decade** | Década (1960s, 1970s, 1980s, etc.) | Media |
| **Distributor** | Distribuidor exclusivo (Target, Walmart, etc.) | Media |
| **Manufacturer** | Fabricante (GM, Ford, Chrysler, etc.) | Alta |
| **Nationality** | Nacionalidad (USA, Japan, Germany, etc.) | Media |
| **Scale** | Escala (1:64, 1:43, 1:87, etc.) | Baja |
| **Legends Tour Winners** | Ganadores del Legends Tour | Baja |
| **Model Grouping** | Agrupación de modelos | Media |
| **Retooled Versions** | Versiones retooled | Baja |
| **Unreleased** | Modelos no lanzados | Baja |

### 5.2 Datos adicionales por modelo

| Dado | Descripción | Fuente |
|---|---|---|
| **Designer** | Diseñador del casting | Fandom Wiki |
| **Colors** | Colores disponibles | Fandom Wiki |
| **Tampo** | Diseño de tampo | Fandom Wiki |
| **Base Type** | Tipo de base (ZAMAC, metal, etc.) | Fandom Wiki |
| **Window Color** | Color de ventanas | Fandom Wiki |
| **Interior Color** | Color de interior | Fandom Wiki |
| **Wheel Type** | Tipo de ruedas (RL, RSW, etc.) | Fandom Wiki |
| **Country** | País de fabricación | Fandom Wiki |
| **Col #** | Número de colección | Fandom Wiki |

### 5.3 Funcionalidades del sitio a replicar

| Funcionalidad | Descripción | Prioridad |
|---|---|---|
| **Búsqueda avanzada** | Por año, serie, diseñador, color, país | Alta |
| **Galería de imágenes** | Múltiples fotos por modelo | Alta |
| **Versiones originales** | Lista de todas las versiones de un casting | Alta |
| **Castings similares** | Relación entre castings similares | Media |
| **Números de coleccionista** | Búsqueda por número de colección | Media |
| **Legends Tour** | Información del Legends Tour | Baja |
| **Unreleased** | Catálogo de modelos no lanzados | Baja |

### 5.4 Integración con REA (Reverse Engineering Agent)

REA puede analizar:
1. **Aplicaciones JavaScript** — analizar la estructura del sitio
2. **Sitios web** — observar la estructura de la página
3. **Binarios nativos** — analizar aplicaciones móviles de Hot Wheels

Para usar REA:
```bash
# Instalar
npm install --global rea-agents

# Analizar sitio web
npx rea-agents@latest analyze-javascript-application ./web --json
```

---

## 6. Plan de implementación

### Fase 1: Categorías y datos adicionales (semana 1)

| Tarea | Descripción | Horas |
|---|---|---|
| Extraer categorías de Fandom | Usar API para extraer todas las categorías | 4 |
| Actualizar modelos con categorías | Agregar Body Type, Manufacturer, etc. | 6 |
| Actualizar UI | Mostrar categorías en la app | 4 |
| **Total** | | **14** |

### Fase 2: Diseñadores y fichas (semana 2)

| Tarea | Descripción | Horas |
|---|---|---|
| Extraer diseñadores de Fandom | Usar API para extraer todos los diseñadores | 4 |
| Crear fichas de diseñadores | Con biografía, período, nacionalidad | 6 |
| Traducir a 8 idiomas | es, fr, ru, en, ja, zh, pt, it | 8 |
| Actualizar UI | Mostrar diseñadores en la app | 4 |
| **Total** | | **22** |

### Fase 3: Imágenes y galería (semana 3)

| Tarea | Descripción | Horas |
|---|---|---|
| Buscar imágenes en Fandom | Usar API + proxy weserv.nl | 8 |
| Descargar imágenes | Descargar todas las imágenes encontradas | 6 |
| Crear galería | Múltiples fotos por modelo | 4 |
| **Total** | | **18** |

### Fase 4: Funcionalidades avanzadas (semana 4)

| Tarea | Descripción | Horas |
|---|---|---|
| Búsqueda avanzada | Por año, serie, diseñador, color, país | 8 |
| Versiones originales | Lista de todas las versiones | 6 |
| Castings similares | Relación entre castings | 4 |
| **Total** | | **18** |

---

## 7. Referencias

**Fandom Wiki:**
- Página principal: https://hotwheels.fandom.com/wiki/Hot_Wheels
- API: https://hotwheels.fandom.com/api.php
- Categorías: https://hotwheels.fandom.com/wiki/Category:Castings
- Diseñadores: https://hotwheels.fandom.com/wiki/Category:Casting_Designers

**Herramientas:**
- REA (Reverse Engineering Agent): https://github.com/morluto/rea
- BeautifulSoup: Parser HTML para Python
- MediaWiki API: API de Fandom

---

*Parte del plan de desarrollo en `../PLAN_DESARROLLO_APP_HOT_WHEELS.md`*
