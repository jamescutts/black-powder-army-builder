import type { ReactNode } from "react";

/**
 * One version of a page for the installed app and another for the browser, for pages that differ too
 * much for a class or two (see lib/appMode.ts). Both are sent and drawn; the page's app mark shows one
 * and hides the other from the first frame, so neither flashes up first. Each still runs its effects, so
 * keep anything costly in the app version behind useIsApp().
 */
export function AppSwitch({ app, browser }: { app: ReactNode; browser: ReactNode }) {
  return (
    <>
      <div className="app-only">{app}</div>
      <div className="app-hidden">{browser}</div>
    </>
  );
}
