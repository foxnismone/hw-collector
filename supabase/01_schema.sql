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
