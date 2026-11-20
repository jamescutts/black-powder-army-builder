import type { Nation } from "@/data/types";
import type { RosterState, RosterUnitLine } from "@/types/army";

// Saved army lists, kept in this browser's localStorage. Each list has its own id, so a nation can
// have as many as you like (an 1812 corps and a smaller club-night force, say). The My armies page
// (app/armies) lists them all; the builder opens one by its id (?list=...).

const LIST_PREFIX = "black-powder-army-builder:list:";
// Older versions kept one army per nation under these keys, and before that a single army under the
// last. They're moved into lists the first time anything reads the saves.
const NATION_PREFIX = "black-powder-army-builder:roster:";
const LEGACY_KEY = "black-powder-army-builder:roster";

/** Fired on window whenever a list is saved or deleted, so the header's count and My armies keep up */
export const LISTS_CHANGED_EVENT = "army-lists-changed";

export interface SavedList {
  id: string;
  /** When it was first saved and last changed, in ms */
  createdAt: number;
  updatedAt: number;
  roster: RosterState;
}

const keyFor = (id: string) => LIST_PREFIX + id;

export function newListId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

function storage(): Storage | null {
  try {
    return typeof window === "undefined" ? null : window.localStorage;
  } catch {
    return null;
  }
}

function parse<T>(raw: string | null): T | null {
  try {
    return raw ? (JSON.parse(raw) as T) : null;
  } catch {
    return null;
  }
}

function changed() {
  try {
    window.dispatchEvent(new Event(LISTS_CHANGED_EVENT));
  } catch {
    // no window (server)
  }
}

/** Moves armies saved by older versions (one per nation) into lists of their own */
function migrate(store: Storage) {
  const oldKeys: string[] = [];
  for (let i = 0; i < store.length; i++) {
    const key = store.key(i);
    if (key && (key.startsWith(NATION_PREFIX) || key === LEGACY_KEY)) oldKeys.push(key);
  }
  if (oldKeys.length === 0) return;

  const migrated = new Set<string>();
  // Per-nation saves first: where a nation has both, its own save is the newer one
  oldKeys.sort((a, b) => Number(a === LEGACY_KEY) - Number(b === LEGACY_KEY));
  for (const key of oldKeys) {
    const roster = parse<RosterState>(store.getItem(key));
    try {
      if (roster?.nationId && !migrated.has(roster.nationId)) {
        const now = Date.now();
        const list: SavedList = { id: newListId(), createdAt: now, updatedAt: now, roster };
        store.setItem(keyFor(list.id), JSON.stringify(list));
        migrated.add(roster.nationId);
      }
      store.removeItem(key);
    } catch {
      // Storage full: leave the old save where it is and try again next time
    }
  }
}

/** Every saved list, most recently changed first */
export function listSaved(): SavedList[] {
  const store = storage();
  if (!store) return [];
  migrate(store);
  const lists: SavedList[] = [];
  try {
    for (let i = 0; i < store.length; i++) {
      const key = store.key(i);
      if (!key?.startsWith(LIST_PREFIX)) continue;
      const list = parse<SavedList>(store.getItem(key));
      if (list?.roster?.nationId) lists.push(list);
    }
  } catch {
    return [];
  }
  return lists.sort((a, b) => b.updatedAt - a.updatedAt);
}

/** One nation's saved lists, most recently changed first */
export function listSavedFor(nationId: string): SavedList[] {
  return listSaved().filter((l) => l.roster.nationId === nationId);
}

/**
 * A saved list's army, tidied against the current data: brigades, slots and units that have since been
 * removed or reshaped in the army list are dropped rather than breaking the builder. Null when there's no
 * such list, or it belongs to another nation.
 */
export function loadList(nation: Nation, id: string): RosterState | null {
  const store = storage();
  if (!store) return null;
  migrate(store);
  const saved = parse<SavedList>(store.getItem(keyFor(id)))?.roster;
  if (!saved || saved.nationId !== nation.id) return null;
  return tidy(nation, saved);
}

function tidy(nation: Nation, saved: RosterState): RosterState | null {
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

const isEmpty = (r: RosterState) => r.commandItems.length === 0 && r.brigadeInstances.length === 0 && !r.armyName.trim();

/**
 * Saves the army as list `id`. A list with no units and no name isn't kept, so starting a new list and
 * leaving it doesn't leave an empty one behind.
 */
export function saveList(id: string, roster: RosterState) {
  const store = storage();
  if (!store) return;
  try {
    const key = keyFor(id);
    const existing = parse<SavedList>(store.getItem(key));
    if (isEmpty(roster)) {
      if (existing) {
        store.removeItem(key);
        changed();
      }
      return;
    }
    // Unchanged (as when the builder first opens a list): keep its "last changed" time as it was
    if (existing && JSON.stringify(existing.roster) === JSON.stringify(roster)) return;
    const now = Date.now();
    const list: SavedList = { id, createdAt: existing?.createdAt ?? now, updatedAt: now, roster };
    store.setItem(key, JSON.stringify(list));
    changed();
  } catch {
    // Storage full or blocked (private browsing): the builder still works, it just won't remember
  }
}

export function deleteList(id: string) {
  const store = storage();
  if (!store) return;
  try {
    store.removeItem(keyFor(id));
    changed();
  } catch {
    // ignore
  }
}

/** Copies a list under a new id, named as a copy. Returns the new id, or null if it couldn't. */
export function duplicateList(id: string): string | null {
  const store = storage();
  const source = store && parse<SavedList>(store.getItem(keyFor(id)));
  if (!store || !source) return null;
  const copyId = newListId();
  const now = Date.now();
  const name = source.roster.armyName.trim();
  const copy: SavedList = {
    id: copyId,
    createdAt: now,
    updatedAt: now,
    roster: { ...source.roster, armyName: name ? `${name} (copy)` : "Copy" },
  };
  try {
    store.setItem(keyFor(copyId), JSON.stringify(copy));
    changed();
    return copyId;
  } catch {
    return null;
  }
}

/** The builder's address for one saved list */
export function listHref(supplementId: string, nationId: string, id: string): string {
  return `/black-powder/${supplementId}/${nationId}?list=${encodeURIComponent(id)}`;
}
