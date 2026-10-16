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
