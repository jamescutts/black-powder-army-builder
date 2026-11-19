import { getNationsForSupplement, getSupplement, supplements } from "@/data";
import { OG_SIZE, pageCard } from "@/lib/og";

// Each supplement's sharing image: its name, with the flags of up to three of its armies
export const alt = "A Black Powder supplement on Army Builder";
export const size = OG_SIZE;
export const contentType = "image/png";

export function generateStaticParams() {
  return supplements.map((s) => ({ supplement: s.id }));
}

export default async function Image({ params }: { params: Promise<{ supplement: string }> }) {
  const supplement = getSupplement((await params).supplement);
  const armies = supplement ? getNationsForSupplement(supplement.id) : [];
  const flags = [...new Set(armies.map((n) => n.flagFile ?? n.flagFiles?.[0]).filter((f): f is string => !!f))];
  return pageCard({
    kicker: `Black Powder · ${armies.length} army ${armies.length === 1 ? "list" : "lists"}`,
    title: supplement?.name ?? "Black Powder",
    flags: flags.slice(0, 2),
  });
}
