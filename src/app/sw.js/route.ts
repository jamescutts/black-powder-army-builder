// The service worker, which lets the site (and the installed app) open without a connection. Built once
// at build time, with that build's version and every page to save written into it, so each deploy is a new
// worker and browsers pick it up on their next visit.
//
// What it does:
//  - On install, saves every page (home, Black Powder, My armies, each supplement and army list) and the files those
//    pages use: scripts, styles, fonts, flags and icons. Files the last version already saved are copied
//    across rather than downloaded again.
//  - Pages: from the network when it answers within a few seconds (saving the fresh copy), otherwise the
//    saved copy, so a weak signal at the club doesn't leave you staring at a blank screen.
//  - In-app navigation (Next's RSC requests): when offline, or slow and the page is saved, it fails the
//    request on purpose. Next then falls back to loading the whole page, which comes from the saved copy.
//  - Build files (/_next/static/...) never change once built, so they come from the cache first.
//  - Home page paintings from Wikimedia are kept once seen.
//  - It tells open pages when the network fails it and when it answers again, so they can show they're
//    offline (lib/offline.ts). Only real failures count: not a request the page itself gave up on (a
//    prefetch dropped as you moved on), nor a slow answer, which still gets the saved copy after a few
//    seconds but isn't proof of no connection.
//
// Rosters themselves live in the browser's localStorage (lib/storage.ts), which works offline already.

import { nations, supplements } from "@/data";
import { battles, campaignsWithBattles } from "@/data/battles";
import { battleHref, campaignHref, HISTORICAL_FORCES_PATH } from "@/lib/forces";

export const dynamic = "force-static";

const PAGES = [
  "/",
  "/black-powder",
  "/armies",
  ...supplements.map((s) => `/black-powder/${s.id}`),
  ...nations.map((n) => `/black-powder/${n.supplementId}/${n.id}`),
  HISTORICAL_FORCES_PATH,
  ...campaignsWithBattles().map((c) => campaignHref(c.id)),
  ...battles.map((b) => battleHref(b)),
];

// Saved alongside the pages: site search's data, the manifest and the installed app's icons
const EXTRAS = [
  "/search-index.json",
  "/manifest.webmanifest",
  "/app-icons/icon-192.png",
  "/app-icons/icon-512.png",
  "/app-icons/maskable-192.png",
  "/app-icons/maskable-512.png",
];

const WORKER = String.raw`
const VERSION = __VERSION__;
const PAGES = __PAGES__;
const EXTRAS = __EXTRAS__;

const PAGE_CACHE = "ab-pages-" + VERSION;
const STATIC_CACHE = "ab-static-" + VERSION;
const ART_CACHE = "ab-art";
const KEEP = [PAGE_CACHE, STATIC_CACHE, ART_CACHE];
const WARMED = "/__offline-warmed";

// How long a page or in-app navigation waits on the network before using the saved copy
const NETWORK_WAIT_MS = 4000;

// Same-site files a page refers to, found in its HTML (attributes, and the inline data Next sends
// along with it, where quotes are escaped) and in its stylesheets (fonts)
const ASSET_RE = /(?<=["'(\s,])\/(?!\/)[\w\-./%@~]+\.(?:js|css|woff2?|ttf|png|svg|jpe?g|webp|gif|ico)(?:\?[\w\-=.%]+)?/g;
const ICON_RE = /(?<=["'(\s,])\/(?:apple-)?icon(?:\.\w+)?\?[\w\-.]+/g;

self.addEventListener("install", (event) => {
  event.waitUntil(precache().then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    (async () => {
      const names = await caches.keys();
      await Promise.all(names.filter((n) => n.startsWith("ab-") && !KEEP.includes(n)).map((n) => caches.delete(n)));
      await self.clients.claim();
      const clients = await self.clients.matchAll({ type: "window" });
      const status = await statusMessage();
      clients.forEach((c) => c.postMessage(status));
    })()
  );
});

self.addEventListener("message", (event) => {
  const type = event.data && event.data.type;
  if (type === "status") {
    event.waitUntil(statusMessage().then((s) => event.source && event.source.postMessage(s)));
  } else if (type === "warmed") {
    // The page has loaded the PDF libraries through this worker, so they're saved for offline exports
    event.waitUntil(caches.open(PAGE_CACHE).then((c) => c.put(WARMED, new Response("1"))));
  }
});

async function statusMessage() {
  const warmed = !!(await (await caches.open(PAGE_CACHE)).match(WARMED));
  return { type: "offline-status", version: VERSION, warmed, network: networkOk !== false };
}

// Whether the network last answered: null until something's been asked of it. Open pages are told when
// it changes (and a page asking for the status hears it), so they can show they're offline.
let networkOk = null;
// A request the page cancelled fails too, but says nothing about the connection
const failed = (req) => {
  if (!(req.signal && req.signal.aborted)) report(false);
};
function report(ok) {
  if (ok === networkOk) return;
  networkOk = ok;
  self.clients.matchAll({ type: "window" }).then((cs) => cs.forEach((c) => c.postMessage({ type: "network", ok })));
}

async function precache() {
  const pages = await caches.open(PAGE_CACHE);
  const statics = await caches.open(STATIC_CACHE);
  const assets = new Set();
  const collect = (text) => {
    for (const m of text.matchAll(ASSET_RE)) assets.add(m[0]);
    for (const m of text.matchAll(ICON_RE)) assets.add(m[0]);
  };

  // Pages first, gathering what they refer to. One that fails is skipped (it'll be saved when visited),
  // so a single hiccup doesn't stop the rest from working offline.
  await Promise.allSettled(
    PAGES.concat(EXTRAS).map(async (path) => {
      const res = await fetch(path, { cache: "no-cache" });
      if (!res.ok || res.redirected) return;
      if ((res.headers.get("content-type") || "").includes("text/html")) collect(await res.clone().text());
      await pages.put(path, res);
    })
  );

  // Then the files, reusing the last version's copy of any that haven't changed. Stylesheets name their
  // fonts, so they're read for more files to save.
  const done = new Set();
  const save = async (path) => {
    if (done.has(path)) return;
    done.add(path);
    let res = await caches.match(path);
    if (!res) {
      res = await fetch(path);
      if (!res.ok || res.redirected) return;
    }
    if (path.split("?")[0].endsWith(".css")) {
      const before = assets.size;
      collect(await res.clone().text());
      if (assets.size > before) await Promise.allSettled([...assets].map(save));
    }
    await statics.put(path, res);
  };
  await Promise.allSettled([...assets].map(save));
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  if (url.origin !== self.location.origin) {
    if (req.destination === "image" && /(^|\.)wikimedia\.org$/.test(url.hostname)) {
      event.respondWith(cacheFirst(req, ART_CACHE));
    }
    return;
  }
  if (url.pathname === "/sw.js") return;

  if (req.mode === "navigate") {
    event.respondWith(page(event, url));
  } else if (req.headers.get("RSC")) {
    event.respondWith(inApp(req, url));
  } else if (url.pathname.startsWith("/_next/static/")) {
    event.respondWith(cacheFirst(req, STATIC_CACHE));
  } else {
    event.respondWith(saved(req));
  }
});

const pathKey = (url) => (url.pathname.length > 1 ? url.pathname.replace(/\/$/, "") : url.pathname);
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function page(event, url) {
  const key = pathKey(url);
  const cache = await caches.open(PAGE_CACHE);
  const cached = await cache.match(key);

  const network = fetch(event.request).then(async (res) => {
    report(true);
    if (res.ok && res.type === "basic" && (res.headers.get("content-type") || "").includes("text/html")) {
      await cache.put(key, res.clone());
    }
    return res;
  });
  event.waitUntil(network.catch(() => failed(event.request)));

  if (!cached) return network.catch(() => offlinePage());
  return Promise.race([network.catch(() => cached), wait(NETWORK_WAIT_MS).then(() => cached)]);
}

async function inApp(req, url) {
  const isSaved = !!(await (await caches.open(PAGE_CACHE)).match(pathKey(url)));
  if (!isSaved) return fetch(req);
  if (self.navigator.onLine === false) {
    report(false);
    return Response.error();
  }
  return Promise.race([
    fetch(req).then(
      (res) => (report(true), res),
      () => (failed(req), Response.error())
    ),
    wait(NETWORK_WAIT_MS).then(() => Response.error()),
  ]);
}

async function cacheFirst(req, cacheName) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  if (res.ok || res.type === "opaque") await cache.put(req, res.clone());
  return res;
}

// Anything else on the site (flags, icons, search data): the network, falling back to a saved copy
async function saved(req) {
  try {
    const res = await fetch(req);
    report(true);
    if (res.ok) return res;
    return (await caches.match(req)) || res;
  } catch (err) {
    failed(req);
    const hit = await caches.match(req);
    if (hit) return hit;
    throw err;
  }
}

function offlinePage() {
  const html = '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    + '<meta name="viewport" content="width=device-width, initial-scale=1"><title>Offline | Army Builder</title>'
    + '<style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;'
    + 'background:#e8dec4;color:#2b1f14;font-family:Georgia,serif;padding:16px;box-sizing:border-box}'
    + 'main{max-width:420px;text-align:center}h1{font-size:22px;margin:0 0 8px}'
    + 'a{color:#33200f}</style></head><body><main><h1>You’re offline</h1>'
    + '<p>This page hasn’t been saved for offline use yet. Your army lists and saved rosters are still '
    + 'available.</p><p><a href="/black-powder">Go to the Black Powder army lists</a></p></main></body></html>';
  return new Response(html, { status: 503, headers: { "content-type": "text/html; charset=utf-8" } });
}
`;

export function GET() {
  const source = WORKER.replace("__VERSION__", JSON.stringify(process.env.NEXT_PUBLIC_BUILD_VERSION ?? "dev"))
    .replace("__PAGES__", JSON.stringify(PAGES))
    .replace("__EXTRAS__", JSON.stringify(EXTRAS));
  return new Response(source, {
    headers: {
      "content-type": "application/javascript; charset=utf-8",
      "cache-control": "no-cache",
    },
  });
}
