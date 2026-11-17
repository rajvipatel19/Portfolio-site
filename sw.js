/* Service worker: when a page can't load because there's no internet, show the offline page (a little firefly game).
   It only steps in when the network fails; everything else loads normally, so the site never shows stale content. */
const CACHE = "offline-v2";
const KEY = "/__offline__";

self.addEventListener("install", (e) => {
  e.waitUntil((async () => {
    const res = await fetch("/offline.html", { cache: "reload" });
    // re-wrap the response so a redirect on the host (e.g. /offline.html -> /offline) can still be served for any page
    const page = new Response(await res.blob(), { status: 200, headers: { "Content-Type": "text/html; charset=utf-8" } });
    await (await caches.open(CACHE)).put(KEY, page);
    self.skipWaiting();
  })());
});

self.addEventListener("activate", (e) => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== CACHE) await caches.delete(k);
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", (e) => {
  if (e.request.mode !== "navigate") return;
  e.respondWith(fetch(e.request).catch(async () => (await caches.match(KEY)) || Response.error()));
});
