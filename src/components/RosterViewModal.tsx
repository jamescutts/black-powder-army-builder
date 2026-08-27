"use client";

import { Alert, Badge, Button, Divider, Group, List, Modal, Stack, Table, Text, Title } from "@mantine/core";
import { IconAlertTriangle, IconEye, IconPrinter } from "@tabler/icons-react";
import { useDisclosure } from "@mantine/hooks";
import type { Nation, UnitEntry } from "@/data/types";
import type { RosterState, RosterUnitLine } from "@/types/army";
import { unitCost, unitStatLine } from "@/lib/units";
import { getSupplement } from "@/data";
import { validateRoster } from "@/lib/validate";

interface Props {
  nation: Nation;
  roster: RosterState;
}

function getStaffRating(unit: UnitEntry, variantLabel?: string): number | undefined {
  if (unit.staffRating !== undefined) return unit.staffRating;
  if (variantLabel && unit.variants) {
    const variant = unit.variants.find((v) => v.label === variantLabel);
    if (variant?.staffRating !== undefined) return variant.staffRating;
  }
  return undefined;
}

function lineTotal(nation: Nation, line: RosterUnitLine): number {
  const unit = nation.units.find((u) => u.id === line.unitId);
  if (!unit) return 0;
  return unitCost(unit, line.variantLabel) * line.qty;
}

function UnitRow({ nation, line }: { nation: Nation; line: RosterUnitLine }) {
  const unit = nation.units.find((u) => u.id === line.unitId);
  if (!unit) return null;
  const sr = unit.category === "Command" ? getStaffRating(unit, line.variantLabel) : undefined;
  const stats = unitStatLine(unit);
  const cost = lineTotal(nation, line);

  return (
    <Table.Tr>
      <Table.Td>
        <Group gap={6} wrap="nowrap" align="center">
          <span>
            {line.qty > 1 ? `${line.qty}× ` : ""}
            {unit.name}
          </span>
          {sr !== undefined && (
            <Badge size="sm" variant="light" color="brown">Staff Rating {sr}</Badge>
          )}
        </Group>
      </Table.Td>
      <Table.Td>{unit.type}</Table.Td>
      <Table.Td>{stats || "\u2014"}</Table.Td>
      <Table.Td>{unit.special?.join(", ") || "\u2014"}</Table.Td>
      <Table.Td style={{ textAlign: "right" }}>{cost}</Table.Td>
    </Table.Tr>
  );
}

function RosterContent({ nation, roster }: Props) {
  const commandTotal = roster.commandItems.reduce((s, l) => s + lineTotal(nation, l), 0);

  const brigadeTotals = roster.brigadeInstances.map((instance) => {
    const bt = nation.brigades.find((b) => b.id === instance.brigadeTypeId);
    const commanderCost = instance.commanderLine ? lineTotal(nation, instance.commanderLine) : 0;
    const total =
      commanderCost + instance.slotLines.flat().reduce((s, l) => s + lineTotal(nation, l), 0);
    return { instance, bt, total };
  });

  const grandTotal = commandTotal + brigadeTotals.reduce((s, b) => s + b.total, 0);
  const supplement = getSupplement(nation.supplementId);

  return (
    <Stack gap="md">
      <Group justify="space-between" align="center">
        <Group gap="sm" align="center">
          {nation.flagFile && (
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
                src={nation.flagFile}
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
          <Stack gap={0}>
            <Title order={3}>{nation.name}</Title>
            <Text size="sm" c="dimmed">
              {supplement?.name ? `${supplement.name} \u2014 ` : ""}
              {roster.brigadeInstances.length} brigade
              {roster.brigadeInstances.length === 1 ? "" : "s"}
            </Text>
          </Stack>
        </Group>
        <Badge size="xl" variant="filled" color="brown">
          {grandTotal} pts
        </Badge>
      </Group>

      {(() => {
        const issues = validateRoster(nation, roster);
        if (issues.length === 0) return null;
        return (
          <Alert color="red" variant="light" icon={<IconAlertTriangle />} title="Roster issues">
            <List size="sm" spacing={4}>
              {issues.map((issue, idx) => (
                <List.Item key={idx}>{issue.message}</List.Item>
              ))}
            </List>
          </Alert>
        );
      })()}

      {roster.commandItems.length > 0 && (
        <>
          <Title order={4} c="brown.7" mt="sm" style={{ fontFamily: "var(--font-heading), serif" }}>
            Army Command
          </Title>
          <Stack gap="xs">
            {roster.commandItems.map((line) => {
              const unit = nation.units.find((u) => u.id === line.unitId);
              if (!unit) return null;
              const sr = getStaffRating(unit, line.variantLabel);
              const cost = lineTotal(nation, line);
              return (
                <Group gap="sm" align="center" wrap="nowrap" key={line.key}
                  style={{ padding: "8px 12px", border: "1px solid var(--mantine-color-gray-3)", borderRadius: 6 }}
                >
                  {sr !== undefined && (
                    <Group gap={8} align="center" wrap="nowrap" style={{
                      flexShrink: 0,
                      padding: "6px 10px",
                      borderRadius: 6,
                      backgroundColor: "var(--mantine-color-brown-light)",
                    }}>
                      <Stack gap={0}>
                        <Text size="10px" c="dark" fw={600} tt="uppercase" lh={1}>Staff</Text>
                        <Text size="10px" c="dark" fw={600} tt="uppercase" lh={1}>Rating</Text>
                      </Stack>
                      <Text size="xl" fw={700} c="dark" lh={1}>{sr}</Text>
                    </Group>
                  )}
                  <Stack gap={2} style={{ flex: 1, minWidth: 0 }}>
                    <Text fw={600} size="sm">{unit.name}</Text>
                    {unit.special && unit.special.length > 0 && (
                      <Text size="xs" c="dimmed">{unit.special.join(", ")}</Text>
                    )}
                  </Stack>
                  <Text fw={700} size="sm" style={{ whiteSpace: "nowrap", flexShrink: 0 }}>{cost} pts</Text>
                </Group>
              );
            })}
          </Stack>
        </>
      )}

      {brigadeTotals.map(({ instance, bt, total }) => {
        if (!bt) return null;
        const allLines = [
          ...(instance.commanderLine ? [instance.commanderLine] : []),
          ...instance.slotLines.flat(),
        ];
        return (
          <div key={instance.key}>
            <Group justify="space-between" align="baseline" mt="sm">
              <Title order={4} c="brown.7" style={{ fontFamily: "var(--font-heading), serif" }}>
                {bt.name}
              </Title>
              <Text size="sm" c="dimmed">{total} pts</Text>
            </Group>
            <Table verticalSpacing={4} fz="xs" layout="fixed">
              <colgroup>
                <col style={{ width: "22%" }} />
                <col style={{ width: "14%" }} />
                <col style={{ width: "16%" }} />
                <col style={{ width: "40%" }} />
                <col style={{ width: "8%" }} />
              </colgroup>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Unit</Table.Th>
                  <Table.Th>Type</Table.Th>
                  <Table.Th>Stats</Table.Th>
                  <Table.Th>Special</Table.Th>
                  <Table.Th style={{ textAlign: "right" }}>Pts</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {allLines.map((line) => (
                  <UnitRow key={line.key} nation={nation} line={line} />
                ))}
              </Table.Tbody>
            </Table>
          </div>
        );
      })}

      <Divider />
      <Group justify="flex-end">
        <Text fw={700} size="lg">
          Total: {grandTotal} pts
        </Text>
      </Group>

      {nation.notes.length > 0 && (
        <>
          <Title order={4} c="brown.7" mt="sm" style={{ fontFamily: "var(--font-heading), serif" }}>
            Army Notes
          </Title>
          <List size="xs" spacing={4}>
            {nation.notes.map((note, i) => (
              <List.Item key={i}>{note}</List.Item>
            ))}
          </List>
        </>
      )}
    </Stack>
  );
}

export function RosterViewModal({ nation, roster }: Props) {
  const [opened, { open, close }] = useDisclosure(false);

  function handlePrint() {
    // Open the modal first if not already open, then print
    if (!opened) {
      open();
      // Wait for modal to render before printing
      setTimeout(() => window.print(), 300);
    } else {
      window.print();
    }
  }

  return (
    <>
      <Group grow>
        <Button
          color="brown"
          leftSection={<IconEye size={16} />}
          onClick={open}
        >
          View
        </Button>
        <Button
          color="brown"
          leftSection={<IconPrinter size={16} />}
          onClick={handlePrint}
        >
          Print
        </Button>
      </Group>

      <Modal
        opened={opened}
        onClose={close}
        title="Army Roster"
        size="90%"
        centered
      >
        <RosterContent nation={nation} roster={roster} />
      </Modal>
    </>
  );
}
