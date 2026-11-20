import type { Metadata } from "next";
import { MyArmies } from "@/components/MyArmies";
import { pageMeta } from "@/lib/meta";

// Each visitor's own saved lists, read from their browser, so there's nothing here for search engines
export const metadata: Metadata = {
  ...pageMeta({
    title: "My armies",
    description: "Your saved army lists: open, copy or delete them.",
    path: "/armies",
  }),
  robots: { index: false },
};

export default function ArmiesPage() {
  return <MyArmies />;
}
