"use client";

import Link from "next/link";
import { useState } from "react";
import { Anchor, Box, Button, Card, Container, Grid, Group, SimpleGrid, Stack, Text, Title } from "@mantine/core";
import { IconArrowRight, IconDownload } from "@tabler/icons-react";
import { ARTWORK } from "@/data/artwork";
import { useInstallApp } from "@/components/InstallApp";

export interface HomeCounts {
  rulesets: number;
  supplements: number;
  armies: number;
  unitTypes: number;
}

export interface HomeRuleset {
  id: string;
  name: string;
  blurb: string;
  href: string;
  supplements: number;
  armies: number;
}

export interface HomeSupplement {
  id: string;
  name: string;
  blurb: string;
  armies: number;
}

/** An army to link to directly from the home page */
export interface HomeArmy {
  name: string;
  blurb: string;
  supplement: string;
  flags: string[];
  href: string;
}

// Wilhelm Camphausen's Blücher Crossing the Rhine at Kaub (1859), public domain; the 960px one is the fallback
const HERO = {
  large:
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/69/Wilhelm_Camphausen%2C_Bl%C3%BCchers_Rhein%C3%BCbergang_bei_Kaub.jpg/1920px-Wilhelm_Camphausen%2C_Bl%C3%BCchers_Rhein%C3%BCbergang_bei_Kaub.jpg",
  small:
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/69/Wilhelm_Camphausen%2C_Bl%C3%BCchers_Rhein%C3%BCbergang_bei_Kaub.jpg/960px-Wilhelm_Camphausen%2C_Bl%C3%BCchers_Rhein%C3%BCbergang_bei_Kaub.jpg",
  page: "https://commons.wikimedia.org/wiki/File:Wilhelm_Camphausen,_Bl%C3%BCchers_Rhein%C3%BCbergang_bei_Kaub.jpg",
};

const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;

function Hero({ counts }: { counts: HomeCounts }) {
  const [src, setSrc] = useState(HERO.large);
  // Offered beside the main button only where the browser can install the site
  const { mode: installMode, install, help: installHelp } = useInstallApp();

  return (
    <Box component="section" className="home-hero">
      {/* Plain img: the file is served by Wikimedia, not optimised through Next */}
      <img
        src={src}
        alt=""
        className="home-hero-image"
        fetchPriority="high"
        onError={() => src !== HERO.small && setSrc(HERO.small)}
      />
      <div className="home-hero-shade" aria-hidden />

      <Container size="xl" className="home-hero-inner">
        <Stack className="home-hero-body" gap="md">
          <Text className="home-hero-kicker" fw={600} size="sm" tt="uppercase">
            Tabletop wargame army lists
          </Text>
          <Title order={1} className="home-hero-title">
            Build your army lists
            <span className="home-hero-asterisk" aria-hidden>
              *
            </span>
          </Title>
          <Text className="home-hero-lead" size="lg">
            Pick a rule set and an army, then build your list. Army Builder checks it against the book&apos;s limits,
            totals your points as you go, and prints or saves your roster as a PDF.
          </Text>
          <Group gap="sm" mt="xs">
            <Button
              component={Link}
              href="/black-powder"
              size="md"
              className="home-hero-primary"
              rightSection={<IconArrowRight size={18} />}
            >
              {/* While Black Powder is the only rule set; "Choose a rule set" once there's a second */}
              Start a Black Powder army
            </Button>
            {installMode && (
              <Button
                size="md"
                variant="outline"
                className="home-hero-secondary"
                leftSection={<IconDownload size={18} />}
                onClick={install}
              >
                Install the app
              </Button>
            )}
          </Group>
          {installMode && (
            <Text size="sm" className="home-hero-note">
              Installed, it works with no signal, so your armies are there at the club or a show.
            </Text>
          )}
          {installHelp}
        </Stack>

        <Group className="home-hero-stats" gap="xl" wrap="wrap">
          <Stat value={counts.rulesets} label={counts.rulesets === 1 ? "rule set" : "rule sets"} />
          <Stat value={counts.supplements} label={counts.supplements === 1 ? "supplement" : "supplements"} />
          <Stat value={counts.armies} label={counts.armies === 1 ? "army list" : "army lists"} />
          <Stat value={counts.unitTypes} label={counts.unitTypes === 1 ? "unit type" : "unit types"} />
        </Group>
      </Container>

      <Anchor href={HERO.page} target="_blank" rel="noopener" className="home-hero-credit" size="xs">
        Blücher Crossing the Rhine at Kaub, Wilhelm Camphausen · public domain
      </Anchor>
    </Box>
  );
}

function Stat({ value, label }: { value: number; label: string }) {
  return (
    <div>
      <Text className="home-hero-stat" ff="heading" fw={600} lh={1}>
        {value.toLocaleString("en-GB")}
      </Text>
      <Text size="sm" className="home-hero-stat-label">
        {label}
      </Text>
    </div>
  );
}

/** A section running the full window width, its content lined up with the header */
function Band({ tone, children }: { tone?: "tint"; children: React.ReactNode }) {
  return (
    <Box component="section" className="home-band" data-tone={tone}>
      <Container size="xl">{children}</Container>
    </Box>
  );
}

interface Feature {
  count: string;
  title: string;
  body: string;
  points?: string[];
  href: string;
  cta: string;
}

/** A section introducing one part of the site, as on Fleet Ledger: what it is on the left, what you can do on the right, then cards */
function FeatureSection({ f, children }: { f: Feature; children: React.ReactNode }) {
  return (
    <Stack gap="xl">
      <Grid gap="xl" align="flex-end">
        <Grid.Col span={{ base: 12, md: 7 }}>
          <Stack gap={6}>
            <Text size="xs" c="dimmed" fw={600} tt="uppercase">
              {f.count}
            </Text>
            <Title order={2} c="brown.8">
              {f.title}
            </Title>
            <Text style={{ lineHeight: 1.6 }} maw="62ch">
              {f.body}
            </Text>
          </Stack>
        </Grid.Col>
        <Grid.Col span={{ base: 12, md: 5 }}>
          <Group justify={f.points ? "space-between" : "flex-end"} align="flex-end" gap="md">
            {f.points && (
              <Box component="ul" className="home-card-points">
                {f.points.map((p) => (
                  <li key={p}>
                    <Text size="sm" c="dimmed" span>
                      {p}
                    </Text>
                  </li>
                ))}
              </Box>
            )}
            <Button component={Link} href={f.href} color="brown.7" rightSection={<IconArrowRight size={18} />}>
              {f.cta}
            </Button>
          </Group>
        </Grid.Col>
      </Grid>
      {children}
    </Stack>
  );
}

/** A painting across the top of a card, or a plain tinted band where there isn't one yet */
function CardPhoto({ id }: { id: string }) {
  const art = ARTWORK[id];
  return (
    <div className="home-card-photo" data-empty={!art || undefined}>
      {art && <img src={art.src} alt={`${art.title}, ${art.artist}`} loading="lazy" />}
    </div>
  );
}

function RulesetCard({ r }: { r: HomeRuleset }) {
  return (
    <Card component={Link} href={r.href} withBorder radius="md" padding={0} className="picker-card home-card home-card-wide">
      <CardPhoto id={r.id} />
      <Stack gap={6} p="lg" style={{ flex: 1 }} justify="center">
        <Text size="xs" c="dimmed" fw={600}>
          Horse and musket
        </Text>
        <Text ff="heading" fw={600} fz={26} lh={1.2} c="brown.8">
          {r.name}
        </Text>
        <Text style={{ lineHeight: 1.6 }}>{r.blurb}</Text>
        <Text size="sm" c="dimmed" fw={600} mt={4}>
          {plural(r.supplements, "supplement", "supplements")} · {plural(r.armies, "army list", "army lists")}
        </Text>
      </Stack>
    </Card>
  );
}

function SupplementCard({ s }: { s: HomeSupplement }) {
  return (
    <Card component={Link} href={`/black-powder/${s.id}`} withBorder radius="md" padding={0} className="picker-card home-card">
      <CardPhoto id={s.id} />
      <Stack gap={6} p="md" style={{ flex: 1 }}>
        <Text size="xs" c="dimmed" fw={600}>
          {plural(s.armies, "army list", "army lists")}
        </Text>
        <Text ff="heading" fw={600} fz="lg" lh={1.25} c="brown.8">
          {s.name}
        </Text>
        <Text size="sm" c="dimmed" style={{ lineHeight: 1.5 }}>
          {s.blurb}
        </Text>
      </Stack>
    </Card>
  );
}

function ArmyCard({ a }: { a: HomeArmy }) {
  return (
    <Card component={Link} href={a.href} withBorder radius="md" padding={0} className="picker-card home-card">
      <div className="home-card-flags" aria-hidden>
        {a.flags.map((f) => (
          <div key={f} className="home-card-flag">
            <img src={f} alt="" />
          </div>
        ))}
      </div>
      <Stack gap={4} p="md" style={{ flex: 1 }}>
        <Text size="xs" c="dimmed" fw={600}>
          {a.supplement}
        </Text>
        <Text ff="heading" fw={600} fz="md" lh={1.25} c="brown.8">
          {a.name}
        </Text>
        <Text size="sm" c="dimmed" lineClamp={2} style={{ lineHeight: 1.5 }}>
          {a.blurb}
        </Text>
      </Stack>
    </Card>
  );
}

export function HomeView({
  counts,
  rulesets,
  supplements,
  armies,
}: {
  counts: HomeCounts;
  rulesets: HomeRuleset[];
  supplements: HomeSupplement[];
  /** A few armies to link to directly */
  armies: HomeArmy[];
}) {
  const rulesetsFeature: Feature = {
    count: plural(counts.rulesets, "rule set", "rule sets"),
    title: "Pick your rule set",
    body: "Each rule set has its own supplements and army lists. Choose one, then the army you want to field, and build your list unit by unit.",
    points: ["Limits checked as you build", "Points totals and roster issues", "Print or save as PDF"],
    href: "/black-powder",
    cta: "Start a Black Powder army",
  };
  const supplementsFeature: Feature = {
    count: `${plural(counts.supplements, "supplement", "supplements")} · ${plural(counts.armies, "army list", "army lists")}`,
    title: "Black Powder supplements",
    body: "Every army list comes from a Black Powder supplement, with that book's brigade limits, ratios and points caps.",
    href: "/black-powder",
    cta: "Choose an army",
  };

  return (
    <Stack gap={0} className="home-bands">
      <Hero counts={counts} />

      {/* What the asterisk on the hero title points to */}
      <Box component="aside" className="home-wip">
        <Container size="xl">
          <Text size="sm">
            <span className="home-wip-mark" aria-hidden>
              *
            </span>{" "}
            Army Builder is a work in progress. Not every supplement or army list is in yet. Unit upgrades and
            downgrades are in for every official list, though the Peninsular lists&apos; Early, Middle and Late
            periods aren&apos;t enforced, and allied contingents can&apos;t be built yet.
          </Text>
        </Container>
      </Box>

      <Band>
        <FeatureSection f={rulesetsFeature}>
          {rulesets.map((r) => (
            <RulesetCard key={r.id} r={r} />
          ))}
        </FeatureSection>
      </Band>

      <Band tone="tint">
        <FeatureSection f={supplementsFeature}>
          <SimpleGrid cols={{ base: 1, sm: 2, md: 3 }} spacing="md">
            {supplements.map((s) => (
              <SupplementCard key={s.id} s={s} />
            ))}
          </SimpleGrid>
        </FeatureSection>
      </Band>

      {armies.length > 0 && (
        <Band>
          <Stack gap="sm">
            <Group justify="space-between" align="flex-end" gap="sm">
              <Title order={2} size="h3" c="brown.8">
                Or start with a famous army
              </Title>
              <Anchor component={Link} href="/black-powder" size="sm" c="brown.7">
                All armies →
              </Anchor>
            </Group>
            <SimpleGrid cols={{ base: 1, xs: 2, md: 4 }} spacing="md">
              {armies.map((a) => (
                <ArmyCard key={a.href} a={a} />
              ))}
            </SimpleGrid>
          </Stack>
        </Band>
      )}
    </Stack>
  );
}
