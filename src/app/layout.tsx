import "@mantine/core/styles.css";
import "./globals.css";

import type { Metadata } from "next";
import { ColorSchemeScript, MantineProvider } from "@mantine/core";
import { bodyFont, headingFont, scriptFont } from "./fonts";
import { theme } from "@/theme";

export const metadata: Metadata = {
  title: "Army Builder",
  description: "Points calculators for tabletop wargame army lists.",
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
        </MantineProvider>
      </body>
    </html>
  );
}
