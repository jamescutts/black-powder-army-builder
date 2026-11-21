import Link from "next/link";
import { SiteDisclaimer } from "./SiteDisclaimer";
import { InstallApp } from "./InstallApp";
import { KOFI_URL } from "@/lib/meta";

/** The Ko-fi appeal, as a band of its own above the dark part of the footer */
function Support() {
  return (
    <section className="site-support" aria-label="Support Army Builder">
      <div className="site-inner site-support-inner">
        <div className="site-support-text">
          <div className="site-support-title">
            {/* Phones show the Ko-fi button just below, so the cup would repeat it */}
            <img src="/kofi/kofi-cup.png" alt="" width={32} height={26} aria-hidden className="site-support-cup" />
            <h2>Support Army Builder</h2>
          </div>
          <p>
            Army Builder is free to use. If you&apos;ve found it useful, a tip on Ko-fi simply helps cover the costs of
            keeping the site running.
          </p>
        </div>
        {/* Ko-fi's own button artwork */}
        <a href={KOFI_URL} target="_blank" rel="noopener" className="kofi-button needs-network">
          <img src="/kofi/support-me-on-kofi-beige.png" alt="Support me on Ko-fi" width={245} height={50} />
        </a>
      </div>
    </section>
  );
}

const LINKS = [
  { href: "/", label: "Home" },
  { href: "/black-powder", label: "Black Powder" },
  { href: "/armies", label: "My armies" },
];

/**
 * The disclaimer (on pages that need it), the support band, then a dark band across the full window
 * matching the header, with its content lined up to the page column. Not in the installed app: its
 * home page has an About section instead (AppHome).
 */
export function SiteFooter() {
  return (
    <footer className="site-footer app-hidden">
      <SiteDisclaimer />
      <Support />
      <div className="site-footer-main">
        <div className="site-inner site-footer-grid">
          <div className="site-footer-col">
            <div className="site-brand">
              <span className="site-brand-script">Army Builder</span>
            </div>
            <p className="site-footer-muted">
              Points calculators for tabletop wargame army lists, starting with Black Powder&apos;s horse-and-musket
              supplements.
            </p>
          </div>

          <div className="site-footer-col">
            <p className="site-footer-heading">Explore</p>
            {LINKS.map((l) => (
              <Link key={l.href} href={l.href} className="site-footer-link">
                {l.label}
              </Link>
            ))}
            <InstallApp className="site-footer-link site-footer-button" />
          </div>

          <div className="site-footer-col">
            <p className="site-footer-heading">Credits</p>
            <p>
              Built by{" "}
              <a href="https://shakosandsprues.com" target="_blank" rel="noopener" className="site-footer-link">
                Shakos and Sprues
              </a>{" "}
              (James Cutts)
            </p>
            <p className="site-footer-muted">
              Paintings from Wikimedia Commons, all public domain. Prussian flag by{" "}
              <a
                href="https://commons.wikimedia.org/wiki/File:Flag_of_the_Kingdom_of_Prussia_(1803-1892).svg"
                target="_blank"
                rel="noreferrer"
                className="site-footer-link"
              >
                David Liuzzo
              </a>
              .
            </p>
            <p className="site-footer-muted">
              An unofficial, fan-made tool. <em>Black Powder</em> and its supplements are &copy;{" "}
              <a href="https://www.warlordgames.com" target="_blank" rel="noreferrer" className="site-footer-link">
                Warlord Games
              </a>
              .
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
