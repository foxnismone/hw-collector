/* ===== Cliente Supabase — multiusuario para HW Collector ===== */
const SBClient = (function() {
  let sb = null;
  let sesion = null;
  let perfil = null;
  let syncPending = false;
  let syncTimer = null;
  let escuchandoAuth = false;

  const URL = 'https://wgoqtqwxikqhrgulclqk.supabase.co';
  const KEY  = 'sb_publishable_Jn2KEus4MeiBUOOZBX31eA_esHdE7Km';
  const PREFIJO_SYNC = 'hwcol_sync';

  // ---------------------------------------------------------------- init
  function init() {
    try {
      if (typeof window.supabase === 'undefined') {
        console.warn('[SBClient] supabase.js no cargado');
        return false;
      }
      sb = window.supabase.createClient(URL, KEY, {
        auth: {
          persistSession: true,
          autoRefreshToken: true,
          detectSessionInUrl: true
        }
      });
      if (!escuchandoAuth) {
        sb.auth.onAuthStateChange((evento, s) => {
          sesion = s;
          if (evento === 'SIGNED_IN' || evento === 'SIGNED_OUT') {
            perfil = null;
            refrescarBadgeCuenta();
            if (evento === 'SIGNED_IN') sincronizarDesde();
          }
        });
        escuchandoAuth = true;
      }
      return true;
    } catch (e) {
      console.warn('[SBClient] init falló:', e.message);
      return false;
    }
  }

  // ------------------------------------------------------------- auth
  function estaLogueado() { return !!sesion; }

  function getEmail() { return sesion?.user?.email || null; }

  async function registrar(email, password, nombrePerfil) {
    if (!sb) return { error: 'cliente no disponible' };
    const { data, error } = await sb.auth.signUp({
      email, password,
      options: { data: { nombre_perfil: nombrePerfil || email.split('@')[0] } }
    });
    if (error) return { error: traducirError(error) };
    sesion = data.session || null;
    return { ok: !!data.user, necesitaConfirmar: !data.session };
  }

  async function iniciarSesion(email, password) {
    if (!sb) return { error: 'cliente no disponible' };
    const { data, error } = await sb.auth.signInWithPassword({ email, password });
    if (error) return { error: traducirError(error) };
    sesion = data.session;
    perfil = null;
    return { ok: true };
  }

  async function cerrarSesion() {
    if (!sb) return;
    await sb.auth.signOut();
    sesion = null;
    perfil = null;
    localStorage.removeItem(PREFIJO_SYNC);
    refrescarBadgeCuenta();
  }

  // ------------------------------------------------------------ perfil
  async function getPerfil(fuerza) {
    if (!sesion) return null;
    if (perfil && !fuerza) return perfil;
    const { data, error } = await sb.from('perfiles').select('*').eq('id', sesion.user.id).single();
    if (error) { console.warn('[SBClient] getPerfil:', error.message); return null; }
    perfil = data;
    return perfil;
  }

  async function actualizarPerfil(cambios) {
    if (!sb || !sesion) return { error: 'sin sesión' };
    const permitido = ['nombre_perfil','bio','tipo_coleccionista','avatar_url','visibilidad','comuna','region','geo_consentida','stats_anonimas'];
    const datos = {};
    permitido.forEach(k => { if (cambios[k] !== undefined) datos[k] = cambios[k]; });
    const { error } = await sb.from('perfiles').update(datos).eq('id', sesion.user.id);
    if (error) return { error: error.message };
    perfil = { ...(perfil || {}), ...datos };
    return { ok: true };
  }

  async function actualizarGeo(comuna, region) {
    if (!sb || !sesion) return { error: 'sin sesión' };
    return actualizarPerfil({ comuna, region, geo_consentida: true, geo_actualizada: new Date().toISOString() });
  }

  // -------------------------------------------------------- colecciones
  async function listarColecciones() {
    if (!sb || !sesion) return [];
    const { data, error } = await sb.from('colecciones').select('*').eq('usuario_id', sesion.user.id).order('creada', { ascending: true });
    if (error) { console.warn('[SBClient] listarColecciones:', error.message); return []; }
    return data || [];
  }

  async function crearColeccion(nombre, esBase, visibilidad) {
    if (!sb || !sesion) return { error: 'sin sesión' };
    const { data, error } = await sb.from('colecciones')
      .insert({ usuario_id: sesion.user.id, nombre: nombre || 'Mi colección', es_base: !!esBase, visibilidad: visibilidad || 'privada' })
      .select().single();
    if (error) return { error: error.message };
    return { ok: true, coleccion: data };
  }

  // ------------------------------------------------------------- autos
  async function listarAutos(coleccionId) {
    if (!sb || !sesion) return [];
    const { data, error } = await sb.from('autos_coleccion').select('*').eq('coleccion_id', coleccionId).order('agregado', { ascending: true });
    if (error) { console.warn('[SBClient] listarAutos:', error.message); return []; }
    return data || [];
  }

  async function agregarAuto(coleccionId, datos) {
    if (!sb || !sesion) return { error: 'sin sesión' };
    const { data, error } = await sb.from('autos_coleccion')
      .insert({
        coleccion_id: coleccionId,
        usuario_id: sesion.user.id,
        catalog_id: datos.catalog_id || null,
        barcode: datos.barcode || null,
        nombre_libre: datos.nombre_libre || null,
        cantidad: datos.cantidad || 1,
        condicion: datos.condicion || 'carded-nuevo',
        ubicacion: datos.ubicacion || '',
        notas: datos.notas || '',
        subcoleccion: datos.subcoleccion || ''
      })
      .select().single();
    if (error) return { error: error.message };
    return { ok: true, auto: data };
  }

  async function actualizarAuto(id, datos) {
    if (!sb || !sesion) return { error: 'sin sesión' };
    const { error } = await sb.from('autos_coleccion').update(datos).eq('id', id);
    if (error) return { error: error.message };
    return { ok: true };
  }

  async function eliminarAuto(id) {
    if (!sb || !sesion) return { error: 'sin sesión' };
    const { error } = await sb.from('autos_coleccion').delete().eq('id', id);
    if (error) return { error: error.message };
    return { ok: true };
  }

  // ------------------------------------------------------- sincronizacion
  function marcaPendiente() {
    syncPending = true;
    if (syncTimer) clearTimeout(syncTimer);
    syncTimer = setTimeout(() => sincronizarHacia(), 2000);
  }

  function syncGetMarca() {
    try { return JSON.parse(localStorage.getItem(PREFIJO_SYNC) || '0'); } catch (e) { return 0; }
  }
  function syncSetMarca(n) {
    try { localStorage.setItem(PREFIJO_SYNC, JSON.stringify(n)); } catch (e) {}
  }

  async function sincronizarHacia() {
    if (!sb || !sesion || !syncPending) return;
    syncPending = false;
    try {
      const mis = Object.entries(col || {}).map(([id, o]) => ({ catalog_id: id, cantidad: o.q, condicion: o.c, ubicacion: o.u, notas: o.notas, subcoleccion: o.subcoleccion }));
      const { error } = await sb.rpc('hw_sync_autos', { p_coleccion_id: null, p_autos: mis });
      if (!error) syncSetMarca(Date.now());
    } catch (e) {
      syncPending = true;
    }
  }

  async function sincronizarDesde() {
    if (!sb || !sesion) return;
    try {
      const colecciones = await listarColecciones();
      const todas = [];
      for (const c of colecciones) {
        const autos = await listarAutos(c.id);
        autos.forEach(a => todas.push({ id: a.catalog_id, q: a.cantidad, c: a.condicion, u: a.ubicacion, notas: a.notas, subcoleccion: a.subcoleccion }));
      }
      const ultima = syncGetMarca();
      if (todas.length >= (ultima ? 0 : 0)) {
        col = {};
        todas.forEach(a => { if (a.id) col[a.id] = { q: a.q || 1, c: a.c || 'carded-nuevo', u: a.u || '', notas: a.notas || '', subcoleccion: a.subcoleccion || '' }; });
        syncSetMarca(Date.now());
        if (typeof saveCol === 'function') saveCol();
        if (typeof refreshAll === 'function') refreshAll();
      }
    } catch (e) {
      console.warn('[SBClient] sync desde:', e.message);
    }
  }

  async function sincronizarAhora() {
    if (!sb || !sesion) return { error: 'sin sesión' };
    await sincronizarHacia();
    await sincronizarDesde();
    return { ok: true };
  }

  // ----------------------------------------------------------- utilidades
  function refrescarBadgeCuenta() {
    const b = document.getElementById('ctabadge');
    const btn = document.getElementById('ctabtn');
    if (btn) btn.style.display = '';
    if (!b) return;
    if (sesion) {
      b.style.display = '';
      b.textContent = 'cuenta: ' + (sesion.user.email || '');
      b.className = 'fchip nuevo';
    } else {
      b.style.display = 'none';
    }
  }

  function traducirError(err) {
    const m = (err && err.message || '').toLowerCase();
    if (m.includes('email not confirmed') || m.includes('confirm')) return 'Confirmá tu email antes de entrar (revisá la bandeja).';
    if (m.includes('invalid login')) return 'Email o contraseña incorrectos.';
    if (m.includes('already registered') || m.includes('already been registered')) return 'Ese email ya está registrado. Iniciá sesión.';
    if (m.includes('rate limit')) return 'Demasiados intentos. Esperá un momento.';
    if (m.includes('password') && m.includes('8')) return 'La contraseña debe tener al menos 8 caracteres.';
    return err && err.message || 'Ocurrió un error inesperado.';
  }

  return { init, estaLogueado, getEmail, registrar, iniciarSesion, cerrarSesion, getPerfil, actualizarPerfil, actualizarGeo, listarColecciones, crearColeccion, listarAutos, agregarAuto, actualizarAuto, eliminarAuto, marcaPendiente, sincronizarHacia, sincronizarDesde, sincronizarAhora, refrescarBadgeCuenta };
})();
