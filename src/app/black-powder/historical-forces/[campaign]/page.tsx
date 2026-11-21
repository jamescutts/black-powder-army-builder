import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { CampaignForces } from "@/components/HistoricalForces";
import { battlesIn, campaigns, getCampaign } from "@/data/battles";
import { campaignHref } from "@/lib/forces";
import { pageMeta } from "@/lib/meta";

// Built ahead of time, so the installed app can save every page for use offline (app/sw.js)
export function generateStaticParams() {
  return campaigns.filter((c) => battlesIn(c.id).length > 0).map((c) => ({ campaign: c.id }));
}

export async function generateMetadata({ params }: { params: Promise<{ campaign: string }> }): Promise<Metadata> {
  const campaign = getCampaign((await params).campaign);
  if (!campaign) return {};
  const battles = battlesIn(campaign.id);
  return pageMeta({
    title: `${campaign.name} · Historical forces`,
    description: `Black Powder forces from ${campaign.name} (${campaign.dates}) as they fought at ${battles.map((b) => b.name).join(", ")}, ready to open as lists of your own.`,
    path: campaignHref(campaign.id),
  });
}

export default async function CampaignPage({ params }: { params: Promise<{ campaign: string }> }) {
  const { campaign } = await params;
  if (!getCampaign(campaign) || battlesIn(campaign).length === 0) notFound();
  return <CampaignForces campaignId={campaign} />;
}
