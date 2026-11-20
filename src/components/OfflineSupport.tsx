"use client";

import { useEffect, useState } from "react";
import { Button, Group, Notification, Text } from "@mantine/core";
import { loadPdfLibs } from "@/lib/pdfLibs";

const BUILD_VERSION = process.env.NEXT_PUBLIC_BUILD_VERSION;

/** How often, at most, coming back to the page asks whether there's a new version */
const UPDATE_CHECK_GAP_MS = 5 * 60 * 1000;

type WorkerStatus = { type: "offline-status"; version: string; warmed: boolean };

/**
 * Starts the service worker (app/sw.js) that saves the site for use offline, and offers a reload when a
 * newer version of the site takes over.
 *
 * The PDF export loads its libraries only when first used, so the worker can't find them in any page.
 * Once this build's worker is in charge, the page loads them once in a quiet moment, through the worker,
 * so exporting works offline too.
 *
 * A new deploy is a new worker. Pages normally come fresh from the network, so most visits already show
 * it, but an installed app left open (on a phone, resumed from the background without reloading) keeps
 * showing the version it opened with. When a newer worker takes over a page from an older build, the page
 * says so and offers to reload.
 */
export function OfflineSupport() {
  const [updateReady, setUpdateReady] = useState(false);

  useEffect(() => {
    if (!("serviceWorker" in navigator)) return;

    // Not while developing: a worker serving saved copies would hide every change
    if (process.env.NODE_ENV !== "production") {
      navigator.serviceWorker.getRegistrations().then((regs) => regs.forEach((r) => r.unregister()));
      return;
    }

    // Set once a worker has taken over this page since it loaded. Only then does a different version
    // mean this page is out of date: before that, the worker in charge may be older than the page (the
    // page came fresh from the network while the new worker was still saving files).
    let takenOver = false;
    let warming = false;
    const onMessage = (event: MessageEvent) => {
      const status = event.data as WorkerStatus | undefined;
      if (status?.type !== "offline-status") return;
      if (status.version !== BUILD_VERSION) {
        if (takenOver) setUpdateReady(true);
        // A worker from another build would save the wrong files, so don't warm it up
        return;
      }
      if (status.warmed || warming) return;
      warming = true;
      whenIdle(() =>
        loadPdfLibs()
          .then(() => navigator.serviceWorker.controller?.postMessage({ type: "warmed" }))
          .catch(() => {})
          .finally(() => (warming = false))
      );
    };
    // A newer worker has taken over: ask which version it is (it also says so itself as it starts)
    const onControllerChange = () => {
      takenOver = true;
      navigator.serviceWorker.controller?.postMessage({ type: "status" });
    };
    navigator.serviceWorker.addEventListener("message", onMessage);
    navigator.serviceWorker.addEventListener("controllerchange", onControllerChange);

    const registration = navigator.serviceWorker.register("/sw.js", { scope: "/" });
    registration
      .then(() => navigator.serviceWorker.controller?.postMessage({ type: "status" }))
      .catch(() => {});

    // Browsers look for a new worker when a page loads, not when an app comes back from the background,
    // so look on returning too (not more than every few minutes)
    let lastCheck = Date.now();
    const onVisible = () => {
      if (document.visibilityState !== "visible" || Date.now() - lastCheck < UPDATE_CHECK_GAP_MS) return;
      lastCheck = Date.now();
      registration.then((reg) => reg.update()).catch(() => {});
    };
    document.addEventListener("visibilitychange", onVisible);

    // Installed apps ask to keep their saved data, so the browser doesn't clear it to free up space.
    // Only once installed: some browsers ask the user, which would be odd on a first visit.
    if (window.matchMedia("(display-mode: standalone)").matches) {
      navigator.storage?.persist?.().catch(() => {});
    }

    return () => {
      navigator.serviceWorker.removeEventListener("message", onMessage);
      navigator.serviceWorker.removeEventListener("controllerchange", onControllerChange);
      document.removeEventListener("visibilitychange", onVisible);
    };
  }, []);

  if (!updateReady) return null;
  return (
    <div className="undo-toast" role="status">
      <Notification withBorder color="brown" onClose={() => setUpdateReady(false)}>
        <Group justify="space-between" wrap="nowrap" gap="md">
          <Text size="sm">A new version of Army Builder is ready.</Text>
          <Button size="compact-sm" variant="light" onClick={() => window.location.reload()}>
            Reload
          </Button>
        </Group>
      </Notification>
    </div>
  );
}

function whenIdle(fn: () => void) {
  if ("requestIdleCallback" in window) window.requestIdleCallback(fn, { timeout: 10000 });
  else setTimeout(fn, 3000);
}
