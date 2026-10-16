/* HW Collector — service worker (offline-first) */
<<<<<<< HEAD
const CACHE = 'hwcollector-v7';
=======
const CACHE = 'hwcollector-v3';
>>>>>>> origin/main
const SHELL = ['./','./index.html','./galeria_catalogo.html','./galeria_coleccion.html',
               './manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png','./icons/apple-touch-icon.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).catch(()=>{}).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;
  /* API del puente (agente, sync, voz): siempre red, nunca caché */
  if (/^\/(agent|sync|tts)/.test(url.pathname)) return;
  if (req.destination === 'image') {                       /* imágenes: cache-first */
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => {
      const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); return r;
    }).catch(() => hit)));
    return;
  }
  e.respondWith(fetch(req).then(r => {                     /* resto: red primero, caché de respaldo */
    const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); return r;
  }).catch(() => caches.match(req).then(h => h || caches.match('./index.html'))));
});
