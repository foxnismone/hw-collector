/* HW Collector — service worker (offline-first) */
const CACHE = 'hwcollector-v10';
const SHELL = ['./','./index.html','./galeria_catalogo.html','./galeria_coleccion.html',
               './manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png','./icons/apple-touch-icon.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).catch(()=>{}).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('message', e => {
  if (e.data && e.data.type === 'SKIP_WAITING') self.skipWaiting();
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;
  /* API del puente (agente, sync, voz): siempre red, nunca caché */
  if (url.origin === location.origin && /^\/(agent|sync|tts)/.test(url.pathname)) return;
  if (req.destination === 'image') {                       /* imágenes: RED PRIMERO (refresca datos corregidos), caché de respaldo offline */
    e.respondWith(fetch(req).then(r => {
      if (r && (r.ok || r.type === 'opaque')) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)).catch(()=>{}); }
      return r;
    }).catch(() => caches.match(req).then(h => h || Response.error())));
    return;
  }
  e.respondWith(fetch(req).then(r => {                     /* resto: red primero, caché de respaldo */
    const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); return r;
  }).catch(() => caches.match(req).then(h => h || caches.match('./index.html'))));
});
