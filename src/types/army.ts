export interface RosterUnitLine {
  key: string;
  unitId: string;
  variantLabel?: string;
  qty: number;
}

/** A single regiment instance within a regiment-type slot */
export interface RosterRegimentInstance {
  key: string;
  /** One array of unit lines per regiment sub-slot, indexed same as RegimentDef.slots */
  slotLines: RosterUnitLine[][];
}

export interface RosterBrigadeInstance {
  key: string;
  brigadeTypeId: string;
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
  armyName: string;
  /** Free-standing Command category units (Divisional/Brigade Commanders) */
  commandItems: RosterUnitLine[];
  brigadeInstances: RosterBrigadeInstance[];
}

export function emptyRoster(nationId: string): RosterState {
  return { nationId, armyName: "My Army", commandItems: [], brigadeInstances: [] };
}
