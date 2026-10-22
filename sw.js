/* HW Collector — service worker v20 (FIX ANDROID: no cachear HTML en install) */
const CACHE = 'hwcollector-v34';
const CRITICOS = ['./manifest.webmanifest','./icons/icon-192.jpg','./icons/icon-512.jpg','./icons/apple-touch-icon.jpg'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CRITICOS)).catch(()=>{}).then(() => self.skipWaiting()));
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
  /* API del puente: siempre red */
  if (url.origin === location.origin && /^\/(agent|sync|tts)/.test(url.pathname)) return;
  /* NUNCA cachear documentos (index.html ~7MB causa crash en Android PWA) */
  if (req.destination === 'document' || url.pathname.endsWith('.html')) {
    e.respondWith(fetch(req).catch(() => caches.match(req).then(h => h || caches.match('./index.html'))));
    return;
  }
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
