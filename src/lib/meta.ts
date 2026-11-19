import type { Metadata } from "next";

// The site's public address, for full links in sharing previews, the sitemap and robots.txt.
// Override with NEXT_PUBLIC_SITE_URL (e.g. on a preview deployment).
export const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL ?? "https://builder.shakosandsprues.com").replace(/\/$/, "");
export const SITE_NAME = "Army Builder";
export const SITE_DESCRIPTION =
  "Points calculators for tabletop wargame army lists. Build a Black Powder army, check it against the book's limits and print or save your roster.";

/**
 * Metadata for one page: its title (with " | Army Builder" added), description and address, with
 * matching Open Graph and Twitter details. Next replaces openGraph wholesale rather than merging it, so
 * every page sets the whole object here. Sharing images come from the opengraph-image files.
 */
export function pageMeta({ title, description, path }: { title?: string; description: string; path: string }): Metadata {
  const fullTitle = title ? `${title} | ${SITE_NAME}` : SITE_NAME;
  return {
    // The full title, so it doesn't depend on which layout's title template reaches the page
    ...(title ? { title: { absolute: fullTitle } } : {}),
    description,
    alternates: { canonical: path },
    openGraph: {
      type: "website",
      siteName: SITE_NAME,
      locale: "en_GB",
      url: path,
      title: fullTitle,
      description,
    },
    twitter: { card: "summary_large_image", title: fullTitle, description },
  };
}
