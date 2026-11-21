import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { CampaignBattles } from "@/components/HistoricalForces";
import { campaignsWithBattles, getCampaign, scheduleIn } from "@/data/battles";
import { campaignHref } from "@/lib/forces";
import { pageMeta } from "@/lib/meta";

// Built ahead of time, so the installed app can save every page for use offline (app/sw.js)
export function generateStaticParams() {
  return campaignsWithBattles().map((c) => ({ campaign: c.id }));
}

export async function generateMetadata({ params }: { params: Promise<{ campaign: string }> }): Promise<Metadata> {
  const campaign = getCampaign((await params).campaign);
  if (!campaign) return {};
  const battles = scheduleIn(campaign.id);
  return pageMeta({
    title: `${campaign.name} · Historical forces`,
    description: `Black Powder forces from ${campaign.name} (${campaign.dates}) at ${battles.map((b) => b.name).join(", ")}, ready to open as lists of your own.`,
    path: campaignHref(campaign.id),
  });
}

export default async function CampaignPage({ params }: { params: Promise<{ campaign: string }> }) {
  const { campaign } = await params;
  if (!getCampaign(campaign) || scheduleIn(campaign).length === 0) notFound();
  return <CampaignBattles campaignId={campaign} />;
}
