import { supplements, nations, getNation, getNationsForSupplement, getSupplement } from "@/data";
import { RULESETS } from "@/data/rulesets";
import type { Nation } from "@/data/types";
import { HomeView } from "@/components/HomeView";
import { AppHome } from "@/components/AppHome";
import { AppSwitch } from "@/components/AppSwitch";
import { SITE_DESCRIPTION, pageMeta } from "@/lib/meta";

export const metadata = pageMeta({ description: SITE_DESCRIPTION, path: "/" });

// Each from a different nation, so no flag shows twice
const FEATURED_ARMIES = [
  "france",
  "russia",
  "austria",
  "bavaria",
  "grand-duchy-of-warsaw",
  "peninsular-british",
  "spanish",
  "prussians-1815",
];

// Counts and supplement summaries are worked out here, on the server, so the home page
// doesn't send every army list to the browser.
export default function HomePage() {
  const counts = {
    rulesets: RULESETS.length,
    supplements: supplements.length,
    armies: nations.length,
    unitTypes: nations.reduce((sum, n) => sum + n.units.length, 0),
  };
  const supplementSummaries = supplements.map((s) => ({
    id: s.id,
    name: s.name,
    blurb: s.blurb,
    armies: getNationsForSupplement(s.id).length,
  }));

  const rulesets = RULESETS.map((r) => ({
    ...r,
    // Black Powder is the only rule set so far, so every supplement and army is one of its
    supplements: supplements.length,
    armies: nations.length,
  }));
  const toHomeArmy = (n: Nation) => ({
    name: n.name,
    blurb: n.blurb,
    supplement: getSupplement(n.supplementId)?.name ?? "",
    flags: n.flagFiles ?? (n.flagFile ? [n.flagFile] : []),
    href: `/black-powder/${n.supplementId}/${n.id}`,
  });
  // A few well-known armies to link to directly, one from each book where possible
  const armies = FEATURED_ARMIES.map(getNation)
    .filter((n) => n !== undefined)
    .map(toHomeArmy);
  // The app lists every army, book by book, to scroll through
  const allArmies = nations.map(toHomeArmy);

  // The installed app opens on its own home page, for getting back to an army; the browser's introduces the site
  return (
    <AppSwitch
      app={<AppHome supplements={supplementSummaries} armies={allArmies} />}
      browser={<HomeView counts={counts} rulesets={rulesets} supplements={supplementSummaries} armies={armies} />}
    />
  );
}
