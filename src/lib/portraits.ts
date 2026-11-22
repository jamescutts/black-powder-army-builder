import type { HistoricalArt } from "@/data/types";
import type { RosterState } from "@/types/army";
import { getForce } from "@/data/battles";
import named from "@/data/commander-portraits.json";

// The army lists' named commanders' portraits, by unit id (written by scripts/forces/commanders.py)
const NAMED = named as Record<string, HistoricalArt>;

/**
 * The portrait of an army's commander, for the roster's head: a named commander of the list's, when one leads
 * it, else the commander of the historical force the list was started from, when that force has one.
 */
export function armyPortrait(roster: RosterState): HistoricalArt | undefined {
  for (const line of roster.commandItems) {
    const p = NAMED[line.unitId];
    if (p) return p;
  }
  return roster.sourceForceId ? getForce(roster.sourceForceId)?.portrait : undefined;
}
