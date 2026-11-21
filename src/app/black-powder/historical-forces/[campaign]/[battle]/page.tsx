import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { BattleForces } from "@/components/HistoricalForces";
import { battles, getBattle, getCampaign } from "@/data/battles";
import { battleHref } from "@/lib/forces";
import { pageMeta } from "@/lib/meta";

// Built ahead of time, so the installed app can save every page for use offline (app/sw.js)
export function generateStaticParams() {
  return battles.map((b) => ({ campaign: b.campaign, battle: b.id }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ campaign: string; battle: string }>;
}): Promise<Metadata> {
  const { campaign: campaignId, battle: battleId } = await params;
  const campaign = getCampaign(campaignId);
  const battle = getBattle(campaignId, battleId);
  if (!campaign || !battle) return {};
  return pageMeta({
    title: `${battle.name}, ${battle.date} · Historical forces`,
    description: `Black Powder forces as they fought at ${battle.name} (${battle.date}), in ${campaign.name}: ${battle.forces.map((f) => f.name).slice(0, 6).join(", ")}${battle.forces.length > 6 ? " and more" : ""}. Open one as a list of your own.`,
    path: battleHref(battle),
  });
}

export default async function BattlePage({ params }: { params: Promise<{ campaign: string; battle: string }> }) {
  const { campaign, battle } = await params;
  if (!getBattle(campaign, battle)) notFound();
  return <BattleForces campaignId={campaign} battleId={battle} />;
}
