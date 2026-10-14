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
