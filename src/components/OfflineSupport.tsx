"use client";

import { useEffect } from "react";
import { loadPdfLibs } from "@/lib/pdfLibs";

const BUILD_VERSION = process.env.NEXT_PUBLIC_BUILD_VERSION;

type WorkerStatus = { type: "offline-status"; version: string; warmed: boolean };

/**
 * Starts the service worker (app/sw.js) that saves the site for use offline. Draws nothing.
 *
 * The PDF export loads its libraries only when first used, so the worker can't find them in any page.
 * Once this build's worker is in charge, the page loads them once in a quiet moment, through the worker,
 * so exporting works offline too.
 */
export function OfflineSupport() {
  useEffect(() => {
    if (!("serviceWorker" in navigator)) return;

    // Not while developing: a worker serving saved copies would hide every change
    if (process.env.NODE_ENV !== "production") {
      navigator.serviceWorker.getRegistrations().then((regs) => regs.forEach((r) => r.unregister()));
      return;
    }

    let warming = false;
    const onMessage = (event: MessageEvent) => {
      const status = event.data as WorkerStatus | undefined;
      if (status?.type !== "offline-status" || status.warmed || warming) return;
      // A worker from another build (this page is older or newer than it) would save the wrong files
      if (status.version !== BUILD_VERSION) return;
      warming = true;
      whenIdle(() =>
        loadPdfLibs()
          .then(() => navigator.serviceWorker.controller?.postMessage({ type: "warmed" }))
          .catch(() => {})
          .finally(() => (warming = false))
      );
    };
    navigator.serviceWorker.addEventListener("message", onMessage);

    navigator.serviceWorker
      .register("/sw.js", { scope: "/" })
      .then(() => navigator.serviceWorker.controller?.postMessage({ type: "status" }))
      .catch(() => {});

    // Installed apps ask to keep their saved data, so the browser doesn't clear it to free up space.
    // Only once installed: some browsers ask the user, which would be odd on a first visit.
    if (window.matchMedia("(display-mode: standalone)").matches) {
      navigator.storage?.persist?.().catch(() => {});
    }

    return () => navigator.serviceWorker.removeEventListener("message", onMessage);
  }, []);

  return null;
}

function whenIdle(fn: () => void) {
  if ("requestIdleCallback" in window) window.requestIdleCallback(fn, { timeout: 10000 });
  else setTimeout(fn, 3000);
}
