-- ============================================================================
--  HW Collector — Extensión de perfil
--  02_perfil_extension.sql — Avatar, bio y tipo de coleccionista
--  Ejecutar DESPUÉS de 01_schema.sql, en el SQL Editor de Supabase.
-- ============================================================================

-- Nuevos campos en perfiles
alter table public.perfiles add column if not exists avatar_url text;
alter table public.perfiles add column if not exists bio text check (char_length(bio) <= 200);
alter table public.perfiles add column if not exists tipo_coleccionista text
  check (tipo_coleccionista in ('privado', 'vendedor', 'revendedor', 'inversor'));

-- Índice para búsquedas por tipo de coleccionista
create index if not exists idx_perfiles_tipo on public.perfiles (tipo_coleccionista)
  where tipo_coleccionista is not null;

-- Comentarios
comment on column public.perfiles.avatar_url is 'URL del avatar (generado por DiceBear a partir del email).';
comment on column public.perfiles.bio is 'Descripción corta del coleccionista (máx. 200 caracteres).';
comment on column public.perfiles.tipo_coleccionista is 'Tipo de coleccionista: privado, vendedor, revendedor, inversor.';

-- Trigger de actualización automática de 'actualizado'
create or replace function public.touch_perfil()
returns trigger language plpgsql as $$
begin
  new.actualizado = now();
  return new;
end $$;

drop trigger if exists trg_perfil_touch on public.perfiles;
create trigger trg_perfil_touch
  before update on public.perfiles
  for each row execute function public.touch_perfil();
