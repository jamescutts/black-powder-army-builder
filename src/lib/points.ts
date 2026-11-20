import type { Nation } from "@/data/types";
import type { RosterBrigadeInstance, RosterState, RosterUnitLine } from "@/types/army";
import { unitCost } from "@/lib/units";
import { brigadeUnitLines, freeLines, resolveLine, type LineContext } from "@/lib/options";

/** Points for one line of the roster (a unit with its options, times how many), less any free credit */
export function lineTotal(nation: Nation, line: RosterUnitLine, ctx: LineContext = {}): number {
  const resolved = resolveLine(nation, line, ctx);
  if (!resolved) return 0;
  const cost = resolved.cost * line.qty;
  // A free unit costs nothing, never less: a downgrade on it doesn't take points off the rest of the army
  const credit = ctx.free?.get(line.key) ?? 0;
  return credit ? Math.max(0, cost - credit) : cost;
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

/** A brigade's points. Pass the army's `freeLines` so a free unit in it isn't charged. */
export function brigadeTotal(nation: Nation, instance: RosterBrigadeInstance, free?: ReadonlyMap<string, number>): number {
  const bt = nation.brigades.find((b) => b.id === instance.brigadeTypeId);
  return (
    (instance.commanderLine ? commanderTotal(nation, instance.commanderLine) : 0) +
    brigadeUnitLines(instance).reduce(
      (s, { line, regiment }) => s + lineTotal(nation, line, { bt, regimentOptions: regiment?.options, free }),
      0
    )
  );
}

export function commandTotal(nation: Nation, roster: RosterState): number {
  return roster.commandItems.reduce((s, l) => s + commanderTotal(nation, l), 0);
}

export function rosterTotal(nation: Nation, roster: RosterState): number {
  const free = freeLines(nation, roster);
  return commandTotal(nation, roster) + roster.brigadeInstances.reduce((s, b) => s + brigadeTotal(nation, b, free), 0);
}

/** How many unit lines the army has, command included */
export function unitCount(roster: RosterState): number {
  return roster.commandItems.length + roster.brigadeInstances.reduce((s, b) => s + brigadeLines(b).length, 0);
}
