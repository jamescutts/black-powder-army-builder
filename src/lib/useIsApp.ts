"use client";

import { useSyncExternalStore } from "react";
import { isAppMode } from "./appMode";

function subscribe(onChange: () => void) {
  window.addEventListener("appmodechange", onChange);
  return () => window.removeEventListener("appmodechange", onChange);
}

/**
 * Whether the page is running as the installed app (see lib/appMode.ts). False while the page is drawn
 * on the server and hydrating, then the real answer. For styling, `[data-app]` in CSS is better, as it
 * applies from the first frame.
 */
export function useIsApp(): boolean {
  return useSyncExternalStore(subscribe, isAppMode, () => false);
}
