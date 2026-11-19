import type { Metadata } from "next";
import { DisclaimerModal } from "@/components/DisclaimerModal";
import { pageMeta } from "@/lib/meta";

// The supplement picker's details; supplements and armies below set their own
export const metadata: Metadata = pageMeta({
  title: "Black Powder",
  description:
    "Points calculator for Black Powder supplement army lists. Choose a supplement and an army, then build your list and check it against the book's brigade limits.",
  path: "/black-powder",
});

export default function BlackPowderLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <DisclaimerModal />
      {children}
    </>
  );
}
