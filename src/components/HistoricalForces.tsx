"use client";

import Link from "next/link";
import { Anchor, Badge, Breadcrumbs, Card, Container, Group, SimpleGrid, Stack, Text, Title } from "@mantine/core";
import { IconBook2, IconChevronLeft } from "@tabler/icons-react";
import { getNation, getSupplement } from "@/data";
import { battlesIn, campaigns, getCampaign } from "@/data/battles";
import type { HistoricalForce } from "@/data/types";
import { campaignHref, forceHref, HISTORICAL_FORCES_PATH, rosterFromForce } from "@/lib/forces";
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
            if (battles.length === 0) return null;
            const forces = battles.reduce((n, b) => n + b.forces.length, 0);
            return (
              <Card key={campaign.id} withBorder radius="md" padding="lg" className="picker-card saved-list-card">
                <Stack gap={6}>
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
                <Group justify="space-between" align="center" gap="xs" style={{ marginTop: "auto", paddingTop: 16 }}>
                  <Text size="sm" c="brown.9">
                    {battles.map((b) => b.name).join(" · ")}
                  </Text>
                  <Badge color="brown" variant="filled" size="lg">
                    {plural(forces, "force", "forces")}
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
 * One campaign's page: its battles in the order they were fought, each with its forces grouped by side
 * as cards like My armies'. Opening a force starts a new list from it.
 */
export function CampaignForces({ campaignId }: { campaignId: string }) {
  const campaign = getCampaign(campaignId)!;
  const battles = battlesIn(campaign.id);
  return (
    <Container size="xl" py="lg">
      <Stack gap="xl">
        <Stack gap={6}>
          <Anchor component={Link} href={HISTORICAL_FORCES_PATH} size="sm" c="brown.7" className="army-back app-only">
            <IconChevronLeft size={18} aria-hidden />
            Historical forces
          </Anchor>
          <Breadcrumbs separator="›" className="army-crumbs app-hidden">
            <Anchor component={Link} href="/black-powder" size="sm" c="brown.7">
              Black Powder
            </Anchor>
            <Anchor component={Link} href={HISTORICAL_FORCES_PATH} size="sm" c="brown.7">
              Historical forces
            </Anchor>
            <Text size="sm" c="brown.9">
              {campaign.name}
            </Text>
          </Breadcrumbs>
          <Title order={1} className="army-title">
            {campaign.name}
          </Title>
          <Text size="sm" fw={600} c="brown.8">
            {campaign.dates}
          </Text>
          <Text size="md" c="brown.9" maw={760} style={{ lineHeight: 1.55 }}>
            {campaign.summary}
          </Text>
          {/* The campaign's battles, to jump straight to one */}
          <Group gap="xs" mt={4} component="nav" aria-label={`${campaign.name} battles`}>
            {battles.map((b) => (
              <Anchor key={b.id} href={`#${b.id}`} className="battle-jump">
                {b.name} <span className="battle-jump-date">{b.date}</span>
              </Anchor>
            ))}
          </Group>
        </Stack>

        {battles.map((battle) => {
          // Sides in the order the battle lists their first force
          const sides = [...new Set(battle.forces.map((f) => f.side))];
          return (
            <section key={battle.id} id={battle.id} className="battle-section">
              <Stack gap="md">
                <Stack gap={4}>
                  <Title order={2} className="builder-heading">
                    {battle.name}
                  </Title>
                  <Text size="sm" c="brown.8" fw={600}>
                    {battle.date}
                  </Text>
                  <Text size="sm" c="brown.9" maw={760} style={{ lineHeight: 1.55 }}>
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
            </section>
          );
        })}
      </Stack>
    </Container>
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
