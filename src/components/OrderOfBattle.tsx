"use client";

import { Anchor, SimpleGrid, Stack, Text, Title } from "@mantine/core";
import type { CSSProperties } from "react";
import { getNation } from "@/data";
import type { ForceBrigade, HistoricalBattle, HistoricalForce } from "@/data/types";

// Each army's colour, edging its side and its forces as Fleet Ledger edges its navies: the campaign maps' colours
// for the main armies, and their own for the contingents that fought among them
const ARMY_COLOURS: [RegExp, string][] = [
  [/imperial-guard/, "#1d3157"],
  [/^(france|french|peninsular-french)/, "#2b4a7e"],
  [/^russia/, "#2f6b3a"],
  [/^prussia/, "#2e2b28"],
  [/^austria/, "#b4561a"],
  [/british|anglo/, "#a3322a"],
  [/^spanish/, "#c4962b"],
  [/^saxony/, "#5b8c3a"],
  [/^italy/, "#3f7a52"],
  [/confederation|wurttemberg|bavaria|westphalia/, "#8a6d1f"],
  [/warsaw|vistula/, "#b0263a"],
  [/^brunswick/, "#3a3a3a"],
  [/dutch|nassau/, "#d06a1e"],
];
const SIDE_COLOURS: [RegExp, string][] = [
  [/French|Polish|Grande/, "#2b4a7e"],
  [/Russian/, "#2f6b3a"],
  [/Prussian/, "#2e2b28"],
  [/Austrian/, "#b4561a"],
  [/British|Anglo/, "#a3322a"],
  [/Spanish/, "#c4962b"],
  [/Saxon/, "#5b8c3a"],
];
const colourOf = (table: [RegExp, string][], key: string) => table.find(([re]) => re.test(key))?.[1] ?? "#6b3d17";
const armyColour = (nationId: string) => colourOf(ARMY_COLOURS, nationId);
const sideColour = (side: string, forces: HistoricalForce[]) =>
  forces[0] ? armyColour(forces[0].nationId) : colourOf(SIDE_COLOURS, side);

/** A unit's name as the force gives it, or its type's name in its list */
function unitName(force: HistoricalForce, unitId: string, name?: string): string {
  if (name) return name;
  return getNation(force.nationId)?.units.find((u) => u.id === unitId)?.name ?? unitId;
}

/** A brigade's units as one line: each regiment as its name (with its battalions when it has more than one),
 *  then its other units (batteries, cavalry) by name */
function brigadeUnits(force: HistoricalForce, b: ForceBrigade): string {
  const parts: string[] = [];
  for (const r of b.regiments ?? []) {
    if (r.units.length === 1) parts.push(unitName(force, r.units[0].unit, r.units[0].name));
    else parts.push(`${r.name} (${r.units.length} bns)`);
  }
  for (const u of b.units ?? []) parts.push(unitName(force, u.unit, u.name));
  return parts.join(", ");
}

/**
 * A battle's order of battle, below its map: each side's forces as they're written here, brigade by
 * brigade with their commanders and units by their historical names, what's left out of them, the forces still
 * to come, and the sources they were built from.
 */
export function OrderOfBattle({ battle }: { battle: HistoricalBattle }) {
  const toCome = battle.toCome ?? [];
  const sides = [...new Set([...battle.forces.map((f) => f.side), ...toCome.map((f) => f.side)])];
  // Columns: the battle's alliances stacked, each with the sides it has here, and every other side on its own
  const allied = (battle.alliances ?? []).map((a) => a.filter((s) => sides.includes(s))).filter((a) => a.length > 0);
  const groups = [
    ...allied,
    ...sides.filter((s) => !allied.some((a) => a.includes(s))).map((s) => [s]),
  ].sort((a, b) => sides.indexOf(a[0]) - sides.indexOf(b[0]));
  return (
    <Stack gap="xs" component="section" id="order-of-battle" mt="md">
      <Title order={2} className="builder-heading">
        Order of battle
      </Title>
      <Text size="sm" c="brown.9">
        The forces above as their orders of battle give them, brigade by brigade, with the sources they were built from.
      </Text>
        <SimpleGrid cols={{ base: 1, md: Math.min(groups.length, 3) }} spacing="xl" className="oob" mt="xs">
          {groups.map((group) => (
            <Stack
              key={group.join("+")}
              gap="lg"
              className="oob-side"
              style={{ "--oob-colour": sideColour(group[0], battle.forces.filter((f) => f.side === group[0])) } as CSSProperties}
            >
              {group.length > 1 && (
                <Text size="sm" tt="uppercase" fw={700} c="brown.9" lts={0.6}>
                  {group.join(" and ")}
                </Text>
              )}
              {group.map((side) => {
            const info = battle.sides?.[side];
            const forces = battle.forces.filter((f) => f.side === side);
            return (
              <Stack key={side} gap="md">
                <Text size="xs" tt="uppercase" fw={700} c="brown.8" lts={0.6}>
                  {side}
                  {info && (
                    <Text span inherit tt="none" fw={600} lts={0}>
                      {" "}
                      · {info.commander}
                    </Text>
                  )}
                </Text>
                {forces.map((f) => (
                    <div key={f.id} className="oob-force" style={{ "--oob-colour": armyColour(f.nationId) } as CSSProperties}>
                      <Text fw={600} c="brown.9" size="sm">
                        {f.name}
                        {f.formation && (
                          <Text span size="sm" fw={400} c="brown.8">
                            {" "}
                            · {f.formation}
                          </Text>
                        )}
                      </Text>
                      {(f.command ?? []).length > 0 && (
                        <Text size="xs" c="brown.8">
                          Commanded by {(f.command ?? []).map((c) => unitName(f, c.unit, c.name)).join(", ")}
                        </Text>
                      )}
                      <ul className="oob-brigades">
                        {f.brigades.map((b, i) => (
                          <li key={i}>
                            <Text span size="sm" fw={600} c="brown.9">
                              {b.name}
                            </Text>
                            {b.commander?.name && (
                              <Text span size="sm" c="brown.8">
                                {" "}
                                ({b.commander.name})
                              </Text>
                            )}
                            <Text span size="sm" c="brown.9">
                              : {brigadeUnits(f, b)}
                            </Text>
                          </li>
                        ))}
                      </ul>
                      {(f.missing ?? []).length > 0 && (
                        <Text size="xs" c="brown.8" fs="italic" pl="md">
                          Not in the force: {(f.missing ?? []).map((m) => m.name).join("; ")}
                        </Text>
                      )}
                    </div>
                  ))}
                {toCome
                  .filter((f) => f.side === side)
                  .map((f) => (
                    <div key={f.name} className="oob-force oob-to-come" style={{ "--oob-colour": colourOf(SIDE_COLOURS, side) } as CSSProperties}>
                      <Text fw={600} c="brown.8" size="sm">
                        {f.name}
                        {f.formation && (
                          <Text span size="sm" fw={400}>
                            {" "}
                            · {f.formation}
                          </Text>
                        )}
                        <Text span size="xs" fs="italic" fw={400}>
                          {" "}
                          (still to come)
                        </Text>
                      </Text>
                      <Text size="sm" c="brown.8" pl="md">
                        {f.summary}
                      </Text>
                    </div>
                  ))}
              </Stack>
            );
          })}
            </Stack>
          ))}
        </SimpleGrid>
        {battle.sources.length > 0 && (
            <div className="oob-sources">
              <Text size="xs" tt="uppercase" fw={700} c="brown.8" lts={0.6}>
                Sources
              </Text>
              <ul>
                {battle.sources.map((s) => (
                  <li key={s.label}>
                    {s.url ? (
                      <Anchor href={s.url} target="_blank" rel="noreferrer" size="sm" c="brown.7">
                        {s.label}
                      </Anchor>
                    ) : (
                      <Text span size="sm">
                        {s.label}
                      </Text>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
    </Stack>
  );
}
