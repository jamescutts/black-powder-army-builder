import { EB_Garamond, Cinzel, Tangerine } from "next/font/google";

// Body text — a classic old-book serif, close to the supplement's own typesetting.
export const bodyFont = EB_Garamond({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-body",
  display: "swap",
});

// Section headings — an engraved-capitals display serif for that period title-page feel.
export const headingFont = Cinzel({
  subsets: ["latin"],
  weight: ["400", "600", "700", "900"],
  variable: "--font-heading",
  display: "swap",
});

// Decorative flourish, used sparingly (the app title) to echo the book's script logotype.
export const scriptFont = Tangerine({
  subsets: ["latin"],
  weight: ["700"],
  variable: "--font-script",
  display: "swap",
});
