import type { Metadata } from "next";
import { HistoricalCampaigns } from "@/components/HistoricalForces";
import { campaigns } from "@/data/battles";
import { HISTORICAL_FORCES_PATH } from "@/lib/forces";
import { pageMeta } from "@/lib/meta";

export const metadata: Metadata = pageMeta({
  title: "Historical forces",
  description: `Black Powder divisions as they fought, from real orders of battle (${campaigns.map((c) => c.name).join(", ")}). Open one as a list of your own and change it as you like.`,
  path: HISTORICAL_FORCES_PATH,
});

export default function HistoricalForcesPage() {
  return <HistoricalCampaigns />;
}
