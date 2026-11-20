import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import staticAssetsIncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/static-assets-incremental-cache";

// The site is fully prerendered and never revalidates, so the Worker serves build-time output (the
// share images especially, which read their fonts from disk and can't be drawn on the Worker) from
// its static assets rather than rendering it again.
const config = defineCloudflareConfig({
  incrementalCache: staticAssetsIncrementalCache,
  enableCacheInterception: true,
});

// `npm run build` runs the OpenNext build (so Cloudflare's default build command
// produces the Worker), and OpenNext runs Next itself through `build:next`.
config.buildCommand = "npm run build:next";

export default config;
