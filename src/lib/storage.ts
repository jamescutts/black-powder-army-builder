import type { Nation } from "@/data/types";
import type { RosterState, RosterUnitLine } from "@/types/army";

// Each nation keeps its own army, so switching to another list and back doesn't lose anything.
const KEY_PREFIX = "black-powder-army-builder:roster:";
// Older versions kept a single army under this key; it's adopted by its nation the first time that list opens.
const LEGACY_KEY = "black-powder-army-builder:roster";

const keyFor = (nationId: string) => KEY_PREFIX + nationId;

function read(key: string): RosterState | null {
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as RosterState) : null;
  } catch {
    return null;
  }
}

/**
 * The saved army for this nation, tidied against the current data: brigades, slots and units that
 * have since been removed or reshaped in the army list are dropped rather than breaking the builder.
 */
export function loadRoster(nation: Nation): RosterState | null {
  if (typeof window === "undefined") return null;
  let saved = read(keyFor(nation.id));
  if (!saved) {
    const legacy = read(LEGACY_KEY);
    if (legacy?.nationId === nation.id) saved = legacy;
  }
  if (!saved || saved.nationId !== nation.id) return null;

  const unitIds = new Set(nation.units.map((u) => u.id));
  const keepLines = (lines: RosterUnitLine[] | undefined) =>
    (Array.isArray(lines) ? lines : []).filter((l) => unitIds.has(l.unitId) && l.qty > 0);

  try {
    return {
      nationId: nation.id,
      // "My Army" was the old placeholder rather than a name anyone chose
      armyName: saved.armyName && saved.armyName !== "My Army" ? saved.armyName : "",
      commandItems: keepLines(saved.commandItems),
      brigadeInstances: (saved.brigadeInstances ?? []).flatMap((bi) => {
        const bt = nation.brigades.find((b) => b.id === bi.brigadeTypeId);
        if (!bt) return [];
        return [
          {
            ...bi,
            name: typeof bi.name === "string" && bi.name.trim() ? bi.name : undefined,
            commanderLine: bi.commanderLine && unitIds.has(bi.commanderLine.unitId) ? bi.commanderLine : null,
            slotLines: bt.slots.map((_, i) => keepLines(bi.slotLines?.[i])),
            regimentSlots: bt.slots.map((slot, i) =>
              slot.regiment
                ? (bi.regimentSlots?.[i] ?? []).map((reg) => ({
                    ...reg,
                    slotLines: slot.regiment!.slots.map((_, j) => keepLines(reg.slotLines?.[j])),
                  }))
                : null
            ),
          },
        ];
      }),
    };
  } catch {
    return null;
  }
}

/** Saves the army under its nation; an empty, unnamed army clears the save instead of storing nothing. */
export function saveRoster(roster: RosterState) {
  if (typeof window === "undefined") return;
  try {
    const key = keyFor(roster.nationId);
    if (roster.commandItems.length === 0 && roster.brigadeInstances.length === 0 && !roster.armyName.trim()) {
      window.localStorage.removeItem(key);
    } else {
      window.localStorage.setItem(key, JSON.stringify(roster));
    }
    // Once a nation has its own save, the old shared one isn't needed for it
    if (read(LEGACY_KEY)?.nationId === roster.nationId) window.localStorage.removeItem(LEGACY_KEY);
  } catch {
    // Storage full or blocked (private browsing): the builder still works, it just won't remember
  }
}

export function clearRoster(nationId: string) {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.removeItem(keyFor(nationId));
  } catch {
    // ignore
  }
}
