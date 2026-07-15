// R0T4S — service worker
// Estratégia: a página vem sempre da REDE primeiro (para as atualizações chegarem logo),
// com recurso à cópia guardada se estiveres offline. As bibliotecas (Tesseract, ZXing,
// jsPDF…) ficam em cache depois da primeira utilização, para arranques rápidos.
const CACHE = 'r0t4s-v2';
const BASE = ['./index.html', './icon-192.png', './icon-512.png', './icon-180.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(BASE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET') return;

  // navegação/página: rede primeiro, cache como recurso
  if (e.request.mode === 'navigate' || url.pathname.endsWith('index.html')) {
    e.respondWith(
      fetch(e.request)
        .then(r => { const cp = r.clone(); caches.open(CACHE).then(c => c.put('./index.html', cp)); return r; })
        .catch(() => caches.match('./index.html'))
    );
    return;
  }

  // APIs de mapas/CTT: sempre rede (dados vivos), nunca cache
  if (/nominatim|geoapi/.test(url.hostname)) return;

  // bibliotecas de CDN e ícones: cache primeiro, rede para preencher
  e.respondWith(
    caches.match(e.request).then(hit => hit || fetch(e.request).then(r => {
      if (r.ok && (url.origin === location.origin || /cdnjs|jsdelivr|unpkg/.test(url.hostname))) {
        const cp = r.clone(); caches.open(CACHE).then(c => c.put(e.request, cp));
      }
      return r;
    }))
  );
});
