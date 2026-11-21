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
   * The player's own name for this unit, e.g. "1st Bn, Leib Regiment", or for a commander line the
   * commander's, e.g. "Generalmajor v. Horn". Its type is always shown alongside.
   */
  name?: string;
  /**
   * For a battery whose brigade type has `attachBatteries`: the key of the brigade instance it's
   * attached to, if any
   */
  attachedTo?: string;
}

/** A single regiment instance within a regiment-type slot */
export interface RosterRegimentInstance {
  key: string;
  /** The player's own name for this regiment, e.g. "Infantry Regiment No. 3"; its label and number otherwise */
  name?: string;
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
  /**
   * The campaign period the list is built for (an id from the nation's `periods`), for lists whose book
   * has them; unset for any period
   */
  period?: string;
  /**
   * The historical force (`HistoricalForce.id`) the list was started from, if any: the builder says so,
   * can put it back as it was, and shows where that force breaks the list's rules as historical
   * departures rather than mistakes
   */
  sourceForceId?: string;
  /** Free-standing Command category units (Divisional/Brigade Commanders) */
  commandItems: RosterUnitLine[];
  brigadeInstances: RosterBrigadeInstance[];
}

export function emptyRoster(nationId: string): RosterState {
  return { nationId, armyName: "", commandItems: [], brigadeInstances: [] };
}
