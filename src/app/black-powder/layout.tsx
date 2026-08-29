import type { Metadata } from "next";
import { DisclaimerModal } from "@/components/DisclaimerModal";

export const metadata: Metadata = {
  title: "Black Powder Army Builder",
  description: "Points calculator for Black Powder supplement army lists.",
};

export default function BlackPowderLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <DisclaimerModal />
      {children}
      <footer style={{
        borderTop: "1px solid var(--mantine-color-gray-3)",
        marginTop: "var(--mantine-spacing-xl)",
        padding: "var(--mantine-spacing-lg) var(--mantine-spacing-xl)",
        textAlign: "center",
      }}>
        <p style={{ margin: "0 0 6px", fontSize: "var(--mantine-font-size-xs)", color: "var(--mantine-color-dimmed)", lineHeight: 1.6 }}>
          This is an unofficial, fan-made tool and is not affiliated with, endorsed by, or associated with{" "}
          <a href="https://www.warlordgames.com" target="_blank" rel="noreferrer" style={{ color: "var(--mantine-color-brown-7)" }}>
            Warlord Games
          </a>{" "}in any way.
        </p>
        <p style={{ margin: "0 0 6px", fontSize: "var(--mantine-font-size-xs)", color: "var(--mantine-color-dimmed)", lineHeight: 1.6 }}>
          <em>Black Powder</em>, all supplement titles, army list content, and associated intellectual property are copyright &copy; Warlord Games. All rights reserved.
        </p>
      </footer>
    </>
  );
}
