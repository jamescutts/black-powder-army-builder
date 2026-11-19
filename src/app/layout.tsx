import "@mantine/core/styles.css";
import "./globals.css";

import type { Metadata, Viewport } from "next";
import { ColorSchemeScript, MantineProvider, mantineHtmlProps } from "@mantine/core";
import { bodyFont, headingFont, scriptFont } from "./fonts";
import { theme } from "@/theme";
import { SITE_DESCRIPTION, SITE_NAME, SITE_URL, pageMeta } from "@/lib/meta";
import { SiteHeader } from "@/components/SiteHeader";
import { SiteFooter } from "@/components/SiteFooter";

// Site-wide defaults; each page adds its own title, description and address (see pageMeta). No canonical
// address or sharing URL here, or pages without their own (like the old /builder redirects) would claim
// to be the home page.
const { alternates: _alternates, openGraph: siteOpenGraph, ...siteMeta } = pageMeta({
  description: SITE_DESCRIPTION,
  path: "/",
});
export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  ...siteMeta,
  title: { default: SITE_NAME, template: `%s | ${SITE_NAME}` },
  applicationName: SITE_NAME,
  openGraph: { ...siteOpenGraph, url: undefined },
};

// Browser chrome on phones matches the header band
export const viewport: Viewport = {
  themeColor: "#33200f",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      {...mantineHtmlProps}
      className={`${bodyFont.variable} ${headingFont.variable} ${scriptFont.variable}`}
    >
      <head>
        <ColorSchemeScript defaultColorScheme="light" forceColorScheme="light" />
      </head>
      <body>
        <MantineProvider theme={theme} defaultColorScheme="light" forceColorScheme="light">
          {/* Column layout keeps the footer at the bottom of short pages */}
          <div className="site-shell">
            <SiteHeader />
            <main className="site-main">{children}</main>
            <SiteFooter />
          </div>
        </MantineProvider>
      </body>
    </html>
  );
}
