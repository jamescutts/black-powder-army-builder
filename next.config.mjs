// One id per build. The service worker (app/sw.js) names its caches after it, so each deploy replaces
// the last one's saved copy of the site, and the page uses it to tell whether the worker matches it.
const buildVersion = Date.now().toString(36);

/** @type {import('next').NextConfig} */
const nextConfig = {
  env: { NEXT_PUBLIC_BUILD_VERSION: buildVersion },
};

export default nextConfig;
