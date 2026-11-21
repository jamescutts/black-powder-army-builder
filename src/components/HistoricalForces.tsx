"use client";

import Link from "next/link";
import { Anchor, Badge, Breadcrumbs, Card, Container, Group, SimpleGrid, Stack, Text, Title } from "@mantine/core";
import { IconBook2, IconChevronLeft } from "@tabler/icons-react";
import { getNation, getSupplement } from "@/data";
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

/** The way back up from a campaign or battle page: a back link in the app, breadcrumbs in the browser */
function Crumbs({ trail, here }: { trail: { href: string; label: string }[]; here: string }) {
  const up = trail[trail.length - 1];
  return (
    <>
      <Anchor component={Link} href={up.href} size="sm" c="brown.7" className="army-back app-only">
        <IconChevronLeft size={18} aria-hidden />
        {up.label}
      </Anchor>
      <Breadcrumbs separator="›" className="army-crumbs app-hidden">
        <Anchor component={Link} href="/black-powder" size="sm" c="brown.7">
          Black Powder
        </Anchor>
        {trail.map((t) => (
          <Anchor key={t.href} component={Link} href={t.href} size="sm" c="brown.7">
            {t.label}
          </Anchor>
        ))}
        <Text size="sm" c="brown.9">
          {here}
        </Text>
      </Breadcrumbs>
    </>
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
  return (
    <Container size="xl" py="lg">
      <Stack gap="xl">
        <Stack gap={6}>
          <Crumbs trail={[{ href: HISTORICAL_FORCES_PATH, label: "Historical forces" }]} here={campaign.name} />
          <Title order={1} className="army-title">
            {campaign.name}
          </Title>
          <Text size="sm" fw={600} c="brown.8">
            {campaign.dates}
          </Text>
          <Text size="md" c="brown.9" maw={760} style={{ lineHeight: 1.55 }}>
            {campaign.summary}
          </Text>
        </Stack>

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
            const sides = [...new Set(battle.forces.map((f) => f.side))].map(
              (side) => `${plural(battle.forces.filter((f) => f.side === side).length, side, side)}`
            );
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
                  <Text size="xs" c="brown.8">
                    {sides.join(" · ")}
                  </Text>
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
  return (
    <Container size="xl" py="lg">
      <Stack gap="xl">
        <Stack gap={6}>
          <Crumbs
            trail={[
              { href: HISTORICAL_FORCES_PATH, label: "Historical forces" },
              { href: campaignHref(campaign.id), label: campaign.name },
            ]}
            here={battle.name}
          />
          {battle.art && <BattleArt art={battle.art} />}
          <Title order={1} className="army-title">
            {battle.name}
          </Title>
          <Text size="sm" fw={600} c="brown.8">
            {battle.date} · {campaign.name}
          </Text>
          <Text size="md" c="brown.9" maw={760} style={{ lineHeight: 1.55 }}>
            {battle.summary}
          </Text>
        </Stack>
        {sides.map((side) => (
          <Stack gap="xs" key={side}>
            <Text size="xs" tt="uppercase" fw={700} c="brown.8" lts={0.6}>
              {side}
            </Text>
            <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="md">
              {battle.forces
                .filter((f) => f.side === side)
                .map((force) => (
                  <ForceCard key={force.id} force={force} />
                ))}
            </SimpleGrid>
          </Stack>
        ))}
      </Stack>
    </Container>
  );
}

/** A battle's painting as a banner at the head of its section, credited and linked to its Commons page */
function BattleArt({ art }: { art: HistoricalArt }) {
  return (
    <figure className="battle-art">
      <img src={art.src} alt={`${art.title}, ${art.artist}`} loading="lazy" style={{ objectPosition: art.focus }} />
      <figcaption>
        <Anchor href={art.page} target="_blank" rel="noreferrer" inherit c="inherit">
          <i>{art.title}</i>, {art.artist}
          {art.date && `, ${art.date}`}
        </Anchor>
      </figcaption>
    </figure>
  );
}

function ForceCard({ force }: { force: HistoricalForce }) {
  const base = getNation(force.nationId)!;
  const supplement = getSupplement(base.supplementId);
  const nation = nationForPeriod(base, force.period);
  const { roster } = rosterFromForce(nation, force);
  const departures = validateRoster(nation, roster).filter((i) => i.level === "historical").length;
  const flag = base.flagFile ?? base.flagFiles?.[0];

  return (
    <Card withBorder radius="md" padding="md" className="picker-card saved-list-card">
      <Group gap="sm" wrap="nowrap" align="flex-start">
        {flag && (
          <span className="army-flag saved-list-flag">
            <img src={flag} alt="" />
          </span>
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
