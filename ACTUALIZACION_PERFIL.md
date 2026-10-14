# ACTUALIZACION_PERFIL.md — Perfil de coleccionista, avatar y cierre de modal

> Actualización de la funcionalidad de cuenta y perfil en HW Collector.
> Fecha: 12-oct-2026 · Estado: **propuesta con fixes listos para aplicar**

---

## 1. Bug encontrado: el modal no se cierra

### Síntomo
Al crear una cuenta (o entrar), el modal **permanece abierto** y el usuario no recibe una señal clara de que la operación terminó.

### Causa raíz
En `hacerRegistro()`, cuando el registro requiere confirmación por email (`r.necesitaConfirmar === true`), la función **no llama `toggleCuenta()`**. Solo muestra un mensaje dentro del modal, que queda abierto.

En `hacerLogin()` sí se cierra, pero el cierre y el mensaje están mezclados, y si `sincronizarDesde()` falla, el usuario queda con el modal cerrado sin saber qué pasó.

### Fix
Cerrar el modal **siempre** después de una operación exitosa, y mover el mensaje de resultado al **log de la app** (no dentro del modal):

```js
async function hacerRegistro(){
  // ...validar y llamar a SBClient.registrar...
  if(r.error){ logMsg('a', r.error); return; }        // error: modal queda abierto (bien)
  logMsg('i', r.necesitaConfirmar
    ? 'Cuenta creada. <b>Revisá tu email</b> para confirmarla.'
    : 'Cuenta creada y sesión iniciada. ¡Bienvenido!');
  toggleCuenta();                                       // ← SIEMPRE cerrar
  if(!r.necesitaConfirmar) SBClient.refrescarBadgeCuenta();
}

async function hacerLogin(){
  // ...validar y llamar a SBClient.iniciarSesion...
  if(r.error){ logMsg('a', r.error); return; }
  logMsg('i','Bienvenido de nuevo.');
  toggleCuenta();                                       // ← SIEMPRE cerrar
  SBClient.refrescarBadgeCuenta();
  SBClient.sincronizarDesde().catch(()=>{});           // sync en background, sin bloquear
}
```

### Regla de diseño
> **Un modal de auth nunca queda abierto después de una operación exitosa.**
> El resultado se comunica en el log (persistente, con historial), no en el modal (transitorio).

---

## 2. Investigación: tipos de coleccionistas

### 2.1 Qué dice la comunidad

La distinción entre **coleccionista** y **revendedor** es de las más sensibles en la comunidad de Hot Wheels (r/HotWheels, foros de numismática):

> *"Collectors =/= resellers. Please don't confuse the two groups of people."* — u/kratos1394, r/HotWheels

> *"Flippers are not collectors; they are opportunists profiting from someone else's passion."* — r/HotWheels

> *"I have been collecting for over 20 years and I don't think I've ever sold anything except mainlines I had extras of, and never for more than what I paid for them. When I find something valuable, I buy it and keep it. That is how real collectors roll."* — r/HotWheels

La comunidad distingue con claridad:
- **Coleccionista**: conserva, no vende (o vende lo mínimo).
- **Revendedor / Flipper**: compra para revender, a menudo a 2-3× el retail.
- **Coleccionista que vende**: un punto medio — vende excedentes o piezas que ya no le interesan, pero no es su negocio principal.

### 2.2 Tipos de coleccionistas (taxonomía consolidada)

Combinando la literatura de coleccionismo (numismática, filatelia) con la comunidad de Hot Wheels:

| Tipo | Motivación principal | Vende? | Perfil |
|---|---|---|---|
| **Coleccionista privado** | Pleno personal, nostalgia, estética | ❌ Nunca (o solo excedentes sin ánimo de lucro) | "Guarda todo" |
| **Coleccionista que vende** | Colecciona, pero rota piezas | ⚠️ Ocasionalmente, para financiar la colección | "Vende para seguir comprando" |
| **Revendedor (Flipper)** | Ganancia a corto plazo | ✅ Sí, es su negocio | "Compra para revender" |
| **Inversor** | Valorización a largo plazo | ✅ Cuando el valor sube | "Mantiene, espera, vende caro" |
| **Completista** | Tener toda la serie/colección | ❌ No, le faltan piezas | "Busca los que le faltan" |
| **Especialista** | Un tema, marca o era específica | ⚠️ Si no encaja en su foco | "Solo lo que me interesa" |

### 2.3 Los tres que pidió el usuario

| Opción | Descripción | Uso en la app |
|---|---|---|
| **Revendedor** | Compra para revender. Puede usar la app para gestionar inventario, precios y ventas. | Etiqueta pública si el usuario quiere ser encontrado por compradores. |
| **Coleccionista que vende** | Colecciona, pero vende excedentes o piezas que ya no le interesan. | Etiqueta pública para intercambios y ventas ocasionales. |
| **Coleccionista privado** | Compra para su propia colección, no vende. | Sin etiqueta de venta; perfil orientado a mostrar y organizar. |

### 2.4 Recomendación

Ofrecer las **tres opciones** que pidió el usuario, más una cuarta que la comunidad usa mucho:

| Valor | Nombre en la app | Descripción corta |
|---|---|---|
| `privado` | Coleccionista privado | Colecciono para mí, no vendo |
| `vendedor` | Coleccionista que vende | Vendo excedentes para seguir coleccionando |
| `revendedor` | Revendedor | Compro para revender, es parte de mi negocio |
| `inversor` | Inversor | Mantengo a largo plazo por su valor |

> **Nota de privacidad:** el tipo de coleccionista es dato personal. Debe ser **opcional** y el usuario debe poder cambiarlo cuando quiera. Si se muestra públicamente, debe ser solo si el usuario lo consiente.

---

## 3. Diseño de perfiles: qué funciona

### 3.1 Patrones de UX verificados

Basado en la investigación de diseño de perfiles de usuario:

| Elemento | Recomendación | Por qué |
|---|---|---|
| **Avatar** | 96-128 px, circular | Tamaño ideal para mobile y desktop |
| **Nombre** | 1-2 líneas, prominente | Identidad principal |
| **Bio / descripción** | 1-3 líneas, máx. ~200 caracteres | Sin overflow, scanneable |
| **Tipo de coleccionista** | Badge/chip pequeño bajo el nombre | Identidad secundaria, no intrusivo |
| **Stats strip** | 3-4 números (autos, series completadas, valor) | "Social proof" inmediato |
| **Acción primaria** | "Editar perfil" | En modales, "Cerrar"; en página, "Editar" |

### 3.2 Estructura propuesta del perfil

```
┌─────────────────────────────────────────┐
│  [Avatar 96px]   Nombre de perfil       │
│                  [Tipo de coleccionista] │
│                  "Coleccionista privado" │
│                                         │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │
│  │  11  │ │  3   │ │  2   │ │ $XXX │  │
│  │autos │ │series│ │años │ │valor │  │
│  └──────┘ └──────┘ └──────┘ └──────┘  │
│                                         │
│  Bio: "Colecciono Muscle Cars y JDM..." │
│  (máx. 3 líneas)                        │
│                                         │
│  [Editar perfil]                        │
└─────────────────────────────────────────┘
```

### 3.3 Reglas

- **Header del perfil < 200px en mobile** — que el contenido principal sea visible sin scrollear
- **3-4 stats** — suficientes para dar una idea, sin abrumar
- **Editar es la acción primaria** — siempre visible, no esconderla
- **El tipo de coleccionista es editable** — no es una etiqueta permanente

---

## 4. Avatar: cómo generarlo sin fotos ni backend

### 4.1 Opción recomendada: DiceBear

**DiceBear** es una librería open source (MIT) que genera avatares SVG deterministas a partir de un "seed":

| Característica | Valor |
|---|---|
| Gratis | ✅ 100% (no comercial) |
| API key | ❌ No requiere |
| Estilos | 61 (pixel-art, lorelei, bottts, adventurer-neutral, etc.) |
| Determinista | ✅ Mismo seed = mismo avatar |
| Formato | SVG (escala infinita), PNG, WebP, AVIF |
| Rate limit | 50 req/s para SVG |
| Licencia | MIT (algunos estilos CC0, otros CC-BY-4.0) |

**URL de ejemplo:**
```
https://api.dicebear.com/10.x/pixel-art/svg?seed=foxnismo
https://api.dicebear.com/10.x/lorelei/svg?seed=foxnismo
https://api.dicebear.com/10.x/bottts/svg?seed=foxnismo
```

### 4.2 Por qué DiceBear y no otras

| Opción | Problema |
|---|---|
| **Gravatar** | Requiere que el usuario tenga cuenta Gravatar con foto |
| **UI Avatars** | Solo iniciales, muy básico |
| **Subir foto** | Requiere backend de Storage (más complejo) + permisos de cámara |
| **Iniciales** | Aburrido, no distingue a usuarios |
| **DiceBear** | ✅ Sin backend, sin key, determinista, bonito |

### 4.3 Seed: qué usar

El seed determina el avatar. Opciones:

| Seed | Ventaja | Desventaja |
|---|---|---|
| **Email** | Único por usuario | Si cambia de email, cambia el avatar |
| **User ID (UUID)** | Nunca cambia | Hay que generar el UUID antes |
| **Nombre de perfil** | Legible | Puede cambiar, puede colisionar |

**Recomendación:** usar el **email** como seed. Es único, estable, y si el usuario cambia de email, el avatar cambia (aceptable). Alternativa: hash SHA-256 del email para anonimizar.

### 4.4 Estilos recomendados para Hot Wheels

| Estilo | Look | Licencia |
|---|---|---|
| `pixel-art` | 8-bit, retro gamer | CC0 |
| `bottts` | Robots simpáticos | CC0 |
| `adventurer-neutral` | Caras minimalistas | CC-BY-4.0 (atribución) |
| `lorelei` | Ilustrados, coloridos | CC0 |
| `thumbs` | Pulgares, simples | CC0 |

**Recomendación:** `pixel-art` (CC0, encaja con la estética de juguete/retro de Hot Wheels) o `bottts` (CC0, divertido).

---

## 5. Especificación de la actualización

### 5.1 Cambios en el esquema de datos

```sql
-- Nuevos campos en perfiles
alter table public.perfiles add column if not exists avatar_url text;
alter table public.perfiles add column if not exists bio text check (char_length(bio) <= 200);
alter table public.perfiles add column if not exists tipo_coleccionista text
  check (tipo_coleccionista in ('privado','vendedor','revendedor','inversor'));

-- Índice para búsquedas por tipo
create index if not exists idx_perfiles_tipo on public.perfiles (tipo_coleccionista)
  where tipo_coleccionista is not null;
```

### 5.2 Flujo de perfil (post-login)

```
Login exitoso
   ↓
Modal se cierra (fix)
   ↓
Badge muestra email
   ↓
Perfil se carga con:
  ├─ Avatar (DiceBear con seed=email)
  ├─ Nombre de perfil
  ├─ Tipo de coleccionista (editable, opcional)
  ├─ Bio (editable, máx. 200 caracteres)
  ├─ Stats: autos, series, años, valor estimado
  ├─ Privacidad (ya existe)
  └─ Botón "Editar perfil"
```

### 5.3 Modal de edición de perfil

```
┌─────────────────────────────────┐
│  [Avatar 96px]  Cambiar avatar  │ ← genera uno nuevo de DiceBear
│                                 │
│  Nombre de perfil:              │
│  [________________________]      │
│                                 │
│  Tipo de coleccionista:         │
│  [Seleccionar ▾]                │
│   • Coleccionista privado       │
│   • Coleccionista que vende     │
│   • Revendedor                  │
│   • Inversor                    │
│                                 │
│  Bio (máx. 200 caracteres):     │
│  [________________________]      │
│  [________________________]      │
│  123 / 200                      │
│                                 │
│  Privacidad de la colección:    │
│  [Privada ▾]                    │
│                                 │
│  [Guardar]  [Cancelar]          │
└─────────────────────────────────┘
```

### 5.4 Stats del perfil

| Stat | Fuente | Cálculo |
|---|---|---|
| **Autos** | `autos_coleccion` | `sum(cantidad)` |
| **Modelos distintos** | `autos_coleccion` | `count(distinct catalog_id)` |
| **Valor estimado** | `autos_coleccion` + catálogo | `sum(cantidad × valor_ref × factor_condicion)` |
| **Serie más representada** | `autos_coleccion.subcoleccion` | `mode(subcoleccion)` |

### 5.5 Privacidad del perfil

| Dato | Por defecto | Visible a |
|---|---|---|
| Nombre de perfil | — | Cualquiera (si la colección es pública) |
| Avatar | Generado | Cualquiera |
| Bio | Vacío | Cualquiera (si la colección es pública) |
| Tipo de coleccionista | NULL (no especificado) | Solo si el usuario lo marca como público |
| Email | — | Nunca público (solo el usuario y el staff) |
| Comuna | NULL | Solo si `geo_consentida` |
| Stats | Agregadas | Solo si `stats_anonimas` |

---

## 6. Verificación

### Tests manuales

| # | Test | Esperado |
|---|---|---|
| 1 | Crear cuenta sin confirmación | Modal se cierra, log muestra "Bienvenido" |
| 2 | Crear cuenta con confirmación | Modal se cierra, log muestra "Revisá tu email" |
| 3 | Login exitoso | Modal se cierra, badge muestra email |
| 4 | Login fallido | Modal queda abierto, log muestra el error |
| 5 | Ver perfil | Avatar generado, nombre, bio, tipo, stats |
| 6 | Editar perfil | Cambios guardados, avatar nuevo si se regenera |
| 7 | Cambiar tipo | Se guarda y muestra en el perfil |
| 8 | Bio con 201 caracteres | Se rechaza o trunca a 200 |

### Tests de aislamiento (con dos usuarios)

| # | Test | Esperado |
|---|---|---|
| 9 | El usuario A ve su perfil | ✅ Sus datos |
| 10 | El usuario B ve el perfil de A | ❌ Solo si A lo hizo público |
| 11 | El email de A nunca es visible | ❌ Nunca |

---

## 7. Referencias

**Comunidad Hot Wheels**
- r/HotWheels — *"Collectors =/= resellers"* · https://www.reddit.com/r/HotWheels/comments/ykodwt/
- r/HotWheels — *"Resellers are a Necessity"* · https://www.reddit.com/r/HotWheels/comments/1mrm24q/
- Jalopnik — *"Collecting Hot Wheels Sucks Right Now"* · https://www.jalopnik.com/collecting-hot-wheels-sucks-resellers-scalpers-die-cast-1850197356/

**Taxonomía de coleccionismo**
- Wikipedia — *Coleccionismo de monedas* · https://es.wikipedia.org/wiki/Coleccionismo_de_monedas
- APMEX — *Numismatist vs Coin Collectors* · https://learn.apmex.com/learning-guide/coin-collecting/what-is-a-numismatist/

**Diseño de perfiles**
- Gummble — *Profile UI Design Patterns* · https://gummble.com/patterns/profile
- Pixso — *User Avatar Design* · https://pixso.net/articles/user-avatar-design/

**Avatares**
- DiceBear — HTTP API · https://www.dicebear.com/integrations/http-api/
- DiceBear — Estilos · https://www.dicebear.com/styles/

---

*Parte del plan multiusuario en `../PLAN_MULTIUSUARIO.md`*
