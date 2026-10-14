# PLAN_MULTIUSUARIO.md — Colecciones múltiples, roles y privacidad

> Documento de trabajo para la nueva función multiusuario de HW Collector.
> Fecha: 12-oct-2026 · Estado: **propuesta para revisión** (no implementado)

---

## 1. Resumen ejecutivo

Querés que la app pase de ser **una colección local en un dispositivo** a una **plataforma con cuentas** donde cada coleccionista tiene su colección, se registra con nombre verificado, aporta su ubicación, arranca su colección escaneando al menos 10 autos, y donde los administradores ven estadísticas de valor y las colecciones de los demás.

**La idea es viable y es el camino natural del producto.** Pero tiene **un punto que no se puede implementar como está planteado**: que un administrador vea las colecciones privadas de los usuarios "sin necesidad de permisos". En Chile eso choca de frente con la Ley 21.719 de protección de datos personales (vigente el 1-dic-2026, con multas de hasta 20.000 UTM ≈ US$1,4 millones) y además es una mala práctica de seguridad que ha causado filtraciones reales en apps multi-inquilino.

**La buena noticia:** se puede lograr *casi todo* lo que querés —incluida la visibilidad para administradores— con un diseño que sí es legal y que además es más seguro. La sección 4 lo explica.

---

## 2. Qué pide la idea original, punto por punto

| # | Pedido | Veredicto | Nota |
|---|---|---|---|
| 1 | Múltiples usuarios con su colección propia | ✅ Viable | Requiere backend (hoy la app es 100% estática) |
| 2 | Registro verificado con nombre | ✅ Viable, con matices | "Verificado" hay que definirlo (ver §5) |
| 3 | Tomar geolocalización | ⚠️ Viable con condiciones | Consentimiento explícito + minimización (ver §7) |
| 4 | Escanear ≥10 autos para crear la colección base | ✅ Viable y **buena idea** | Es un onboarding excelente (ver §6) |
| 5 | Guardar privadamente su colección | ✅ Viable | RLS en la base de datos (ver §8) |
| 6 | Valores, ventas y estadísticas solo para admin | ✅ Viable | Con matiz: datos **agregados**, no individuales (ver §4) |
| 7 | Admin ve colecciones de otros sin permisos | ❌ **No se puede así** | Ilegal bajo Ley 21.719 + riesgo de filtración (ver §4) |

---

## 3. El problema legal, concreto

### 3.1 Lo que dice la ley chilena

La **Ley 21.719** (publicada 13-dic-2024) entra en vigencia el **1 de diciembre de 2026** — es decir, en semanas. Reemplaza la Ley 19.628 y crea la Agencia de Protección de Datos Personales con facultades de supervisión, investigación y sanción.

Los artículos que golpean directamente este diseño:

> **Art. 14 bis** — *"El responsable de datos personales y quienes tengan acceso a ellos deberán guardar secreto o confidencialidad acerca de los mismos. El responsable establecerá controles y medidas adecuadas para preservar el secreto o confidencialidad."*

> *"El responsable de datos está obligado a mantener secreto o confidencialidad acerca de los datos personales que conciernan a un titular, **salvo cuando el titular los hubiere hecho manifiestamente públicos**. Este deber subsiste aún después de concluida la relación con el titular."*

Traducción al caso: **una colección privada es un dato personal del usuario.** Que un administrador la lea sin consentimiento viola el deber de confidencialidad. No hay una excepción de "es el admin de la app".

Además, la ley obliga a:
- **Finalidad específica y explícita** (art. 14 letra b): no se puede recolectar "por si acaso"
- **Derechos del titular**: acceso, rectificación, supresión, oposición, portabilidad y bloqueo
- **Consentimiento** como base de licitud para el tratamiento
- Multas de hasta **20.000 UTM** (≈ US$1,39 millones) según gravedad

> Nota: en septiembre de 2026 el Gobierno propuso postergar la vigencia al 1-dic-2027. **Aunque se postergue, el diseño correcto es el mismo** — y hacerlo bien ahora evita una migración dolorosa después.

### 3.2 Por qué además es una mala idea técnica

El consenso de seguridad en sistemas multi-inquilino (OWASP, PostgreSQL) es tajante:

- **"Decide si los administradores internos son de confianza, auditados, con aprobación, o técnicamente impedidos de leer los datos del cliente."** La opción "confianza total" es la que produce las filtraciones.
- Los casos reales de fuga de datos multi-tenant casi siempre vienen de **una ruta de acceso que se saltó el filtro por inquilino** — típicamente un panel de administración.
- Un admin comprometido (phishing, contraseña filtrada) con acceso libre = **fuga de todos los usuarios de una vez**.
- Bajo la Ley 21.719, esa fuga es una infracción gravísima con multa y obligación de notificación.

**El riesgo real:** si el admin ve todo sin control y su cuenta cae, no se filtra una colección — se filtran todas, con nombre, ubicación y valor estimado de cada persona.

---

## 4. Cómo lograr lo que querés, legalmente (y mejor)

En vez de "el admin ve todo", se implementa **visibilidad con consentimiento + acceso auditado**. El administrador obtiene lo que necesita (estadísticas, salud del sistema, detección de abuso) y además puede ver colecciones **cuando el usuario lo autoriza**.

### 4.1 Tres niveles de visibilidad por colección

Cada usuario elige el nivel de su colección, y lo puede cambiar cuando quiera:

| Nivel | Quién la ve | Uso |
|---|---|---|
| **Privada** (por defecto) | Solo el dueño | Nadie más, ni el admin |
| **Compartida** | Dueño + admins autorizados por el usuario | Soporte, verificación, curación |
| **Pública** | Cualquiera con el enlace | Compartir en redes, perfil público |

### 4.2 Lo que el administrador ve siempre (sin necesitar permiso)

Estos son **datos agregados o del sistema**, no datos personales de terceros:

- Cantidad total de usuarios, colecciones y autos registrados
- Distribución de valores (promedio, mediana, percentiles) sobre el **conjunto agregado**
- Modelos más coleccionados, series más completadas
- Autos más escaneados, códigos de barras más consultados
- Mapa de densidad **por comuna/ciudad** (nunca coordenadas de una persona)
- Estado del sistema: sincronizaciones, errores, cuota de IA
- Detección de abuso: cuentas que escanean a ritmo imposible, spam

**Esto es lo valioso para administrar el producto** y no toca la privacidad de nadie.

### 4.3 Lo que el administrador puede ver con autorización

- Colecciones marcadas como **Compartidas** por su dueño
- Colecciones **Públicas** (cualquiera las ve)
- Casos de soporte: el usuario da acceso temporal a su colección, **con registro de quién, cuándo y por qué**

### 4.4 El "break-glass" (acceso de emergencia)

Para casos reales (una denuncia, un requerimiento legal, un incidente), existe un acceso de emergencia que:

1. Exige **motivo escrito** y queda registrado
2. Es **temporal** (expira solo, ej. 24 h)
3. **Notifica al usuario** afectado cuando corresponda
4. Genera una **entrada de auditoría inmutable**

Así el admin tiene la capacidad cuando de verdad se necesita, sin que sea un acceso permanente y silencioso.

### 4.5 Comparación

| | Idea original | Diseño propuesto |
|---|---|---|
| Admin ve colecciones privadas | Siempre, sin permiso | Solo con consentimiento o break-glass auditado |
| Legalidad Ley 21.719 | ❌ Infracción | ✅ Cumple |
| Riesgo si cae la cuenta admin | Fuga total | Fuga limitada a lo compartido |
| Estadísticas de valor | ✅ Sí | ✅ Sí (y mejores: agregadas) |
| El usuario confía y comparte más | Difícil | Sí, porque controla su privacidad |

---

## 5. "Registro verificado con nombre" — qué significa

Hay tres niveles y conviene elegir bien, porque cada uno tiene costo y fricción:

| Nivel | Qué implica | Fricción | Cuándo usarlo |
|---|---|---|---|
| **A. Email verificado** | Cuenta + link de confirmación | Baja | Recomendado para arrancar |
| **B. A + teléfono** | Código SMS | Media (costo por SMS) | Si hay que frenar multicuentas |
| **C. Identidad real** | Documento + selfie (KYC) | Alta (proveedor pago) | Solo si hay dinero de por medio |

**Recomendación:** nivel **A** al inicio. "Verificado" = email confirmado + nombre de perfil elegido por el usuario (no se valida contra documento). Si más adelante se agrega marketplace con pagos, ahí sí se justifica B o C.

**Importante:** el nombre de perfil es dato personal. Debe poder ser un alias y no tiene por qué ser el nombre legal.

---

## 6. Onboarding: la colección base de 10 autos

Esta parte de tu idea es la mejor y hay que pulirla, porque es lo que engancha al usuario.

### 6.1 Flujo propuesto

```
1. Crear cuenta (email + nombre de perfil)
        ↓
2. Consentimientos separados y opcionales:
   [ ] Ubicación (comuna)     → para mapa y estadísticas locales
   [ ] Colección pública      → para perfil compartible
   [ ] Estadísticas anónimas  → para el panel de administración
   (Todos por defecto APAGADOS, se pueden activar después)
        ↓
3. "Armemos tu colección base" — meta: 10 autos
        ↓
   Para cada auto, tres caminos:
   a) 📷 Escanear código de barras (rápido)
   b) 🔍 Buscar por nombre / año / serie
   c) ✍️ Cargar a mano si no está en el catálogo
        ↓
4. Barra de progreso 0/10 → 10/10
   (se puede guardar y seguir después: no bloquear)
        ↓
5. Al llegar a 10: se calcula y muestra
   - Valor de referencia de la colección base
   - Índice de coleccionabilidad promedio
   - Series y años representados
   - Sugerencia: "te faltan 3 autos para completar la serie X"
        ↓
6. Pregunta final: ¿compartir tu colección base?
   [Privada]  [Compartida]  [Pública]
```

### 6.2 Por qué 10 es un buen número

- Suficiente para que las estadísticas tengan sentido (una colección de 1 no dice nada)
- Poco como para no asustar en el registro
- Permite detectar patrones: años, series, clases
- Da una primera "recompensa" (el resumen de valor) que motiva a seguir

### 6.3 Detalles de diseño

- **No bloquear**: si el usuario se cansa en el auto 4, su colección se guarda igual. El contador de "colección base completa" queda pendiente y se lo puede retomar.
- **Modo rápido**: si el usuario ya tiene su colección en otra app o en una planilla, ofrecer **importar CSV** y saltar el escaneo.
- **Detección de duplicados**: al escanear, si el código ya está en su colección, preguntar "¿sumás otra unidad?" en vez de duplicar el registro.
- **Auto no catalogado**: guardar el código de barras crudo y el nombre que escriba el usuario, marcado como "pendiente de catalogar". Alimenta el catálogo.

---

## 7. Geolocalización sin meterse en problemas

La ubicación es **dato personal** y las autoridades (CNIL, EDPB) son muy específicas:

### 7.1 Reglas que hay que cumplir

| Regla | Cómo se implementa |
|---|---|
| **Consentimiento explícito, libre y separado** | Checkbox propio, apagado por defecto, no atado al registro |
| **Minimización** | Guardar **comuna/ciudad**, no coordenadas exactas |
| **No recolección en segundo plano** | Solo se pide cuando el usuario abre el mapa o completa su perfil |
| **Retención limitada** | La ubicación expira (ej. 12 meses) y se pide de nuevo |
| **Derecho a retirar el consentimiento** | Un botón que borra la ubicación y desactiva el mapa |
| **Finalidad explícita** | Decir para qué: "mostrar tu colección en el mapa y comparar precios de tu zona" |

### 7.2 Qué se guarda

```
❌ NO:  lat: -33.4489, lng: -70.6693   (tu casa)
✅ SÍ:  comuna: "Providencia", región: "Metropolitana"
```

Se puede calcular la comuna a partir de las coordenadas **en el dispositivo** y descartar las coordenadas antes de enviarlas al servidor. Así el servidor nunca ve dónde vive exactamente el usuario.

### 7.3 Por qué esto además es mejor producto

El mapa por comuna sirve para lo que querés (densidad de coleccionistas, precios locales, ferias cercanas) **sin** el riesgo de tener en la base de datos la ubicación exacta de cada persona — que es exactamente el dato que más se filtra y más daño hace.

---

## 8. Arquitectura técnica propuesta

### 8.1 El cambio de fondo

Hoy la app es **100% estática** (GitHub Pages + `localStorage`). Multiusuario **exige backend**: base de datos, autenticación y reglas de acceso del lado del servidor.

**Recomendación: Supabase** (plan gratuito).

| Pieza | Qué da | Límite free |
|---|---|---|
| PostgreSQL | Base de datos relacional real | 500 MB |
| Auth | Registro, login, OAuth, email verificado | 50.000 usuarios activos/mes |
| **Row Level Security** | Aislamiento por usuario **en la base de datos** | Ilimitado |
| Storage | Fotos de los autos del usuario | 1 GB |
| Edge Functions | Lógica del servidor | 500.000 llamadas/mes |

**Ventajas frente a Firebase:** es PostgreSQL de verdad (consultas complejas para estadísticas), RLS nativo, y no hay que reescribir el motor de la app.

**Advertencia operativa:** los proyectos gratuitos de Supabase **se pausan tras 7 días sin actividad**. Se reactivan con un clic, sin pérdida de datos, pero hay que tenerlo presente (un ping semanal lo evita).

### 8.2 Diagrama

```
┌─────────────────────────────────────────────────────────┐
│  App (GitHub Pages / PWA)                               │
│  ├─ Catálogo (2.177 autos, estático, offline)           │
│  ├─ Colección local (localStorage, funciona sin cuenta) │
│  └─ Si hay sesión → sincroniza con Supabase             │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS + JWT
┌──────────────────────▼──────────────────────────────────┐
│  Supabase                                               │
│  ├─ Auth      → usuarios, email verificado, sesiones    │
│  ├─ Postgres  → colecciones, autos, auditoría           │
│  │   └─ RLS   → cada usuario ve SOLO lo suyo            │
│  ├─ Vistas    → estadísticas AGREGADAS (sin datos pers.)│
│  └─ Storage   → fotos propias                           │
└─────────────────────────────────────────────────────────┘
```

### 8.3 Principio clave

**La app sin cuenta sigue funcionando igual que hoy.** El multiusuario es una capa que se suma: si el usuario no quiere cuenta, usa la app local como hasta ahora. Esto no rompe nada de lo ya hecho.

---

## 9. Modelo de datos

### 9.1 Tablas

```sql
-- Perfiles (extiende auth.users de Supabase)
create table perfiles (
  id              uuid primary key references auth.users(id) on delete cascade,
  nombre_perfil   text not null check (char_length(nombre_perfil) between 2 and 40),
  email_verificado boolean default false,
  rol             text not null default 'coleccionista'
                  check (rol in ('coleccionista','curador','admin')),
  -- Privacidad: todo apagado por defecto
  visibilidad     text not null default 'privada'
                  check (visibilidad in ('privada','compartida','publica')),
  comuna          text,                    -- solo comuna, nunca coordenadas
  region          text,
  geo_consentida  boolean default false,
  geo_actualizada timestamptz,
  stats_anonimas  boolean default false,   -- aportar a estadísticas agregadas
  creado          timestamptz default now(),
  actualizado     timestamptz default now()
);

-- Colecciones
create table colecciones (
  id          uuid primary key default gen_random_uuid(),
  usuario_id  uuid not null references perfiles(id) on delete cascade,
  nombre      text not null default 'Mi colección',
  es_base     boolean default false,        -- la colección de arranque (10 autos)
  creada      timestamptz default now()
);

-- Autos en una colección
create table autos_coleccion (
  id             uuid primary key default gen_random_uuid(),
  coleccion_id   uuid not null references colecciones(id) on delete cascade,
  usuario_id     uuid not null references perfiles(id) on delete cascade,
  catalog_id     text,                       -- id del catálogo (puede ser null)
  barcode        text,                       -- código de barras escaneado
  nombre_libre   text,                       -- si no está catalogado
  cantidad       int not null default 1 check (cantidad > 0),
  condicion      text not null default 'carded-nuevo',
  ubicacion      text,
  notas          text,
  subcoleccion   text,
  foto_url       text,
  agregado       timestamptz default now(),
  unique (coleccion_id, catalog_id, condicion)
);

-- Auditoría: quién accedió a qué
create table auditoria (
  id           bigserial primary key,
  actor_id     uuid references perfiles(id),
  actor_rol    text,
  accion       text not null,          -- 'ver_coleccion','exportar','break_glass',...
  objetivo_id  uuid,                   -- usuario o colección afectada
  motivo       text,                   -- obligatorio en accesos privilegiados
  expira       timestamptz,            -- para break-glass
  ip           inet,
  user_agent   text,
  creado       timestamptz default now()
);
```

### 9.2 Índices

```sql
create index on autos_coleccion (usuario_id);
create index on autos_coleccion (coleccion_id);
create index on autos_coleccion (catalog_id);
create index on autos_coleccion (barcode);
create index on auditoria (actor_id, creado desc);
create index on perfiles (comuna);
```

---

## 10. Reglas de acceso (RLS)

**Deny by default**: con RLS activado y sin política, nadie ve nada. Cada política es un permiso explícito.

```sql
alter table perfiles         enable row level security;
alter table colecciones      enable row level security;
alter table autos_coleccion  enable row level security;
alter table auditoria        enable row level security;

-- PERFILES: cada uno ve y edita el suyo
create policy "perfil propio: ver" on perfiles
  for select using (auth.uid() = id);

create policy "perfil propio: editar" on perfiles
  for update using (auth.uid() = id);

-- COLECCIONES: el dueño siempre
create policy "coleccion propia" on colecciones
  for all using (auth.uid() = usuario_id);

-- COLECCIONES: los admins SOLO si está compartida o pública
create policy "admin ve compartidas o publicas" on colecciones
  for select using (
    exists (
      select 1 from perfiles p
      where p.id = auth.uid() and p.rol in ('admin','curador')
    )
    and visibilidad in ('compartida','publica')
  );

-- AUTOS: el dueño siempre
create policy "autos propios" on autos_coleccion
  for all using (auth.uid() = usuario_id);

-- AUTOS: admins solo de colecciones compartidas/públicas
create policy "admin ve autos compartidos" on autos_coleccion
  for select using (
    exists (
      select 1 from colecciones c
      join perfiles p on p.id = auth.uid()
      where c.id = autos_coleccion.coleccion_id
        and c.visibilidad in ('compartida','publica')
        and p.rol in ('admin','curador')
    )
  );

-- AUDITORÍA: solo lectura para admins, nadie puede editar ni borrar
create policy "auditoria: solo admin lee" on auditoria
  for select using (
    exists (select 1 from perfiles p
            where p.id = auth.uid() and p.rol = 'admin')
  );
```

### 10.1 Regla de oro

**Nunca confiar en el `usuario_id` que manda el cliente.** El aislamiento se deriva de `auth.uid()` (el token de la sesión), no de un parámetro que el navegador pueda falsificar. Con RLS activo, aunque el código de la app tenga un error y olvide filtrar, **PostgreSQL igual filtra**.

### 10.2 Matriz de permisos

| Acción | Coleccionista | Curador | Admin |
|---|---|---|---|
| Ver/editar su colección | ✅ | ✅ | ✅ |
| Ver colección **pública** de otro | ✅ | ✅ | ✅ |
| Ver colección **compartida** de otro | ❌ | ✅ | ✅ |
| Ver colección **privada** de otro | ❌ | ❌ | ❌ (salvo break-glass auditado) |
| Ver estadísticas agregadas | ❌ | ✅ | ✅ |
| Ver precios de venta y tendencias | ❌ | ✅ | ✅ |
| Cambiar el rol de un usuario | ❌ | ❌ | ✅ |
| Ver el registro de auditoría | ❌ | ❌ | ✅ |
| Exportar datos de otro usuario | ❌ | ❌ | Solo con break-glass + motivo |

---

## 11. Estadísticas para administradores

Lo que el admin ve son **vistas agregadas**, no filas de personas. Ejemplo:

```sql
create or replace view stats_coleccionables as
select
  a.catalog_id,
  count(distinct a.usuario_id) as coleccionistas,
  sum(a.cantidad)              as unidades_totales,
  count(*) filter (where a.condicion = 'carded-nuevo') as en_tarjeta
from autos_coleccion a
join perfiles p on p.id = a.usuario_id
where p.stats_anonimas = true          -- solo de quienes aceptaron
group by a.catalog_id
having count(distinct a.usuario_id) >= 5;   -- mínimo 5 para no exponer a nadie
```

**El umbral de 5 es clave:** si solo 1 persona tiene ese auto, mostrarlo sería revelar su colección. Con `>= 5` la estadística es genuinamente anónima (k-anonimato).

Vistas a construir:
- `stats_coleccionables` — por modelo: cuántos lo tienen, condición, series
- `stats_series` — series más completadas y su valor agregado
- `stats_valor` — distribución de valores (mediana, percentiles) por clase
- `stats_geografia` — densidad por comuna (solo de usuarios que consintieron)
- `stats_actividad` — altas, sincronizaciones, escaneos por día

---

## 12. Sincronización local ↔ nube

La app ya funciona offline. Con cuenta, hay que resolver el conflicto entre lo local y lo remoto:

| Situación | Resolución propuesta |
|---|---|
| Usuario sin cuenta | Solo `localStorage` (como hoy) |
| Usuario con cuenta, online | Se sube y baja automáticamente |
| Usuario con cuenta, offline | Se guarda local y se encola |
| Al reconectar | Se sube la cola y se resuelve el conflicto |
| Mismo auto editado en dos lados | Gana el cambio **más reciente** (`actualizado`), y se avisa |

**Regla:** al crear la cuenta, se ofrece **migrar la colección local** a la nube (una sola vez, con confirmación).

---

## 13. Plan por fases

### Fase 0 — Preparación (1-2 días)
- [ ] Definir los textos legales: política de privacidad y términos de uso
- [ ] Definir la base de licitud de cada dato (qué se pide y para qué)
- [ ] Decidir si "verificado" es solo email (recomendado) o más

### Fase 1 — Backend y cuentas (3-5 días)
- [ ] Crear proyecto en Supabase
- [ ] Ejecutar el esquema SQL (§9) y las políticas RLS (§10)
- [ ] Registro con email verificado
- [ ] Perfil con nombre de perfil y consentimientos separados
- [ ] **Prueba obligatoria de aislamiento**: crear 2 usuarios y verificar que A no puede leer nada de B (ni por API ni por consulta directa)

### Fase 2 — Colecciones en la nube (3-4 días)
- [ ] Migrar la colección local a la nube (con confirmación)
- [ ] Sincronización bidireccional con cola offline
- [ ] Los 3 niveles de visibilidad
- [ ] Fotos propias en Storage

### Fase 3 — Onboarding de los 10 autos (2-3 días)
- [ ] Flujo guiado con barra de progreso
- [ ] Escaneo de código de barras integrado (ya existe el detector)
- [ ] Búsqueda por nombre / año / serie
- [ ] Importar CSV para quien ya tiene su colección
- [ ] Resumen al llegar a 10 (valor, índice, series)

### Fase 4 — Geolocalización con privacidad (2 días)
- [ ] Cálculo de comuna en el dispositivo (nunca enviar coordenadas)
- [ ] Consentimiento explícito y separado
- [ ] Mapa de densidad agregada
- [ ] Botón para borrar la ubicación

### Fase 5 — Panel de administración (3-4 días)
- [ ] Vistas agregadas con k-anonimato (mínimo 5)
- [ ] Gestión de usuarios y roles
- [ ] Registro de auditoría visible
- [ ] Break-glass con motivo y expiración
- [ ] Exportación de datos (con registro)

### Fase 6 — Cumplimiento y cierre (2 días)
- [ ] Derechos del titular: acceso, rectificación, supresión, portabilidad
- [ ] Botón "borrar mi cuenta y mis datos" que borra de verdad
- [ ] Exportar mi colección (portabilidad)
- [ ] Retención de ubicación (expiración a 12 meses)
- [ ] Revisar que ninguna consulta exponga datos de terceros

**Total estimado: 16-23 días de trabajo efectivo.**

---

## 14. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Fuga de datos por el panel admin | Crítico (multa + daño) | RLS + break-glass auditado + sin acceso libre |
| RLS mal configurado deja datos expuestos | Crítico | Probar el aislamiento con 2+ cuentas antes de publicar |
| Supabase pausa el proyecto por inactividad | Medio | Ping semanal automático |
| Usuario no entiende los consentimientos | Medio | Textos claros, todo apagado por defecto, explicar el beneficio |
| Geolocalización mal usada | Alto (legal) | Solo comuna, opt-in, expira, se puede borrar |
| Cuenta admin comprometida | Alto | 2FA obligatorio para roles admin |
| La app se vuelve dependiente de la nube | Medio | El modo local sigue funcionando igual que hoy |
| Costos al crecer | Bajo | Free tier hasta ~500 MB; plan Pro US$25/mes si se supera |

---

## 15. Decisiones tomadas

| # | Decisión | Elegido | Fecha |
|---|---|---|---|
| 1 | Acceso de admin a colecciones privadas | ⏸️ **PENDIENTE** — no se asume; se retoma antes de la Fase 5 | — |
| 2 | Nivel de verificación | ✅ **Solo email verificado** (rápido, gratis) | 12-oct-2026 |
| 3 | Colección base de 10 autos | ✅ **Sugerida** — se motiva con progreso, **no bloquea** | 12-oct-2026 |
| 4 | Precisión de ubicación | ✅ **Comuna/ciudad**, calculada en el celular (nunca coordenadas) | 12-oct-2026 |
| 5 | Alcance | ✅ **Plan completo** (6 fases, 16-23 días) | 12-oct-2026 |
| 6 | Quién ve las estadísticas | Por definir (recomendado: admin y curador) | — |
| 7 | Migración de la colección local | Por definir (recomendado: preguntar al crear cuenta) | — |

> **Nota sobre la decisión 1:** las Fases 1 a 4 **no dependen** de ella (cuentas, colecciones, onboarding y geolocalización funcionan con el modelo de privacidad por defecto). La Fase 5 (panel de administración) sí la necesita resuelta.

### 15.1 Estado de implementación

| Fase | Estado |
|---|---|
| 0 — Preparación legal | ⏳ En curso |
| 1 — Backend y cuentas | ✅ **Esquema aplicado y verificado** (12-oct-2026) |
| 2 — Colecciones en la nube | Pendiente (código del cliente) |
| 3 — Onboarding 10 autos | Pendiente |
| 4 — Geolocalización | Pendiente |
| 5 — Panel de administración | ⏸️ Bloqueada por decisión 1 |
| 6 — Cumplimiento | Pendiente |

**Proyecto Supabase:** `wgoqtqwxikqhrgulclqk` · ver `supabase/VERIFICACION_SUPABASE.md`

Verificado el 12-oct-2026:
- ✅ Las 5 tablas creadas
- ✅ RLS activo (los 4 intentos de escritura sin autenticación fueron rechazados con `42501`)
- ✅ Las vistas de estadísticas fuera del alcance del rol `anon`
- ⏳ Falta la prueba con 2 usuarios autenticados (requiere crearlos desde el panel)

### 15.2 Cómo se aplica el plan

El código de la base vive en `supabase/`:

```
supabase/
  01_schema.sql     → tablas, índices y tipos
  02_policies.sql   → Row Level Security (deny by default)
  03_views.sql      → estadísticas agregadas con k-anonimato
  04_seed.sql       → datos de prueba (2 usuarios para validar el aislamiento)
  README.md         → guía de puesta en marcha paso a paso
```

**Orden de ejecución:** `01` → `02` → `03`. El `04` es solo para pruebas.


---

## 16. Lo que NO cambia

Para que quede claro el alcance:

- ✅ El **catálogo de 2.177 autos** sigue igual, estático y offline
- ✅ El **asistente con IA** (Groq) sigue igual
- ✅ La app **sigue funcionando sin cuenta**, como hoy
- ✅ El **puente** con la PC sigue siendo opcional
- ✅ **GitHub Pages** sigue siendo el host de la app

El multiusuario es **una capa nueva encima**, no un reemplazo.

---

## 17. Referencias

**Legales (Chile)**
- Ley 21.719 — Protección de Datos Personales · https://www.bcn.cl/leychile/Navegar?idNorma=1209272
- Guía práctica de implementación (Gobierno Digital) · https://wikiguias.digital.gob.cl/es/datos-personales/guia-practica-implementacion-nueva-ley-datos-personales
- Propuesta de postergación a dic-2027 · https://www.economia.gob.cl/2026/09/01/gobierno-propone-ampliar-plazo-para-implementar-nueva-ley-de-proteccion-de-datos-y-institucionalidad.htm

**Seguridad multi-inquilino**
- OWASP — Multi Tenant Security Cheat Sheet · https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html
- PostgreSQL Row Level Security (documentación oficial)

**Privacidad y geolocalización**
- CNIL — Géolocalisation et applications mobiles · https://www.cnil.fr/fr/geolocalisation-applications-mobiles-quelles-regles
- EDPB — Guidelines 04/2020 on location data

**Infraestructura**
- Supabase — Precios y límites del plan gratuito · https://supabase.com/pricing

---

*Documento generado como propuesta de trabajo. No implementado todavía.*
