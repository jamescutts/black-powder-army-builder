import { nations, supplements } from "@/data";
import { RULESETS } from "@/data/rulesets";
import { OG_SIZE, siteCard } from "@/lib/og";

// The site's sharing image, used by every page without its own
export const alt = "Army Builder: points calculators for tabletop wargame army lists";
export const size = OG_SIZE;
export const contentType = "image/png";

const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;

export default function Image() {
  return siteCard({
    tagline: "Points calculators for tabletop wargame army lists",
    stats: [
      plural(RULESETS.length, "rule set", "rule sets"),
      plural(supplements.length, "supplement", "supplements"),
      plural(nations.length, "army list", "army lists"),
    ].join(" · "),
  });
}
