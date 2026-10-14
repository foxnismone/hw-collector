-- ============================================================================
--  HW Collector — ESQUEMA MULTIUSUARIO COMPLETO
--  Pegá TODO este archivo en el SQL Editor de Supabase y presioná Run.
--  Incluye: tablas + políticas RLS + vistas de estadísticas.
-- ============================================================================

-- ═══════════════════════════════════════════════════════════
--  01_schema.sql
-- ═══════════════════════════════════════════════════════════

-- ============================================================================
--  HW Collector — Multiusuario
--  01_schema.sql — Tablas, tipos e índices
--  Ejecutar PRIMERO, en el SQL Editor de Supabase.
-- ============================================================================

-- Extensiones necesarias
create extension if not exists "pgcrypto";      -- gen_random_uuid()
create extension if not exists "citext";        -- emails sin distinguir mayúsculas

-- ----------------------------------------------------------------------------
--  PERFILES
--  Extiende auth.users (que maneja Supabase). Un perfil por cuenta.
-- ----------------------------------------------------------------------------
create table if not exists public.perfiles (
  id                uuid primary key references auth.users(id) on delete cascade,
  nombre_perfil     text not null
                    check (char_length(trim(nombre_perfil)) between 2 and 40),
  email             citext,
  email_verificado  boolean not null default false,
  rol               text not null default 'coleccionista'
                    check (rol in ('coleccionista', 'curador', 'admin')),

  -- Privacidad: TODO apagado por defecto (opt-in explícito)
  visibilidad       text not null default 'privada'
                    check (visibilidad in ('privada', 'compartida', 'publica')),
  comuna            text,          -- solo comuna, NUNCA coordenadas
  region            text,
  geo_consentida    boolean not null default false,
  geo_actualizada   timestamptz,
  stats_anonimas    boolean not null default false,

  creado            timestamptz not null default now(),
  actualizado       timestamptz not null default now()
);

comment on table  public.perfiles is 'Perfil público/privado de cada coleccionista.';
comment on column public.perfiles.comuna is 'Comuna o ciudad. Nunca se guardan coordenadas exactas (Ley 21.719 + minimización).';
comment on column public.perfiles.geo_consentida is 'Consentimiento explícito y revocable para usar la ubicación.';
comment on column public.perfiles.stats_anonimas is 'Si el usuario acepta aportar a las estadísticas agregadas (k-anonimato).';

-- ----------------------------------------------------------------------------
--  COLECCIONES
--  Un usuario puede tener varias (la base de arranque + las que quiera).
-- ----------------------------------------------------------------------------
create table if not exists public.colecciones (
  id          uuid primary key default gen_random_uuid(),
  usuario_id  uuid not null references public.perfiles(id) on delete cascade,
  nombre      text not null default 'Mi colección'
              check (char_length(trim(nombre)) between 1 and 60),
  descripcion text,
  es_base     boolean not null default false,   -- la colección de arranque
  visibilidad text not null default 'privada'
              check (visibilidad in ('privada', 'compartida', 'publica')),
  creada      timestamptz not null default now(),
  actualizada timestamptz not null default now()
);

comment on table public.colecciones is 'Colección de un usuario. La visibilidad puede sobrescribir la del perfil.';

-- Un solo "colección base" por usuario
create unique index if not exists un_solo_base_por_usuario
  on public.colecciones (usuario_id) where es_base;

-- ----------------------------------------------------------------------------
--  AUTOS EN COLECCIÓN
-- ----------------------------------------------------------------------------
create table if not exists public.autos_coleccion (
  id            uuid primary key default gen_random_uuid(),
  coleccion_id  uuid not null references public.colecciones(id) on delete cascade,
  usuario_id    uuid not null references public.perfiles(id) on delete cascade,

  catalog_id    text,        -- id del catálogo (ej. '2024-HTF24'); null si no está catalogado
  barcode       text,        -- código de barras escaneado
  nombre_libre  text,        -- nombre escrito por el usuario si no está en el catálogo

  cantidad      int  not null default 1 check (cantidad > 0 and cantidad <= 9999),
  condicion     text not null default 'carded-nuevo'
                check (condicion in ('carded-nuevo','carded-dañado','loose-mint','loose-bueno','loose-jugado')),
  ubicacion     text,
  notas         text,
  subcoleccion  text,
  foto_url      text,

  agregado      timestamptz not null default now(),
  actualizado   timestamptz not null default now(),

  -- Un mismo auto + condición no se duplica: se suma cantidad
  unique (coleccion_id, catalog_id, condicion)
);

comment on column public.autos_coleccion.nombre_libre is 'Para autos que no están en el catálogo. Alimenta la curación.';
comment on column public.autos_coleccion.barcode is 'Código escaneado. Sirve para identificar y para el catálogo colaborativo.';

-- ----------------------------------------------------------------------------
--  AUDITORÍA
--  Registro inmutable de accesos, cambios de rol y break-glass.
--  Sin políticas de UPDATE/DELETE: nadie puede alterar el historial.
-- ----------------------------------------------------------------------------
create table if not exists public.auditoria (
  id          bigserial primary key,
  actor_id    uuid references public.perfiles(id) on delete set null,
  actor_rol   text,
  accion      text not null,   -- 'ver_coleccion' | 'exportar' | 'cambio_rol' | 'break_glass' | ...
  objetivo_id uuid,            -- usuario o colección afectada
  objetivo_tipo text,          -- 'perfil' | 'coleccion' | 'auto'
  motivo      text,            -- OBLIGATORIO en accesos privilegiados
  expira      timestamptz,     -- solo break-glass
  ip          inet,
  user_agent  text,
  detalle     jsonb,
  creado      timestamptz not null default now()
);

comment on table public.auditoria is 'Historial de accesos y acciones sensibles. Inmutable por diseño.';

-- ----------------------------------------------------------------------------
--  ÍNDICES
-- ----------------------------------------------------------------------------
create index if not exists idx_perfiles_comuna      on public.perfiles (comuna) where comuna is not null;
create index if not exists idx_perfiles_rol         on public.perfiles (rol);
create index if not exists idx_perfiles_visibilidad on public.perfiles (visibilidad);

create index if not exists idx_colecciones_usuario  on public.colecciones (usuario_id);
create index if not exists idx_colecciones_visib    on public.colecciones (visibilidad);

create index if not exists idx_autos_usuario        on public.autos_coleccion (usuario_id);
create index if not exists idx_autos_coleccion      on public.autos_coleccion (coleccion_id);
create index if not exists idx_autos_catalog        on public.autos_coleccion (catalog_id) where catalog_id is not null;
create index if not exists idx_autos_barcode        on public.autos_coleccion (barcode) where barcode is not null;

create index if not exists idx_auditoria_actor      on public.auditoria (actor_id, creado desc);
create index if not exists idx_auditoria_objetivo   on public.auditoria (objetivo_id, creado desc);
create index if not exists idx_auditoria_accion     on public.auditoria (accion, creado desc);

-- ----------------------------------------------------------------------------
--  TRIGGERS
-- ----------------------------------------------------------------------------

-- actualizado = now() al modificar
create or replace function public.tocar_actualizado()
returns trigger
language plpgsql
as $$
begin
  new.actualizado = now();
  return new;
end;
$$;

drop trigger if exists trg_perfiles_actualizado on public.perfiles;
create trigger trg_perfiles_actualizado
  before update on public.perfiles
  for each row execute function public.tocar_actualizado();

drop trigger if exists trg_colecciones_actualizado on public.colecciones;
create trigger trg_colecciones_actualizado
  before update on public.colecciones
  for each row execute function public.tocar_actualizado();

drop trigger if exists trg_autos_actualizado on public.autos_coleccion;
create trigger trg_autos_actualizado
  before update on public.autos_coleccion
  for each row execute function public.tocar_actualizado();

-- Al crear una cuenta nueva, crear su perfil automáticamente
create or replace function public.crear_perfil_nuevo()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.perfiles (id, email, email_verificado, nombre_perfil)
  values (
    new.id,
    new.email,
    (new.email_confirmed_at is not null),
    coalesce(
      nullif(trim(new.raw_user_meta_data->>'nombre_perfil'), ''),
      split_part(coalesce(new.email, 'coleccionista'), '@', 1)
    )
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists trg_crear_perfil on auth.users;
create trigger trg_crear_perfil
  after insert on auth.users
  for each row execute function public.crear_perfil_nuevo();

-- ----------------------------------------------------------------------------
--  FUNCIÓN AUXILIAR: ¿es admin o curador?
--  security definer para poder leer perfiles desde las políticas sin recursión.
-- ----------------------------------------------------------------------------
create or replace function public.es_staff()
returns boolean
language sql
stable
security definer set search_path = public
as $$
  select exists (
    select 1 from public.perfiles p
    where p.id = auth.uid()
      and p.rol in ('admin', 'curador')
  );
$$;

create or replace function public.es_admin()
returns boolean
language sql
stable
security definer set search_path = public
as $$
  select exists (
    select 1 from public.perfiles p
    where p.id = auth.uid()
      and p.rol = 'admin'
  );
$$;

-- ----------------------------------------------------------------------------
--  FUNCIÓN: registrar en auditoría
-- ----------------------------------------------------------------------------
create or replace function public.auditar(
  p_accion        text,
  p_objetivo_id   uuid default null,
  p_objetivo_tipo text default null,
  p_motivo        text default null,
  p_detalle       jsonb default null
)
returns void
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.auditoria (actor_id, actor_rol, accion, objetivo_id, objetivo_tipo, motivo, detalle)
  values (
    auth.uid(),
    (select rol from public.perfiles where id = auth.uid()),
    p_accion,
    p_objetivo_id,
    p_objetivo_tipo,
    p_motivo,
    p_detalle
  );
end;
$$;

-- ============================================================================
--  FIN 01_schema.sql
--  Siguiente: 02_policies.sql
-- ============================================================================


-- ═══════════════════════════════════════════════════════════
--  02_policies.sql
-- ═══════════════════════════════════════════════════════════

-- ============================================================================
--  HW Collector — Multiusuario
--  02_policies.sql — Row Level Security
--  Ejecutar DESPUÉS de 01_schema.sql.
--
--  PRINCIPIO: deny by default.
--  Con RLS activado y sin política aplicable, NADIE ve nada.
--  Cada política de abajo es un permiso explícito y acotado.
--
--  REGLA DE ORO: el aislamiento se deriva de auth.uid() (token de la sesión),
--  NUNCA del usuario_id que mande el cliente. Aunque la app tenga un bug y
--  olvide filtrar, PostgreSQL filtra igual.
-- ============================================================================

alter table public.perfiles         enable row level security;
alter table public.colecciones      enable row level security;
alter table public.autos_coleccion  enable row level security;
alter table public.auditoria        enable row level security;

-- ============================================================================
--  PERFILES
-- ============================================================================

-- Cada usuario ve su propio perfil
drop policy if exists "perfil: ver el propio" on public.perfiles;
create policy "perfil: ver el propio" on public.perfiles
  for select
  using (auth.uid() = id);

-- Perfiles públicos: solo los campos de descubrimiento (nombre, comuna, región).
-- No expone email ni preferencias de privacidad.
drop policy if exists "perfil: ver publicos" on public.perfiles;
create policy "perfil: ver publicos" on public.perfiles
  for select
  using (
    exists (
      select 1 from public.colecciones c
      where c.usuario_id = perfiles.id
        and c.visibilidad = 'publica'
    )
  );

-- Staff puede ver perfiles para administrar (rol, comuna agregada)
drop policy if exists "perfil: staff ve" on public.perfiles;
create policy "perfil: staff ve" on public.perfiles
  for select
  using (public.es_staff());

-- Cada usuario edita SOLO su perfil, y NO puede cambiarse el rol ni el email_verificado
drop policy if exists "perfil: editar el propio" on public.perfiles;
create policy "perfil: editar el propio" on public.perfiles
  for update
  using (auth.uid() = id)
  with check (
    auth.uid() = id
    and rol = (select p.rol from public.perfiles p where p.id = auth.uid())
    and email_verificado = (select p.email_verificado from public.perfiles p where p.id = auth.uid())
  );

-- Solo un admin puede cambiar el rol de alguien
drop policy if exists "perfil: admin cambia rol" on public.perfiles;
create policy "perfil: admin cambia rol" on public.perfiles
  for update
  using (public.es_admin())
  with check (public.es_admin());

-- El alta del perfil la hace el trigger (security definer), no el cliente.
-- No se define política de INSERT: nadie inserta perfiles a mano.

-- ============================================================================
--  COLECCIONES
-- ============================================================================

-- El dueño ve y gestiona las suyas
drop policy if exists "coleccion: dueno todo" on public.colecciones;
create policy "coleccion: dueno todo" on public.colecciones
  for all
  using (auth.uid() = usuario_id)
  with check (auth.uid() = usuario_id);

-- Cualquiera autenticado ve las colecciones PÚBLICAS
drop policy if exists "coleccion: publicas visibles" on public.colecciones;
create policy "coleccion: publicas visibles" on public.colecciones
  for select
  using (visibilidad = 'publica');

-- Staff ve las COMPARTIDAS y PÚBLICAS.
-- Las PRIVADAS quedan fuera: ni el admin las ve (Ley 21.719, art. 14 bis).
drop policy if exists "coleccion: staff ve compartidas" on public.colecciones;
create policy "coleccion: staff ve compartidas" on public.colecciones
  for select
  using (
    public.es_staff()
    and visibilidad in ('compartida', 'publica')
  );

-- ============================================================================
--  AUTOS EN COLECCIÓN
-- ============================================================================

-- El dueño gestiona los suyos
drop policy if exists "autos: dueno todo" on public.autos_coleccion;
create policy "autos: dueno todo" on public.autos_coleccion
  for all
  using (auth.uid() = usuario_id)
  with check (auth.uid() = usuario_id);

-- Se ven los autos de colecciones PÚBLICAS
drop policy if exists "autos: de colecciones publicas" on public.autos_coleccion;
create policy "autos: de colecciones publicas" on public.autos_coleccion
  for select
  using (
    exists (
      select 1 from public.colecciones c
      where c.id = autos_coleccion.coleccion_id
        and c.visibilidad = 'publica'
    )
  );

-- Staff ve los autos de colecciones COMPARTIDAS o PÚBLICAS (nunca privadas)
drop policy if exists "autos: staff ve compartidas" on public.autos_coleccion;
create policy "autos: staff ve compartidas" on public.autos_coleccion
  for select
  using (
    public.es_staff()
    and exists (
      select 1 from public.colecciones c
      where c.id = autos_coleccion.coleccion_id
        and c.visibilidad in ('compartida', 'publica')
    )
  );

-- ============================================================================
--  AUDITORÍA
--  Solo se puede INSERTAR (vía la función auditar) y LEER como admin.
--  No hay política de UPDATE ni DELETE: el historial es inmutable.
-- ============================================================================

drop policy if exists "auditoria: admin lee" on public.auditoria;
create policy "auditoria: admin lee" on public.auditoria
  for select
  using (public.es_admin());

drop policy if exists "auditoria: registrar" on public.auditoria;
create policy "auditoria: registrar" on public.auditoria
  for insert
  with check (auth.uid() = actor_id);

-- ============================================================================
--  BREAK-GLASS — acceso de emergencia auditado
--
--  Se define la TABLA de solicitudes. El acceso real se concede con una
--  función que valida motivo + expiración y deja rastro en auditoría.
--  (La Fase 5 lo conecta a la interfaz del panel de administración.)
-- ============================================================================

create table if not exists public.break_glass (
  id           uuid primary key default gen_random_uuid(),
  admin_id     uuid not null references public.perfiles(id) on delete cascade,
  objetivo_id  uuid not null references public.perfiles(id) on delete cascade,
  motivo       text not null check (char_length(trim(motivo)) >= 20),
  concedido    timestamptz not null default now(),
  expira       timestamptz not null default (now() + interval '24 hours'),
  revocado     timestamptz,
  notificado   boolean not null default false
);

comment on table public.break_glass is
  'Acceso de emergencia a una colección privada. Exige motivo (mín. 20 caracteres), expira en 24 h y queda auditado.';

alter table public.break_glass enable row level security;

drop policy if exists "break_glass: admin gestiona" on public.break_glass;
create policy "break_glass: admin gestiona" on public.break_glass
  for all
  using (public.es_admin())
  with check (public.es_admin());

-- El usuario afectado ve que se pidió acceso a sus datos
drop policy if exists "break_glass: afectado ve" on public.break_glass;
create policy "break_glass: afectado ve" on public.break_glass
  for select
  using (auth.uid() = objetivo_id);

-- ============================================================================
--  FUNCIÓN: conceder break-glass (con auditoría obligatoria)
-- ============================================================================

create or replace function public.conceder_break_glass(
  p_objetivo_id uuid,
  p_motivo      text
)
returns uuid
language plpgsql
security definer set search_path = public
as $$
declare
  v_id uuid;
begin
  if not public.es_admin() then
    raise exception 'Solo un administrador puede conceder acceso de emergencia.';
  end if;

  if char_length(trim(coalesce(p_motivo, ''))) < 20 then
    raise exception 'El motivo debe tener al menos 20 caracteres.';
  end if;

  insert into public.break_glass (admin_id, objetivo_id, motivo)
  values (auth.uid(), p_objetivo_id, p_motivo)
  returning id into v_id;

  perform public.auditar(
    'break_glass',
    p_objetivo_id,
    'perfil',
    p_motivo,
    jsonb_build_object('break_glass_id', v_id, 'expira_horas', 24)
  );

  return v_id;
end;
$$;

-- ============================================================================
--  VERIFICACIÓN (ejecutar a mano y comprobar que todas dan true)
-- ============================================================================

-- select relname, relrowsecurity
-- from pg_class
-- where relname in ('perfiles','colecciones','autos_coleccion','auditoria','break_glass');
--   → todas deben tener relrowsecurity = true

-- select tablename, count(*) as politicas
-- from pg_policies
-- where schemaname = 'public'
-- group by tablename;

-- ============================================================================
--  FIN 02_policies.sql
--  Siguiente: 03_views.sql
-- ============================================================================


-- ═══════════════════════════════════════════════════════════
--  03_views.sql
-- ═══════════════════════════════════════════════════════════

-- ============================================================================
--  HW Collector — Multiusuario
--  03_views.sql — Estadísticas agregadas para administradores
--  Ejecutar DESPUÉS de 02_policies.sql.
--
--  PRINCIPIO: el admin ve AGREGADOS, nunca filas de personas.
--  K-ANONIMATO: ninguna estadística se muestra si la sostienen menos de
--  K_MIN personas. Así no se puede deducir la colección de nadie.
--
--  Las vistas se crean con security_invoker = false para que puedan agregar
--  sobre filas que el RLS ocultaría al admin. El filtro de privacidad NO es
--  el RLS acá: es (a) el consentimiento stats_anonimas y (b) el k-anonimato.
-- ============================================================================

-- Mínimo de personas para publicar una estadística
create or replace function public.k_min()
returns int language sql immutable as $$ select 5 $$;

-- ----------------------------------------------------------------------------
--  1. Coleccionables: cuántos tienen cada modelo
-- ----------------------------------------------------------------------------
create or replace view public.stats_coleccionables
with (security_invoker = false)
as
select
  a.catalog_id,
  count(distinct a.usuario_id)                                as coleccionistas,
  sum(a.cantidad)                                             as unidades,
  count(*) filter (where a.condicion = 'carded-nuevo')        as en_tarjeta,
  count(*) filter (where a.condicion like 'loose%')           as sueltos,
  round(avg(a.cantidad)::numeric, 2)                          as promedio_por_persona
from public.autos_coleccion a
join public.perfiles p on p.id = a.usuario_id
where a.catalog_id is not null
  and p.stats_anonimas = true
group by a.catalog_id
having count(distinct a.usuario_id) >= public.k_min();

comment on view public.stats_coleccionables is
  'Por modelo: cuántos coleccionistas lo tienen. Solo de usuarios que aceptaron aportar y con k>=5.';

-- ----------------------------------------------------------------------------
--  2. Series más coleccionadas
-- ----------------------------------------------------------------------------
create or replace view public.stats_series
with (security_invoker = false)
as
select
  a.subcoleccion                                             as serie,
  count(distinct a.usuario_id)                               as coleccionistas,
  count(distinct a.catalog_id)                               as modelos_distintos,
  sum(a.cantidad)                                            as unidades
from public.autos_coleccion a
join public.perfiles p on p.id = a.usuario_id
where a.subcoleccion is not null
  and p.stats_anonimas = true
group by a.subcoleccion
having count(distinct a.usuario_id) >= public.k_min();

comment on view public.stats_series is 'Series declaradas por los usuarios, agregadas con k>=5.';

-- ----------------------------------------------------------------------------
--  3. Condición de las piezas (salud de las colecciones)
-- ----------------------------------------------------------------------------
create or replace view public.stats_condicion
with (security_invoker = false)
as
select
  a.condicion,
  count(distinct a.usuario_id) as coleccionistas,
  sum(a.cantidad)              as unidades,
  round(100.0 * sum(a.cantidad) / sum(sum(a.cantidad)) over (), 1) as porcentaje
from public.autos_coleccion a
join public.perfiles p on p.id = a.usuario_id
where p.stats_anonimas = true
group by a.condicion
having count(distinct a.usuario_id) >= public.k_min();

-- ----------------------------------------------------------------------------
--  4. Geografía: densidad por comuna (solo de quienes consintieron)
-- ----------------------------------------------------------------------------
create or replace view public.stats_geografia
with (security_invoker = false)
as
select
  p.region,
  p.comuna,
  count(*)                     as coleccionistas,
  sum(coalesce(c.autos, 0))    as autos_totales
from public.perfiles p
left join (
  select usuario_id, sum(cantidad) as autos
  from public.autos_coleccion
  group by usuario_id
) c on c.usuario_id = p.id
where p.geo_consentida = true
  and p.comuna is not null
group by p.region, p.comuna
having count(*) >= public.k_min();

comment on view public.stats_geografia is
  'Densidad por comuna. Solo de usuarios que dieron consentimiento explícito, con k>=5. Nunca coordenadas.';

-- ----------------------------------------------------------------------------
--  5. Actividad del sistema (sin datos personales)
-- ----------------------------------------------------------------------------
create or replace view public.stats_actividad
with (security_invoker = false)
as
select
  date_trunc('day', a.agregado)::date as dia,
  count(distinct a.usuario_id)        as usuarios_activos,
  count(*)                            as autos_agregados,
  count(*) filter (where a.barcode is not null) as por_escaneo
from public.autos_coleccion a
group by 1
order by 1 desc;

comment on view public.stats_actividad is 'Actividad diaria agregada. Sin datos personales.';

-- ----------------------------------------------------------------------------
--  6. Salud de la plataforma (solo admins)
-- ----------------------------------------------------------------------------
create or replace view public.stats_plataforma
with (security_invoker = false)
as
select
  (select count(*) from public.perfiles)                                as usuarios_total,
  (select count(*) from public.perfiles where email_verificado)         as verificados,
  (select count(*) from public.colecciones)                             as colecciones_total,
  (select count(*) from public.colecciones where visibilidad='publica') as publicas,
  (select count(*) from public.colecciones where visibilidad='compartida') as compartidas,
  (select count(*) from public.autos_coleccion)                         as autos_total,
  (select count(distinct catalog_id) from public.autos_coleccion where catalog_id is not null) as modelos_distintos,
  (select count(*) from public.perfiles where geo_consentida)           as con_geo,
  (select count(*) from public.perfiles where stats_anonimas)           as con_stats;

-- ----------------------------------------------------------------------------
--  7. Top de modelos por coleccionistas (para el panel)
-- ----------------------------------------------------------------------------
create or replace view public.stats_top_modelos
with (security_invoker = false)
as
select *
from public.stats_coleccionables
order by coleccionistas desc, unidades desc
limit 100;

-- ----------------------------------------------------------------------------
--  8. Autos que nadie tiene (oportunidad de catálogo colaborativo)
--     Solo cuenta códigos escaneados por k+ personas y sin catalog_id.
-- ----------------------------------------------------------------------------
create or replace view public.stats_sin_catalogar
with (security_invoker = false)
as
select
  a.barcode,
  count(distinct a.usuario_id) as reportado_por,
  min(a.agregado)              as primera_vez
from public.autos_coleccion a
where a.catalog_id is null
  and a.barcode is not null
group by a.barcode
having count(distinct a.usuario_id) >= public.k_min();

comment on view public.stats_sin_catalogar is
  'Códigos escaneados que no están en el catálogo. Útil para ampliarlo, con k>=5.';

-- ============================================================================
--  PERMISOS DE LAS VISTAS
--  Solo el staff puede consultarlas.
-- ============================================================================

revoke all on public.stats_coleccionables  from anon, authenticated;
revoke all on public.stats_series          from anon, authenticated;
revoke all on public.stats_condicion       from anon, authenticated;
revoke all on public.stats_geografia       from anon, authenticated;
revoke all on public.stats_actividad       from anon, authenticated;
revoke all on public.stats_plataforma      from anon, authenticated;
revoke all on public.stats_top_modelos     from anon, authenticated;
revoke all on public.stats_sin_catalogar   from anon, authenticated;

grant select on public.stats_coleccionables to authenticated;
grant select on public.stats_series         to authenticated;
grant select on public.stats_condicion      to authenticated;
grant select on public.stats_geografia      to authenticated;
grant select on public.stats_actividad      to authenticated;
grant select on public.stats_plataforma     to authenticated;
grant select on public.stats_top_modelos    to authenticated;
grant select on public.stats_sin_catalogar  to authenticated;

-- Nota: el grant permite consultar, pero la app solo las pide si el rol es
-- staff. Para blindarlo del todo, envolver el acceso en funciones
-- security definer que validen es_staff() antes de devolver filas.

create or replace function public.obtener_stats_plataforma()
returns setof public.stats_plataforma
language sql
stable
security definer set search_path = public
as $$
  select * from public.stats_plataforma
  where public.es_staff();
$$;

comment on function public.obtener_stats_plataforma is
  'Devuelve las estadísticas de plataforma SOLO si quien consulta es staff. Devuelve vacío si no.';

-- ============================================================================
--  FIN 03_views.sql
--  Siguiente: 04_seed.sql (datos de prueba)
-- ============================================================================


-- ============================================================================
--  VERIFICACIÓN — se ejecuta sola al final
--  Mirá los resultados: todas las tablas deben decir relrowsecurity = true
-- ============================================================================

select relname as tabla, relrowsecurity as rls_activo
from pg_class
where relname in ('perfiles','colecciones','autos_coleccion','auditoria','break_glass')
order by relname;

select tablename as tabla, count(*) as politicas
from pg_policies where schemaname='public'
group by tablename order by tablename;

select table_name as vista from information_schema.views
where table_schema='public' and table_name like 'stats_%' order by table_name;
