# supabase/ — Puesta en marcha del backend multiusuario

Guía para dejar andando la parte de cuentas y colecciones de HW Collector.

**Tiempo total: ~15 minutos.** Todo con el plan gratuito de Supabase (sin tarjeta).

---

## Requisitos

- Una cuenta en [supabase.com](https://supabase.com) (se crea con GitHub o email)
- Nada más: no hace falta instalar software

---

## Paso 1 — Crear el proyecto (3 min)

1. Entrá a **https://supabase.com/dashboard** → **New project**
2. Completá:
   - **Name**: `hw-collector`
   - **Database Password**: generá una fuerte y **guardala** (la vas a necesitar)
   - **Region**: elegí la más cercana — para Chile, **South America (São Paulo)**
3. Esperá ~2 minutos mientras provisiona

---

## Paso 2 — Ejecutar el esquema (5 min)

En el panel del proyecto: **SQL Editor** → **New query**.

Ejecutá los archivos **en este orden**, uno por uno (copiá y pegá el contenido completo, después **Run**):

| Orden | Archivo | Qué crea |
|---|---|---|
| 1️⃣ | `01_schema.sql` | Tablas, índices, triggers y funciones auxiliares |
| 2️⃣ | `02_policies.sql` | Row Level Security (el aislamiento entre usuarios) |
| 3️⃣ | `03_views.sql` | Estadísticas agregadas con k-anonimato |

> ⚠️ **No saltees el orden.** Las políticas (2) necesitan las tablas (1), y las vistas (3) necesitan las funciones de las políticas.

Al terminar, verificá que todo quedó bien:

```sql
-- Todas deben mostrar relrowsecurity = true
select relname, relrowsecurity
from pg_class
where relname in ('perfiles','colecciones','autos_coleccion','auditoria','break_glass');

-- Cuántas políticas quedaron por tabla
select tablename, count(*) as politicas
from pg_policies
where schemaname = 'public'
group by tablename
order by tablename;
```

**Esperado:** las 5 tablas con `relrowsecurity = true` y políticas en las 5.

---

## Paso 3 — Configurar la autenticación (3 min)

En el panel: **Authentication** → **Sign In / Providers**:

- ✅ **Email** habilitado
- ✅ **Confirm email** activado (así el registro queda verificado de verdad)
- ❌ Desactivá los proveedores que no uses

Después, en **Authentication** → **URL Configuration**:

- **Site URL**: `https://foxnismone.github.io/hw-collector/`
- **Redirect URLs**: agregá la misma

Esto es necesario para que los enlaces de confirmación por email vuelvan a la app.

---

## Paso 4 — Obtener las claves (2 min)

**Project Settings** → **API**. Vas a necesitar dos datos:

| Dato | Dónde está | ¿Es secreto? |
|---|---|---|
| **Project URL** | `https://xxxxx.supabase.co` | No |
| **anon public key** | Un JWT largo que empieza con `eyJ...` | **No** — está diseñada para ir en el navegador |

> ⚠️ **NUNCA** uses la clave `service_role` en la app. Esa **sí** es secreta: salta todas las políticas RLS. Si se filtra, cualquiera lee toda la base. Solo va en scripts de servidor.

La `anon key` es pública por diseño: la protección real no es la clave, son **las políticas RLS**. Aunque alguien tenga la anon key, no puede leer datos de otros usuarios.

---

## Paso 5 — Conectar la app (2 min)

Hay dos formas. Elegí una:

### Opción A — Pegarla en la app (más simple)

En la app → pestaña **Cuenta** (o donde se indique) → pegá la URL y la anon key. Se guardan en `localStorage` del navegador.

### Opción B — En el build (si preferís que venga configurada)

Editá `build/build_app.py` y completá:

```python
SUPABASE_URL = "https://xxxxx.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOi..."
```

Y regenerá: `python build/build_app.py`

> Como la anon key es pública, no hay problema en que quede en el repo. La seguridad está en las políticas RLS.

---

## Paso 6 — PROBAR EL AISLAMIENTO (obligatorio, 5 min)

**Este paso no se puede saltear.** Un error acá significa que un usuario puede leer los datos de otro.

### 6.1 Crear dos usuarios de prueba

**Authentication** → **Users** → **Add user** → **Create new user**:

| Email | Contraseña | Auto Confirm |
|---|---|---|
| `usuario.a@ejemplo.cl` | `probar1234` | ✅ |
| `usuario.b@ejemplo.cl` | `probar1234` | ✅ |

### 6.2 Cargar los datos de prueba

En el **SQL Editor**, ejecutá `04_seed.sql` (los pasos 2 y 3; los comentados no).

### 6.3 Correr las pruebas

Seguí las consultas del **Paso 4 de `04_seed.sql`**. Las tres que importan:

| Prueba | Cómo | Esperado |
|---|---|---|
| **(a)** B no ve la colección privada de A | Impersonar B y consultar | **0 filas** |
| **(d)** A (admin) no ve la colección privada de B | Impersonar A y consultar | **0 filas** ← el test clave |
| **(e)** A sí ve la colección pública de B | Poner la de B como pública | **1 fila** |

**Cómo impersonar un usuario:** en **Authentication** → **Users**, menú de los tres puntos del usuario → **Impersonate user**. El SQL Editor pasa a ejecutar como ese usuario, y así se prueba qué ve de verdad.

### 6.4 Pruebas adicionales

```sql
-- (f) Las estadísticas NO aparecen con menos de 5 personas
select * from public.stats_coleccionables;   -- esperado: 0 filas (hay 2 usuarios)

-- (h) La auditoría no se puede modificar
update public.auditoria set motivo = 'alterado' where id = 1;   -- esperado: error de permiso
```

**Si alguna prueba falla, no publiques.** Revisá que `02_policies.sql` se haya ejecutado completo.

---

## Estructura de la base

```
perfiles          → un registro por cuenta (nombre, rol, privacidad, comuna)
colecciones       → varias por usuario; la "base" es la del onboarding
autos_coleccion   → los autos, con condición, ubicación, subcolección y foto
auditoria         → historial inmutable de accesos y cambios sensibles
break_glass       → accesos de emergencia con motivo y expiración
```

### Vistas de estadísticas (solo staff)

```
stats_coleccionables   → por modelo: cuántos coleccionistas lo tienen
stats_series           → series declaradas por los usuarios
stats_condicion        → estado de las piezas (en tarjeta / sueltas)
stats_geografia        → densidad por comuna
stats_actividad        → altas y escaneos por día
stats_plataforma       → salud general (usuarios, verificados, etc.)
stats_top_modelos      → ranking para el panel
stats_sin_catalogar    → códigos escaneados que no están en el catálogo
```

**Todas aplican k-anonimato:** si menos de **5 personas** sostienen un dato, no se muestra. Así no se puede deducir la colección de nadie.

---

## Notas operativas

### El proyecto gratuito se pausa a los 7 días sin actividad

Supabase pausa los proyectos del plan free tras una semana sin consultas. Se reactiva con un clic desde el panel, **sin pérdida de datos**, pero mientras está pausado la app no sincroniza.

**Mitigación:** dejá un ping semanal. Se puede con un cron que haga una consulta simple, o abriendo el panel de vez en cuando.

### Límites del plan gratuito

| Recurso | Límite | Alcanza para |
|---|---|---|
| Base de datos | 500 MB | ~500.000 filas |
| Usuarios activos | 50.000/mes | Muchísimo |
| Storage (fotos) | 1 GB | ~2.000 fotos de 500 KB |
| Transferencia | 5 GB/mes | ~1.000 usuarios diarios |

Si se supera, el plan Pro son US$25/mes.

### Copias de seguridad

El plan gratuito no incluye backups automáticos. Para exportar:

```bash
# Requiere pg_dump y la contraseña de la base
pg_dump "postgresql://postgres:[PASSWORD]@db.[PROYECTO].supabase.co:5432/postgres" > respaldo.sql
```

---

## Cumplimiento (Ley 21.719)

Lo que ya está resuelto en el esquema:

- ✅ **Consentimiento separado** por finalidad (`geo_consentida`, `stats_anonimas`), apagados por defecto
- ✅ **Minimización**: se guarda comuna, nunca coordenadas
- ✅ **Confidencialidad**: ni el admin lee colecciones privadas (art. 14 bis)
- ✅ **Acceso privilegiado auditado**: `break_glass` exige motivo, expira y deja rastro
- ✅ **Derecho de supresión**: `on delete cascade` desde `auth.users` borra todo
- ✅ **Portabilidad**: los datos son consultables y exportables por su dueño

Lo que falta implementar (Fase 6):

- [ ] Textos de política de privacidad y términos de uso
- [ ] Botón "borrar mi cuenta y mis datos" en la app
- [ ] Botón "exportar mi colección" (portabilidad)
- [ ] Expiración automática de la ubicación a los 12 meses
- [ ] Registro de qué finalidad justifica cada dato

---

## Referencias

- [Supabase — Precios y límites](https://supabase.com/pricing)
- [Supabase — Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [OWASP — Multi Tenant Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html)
- [Ley 21.719 — Protección de Datos Personales (Chile)](https://www.bcn.cl/leychile/Navegar?idNorma=1209272)

---

*Parte del plan en `../PLAN_MULTIUSUARIO.md`*
