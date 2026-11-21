"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { IconWifiOff } from "@tabler/icons-react";
import { SiteSearch } from "./SiteSearch";
import { listSaved, LISTS_CHANGED_EVENT } from "@/lib/storage";
import { useSwipeNav } from "@/lib/useSwipeNav";

const NAV = [
  { href: "/", label: "Home" },
  { href: "/black-powder", label: "Black Powder" },
  { href: "/black-powder/battles", label: "Historical forces" },
];

/**
 * A dark ink band across the top: the site name (the same on every page, in the script face), tagline,
 * an Offline pill while there's no connection, and search, then the main menu below, which shows where you are, with My armies at its far end.
 */
export function SiteHeader() {
  const pathname = usePathname();
  // The longest link the address starts with is where you are, so Historical forces isn't also Black Powder
  const current = NAV.filter((i) => (i.href === "/" ? pathname === "/" : pathname.startsWith(i.href))).sort(
    (a, b) => b.href.length - a.href.length
  )[0]?.href;
  const isActive = (href: string) => href === current;
  const savedCount = useSavedCount();
  // On touch screens, swiping sideways moves between these menu pages (lib/useSwipeNav.ts)
  useSwipeNav();

  return (
    <header className="site-header">
      <div className="site-inner">
        <div className="site-header-top">
          <Link href="/" className="site-brand">
            <span className="site-brand-script">Army Builder</span>
          </Link>
          <span className="site-header-muted site-header-tagline">
            Points calculators for tabletop wargame army lists
          </span>
          {/* Only while there's no connection (lib/offline.ts): everything but links to other sites still works */}
          <span className="offline-pill offline-only" role="status">
            <IconWifiOff size={14} aria-hidden />
            Offline<span className="offline-pill-more"> · your armies are saved on this device</span>
          </span>
          <SiteSearch />
        </div>

        <nav aria-label="Main" className="topnav">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="topnav-link"
              data-active={isActive(item.href) || undefined}
              aria-current={pathname === item.href ? "page" : undefined}
            >
              {item.label}
            </Link>
          ))}
          <Link
            href="/armies"
            className="topnav-link topnav-end"
            data-active={pathname === "/armies" || undefined}
            aria-current={pathname === "/armies" ? "page" : undefined}
          >
            My armies
            {savedCount > 0 && (
              <span className="topnav-count" aria-label={`${savedCount} saved`}>
                {savedCount}
              </span>
            )}
          </Link>
        </nav>
      </div>
    </header>
  );
}

/** How many armies are saved in this browser, kept up to date as they're saved and deleted */
function useSavedCount(): number {
  const [count, setCount] = useState(0);
  useEffect(() => {
    const refresh = () => setCount(listSaved().length);
    refresh();
    window.addEventListener(LISTS_CHANGED_EVENT, refresh);
    window.addEventListener("storage", refresh);
    return () => {
      window.removeEventListener(LISTS_CHANGED_EVENT, refresh);
      window.removeEventListener("storage", refresh);
    };
  }, []);
  return count;
}
