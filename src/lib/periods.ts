import type { BrigadeSlot, BrigadeType, CampaignPeriod, Nation, UnitOption } from "@/data/types";
import type { RosterState } from "@/types/army";

/** The period the list is built for, or undefined for any period (or a list whose book has none) */
export function rosterPeriod(nation: Nation, roster: RosterState): CampaignPeriod | undefined {
  return roster.period ? nation.periods?.find((p) => p.id === roster.period) : undefined;
}

/** "Middle period (1809-1812)" */
export function periodText(period: CampaignPeriod): string {
  return `${period.label} period (${period.years})`;
}

/**
 * Whether a choice tagged with `periods` is offered in the list's period. Untagged choices are offered in
 * every period, and every choice is offered while the list has no period.
 */
export function inPeriod(periods: string[] | undefined, period: string | undefined): boolean {
  return !periods?.length || !period || periods.includes(period);
}

/** "Middle, Late" for the periods a choice belongs to, in the book's order */
function periodNames(nation: Nation, periods: string[]): string[] {
  return (nation.periods ?? []).filter((p) => periods.includes(p.id)).map((p) => p.label);
}

/** "Middle and Late period only", for a choice outside the list's period */
export function periodOnlyText(nation: Nation, periods: string[]): string {
  const labels = periodNames(nation, periods);
  const joined = labels.length > 1 ? `${labels.slice(0, -1).join(", ")} and ${labels[labels.length - 1]}` : labels[0];
  return `${joined} period only`;
}

/** An object as it is in one period: its `periodOverrides` for that period merged over it (null removes) */
function overridden<T extends { periodOverrides?: Record<string, Record<string, unknown>> }>(base: T, period?: string): T {
  const over = period ? base.periodOverrides?.[period] : undefined;
  if (!over) return base;
  const out: Record<string, unknown> = { ...base };
  for (const [key, value] of Object.entries(over)) {
    if (value === null) delete out[key];
    else out[key] = value;
  }
  return out as T;
}

/**
 * The list as it stands in the player's chosen period, for the builder, summary and checks: each period's
 * own limits in place of the usual ones, and anything from another period marked with why
 * (`periodBlocked`), so the pickers grey it out and the checks flag it if the list already has it. Nothing
 * is taken away, so a list that changes period keeps its units and says what no longer fits.
 *
 * An upgrade from only some periods keeps them in its name ("Veteran, Elite 4+ (Late)") unless the list
 * is built for one of them, when it needs no saying.
 */
export function nationForPeriod(nation: Nation, period: string | undefined): Nation {
  if (!nation.periods?.length) return nation;
  const blocked = (periods?: string[]) => (inPeriod(periods, period) ? undefined : periodOnlyText(nation, periods!));
  const option = (o: UnitOption): UnitOption => {
    const own = overridden(o, period);
    const named = o.periods?.length && !(period && o.periods.includes(period));
    return {
      ...own,
      label: named ? `${o.label} (${periodNames(nation, o.periods!).join(", ")})` : o.label,
      periodBlocked: blocked(o.periods),
    };
  };
  const slot = (s: BrigadeSlot): BrigadeSlot => ({ ...overridden(s, period), periodBlocked: blocked(s.periods) });
  const brigade = (bt: BrigadeType): BrigadeType => {
    const own = overridden(bt, period);
    return {
      ...own,
      periodBlocked: blocked(bt.periods),
      slots: own.slots.map(slot),
      options: own.options?.map(option),
    };
  };
  return {
    ...nation,
    units: nation.units.map((u) =>
      u.variants?.some((v) => v.periods?.length)
        ? { ...u, variants: u.variants.map((v) => ({ ...v, periodBlocked: blocked(v.periods) })) }
        : u
    ),
    brigades: nation.brigades.map(brigade),
    unitRatioCaps: nation.unitRatioCaps?.map((cap) => overridden(cap, period)),
  };
}

/** Why a unit can't be taken in a slot in the list's period, or null */
export function unitPeriodBlocked(nation: Nation, slot: BrigadeSlot, unitId: string, period: string | undefined): string | null {
  const periods = slot.unitPeriods?.[unitId];
  return periods && !inPeriod(periods, period) ? periodOnlyText(nation, periods) : null;
}
