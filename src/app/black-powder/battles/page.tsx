import type { Metadata } from "next";
import { HistoricalForces } from "@/components/HistoricalForces";
import { pageMeta } from "@/lib/meta";
import { battles } from "@/data/battles";

export const metadata: Metadata = pageMeta({
  title: "Historical forces",
  description:
    `Black Powder divisions as they fought, from real orders of battle (${battles.map((b) => b.name).join(", ")}). Open one as a list of your own and change it as you like.`,
  path: "/black-powder/battles",
});

export default function HistoricalForcesPage() {
  return <HistoricalForces />;
}
