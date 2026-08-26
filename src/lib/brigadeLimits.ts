import type { BrigadeType } from "@/data/types";
import type { RosterBrigadeInstance } from "@/types/army";

export function countByType(instances: RosterBrigadeInstance[], brigadeTypeId: string): number {
  return instances.filter((bi) => bi.brigadeTypeId === brigadeTypeId).length;
}

function countByTypes(instances: RosterBrigadeInstance[], brigadeTypeIds: string[]): number {
  return brigadeTypeIds.reduce((sum, id) => sum + countByType(instances, id), 0);
}

/** The effective maximum for this brigade type given how many of its ratio-linked brigade types are in the army. */
export function effectiveMax(bt: BrigadeType, instances: RosterBrigadeInstance[]): number {
  if (!bt.maxRatio) return bt.max;
  const linkedCount = countByTypes(instances, bt.maxRatio.brigadeTypeIds);
  const ratioMax = Math.floor(linkedCount / bt.maxRatio.ratio);
  return Math.min(bt.max, ratioMax);
}

/** Whether this brigade type's `requires` precondition (if any) is currently met. */
export function requirementMet(bt: BrigadeType, instances: RosterBrigadeInstance[]): boolean {
  if (!bt.requires) return true;
  return countByTypes(instances, bt.requires.brigadeTypeIds) >= bt.requires.min;
}

export function requirementLabel(bt: BrigadeType, nationBrigades: BrigadeType[]): string | null {
  if (!bt.requires) return null;
  const names = bt.requires.brigadeTypeIds.map(
    (id) => nationBrigades.find((b) => b.id === id)?.name ?? id
  );
  return `Requires at least ${bt.requires.min} × ${names.join("/")}`;
}
