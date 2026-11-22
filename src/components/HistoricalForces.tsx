"use client";

import Link from "next/link";
import { useState } from "react";
import { Anchor, Badge, Breadcrumbs, Card, Container, Group, SimpleGrid, Stack, Text, Title } from "@mantine/core";
import { IconBook2, IconChevronLeft } from "@tabler/icons-react";
import { getNation, getSupplement } from "@/data";
import { CampaignMap, hasCampaignMap, routesAt } from "./CampaignMap";
import { battlePlaces, campaignMaps } from "@/data/battles/geo";
import { battlesIn, campaigns, getCampaign, isPlanned, scheduleIn } from "@/data/battles";
import type { HistoricalArt, HistoricalForce } from "@/data/types";
import { battleHref, campaignHref, forceHref, HISTORICAL_FORCES_PATH, rosterFromForce } from "@/lib/forces";
import { nationForPeriod } from "@/lib/periods";
import { rosterTotal, unitCount } from "@/lib/points";
import { validateRoster } from "@/lib/validate";

const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;

/**
 * Historical forces: prebuilt divisions at the game's scale, from real orders of battle. This page lists
 * the campaigns, each a card like My armies' that opens the campaign's own page.
 */
export function HistoricalCampaigns() {
  return (
    <Container size="xl" py="lg">
      <Stack gap="xl">
        <Stack gap={6}>
          <Title order={1} className="army-title">
            Historical forces
          </Title>
          <Text size="md" c="brown.9" maw={720} style={{ lineHeight: 1.55 }}>
            Divisions as they fought, from real orders of battle, ready to play. Choose a campaign, then open a force
            and it becomes a list of your own to change as you like. Where history broke the army list&apos;s rules,
            the builder shows it as a historical departure rather than a mistake.
          </Text>
        </Stack>

        <SimpleGrid cols={{ base: 1, md: 2 }} spacing="md">
          {campaigns.map((campaign) => {
            const battles = battlesIn(campaign.id);
            const toCome = scheduleIn(campaign.id).length - battles.length;
            // A campaign with no battles listed yet: its card, without a link, saying so
            if (battles.length === 0 && toCome === 0) {
              return (
                <Card key={campaign.id} withBorder radius="md" padding={0} className="home-card campaign-soon">
                  <div className="home-card-photo" data-empty={!campaign.art || undefined}>
                    {campaign.art && (
                      <img
                        src={campaign.art.src}
                        alt={`${campaign.art.title}, ${campaign.art.artist}`}
                        loading="lazy"
                        style={{ objectPosition: campaign.art.focus }}
                      />
                    )}
                  </div>
                  <Stack gap={6} p="lg" pb={0}>
                    <Text ff="heading" fw={600} fz={24} lh={1.2} c="brown.8">
                      {campaign.name}
                    </Text>
                    <Text size="sm" fw={600} c="brown.8">
                      {campaign.dates}
                    </Text>
                    <Text size="sm" c="brown.9" style={{ lineHeight: 1.55 }}>
                      {campaign.summary}
                    </Text>
                  </Stack>
                  <Group justify="flex-end" p="lg" style={{ marginTop: "auto" }}>
                    <Badge color="gray" variant="light" size="lg">
                      Coming soon
                    </Badge>
                  </Group>
                </Card>
              );
            }
            const forces = battles.reduce((n, b) => n + b.forces.length, 0);
            return (
              <Card key={campaign.id} withBorder radius="md" padding={0} className="picker-card home-card saved-list-card">
                {/* A painting across the top, as the book cards on the home page have */}
                <div className="home-card-photo" data-empty={!campaign.art || undefined}>
                  {campaign.art && (
                    <img
                        src={campaign.art.src}
                        alt={`${campaign.art.title}, ${campaign.art.artist}`}
                        loading="lazy"
                        style={{ objectPosition: campaign.art.focus }}
                      />
                  )}
                </div>
                <Stack gap={6} p="lg" pb={0}>
                  {/* The card's link: it covers the whole card (see .saved-list-link) */}
                  <Link href={campaignHref(campaign.id)} className="saved-list-link">
                    <Text ff="heading" fw={600} fz={24} lh={1.2} c="brown.8">
                      {campaign.name}
                    </Text>
                  </Link>
                  <Text size="sm" fw={600} c="brown.8">
                    {campaign.dates}
                  </Text>
                  <Text size="sm" c="brown.9" style={{ lineHeight: 1.55 }}>
                    {campaign.summary}
                  </Text>
                </Stack>
                <Group justify="space-between" align="center" gap="xs" p="lg" style={{ marginTop: "auto" }}>
                  <Text size="sm" c="brown.9">
                    {battles.map((b) => b.name).join(" · ")}
                    {toCome > 0 && (
                      <Text span size="sm" c="brown.8">
                        {battles.length > 0 ? ` · ${toCome} more to come` : plural(toCome, "battle to come", "battles to come")}
                      </Text>
                    )}
                  </Text>
                  {forces > 0 ? (
                    <Badge color="brown" variant="filled" size="lg">
                      {plural(forces, "force", "forces")}
                    </Badge>
                  ) : (
                    <Badge color="gray" variant="light" size="lg">
                      Coming soon
                    </Badge>
                  )}
                </Group>
              </Card>
            );
          })}
        </SimpleGrid>
      </Stack>
    </Container>
  );
}

/**
 * One campaign's page: its battles in the order they were fought, each a card with its painting, date,
 * summary and forces by side, opening the battle's own page.
 */
export function CampaignBattles({ campaignId }: { campaignId: string }) {
  const campaign = getCampaign(campaignId)!;
  // Every battle in order, those still to come among them
  const battles = scheduleIn(campaign.id);
  const fought = battles.filter((b) => !isPlanned(b));
  const forces = fought.reduce((n, b) => n + b.forces.length, 0);
  return (
    <>
      <HistoryHero
        art={campaign.art}
        trail={[{ href: HISTORICAL_FORCES_PATH, label: "Historical forces" }]}
        title={campaign.name}
        dates={campaign.dates}
        summary={campaign.summary}
        stats={[
          { value: fought.length, label: fought.length === 1 ? "battle" : "battles" },
          { value: forces, label: forces === 1 ? "force" : "forces" },
        ]}
      />
    <Container size="xl" py="xl">
      <Stack gap="lg">
        {hasCampaignMap(campaign.id) && (
          <Stack gap="xs" component="section" id="map">
            <Title order={2} className="builder-heading">
              How the armies moved
            </Title>
            <Text size="sm" c="brown.9">
              Click a route to see who marched, or a battle for its summary. Routes are approximate.
            </Text>
            <CampaignMap campaignId={campaign.id} />
          </Stack>
        )}
        <Title order={2} className="builder-heading">
          Battles
        </Title>
        <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="md">
          {battles.map((battle) => {
            // A battle still to come: its card, without a link, saying so
            if (isPlanned(battle)) {
              return (
                <Card key={battle.id} withBorder radius="md" padding={0} className="home-card campaign-soon">
                  {/* No empty picture band here, so a run of battles to come stays compact */}
                  {battle.art && (
                    <div className="home-card-photo">
                      <img
                        src={battle.art.src}
                        alt={`${battle.art.title}, ${battle.art.artist}`}
                        loading="lazy"
                        style={{ objectPosition: battle.art.focus }}
                      />
                    </div>
                  )}
                  <Stack gap={6} p="md" pb={0}>
                    <Text ff="heading" fw={600} fz={22} lh={1.2} c="brown.8">
                      {battle.name}
                    </Text>
                    <Text size="sm" fw={600} c="brown.8">
                      {battle.date}
                    </Text>
                    <Text size="sm" c="brown.9" lineClamp={4} style={{ lineHeight: 1.5 }}>
                      {battle.summary}
                    </Text>
                  </Stack>
                  <Group justify="flex-end" p="md" style={{ marginTop: "auto" }}>
                    <Badge color="gray" variant="light" size="lg">
                      Coming soon
                    </Badge>
                  </Group>
                </Card>
              );
            }
            // Each side with its number of forces and the flag of its first force's army
            const sides = [...new Set(battle.forces.map((f) => f.side))].map((side) => {
              const forces = battle.forces.filter((f) => f.side === side);
              const nation = getNation(forces[0].nationId);
              return { side, label: plural(forces.length, side, side), flag: forces[0].flag ?? nation?.flagFile ?? nation?.flagFiles?.[0] };
            });
            return (
              <Card key={battle.id} withBorder radius="md" padding={0} className="picker-card home-card saved-list-card">
                <div className="home-card-photo" data-empty={!battle.art || undefined}>
                  {battle.art && (
                    <img
                      src={battle.art.src}
                      alt={`${battle.art.title}, ${battle.art.artist}`}
                      loading="lazy"
                      style={{ objectPosition: battle.art.focus }}
                    />
                  )}
                </div>
                <Stack gap={6} p="md" pb={0}>
                  {/* The card's link: it covers the whole card (see .saved-list-link) */}
                  <Link href={battleHref(battle)} className="saved-list-link">
                    <Text ff="heading" fw={600} fz={22} lh={1.2} c="brown.8">
                      {battle.name}
                    </Text>
                  </Link>
                  <Text size="sm" fw={600} c="brown.8">
                    {battle.date}
                  </Text>
                  <Text size="sm" c="brown.9" lineClamp={4} style={{ lineHeight: 1.5 }}>
                    {battle.summary}
                  </Text>
                </Stack>
                <Group justify="space-between" align="center" gap="xs" p="md" style={{ marginTop: "auto" }}>
                  <Group gap={10} wrap="wrap" style={{ minWidth: 0 }}>
                    {sides.map((s) => (
                      <Group key={s.side} gap={5} wrap="nowrap">
                        {s.flag && (
                          <span className="army-flag side-flag" aria-hidden>
                            <img src={s.flag} alt="" />
                          </span>
                        )}
                        <Text size="xs" c="brown.8">
                          {s.label}
                        </Text>
                      </Group>
                    ))}
                  </Group>
                  <Badge color="brown" variant="filled" size="lg">
                    {plural(battle.forces.length, "force", "forces")}
                  </Badge>
                </Group>
              </Card>
            );
          })}
        </SimpleGrid>
      </Stack>
    </Container>
    </>
  );
}

/**
 * One battle's page: its painting, what happened, and its forces grouped by side as cards like My
 * armies'. Opening a force starts a new list from it.
 */
export function BattleForces({ campaignId, battleId }: { campaignId: string; battleId: string }) {
  const campaign = getCampaign(campaignId)!;
  const battle = battlesIn(campaign.id).find((b) => b.id === battleId)!;
  // Sides in the order the battle lists their first force
  const sides = [...new Set(battle.forces.map((f) => f.side))];
  // Each side's forces together: their points, units and brigades
  const totals = Object.fromEntries(
    sides.map((side) => {
      const t = { points: 0, units: 0, brigades: 0 };
      for (const force of battle.forces.filter((f) => f.side === side)) {
        const nation = nationForPeriod(getNation(force.nationId)!, force.period);
        const { roster } = rosterFromForce(nation, force);
        t.points += rosterTotal(nation, roster);
        t.units += unitCount(roster);
        t.brigades += roster.brigadeInstances.length;
      }
      return [side, t];
    })
  );
  return (
    <>
      <HistoryHero
        art={battle.art}
        trail={[
          { href: HISTORICAL_FORCES_PATH, label: "Historical forces" },
          { href: campaignHref(campaign.id), label: campaign.name },
        ]}
        title={battle.name}
        dates={battle.date}
        summary={battle.summary}
        stats={sides.map((side) => {
          const units = totals[side].units;
          return { value: units, label: `${side} ${units === 1 ? "unit" : "units"}` };
        })}
      />
    <Container size="xl" py="xl">
      <Stack gap="lg">
        <Title order={2} className="builder-heading">
          Forces
        </Title>
        {sides.map((side) => (
          <Stack gap="sm" key={side}>
            <SideHead side={side} info={battle.sides?.[side]} totals={totals[side]} />
            <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="md">
              {battle.forces
                .filter((f) => f.side === side)
                .map((force) => (
                  <ForceCard key={force.id} force={force} />
                ))}
            </SimpleGrid>
          </Stack>
        ))}
        <BattleMap campaignId={campaign.id} battleId={battle.id} name={battle.name} />
      </Stack>
    </Container>
    </>
  );
}

/** A battle's place in its campaign, as on Fleet Ledger's battle pages: the campaign's map centred on it,
 * with the marches that led to it and away from it, listed beneath */
function BattleMap({ campaignId, battleId, name }: { campaignId: string; battleId: string; name: string }) {
  if (!hasCampaignMap(campaignId) || !battlePlaces[battleId]) return null;
  const routes = routesAt(campaignId, battleId);
  const sides = new Map(campaignMaps[campaignId].sides.map((s) => [s.id, s]));
  return (
    <Stack gap="xs" component="section" id="map" mt="md">
      <Title order={2} className="builder-heading">
        Where it was fought
      </Title>
      <Text size="sm" c="brown.9">
        {routes.length
          ? `${name} on the campaign's map, with the marches that led to it and away from it. Routes are approximate.`
          : `${name} on the campaign's map. Routes are approximate.`}
      </Text>
      <CampaignMap campaignId={campaignId} focus={battleId} />
      {routes.length > 0 && (
        <ul className="battle-routes">
          {routes.map((r) => {
            const side = sides.get(r.side)!;
            return (
              <li key={r.name}>
                <svg width="26" height="8" aria-hidden="true">
                  <line x1="2" y1="4" x2="24" y2="4" stroke={side.colour} strokeWidth="3" strokeDasharray={side.dash} strokeLinecap="round" />
                </svg>
                <Text size="sm" c="brown.9">
                  <Text span fw={600}>
                    {r.name}
                  </Text>
                  {" · "}
                  <Text span style={{ whiteSpace: "nowrap" }}>
                    {r.dates}
                  </Text>
                </Text>
              </li>
            );
          })}
        </ul>
      )}
    </Stack>
  );
}

/**
 * A campaign's or battle's page head, as Fleet Ledger's: its painting across the full width, shaded from
 * the left, with the way back, title, dates, summary (folded to a few lines, with "Read more") and a row
 * of figures over it, and the painting's credit in the corner. Without a painting, a plain dark band.
 */
function HistoryHero({
  art,
  trail,
  title,
  dates,
  summary,
  stats,
}: {
  art?: HistoricalArt;
  trail: { href: string; label: string }[];
  title: string;
  dates: string;
  summary: string;
  stats: { value: number; label: string }[];
}) {
  const [open, setOpen] = useState(false);
  const up = trail[trail.length - 1];
  return (
    <section className="home-hero history-hero" data-empty={!art || undefined}>
      {art && <img src={art.src} alt="" className="home-hero-image" style={{ objectPosition: art.focus ?? "50% 40%" }} />}
      <div className="home-hero-shade" aria-hidden />
      <Container size="xl" className="home-hero-inner">
        <Stack className="home-hero-body" gap="sm">
          <Anchor component={Link} href={up.href} size="sm" className="history-hero-crumb army-back app-only">
            <IconChevronLeft size={18} aria-hidden />
            {up.label}
          </Anchor>
          <Breadcrumbs separator="›" className="history-hero-crumbs app-hidden">
            <Anchor component={Link} href="/black-powder" size="sm" className="history-hero-crumb">
              Black Powder
            </Anchor>
            {trail.map((t) => (
              <Anchor key={t.href} component={Link} href={t.href} size="sm" className="history-hero-crumb">
                {t.label}
              </Anchor>
            ))}
          </Breadcrumbs>
          <Title order={1} className="home-hero-title history-hero-title">
            {title}
          </Title>
          <Text fw={600} size="sm" className="history-hero-dates">
            {dates}
          </Text>
          <div>
            <Text className="home-hero-lead history-hero-lead" data-open={open || undefined}>
              {summary}
            </Text>
            {summary.length > 240 && (
              <button type="button" className="history-hero-more" onClick={() => setOpen((o) => !o)} aria-expanded={open}>
                {open ? "Show less" : "Read more"}
              </button>
            )}
          </div>
        </Stack>
        <Group className="home-hero-stats history-hero-stats" gap="xl" wrap="wrap">
          {stats.map((s) => (
            <div key={s.label}>
              <Text className="home-hero-stat" ff="heading" fw={600} lh={1}>
                {s.value}
              </Text>
              <Text size="sm" className="home-hero-stat-label">
                {s.label}
              </Text>
            </div>
          ))}
        </Group>
      </Container>
      {art && (
        <Anchor href={art.page} target="_blank" rel="noreferrer" className="home-hero-credit" size="xs">
          {art.title} · {art.artist}
          {art.date && `, ${art.date}`} · public domain
        </Anchor>
      )}
    </section>
  );
}

/** A side's head on a battle page: its commander's portrait and name, and across from them its forces' totals */
function SideHead({
  side,
  info,
  totals,
}: {
  side: string;
  info?: { commander: string; portrait?: HistoricalArt };
  totals: { points: number; units: number; brigades: number };
}) {
  const p = info?.portrait;
  return (
    <Group justify="space-between" align="center" gap="sm" className="side-head">
      <Group gap="sm" wrap="nowrap">
        {p && (
          <a href={p.page} target="_blank" rel="noreferrer" className="side-head-portrait" title={`${p.title}, ${p.artist}${p.date ? `, ${p.date}` : ""}`}>
            <img src={p.src} alt={`${p.title}, ${p.artist}`} loading="lazy" style={{ objectPosition: p.focus ?? "50% 20%" }} />
          </a>
        )}
        <div>
          <Text size="xs" tt="uppercase" fw={700} c="brown.8" lts={0.6}>
            {side}
          </Text>
          {info && (
            <Text ff="heading" fw={600} fz="lg" lh={1.25} c="brown.9">
              {info.commander}
            </Text>
          )}
        </div>
      </Group>
      <Stack gap={4} className="side-head-totals">
        <Text ff="heading" fw={600} fz="xl" lh={1.1} c="brown.9">
          {totals.points.toLocaleString("en-GB")} pts
        </Text>
        <Text size="xs" c="brown.8">
          {plural(totals.units, "unit", "units")} · {plural(totals.brigades, "brigade", "brigades")}
        </Text>
      </Stack>
    </Group>
  );
}

function ForceCard({ force }: { force: HistoricalForce }) {
  const base = getNation(force.nationId)!;
  const supplement = getSupplement(base.supplementId);
  const nation = nationForPeriod(base, force.period);
  const { roster } = rosterFromForce(nation, force);
  const departures = validateRoster(nation, roster).filter((i) => i.level === "historical").length;
  const flag = force.flag ?? base.flagFile ?? base.flagFiles?.[0];

  return (
    <Card withBorder radius="md" padding="md" className="picker-card saved-list-card">
      <Group gap="sm" wrap="nowrap" align="flex-start">
        {/* The force's commander where there's a portrait of him, with the army's flag on its corner; the flag
            alone otherwise */}
        {force.portrait ? (
          <span className="force-portrait" title={`${force.portrait.title}, ${force.portrait.artist}`}>
            <img
              src={force.portrait.src}
              alt={`${force.portrait.title}, ${force.portrait.artist}`}
              loading="lazy"
              style={{ objectPosition: force.portrait.focus ?? "50% 20%" }}
            />
            {flag && (
              <span className="force-portrait-flag">
                <img src={flag} alt="" />
              </span>
            )}
          </span>
        ) : (
          flag && (
            <span className="army-flag saved-list-flag">
              <img src={flag} alt="" />
            </span>
          )
        )}
        <Stack gap={2} style={{ minWidth: 0 }}>
          {/* The card's link: it covers the whole card (see .saved-list-link) */}
          <Link href={forceHref(base.supplementId, force)} className="saved-list-link">
            <Text ff="heading" fw={600} fz="lg" lh={1.25} c="brown.8">
              {force.name}
            </Text>
          </Link>
          {force.formation && (
            <Text size="sm" lh={1.35}>
              {force.formation}
            </Text>
          )}
          <Text size="xs" c="brown.8">
            {base.name}
            {supplement && <> · {supplement.name}</>}
          </Text>
        </Stack>
      </Group>

      <Text size="sm" mt="sm" lineClamp={4} style={{ lineHeight: 1.5 }}>
        {force.summary}
      </Text>

      <Group justify="space-between" align="center" gap="xs" style={{ marginTop: "auto", paddingTop: 12 }}>
        <Text size="xs" c="brown.8">
          {plural(unitCount(roster), "unit", "units")} · {plural(roster.brigadeInstances.length, "brigade", "brigades")}
          {departures > 0 && (
            <>
              {" "}
              · <IconBook2 size={12} aria-hidden style={{ verticalAlign: "-1px" }} />{" "}
              {plural(departures, "departure", "departures")}
            </>
          )}
        </Text>
        <Badge color="brown" variant="filled" size="lg">
          {rosterTotal(nation, roster)} pts
        </Badge>
      </Group>
    </Card>
  );
}
