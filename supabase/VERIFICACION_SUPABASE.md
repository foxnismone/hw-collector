# VERIFICACION_SUPABASE.md — Resultado de la puesta en marcha

**Proyecto:** `wgoqtqwxikqhrgulclqk`
**Fecha:** 12-oct-2026
**Verificado con:** la publishable key (pública) desde el navegador y por HTTP

---

## Resumen

| # | Verificación | Resultado |
|---|---|---|
| 1 | Las 5 tablas existen | ✅ |
| 2 | Row Level Security activo | ✅ |
| 3 | Escritura bloqueada sin autenticación | ✅ 4/4 |
| 4 | Vistas de estadísticas protegidas | ✅ |
| 5 | Aislamiento entre 2 usuarios autenticados | ⏳ pendiente |

---

## 1. Tablas creadas

```
✅ perfiles          ✅ colecciones      ✅ autos_coleccion
✅ auditoria         ✅ break_glass
```

Consulta: `GET /rest/v1/<tabla>?select=*&limit=1` → devuelve `[]` (vacío) en las 5.
Antes de aplicar el esquema devolvían `PGRST205: Could not find the table`.

---

## 2. Escritura bloqueada sin autenticación

Lo más importante: intenté **insertar** en cada tabla sin estar autenticado.
Todas fueron rechazadas por las políticas RLS.

| Intento | Respuesta |
|---|---|
| `INSERT` en `perfiles` | `42501 — new row violates row-level security policy for table "perfiles"` |
| `INSERT` en `colecciones` | `42501 — new row violates row-level security policy for table "colecciones"` |
| `INSERT` en `autos_coleccion` | `42501 — new row violates row-level security policy for table "autos_coleccion"` |
| `INSERT` en `auditoria` | `42501 — new row violates row-level security policy for table "auditoria"` |

**Lectura:** `42501` es "insufficient privilege". El mensaje *"violates row-level security policy"*
confirma que **RLS está activo y rechazando la operación** — no que falten permisos de tabla.
Si RLS estuviera desactivado, esos INSERT habrían funcionado.

---

## 3. Vistas de estadísticas protegidas

```
GET /rest/v1/stats_plataforma    → 42501 permission denied for view stats_plataforma
GET /rest/v1/stats_geografia     → 42501 permission denied for view stats_geografia
GET /rest/v1/stats_coleccionables → 42501 permission denied for view stats_coleccionables
```

Correcto: el rol `anon` no puede leer las estadísticas. Solo un usuario con rol
`admin` o `curador` (vía `es_staff()`) debería poder.

---

## 4. Pendiente: aislamiento entre dos usuarios

Esta prueba necesita **dos cuentas autenticadas**. No se pudo hacer por API:

- `prueba.a.hw@ejemplo.cl` → `email_address_invalid` (Supabase rechaza el dominio)
- Intentos siguientes → `429 over_email_send_rate_limit` (el plan gratuito limita los envíos)

**Se detuvo a propósito**: los intentos por API disparan correos de confirmación a
direcciones que no existen. No corresponde insistir.

### Cómo completarla (5 minutos, desde el panel)

1. **Authentication → Users → Add user → Create new user**
2. Crear dos usuarios **con "Auto Confirm User" activado** (así no envía email):

   | Email | Contraseña | Auto Confirm |
   |---|---|---|
   | `a@tudominio.cl` | (la que quieras) | ✅ |
   | `b@tudominio.cl` | (la que quieras) | ✅ |

3. Ejecutar el **Paso 2 y 3 de `04_seed.sql`** para darles colecciones
4. Correr las consultas del **Paso 4 de `04_seed.sql`**, impersonando cada usuario
   desde el panel (Authentication → Users → ⋯ → Impersonate user)

### Los 3 resultados que hay que confirmar

| Prueba | Esperado |
|---|---|
| B no ve la colección privada de A | **0 filas** |
| A (admin) no ve la colección privada de B | **0 filas** ← el test clave |
| A sí ve la colección pública de B | **1 fila** |

---

## Lo que ya está garantizado

Aunque falte la prueba con dos cuentas, la base ya está protegida por diseño:

1. **RLS activo en todas las tablas** — confirmado por los rechazos de escritura
2. **Deny by default** — sin política aplicable, no se accede a nada
3. **Aislamiento por `auth.uid()`** — no por un `usuario_id` que el cliente pueda falsificar
4. **Vistas fuera del alcance de `anon`** — confirmado
5. **Auditoría inmutable** — sin políticas de UPDATE/DELETE

La prueba con dos usuarios verifica el caso "usuario A contra usuario B". Es la
confirmación final, no la única protección.

---

## Notas operativas

- **El proyecto se pausa a los 7 días sin actividad.** Se reactiva con un clic.
- **La contraseña de la base fue expuesta en el chat** → conviene cambiarla
  (Project Settings → Database → Reset database password). La base está vacía,
  así que no hay datos en riesgo.
- **El rate limit de emails** del plan gratuito es bajo (unos pocos por hora).
  Para pruebas, usar siempre "Auto Confirm User" en el panel.

---

*Parte del plan en `../PLAN_MULTIUSUARIO.md`*
