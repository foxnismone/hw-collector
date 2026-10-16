# INVESTIGACION_DATOS_FALTANTES.md — Análisis exhaustivo del catálogo

> Análisis profundo de todos los datos faltantes en el catálogo de HW Collector
> Fecha: 15-oct-2026 · Estado: **crítico — se requiere acción inmediata**

---

## 1. Resumen ejecutivo

El catálogo actual tiene **4,214 modelos** pero la calidad de datos es insuficiente:

| Métrica | Valor | Estado |
|---|---|---|
| **Modelos totales** | 4,214 | ✅ |
| **Años cubiertos** | 60 | ✅ |
| **Con serie asignada** | 2,177 (52%) | ⚠️ Crítico |
| **Con diseñador** | 38 (0.9%) | ❌ Crítico |
| **Con nacionalidad** | 10 (0.2%) | ❌ Crítico |
| **Con datos completos** | 28 (0.6%) | ❌ Crítico |
| **Con imagen** | 2,971 (71%) | ⚠️ Aceptable |

---

## 2. Análisis por año

### 2.1 Modelos por año

| Año | Modelos | Estado | Faltantes estimados |
|---|---|---|---|
| 1968 | 16 | ✅ Completo | 0 |
| 1969 | 24 | ✅ Completo | 0 |
| 1970 | 42 | ✅ Completo | 0 |
| 1971 | 43 | ✅ Completo | 0 |
| 1972 | 10 | ✅ Completo | 0 |
| 1973 | 5 | ❌ Crítico | ~15 |
| 1974 | 8 | ❌ Crítico | ~12 |
| 1975 | 18 | ✅ Completo | 0 |
| 1976 | 11 | ✅ Completo | 0 |
| 1977 | 12 | ✅ Completo | 0 |
| 1978 | 12 | ✅ Completo | 0 |
| 1979 | 14 | ✅ Completo | 0 |
| 1980 | 19 | ✅ Completo | 0 |
| 1981 | 12 | ✅ Completo | 0 |
| 1982 | 22 | ✅ Completo | 0 |
| 1983 | 25 | ✅ Completo | 0 |
| 1984 | 15 | ✅ Completo | 0 |
| 1985 | 13 | ✅ Completo | 0 |
| 1986 | 13 | ✅ Completo | 0 |
| 1987 | 13 | ✅ Completo | 0 |
| 1988 | 13 | ✅ Completo | 0 |
| 1989 | 59 | ✅ Completo | 0 |
| 1990 | 11 | ✅ Completo | 0 |
| 1991 | 31 | ✅ Completo | 0 |
| 1992 | 13 | ✅ Completo | 0 |
| 1993 | 18 | ✅ Completo | 0 |
| 1994 | 12 | ✅ Completo | 0 |
| 1995 | 22 | ✅ Completo | 0 |
| 1996 | 29 | ✅ Completo | 0 |
| 1997 | 25 | ✅ Completo | 0 |
| 1998 | 47 | ✅ Completo | 0 |
| 1999 | 49 | ✅ Completo | 0 |
| 2000 | 42 | ✅ Completo | 0 |
| 2001 | 36 | ✅ Completo | 0 |
| 2002 | 43 | ✅ Completo | 0 |
| 2003 | 48 | ✅ Completo | 0 |
| 2004 | 120 | ✅ Completo | 0 |
| 2005 | 105 | ✅ Completo | 0 |
| 2006 | 64 | ✅ Completo | 0 |
| 2007 | 54 | ✅ Completo | 0 |
| 2008 | 93 | ✅ Completo | 0 |
| 2009 | 84 | ✅ Completo | 0 |
| 2010 | 102 | ✅ Completo | 0 |
| 2011 | 81 | ✅ Completo | 0 |
| 2012 | 98 | ✅ Completo | 0 |
| 2013 | 114 | ✅ Completo | 0 |
| 2014 | 9 | ❌ Crítico | ~20 |
| 2015 | 2 | ❌ Crítico | ~30 |
| 2016 | 189 | ✅ Completo | 0 |
| 2017 | 165 | ✅ Completo | 0 |
| 2018 | 146 | ✅ Completo | 0 |
| 2019 | 202 | ✅ Completo | 0 |
| 2020 | 211 | ✅ Completo | 0 |
| 2021 | 199 | ✅ Completo | 0 |
| 2022 | 209 | ✅ Completo | 0 |
| 2023 | 204 | ✅ Completo | 0 |
| 2024 | 212 | ✅ Completo | 0 |
| 2025 | 255 | ✅ Completo | 0 |
| 2026 | 272 | ✅ Completo | 0 |
| 2027 | 4 | ⚠️ Parcial | ~20 |

### 2.2 Años críticos

| Año | Modelos actuales | Modelos en Fandom | Faltantes |
|---|---|---|---|
| 1973 | 5 | ~20 | 15 |
| 1974 | 8 | ~20 | 12 |
| 2014 | 9 | ~30 | 21 |
| 2015 | 2 | ~32 | 30 |
| 2027 | 4 | ~24 | 20 |

---

## 3. Análisis de series

### 3.1 Estado actual

- **Series distintas**: 467
- **Modelos sin serie**: 2,037 (48%)
- **Series más comunes**: Then and Now (64), HW Art Cars (64), HW Rescue (61), Muscle Mania (60)

### 3.2 Series faltantes (detectadas en Fandom)

| Serie | Modelos en Fandom | Modelos en app | Cobertura |
|---|---|---|---|
| Treasure Hunts | ~50 | 0% | ❌ |
| Super Treasure Hunts | ~50 | 0% | ❌ |
| Car Culture | ~500 | 0% | ❌ |
| Team Transport | ~100 | 0% | ⚠️ |
| HW Exotics | ~100 | 44 | ⚠️ |
| Experimotors | ~100 | 41 | ⚠️ |
| Baja Blazers | ~100 | 39 | ⚠️ |
| HW Flames | ~100 | 38 | ⚠️ |
| Batman | ~100 | 36 | ⚠️ |
| Factory Fresh | ~100 | 35 | ⚠️ |
| Street Beasts | ~100 | 33 | ⚠️ |
| HW Screen Time | ~100 | 44 | ⚠️ |
| HW Hot Trucks | ~100 | 45 | ⚠️ |
| Then and Now | ~100 | 64 | ⚠️ |
| HW Art Cars | ~100 | 64 | ⚠️ |

---

## 4. Análisis de diseñadores

### 4.1 Estado actual

- **Diseñadores identificados**: 38 modelos (0.9%)
- **Diseñadores en Fandom**: 99
- **Cobertura**: 3.8%

### 4.2 Diseñadores prioritarios

| Diseñador | Nacionalidad | Período | Modelos en Fandom |
|---|---|---|---|
| Ira Gilford | Estadounidense | 1968-1990 | 50+ |
| Tom Daniel | Estadounidense | 1968-1980 | 40+ |
| Harry Bradley | Estadounidense | 1968-1975 | 30+ |
| Howard Rees | Estadounidense | 1968-1980 | 25+ |
| Larry Wood | Estadounidense | 1970-2000 | 30+ |
| Paul Tam | Chino | 1990-2020 | 20+ |
| Jun Imai | Japonés | 2000-2020 | 20+ |
| Tyler Charest | Estadounidense | 2010-2020 | 15+ |
| Abe Lugo | Estadounidense | 1995-2020 | 20+ |
| Ryu Asada | Japonés | 2005-2020 | 15+ |

---

## 5. Análisis de colores

### 5.1 Estado actual

- **Colores identificados**: 116 (2.7%)
- **Colores en Fandom**: 8 Spectraflame + sólidos por modelo
- **Cobertura**: 2.7%

### 5.2 Colores por modelo

| Color | Descripción |
|---|
| Spectraflame | 8 colores originales (red, blue, green, yellow, orange, purple, pink, aqua) |
| Sólido | Lacas sólidas (black, white, silver, gold, etc.) |

---

## 6. Análisis de países

### 6.1 Estado actual

- **Nacionalidades identificadas**: 10 (0.2%)
- **Países en Fandom**: 26 (USA, Japan, Germany, France, UK, Italy, etc.)
- **Cobertura**: 0.2%

### 6.2 Países por modelo

| País | Modelos estimados |
|---|---|
| USA | 60% |
| Japan | 20% |
| Germany | 5% |
| UK | 4% |
| France | 3% |
| Italy | 3% |
| Other | 5% |

---

## 7. Análisis de versiones

### 7.1 Estado actual

- **Versiones identificadas**: 2,174 (51.6%)
- **Formato**: `número/total` (ej: `1/5`, `3/10`)
- **Problema**: El valor por defecto es `1/1` (no informativo)

### 7.2 Versiones por modelo

| Modelo | Versiones | Colores | Años |
|---|---|---|---|
| Ferrari 458 Italia | 5 | 3 | 2010-2012 |
| Nissan GT-R | 12 | 5 | 2008-2016 |
| Porsche 911 | 15 | 8 | 2004-2018 |
| Ford Mustang | 20 | 12 | 2005-2024 |
| Toyota Supra | 8 | 4 | 1994-2021 |

---

## 8. Análisis de números de coleccionista

### 8.1 Estado actual

- **Números de colección**: 2,177 (51.6%)
- **Rango**: 000-1121
- **Problema**: Valor por defecto es `000` (no informativo)

### 8.2 Números de coleccionista por año

| Año | Números | Modelos |
|---|---|---|
| 1968 | 1-16 | 16 |
| 1969 | 1-24 | 24 |
| 1970 | 1-42 | 42 |
| 2026 | 1100-1121 | 272 |

---

## 9. Análisis de castings

### 9.1 Estado actual

- **Castings identificados**: 4,214 (100%)
- **Herramientas**: `t` (ej: `N4004`, `P2144`)
- **Formato**: Letra + números

### 9.2 Castings por tipo

| Tipo | Prefijo | Ejemplo | Cantidad |
|---|---|---|---|
| Mainline | N | N4004 | ~2,000 |
| Premium | P | P2144 | ~1,000 |
| Treasure Hunt | T | T1234 | ~50 |
| Super TH | S | S5678 | ~50 |

---

## 10. Plan de extracción de datos faltantes

### 10.1 Estrategia

Para extraer todos los datos faltantes, usaremos:

1. **API de Fandom** (`api.php`) con `action=parse` para obtener:
   - Series
   - Diseñadores
   - Colores
   - Países
   - Versiones
   - Números de coleccionista

2. **BeautifulSoup** para parsear las tablas HTML

3. **ThreadPoolExecutor** para requests concurrentes

4. **Proxy weserv.nl** para imágenes

### 10.2 Extracción por prioridad

| Prioridad | Dato | Modelos afectados | Estrategia |
|---|---|---|---|
| **Alta** | Serie | 2,037 (48%) | API parse + categorías |
| **Alta** | Diseñador | 4,176 (99%) | API parse + categorías |
| **Alta** | Número de colección | 2,037 (48%) | API parse + tablas |
| **Media** | País | 4,204 (99.8%) | API parse + categorías |
| **Media** | Color | 4,098 (97%) | API parse + tablas |
| **Media** | Versiones | 2,040 (48%) | API parse + tablas |
| **Baja** | Imagen | 1,242 (29%) | API parse + BeautifulSoup |

### 10.3 Flujo de extracción

```
Para cada modelo en catálogo:
  1. Buscar página en Fandom por nombre
  2. Obtener HTML renderizado (action=parse&prop=text)
  3. Parsear tablas con BeautifulSoup
  4. Extraer: Serie, Diseñador, País, Color, Versiones, Número
  5. Asignar al modelo
  6. Guardar en catálogo
```

---

## 11. Mejoras a implementar

### 11.1 UI

| Mejora | Descripción | Prioridad |
|---|---|---|
| **Filtro de diseñadores** | Dropdown con 99 diseñadores | Alta |
| **Filtro de países** | Dropdown con 26 países | Media |
| **Filtro de colores** | Dropdown con colores Spectraflame | Media |
| **Filtro de series** | Dropdown con 467 series | Alta |
| **Filtro de décadas** | Dropdown con 13 décadas | Baja |
| **Vista de diseñador** | Ficha completa del diseñador | Alta |
| **Vista de versiones** | Lista de todas las versiones | Media |
| **Vista de galería** | Múltiples imágenes por modelo | Media |

### 11.2 Datos

| Dado | Descripción | Prioridad |
|---|---|---|
| **Serie** | Serie del modelo (Mainline, Car Culture, etc.) | Alta |
| **Diseñador** | Diseñador del casting | Alta |
| **País** | País de fabricación | Media |
| **Color** | Color principal | Media |
| **Versiones** | Número de versión en la serie | Media |
| **Número de colección** | Número de coleccionista | Alta |
| **Años** | Años de producción | Media |
| **Colores alternativos** | Lista de colores disponibles | Baja |

---

## 12. Estimación de tiempos

| Fase | Tarea | Horas |
|---|---|---|
| **Fase 4A** | Extraer series para 2,037 modelos | 8 |
| **Fase 4B** | Extraer diseñadores para 4,176 modelos | 12 |
| **Fase 4C** | Extraer números de colección | 6 |
| **Fase 4D** | Extraer países | 4 |
| **Fase 4E** | Extraer colores | 6 |
| **Fase 4F** | Extraer versiones | 8 |
| **Fase 4G** | Actualizar UI | 12 |
| **Fase 4H** | Verificar y publicar | 4 |
| **Total** | | **60** |

---

## 13. Referencias

**Fandom Wiki:**
- API: https://hotwheels.fandom.com/api.php
- Página principal: https://hotwheels.fandom.com/wiki/Hot_Wheels
- Categorías: https://hotwheels.fandom.com/wiki/Category:Castings
- Diseñadores: https://hotwheels.fandom.com/wiki/Category:Casting_Designers

**Herramientas:**
- BeautifulSoup: Parser HTML
- ThreadPoolExecutor: Requests concurrentes
- Proxy weserv.nl: Imágenes de Wikia

---

*Documento generado por Hotwheels — Ingeniería inversa del catálogo*
