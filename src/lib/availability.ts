import type { BrigadeSlot, BrigadeType, Nation, RegimentSlot } from "@/data/types";
import type { RosterBrigadeInstance, RosterState, RosterUnitLine } from "@/types/army";
import {
  armyUnitCountRequirementMet,
  brigadeCountRequirementMet,
  choiceTaken,
  choicesTaken,
  countUnitsInArmy,
  countUnitsInInstance,
  effectiveUnitCapMax,
  slotUnitCount,
  unitCapRequirementMet,
} from "@/lib/brigadeLimits";
import { unitNoun } from "@/lib/options";

// What the builder can still add, and why not when it can't: the same rules validate.ts checks, asked
// before a unit is added rather than after, so the pickers can grey out what isn't allowed.

const unitName = (nation: Nation, id: string) => nation.units.find((u) => u.id === id)?.name ?? id;
const countOf = (lines: RosterUnitLine[], ids: string[]) =>
  lines.filter((l) => ids.includes(l.unitId)).reduce((s, l) => s + l.qty, 0);

/** Where a slot sits, for the rules that look beyond the slot itself */
export interface SlotPlace {
  nation: Nation;
  roster: RosterState;
  bt: BrigadeType;
  instance: RosterBrigadeInstance;
  /** The slot's index in the brigade type (for a regiment's sub-slot, the regiment slot's index) */
  slotIndex: number;
}

/**
 * Why nothing can be added to a slot yet, e.g. "Needs 6 infantry battalions in this brigade first
 * (has 4)", or null when it's open.
 */
export function slotLockedReason(place: SlotPlace, slot: BrigadeSlot): string | null {
  const { nation, roster, instance } = place;
  if (slot.requiresBrigadeCount && !brigadeCountRequirementMet(slot, instance)) {
    const { unitIds, min } = slot.requiresBrigadeCount;
    const have = countUnitsInInstance(instance, unitIds);
    return `Needs ${min} ${unitNoun(nation, unitIds, min)} in this brigade first (has ${have})`;
  }
  if (slot.requiresArmyUnitCount && !armyUnitCountRequirementMet(slot, roster.brigadeInstances)) {
    const { unitIds, min } = slot.requiresArmyUnitCount;
    const have = countUnitsInArmy(roster.brigadeInstances, unitIds);
    return `Needs ${min} ${unitNoun(nation, unitIds, min)} in the army first (has ${have})`;
  }
  return null;
}

/** Why the brigade can't take another unit in this slot because it's at its battalion limit, or null */
export function brigadeFullReason(place: SlotPlace): string | null {
  const { bt, instance, slotIndex } = place;
  const cap = bt.maxBattalions;
  if (!cap || (cap.countSlotIndices && !cap.countSlotIndices.includes(slotIndex))) return null;
  const indices = cap.countSlotIndices ?? bt.slots.map((_, i) => i);
  const count = indices.reduce((s, i) => s + slotUnitCount(instance, i), 0);
  return count >= cap.max ? `The brigade has its ${cap.max} battalions` : null;
}

/**
 * Why one more of a unit can't be added to a brigade's (flat) slot right now, or null if it can. Only
 * the per-unit rules: the slot's own total and locks are shown by its badge and `slotLockedReason`.
 */
export function unitBlockedInSlot(place: SlotPlace, slot: BrigadeSlot, lines: RosterUnitLine[], unitId: string): string | null {
  const { nation, roster, bt, instance, slotIndex } = place;

  const full = brigadeFullReason(place);
  if (full) return full;

  // One kind can't outnumber another in the brigade (Austria's Advanced Guard: cavalry ≤ infantry)
  const balance = bt.atLeastAsMany;
  if (balance?.asUnitIds.includes(unitId)) {
    if (countUnitsInInstance(instance, balance.asUnitIds) + 1 > countUnitsInInstance(instance, balance.unitIds)) {
      return balance.label;
    }
  }

  // A brigade limited in how many of its choices it takes (Austria's Grenadier Brigade: 2 of 3)
  const choiceReason = choiceBlockedReason(bt, instance, slotIndex, unitId);
  if (choiceReason) return choiceReason;

  for (const cap of slot.unitGroupCaps ?? []) {
    if (!cap.unitIds.includes(unitId)) continue;
    const inArmy = roster.brigadeInstances
      .filter((bi) => bi.brigadeTypeId === bt.id)
      .reduce((s, bi) => s + countOf(bi.slotLines[slotIndex] ?? [], cap.unitIds), 0);
    if (inArmy >= cap.armyMax) return `Up to ${cap.armyMax} ${cap.label} in the army`;
  }

  if (slot.singleUnitType) {
    const other = lines.find((l) => l.qty > 0 && l.unitId !== unitId);
    if (other) return `Can't mix with ${unitName(nation, other.unitId)}`;
  }

  const limit = slot.unitLimits?.find((u) => u.unitId === unitId);
  if (limit && countOf(lines, [unitId]) >= limit.max) return `Up to ${limit.max} per brigade`;

  for (const g of slot.unitGroupLimits ?? []) {
    if (g.unitIds.includes(unitId) && countOf(lines, g.unitIds) >= g.max) {
      const label = g.label ?? g.unitIds.map((id) => unitName(nation, id)).join(" / ");
      return `Up to ${g.max} ${label} combined`;
    }
  }

  if (slot.mutuallyExclusiveGroups) {
    const groups = slot.mutuallyExclusiveGroups;
    const maxGroups = groups.find((g) => g.maxGroups != null)?.maxGroups ?? 1;
    const own = groups.find((g) => g.unitIds.includes(unitId));
    const present = groups.filter((g) => g !== own && lines.some((l) => l.qty > 0 && g.unitIds.includes(l.unitId)));
    const ownPresent = own && lines.some((l) => l.qty > 0 && own.unitIds.includes(l.unitId));
    if (own && !ownPresent && present.length >= maxGroups) {
      const names = present.map((g) => g.label ?? g.unitIds.map((id) => unitName(nation, id)).join("/"));
      return maxGroups === 1 ? `Not with ${names.join(", ")}` : `Already ${maxGroups} of these options`;
    }
  }

  const dyn = slot.dynamicUnitLimits?.find((d) => d.unitId === unitId);
  if (dyn) {
    const have = countOf(lines, [unitId]);
    if (dyn.perBattalions) {
      const battalions = dyn.perBattalions.countSlotIndices.reduce((s, i) => s + slotUnitCount(instance, i), 0);
      if (have >= Math.floor(battalions / dyn.perBattalions.ratio)) {
        // Named for what's counted: battalions, or batteries (an Artillery Brigade's Heavies, "up to half")
        const counted = dyn.perBattalions.countSlotIndices.flatMap((i) => [
          ...(bt.slots[i]?.unitIds ?? []),
          ...(bt.slots[i]?.regiment?.slots.flatMap((sub) => sub.unitIds) ?? []),
        ]);
        const noun = unitNoun(nation, counted, 2);
        return `1 per ${dyn.perBattalions.ratio} ${noun} (${battalions} in the brigade)`;
      }
    }
    if (dyn.perQualifyingRegiment) {
      const { regimentSlotIndices, minBattalions } = dyn.perQualifyingRegiment;
      let qualifying = 0;
      for (const i of regimentSlotIndices) {
        for (const reg of instance.regimentSlots?.[i] ?? []) {
          if (reg.slotLines.flat().reduce((s, l) => s + l.qty, 0) >= minBattalions) qualifying += 1;
        }
      }
      if (have >= qualifying) return `1 per regiment of ${minBattalions}+ battalions`;
    }
  }

  const cap = slot.unitCaps?.find((c) => c.unitId === unitId);
  if (cap) {
    if (!unitCapRequirementMet(cap, roster.brigadeInstances)) {
      return `Needs ${cap.requiresBrigades!.min} brigades first`;
    }
    const inArmy = roster.brigadeInstances
      .filter((bi) => bi.brigadeTypeId === bt.id)
      .reduce((s, bi) => s + countOf(bi.slotLines[slotIndex] ?? [], [unitId]), 0);
    const max = effectiveUnitCapMax(cap, roster.brigadeInstances);
    if (inArmy >= max) {
      return max === 0 && cap.maxRatio
        ? `Needs ${cap.maxRatio.ratio} brigades first`
        : `Up to ${max} in the army`;
    }
  }

  for (const rc of nation.unitRatioCaps ?? []) {
    if (!rc.capUnitIds.includes(unitId)) continue;
    if (rc.brigadeTypeIds && !rc.brigadeTypeIds.includes(bt.id)) continue;
    const have = countUnitsInArmy(
      roster.brigadeInstances.filter((bi) => !rc.brigadeTypeIds || rc.brigadeTypeIds.includes(bi.brigadeTypeId)),
      rc.capUnitIds
    );
    const per = countUnitsInArmy(roster.brigadeInstances, rc.perUnitIds);
    if (have >= Math.floor(per / rc.ratio)) {
      return `1 per ${rc.ratio} ${unitNoun(nation, rc.perUnitIds, rc.ratio)} in the army (has ${per})`;
    }
  }

  return null;
}

/**
 * Why taking a choice would break a brigade's `maxChoices` rule, or null. Adding to a choice that's
 * already taken is fine; starting a new one isn't once the brigade has its maximum.
 */
export function choiceBlockedReason(bt: BrigadeType, instance: RosterBrigadeInstance, slotIndex: number, unitId?: string): string | null {
  const rule = bt.maxChoices;
  if (!rule) return null;
  const choice = rule.choices.find((c) => c.slotIndex === slotIndex && (!unitId || !c.unitIds || c.unitIds.includes(unitId)));
  if (!choice || choiceTaken(instance, choice)) return null;
  return choicesTaken(bt, instance) >= rule.max ? rule.label : null;
}

/** Why one more of a unit can't be added to a regiment's sub-slot right now, or null if it can */
export function unitBlockedInRegimentSlot(
  place: SlotPlace,
  sub: RegimentSlot,
  lines: RosterUnitLine[],
  unitId: string
): string | null {
  const { nation } = place;
  const full = brigadeFullReason(place);
  if (full) return full;
  if (sub.singleUnitType) {
    const other = lines.find((l) => l.qty > 0 && l.unitId !== unitId);
    if (other) return `Can't mix with ${unitName(nation, other.unitId)}`;
  }
  const limit = sub.unitLimits?.find((u) => u.unitId === unitId);
  if (limit && countOf(lines, [unitId]) >= limit.max) return `Up to ${limit.max} per regiment`;
  return null;
}

/**
 * Why another regiment can't be added to a regiment slot, or null if it can: the slot's own maximum,
 * the brigade's combined regiment limit, the army-wide limit, or the brigade's battalion limit (a new
 * regiment starts with its minimum battalions).
 */
export function regimentBlockedReason(place: SlotPlace): string | null {
  const { roster, bt, instance, slotIndex } = place;
  const regDef = bt.slots[slotIndex].regiment!;
  const regiments = instance.regimentSlots?.[slotIndex] ?? [];
  if (regiments.length >= regDef.max) return `Up to ${regDef.max} per brigade`;

  const choiceReason = choiceBlockedReason(bt, instance, slotIndex);
  if (choiceReason) return choiceReason;

  // Only so many brigades may take more than a set number of these regiments (the Guard's Middle Guard)
  const above = regDef.limitBrigadesAbove;
  if (above && regiments.length >= above.count) {
    const others = roster.brigadeInstances.filter(
      (bi) => bi.key !== instance.key && bi.brigadeTypeId === bt.id && (bi.regimentSlots?.[slotIndex]?.length ?? 0) > above.count
    ).length;
    if (others >= above.maxBrigades) {
      return `Only ${above.maxBrigades} brigade${above.maxBrigades === 1 ? "" : "s"} may take more than ${above.count}`;
    }
  }

  const total = bt.maxRegimentsTotal;
  if (total?.slotIndices.includes(slotIndex)) {
    const n = total.slotIndices.reduce((s, i) => s + (instance.regimentSlots?.[i]?.length ?? 0), 0);
    if (n >= total.max) return `The brigade has its ${total.max} regiments`;
  }

  if (regDef.armyMax !== undefined) {
    const inArmy = roster.brigadeInstances
      .filter((bi) => bi.brigadeTypeId === bt.id)
      .reduce((s, bi) => s + (bi.regimentSlots?.[slotIndex]?.length ?? 0), 0);
    if (inArmy >= regDef.armyMax) return `Up to ${regDef.armyMax} in the army`;
  }

  const cap = bt.maxBattalions;
  if (cap && (!cap.countSlotIndices || cap.countSlotIndices.includes(slotIndex))) {
    const indices = cap.countSlotIndices ?? bt.slots.map((_, i) => i);
    const count = indices.reduce((s, i) => s + slotUnitCount(instance, i), 0);
    const needs = regDef.slots.reduce((s, sub) => s + sub.min, 0);
    if (count + needs > cap.max) return `The brigade has its ${cap.max} battalions`;
  }
  return null;
}
