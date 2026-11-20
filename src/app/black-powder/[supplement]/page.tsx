import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getSupplement, getNationsForSupplement, supplements } from "@/data";
import { pageMeta } from "@/lib/meta";
import { SupplementNationPicker } from "@/components/SupplementNationPicker";

// Built ahead of time, so the installed app can save every page for use offline (app/sw.js)
export function generateStaticParams() {
  return supplements.map((s) => ({ supplement: s.id }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ supplement: string }>;
}): Promise<Metadata> {
  const supplement = getSupplement((await params).supplement);
  if (!supplement) return {};
  const count = getNationsForSupplement(supplement.id).length;
  return pageMeta({
    title: `${supplement.name} · Black Powder`,
    description: `${supplement.blurb} ${count} army ${count === 1 ? "list" : "lists"} to build from.`,
    path: `/black-powder/${supplement.id}`,
  });
}

export default async function SupplementPage({
  params,
}: {
  params: Promise<{ supplement: string }>;
}) {
  const { supplement } = await params;
  if (!getSupplement(supplement)) notFound();
  return <SupplementNationPicker initialSupplementId={supplement} />;
}
