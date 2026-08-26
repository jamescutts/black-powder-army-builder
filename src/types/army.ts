export interface RosterUnitLine {
  key: string;
  unitId: string;
  variantLabel?: string;
  qty: number;
}

export interface RosterBrigadeInstance {
  key: string;
  brigadeTypeId: string;
  /** The brigade's own commander, required whenever the brigade type declares a `commanderUnitId` */
  commanderLine: RosterUnitLine | null;
  /** One array of lines per slot, indexed the same as the brigade type's `slots` array */
  slotLines: RosterUnitLine[][];
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
