import type { BrigadeType, BrigadeSlot } from "@/data/types";
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

// ─── Per-unit conditional cap helpers ────────────────────────────────────────

type UnitCap = NonNullable<BrigadeSlot["unitCaps"]>[number];

/**
 * Whether the prerequisite for a unit cap is satisfied.
 * Returns true if the cap has no `requiresBrigades` condition, or if the condition is met.
 */
export function unitCapRequirementMet(cap: UnitCap, instances: RosterBrigadeInstance[]): boolean {
  if (!cap.requiresBrigades) return true;
  return countByTypes(instances, cap.requiresBrigades.brigadeTypeIds) >= cap.requiresBrigades.min;
}

/**
 * Compute the effective army-wide maximum for a unit cap, taking into account its `maxRatio`
 * scaling (if any). Without maxRatio the base `armyMax` is returned unchanged.
 */
export function effectiveUnitCapMax(cap: UnitCap, instances: RosterBrigadeInstance[]): number {
  if (!cap.maxRatio) return cap.armyMax;
  const linkedCount = countByTypes(instances, cap.maxRatio.brigadeTypeIds);
  const ratioMax = Math.floor(linkedCount / cap.maxRatio.ratio);
  return Math.min(cap.armyMax, ratioMax);
}

// ─── Slot-level prerequisite (requiresSlotFill) ──────────────────────────────

/**
 * Count total unit qty for a given slot index in a brigade instance.
 * Handles both flat slots (slotLines) and regiment slots (regimentSlots).
 */
export function slotUnitCount(instance: RosterBrigadeInstance, slotIndex: number): number {
  // Check regiment slots first
  const regiments = instance.regimentSlots?.[slotIndex];
  if (regiments && regiments.length > 0) {
    return regiments.reduce((sum, reg) =>
      sum + reg.slotLines.reduce((rSum, lines) =>
        rSum + lines.reduce((lSum, l) => lSum + l.qty, 0), 0), 0);
  }
  // Fall back to flat slot lines
  const lines = instance.slotLines[slotIndex] ?? [];
  return lines.reduce((s, l) => s + l.qty, 0);
}

/**
 * Whether a slot's `requiresSlotFill` condition is met for a given brigade instance.
 * Sums the qty of units across the specified sibling slot indices (supporting both flat and
 * regiment slots) and checks against the minimum.
 */
export function slotFillRequirementMet(
  slot: BrigadeSlot,
  instance: RosterBrigadeInstance
): boolean {
  if (!slot.requiresSlotFill) return true;
  const total = slot.requiresSlotFill.slotIndices.reduce(
    (sum, idx) => sum + slotUnitCount(instance, idx), 0
  );
  return total >= slot.requiresSlotFill.min;
}
