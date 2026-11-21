"use client";

import Link from "next/link";
import { Anchor, Badge, Card, Container, Group, SimpleGrid, Stack, Text, Title } from "@mantine/core";
import { IconBook2 } from "@tabler/icons-react";
import { getNation, getSupplement } from "@/data";
import { battlesIn, campaigns } from "@/data/battles";
import type { HistoricalForce } from "@/data/types";
import { forceHref, rosterFromForce } from "@/lib/forces";
import { nationForPeriod } from "@/lib/periods";
import { rosterTotal, unitCount } from "@/lib/points";
import { validateRoster } from "@/lib/validate";

const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;

/**
 * Prebuilt historical forces at the game's divisional scale: a heading for each campaign, its battles
 * in the order they were fought, and each battle's forces grouped by side, as cards like My armies'.
 * Opening one starts a new list from it, to change as you like.
 */
export function HistoricalForces() {
  return (
    <Container size="xl" py="lg">
      <Stack gap="xl">
        <Stack gap={6}>
          <Title order={1} className="army-title">
            Historical forces
          </Title>
          <Text size="md" c="brown.9" maw={720} style={{ lineHeight: 1.55 }}>
            Divisions as they fought, from real orders of battle, ready to play. Open one and it becomes a list of
            your own to change as you like. Where history broke the army list&apos;s rules, the builder shows it as a
            historical departure rather than a mistake.
          </Text>
        </Stack>

        {campaigns.map((campaign) => {
          const battles = battlesIn(campaign.id);
          if (battles.length === 0) return null;
          return (
            <section key={campaign.id} id={campaign.id} className="campaign-section">
              <Stack gap="xl">
                <Stack gap={6} className="campaign-head">
                  <Title order={2} className="campaign-title">
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
                          <Title order={3} className="builder-heading">
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
