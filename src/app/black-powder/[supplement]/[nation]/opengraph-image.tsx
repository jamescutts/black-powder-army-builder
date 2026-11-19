import { getNation, getSupplement, nations } from "@/data";
import { OG_SIZE, pageCard } from "@/lib/og";

// Each army's sharing image, so a shared list previews as its name, book and flag
export const alt = "A Black Powder army list on Army Builder";
export const size = OG_SIZE;
export const contentType = "image/png";

export function generateStaticParams() {
  return nations.map((n) => ({ supplement: n.supplementId, nation: n.id }));
}

export default async function Image({ params }: { params: Promise<{ supplement: string; nation: string }> }) {
  const { nation: nationId } = await params;
  const nation = getNation(nationId);
  const supplement = nation ? getSupplement(nation.supplementId) : undefined;
  const flags = nation?.flagFiles ?? (nation?.flagFile ? [nation.flagFile] : []);
  return pageCard({
    kicker: supplement ? `Black Powder · ${supplement.name}` : "Black Powder",
    title: nation?.name ?? "Army list",
    flags,
  });
}
