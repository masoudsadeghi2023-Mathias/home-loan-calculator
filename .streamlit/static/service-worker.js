const CACHE_NAME = "streamlit-pwa-cache-v1";

// فایل‌هایی که باید کش شوند
const urlsToCache = [
  "/",
  "/index.html",
  "/manifest.json",
  "/logo-192.png",
  "/logo-512.png"
];

// نصب Service Worker
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting();
});

// فعال‌سازی
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// هندل کردن درخواست‌ها
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      // اگر در کش بود → همان را بده
      if (response) return response;

      // اگر نبود → از شبکه بگیر و در کش ذخیره کن
      return fetch(event.request).then(networkResponse => {
        return caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, networkResponse.clone());
          return networkResponse;
        });
      });
    })
  );
});
