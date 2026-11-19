import type { MetadataRoute } from "next";
import { nations, supplements } from "@/data";
import { SITE_URL } from "@/lib/meta";

// Every page worth finding: home, the Black Powder picker, each supplement and each army.
// The docs and the old /builder redirects are left out.
export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: `${SITE_URL}/`, priority: 1 },
    { url: `${SITE_URL}/black-powder`, priority: 0.9 },
    ...supplements.map((s) => ({ url: `${SITE_URL}/black-powder/${s.id}`, priority: 0.7 })),
    ...nations.map((n) => ({ url: `${SITE_URL}/black-powder/${n.supplementId}/${n.id}`, priority: 0.6 })),
  ];
}
