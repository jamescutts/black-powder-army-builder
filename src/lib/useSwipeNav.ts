"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";

/** The main menu's pages, in its order, that a swipe moves between */
const SECTIONS = ["/", "/black-powder", "/black-powder/historical-forces", "/armies"];

// A swipe: mostly sideways, far enough and quick enough to mean it, rather than a slow drag or a scroll
const MIN_DISTANCE = 70;
const MAX_TIME_MS = 600;
// Touches starting this close to the screen's sides are the phone's own back and forward gestures
const EDGE = 24;

/**
 * Which menu page this is: Home, the Black Powder pages (its book pages too, but not the army builder,
 * whose page is for building), Historical forces (its campaign pages too), or My armies. Null elsewhere,
 * where swiping does nothing.
 */
function sectionOf(pathname: string): number | null {
  if (pathname === "/") return 0;
  if (pathname === "/armies") return 3;
  const parts = pathname.split("/").filter(Boolean);
  if (parts[0] === "black-powder" && parts[1] === "historical-forces") return 2;
  if (parts[0] === "black-powder" && parts.length <= 2 && parts[1] !== "builder") return 1;
  return null;
}

/** Whether a touch begins on something that takes sideways movement or text itself */
function ownsSwipe(target: EventTarget | null): boolean {
  if (!(target instanceof Element)) return true;
  if (target.closest("input, textarea, select, [contenteditable], [role='dialog'], [data-no-swipe]")) return true;
  // Anything that scrolls sideways (the app's army tiles, a wide table) keeps its own swipes
  for (let el: Element | null = target; el && el !== document.body; el = el.parentElement) {
    if (el.scrollWidth > el.clientWidth + 1) {
      const overflow = getComputedStyle(el).overflowX;
      if (overflow === "auto" || overflow === "scroll") return true;
    }
  }
  return false;
}

/**
 * On touch screens, swiping left or right moves to the next or previous page of the main menu (Home,
 * Black Powder, My armies), as a phone's tabs do. Not in the army builder, nor from anything that
 * scrolls sideways, a text field or a pop-up, nor from the screen's edges.
 */
export function useSwipeNav() {
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    const section = sectionOf(pathname);
    if (section === null) return;

    let start: { x: number; y: number; t: number } | null = null;

    const onStart = (e: TouchEvent) => {
      const touch = e.touches[0];
      start = null;
      if (e.touches.length !== 1 || !touch) return;
      if (touch.clientX < EDGE || touch.clientX > window.innerWidth - EDGE) return;
      if (ownsSwipe(e.target)) return;
      start = { x: touch.clientX, y: touch.clientY, t: e.timeStamp };
    };

    const onEnd = (e: TouchEvent) => {
      const touch = e.changedTouches[0];
      if (!start || !touch) return;
      const dx = touch.clientX - start.x;
      const dy = touch.clientY - start.y;
      const quick = e.timeStamp - start.t < MAX_TIME_MS;
      start = null;
      if (!quick || Math.abs(dx) < MIN_DISTANCE || Math.abs(dx) < Math.abs(dy) * 2) return;
      if (window.getSelection()?.toString()) return;
      // Finger moving left brings in the next page, as with tabs
      const next = section + (dx < 0 ? 1 : -1);
      if (next < 0 || next >= SECTIONS.length) return;
      router.push(SECTIONS[next]);
    };

    window.addEventListener("touchstart", onStart, { passive: true });
    window.addEventListener("touchend", onEnd, { passive: true });
    return () => {
      window.removeEventListener("touchstart", onStart);
      window.removeEventListener("touchend", onEnd);
    };
  }, [pathname, router]);
}
