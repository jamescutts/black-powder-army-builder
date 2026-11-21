"use client";

import Link from "next/link";
import dynamic from "next/dynamic";
import { useEffect, useRef, useState } from "react";
import { ActionIcon, Button, Container, Group, Stack, Text, Title } from "@mantine/core";
import { IconArrowUpRight, IconChevronLeft, IconChevronRight, IconInfoCircle, IconPlus, IconTool } from "@tabler/icons-react";
import { HERO, type HomeArmy, type HomeSupplement } from "@/components/HomeView";
import { useIsApp } from "@/lib/useIsApp";
import { KOFI_URL } from "@/lib/meta";
import { DisclaimerText } from "@/components/SiteDisclaimer";

// Your armies need every army list to add up their points, so they're loaded only in the app, never for
// the browser's home page (which draws this page too, hidden: see AppSwitch)
const RecentArmies = dynamic(() => import("@/components/RecentArmies"), { ssr: false });

const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;

/**
 * The installed app's home page: somewhere to carry on or start an army, rather than the browser's
 * introduction to the site (HomeView). A short banner, your armies, the books, every army to start
 * from, then the fan-tool disclaimer, the Ko-fi appeal and About, which stand in for the browser's
 * footer (the app has none).
 */
export function AppHome({ supplements, armies }: { supplements: HomeSupplement[]; armies: HomeArmy[] }) {
  const isApp = useIsApp();
  // The same painting as the browser's home page, so it's the one file either way
  const [src, setSrc] = useState(HERO.large);

  return (
    <Container size="md" className="app-home">
      <Stack gap="xl">
        {/* The banner, with the work-in-progress note joined on beneath it, as the browser's hero has */}
        <section className="app-home-banner">
          <img src={src} alt="" className="app-home-banner-image" onError={() => src !== HERO.small && setSrc(HERO.small)} />
          <div className="app-home-banner-body">
            <Title order={1} className="app-home-title">
              Build your army lists
            </Title>
            <Button
              component={Link}
              href="/black-powder"
              size="sm"
              className="home-hero-primary"
              leftSection={<IconPlus size={16} />}
            >
              New army
            </Button>
          </div>
          <p className="app-home-wip">Army Builder is a work in progress: not every book or army list is in yet.</p>
        </section>

        {isApp && <RecentArmies />}

        <Stack gap="xs" component="section" aria-labelledby="app-home-books">
          <Title order={2} id="app-home-books" className="app-home-heading">
            Black Powder books
          </Title>
          <div className="app-list">
            {supplements.map((s) => (
              <Link key={s.id} href={`/black-powder/${s.id}`} className="app-list-row">
                <span className="app-list-text">
                  <Text ff="heading" fw={600} lh={1.25} c="brown.8">
                    {s.name}
                  </Text>
                  <Text size="xs" c="dimmed">
                    {plural(s.armies, "army list", "army lists")}
                  </Text>
                </span>
                <IconChevronRight size={18} className="app-list-chevron" aria-hidden />
              </Link>
            ))}
          </div>
        </Stack>

        {armies.length > 0 && <AllArmies armies={armies} />}

        {/* The browser's footer, as the app has it: no footer, but the disclaimer where it can't be missed,
            then what an app's About screen would have */}
        <section className="app-fan-card" aria-labelledby="app-home-fan">
          <div className="app-fan-card-head">
            <IconInfoCircle size={20} aria-hidden />
            <h2 id="app-home-fan" className="app-fan-card-label">
              Unofficial fan tool
            </h2>
          </div>
          <p className="app-fan-card-text">
            <DisclaimerText />
          </p>
          {/* Where the books come from, as the support card below leads to Ko-fi */}
          <Button
            component="a"
            href="https://www.warlordgames.com"
            target="_blank"
            rel="noreferrer"
            size="sm"
            mt="sm"
            rightSection={<IconArrowUpRight size={16} />}
            className="app-fan-card-button needs-network"
          >
            Visit Warlord Games
          </Button>
        </section>

        <Stack gap="xs" component="section" aria-labelledby="app-home-about">
          <Title order={2} id="app-home-about" className="app-home-heading">
            About
          </Title>
          {/* The footer's Ko-fi appeal, as a card, with Ko-fi's own button artwork, then who made it */}
          <div className="app-support-card">
            <h3 className="app-support-card-title">Support Army Builder</h3>
            <p className="app-support-card-text">
              Army Builder is free to use. If you&apos;ve found it useful, a tip on Ko-fi simply helps cover the costs
              of keeping the site running.
            </p>
            <a href={KOFI_URL} target="_blank" rel="noopener" className="kofi-button needs-network">
              <img src="/kofi/support-me-on-kofi-beige.png" alt="Support me on Ko-fi" width={245} height={50} />
            </a>
          </div>
          <div className="app-list">
            <a href="https://shakosandsprues.com" target="_blank" rel="noopener" className="app-list-row needs-network">
              <IconTool size={20} className="app-list-icon" aria-hidden />
              <span className="app-list-text">
                <Text fw={600} lh={1.25} c="brown.8">
                  Built by Shakos and Sprues
                </Text>
                <Text size="xs" c="dimmed">
                  James Cutts
                </Text>
              </span>
              <IconArrowUpRight size={18} className="app-list-chevron" aria-hidden />
            </a>
          </div>
        </Stack>
      </Stack>
    </Container>
  );
}

/**
 * Every army as flag tiles, book by book, in two rows that scroll sideways: 2 columns in view on a phone
 * and 4 where there's room, with the next column peeking in to show there are more. No scrollbar: ‹ ›
 * buttons by the heading page through, for a mouse (which can't swipe) and as a plain signpost on a phone.
 */
function AllArmies({ armies }: { armies: HomeArmy[] }) {
  const scroller = useRef<HTMLDivElement>(null);
  // Whether there's more to either side, for the buttons
  const [ends, setEnds] = useState({ start: true, end: false });

  const update = () => {
    const el = scroller.current;
    if (!el) return;
    setEnds({ start: el.scrollLeft <= 1, end: el.scrollLeft + el.clientWidth >= el.scrollWidth - 1 });
  };
  useEffect(() => {
    update();
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);

  // A page at a time, less a column so where you were stays in sight; the tiles' snapping lines it up
  const page = (direction: 1 | -1) => {
    const el = scroller.current;
    if (!el) return;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    el.scrollBy({ left: direction * el.clientWidth * 0.75, behavior: reduce ? "auto" : "smooth" });
  };

  return (
    <Stack gap="xs" component="section" aria-labelledby="app-home-start">
      <Group justify="space-between" align="center" gap="xs">
        <Group gap={8} align="baseline">
          <Title order={2} id="app-home-start" className="app-home-heading">
            All armies
          </Title>
          <Text size="xs" c="dimmed">
            {armies.length}
          </Text>
        </Group>
        <Group gap={6} className="app-army-pager">
          <ActionIcon variant="default" radius="xl" onClick={() => page(-1)} disabled={ends.start} aria-label="Earlier armies">
            <IconChevronLeft size={16} />
          </ActionIcon>
          <ActionIcon variant="default" radius="xl" onClick={() => page(1)} disabled={ends.end} aria-label="More armies">
            <IconChevronRight size={16} />
          </ActionIcon>
        </Group>
      </Group>
      <div className="app-army-scroll" ref={scroller} onScroll={update}>
        {armies.map((a) => {
          const { name, of } = tileName(a.name);
          return (
            <Link key={a.href} href={a.href} className="app-army-tile" title={a.name}>
              <span className="app-army-tile-flags" aria-hidden>
                {a.flags.map((f) => (
                  <span key={f} className="army-flag app-army-tile-flag">
                    <img src={f} alt="" />
                  </span>
                ))}
              </span>
              {/* Two lines at most, so a few long names don't make every row tall. Armies that are parts of
                  one ("The Anglo-Netherlands Army 1815 — Brunswick") lead with their part, which is what tells
                  them apart, over the whole army's name */}
              <Text ff="heading" fw={600} size="sm" lh={1.25} c="brown.8" ta="center" lineClamp={2}>
                {name}
              </Text>
              {of && (
                <Text size="xs" c="dimmed" lh={1.3} ta="center" lineClamp={1} mt={-4}>
                  {of}
                </Text>
              )}
            </Link>
          );
        })}
      </div>
    </Stack>
  );
}

/** An army's name for its tile: "The Anglo-Netherlands Army 1815 — Brunswick" as "Brunswick", of the rest */
function tileName(name: string): { name: string; of?: string } {
  const [whole, part] = name.split(" — ");
  return part ? { name: part, of: whole } : { name };
}
