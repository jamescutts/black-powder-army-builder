export type UnitCategory = "Command" | "Infantry" | "Cavalry" | "Artillery" | "Support";

export interface UnitVariant {
  /** Short label shown in a select, e.g. "Musket" or "Staff rating 8" */
  label: string;
  cost: number;
  /** Optional stat overrides for this variant, merged over the base unit stats */
  handToHand?: string;
  shooting?: string;
}

export interface UnitEntry {
  id: string;
  name: string;
  category: UnitCategory;
  type: string;
  armament: string;
  handToHand?: string;
  shooting?: string;
  morale?: string;
  stamina?: string;
  special?: string[];
  /** Flat cost, used when the unit has a single price */
  cost?: number;
  /** Alternative priced options (weapon choice, staff rating, half/full battery, etc.) */
  variants?: UnitVariant[];
}

export interface BrigadeSlot {
  /** Label for this slot within the brigade, e.g. "Infantry Battalion" */
  label: string;
  /** Unit ids (from the nation's `units` list) eligible to fill this slot */
  unitIds: string[];
  /** Minimum number of units required in this slot per brigade instance */
  min: number;
  /** Maximum number of units allowed in this slot per brigade instance */
  max: number;
  /**
   * Per-unit caps that apply across every instance of this brigade type in the army
   * (not just one instance), e.g. "max 1 Chasseurs à Cheval de la Garde regiment in the army"
   * even though several brigades of this type may be taken.
   */
  unitCaps?: { unitId: string; armyMax: number }[];
}

export interface BrigadeType {
  id: string;
  name: string;
  /** Minimum number of this brigade type required in the army */
  min: number;
  /** Absolute maximum number of this brigade type allowed in the army */
  max: number;
  /**
   * Caps the number of this brigade type by how many of one or more other brigade types have been
   * taken (summed), e.g. French Light Cavalry Brigades are "1 per 2 Infantry Brigades" ->
   * { brigadeTypeIds: ["fr-infantry-brigade"], ratio: 2 }. Effective max is
   * min(max, floor(sum(count(brigadeTypeIds)) / ratio)).
   */
  maxRatio?: { brigadeTypeIds: string[]; ratio: number };
  /**
   * This brigade type cannot be added until the summed count of `brigadeTypeIds` reaches `min`,
   * e.g. a Heavy Cavalry Brigade that needs "2 Infantry Brigades taken" first.
   */
  requires?: { brigadeTypeIds: string[]; min: number };
  /**
   * Unit id (from the nation's `units` list, category "Command") this brigade must be led by.
   * Omitted for pooled/attached support brigades that don't carry their own commander
   * (e.g. reserve artillery, earthworks).
   */
  commanderUnitId?: string;
  slots: BrigadeSlot[];
  /** Extra conditions from the book that aren't structurally enforced (e.g. per-1000-point scaling, battalion-count thresholds) */
  note?: string;
}

export interface Supplement {
  id: string;
  name: string;
  blurb: string;
}

export interface Nation {
  id: string;
  /**
   * Id of the Supplement this nation's army list belongs to. Not present in the source JSON file —
   * it's attached at import time in src/data/index.ts based on which supplement's `nations/` folder
   * the file lives in.
   */
  supplementId: string;
  name: string;
  blurb: string;
  units: UnitEntry[];
  /** Brigade types available to this nation. Infantry/Cavalry/Artillery units can only be added inside a brigade instance. */
  brigades: BrigadeType[];
  /** Freeform bullet-point summary of the brigade / force-organisation rules for reference */
  notes: string[];
  alliesNote?: string;
}
