"use client";

import { Alert, Badge, Divider, Group, List, Paper, ScrollArea, Stack, Text } from "@mantine/core";
import { IconAlertTriangle, IconCircleCheck } from "@tabler/icons-react";
import type { Nation } from "@/data/types";
import type { RosterState, RosterUnitLine } from "@/types/army";
import { unitCost } from "@/lib/units";
import { validateRoster } from "@/lib/validate";

interface Props {
  nation: Nation;
  roster: RosterState;
}

function lineTotal(nation: Nation, line: RosterUnitLine): number {
  const unit = nation.units.find((u) => u.id === line.unitId);
  if (!unit) return 0;
  return unitCost(unit, line.variantLabel) * line.qty;
}

function LineList({
  nation,
  lines,
  commander = false,
}: {
  nation: Nation;
  lines: RosterUnitLine[];
  commander?: boolean;
}) {
  return (
    <Stack gap={2}>
      {lines.map((line) => {
        const unit = nation.units.find((u) => u.id === line.unitId);
        if (!unit) return null;
        return (
          <Group key={line.key} justify="space-between" wrap="nowrap">
            <Text
              size="xs"
              c={commander ? "brown.6" : undefined}
              fs={commander ? "italic" : undefined}
              style={{ flex: 1, minWidth: 0 }}
              truncate
            >
              {commander ? "★ " : ""}
              {line.qty > 1 ? `${line.qty}× ` : ""}
              {unit.name}
              {line.variantLabel ? ` (${line.variantLabel})` : ""}
            </Text>
            <Text size="xs" c="dimmed">
              {lineTotal(nation, line)}
            </Text>
          </Group>
        );
      })}
    </Stack>
  );
}

export function RosterPanel({ nation, roster }: Props) {
  const commandTotal = roster.commandItems.reduce((s, l) => s + lineTotal(nation, l), 0);

  const brigadeTotals = roster.brigadeInstances.map((instance) => {
    const bt = nation.brigades.find((b) => b.id === instance.brigadeTypeId);
    const commanderCost = instance.commanderLine ? lineTotal(nation, instance.commanderLine) : 0;
    const total =
      commanderCost + instance.slotLines.flat().reduce((s, l) => s + lineTotal(nation, l), 0);
    return { instance, bt, total };
  });

  const grandTotal =
    commandTotal + brigadeTotals.reduce((s, b) => s + b.total, 0);

  const issues = validateRoster(nation, roster);

  return (
    <Stack gap="md">
      <Paper withBorder p="md" radius="md">
        <Group justify="space-between" mb="sm">
          <Text fw={700} size="lg">
            Roster
          </Text>
          <Badge size="xl" variant="filled" color="brown">
            {grandTotal} pts
          </Badge>
        </Group>

        <ScrollArea.Autosize mah={420}>
          <Stack gap="sm">
            {roster.commandItems.length > 0 && (
              <div>
                <Group justify="space-between">
                  <Text size="sm" fw={600}>
                    Command
                  </Text>
                  <Text size="xs" c="dimmed">
                    {commandTotal} pts
                  </Text>
                </Group>
                <LineList nation={nation} lines={roster.commandItems} />
              </div>
            )}

            {brigadeTotals.map(({ instance, bt, total }) => {
              const lines = instance.slotLines.flat();
              if (!bt) return null;
              return (
                <div key={instance.key}>
                  <Group justify="space-between">
                    <Text size="sm" fw={600}>
                      {bt.name}
                    </Text>
                    <Text size="xs" c="dimmed">
                      {total} pts
                    </Text>
                  </Group>
                  {instance.commanderLine && (
                    <LineList nation={nation} lines={[instance.commanderLine]} commander />
                  )}
                  {lines.length > 0 ? (
                    <LineList nation={nation} lines={lines} />
                  ) : (
                    <Text size="xs" c="dimmed" fs="italic">
                      No units yet
                    </Text>
                  )}
                </div>
              );
            })}

            {roster.commandItems.length === 0 && brigadeTotals.length === 0 && (
              <Text c="dimmed" size="sm">
                No units added yet. Start with a Divisional Commander, then add brigades.
              </Text>
            )}
          </Stack>
        </ScrollArea.Autosize>

        <Divider my="sm" />
        <Group justify="space-between">
          <Text size="sm" c="dimmed">
            {roster.brigadeInstances.length} brigade{roster.brigadeInstances.length === 1 ? "" : "s"}
          </Text>
          <Text fw={700}>{grandTotal} pts total</Text>
        </Group>
      </Paper>

      {issues.length === 0 ? (
        <Alert color="green" variant="light" icon={<IconCircleCheck />}>
          Roster meets every brigade&apos;s minimum/maximum requirement.
        </Alert>
      ) : (
        <Alert color="red" variant="light" icon={<IconAlertTriangle />} title="Roster issues">
          <List size="sm" spacing={4}>
            {issues.map((i, idx) => (
              <List.Item key={idx}>{i.message}</List.Item>
            ))}
          </List>
        </Alert>
      )}
    </Stack>
  );
}
