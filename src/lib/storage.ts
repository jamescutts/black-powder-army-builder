import type { RosterState } from "@/types/army";

const STORAGE_KEY = "black-powder-army-builder:roster";

export function loadRoster(): RosterState | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as RosterState;
  } catch {
    return null;
  }
}

export function saveRoster(roster: RosterState) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(roster));
}

export function clearRoster() {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(STORAGE_KEY);
}
