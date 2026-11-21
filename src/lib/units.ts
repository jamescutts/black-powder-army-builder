import type { UnitEntry } from "@/data/types";

export function unitCost(unit: UnitEntry, variantLabel?: string): number {
  if (unit.variants && unit.variants.length > 0) {
    const variant = unit.variants.find((v) => v.label === variantLabel) ?? unit.variants[0];
    return variant.cost;
  }
  return unit.cost ?? 0;
}

export function defaultVariantLabel(unit: UnitEntry): string | undefined {
  return unit.variants && unit.variants.length > 0 ? unit.variants[0].label : undefined;
}

export function unitStatLine(unit: UnitEntry): string {
  const parts: string[] = [];
  if (unit.handToHand) parts.push(`H2H ${unit.handToHand}`);
  if (unit.shooting) parts.push(`Sh ${unit.shooting}`);
  if (unit.morale) parts.push(`Mo ${unit.morale}`);
  if (unit.stamina) parts.push(`St ${unit.stamina}`);
  return parts.join(" · ");
}

/**
 * A unit's priced choices for a Select. One from another campaign period is left out, unless it's the
 * one already chosen, which stays (and says why it doesn't fit) so the Select can still show it.
 */
export function variantSelectData(unit: UnitEntry, current?: string): { value: string; label: string }[] {
  return (unit.variants ?? [])
    .filter((v) => !v.periodBlocked || v.label === current)
    .map((v) => ({
      value: v.label,
      label: v.periodBlocked ? `${v.label} (${v.cost} pts, ${v.periodBlocked})` : `${v.label} (${v.cost} pts)`,
    }));
}
