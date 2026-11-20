import type { BrigadeType, Nation } from "@/data/types";
import type { RosterBrigadeInstance, RosterState } from "@/types/army";
import { emptyRoster } from "@/types/army";
import { newKey } from "@/lib/id";
import { defaultVariantLabel } from "@/lib/units";
import { requirementMet } from "@/lib/brigadeLimits";

/** A new, empty brigade of a type: its commander (at the cheapest rating) and nothing else yet */
export function newBrigadeInstance(nation: Nation, bt: BrigadeType): RosterBrigadeInstance {
  const commanderUnit = bt.commanderUnitId ? nation.units.find((u) => u.id === bt.commanderUnitId) : undefined;
  return {
    key: newKey("brigade"),
    brigadeTypeId: bt.id,
    commanderLine: commanderUnit
      ? { key: newKey("cmd"), unitId: commanderUnit.id, variantLabel: defaultVariantLabel(commanderUnit), qty: 1 }
      : null,
    slotLines: bt.slots.map(() => []),
    regimentSlots: bt.slots.map((slot) => (slot.regiment ? [] : null)),
  };
}

/**
 * How a new list starts: with the brigades the army must have (e.g. "at least 1 Infantry Brigade"),
 * in the order the army list gives them, so there's no need to go looking for them first.
 */
export function startingRoster(nation: Nation): RosterState {
  const roster = emptyRoster(nation.id);
  for (const bt of nation.brigades) {
    for (let i = 0; i < bt.min; i++) {
      // A required brigade that itself needs another first is left for the player to add
      if (!requirementMet(bt, roster.brigadeInstances)) break;
      roster.brigadeInstances.push(newBrigadeInstance(nation, bt));
    }
  }
  return roster;
}
