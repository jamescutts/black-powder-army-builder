"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { SiteSearch } from "./SiteSearch";

const NAV = [
  { href: "/", label: "Home" },
  { href: "/black-powder", label: "Black Powder" },
];

/**
 * A dark ink band across the top: the site name (the same on every page, in the script face), tagline and
 * search, then the main menu below, which shows where you are.
 */
export function SiteHeader() {
  const pathname = usePathname();
  const isActive = (href: string) => (href === "/" ? pathname === "/" : pathname.startsWith(href));

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
        </nav>
      </div>
    </header>
  );
}
