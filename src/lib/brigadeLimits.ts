import type { BrigadeType, BrigadeSlot } from "@/data/types";
import type { RosterBrigadeInstance, RosterUnitLine } from "@/types/army";

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

// ─── Brigade-level unit count prerequisite (requiresBrigadeCount) ────────────

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
 * Count the total qty of the specified unit ids within a single brigade instance
 * (every slot, flat and regiment sub-slots).
 */
export function countUnitsInInstance(instance: RosterBrigadeInstance, unitIds: string[]): number {
  const idSet = new Set(unitIds);
  let total = 0;
  // Flat slots
  for (const lines of instance.slotLines) {
    for (const line of lines) {
      if (idSet.has(line.unitId)) total += line.qty;
    }
  }
  // Regiment slots
  for (const regSlot of instance.regimentSlots ?? []) {
    if (!regSlot) continue;
    for (const reg of regSlot) {
      for (const lines of reg.slotLines) {
        for (const line of lines) {
          if (idSet.has(line.unitId)) total += line.qty;
        }
      }
    }
  }
  return total;
}

/**
 * Whether a slot's `requiresBrigadeCount` condition is met for a given brigade instance.
 * Counts the qty of the listed unit ids within this brigade instance (all slots, flat and
 * regiment sub-slots) and checks against the minimum.
 */
export function brigadeCountRequirementMet(
  slot: BrigadeSlot,
  instance: RosterBrigadeInstance
): boolean {
  if (!slot.requiresBrigadeCount) return true;
  const total = countUnitsInInstance(instance, slot.requiresBrigadeCount.unitIds);
  return total >= slot.requiresBrigadeCount.min;
}

// ─── Army-wide unit count requirement ────────────────────────────────────────

/**
 * Count the total qty of specified unit ids across the entire army (all brigade instances,
 * flat slots and regiment sub-slots).
 */
export function countUnitsInArmy(instances: RosterBrigadeInstance[], unitIds: string[]): number {
  const idSet = new Set(unitIds);
  let total = 0;
  for (const bi of instances) {
    // Flat slots
    for (const lines of bi.slotLines) {
      for (const line of lines) {
        if (idSet.has(line.unitId)) total += line.qty;
      }
    }
    // Regiment slots
    for (const regSlot of bi.regimentSlots ?? []) {
      if (!regSlot) continue;
      for (const reg of regSlot) {
        for (const lines of reg.slotLines) {
          for (const line of lines) {
            if (idSet.has(line.unitId)) total += line.qty;
          }
        }
      }
    }
  }
  return total;
}

/**
 * Whether a slot's `requiresArmyUnitCount` condition is met.
 */
export function armyUnitCountRequirementMet(
  slot: BrigadeSlot,
  instances: RosterBrigadeInstance[]
): boolean {
  if (!slot.requiresArmyUnitCount) return true;
  const count = countUnitsInArmy(instances, slot.requiresArmyUnitCount.unitIds);
  return count >= slot.requiresArmyUnitCount.min;
}

// ─── Effective per-slot max for the UI badge (dynamic caps) ──────────────────

/**
 * Compute the effective max qty for a flat slot given its current lines and the brigade instance.
 * Considers static `max`, per-unit `unitLimits`, and `dynamicUnitLimits` (regimental artillery
 * ratios). Because dynamic slots use `singleUnitType`, the effective max is the cap that applies
 * to whichever unit type is currently in the slot (falling back to the static max when empty).
 */
export function effectiveSlotMax(
  slot: BrigadeSlot,
  lines: RosterUnitLine[],
  instance: RosterBrigadeInstance
): number {
  // Determine which unit ids are currently present
  const presentIds = [...new Set(lines.filter((l) => l.qty > 0).map((l) => l.unitId))];

  const capForUnit = (unitId: string): number => {
    // dynamicUnitLimits take priority
    const dyn = slot.dynamicUnitLimits?.find((d) => d.unitId === unitId);
    if (dyn) {
      if (dyn.perBattalions) {
        const battalions = dyn.perBattalions.countSlotIndices.reduce(
          (sum, idx) => sum + slotUnitCount(instance, idx), 0
        );
        return Math.floor(battalions / dyn.perBattalions.ratio);
      }
      if (dyn.perQualifyingRegiment) {
        const { regimentSlotIndices, minBattalions } = dyn.perQualifyingRegiment;
        let qualifying = 0;
        for (const idx of regimentSlotIndices) {
          for (const reg of instance.regimentSlots?.[idx] ?? []) {
            const bn = reg.slotLines.reduce((s, ls) => s + ls.reduce((a, l) => a + l.qty, 0), 0);
            if (bn >= minBattalions) qualifying += 1;
          }
        }
        return qualifying;
      }
    }
    const lim = slot.unitLimits?.find((u) => u.unitId === unitId);
    if (lim) return lim.max;
    return slot.max;
  };

  if (presentIds.length === 0) {
    // Nothing picked yet: if every eligible unit shares the same dynamic/limit we could show it,
    // but generally fall back to the static slot max.
    return slot.max;
  }
  // For singleUnitType slots (one present id) or slots with dynamic ratios, the effective max is
  // the cap that applies to whichever unit type is present. For ordinary mixed slots, per-unit
  // `unitLimits` cap individual units but do NOT reduce the slot's overall capacity, so the
  // effective total max is the static slot max.
  const usesDynamicOrSingle = slot.singleUnitType || (slot.dynamicUnitLimits?.length ?? 0) > 0;
  if (!usesDynamicOrSingle) {
    return slot.max;
  }
  return Math.max(...presentIds.map(capForUnit));
}
