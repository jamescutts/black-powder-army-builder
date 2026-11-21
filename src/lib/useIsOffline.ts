"use client";

import { useSyncExternalStore } from "react";
import { isOffline } from "./offline";

function subscribe(onChange: () => void) {
  window.addEventListener("offlinechange", onChange);
  return () => window.removeEventListener("offlinechange", onChange);
}

/**
 * Whether the page has no connection (see lib/offline.ts). False while the page is drawn on the server and
 * hydrating, then the real answer. For styling, `[data-offline]` in CSS is better, as it applies at once.
 */
export function useIsOffline(): boolean {
  return useSyncExternalStore(subscribe, isOffline, () => false);
}
