import type { BrigadeType, Nation, UnitEntry, UnitOption } from "@/data/types";
import type { RosterBrigadeInstance, RosterRegimentInstance, RosterState, RosterUnitLine } from "@/types/army";
import { unitCost } from "@/lib/units";

/** Where a unit line sits, which decides which options it can have and which apply to it */
export interface LineContext {
  bt?: BrigadeType;
  /** The options its regiment has taken, when it's in one */
  regimentOptions?: string[];
  /** The army's free lines and the points each is credited (see `freeLines`) */
  free?: ReadonlyMap<string, number>;
}

/** A unit as fielded: after its options, with the name, points, rules and stats to show for it */
export interface ResolvedUnit {
  /** The unit picked in the slot */
  base: UnitEntry;
  /** The unit it is once swaps apply (e.g. Guard Musketeer for a Musketeer in a Guard regiment) */
  unit: UnitEntry;
  /** Points for one of it, options included */
  cost: number;
  /** Labels of the options that don't swap the unit, e.g. ["Veteran", "Large"] */
  tags: string[];
  /** "Guard Musketeer (Veteran, Large)" */
  name: string;
  special: string[];
  handToHand?: string;
  shooting?: string;
  /** e.g. "5" for a battalion downgraded to Morale 5 */
  morale?: string;
  /** Changed by size: a Large unit has one more than standard, a Small unit one fewer */
  stamina?: string;
}

export const unitOptionsOf = (bt: BrigadeType | undefined) => (bt?.options ?? []).filter((o) => o.scope !== "regiment");
export const regimentOptionsOf = (bt: BrigadeType | undefined) => (bt?.options ?? []).filter((o) => o.scope === "regiment");

/** The unit-scope options a unit can be offered in this brigade */
export function optionsForUnit(bt: BrigadeType | undefined, unitId: string): UnitOption[] {
  return unitOptionsOf(bt).filter((o) => o.appliesTo.includes(unitId));
}

/** The regiment-scope options a regiment can take, given the units its slots accept */
export function optionsForRegiment(bt: BrigadeType | undefined, unitIds: string[]): UnitOption[] {
  return regimentOptionsOf(bt).filter((o) => o.appliesTo.some((id) => unitIds.includes(id)));
}

function addToStat(stat: string | undefined, bonus: number | undefined, floor = 0): string | undefined {
  if (!bonus || stat === undefined || !/^\d+$/.test(stat)) return stat;
  return String(Math.max(floor, Number(stat) + bonus));
}

const SIZE_RANK = { small: -1, standard: 0, large: 1 } as const;

/** A unit's own size, read from its rules: Large, Small, or standard (Tiny units don't change size) */
function sizeOf(special: string[] | undefined): keyof typeof SIZE_RANK | "tiny" {
  if (special?.includes("Tiny")) return "tiny";
  if (special?.includes("Large")) return "large";
  if (special?.includes("Small")) return "small";
  return "standard";
}

/** What a line's unit is once its own and its regiment's options apply */
export function resolveLine(nation: Nation, line: RosterUnitLine, ctx: LineContext = {}): ResolvedUnit | null {
  const base = nation.units.find((u) => u.id === line.unitId);
  if (!base) return null;

  // Regiment options first (Guard), then the unit's own (Veteran, Half battery), each only where it applies
  const regimentOpts = regimentOptionsOf(ctx.bt).filter(
    (o) => ctx.regimentOptions?.includes(o.id) && o.appliesTo.includes(base.id)
  );
  const unitOpts = optionsForUnit(ctx.bt, base.id).filter((o) => line.options?.includes(o.id));
  const applied = [...regimentOpts, ...unitOpts];

  let unit = base;
  for (const o of applied) {
    const to = o.swapTo?.[unit.id] ?? o.swapTo?.[base.id];
    const swapped = to ? nation.units.find((u) => u.id === to) : undefined;
    if (swapped) unit = swapped;
  }

  const modifiers = applied.filter((o) => !o.swapTo);
  const cost =
    unitCost(unit, unit === base ? line.variantLabel : undefined) + modifiers.reduce((s, o) => s + (o.cost ?? 0), 0);
  const tags = unitOpts.filter((o) => !o.swapTo).map((o) => o.label);
  const removed = new Set(modifiers.flatMap((o) => o.removeSpecial ?? []));
  const special = [...new Set([...(unit.special ?? []), ...modifiers.flatMap((o) => o.addSpecial ?? [])])].filter(
    (rule) => !removed.has(rule)
  );
  const bonus = (key: "handToHand" | "shooting" | "morale") => modifiers.reduce((s, o) => s + (o.statBonus?.[key] ?? 0), 0);

  // A size option moves the unit from its own size to the new one, a step at a time
  const resize = [...modifiers].reverse().find((o) => o.size);
  const own = sizeOf(unit.special);
  const steps = resize?.size && own !== "tiny" ? SIZE_RANK[resize.size] - SIZE_RANK[own] : 0;
  if (steps !== 0) {
    const sized = special.filter((rule) => rule !== "Large" && rule !== "Small");
    if (resize!.size !== "standard") sized.push(resize!.size === "large" ? "Large" : "Small");
    special.splice(0, special.length, ...sized);
  }

  return {
    base,
    unit,
    cost,
    tags,
    name: tags.length ? `${unit.name} (${tags.join(", ")})` : unit.name,
    special,
    handToHand: addToStat(unit.handToHand, bonus("handToHand") + 2 * steps),
    shooting: addToStat(unit.shooting, bonus("shooting") + (unit.shooting === "0" ? 0 : steps)),
    morale: addToStat(unit.morale, bonus("morale")),
    stamina: addToStat(unit.stamina, steps, 1),
  };
}

/** Every unit line in a brigade, each with the context it sits in (commander excluded) */
export function brigadeUnitLines(
  instance: RosterBrigadeInstance
): { line: RosterUnitLine; regiment?: RosterRegimentInstance }[] {
  return [
    ...instance.slotLines.flat().map((line) => ({ line })),
    ...(instance.regimentSlots ?? []).flatMap((slot) =>
      (slot ?? []).flatMap((regiment) => regiment.slotLines.flat().map((line) => ({ line, regiment })))
    ),
  ];
}

/** The brigades an option's limit counts over: the whole army when it says so, else the one brigade */
function limitScope(o: UnitOption, instance: RosterBrigadeInstance, army?: RosterBrigadeInstance[]) {
  return o.limit?.armyWide && army ? army : [instance];
}

/** How many of a unit option the brigade (or army) may have; Infinity when it isn't limited */
export function optionAllowance(o: UnitOption, instance: RosterBrigadeInstance, army?: RosterBrigadeInstance[]): number {
  let allowed = o.limit?.max ?? Infinity;
  if (o.limit?.per) {
    const ids = new Set(o.limit.per.unitIds);
    const count = limitScope(o, instance, army)
      .flatMap((bi) => brigadeUnitLines(bi))
      .filter(({ line }) => ids.has(line.unitId))
      .reduce((s, { line }) => s + line.qty, 0);
    allowed = Math.min(allowed, Math.floor(count / o.limit.per.ratio));
  }
  return allowed;
}

/** How many units (or, for a regiment option, regiments) in the brigade (or army) have taken an option */
export function optionTaken(o: UnitOption, instance: RosterBrigadeInstance, army?: RosterBrigadeInstance[]): number {
  const scope = limitScope(o, instance, army);
  const ids = [o.id, ...(o.limit?.sharedWith ?? [])];
  if (o.scope === "regiment") {
    return scope.reduce(
      (n, bi) =>
        n +
        (bi.regimentSlots ?? []).reduce(
          (m, slot) => m + (slot ?? []).filter((r) => ids.some((id) => r.options?.includes(id))).length,
          0
        ),
      0
    );
  }
  return scope
    .flatMap((bi) => brigadeUnitLines(bi))
    .filter(({ line }) => ids.some((id) => line.options?.includes(id)))
    .reduce((s, { line }) => s + line.qty, 0);
}

/** What an option adds to one of a unit's cost: its own cost, or the difference its swap makes */
export function optionDelta(nation: Nation, o: UnitOption, base: UnitEntry): number {
  const to = o.swapTo?.[base.id] ? nation.units.find((u) => u.id === o.swapTo![base.id]) : undefined;
  return to ? unitCost(to) - unitCost(base) : (o.cost ?? 0);
}

/** "+8", "−8", or "" when it's free */
export function signedPoints(n: number): string {
  if (n === 0) return "";
  return n > 0 ? `+${n}` : `\u2212${Math.abs(n)}`;
}

/** A regiment option's cost per battalion, e.g. "+11/bn", when it's the same for each unit it covers */
export function regimentOptionCost(nation: Nation, o: UnitOption): string {
  const deltas = new Set(
    o.appliesTo.flatMap((id) => {
      const base = nation.units.find((u) => u.id === id);
      return base ? [optionDelta(nation, o, base)] : [];
    })
  );
  if (deltas.size !== 1) return "";
  const text = signedPoints([...deltas][0]);
  return text ? `${text}/bn` : "";
}

const NOUNS: Record<string, [string, string]> = {
  Infantry: ["battalion", "battalions"],
  Cavalry: ["regiment", "regiments"],
  Artillery: ["battery", "batteries"],
};

/**
 * What the book calls these units: "battalion(s)" for infantry, "regiment(s)" for cavalry, "battery"
 * or "batteries" for artillery, and "unit(s)" when they're a mix.
 */
export function unitNoun(nation: Nation, unitIds: string[], count: number): string {
  const categories = new Set(unitIds.map((id) => nation.units.find((u) => u.id === id)?.category));
  const [one, many] = (categories.size === 1 && NOUNS[[...categories][0] ?? ""]) || ["unit", "units"];
  return count === 1 ? one : many;
}

/** A short limit for a toggle's tooltip, e.g. "1 per 4 battalions" or "1 per brigade" */
export function limitText(nation: Nation, o: UnitOption): string | null {
  const where = o.limit?.armyWide ? "in the army" : "per brigade";
  if (o.limit?.per) {
    const { ratio, unitIds } = o.limit.per;
    const noun = unitNoun(nation, unitIds, ratio);
    return ratio === 2
      ? `up to half of the ${unitNoun(nation, unitIds, 2)}${o.limit.armyWide ? " in the army" : " in the brigade"}`
      : `1 per ${ratio} ${noun}${o.limit.armyWide ? " in the army" : ""}`;
  }
  if (o.limit?.max !== undefined) return `${o.limit.max} ${where}`;
  return null;
}

/**
 * Why a unit can't take an option right now, or null if it can (or already has it). Options in the same
 * group as one it has are fine: taking one swaps out the other.
 */
export function unitOptionBlocked(
  nation: Nation,
  bt: BrigadeType,
  o: UnitOption,
  line: RosterUnitLine,
  instance: RosterBrigadeInstance,
  regimentOptions: string[] = [],
  army?: RosterBrigadeInstance[]
): string | null {
  if (line.options?.includes(o.id)) return null;
  const others = [...(line.options ?? []), ...regimentOptions];
  const clash = (bt.options ?? []).find(
    (other) => others.includes(other.id) && (o.excludes?.includes(other.id) || other.excludes?.includes(o.id))
  );
  if (clash) return o.excludesReason ?? clash.excludesReason ?? `Can't be combined with ${clash.label}`;
  const allowed = optionAllowance(o, instance, army);
  if (optionTaken(o, instance, army) >= allowed) {
    const limit = limitText(nation, o);
    return allowed === 0 && o.limit?.per
      ? `Needs ${o.limit.per.ratio} ${unitNoun(nation, o.limit.per.unitIds, o.limit.per.ratio)} in the ${o.limit.armyWide ? "army" : "brigade"} (${limit})`
      : `Limit reached${limit ? ` (${limit})` : ""}`;
  }
  return null;
}

/** Why a regiment can't take an option right now, or null if it can (or already has it) */
export function regimentOptionBlocked(
  o: UnitOption,
  regiment: RosterRegimentInstance,
  instance: RosterBrigadeInstance,
  army?: RosterBrigadeInstance[]
): string | null {
  if (regiment.options?.includes(o.id)) return null;
  if (optionTaken(o, instance, army) >= optionAllowance(o, instance, army)) {
    return `Only ${o.limit?.max ?? 0} regiment${o.limit?.max === 1 ? "" : "s"} ${o.limit?.armyWide ? "in the army" : "per brigade"}`;
  }
  return null;
}

/**
 * A line with an option turned on or off. Turning one on drops any other from the same group (Large
 * replaces Small).
 */
export function toggleLineOption(bt: BrigadeType, line: RosterUnitLine, optionId: string): RosterUnitLine {
  const current = line.options ?? [];
  if (current.includes(optionId)) {
    const options = current.filter((id) => id !== optionId);
    return { ...line, options: options.length ? options : undefined };
  }
  const o = bt.options?.find((x) => x.id === optionId);
  const sameGroup = new Set(
    o?.group ? (bt.options ?? []).filter((x) => x.group === o.group).map((x) => x.id) : []
  );
  return { ...line, options: [...current.filter((id) => !sameGroup.has(id)), optionId] };
}

/**
 * A regiment with an option turned on or off. Turning one on also drops its units' options it can't be
 * combined with (Veteran comes off a regiment made Guard).
 */
export function toggleRegimentOption(bt: BrigadeType, regiment: RosterRegimentInstance, optionId: string): RosterRegimentInstance {
  const current = regiment.options ?? [];
  if (current.includes(optionId)) {
    const options = current.filter((id) => id !== optionId);
    return { ...regiment, options: options.length ? options : undefined };
  }
  const o = bt.options?.find((x) => x.id === optionId);
  const clashes = new Set(
    (bt.options ?? [])
      .filter((x) => o?.excludes?.includes(x.id) || x.excludes?.includes(optionId))
      .map((x) => x.id)
  );
  return {
    ...regiment,
    options: [...current, optionId],
    slotLines: regiment.slotLines.map((lines) =>
      lines.map((l) => {
        const kept = (l.options ?? []).filter((id) => !clashes.has(id));
        return { ...l, options: kept.length ? kept : undefined };
      })
    ),
  };
}

// ─── Batteries attached to other brigades (e.g. Prussian Army Artillery) ─────

/** The army's attachment rule, from whichever brigade type's batteries can be attached */
export function attachRule(nation: Nation) {
  return nation.brigades.find((b) => b.attachBatteries)?.attachBatteries;
}

/**
 * How many batteries a brigade has: its own (any unit the attachment rule counts as a battery) plus
 * those attached to it from other brigades.
 */
export function batteriesIn(nation: Nation, brigades: RosterBrigadeInstance[], key: string): number {
  const rule = attachRule(nation);
  if (!rule) return 0;
  const ids = new Set(rule.batteryUnitIds);
  const target = brigades.find((b) => b.key === key);
  if (!target) return 0;
  const own = brigadeUnitLines(target)
    .filter(({ line }) => ids.has(line.unitId) && !line.attachedTo)
    .reduce((s, { line }) => s + line.qty, 0);
  const attached = brigades
    .flatMap((b) => brigadeUnitLines(b))
    .filter(({ line }) => line.attachedTo === key)
    .reduce((s, { line }) => s + line.qty, 0);
  return own + attached;
}

/** Brigades a battery can be attached to: every brigade whose own type doesn't attach its batteries out */
export function attachTargets(nation: Nation, brigades: RosterBrigadeInstance[]): RosterBrigadeInstance[] {
  return brigades.filter((b) => !nation.brigades.find((t) => t.id === b.brigadeTypeId)?.attachBatteries);
}

// ─── Units the army gets for free (Russia's free Cossack regiment) ───────────

/**
 * The lines that are free, each with the points it's credited: the base cost of the unit (its upgrades
 * are still paid for). The first lines that qualify, in brigade order, take the free places.
 */
export function freeLines(nation: Nation, roster: RosterState): Map<string, number> {
  const rule = nation.freeUnits;
  const free = new Map<string, number>();
  if (!rule) return free;
  let places =
    rule.count +
    (rule.perCommander ?? []).reduce(
      (n, extra) => n + (roster.commandItems.some((l) => extra.unitIds.includes(l.unitId)) ? extra.count : 0),
      0
    );
  for (const bi of roster.brigadeInstances) {
    if (rule.brigadeTypeIds && !rule.brigadeTypeIds.includes(bi.brigadeTypeId)) continue;
    for (const { line } of brigadeUnitLines(bi)) {
      if (places <= 0) return free;
      if (!rule.unitIds.includes(line.unitId)) continue;
      const unit = nation.units.find((u) => u.id === line.unitId);
      if (!unit) continue;
      free.set(line.key, unitCost(unit, line.variantLabel));
      places -= 1;
    }
  }
  return free;
}
