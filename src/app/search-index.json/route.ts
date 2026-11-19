// The site search's data: every rule set, supplement and army list, with where it lives. Built once at
// build time and fetched by the search box the first time it opens, so the header doesn't carry every list.

import { supplements, nations, getSupplement, getNationsForSupplement } from "@/data";
import { RULESETS } from "@/data/rulesets";
import type { SearchEntry } from "@/lib/search";

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
  ];
  return Response.json(entries);
}
