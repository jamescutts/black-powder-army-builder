import type { Nation } from "@/data/types";
import type { RosterBrigadeInstance, RosterState, RosterUnitLine } from "@/types/army";
import { unitCost } from "@/lib/units";

/** Points for one line of the roster (a unit, times how many) */
export function lineTotal(nation: Nation, line: RosterUnitLine): number {
  const unit = nation.units.find((u) => u.id === line.unitId);
  if (!unit) return 0;
  return unitCost(unit, line.variantLabel) * line.qty;
}

/** Every unit line in a brigade: its commander, its slots and the slots of its regiments */
function brigadeLines(instance: RosterBrigadeInstance): RosterUnitLine[] {
  return [
    ...(instance.commanderLine ? [instance.commanderLine] : []),
    ...instance.slotLines.flat(),
    ...(instance.regimentSlots ?? []).flatMap((slot) => (slot ?? []).flatMap((reg) => reg.slotLines.flat())),
  ];
}

export function brigadeTotal(nation: Nation, instance: RosterBrigadeInstance): number {
  return brigadeLines(instance).reduce((s, l) => s + lineTotal(nation, l), 0);
}

export function rosterTotal(nation: Nation, roster: RosterState): number {
  return (
    roster.commandItems.reduce((s, l) => s + lineTotal(nation, l), 0) +
    roster.brigadeInstances.reduce((s, b) => s + brigadeTotal(nation, b), 0)
  );
}

/** How many unit lines the army has, command included */
export function unitCount(roster: RosterState): number {
  return roster.commandItems.length + roster.brigadeInstances.reduce((s, b) => s + brigadeLines(b).length, 0);
}
