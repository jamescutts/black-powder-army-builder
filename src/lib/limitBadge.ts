/**
 * Plain wording for a slot's count against its limits, e.g. "1 of up to 3", "needs 1–5" or "5 · full",
 * with the badge colour: red when out of range, green when in range, grey for an empty optional slot.
 */
export function limitBadge(
  total: number,
  min: number | undefined,
  max: number | undefined
): { label: string; color: string } {
  const lo = min ?? 0;

  // A cap that's currently zero, e.g. "1 per 500 points" in a small army
  if (max === 0) {
    return total > 0
      ? { label: `${total} · none allowed`, color: "red" }
      : { label: "none allowed yet", color: "gray" };
  }

  if (max !== undefined && total > max) return { label: `too many · ${total} of ${max}`, color: "red" };

  if (total < lo) {
    const need = max === undefined ? `${lo}+` : lo === max ? `${lo}` : `${lo}–${max}`;
    return { label: total === 0 ? `needs ${need}` : `${total} · needs ${need}`, color: "red" };
  }

  if (max !== undefined && total === max) return { label: `${total} · full`, color: "green" };

  if (max === undefined) return { label: `${total}`, color: total === 0 ? "gray" : "green" };
  return { label: `${total} of up to ${max}`, color: total === 0 ? "gray" : "green" };
}
