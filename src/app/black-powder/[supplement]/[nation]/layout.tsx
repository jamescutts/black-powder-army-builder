import type { Metadata } from "next";
import { getNation, getSupplement } from "@/data";
import { pageMeta } from "@/lib/meta";

// The builder page runs in the browser, so its title and description are set here instead
export async function generateMetadata({
  params,
}: {
  params: Promise<{ supplement: string; nation: string }>;
}): Promise<Metadata> {
  const { supplement: supplementId, nation: nationId } = await params;
  const nation = getNation(nationId);
  const supplement = getSupplement(supplementId);
  if (!nation || !supplement || nation.supplementId !== supplement.id) return {};
  return pageMeta({
    title: `${nation.name} · ${supplement.name}`,
    description: `${nation.name}: a Black Powder army list from ${supplement.name}. ${nation.blurb}`,
    path: `/black-powder/${supplement.id}/${nation.id}`,
  });
}

export default function NationLayout({ children }: { children: React.ReactNode }) {
  return children;
}
