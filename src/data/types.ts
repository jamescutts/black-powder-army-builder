export type UnitCategory = "Command" | "Infantry" | "Cavalry" | "Artillery" | "Support";

export interface UnitVariant {
  /** Short label shown in a select, e.g. "Musket" or "Staff rating 8" */
  label: string;
  cost: number;
  /** Staff rating for this variant (commanders only), e.g. 7, 8, or 9 */
  staffRating?: number;
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
  /** Staff rating for named commanders with a fixed rating, e.g. 8 or 9 */
  staffRating?: number;
  /** Flat cost, used when the unit has a single price */
  cost?: number;
  /** Alternative priced options (weapon choice, staff rating, half/full battery, etc.) */
  variants?: UnitVariant[];
}

export interface RegimentSlot {
  /** Label for this sub-slot within the regiment, e.g. "Musketeer Battalion" */
  label: string;
  /** Unit ids eligible to fill this sub-slot */
  unitIds: string[];
  /** Minimum units required in this sub-slot per regiment */
  min: number;
  /** Maximum units allowed in this sub-slot per regiment */
  max: number;
}

export interface RegimentDef {
  /** Display label for the regiment group, e.g. "Infantry Regiment" */
  label: string;
  /** Minimum number of regiments required in this slot per brigade instance */
  min: number;
  /** Maximum number of regiments allowed in this slot per brigade instance */
  max: number;
  /** Internal composition of each regiment instance */
  slots: RegimentSlot[];
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
   * If present, this slot uses a regiment sub-structure instead of the flat unitIds/min/max.
   * The parent `unitIds`, `min`, and `max` are ignored when `regiment` is set.
   */
  regiment?: RegimentDef;
  /**
   * This slot is only available when the total unit qty across the listed sibling slot indices
   * (0-based, same brigade instance) reaches `min`.
   * e.g. "Foot Artillery only if 6+ infantry battalions taken" →
   * { slotIndices: [0, 1], min: 6 } where slots 0 and 1 are Musketeer and Fusilier.
   */
  requiresSlotFill?: { slotIndices: number[]; min: number };
  /**
   * This slot is only available when the total qty of the listed unit ids across the entire army
   * (all brigade instances, all slots including regiment sub-slots) reaches `min`.
   * e.g. "Divisional Artillery requires 8+ infantry battalions" →
   * { unitIds: ["it-line-infantry", "it-light-infantry", ...], min: 8 }
   */
  requiresArmyUnitCount?: { unitIds: string[]; min: number };
  /**
   * Per-unit caps that apply across every instance of this brigade type in the army
   * (not just one instance), e.g. "max 1 Chasseurs à Cheval de la Garde regiment in the army"
   * even though several brigades of this type may be taken.
   *
   * Optional `requiresBrigades`: this unit can only be taken when the summed count of the listed
   * brigade types reaches `min`, e.g. Heavy Artillery requires 3 brigades taken.
   *
   * Optional `maxRatio`: the effective armyMax is dynamic — floor(linkedBrigadeCount / ratio),
   * clamped to armyMax, e.g. Foot batteries at 1 per 2 brigades (max 2).
   */
  unitCaps?: {
    unitId: string;
    armyMax: number;
    /** Unit is only available when this many of the listed brigade types exist in the army */
    requiresBrigades?: { brigadeTypeIds: string[]; min: number };
    /** armyMax is dynamic: min(armyMax, floor(sum(count(brigadeTypeIds)) / ratio)) */
    maxRatio?: { brigadeTypeIds: string[]; ratio: number };
  }[];
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
  /** Path to the flag SVG served from /public, e.g. "/flags/france.svg" */
  flagFile?: string;
  /** Multiple flag paths, used when a nation entry covers several states (e.g. Confederation of the Rhine) */
  flagFiles?: string[];
  units: UnitEntry[];
  /** Brigade types available to this nation. Infantry/Cavalry/Artillery units can only be added inside a brigade instance. */
  brigades: BrigadeType[];
  /** Freeform bullet-point summary of the brigade / force-organisation rules for reference */
  notes: string[];
  alliesNote?: string;
}
