// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/offline/',
    '/custom_offline',
    '/custom_offline_request',
    '/static/css/django-pwa-app.css',
    '/static/main/css/base.css',
    '/static/main/css/index.css',
    '/static/bootstrap/js/bootstrap.bundle.min.js',
    '/static/main/js/jquery-3.3.1.slim.min.js',
    'static/main/images/airbnb.png',
    '/static/bootstrap/css/bootstrap.min.css',
    '/manifest.json',
    '/last_cached'

    // '/css/django-pwa-app.css',
    // '/images/icons/icon-72x72.png',
    // '/images/icons/icon-96x96.png',
    // '/images/icons/icon-128x128.png',
    // '/images/icons/icon-144x144.png',
    // '/images/icons/icon-152x152.png',
    // '/images/icons/icon-192x192.png',
    // '/images/icons/icon-384x384.png',
    // '/images/icons/icon-512x512.png',
    // '/static/images/icons/splash-640x1136.png',
    // '/static/images/icons/splash-750x1334.png',
    // '/static/images/icons/splash-1242x2208.png',
    // '/static/images/icons/splash-1125x2436.png',
    // '/static/images/icons/splash-828x1792.png',
    // '/static/images/icons/splash-1242x2688.png',
    // '/static/images/icons/splash-1536x2048.png',
    // '/static/images/icons/splash-1668x2224.png',
    // '/static/images/icons/splash-1668x2388.png',
    // '/static/images/icons/splash-2048x2732.png',
//    '/requests/127'
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            }).catch((error) => {
            console.log(error)
        })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
            .catch((error) => {
                console.log(error)
            })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (event.request.url.match('/request/*')) {
                    caches.open(staticCacheName).then(function (cache) {
                        cache.add(event.request.url);
                    })
                }
                return response || fetch(event.request);
            })
            .catch(() => {
                if (event.request.url.match('/request/*')) {
                    return caches.match('/custom_offline_request')
                }
                return caches.match('/custom_offline');
            })
    )
});