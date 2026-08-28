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
  /**
   * When true, all units in this sub-slot must be the same unit id (no mixing types).
   * e.g. French Foreign Regiment: Spanish OR Portuguese OR Rhinbund, not mixed.
   */
  singleUnitType?: boolean;
  /** Per-unit caps within this sub-slot, e.g. Rhinbund limited to 1 battalion. */
  unitLimits?: { unitId: string; max: number }[];
}

export interface RegimentDef {
  /** Display label for the regiment group, e.g. "Infantry Regiment" */
  label: string;
  /** Minimum number of regiments required in this slot per brigade instance */
  min: number;
  /** Maximum number of regiments allowed in this slot per brigade instance */
  max: number;
  /**
   * Maximum number of these regiments across the WHOLE army (all brigade instances of this type
   * and, when this slot appears in multiple brigade types, all of them). Used for rules like
   * "max 1 Light Regiment per division". Omit for no army-wide cap.
   */
  armyMax?: number;
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
   * If present, the effective slot `max` scales with the army's total points:
   * effectiveMax = floor(armyPoints / perPoints), clamped to at least the static `max` value if
   * you want a floor — here it simply overrides `max`.
   * e.g. Earthworks "1 per 500 points" → { perPoints: 500 }.
   */
  maxPerPoints?: { perPoints: number };
  /**
   * Per-unit caps within this slot whose max is computed dynamically from the SAME brigade
   * instance's composition. Used for regimental artillery rules:
   *  - `perBattalions`: max = floor(total units in `countSlotIndices` / ratio)
   *    e.g. section "1 per 2 battalions" → { unitId, perBattalions: { countSlotIndices: [0,1,2], ratio: 2 } }
   *  - `perQualifyingRegiment`: max = number of regiments (in `regimentSlotIndices`) whose battalion
   *    count is at least `minBattalions`.
   *    e.g. battery "1 per regiment of 3+ battalions" →
   *    { unitId, perQualifyingRegiment: { regimentSlotIndices: [0,1,2], minBattalions: 3 } }
   */
  dynamicUnitLimits?: {
    unitId: string;
    perBattalions?: { countSlotIndices: number[]; ratio: number };
    perQualifyingRegiment?: { regimentSlotIndices: number[]; minBattalions: number };
  }[];
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
   * When true, all units filling this slot (within a single brigade instance) must be the same
   * unit id — you cannot mix different unit types.
   * e.g. Russian Heavy Cavalry: "cannot mix Cuirassier and Dragoon regiments".
   */
  singleUnitType?: boolean;
  /**
   * Per-unit caps that apply within a single brigade instance (this slot only).
   * e.g. Russian Light Cavalry Brigade: "up to 2 Dragoon, up to 1 Uhlan" per brigade.
   */
  unitLimits?: { unitId: string; max: number }[];
  /**
   * Combined caps on a GROUP of unit ids within a single brigade instance (this slot only).
   * The summed qty of all listed unit ids must not exceed `max`.
   * e.g. Russian Guard Light Cavalry: "up to 1 Life Guard Cossack OR Uhlan" →
   * { unitIds: ["ru-life-guard-cossack", "ru-life-guard-uhlan"], max: 1, label: "Cossack/Uhlan" }
   */
  unitGroupLimits?: { unitIds: string[]; max: number; label?: string }[];
  /**
   * Mutually exclusive unit groups within this slot: at most ONE of the listed groups may have
   * units present in a single brigade instance. Units within the same group can coexist.
   * e.g. French Heavy Cavalry "Carabinier/Cuirassier OR Dragoon" →
   * [{ unitIds: ["fr-carabinier", "fr-cuirassier"], label: "Carabinier/Cuirassier" },
   *  { unitIds: ["fr-dragoon"], label: "Dragoon" }]
   */
  mutuallyExclusiveGroups?: { unitIds: string[]; label?: string }[];
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
   * Maximum total units (battalions/regiments-worth) allowed across ALL slots in a single brigade
   * instance — counts flat slot lines and regiment sub-slot lines together.
   * e.g. French Infantry Brigade "max 10 battalions per brigade" → { maxBattalions: 10 }.
   * By default counts every unit; set `countSlotIndices` to only count specific slots.
   */
  maxBattalions?: { max: number; countSlotIndices?: number[] };
  /**
   * Maximum combined number of regiments across the listed regiment-slot indices in a single
   * brigade instance. e.g. French Infantry Brigade "1-3 Infantry Regiments total" across the
   * Line/Light/Foreign regiment slots → { slotIndices: [0, 1, 2], max: 3 }.
   */
  maxRegimentsTotal?: { slotIndices: number[]; max: number; min?: number };
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
  /**
   * Points-percentage caps on groups of brigade types, relative to the whole army's total points.
   * e.g. Russian Imperial Guard brigades combined may not exceed 25% of the army →
   * { brigadeTypeIds: ["ru-guard-infantry-brigade", ...], maxPercent: 25, label: "Imperial Guard" }
   */
  pointsCaps?: { brigadeTypeIds: string[]; maxPercent: number; label?: string }[];
  /**
   * Army-wide ratio caps on certain units, limited by the count of other units in the army.
   * The total qty of `capUnitIds` across the whole army may not exceed floor(count(perUnitIds) / ratio).
   * e.g. Russian Light batteries: "1 per 6 infantry battalions in the army" →
   * { capUnitIds: ["ru-light-arty-half", "ru-light-arty"], perUnitIds: [<all infantry battalions>], ratio: 6, label: "Light batteries" }
   */
  unitRatioCaps?: {
    capUnitIds: string[];
    perUnitIds: string[];
    ratio: number;
    label?: string;
  }[];
  /** Freeform bullet-point summary of the brigade / force-organisation rules for reference */
  notes: string[];
  alliesNote?: string;
}
