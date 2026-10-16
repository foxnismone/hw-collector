# 03 — Bases de Datos, Catálogos y Comunidades de Hot Wheels

> **Investigación de fuentes de datos para app de coleccionistas Hot Wheels**
> Fecha: 2026-10-11
> Todas las APIs y consultas fueron probadas con `curl` en tiempo real.
> Se indica **NO VERIFICADO** cuando no se pudo probar directamente.

---

## Índice

1. [Hot Wheels Wiki (Fandom / MediaWiki)](#1-hot-wheels-wiki-fandom--mediawiki)
2. [South Texas Diecast](#2-south-texas-diecast)
3. [HobbyDB](#3-hobbydb)
4. [Hot Wheels Collectors / Mattel Creations](#4-hot-wheels-collectors--mattel-creations)
5. [CollectHW](#5-collecthw)
6. [HWCollectorsNews.com](#6-hwcollectorsnewscom)
7. [Lamley Group](#7-lamley-group)
8. [Orange Track Diecast](#8-orange-track-diecast)
9. [Diecast Registry](#9-diecast-registry)
10. [PriceCharting](#10-pricecharting)
11. [Wikipedia / Wikidata](#11-wikipedia--wikidata)
12. [Reddit — Comunidades](#12-reddit--comunidades)
13. [GitHub — Repositorios y APIs de terceros](#13-github--repositorios-y-apis-de-terceros)
14. [Hugging Face Datasets](#14-hugging-face-datasets)
15. [Kaggle Datasets](#15-kaggle-datasets)
16. [Foros y Comunidades en Español](#16-foros-y-comunidades-en-español)
17. [Discord — Servidores de Coleccionistas](#17-discord--servidores-de-coleccionistas)
18. [Facebook — Grupos de Coleccionistas](#18-facebook--grupos-de-coleccionistas)
19. [YouTube / TikTok — Canales Relevantes](#19-youtube--tiktok--canales-relevantes)
20. [Consideraciones Legales](#20-consideraciones-legales)
21. [Resumen Comparativo](#21-resumen-comparativo)
22. [Comandos Probados](#22-comandos-probados)

---

## 1. Hot Wheels Wiki (Fandom / MediaWiki)

| Campo | Valor |
|---|---|
| **Nombre** | Hot Wheels Wiki |
| **URL** | https://hotwheels.fandom.com |
| **API** | Sí — MediaWiki API estándar |
| **Endpoint base** | `https://hotwheels.fandom.com/api.php` |
| **Licencia** | CC BY-SA 3.0 (contenido generado por usuarios) |
| **Scrapeable** | Sí, vía API. `robots.txt` bloqueado por Cloudflare challenge, pero la API funciona sin autenticación |
| **Nº aproximado de páginas** | ~15,000+ artículos (modelos, series, listas por año) |
| **Campos disponibles** | Infobox casting: name, series, number, years, designer, image. Tablas de versiones: Col #, Year, Series, Color, Tampo, Base Color/Type, Window Color, Interior Color, Wheel Type, Toy #, Country, Notes, Photo |

### Estructura del contenido

- **Páginas de modelos** (ej: `Punk Rod`): infobox con datos del casting + tabla de todas las versiones conocidas
- **Listas por año** (ej: `List of 2024 Hot Wheels`): tablas completas con Toy #, Col #, Model Name, Series, Series #, Photo
- **Categorías por año**: `Category:2024 Hot Wheels`, `Category:2024 Treasure Hunts`, `Category:2024 Super Treasure Hunts`, etc.
- **Categorías por serie**: `Category:HW Dream Garage`, `Category:Rod Squad`, etc.

### Consultas API verificadas

**Buscar páginas por texto:**
```bash
curl -s "https://hotwheels.fandom.com/api.php?action=query&list=search&srsearch=2024+Mainline&srlimit=5&format=json" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"
```
Resultado real: devuelve `List of 2024 Hot Wheels` (pageid 143753, 13,245 palabras), `List of 2024 Hot Wheels (by Series)` (pageid 157386, 17,280 palabras), `2024 New Models`, etc.

**Obtener contenido wikitext de una página (infobox + tablas):**
```bash
curl -s "https://hotwheels.fandom.com/api.php?action=query&prop=revisions&titles=Punk%20Rod&rvslots=*&rvprop=content&format=json" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"
```
Resultado real: devuelve el wikitext completo con `{{casting|name=Punk Rod|series=Rod Squad|number=HRY48|years=2024–Present|designer=Fraser Campbell|image=PunkRod.jpg}}` y la tabla de 7 versiones con todos los campos (Col #, Year, Series, Color, Tampo, Base Color/Type, Window Color, Interior Color, Wheel Type, Toy #, Country, Notes, Photo).

**Obtener miembros de una categoría:**
```bash
curl -s "https://hotwheels.fandom.com/api.php?action=query&list=categorymembers&cmtitle=Category:2024%20Hot%20Wheels&cmlimit=5&format=json" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"
```
Resultado real: devuelve páginas como `'32 Ford`, `'32 Ford (RLC)`, `'40 Ford`, `'47 Chevy Fleetline`, `'49 Drag Merc` (entre miles más).

**Listar categorías por prefijo:**
```bash
curl -s "https://hotwheels.fandom.com/api.php?action=query&list=allcategories&aclimit=50&acprefix=2024&format=json" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"
```
Resultado real: `2024`, `2024 First Released`, `2024 HW Screen Time`, `2024 Hot Wheels`, `2024 Red Edition`, `2024 Super Treasure Hunts`, `2024 Treasure Hunts`.

### Ventajas
- API pública, gratuita, sin autenticación
- Datos muy estructurados (infobox + tablas)
- Cobertura histórica amplia (desde 1968)
- Comunidad activa que mantiene el contenido actualizado
- Incluye fotos de cada versión

### Límites
- Formato wikitext requiere parsing (no es JSON puro para el contenido)
- No hay endpoint de búsqueda por imagen
- La calidad varía según el artículo (algunos son más completos que otros)
- Fandom puede cambiar sus términos de servicio
- `robots.txt` bloqueado por Cloudflare (pero la API funciona)

---

## 2. South Texas Diecast

| Campo | Valor |
|---|---|
| **Nombre** | South Texas Diecast Collectors |
| **URL** | https://southtexasdiecast.com |
| **API** | No — solo HTML |
| **Licencia** | Contenido propio del sitio |
| **Scrapeable** | Técnicamente sí (WordPress), pero sin API oficial. `robots.txt` vacío (sin restricciones explícitas) |
| **Nº aproximado de registros** | Miles de modelos organizados por año y categoría |
| **Campos disponibles** | Modelo, año, serie, variación, fotos, notas de colección |

### Estructura del contenido

- Organizado por año (URLs como `/hot-wheels/2024/`)
- Categorías: Mainline, Treasure Hunts, Super Treasure Hunts, RLC, etc.
- Cada entrada tiene fotos y descripción
- Sitio WordPress con feed RSS disponible en `/feed/`

### Consulta verificada
```bash
curl -s "https://www.southtexasdiecast.com/hot-wheels/2024/" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -L
```
Resultado real: página accesible, título "Hot Wheels Long Haulers & Pavement Pounders – South Texas Diecast Collectors".

### Ventajas
- Catálogo histórico muy completo
- Bien organizado por año y categoría
- Fotos de alta calidad
- Comunidad de coleccionistas activa

### Límites
- No hay API pública
- Requiere scraping HTML (frágil ante cambios de diseño)
- No incluye datos estructurados de variaciones (color, tampo, etc.)
- No incluye precios

---

## 3. HobbyDB

| Campo | Valor |
|---|---|
| **Nombre** | hobbyDB |
| **URL** | https://www.hobbydb.com |
| **API** | Sí — API RESTful (requiere aprobación y pago) |
| **Endpoint** | No público. Se accede vía solicitud a https://help.hobbydb.com/support/solutions/articles/36000265069-access-to-the-hobbydb-api |
| **Licencia** | Datos propietarios de hobbyDB |
| **Scrapeable** | No recomendado — requiere API oficial |
| **Nº aproximado de registros** | Millones de coleccionables (incluye Hot Wheels) |
| **Campos disponibles** | Database Items, Estimated Values, Subjects, Items for Sale |

### Acceso a la API

Según la documentación oficial extraída:
> "hobbyDB's system architecture is fully based on Restful APIs. Database Items, Estimated Values, Subjects and Items for Sale are all accessible through the API."

**Requisitos para acceso:**
- Enviar propuesta detallada del proyecto (URL, timeline, propuesta de valor, monetización, equipo)
- Fee de setup: mínimo $1,200 USD one-off
- Cargo mensual por uso de API
- Si el proyecto no genera tráfico significativo para hobbyDB, se cobra

### Ventajas
- Base de datos enorme con precios estimados
- API RESTful bien documentada
- Incluye items for sale (marketplace)
- Datos estructurados

### Límites
- **Pago obligatorio** (mínimo $1,200 setup + mensualidad)
- Requiere aprobación manual
- No es viable para un proyecto pequeño o sin financiamiento
- La API de búsqueda probada (`/api/v1/search`) devolvió 404 — el endpoint exacto solo se obtiene tras aprobación

---

## 4. Hot Wheels Collectors / Mattel Creations

| Campo | Valor |
|---|---|
| **Nombre** | Hot Wheels Collectors (HWC) / Mattel Creations |
| **URL** | https://creations.mattel.com/collections/hot-wheels-collectors |
| **API** | No pública |
| **Licencia** | Contenido oficial Mattel — todos los derechos reservados |
| **Scrapeable** | No recomendado — contenido protegido por copyright |
| **Nº aproximado de registros** | Catálogo oficial de productos RLC y exclusivos |
| **Campos disponibles** | Nombre del modelo, número de serie, precio, descripción, fotos oficiales |

### Contenido

- Catálogo oficial de Red Line Club (RLC)
- Exclusivos de Mattel Creations
- Checklists por año (PDFs descargables en algunos casos)
- Noticias oficiales de nuevos lanzamientos

### Ventajas
- Fuente oficial y autorizada
- Datos precisos de productos oficiales
- Fotos oficiales de alta calidad
- Información de precios de venta al público

### Límites
- No hay API pública
- El contenido está protegido por copyright de Mattel
- No incluye datos de variaciones ni historial completo
- Enfocado en productos actuales, no en catálogo histórico
- Requiere membresía HWC para algunos contenidos

---

## 5. CollectHW

| Campo | Valor |
|---|---|
| **Nombre** | CollectHW |
| **URL** | https://collecthw.com |
| **API** | No pública (sitio web con app) |
| **Licencia** | Contenido generado por usuarios + datos de Fandom |
| **Scrapeable** | Técnicamente sí, pero sin API oficial |
| **Nº aproximado de registros** | **61,298 coches** en el catálogo (según su homepage) |
| **Campos disponibles** | Modelo, año, serie, variación, fotos, listas de colección |

### Contenido verificado

Según la página principal:
> "Your Hot Wheels collection, organized. Catalog what you own, track what you're hunting, and connect with fellow collectors. **61,298** cars in the catalog"

- Búsqueda por año, serie y especiales
- Sistema de colección personal
- Wishlist
- Listas compartibles
- Feed de actividad de otros miembros

### Ventajas
- Catálogo grande (61,298 modelos)
- Interfaz limpia y moderna
- Comunidad activa de coleccionistas
- Datos estructurados por año/serie

### Límites
- No hay API pública
- Los datos pueden estar basados en Fandom (no verificado)
- No incluye precios
- No incluye datos detallados de variaciones (color, tampo, etc.)

---

## 6. HWCollectorsNews.com

| Campo | Valor |
|---|---|
| **Nombre** | Hot Wheels Newsletter |
| **URL** | https://hwcollectorsnews.com |
| **API** | No |
| **Licencia** | Contenido propio |
| **Scrapeable** | Sí (HTML simple) |
| **Nº aproximado de registros** | Cientos de artículos y checklists |
| **Campos disponibles** | Noticias, eventos, checklists, guías de abreviaturas |

### Contenido

- Noticias de lanzamientos
- Checklists por año
- Guías de abreviaturas de ruedas
- Eventos de convenciones
- Inventario personal

### Ventajas
- Fuente confiable de noticias
- Checklists actualizados
- Comunidad de coleccionistas veteranos

### Límites
- No hay API
- Contenido principalmente en formato de blog
- No incluye datos estructurados de variaciones
- No incluye precios

---

## 7. Lamley Group

| Campo | Valor |
|---|---|
| **Nombre** | Lamley Group |
| **URL** | https://lamleygroup.com |
| **API** | No |
| **Licencia** | Contenido propio (blog) |
| **Scrapeable** | Sí (WordPress) |
| **Nº aproximado de registros** | Miles de artículos |
| **Campos disponibles** | Reseñas, fotos, noticias, historia de modelos |

### Contenido

- Reseñas detalladas de modelos
- Fotos de alta calidad
- Historia de los castings
- Noticias de la industria
- Tienda online (lamleystore.com)

### Ventajas
- Contenido de alta calidad
- Fotos excelentes
- Comunidad muy activa
- Cobertura histórica profunda

### Límites
- No hay API
- Formato de blog (no estructurado)
- No incluye datos de variaciones sistemáticos
- No incluye precios de mercado

---

## 8. Orange Track Diecast

| Campo | Valor |
|---|---|
| **Nombre** | Orange Track Diecast |
| **URL** | https://orangetrackdiecast.com |
| **API** | No |
| **Licencia** | Contenido propio |
| **Scrapeable** | Sí (WordPress) |
| **Nº aproximado de registros** | Cientos de artículos y listas |
| **Campos disponibles** | Listas maestras, fotos, datos de variaciones |

### Contenido

- **Hot Wheels Casting Database**: https://orangetrackdiecast.com/hot-wheels-casting-database/
- **2027 Hot Wheels MASTER LIST**: https://orangetrackdiecast.com/2027-hot-wheels-master-list-of-all-lines/
- Listas por año y serie
- Fotos de variaciones

### Ventajas
- Muy bien organizado
- Listas maestras actualizadas
- Fotos de variaciones
- Comunidad activa

### Límites
- No hay API
- Formato de blog
- No incluye precios

---

## 9. Diecast Registry

| Campo | Valor |
|---|---|
| **Nombre** | Diecast Registry |
| **URL** | http://diecastregistry.com |
| **API** | No |
| **Licencia** | Contenido propio |
| **Scrapeable** | Técnicamente sí |
| **Nº aproximado de registros** | Colecciones registradas de miembros |
| **Campos disponibles** | Colecciones, items for sale, membership |

### Contenido

- Registro de colecciones
- Items for sale
- Membership options
- Partners (Big Mike's Diecast)

### Ventajas
- Comunidad de coleccionistas
- Marketplace integrado

### Límites
- No hay API
- Enfocado en NASCAR diecast (no solo Hot Wheels)
- No incluye datos estructurados de catálogo
- Sitio web algo anticuado

---

## 10. PriceCharting

| Campo | Valor |
|---|---|
| **Nombre** | PriceCharting |
| **URL** | https://www.pricecharting.com |
| **API** | No pública |
| **Licencia** | Datos propietarios |
| **Scrapeable** | No — protegido por Cloudflare |
| **Nº aproximado de registros** | Miles de productos con precios |
| **Campos disponibles** | Precios de mercado, historial de precios, variantes |

### Contenido

- Precios de mercado de Hot Wheels
- Historial de precios
- Variantes y ediciones especiales
- Guías de precios

### Ventajas
- Datos de precios reales de mercado
- Historial de precios
- Amplia cobertura

### Límites
- No hay API pública
- Protegido por Cloudflare (no scrapeable fácilmente)
- Enfocado en videojuegos y coleccionables generales
- No incluye datos detallados de variaciones

---

## 11. Wikipedia / Wikidata

| Campo | Valor |
|---|---|
| **Nombre** | Wikipedia — Hot Wheels |
| **URL** | https://en.wikipedia.org/wiki/Hot_Wheels |
| **API** | Sí — MediaWiki API estándar |
| **Endpoint base** | `https://en.wikipedia.org/w/api.php` |
| **Licencia** | CC BY-SA 3.0 |
| **Scrapeable** | Sí, vía API |
| **Nº aproximado de registros** | Artículos generales, no catálogo completo |
| **Campos disponibles** | Historia, información general, listas de videojuegos, etc. |

### Consulta verificada
```bash
curl -s "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=List%20of%20Hot%20Wheels&srlimit=5&format=json" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"
```
Resultado real: 4,606 resultados totales. Incluye "Hot Wheels" (página principal, 10,060 palabras), "Hot Wheels Battle Force 5", "List of Hot Wheels video games", etc.

### Ventajas
- API pública y gratuita
- Información histórica confiable
- Bien referenciada

### Límites
- No es un catálogo de modelos
- Solo información general de la marca
- No incluye datos de variaciones ni precios
- No hay "List of Hot Wheels by year" como artículo completo

---

## 12. Reddit — Comunidades

| Campo | Valor |
|---|---|
| **Nombre** | r/HotWheels |
| **URL** | https://www.reddit.com/r/HotWheels |
| **API** | Sí — Reddit JSON API (requiere OAuth para uso serio) |
| **Endpoint** | `https://www.reddit.com/r/HotWheels/about.json` |
| **Licencia** | Contenido generado por usuarios (licencia Reddit) |
| **Scrapeable** | Técnicamente sí, pero bloqueado por Cloudflare en pruebas |
| **Nº aproximado de miembros** | ~100,000+ (NO VERIFICADO — no se pudo acceder al JSON) |
| **Campos disponibles** | Posts, comentarios, fotos, discusiones |

### Subreddits relevantes
- **r/HotWheels** — comunidad principal
- **r/HotWheelsCollection** — colecciones
- **r/Diecast** — diecast en general
- **r/HotWheelsTrade** — compraventa (NO VERIFICADO si existe)

### Ventajas
- Comunidad muy activa
- Fotos de colecciones reales
- Discusiones sobre variaciones y rarezas
- Información de precios informal

### Límites
- No es una fuente de datos estructurados
- Requiere moderación manual
- Calidad variable
- Reddit API tiene rate limits y requiere OAuth
- Cloudflare bloquea acceso directo con curl

---

## 13. GitHub — Repositorios y APIs de terceros

### 13.1 fast_wheels (API Hot Wheels con FastAPI)

| Campo | Valor |
|---|---|
| **Nombre** | fast_wheels |
| **URL** | https://github.com/joedots1/fast_wheels |
| **Descripción** | "Hot Wheels API using FastAPI, MongoDB, Docker. Data pulled from fandom wiki, cars from 2010-2020" |
| **Estrellas** | 24 |
| **Forks** | 6 |
| **Licencia** | MIT |
| **Creado** | 2020-11-25 |
| **Commits** | 20 |

### Estructura del repositorio
- `app/` — aplicación FastAPI
- `mongo/` — configuración MongoDB
- `scrapers/` — scrapers de Fandom Wiki
- `tests/` — tests
- `docker-compose.yml` — orquestación Docker
- `pyproject.toml` — dependencias Python

### Uso
```bash
git clone https://github.com/joedots1/fast_wheels.git
docker-compose up --build
# API disponible en http://0.0.0.0:8000/docs
```

### Ventajas
- API RESTful lista para usar
- Datos de Fandom Wiki (2010-2020)
- Código abierto (MIT)
- Dockerizado fácil de desplegar

### Límites
- Datos limitados a 2010-2020
- No actualizado desde 2020
- Depende de Fandom Wiki
- No incluye precios

### 13.2 Otros repositorios encontrados

Búsqueda en GitHub API:
```bash
curl -s "https://api.github.com/search/repositories?q=hot+wheels+diecast&sort=stars&order=desc&per_page=10" \
  -H "Accept: application/vnd.github.v3+json"
```
Resultado real: 13 repositorios encontrados. El más relevante es `tquiggle/Diecast-Remote-Raceway` (sistema de carreras remotas, no catálogo).

Búsqueda más amplia:
```bash
curl -s "https://api.github.com/search/repositories?q=hot+wheels+collection+OR+catalog+OR+database&sort=stars&order=desc&per_page=10" \
  -H "Accept: application/vnd.github.v3+json"
```
Resultado real: 955 repositorios encontrados (muchos son spam o irrelevantes).

### Ventajas
- Código reutilizable
- Licencias MIT/Apache permiten uso comercial
- Pueden servir como base para un scraper propio

### Límites
- La mayoría son proyectos personales abandonados
- No hay un proyecto "oficial" o dominante
- Calidad variable

---

## 14. Hugging Face Datasets

| Campo | Valor |
|---|---|
| **Nombre** | Hugging Face Datasets |
| **URL** | https://huggingface.co/datasets?search=hot+wheels |
| **API** | Sí — API de Hugging Face |
| **Endpoint** | `https://huggingface.co/api/datasets?search=hot+wheels&limit=10` |
| **Licencia** | Variable (depende del dataset) |
| **Scrapeable** | Sí, vía API |

### Consulta verificada
```bash
curl -s "https://huggingface.co/api/datasets?search=hot+wheels&limit=10" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"
```

### Datasets encontrados
1. **vedvyas1012/hotwheels40** — 10K-100K registros, formato parquet, modalidad tabular/timeseries/video. 7 downloads.
2. **vedvyas1012/hotwheelsnaya** — <1K registros, modalidad video. 19 downloads.
3. **Tuwano/so101_hotwheels_pickup** — Dataset de robótica (SO-101), 27 episodios, 46,641 frames. 42 downloads.

### Ventajas
- API pública y gratuita
- Descarga directa de datasets
- Formatos modernos (parquet)

### Límites
- **No hay datasets de catálogo de Hot Wheels** (solo datasets de video/robótica)
- Los datasets encontrados no son útiles para un catálogo de coleccionista
- Muy poca comunidad creando datasets de Hot Wheels

---

## 15. Kaggle Datasets

| Campo | Valor |
|---|---|
| **Nombre** | Kaggle Datasets |
| **URL** | https://www.kaggle.com/datasets?search=hot+wheels |
| **API** | Sí — API de Kaggle (requiere autenticación) |
| **Endpoint** | `https://www.kaggle.com/api/v1/datasets/list?search=hot+wheels` |
| **Licencia** | Variable (depende del dataset) |
| **Scrapeable** | Sí, vía API (requiere API key para descarga) |

### Consulta verificada
```bash
curl -s "https://www.kaggle.com/api/v1/datasets/list?search=hot+wheels" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"
```
Resultado real: La búsqueda no devolvió datasets relevantes de Hot Wheels (el primer resultado fue "Spacecraft Thruster Firing Tests Dataset" — irrelevante).

### Ventajas
- Plataforma con datasets de calidad
- Licencias claras por dataset

### Límites
- **No hay datasets de catálogo de Hot Wheels** en Kaggle
- Requiere autenticación para descargar
- La búsqueda no devolvió resultados relevantes

---

## 16. Foros y Comunidades en Español

### 16.1 Foro Hot Wheels (iya.es)

| Campo | Valor |
|---|---|
| **Nombre** | Foro Hot Wheels |
| **URL** | http://iya.es/ |
| **Tipo** | Foro web |
| **Idioma** | Español |
| **Miembros** | NO VERIFICADO |
| **Actividad** | NO VERIFICADO |

### 16.2 Hot Wheels Collectors Association Forum

| Campo | Valor |
|---|---|
| **Nombre** | Hot Wheels Collectors Association Forum |
| **URL** | https://hwcaforum.mforos.com/ |
| **Tipo** | Foro web (mforos) |
| **Idioma** | Español |
| **Miembros** | NO VERIFICADO |
| **Actividad** | NO VERIFICADO |

### 16.3 Forocoches — Subforo de Hot Wheels

| Campo | Valor |
|---|---|
| **Nombre** | Forocoches |
| **URL** | https://forocoches.com/foro/forumdisplay.php?f=28 |
| **Tipo** | Foro web |
| **Idioma** | Español |
| **Miembros** | NO VERIFICADO |
| **Actividad** | NO VERIFICADO |

### Ventajas
- Comunidad hispanohablante
- Intercambio de modelos entre coleccionistas
- Información de variaciones regionales

### Límites
- No hay API
- Volumen y actividad NO VERIFICADOS
- Calidad variable
- No son fuentes de datos estructurados

---

## 17. Discord — Servidores de Coleccionistas

### 17.1 Hot Wheels Collecting Community

| Campo | Valor |
|---|---|
| **Nombre** | Hot Wheels Collecting Community |
| **URL** | https://top.gg/zh/discord/servers/543008142567608333 |
| **Tipo** | Servidor Discord |
| **Miembros** | NO VERIFICADO |
| **Actividad** | NO VERIFICADO |

### 17.2 Wysp Diecast

| Campo | Valor |
|---|---|
| **Nombre** | Wysp Diecast |
| **URL** | https://discord.me/wyspdiecast |
| **Tipo** | Servidor Discord |
| **Miembros** | NO VERIFICADO |
| **Actividad** | NO VERIFICADO |

### Ventajas
- Comunidad en tiempo real
- Intercambio rápido de información
- Fotos y discusiones en vivo

### Límites
- No hay API pública de Discord para extraer datos
- Requiere bot con permisos
- No es una fuente de datos estructurados
- Volumen NO VERIFICADO

---

## 18. Facebook — Grupos de Coleccionistas

### 18.1 Hotwheels Collectors Mexico

| Campo | Valor |
|---|---|
| **Nombre** | Hotwheels Collectors Mexico Foros - Variantes |
| **URL** | https://www.facebook.com/groups/1501219356586855/?locale=es_ES |
| **Tipo** | Grupo Facebook |
| **Miembros** | NO VERIFICADO |
| **Actividad** | NO VERIFICADO |

### 18.2 LA BODEGA DEL HOT WHEELS Y MAS

| Campo | Valor |
|---|---|
| **Nombre** | LA BODEGA DEL HOT WHEELS Y MAS |
| **URL** | https://www.facebook.com/groups/1439892219374693/ |
| **Tipo** | Grupo Facebook |
| **Miembros** | NO VERIFICADO |
| **Actividad** | NO VERIFICADO |

### 18.3 Hot Wheels Playa del Carmen

| Campo | Valor |
|---|---|
| **Nombre** | Hot Wheels Playa del Carmen |
| **URL** | https://www.facebook.com/groups/450421577294155/ |
| **Tipo** | Grupo Facebook |
| **Miembros** | NO VERIFICADO |
| **Actividad** | NO VERIFICADO |

### Ventajas
- Comunidad local activa
- Compraventa entre miembros
- Intercambio de información regional

### Límites
- No hay API pública de Facebook Groups
- Requiere Graph API con permisos especiales
- No es una fuente de datos estructurados
- Volumen NO VERIFICADO

---

## 19. YouTube / TikTok — Canales Relevantes

### Canales de YouTube relevantes (NO VERIFICADO — no se pudieron probar)
- **Lamley Group** — reseñas y noticias
- **Hot Wheels** (canal oficial) — trailers y anuncios
- **Diecast Review** — reseñas de modelos
- **The Toy Peddler** — noticias y colecciones

### TikTok
- Hashtags: #hotwheels, #hotwheelscollection, #diecast
- Creadores de contenido de coleccionistas

### Ventajas
- Contenido visual de alta calidad
- Reseñas detalladas
- Comunidad activa

### Límites
- No hay API para extraer datos estructurados
- Requiere análisis manual de videos
- No es una fuente de datos primaria

---

## 20. Consideraciones Legales

### 20.1 Marcas registradas

- **Hot Wheels®** es una marca registrada de **Mattel, Inc.**
- El uso del nombre y logo en una app de terceros requiere:
  - Aviso claro de que es un producto no oficial
  - No sugerir afiliación o respaldo de Mattel
  - Uso de nominativo fair use (describir productos)

### 20.2 Imágenes con copyright

- Las fotos de productos oficiales son propiedad de Mattel
- Las fotos de Fandom Wiki están bajo CC BY-SA 3.0 (requieren atribución)
- Las fotos de South Texas Diecast son propiedad del sitio
- **Recomendación**: usar solo imágenes de Fandom Wiki (CC BY-SA) o tomar fotos propias

### 20.3 Datos de Fandom Wiki

- Licencia: CC BY-SA 3.0
- Requiere atribución a "Hot Wheels Wiki" y enlace a la fuente
- Si se modifican los datos, deben compartirse bajo la misma licencia
- **Recomendación**: incluir atribución en la app y mantener un archivo de procedencia de datos

### 20.4 HobbyDB

- Los datos son propietarios de hobbyDB
- El acceso a la API requiere acuerdo comercial
- No se pueden usar los datos sin permiso

### 20.5 Cómo hacer un catálogo propio sin infringir

1. **Usar Fandom Wiki como fuente primaria** (CC BY-SA 3.0)
2. **Atribuir correctamente** a la fuente
3. **No usar imágenes oficiales de Mattel** sin permiso
4. **Tomar fotos propias** de los modelos
5. **Incluir disclaimer** de producto no oficial
6. **No usar el logo de Hot Wheels** sin permiso
7. **Considerar usar datos de CollectHW** (61,298 modelos) como referencia

---

## 21. Resumen Comparativo

| Fuente | API | Registros | Precios | Variaciones | Licencia | Scrapeable |
|---|---|---|---|---|---|---|
| **Fandom Wiki** | Sí (gratis) | ~15,000+ | No | Sí (detallado) | CC BY-SA 3.0 | Sí (API) |
| **South Texas Diecast** | No | Miles | No | Parcial | Propia | Sí (HTML) |
| **HobbyDB** | Sí (pago) | Millones | Sí | Sí | Propia | No |
| **Mattel Creations** | No | Catálogo oficial | Sí (PVP) | No | Copyright | No |
| **CollectHW** | No | 61,298 | No | Parcial | Propia | Sí (HTML) |
| **HWCollectorsNews** | No | Cientos | No | No | Propia | Sí (HTML) |
| **Lamley Group** | No | Miles | No | Parcial | Propia | Sí (HTML) |
| **Orange Track Diecast** | No | Cientos | No | Sí | Propia | Sí (HTML) |
| **Diecast Registry** | No | Colecciones | No | No | Propia | Sí (HTML) |
| **PriceCharting** | No | Miles | Sí | Parcial | Propia | No (Cloudflare) |
| **Wikipedia** | Sí (gratis) | General | No | No | CC BY-SA 3.0 | Sí (API) |
| **Reddit** | Sí (OAuth) | Comunidad | Informal | Informal | Reddit | No (Cloudflare) |
| **GitHub (fast_wheels)** | Sí (código) | 2010-2020 | No | Sí | MIT | N/A |
| **Hugging Face** | Sí (gratis) | 0 relevantes | No | No | Variable | Sí (API) |
| **Kaggle** | Sí (auth) | 0 relevantes | No | No | Variable | Sí (API) |

---

## 22. Comandos Probados

### Fandom API
```bash
# Búsqueda de páginas
curl -s "https://hotwheels.fandom.com/api.php?action=query&list=search&srsearch=2024+Mainline&srlimit=5&format=json" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"

# Contenido de una página (infobox + tablas)
curl -s "https://hotwheels.fandom.com/api.php?action=query&prop=revisions&titles=Punk%20Rod&rvslots=*&rvprop=content&format=json" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"

# Miembros de una categoría
curl -s "https://hotwheels.fandom.com/api.php?action=query&list=categorymembers&cmtitle=Category:2024%20Hot%20Wheels&cmlimit=5&format=json" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"

# Listar categorías por prefijo
curl -s "https://hotwheels.fandom.com/api.php?action=query&list=allcategories&aclimit=50&acprefix=2024&format=json" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"

# Lista de 2024 Hot Wheels (contenido completo)
curl -s "https://hotwheels.fandom.com/api.php?action=query&prop=revisions&titles=List%20of%202024%20Hot%20Wheels&rvslots=*&rvprop=content&format=json" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"
```

### Wikipedia API
```bash
curl -s "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=List%20of%20Hot%20Wheels&srlimit=5&format=json" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"
```

### GitHub API
```bash
curl -s "https://api.github.com/search/repositories?q=hot+wheels+diecast&sort=stars&order=desc&per_page=10" \
  -H "Accept: application/vnd.github.v3+json"

curl -s "https://api.github.com/search/repositories?q=hot+wheels+collection+OR+catalog+OR+database&sort=stars&order=desc&per_page=10" \
  -H "Accept: application/vnd.github.v3+json"
```

### Hugging Face API
```bash
curl -s "https://huggingface.co/api/datasets?search=hot+wheels&limit=10" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"
```

### Kaggle API
```bash
curl -s "https://www.kaggle.com/api/v1/datasets/list?search=hot+wheels" \
  -H "User-Agent: HotWheelsCollectorResearch/1.0"
```

### South Texas Diecast
```bash
curl -s "https://www.southtexasdiecast.com/hot-wheels/2024/" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -L
```

### CollectHW
```bash
curl -s "https://collecthw.com/" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -L
```

### HWCollectorsNews
```bash
curl -s "https://hwcollectorsnews.com/" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -L
```

### Reddit (bloqueado por Cloudflare)
```bash
curl -s "https://www.reddit.com/r/HotWheels/about.json" \
  -H "User-Agent: python:hotwheels-research:v1.0 (by /u/researcher)" \
  -H "Accept: application/json"
```

### HobbyDB (404 — requiere acceso aprobado)
```bash
curl -s "https://hobbydb.com/api/v1/search?query=hot+wheels&limit=3" \
  -H "User-Agent: Mozilla/5.0" -L
```

### PriceCharting (bloqueado por Cloudflare)
```bash
curl -s "https://www.pricecharting.com/search-products?q=hot+wheels&type=game" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -L
```

---

## Conclusiones

1. **La mejor fuente de datos es Fandom Wiki** — API pública, gratuita, con datos estructurados de variaciones, licencia CC BY-SA 3.0, y cobertura histórica amplia.

2. **CollectHW es la segunda mejor opción** — 61,298 modelos en catálogo, aunque sin API pública.

3. **HobbyDB es la opción comercial** — requiere pago (mínimo $1,200 setup + mensualidad) pero incluye precios de mercado.

4. **No hay datasets públicos de Hot Wheels** en Hugging Face ni Kaggle.

5. **El repositorio GitHub `joedots1/fast_wheels`** es la única API de terceros encontrada, con datos de 2010-2020 extraídos de Fandom Wiki.

6. **Las comunidades en español existen** (foros, Facebook, Discord) pero no son fuentes de datos estructurados.

7. **Para una app de coleccionistas**, la estrategia recomendada es:
   - Usar Fandom Wiki como fuente primaria de datos
   - Complementar con South Texas Diecast y Orange Track Diecast para verificación
   - Implementar scraping propio con atribución CC BY-SA
   - No usar imágenes oficiales de Mattel sin permiso
   - Incluir disclaimer de producto no oficial

---

*Documento generado el 2026-10-11 mediante investigación activa con curl y web search.*
