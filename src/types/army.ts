export interface RosterUnitLine {
  key: string;
  unitId: string;
  variantLabel?: string;
  /**
   * How many of this unit the line holds. Lists are now one line per unit (so each can take its own
   * upgrades) and new lines are always 1; older saves are split into single lines when they load.
   */
  qty: number;
  /** Ids of the unit-scope options (from the brigade type's `options`) this unit has taken */
  options?: string[];
  /**
   * For a battery whose brigade type has `attachBatteries`: the key of the brigade instance it's
   * attached to, if any
   */
  attachedTo?: string;
}

/** A single regiment instance within a regiment-type slot */
export interface RosterRegimentInstance {
  key: string;
  /** Ids of the regiment-scope options (e.g. Guard status) this regiment has taken */
  options?: string[];
  /** One array of unit lines per regiment sub-slot, indexed same as RegimentDef.slots */
  slotLines: RosterUnitLine[][];
}

export interface RosterBrigadeInstance {
  key: string;
  brigadeTypeId: string;
  /** The player's own name for this brigade, e.g. "Friant's Brigade"; its type is shown alongside */
  name?: string;
  /** The brigade's own commander, required whenever the brigade type declares a `commanderUnitId` */
  commanderLine: RosterUnitLine | null;
  /** One array of lines per slot, indexed the same as the brigade type's `slots` array */
  slotLines: RosterUnitLine[][];
  /**
   * For regiment-type slots: one array of regiment instances per slot, indexed the same as
   * the brigade type's `slots` array. Only populated for slots that have a `regiment` definition.
   * For non-regiment slots this entry is undefined/empty.
   */
  regimentSlots: (RosterRegimentInstance[] | null)[];
}

export interface RosterState {
  nationId: string;
  /** The player's own name for the list, e.g. "Davout's I Corps"; empty until they give it one */
  armyName: string;
  /** Free-standing Command category units (Divisional/Brigade Commanders) */
  commandItems: RosterUnitLine[];
  brigadeInstances: RosterBrigadeInstance[];
}

export function emptyRoster(nationId: string): RosterState {
  return { nationId, armyName: "", commandItems: [], brigadeInstances: [] };
}
