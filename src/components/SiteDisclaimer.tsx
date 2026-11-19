"use client";

import { usePathname } from "next/navigation";

/**
 * A plain-spoken disclaimer, the first row of the footer, shown only on pages that carry Warlord Games' supplements and army list content.
 */
export function SiteDisclaimer() {
  const pathname = usePathname();
  // The home page names the supplements too
  if (pathname !== "/" && !pathname.startsWith("/black-powder")) return null;

  return (
    <section className="site-disclaimer" aria-label="Disclaimer">
      <div className="site-inner">
        <div className="site-disclaimer-row">
          <p className="site-disclaimer-label">Unofficial fan tool</p>
          <p className="site-disclaimer-text">
            This site is not affiliated with, endorsed by, or associated with{" "}
            <a href="https://www.warlordgames.com" target="_blank" rel="noreferrer">
              Warlord Games
            </a>{" "}
            in any way. <em>Black Powder</em>, all supplement titles, army list content and associated intellectual
            property are copyright &copy; Warlord Games. All rights reserved. You will need the relevant books to play;
            this tool only helps you add up points.
          </p>
        </div>
      </div>
    </section>
  );
}
