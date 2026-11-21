"use client";

import type { ReactNode } from "react";
import { usePathname } from "next/navigation";

/**
 * The footer element itself. The installed app shows it only on the home page: elsewhere it's in the
 * way of the builder and lists, and the header already gets you around.
 */
export function SiteFooterShell({ children }: { children: ReactNode }) {
  const home = usePathname() === "/";
  return <footer className={home ? "site-footer" : "site-footer app-hidden"}>{children}</footer>;
}
