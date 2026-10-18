# 📋 Informe QA Profundo — Hot Wheels Collector

**Fecha:** 2026-10-18  
**Proyecto:** Hot Wheels Collector (PWA)  
**Fuentes comparativas:** Fandom Hot Wheels Wiki (hotwheels.fandom.com)  
**Versión analizada:** v2.0.0 (build 2026-10-17)

---

## 1. Catálogo de Modelos

### 1.1 Cobertura General

| Métrica | Valor | % |
|---------|-------|---|
| **Total de modelos** | 4,391 | — |
| Con imagen | 4,389 | 99% |
| Con diseñador asignado | 4,391 | 100% |
| Con país | 4,391 | 100% |
| Con tool number | 4,321 | 98% |
| Con serie | 4,391 | 100% |
| Con ficha (descripción) | 4,391 | 100% |

### 1.2 Cobertura por Año

| Año | Modelos | vs Fandom Wiki* |
|-----|---------|-----------------|
| 2027 | 4 | — |
| 2026 | 272 | ✅ Similar |
| 2025 | 260 | ✅ Similar |
| 2024 | 217 | ✅ Similar |
| 2023 | 204 | ✅ Similar |
| 2022 | 209 | ✅ Similar |
| 2021 | 199 | ✅ Similar |
| 2020 | 212 | ✅ Similar |
| 2019 | 203 | ✅ Similar |
| 2018 | 146 | ✅ Similar |
| 2017 | 165 | ✅ Similar |
| 2016 | 189 | ✅ Similar |
| **2015** | **2** | ⚠️ **Muy bajo** |
| **2014** | **9** | ⚠️ **Muy bajo** |
| 2013 | 114 | ⚠️ Bajo |
| 1968-1995 | 16-104 | ⚠️ **Insuficiente** |

*Fandom Wiki típicamente tiene 200-400+ modelos por año en mainline. Los años 2014-2015 tienen una cobertura significativamente menor.*

### 1.3 Imágenes

| Tipo | Cantidad | % |
|------|----------|---|
| Imágenes por URL externa (Wikia/weserv) | 2,054 | 47% |
| Imágenes locales (existentes en /img) | 2,173 | 49% |
| **Imágenes locales FALTANTES en /img** | **162** | **4%** |
| **URLs externas que no están cacheadas** | **1,520** | **35%** |

**🔴 Problemas encontrados:**

1. **1,520 imágenes referenciadas pero no cacheadas localmente** — El sitio depende de URLs externas de Wikia/weserv que pueden fallar o ser bloqueadas. Esto viola el principio de PWA offline-first.
2. **162 imágenes locales referenciadas pero no existen en /img** — URLs rotas que mostrarán imágenes rotas.
3. **2 modelos sin imagen** — `peterbilt cement mixer?` (1982), `bulldozer?` (1982) — nombres con interrogación indican datos no verificados.

### 1.4 Consistencia de Datos

| Problema | Cantidad | Severidad |
|----------|----------|-----------|
| **IDs duplicados** | 35 | 🔴 Alta |
| Modelos sin tool number | 70 | 🟡 Media |
| Nombres con "?" (sin verificar) | 2 | 🟡 Media |
| Series con código wiki sin limpiar | 532 | 🔴 Alta |

**Ejemplos de IDs duplicados:** Se encontraron 35 IDs que aparecen más de una vez en el catálogo, lo que puede causar errores en la colección y búsqueda.

**Ejemplos de series con código wiki sin limpiar:**
- `[[HW J-Imports Mini Collection (2025)|<font color="bl...`
- `HWC.com Series 11[]`
- `Fast Foodie Ryu's Rides`

---

## 2. Diseñadores

### 2.1 Cobertura General

| Métrica | Valor | % |
|---------|-------|---|
| **Total de diseñadores** | 146 | — |
| Con foto | 146 | 100% |
| Con biografía (>100 chars) | 99 | 67% |
| Con nacionalidad | 129 | 88% |
| Con periodo | 129 | 88% |

### 2.2 Calidad de Biografías

| Problema | Cantidad | Severidad |
|----------|----------|-----------|
| **Biografías con código wiki sin limpiar** | **95/146** | 🔴 **Alta (65%)** |
| Biografías vacías o muy cortas | 47/146 | 🟡 Media (32%) |
| Diseñadores sin nacionalidad | 17/146 | 🟡 Media (12%) |

**Ejemplos de biografías con código wiki sin limpiar:**
```
{{Designer|name=Abe Lugo|years=[[2008]] &ndash; [[2025]]|image=AbeLugo.png}}'''Abraham Lugo''' is a former Hot Wheels...
```

```
[[File:ADSerrano.png|200px|right]]'''Amaury Diaz Serrano''' is a Puerto Rican-American industrial designer...
```

Estas plantillas y wikilinks **no se renderizan** en la app y se muestran como texto crudo.

### 2.3 Nacionalidades

| Nacionalidad | Count |
|--------------|-------|
| Estadounidense | 96 |
| (vacío) | 17 |
| Chino | 6 |
| Británico | 3 |
| Alemán | 3 |
| Chino-estadounidense | 3 |
| Coreano-Americano | 2 |
| Coreano | 2 |
| Hong Kong | 2 |
| Otros | 11 |

### 2.4 Multi Idioma

**🔴 Problema crítico:** Las biografías están **solo en inglés**. No hay traducción al español de las biografías de diseñadores, a pesar de que la app está en español.

---

## 3. Tipos de Ruedas

### 3.1 Cobertura General

| Métrica | Valor | % |
|---------|-------|---|
| **Total de tipos** | 153 | — |
| Con descripción ES | 153 | 100% |
| Con descripción EN | 153 | 100% |
| Con color | 153 | 100% |
| Con categoría | 153 | 100% |

### 3.2 Categorías

| Categoría | Count |
|-----------|-------|
| moderna | 89 |
| rr (Real Riders) | 27 |
| offroad | 12 |
| especial | 11 |
| clasica | 4 |
| mini | 4 |
| moto | 3 |
| micro | 3 |

### 3.3 Evaluación

✅ **Excelente cobertura.** Los tipos de ruedas tienen la mejor calidad de datos del proyecto:
- Bilingüe (ES/EN) al 100%
- Con color para identificación visual
- Con categoría para filtrado
- Con descripciones en ambos idiomas

---

## 4. Series

### 4.1 Cobertura General

| Métrica | Valor | % |
|---------|-------|---|
| **Total de series** | 692 | — |
| Con imagen | 676 | 97% |
| Con descripción (>50 chars) | 574 | 82% |
| Con años | 688 | 99% |

### 4.2 Idioma de Descripciones

| Idioma | Count | % |
|--------|-------|---|
| Español | 630 | 91% |
| Inglés | 48 | 7% |
| Sin descripción | 14 | 2% |

### 4.3 Problemas

| Problema | Cantidad | Severidad |
|----------|----------|-----------|
| **Series en catálogo no están en series_catalog** | **532** | 🔴 **Alta** |
| Series sin imagen | 16 | 🟡 Media |
| Series sin descripción | 15 | 🟡 Media |
| Series sin años | 4 | 🟢 Baja |

**Ejemplos de series faltantes en series_catalog:**
- `HW J-Imports New in Mainline`
- `Nightspeed`
- `HW Heavyweights`
- `HW Digital Circuit Walmart Exclusive`
- `Then and Now Walgreens Exclusive`
- `HW Speed Graphics New in Mainline`
- `Fast Foodie Ryu's Rides`
- `HW Dream Garage`

**Ejemplos de series sin imagen:**
- 5-Packs
- Anniversary Series
- Chase
- Chronological List of Hot Wheels Series
- HW City Series

---

## 5. UX/UI

### 5.1 Estructura Técnica

| Característica | Estado |
|----------------|--------|
| HTML size | 4.18 MB |
| Viewport | ✅ |
| Meta description | ✅ |
| Lang="es" | ✅ |
| PWA Manifest | ✅ |
| Service Worker | ✅ |
| Content Security Policy | ✅ |
| X-Frame-Options: DENY | ✅ |
| X-Content-Type-Options: nosniff | ✅ |
| Referrer-Policy | ✅ |
| Tema de color (#ff4d00) | ✅ |

### 5.2 Diseño

| Aspecto | Evaluación |
|---------|------------|
| Navegación | ✅ Presente |
| Header | ✅ Presente |
| CSS | ✅ Incrustado |
| JavaScript | ✅ Incrustado |
| Imágenes en HTML | 14 (solo iconos/UI) |

### 5.3 Problemas UX/UI

| Problema | Severidad |
|----------|-----------|
| **HTML de 4.18 MB** — Demasiado pesado para carga inicial | 🟡 Media |
| **Imágenes cacheadas que no se descargan** — La PWA no es offline-first | 🔴 Alta |
| **Dependencia de URLs externas** (Wikia/weserv) para el 47% de imágenes | 🔴 Alta |

### 5.4 Comparación con Fandom Wiki

| Aspecto | HW Collector | Fandom Wiki |
|---------|--------------|-------------|
| Cobertura de catálogo | 4,391 modelos | ~10,000+ |
| Cobertura histórica (1968-1995) | ⚠️ Insuficiente | ✅ Completa |
| Imágenes offline | ❌ Depende de red | ✅ Cacheadas |
| Bilingüe | ⚠️ Solo ruedas | ✅ ES/EN/otros |
| Diseñadores | 146 | 100+ |
| Series | 692 | 500+ |

---

## 6. Contenido Multi Idioma

### 6.1 Cobertura por Sección

| Sección | Español | Inglés | Otros |
|---------|---------|--------|-------|
| Catálogo (modelos) | ✅ 100% | ❌ 0% | ❌ |
| Fichas de modelos | ✅ 100% | ❌ 0% | ❌ |
| Diseñadores (biografías) | ❌ 0% | ✅ 100% | ❌ |
| Tipos de ruedas | ✅ 100% | ✅ 100% | ❌ |
| Series (descripciones) | ✅ 91% | ⚠️ 7% | ❌ |
| UI de la app | ✅ 100% | ❌ 0% | ❌ |

### 6.2 Evaluación

🔴 **Problema crítico:** El contenido está **fragmentado por idioma**:
- Las fichas de modelos solo están en español
- Las biografías de diseñadores solo están en inglés
- Solo los tipos de ruedas son completamente bilingües

Esto crea una experiencia inconsistente: un usuario español ve biografías en inglés de diseñadores, y un usuario inglés ve fichas de modelos en español.

---

## 7. Resumen de Problemas por Severidad

### 🔴 Alta (10 problemas)

| # | Problema | Impacto |
|---|----------|---------|
| 1 | 1,520 imágenes no cacheadas localmente | PWA no funciona offline |
| 2 | 35 IDs duplicados en catálogo | Errores en búsqueda y colección |
| 3 | 95 biografías con código wiki sin limpiar (65%) | Texto crudo visible en UI |
| 4 | 532 series en catálogo no están en series_catalog | Filtros y navegación rotos |
| 5 | Biografías de diseñadores solo en inglés | Usuarios españoles no pueden leerlas |
| 6 | Fichas de modelos solo en español | Usuarios ingleses no pueden leerlas |
| 7 | Cobertura histórica insuficiente (1968-1995) | Catálogo incompleto |
| 8 | 162 imágenes locales faltantes | Imágenes rotas en UI |
| 9 | Dependencia de URLs externas (47%) | Vulnerable a bloqueos |
| 10 | Nombres de modelos con "?" sin verificar | Datos no confiables |

### 🟡 Media (7 problemas)

| # | Problema | Impacto |
|---|----------|---------|
| 1 | 70 modelos sin tool number | Búsqueda limitada |
| 2 | 47 biografías vacías o muy cortas | Contenido pobre |
| 3 | 17 diseñadores sin nacionalidad | Info incompleta |
| 4 | 16 series sin imagen | UI menos atractiva |
| 5 | 15 series sin descripción | Info incompleta |
| 6 | HTML de 4.18 MB | Carga lenta |
| 7 | 2 modelos sin imagen | Huecos visuales |

### 🟢 Baja (2 problemas)

| # | Problema | Impacto |
|---|----------|---------|
| 1 | 4 series sin años | Info incompleta |
| 2 | Series con nombres que contienen código wiki | Estética |

---

## 8. Recomendaciones de Mejora

### 8.1 Prioridad Alta

1. **Cachear todas las imágenes localmente** — Descargar las 1,520 imágenes que solo existen como URL externa y guardarlas en `/img`. Esto hará la PWA verdaderamente offline-first.

2. **Limpiar biografías de diseñadores** — Eliminar plantillas `{{Designer|...}}`, wikilinks `[[...]]`, y archivos `[[File:...]]` de las 95 biografías afectadas. Usar regex:
   ```python
   bio = re.sub(r'\{\{[^}]+\}\}', '', bio)
   bio = re.sub(r'\[\[Image:[^\]]+\]\]', '', bio)
   bio = re.sub(r'\[\[File:[^\]]+\]\]', '', bio)
   ```

3. **Limpiar nombres de series** — Eliminar código wiki de los nombres de series (ej: `[[HW J-Imports Mini Collection (2025)|<font color="bl...` → `HW J-Imports Mini Collection (2025)`).

4. **Resolver IDs duplicados** — Regenerar IDs para los 35 duplicados o investigar por qué existen.

5. **Agregar traducción de biografías** — Traducir las biografías de diseñadores al español (o usar un servicio de traducción).

6. **Agregar traducción de fichas** — Traducir las fichas de modelos al inglés.

### 8.2 Prioridad Media

7. **Completar cobertura histórica** — Scrapear los años 1968-1995 más exhaustivamente de Fandom Wiki.

8. **Descargar imágenes faltantes** — Buscar y descargar las 162 imágenes locales faltantes.

9. **Completar biografías vacías** — Buscar las 47 biografías vacías en Fandom Wiki.

10. **Agregar series faltantes** — Agregar las 532 series que están en el catálogo pero no en `series_catalog.json`.

11. **Optimizar HTML** — Considerar separar el JavaScript y CSS en archivos externos para reducir el tamaño inicial.

12. **Agregar nacionalidades faltantes** — Buscar las 17 nacionalidades vacías.

### 8.3 Prioridad Baja

13. **Agregar años a series faltantes** — Completar los 4 series sin años.

14. **Verificar nombres con "?"** — Investigar los 2 modelos con nombres que contienen "?".

15. **Agregar imágenes a series** — Buscar imágenes para las 16 series sin imagen.

---

## 9. Plan de Mejoras

### Fase 1: Corrección de Datos Críticos (Semana 1)

- [ ] Limpiar biografías de diseñadores (95 registros)
- [ ] Limpiar nombres de series (532 registros)
- [ ] Resolver IDs duplicados (35 registros)
- [ ] Descargar imágenes faltantes (162 + 1,520)
- [ ] Verificar nombres con "?" (2 registros)

### Fase 2: Multi Idioma (Semana 2-3)

- [ ] Traducir biografías de diseñadores al español
- [ ] Traducir fichas de modelos al inglés
- [ ] Traducir series al inglés (48 pendientes)

### Fase 3: Cobertura (Semana 3-4)

- [ ] Scrapear años 1968-1995 más exhaustivamente
- [ ] Agregar series faltantes a series_catalog (532)
- [ ] Completar biografías vacías (47)
- [ ] Agregar nacionalidades faltantes (17)

### Fase 4: Optimización (Semana 4-5)

- [ ] Separar JS/CSS en archivos externos
- [ ] Implementar lazy loading de imágenes
- [ ] Optimizar caché de Service Worker
- [ ] Pruebas de rendimiento

---

## 10. Conclusiones

El proyecto Hot Wheels Collector tiene una **base sólida** con 4,391 modelos, 146 diseñadores, 153 tipos de ruedas y 692 series. La cobertura de datos modernos (2016-2026) es buena y comparable con Fandom Wiki.

**Sin embargo, existen problemas críticos que afectan la experiencia del usuario:**

1. **La PWA no es offline-first** — El 47% de las imágenes dependen de URLs externas.
2. **Contenido multi idioma fragmentado** — Cada sección está en un idioma diferente.
3. **Datos sin limpiar** — 65% de las biografías y 532 series tienen código wiki visible.
4. **Cobertura histórica insuficiente** — Los años 1968-1995 tienen muy pocos modelos.

**Los tipos de ruedas son el mejor ejemplo de calidad de datos** — 100% bilingüe, con color, categoría y descripción. Deberían ser el estándar para todas las demás secciones.

**Prioridad inmediata:** Corregir los problemas críticos (imágenes offline, datos sin limpiar, IDs duplicados) antes de agregar más contenido.

---

*Informe generado por Hermes Agent — Hot Wheels Collector Project*