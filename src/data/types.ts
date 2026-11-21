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
  /** The campaign periods (ids from the nation's `periods`) this choice belongs to; all when left out */
  periods?: string[];
  /** Set by the builder (not in the data) when this is outside the list's period: why, e.g. "Late period only" */
  periodBlocked?: string;
}

/**
 * One of a list's campaign periods, e.g. Albion Triumphant's Peninsular "Early (1806-1808)". The player
 * picks one for their list, and choices tagged with other periods aren't offered.
 */
export interface CampaignPeriod {
  /** Short id used to tag choices, e.g. "early" */
  id: string;
  /** e.g. "Early" */
  label: string;
  /** e.g. "1806-1808" */
  years: string;
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
   * Maximum number of these regiments across the whole army, counted over every brigade of this type
   * (not other brigade types that happen to have a similar slot). Used for rules like "max 1 Light
   * Regiment per division". Omit for no army-wide cap.
   */
  armyMax?: number;
  /**
   * Only `maxBrigades` brigades in the army may take more than `count` of these regiments, e.g. the
   * Imperial Guard's "Only one brigade may take two Middle Guard regiments" → { count: 1, maxBrigades: 1 }
   */
  limitBrigadesAbove?: { count: number; maxBrigades: number };
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
   * This slot is only available when the combined qty of the listed unit ids within the SAME
   * brigade instance (counting every slot, flat and regiment sub-slots) reaches `min`.
   * Counting by unit id — rather than by slot position — keeps the rule stable when slots are
   * reordered and lets a mixed slot contribute only its eligible units.
   * e.g. Prussian "Foot Artillery only if 6+ infantry battalions taken" →
   * { unitIds: ["pr-musketeer", "pr-guard-musketeer", "pr-fusilier", "pr-guard-fusilier", "pr-jager"], min: 6 }
   * (a Jäger in the Brigade Support slot counts; a Dragoon/Hussar there does not).
   */
  requiresBrigadeCount?: { unitIds: string[]; min: number };
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
  /** The campaign periods this slot is offered in (ids from the nation's `periods`); all when left out */
  periods?: string[];
  /**
   * Units in this slot offered only in some campaign periods, e.g. a Brunswick Oels company sharing the
   * Tiny company slot with a Rifle company → { "pb-brunswick-oels-coy": ["middle", "late"] }
   */
  unitPeriods?: Record<string, string[]>;
  /**
   * Changes that apply in one campaign period, keyed by period id, e.g. an Early limit of "up to two in
   * the army" in place of the usual "1 in 4" → { "early": { "limit": { "max": 2, "armyWide": true } } }.
   * A null value removes the field in that period (e.g. "maxRatio": null for "0-1" with no ratio).
   */
  periodOverrides?: Record<string, Record<string, unknown>>;
  /** Set by the builder (not in the data) when this is outside the list's period: why, e.g. "Late period only" */
  periodBlocked?: string;
  /**
   * Combined caps on a GROUP of unit ids within a single brigade instance (this slot only).
   * The summed qty of all listed unit ids must not exceed `max`.
   * e.g. Russian Guard Light Cavalry: "up to 1 Life Guard Cossack OR Uhlan" →
   * { unitIds: ["ru-life-guard-cossack", "ru-life-guard-uhlan"], max: 1, label: "Cossack/Uhlan" }
   */
  unitGroupLimits?: { unitIds: string[]; max: number; label?: string }[];
  /**
   * Combined caps on a group of units across the whole army (every brigade of this type, this slot),
   * e.g. the Guard's "Polish or Dutch Lancers… maximum two regiments in the army"
   */
  unitGroupCaps?: { unitIds: string[]; armyMax: number; label: string }[];
  /**
   * Mutually exclusive unit groups within this slot: at most `maxGroups` of the listed groups may
   * have units present in a single brigade instance. Units within the same group can coexist.
   * `maxGroups` defaults to 1 (strictly exclusive). Set it higher for "choose up to N of the
   * following" rules. It is read from the first group entry that defines it.
   * e.g. French Heavy Cavalry "Carabinier/Cuirassier OR Dragoon" (at most one group) →
   * [{ unitIds: ["fr-carabinier", "fr-cuirassier"], label: "Carabinier/Cuirassier" },
   *  { unitIds: ["fr-dragoon"], label: "Dragoon" }]
   * e.g. Austrian Line Brigade "choose up to two of Grenadier / Grenz / 6-pdr" →
   * [{ unitIds: ["at-grenadier"], label: "Grenadier", maxGroups: 2 },
   *  { unitIds: ["at-grenz"], label: "Grenz" },
   *  { unitIds: ["at-6pdr-brigade-battery"], label: "6-pdr Battery" }]
   */
  mutuallyExclusiveGroups?: { unitIds: string[]; label?: string; maxGroups?: number }[];
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

/**
 * An upgrade or downgrade from a brigade's "Options" box in the book, e.g. "Upgrade any infantry battalion
 * to veteran status (Reliable, Elite 5+)... 8 points per battalion". Each unit (or, for `scope: "regiment"`,
 * each regiment) picks its own.
 */
export interface UnitOption {
  /** Unique within its brigade type, e.g. "veteran-infantry" */
  id: string;
  /** Short name shown on the toggle and after the unit's name, e.g. "Veteran" or "Half battery" */
  label: string;
  /**
   * Points per unit, negative for a downgrade. Leave it out for a `swapTo` option: the unit then costs
   * what the unit it becomes costs, e.g. Guard Musketeer 47 in place of Musketeer 36.
   */
  cost?: number;
  /** Unit ids (as picked in the slot, before any swap) this option can be taken on */
  appliesTo: string[];
  /**
   * "unit" (default): each unit takes it on its own. "regiment": the whole regiment takes it, applying to
   * every unit in it that's in `appliesTo`, e.g. "Upgrade 1 Infantry Regiment to Guard Status".
   */
  scope?: "unit" | "regiment";
  /** Options sharing a group can't be combined on one unit, e.g. "size" for Large and Small */
  group?: string;
  /**
   * How many may take it within one brigade: at most `max`, and/or one per `ratio` of the listed units
   * in the brigade, e.g. Large "1 per 4 battalions". For a regiment option this counts regiments.
   */
  limit?: {
    max?: number;
    per?: { unitIds: string[]; ratio: number };
    /**
     * Count across the whole army rather than the one brigade, e.g. Bavaria's "Upgrade 2 battalions in
     * the Army to Large" or "Upgrade up to half of all Infantry battalions to Veteran". Brigade types
     * that share the option (by id) share the count.
     */
    armyWide?: boolean;
    /**
     * Other options (by id) that count toward the same limit, e.g. Austria's German (+8) and Hungarian
     * (+6) Veteran upgrades, which together may cover "up to half of all German or Hungarian battalions"
     */
    sharedWith?: string[];
    /**
     * A cap across the whole army on top of the brigade's own limit, e.g. Britain's "Upgrade 1 in 4
     * battalions to Light infantry (maximum of 3 in army)". Counted by option id, like `armyWide`.
     */
    armyMax?: number;
  };
  /**
   * The size the unit becomes. Each step from its own size (Small, standard, Large) changes Hand-to-Hand
   * by 2 and Shooting and Stamina by 1, as the book's Large and Small stat lines are built (e.g. Austrian
   * Large line 8/4/4/4 against a standard 6/3/4/3), and swaps the Large or Small rule to match. The
   * points come from `cost` as usual.
   */
  size?: "large" | "standard" | "small";
  /** Special rules the unit gains, e.g. ["Reliable", "Elite 5+"] */
  addSpecial?: string[];
  /** Special rules the unit loses, e.g. ["Large"] when the Westphalian Guard is downgraded to standard size */
  removeSpecial?: string[];
  /** Added to the unit's stats, e.g. veteran cavalry's "+1 Hand-to-Hand" → { handToHand: 1 } */
  statBonus?: { handToHand?: number; shooting?: number; morale?: number };
  /**
   * The unit becomes another entry from the nation's units, with that entry's own stats, rules and
   * points, e.g. a half battery { "pr-foot-arty": "pr-foot-arty-half" }.
   */
  swapTo?: Record<string, string>;
  /** Option ids (unit or regiment) this can't be combined with, e.g. Veteran on a Guard regiment */
  excludes?: string[];
  /** Why `excludes` applies, shown on the greyed-out toggle, e.g. "Guard are already Reliable, Elite 4+" */
  excludesReason?: string;
  /** The campaign periods this upgrade is offered in (ids from the nation's `periods`); all when left out */
  periods?: string[];
  /**
   * Changes that apply in one campaign period, keyed by period id, e.g. an Early limit of "up to two in
   * the army" in place of the usual "1 in 4" → { "early": { "limit": { "max": 2, "armyWide": true } } }.
   * A null value removes the field in that period (e.g. "maxRatio": null for "0-1" with no ratio).
   */
  periodOverrides?: Record<string, Record<string, unknown>>;
  /** Set by the builder (not in the data) when this is outside the list's period: why, e.g. "Late period only" */
  periodBlocked?: string;
}

export interface BrigadeType {
  id: string;
  name: string;
  /** The campaign periods this brigade can be taken in (ids from the nation's `periods`); all when left out */
  periods?: string[];
  /**
   * Changes that apply in one campaign period, keyed by period id, e.g. an Early limit of "up to two in
   * the army" in place of the usual "1 in 4" → { "early": { "limit": { "max": 2, "armyWide": true } } }.
   * A null value removes the field in that period (e.g. "maxRatio": null for "0-1" with no ratio).
   */
  periodOverrides?: Record<string, Record<string, unknown>>;
  /** Set by the builder (not in the data) when this is outside the list's period: why, e.g. "Late period only" */
  periodBlocked?: string;
  /** Upgrades and downgrades from this brigade's Options box */
  options?: UnitOption[];
  /**
   * The brigade must have at least as many of `unitIds` as of `asUnitIds`, e.g. Austria's Advanced
   * Guard, whose "infantry battalions must equal or exceed the number of cavalry regiments"
   */
  atLeastAsMany?: { unitIds: string[]; asUnitIds: string[]; label: string };
  /**
   * Brigade types this one can't be taken alongside, e.g. Prussia 1815's "You may choose between
   * Cavalry Brigades or Landwehr Cavalry Brigades"
   */
  excludesBrigadeTypes?: string[];
  /**
   * At most `max` of these choices may be taken: a regiment slot is taken when it has a regiment, a
   * unit slot when it has any of `unitIds` (or any unit). e.g. Austria's Grenadier Brigade "can have a
   * maximum of two further choices" from a Line regiment, a Hussar regiment and a 6-pdr battery.
   */
  maxChoices?: { max: number; choices: { slotIndex: number; unitIds?: string[] }[]; label: string };
  /**
   * The most batteries this brigade can hold, its own and those attached to it, e.g. France's
   * Artillery Brigade "can have no more than 6 batteries". Batteries are counted by the army's
   * `attachBatteries` battery ids.
   */
  maxBatteries?: number;
  /**
   * This brigade's batteries can each be attached to another brigade in the army, which may then hold at
   * most `maxPerBrigade` batteries, its own included. `batteryUnitIds` says which units count as a
   * battery (half batteries are picked as their full battery, so the full ids are enough).
   * e.g. Prussian Army Artillery: "Batteries can be attached to any brigade although a Brigade can have
   * no more than 2 batteries."
   */
  attachBatteries?: { maxPerBrigade?: number; batteryUnitIds: string[] };
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
  maxRatio?: {
    brigadeTypeIds: string[];
    ratio: number;
    /**
     * Linked brigades holding any of these units don't count, e.g. Bavaria's "1 cavalry brigade per
     * infantry brigade, if no cavalry is attached to infantry brigades" → ["bav-chevau-leger"].
     */
    onlyWithout?: string[];
  };
  /**
   * Requires a minimum number of this brigade type that scales with the army's total points:
   * required = ceil(armyPoints / perPoints), i.e. at least one brigade for every `perPoints`
   * points (or fraction thereof) in the army.
   * e.g. Austria "you must have at least 1 Line Brigade per 500 points" → { perPoints: 500 }.
   * This is a per-points floor and is checked in addition to the static `min`.
   */
  minPerPoints?: { perPoints: number };
  /**
   * This brigade type cannot be added until the summed count of `brigadeTypeIds` reaches `min`,
   * e.g. a Heavy Cavalry Brigade that needs "2 Infantry Brigades taken" first.
   */
  requires?: { brigadeTypeIds: string[]; min: number } | { brigadeTypeIds: string[]; min: number }[];
  /**
   * A brigade mostly of one class, with at most `maxOthers` units from the rest, e.g. France's Peninsular
   * Cavalry Brigade: "2-3 Dragoons with up to one Chasseur regiment, or 2-4 Hussars or Chasseurs with up
   * to one Dragoon regiment". Units outside every group aren't counted.
   */
  mixLimit?: { groups: { unitIds: string[]; label: string }[]; maxOthers: number };
  /**
   * Maximum total units (battalions/regiments-worth) allowed across ALL slots in a single brigade
   * instance — counts flat slot lines and regiment sub-slot lines together.
   * e.g. French Infantry Brigade "max 10 battalions per brigade" → { maxBattalions: 10 }.
   * By default counts every unit; set `countSlotIndices` to only count specific slots.
   */
  maxBattalions?: {
    max: number;
    /** The fewest the brigade needs, counted the same way, e.g. a Spanish Vanguard's "1 to 2 battalions" */
    min?: number;
    countSlotIndices?: number[];
    /** Units counted as other than one battalion, e.g. a Spanish Light half-battalion → 0.5 */
    weights?: Record<string, number>;
    /** What's counted, for messages, e.g. "battalions" (the default) or "regiments" */
    noun?: string;
  };
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

/** Attribution for a fan/community-created army list, as opposed to an official Warlord Games book. */
export interface NationAttribution {
  /** Author or creator credited for this army list, e.g. "Napoleonic Wargames" */
  author: string;
  /** Link to the source (video, PDF, forum post, etc.) */
  sourceUrl?: string;
}

/**
 * One allowance for allied brigades, e.g. "up to 25% of points from the Imperial Guard list".
 * A nation can have several of these (see France 1812: 25% Imperial Guard, plus a further 25%
 * from any other allied list).
 */
export interface AlliesRule {
  /** Max percentage of the army's total points that may be spent on allies under this rule */
  maxPercent: number;
  /** Ids (from this data set) of the nations eligible as allies under this rule */
  nationIds?: string[];
  /**
   * Freeform qualifier for anything `nationIds` can't express — a generic "any one allied list"
   * grant with no specific nation named, or extra conditions carried over from the ally's own
   * list (e.g. the ally's minimums still apply to the points spent here).
   */
  note?: string;
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
  /** Set for fan/community-created lists (as opposed to an official Warlord Games supplement) to credit the author */
  attribution?: NationAttribution;
  units: UnitEntry[];
  /**
   * The list's campaign periods, in order, when its book divides it into them (Albion Triumphant's
   * Peninsular lists: Early, Middle and Late). The player picks one, or none to see every choice.
   */
  periods?: CampaignPeriod[];
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
  /**
   * Units that are limited across the whole army, whichever brigade types they're taken in, e.g. the
   * Peninsular British "Brunswick Light Infantry (only unit such per army)", offered in both the Infantry
   * Brigade and the KGL Light Brigade
   */
  armyUnitCaps?: { unitIds: string[]; max: number; label: string }[];
  unitRatioCaps?: {
    capUnitIds: string[];
    /** Count `capUnitIds` only in these brigade types (e.g. the Divisional Artillery, not a cavalry brigade's own battery) */
    brigadeTypeIds?: string[];
    perUnitIds: string[];
    ratio: number;
    label?: string;
    /** Changes in one campaign period, e.g. Late "one battery per 5 battalions" → { "late": { "ratio": 5 } } */
    periodOverrides?: Record<string, Record<string, unknown>>;
  }[];
  /**
   * At most a share of the brigade commanders may be rated above `maxRating`, e.g. Russia's "Half of all
   * Russian Brigade commanders, rounding up, must be Staff Rating 7" →
   * { maxRating: 7, maxShareAbove: 0.5 } (so at most half, rounding down, may be rated 8).
   */
  brigadeCommanderRating?: { maxRating: number; maxShareAbove: number; label: string };
  /**
   * Across the army there can't be more regiments holding `atMost` units than holding `atLeastAs`
   * units, e.g. Austria's "You cannot have more Hungarian than German regiments"
   */
  regimentBalance?: { atMost: string[]; atLeastAs: string[]; label: string }[];
  /**
   * The army commander is optional: the book's list has none, but one can be added (e.g. Albion
   * Triumphant's optional Corps Commander rule), so the builder doesn't ask for one
   */
  armyCommandOptional?: boolean;
  /**
   * The list's upgrades and downgrades are in, including a list whose book has none to add (the Vistula
   * Legion), so its notes don't say they're still to come
   */
  upgradesModelled?: boolean;
  /**
   * Units the army gets for free, e.g. Russia's "one irregular Cossack regiment for free, attached to any
   * cavalry brigade" (and Platov's one more). The first `count` units in the army from `unitIds` (in
   * `brigadeTypeIds`, when given) cost nothing; upgrades bought for them are still paid for. Each entry
   * in `perCommander` adds `count` more while one of its commanders leads the army.
   */
  freeUnits?: {
    unitIds: string[];
    brigadeTypeIds?: string[];
    count: number;
    perCommander?: { unitIds: string[]; count: number }[];
    label: string;
  };
  /**
   * Freeform bullet-point summary of the brigade / force-organisation rules for reference
   * (min/max counts, ratios, per-points scaling, unimplemented upgrades/downgrades, etc.) —
   * not in-game special rules or allied-contingent allowances. See `specialRules` and
   * `alliesRules` for those.
   */
  notes: string[];
  /**
   * National special rules with an in-game effect (formations, commander traits, unique unit
   * interactions, etc.), as opposed to `notes`' force-organisation reminders.
   * e.g. Prussia 1815 → "'No prisoners! No pity!': against a French army, all Prussian infantry
   * and cavalry count as Tough Fighters."
   */
  specialRules?: string[];
  /**
   * Allied-contingent allowances, e.g. "up to 25% of points from the Imperial Guard list".
   * Not currently enforced or buildable in the roster builder — shown for reference only.
   */
  alliesRules?: AlliesRule[];
}
