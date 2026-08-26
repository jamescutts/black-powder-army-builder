import "@mantine/core/styles.css";
import "./globals.css";

import type { Metadata } from "next";
import { ColorSchemeScript, MantineProvider } from "@mantine/core";
import { bodyFont, headingFont, scriptFont } from "./fonts";
import { theme } from "@/theme";

export const metadata: Metadata = {
  title: "Black Powder Army Builder",
  description: "Points calculator for Black Powder supplement army lists.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      className={`${bodyFont.variable} ${headingFont.variable} ${scriptFont.variable}`}
    >
      <head>
        <ColorSchemeScript defaultColorScheme="light" forceColorScheme="light" />
      </head>
      <body>
        <MantineProvider theme={theme} defaultColorScheme="light" forceColorScheme="light">
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
            <p style={{ margin: 0, fontSize: "var(--mantine-font-size-xs)", color: "var(--mantine-color-dimmed)", lineHeight: 1.6 }}>
              This tool contains no reproduction of rules text and is intended solely as a points calculation aid for personal use.
            </p>
          </footer>
        </MantineProvider>
      </body>
    </html>
  );
}
