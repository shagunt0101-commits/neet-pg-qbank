/* NEET PG QBank service worker — offline-first for installed app */
var CACHE = 'qbank-v15'; /* bump when shell or bank files change */

var SHELL = [
  '/',
  '/questions/science.html',
  '/manifest.json',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/icons/icon-512-maskable.png'
];

var BANK = [
  '/questions/bank.js?v=11',
  '/questions/test_2026.js?v=1',
  '/questions/core_btr.js?v=6'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return Promise.all(SHELL.map(function (u) { return c.add(u); }))
        .then(function () {
          /* background-fetch bank files (verified responses); the page's own
             script load also fetches them — cache-first serves whichever wins */
          return Promise.all(BANK.map(function (u) {
            return fetch(u).then(function (r) {
              if (r.ok) c.put(u, r);
            });
          }));
        })
        .then(function () { return self.skipWaiting(); });
    })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; })
        .map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'GET') return;
  var url = new URL(e.request.url);
  /* Firebase SDK + Auth/Firestore calls: never cache, never intercept */
  if (url.origin === 'https://www.gstatic.com') return;
  if (url.origin !== location.origin) return;

  var isBank = BANK.some(function (u) {
    var q = u.indexOf('?');
    return u.indexOf(url.pathname) === 0 && (q === -1 || url.search === u.substring(q));
  });

  if (isBank) {
    /* cache-first for bank files */
    e.respondWith(
      caches.match(e.request).then(function (hit) {
        if (hit) return hit;
        return fetch(e.request).then(function (r) {
          if (r.ok) {
            caches.open(CACHE).then(function (c) { c.put(e.request, r.clone()); });
          }
          return r;
        });
      })
    );
  } else {
    /* network-first for shell; cache fallback offline */
    e.respondWith(
      fetch(e.request).then(function (r) {
        if (r.ok) {
          caches.open(CACHE).then(function (c) { c.put(e.request, r.clone()); });
        }
        return r;
      }).catch(function () { return caches.match(e.request); })
    );
  }
});
