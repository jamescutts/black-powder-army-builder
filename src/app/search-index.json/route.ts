// The site search's data: every rule set, supplement, army list and historical campaign and battle, with
// where it lives. Built once at build time and fetched by the search box the first time it opens, so the
// header doesn't carry every list.

import { supplements, nations, getSupplement, getNationsForSupplement } from "@/data";
import { RULESETS } from "@/data/rulesets";
import type { SearchEntry } from "@/lib/search";
import { battlesIn, campaigns, campaignsWithBattles, isPlanned, scheduleIn } from "@/data/battles";
import { battleHref, campaignHref, HISTORICAL_FORCES_PATH } from "@/lib/forces";

export const dynamic = "force-static";

export function GET() {
  const entries: SearchEntry[] = [
    ...RULESETS.map((r): SearchEntry => ({ k: "rules", t: r.name, d: r.blurb, h: r.href })),
    ...supplements.map((s): SearchEntry => {
      const count = getNationsForSupplement(s.id).length;
      return {
        k: "supplement",
        t: s.name,
        d: `Black Powder · ${count} ${count === 1 ? "army list" : "army lists"}`,
        h: `/black-powder/${s.id}`,
        x: s.blurb,
      };
    }),
    ...nations.map((n): SearchEntry => {
      const supplement = getSupplement(n.supplementId);
      return {
        k: "nation",
        t: n.name,
        d: supplement?.name ?? "",
        h: `/black-powder/${n.supplementId}/${n.id}`,
        // Its book, description and author, so "Waterloo", "Wellington" or a list's author find it too
        x: [supplement?.name, n.blurb, n.attribution?.author].filter(Boolean).join(" "),
      };
    }),
    // Each campaign of historical forces, and each of its battles, with the forces' names and commanders so
    // "Picton" or "Bülow" finds the battle they fought in
    ...campaignsWithBattles().flatMap((c): SearchEntry[] => {
      const battles = battlesIn(c.id);
      return [
        { k: "historical", t: c.name, d: `Historical forces · ${c.dates}`, h: campaignHref(c.id), x: battles.map((b) => b.name).join(" ") },
        ...battles.map((b): SearchEntry => ({
          k: "historical",
          t: b.name,
          d: `${c.name} · ${b.date}`,
          h: battleHref(b),
          x: b.forces.map((f) => `${f.name} ${f.formation ?? ""}`).join(" "),
        })),
        // Battles still to come, so searching for one says so, on its campaign's page
        ...scheduleIn(c.id)
          .filter(isPlanned)
          .map((b): SearchEntry => ({ k: "historical", t: b.name, d: `${c.name} · ${b.date} · coming soon`, h: campaignHref(c.id) })),
      ];
    }),
    // Campaigns still to come, on the Historical forces page
    ...campaigns
      .filter((c) => scheduleIn(c.id).length === 0)
      .map((c): SearchEntry => ({ k: "historical", t: c.name, d: `Historical forces · ${c.dates} · coming soon`, h: HISTORICAL_FORCES_PATH })),
  ];
  return Response.json(entries);
}
