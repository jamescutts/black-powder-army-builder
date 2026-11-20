import type { Nation } from "@/data/types";
import type { RosterBrigadeInstance, RosterState, RosterUnitLine } from "@/types/army";
import { unitCost } from "@/lib/units";
import { brigadeUnitLines, resolveLine, type LineContext } from "@/lib/options";

/** Points for one line of the roster (a unit with its options, times how many) */
export function lineTotal(nation: Nation, line: RosterUnitLine, ctx: LineContext = {}): number {
  const resolved = resolveLine(nation, line, ctx);
  return resolved ? resolved.cost * line.qty : 0;
}

/** Points for a commander line (commanders take no options) */
function commanderTotal(nation: Nation, line: RosterUnitLine): number {
  const unit = nation.units.find((u) => u.id === line.unitId);
  return unit ? unitCost(unit, line.variantLabel) * line.qty : 0;
}

/** Every unit line in a brigade: its commander, its slots and the slots of its regiments */
function brigadeLines(instance: RosterBrigadeInstance): RosterUnitLine[] {
  return [
    ...(instance.commanderLine ? [instance.commanderLine] : []),
    ...brigadeUnitLines(instance).map(({ line }) => line),
  ];
}

export function brigadeTotal(nation: Nation, instance: RosterBrigadeInstance): number {
  const bt = nation.brigades.find((b) => b.id === instance.brigadeTypeId);
  return (
    (instance.commanderLine ? commanderTotal(nation, instance.commanderLine) : 0) +
    brigadeUnitLines(instance).reduce(
      (s, { line, regiment }) => s + lineTotal(nation, line, { bt, regimentOptions: regiment?.options }),
      0
    )
  );
}

export function commandTotal(nation: Nation, roster: RosterState): number {
  return roster.commandItems.reduce((s, l) => s + commanderTotal(nation, l), 0);
}

export function rosterTotal(nation: Nation, roster: RosterState): number {
  return commandTotal(nation, roster) + roster.brigadeInstances.reduce((s, b) => s + brigadeTotal(nation, b), 0);
}

/** How many unit lines the army has, command included */
export function unitCount(roster: RosterState): number {
  return roster.commandItems.length + roster.brigadeInstances.reduce((s, b) => s + brigadeLines(b).length, 0);
}
