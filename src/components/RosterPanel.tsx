"use client";

import { Alert, Badge, Divider, Group, List, Paper, ScrollArea, Stack, Text } from "@mantine/core";
import { IconAlertTriangle, IconCircleCheck } from "@tabler/icons-react";
import type { Nation, UnitEntry } from "@/data/types";
import type { RosterState, RosterUnitLine } from "@/types/army";
import { unitCost } from "@/lib/units";
import { validateRoster } from "@/lib/validate";
import { RosterViewModal } from "@/components/RosterViewModal";

interface Props {
  nation: Nation;
  roster: RosterState;
}

function lineTotal(nation: Nation, line: RosterUnitLine): number {
  const unit = nation.units.find((u) => u.id === line.unitId);
  if (!unit) return 0;
  return unitCost(unit, line.variantLabel) * line.qty;
}

function getStaffRating(unit: UnitEntry, variantLabel?: string): number | undefined {
  // Named commanders have a fixed staffRating on the unit itself
  if (unit.staffRating !== undefined) return unit.staffRating;
  // Generic commanders have staffRating on the selected variant
  if (variantLabel && unit.variants) {
    const variant = unit.variants.find((v) => v.label === variantLabel);
    if (variant?.staffRating !== undefined) return variant.staffRating;
  }
  return undefined;
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
        const sr = unit.category === "Command" ? getStaffRating(unit, line.variantLabel) : undefined;
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
              {sr !== undefined ? ` (Staff Rating ${sr})` : ""}
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
    const flatSlotCost = instance.slotLines.flat().reduce((s, l) => s + lineTotal(nation, l), 0);
    const regimentCost = (instance.regimentSlots ?? []).reduce((sum, regSlot) => {
      if (!regSlot) return sum;
      return sum + regSlot.reduce((rSum, reg) =>
        rSum + reg.slotLines.flat().reduce((lSum, l) => lSum + lineTotal(nation, l), 0), 0);
    }, 0);
    const total = commanderCost + flatSlotCost + regimentCost;
    return { instance, bt, total };
  });

  const grandTotal =
    commandTotal + brigadeTotals.reduce((s, b) => s + b.total, 0);

  const issues = validateRoster(nation, roster);

  return (
    <Stack gap="md">
      <Paper withBorder p="md" radius="md">
        <Group justify="space-between" align="flex-start" wrap="nowrap" mb="sm">
          <Group gap="sm" align="center" wrap="nowrap" style={{ minWidth: 0 }}>
            {(nation.flagFile ?? nation.flagFiles?.[0]) && (
              <div style={{
                position: "relative",
                width: 54,
                height: 36,
                borderRadius: 3,
                border: "1px solid var(--mantine-color-gray-3)",
                overflow: "hidden",
                flexShrink: 0,
              }}>
                <img
                  src={nation.flagFile ?? nation.flagFiles?.[0]}
                  alt={`${nation.name} flag`}
                  style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }}
                />
                <div style={{
                  position: "absolute",
                  inset: 0,
                  background: [
                    "radial-gradient(ellipse at center, transparent 40%, rgba(60,30,5,0.35) 100%)",
                    "linear-gradient(135deg, rgba(180,130,60,0.18) 0%, rgba(120,70,20,0.22) 100%)",
                  ].join(", "),
                  mixBlendMode: "multiply",
                  pointerEvents: "none",
                }} />
              </div>
            )}
            <Stack gap={0} style={{ minWidth: 0 }}>
              <Text fw={700} size="lg">
                Roster
              </Text>
              <Text size="xs" c="dimmed">
                {nation.name}
              </Text>
            </Stack>
          </Group>
          <Badge size="xl" variant="filled" color="brown" style={{ flexShrink: 0 }}>
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
                <LineList nation={nation} lines={roster.commandItems} commander />
              </div>
            )}

            {brigadeTotals.map(({ instance, bt, total }) => {
              const flatLines = instance.slotLines.flat();
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
                  {/* Regiment slots */}
                  {bt.slots.map((slot, slotIdx) => {
                    if (!slot.regiment) return null;
                    const regiments = instance.regimentSlots?.[slotIdx] ?? [];
                    if (regiments.length === 0) return null;
                    return regiments.map((reg, regIdx) => {
                      const regLines = reg.slotLines.flat();
                      if (regLines.length === 0) return null;
                      return (
                        <div key={reg.key} style={{ marginLeft: 8 }}>
                          <Text size="xs" fw={600} c="dimmed">
                            {slot.regiment!.label} #{regIdx + 1}
                          </Text>
                          <LineList nation={nation} lines={regLines} />
                        </div>
                      );
                    });
                  })}
                  {/* Flat slot lines */}
                  {flatLines.length > 0 && (
                    <LineList nation={nation} lines={flatLines} />
                  )}
                  {flatLines.length === 0 && (instance.regimentSlots ?? []).every((r) => !r || r.length === 0) && (
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

      <RosterViewModal nation={nation} roster={roster} />

      {issues.length === 0 ? (
        <Alert color="green" variant="light" icon={<IconCircleCheck />}>
          Roster meets every brigade&apos;s minimum/maximum requirement.
        </Alert>
      ) : (
        <Alert color="red" variant="filled" icon={<IconAlertTriangle />} title="Roster issues">
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
