const relative = new Intl.RelativeTimeFormat("en-GB", { numeric: "auto" });

/** When a saved army was last changed, as "Edited 3 days ago" (a date once it's a month old) */
export function edited(ms: number): string {
  const minutes = Math.round((ms - Date.now()) / 60000);
  if (minutes > -1) return "Edited just now";
  if (minutes > -60) return `Edited ${relative.format(minutes, "minute")}`;
  const hours = Math.round(minutes / 60);
  if (hours > -24) return `Edited ${relative.format(hours, "hour")}`;
  const days = Math.round(hours / 24);
  if (days > -30) return `Edited ${relative.format(days, "day")}`;
  return `Edited ${new Date(ms).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" })}`;
}
