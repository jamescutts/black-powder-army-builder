import type { CampaignPeriod, Nation } from "@/data/types";
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

/** "Middle and Late period only", for a choice outside the list's period */
export function periodOnlyText(nation: Nation, periods: string[]): string {
  const labels = (nation.periods ?? []).filter((p) => periods.includes(p.id)).map((p) => p.label);
  const joined = labels.length > 1 ? `${labels.slice(0, -1).join(", ")} and ${labels[labels.length - 1]}` : labels[0];
  return `${joined} period only`;
}
