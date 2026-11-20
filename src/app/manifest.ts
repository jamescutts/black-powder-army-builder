import type { MetadataRoute } from "next";
import { SITE_DESCRIPTION, SITE_NAME } from "@/lib/meta";

// Makes the site installable as an app (its own window and launcher icon). The service worker
// (app/sw.js) is what lets it then open without a connection.
export default function manifest(): MetadataRoute.Manifest {
  return {
    id: "/",
    name: SITE_NAME,
    short_name: SITE_NAME,
    description: SITE_DESCRIPTION,
    start_url: "/",
    scope: "/",
    display: "standalone",
    // The splash screen while it opens is the page's parchment; the title bar is the header's dark ink
    background_color: "#e8dec4",
    theme_color: "#33200f",
    lang: "en-GB",
    categories: ["games", "utilities"],
    icons: [
      { src: "/app-icons/icon-192.png", sizes: "192x192", type: "image/png", purpose: "any" },
      { src: "/app-icons/icon-512.png", sizes: "512x512", type: "image/png", purpose: "any" },
      { src: "/app-icons/maskable-192.png", sizes: "192x192", type: "image/png", purpose: "maskable" },
      { src: "/app-icons/maskable-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
    ],
    shortcuts: [{ name: "Black Powder army lists", short_name: "Black Powder", url: "/black-powder" }],
  };
}
