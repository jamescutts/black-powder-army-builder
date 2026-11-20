import type { MetadataRoute } from "next";
import { SITE_DESCRIPTION, SITE_NAME } from "@/lib/meta";
import { ICON_BACKGROUND } from "@/lib/appIcon";

// Lets phones install the site as an app with its own name, icon and window. There's no service worker,
// so the installed app loads the live site each time it opens and always shows the latest version.
export default function manifest(): MetadataRoute.Manifest {
  return {
    id: "/",
    name: SITE_NAME,
    short_name: SITE_NAME,
    description: SITE_DESCRIPTION,
    start_url: "/",
    scope: "/",
    display: "standalone",
    // The parchment page colour behind the splash screen, and the header's brown for the status bar
    background_color: "#e8dec4",
    theme_color: ICON_BACKGROUND,
    icons: [
      { src: "/icons/icon-192.png", sizes: "192x192", type: "image/png", purpose: "any" },
      { src: "/icons/icon-512.png", sizes: "512x512", type: "image/png", purpose: "any" },
      { src: "/icons/maskable-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
    ],
  };
}
