-- ============================================================================
--  HW Collector — Multiusuario
--  04_seed.sql — Datos de prueba y VERIFICACIÓN DEL AISLAMIENTO
--
--  Solo para pruebas. No ejecutar en producción.
--
--  Objetivo: probar que un usuario NO puede leer nada de otro.
--  Este es el test obligatorio antes de publicar (ver §13 Fase 1 del plan).
-- ============================================================================

-- ----------------------------------------------------------------------------
--  PASO 1 — Crear dos usuarios de prueba
--
--  Los usuarios se crean desde el panel de Supabase (Authentication → Users →
--  Add user) o por la API. NO se insertan a mano en auth.users.
--
--  Crear:
--    usuario.a@ejemplo.cl   contraseña: probar1234
--    usuario.b@ejemplo.cl   contraseña: probar1234
--
--  Marcá "Auto Confirm User" para que el email quede verificado.
-- ----------------------------------------------------------------------------

-- ----------------------------------------------------------------------------
--  PASO 2 — Asignar roles y visibilidad distinta a cada uno
--  (ejecutar después de crear los usuarios)
-- ----------------------------------------------------------------------------

-- A: admin, colección privada
update public.perfiles
set rol = 'admin',
    visibilidad = 'privada',
    stats_anonimas = true,
    geo_consentida = true,
    comuna = 'Providencia',
    region = 'Metropolitana'
where email = 'usuario.a@ejemplo.cl';

-- B: coleccionista normal, colección privada
update public.perfiles
set rol = 'coleccionista',
    visibilidad = 'privada',
    stats_anonimas = true,
    comuna = 'Ñuñoa',
    region = 'Metropolitana'
where email = 'usuario.b@ejemplo.cl';

-- ----------------------------------------------------------------------------
--  PASO 3 — Crear colecciones y cargar autos
-- ----------------------------------------------------------------------------

insert into public.colecciones (usuario_id, nombre, es_base, visibilidad)
select id, 'Colección base', true, 'privada'
from public.perfiles
where email in ('usuario.a@ejemplo.cl', 'usuario.b@ejemplo.cl')
on conflict do nothing;

-- 10 autos para A (la colección base del onboarding)
insert into public.autos_coleccion (coleccion_id, usuario_id, catalog_id, cantidad, condicion, subcoleccion)
select c.id, c.usuario_id, v.catalog_id, v.cantidad, v.condicion, v.subcoleccion
from public.colecciones c
join public.perfiles p on p.id = c.usuario_id
cross join (values
  ('2024-HTF24', 1, 'carded-nuevo', 'Muscle Cars'),
  ('2023-HKH47', 1, 'carded-nuevo', 'Muscle Cars'),
  ('2022-HCV09', 2, 'carded-dañado', 'Muscle Cars'),
  ('2026-JJK35', 1, 'carded-nuevo', 'JDM'),
  ('2026-JJK34', 1, 'carded-nuevo', 'JDM'),
  ('2026-JJJ14', 1, 'carded-nuevo', 'Super Treasure Hunt 2026'),
  ('2025-HYW18', 3, 'loose-mint', 'Mainline'),
  ('2025-HYW34', 1, 'carded-nuevo', 'Mainline'),
  ('2025-HYY72', 1, 'carded-nuevo', 'Mainline'),
  ('2024-HRY51', 1, 'carded-nuevo', 'Mainline')
) as v(catalog_id, cantidad, condicion, subcoleccion)
where p.email = 'usuario.a@ejemplo.cl'
on conflict do nothing;

-- 2 autos para B (colección distinta y pequeña)
insert into public.autos_coleccion (coleccion_id, usuario_id, catalog_id, cantidad, condicion)
select c.id, c.usuario_id, v.catalog_id, v.cantidad, v.condicion
from public.colecciones c
join public.perfiles p on p.id = c.usuario_id
cross join (values
  ('2026-JJK35', 1, 'loose-bueno'),
  ('2024-HTB08', 1, 'carded-nuevo')
) as v(catalog_id, cantidad, condicion)
where p.email = 'usuario.b@ejemplo.cl'
on conflict do nothing;

-- ============================================================================
--  PASO 4 — VERIFICACIÓN DEL AISLAMIENTO  (el test que no se puede saltear)
--
--  Cómo ejecutarlo:
--    1. En el panel de Supabase, Authentication → Users → usuario B →
--       "Impersonate user" (o generá un JWT de B).
--    2. En el SQL Editor, correr las consultas de abajo.
--    3. El resultado esperado está anotado en cada una.
-- ============================================================================

-- (a) Como B, ¿veo la colección privada de A?
--     ESPERADO: 0 filas
-- select * from public.colecciones c
-- join public.perfiles p on p.id = c.usuario_id
-- where p.email = 'usuario.a@ejemplo.cl';

-- (b) Como B, ¿veo los autos de A?
--     ESPERADO: 0 filas
-- select * from public.autos_coleccion
-- where usuario_id = (select id from public.perfiles where email='usuario.a@ejemplo.cl');

-- (c) Como B, ¿veo mi propia colección?
--     ESPERADO: 2 filas
-- select * from public.autos_coleccion;

-- (d) Como A (admin), ¿veo la colección privada de B?
--     ESPERADO: 0 filas  ← ESTE ES EL TEST CLAVE
--     El admin NO ve colecciones privadas (Ley 21.719, art. 14 bis).
-- select * from public.colecciones c
-- join public.perfiles p on p.id = c.usuario_id
-- where p.email = 'usuario.b@ejemplo.cl';

-- (e) Como A (admin), ¿veo la colección PÚBLICA de B?
--     Primero poné la de B como pública:
--       update public.colecciones set visibilidad='publica'
--       where usuario_id = (select id from public.perfiles where email='usuario.b@ejemplo.cl');
--     ESPERADO: 1 fila (ahora sí, porque B lo hizo público)
-- select * from public.colecciones c
-- join public.perfiles p on p.id = c.usuario_id
-- where p.email = 'usuario.b@ejemplo.cl';

-- (f) Las estadísticas solo aparecen con k >= 5 personas
--     ESPERADO: 0 filas (solo hay 2 usuarios: 2 < 5)
-- select * from public.stats_coleccionables;

-- (g) La tabla de auditoría solo la lee un admin
--     Como B: ESPERADO 0 filas.  Como A: ESPERADO las filas registradas.
-- select * from public.auditoria order by creado desc limit 20;

-- (h) ¿Alguien puede borrar o modificar la auditoría?
--     ESPERADO: error de permiso denegado (no hay política de update/delete)
-- update public.auditoria set motivo = 'alterado' where id = 1;

-- ============================================================================
--  PASO 5 — Limpiar los datos de prueba
-- ============================================================================
-- delete from public.autos_coleccion
--   where usuario_id in (select id from public.perfiles
--                        where email in ('usuario.a@ejemplo.cl','usuario.b@ejemplo.cl'));
-- delete from public.colecciones
--   where usuario_id in (select id from public.perfiles
--                        where email in ('usuario.a@ejemplo.cl','usuario.b@ejemplo.cl'));
-- Los usuarios se borran desde Authentication → Users.
-- (Borrar el usuario en auth.users arrastra el perfil y sus colecciones por
--  las claves foráneas "on delete cascade".)

-- ============================================================================
--  FIN 04_seed.sql
-- ============================================================================
