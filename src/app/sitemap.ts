import type { MetadataRoute } from "next";
import { nations, supplements } from "@/data";
import { battles, campaignsWithBattles } from "@/data/battles";
import { battleHref, campaignHref, HISTORICAL_FORCES_PATH } from "@/lib/forces";
import { SITE_URL } from "@/lib/meta";

// Every page worth finding: home, the Black Powder picker, each supplement and each army.
// The docs and the old /builder redirects are left out.
export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: `${SITE_URL}/`, priority: 1 },
    { url: `${SITE_URL}/black-powder`, priority: 0.9 },
    { url: `${SITE_URL}${HISTORICAL_FORCES_PATH}`, priority: 0.7 },
    ...campaignsWithBattles().map((c) => ({ url: `${SITE_URL}${campaignHref(c.id)}`, priority: 0.6 })),
    ...battles.map((b) => ({ url: `${SITE_URL}${battleHref(b)}`, priority: 0.5 })),
    ...supplements.map((s) => ({ url: `${SITE_URL}/black-powder/${s.id}`, priority: 0.7 })),
    ...nations.map((n) => ({ url: `${SITE_URL}/black-powder/${n.supplementId}/${n.id}`, priority: 0.6 })),
  ];
}
