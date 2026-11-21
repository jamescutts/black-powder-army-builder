"use client";

import { useEffect } from "react";
import { loadPdfLibs } from "@/lib/pdfLibs";
import { reportNetwork } from "@/lib/offline";
import { isAppMode } from "@/lib/appMode";

const BUILD_VERSION = process.env.NEXT_PUBLIC_BUILD_VERSION;

type WorkerMessage =
  | { type: "offline-status"; version: string; warmed: boolean; network?: boolean }
  | { type: "network"; ok: boolean };

/**
 * Starts the service worker (app/sw.js) that saves the site for use offline, and passes on what it finds
 * of the network to the page's offline mark (lib/offline.ts). Draws nothing.
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
      const status = event.data as WorkerMessage | undefined;
      // Whether the network's answering the worker, for the page's offline mark (lib/offline.ts)
      if (status?.type === "network") return reportNetwork(status.ok);
      if (status?.type !== "offline-status") return;
      if (status.network !== undefined) reportNetwork(status.network);
      if (status.warmed || warming) return;
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
    if (isAppMode()) {
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
