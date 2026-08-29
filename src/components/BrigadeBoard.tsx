"use client";

import { useState } from "react";
import {
  ActionIcon,
  Badge,
  Button,
  Group,
  Paper,
  Select,
  Stack,
  Text,
  ThemeIcon,
  Tooltip,
} from "@mantine/core";
import { IconCopy, IconPlus, IconTrash, IconSword } from "@tabler/icons-react";
import type { Nation } from "@/data/types";
import type { RosterBrigadeInstance, RosterRegimentInstance, RosterState } from "@/types/army";
import { UnitLineEditor } from "./UnitLineEditor";
import { defaultVariantLabel, unitCost } from "@/lib/units";
import { newKey } from "@/lib/id";
import { countByType, effectiveMax, effectiveSlotMax } from "@/lib/brigadeLimits";

interface Props {
  nation: Nation;
  roster: RosterState;
  onChange: (roster: RosterState) => void;
}

export function BrigadeBoard({ nation, roster, onChange }: Props) {
  // Army-level commanders only: exclude any Command unit that's tied to a brigade, either as
  // its required commander or as a purchasable option within one of its slots (e.g. a
  // subordinate commander attached to an Infantry Brigade).
  const brigadeScopedCommandIds = new Set<string>();
  for (const b of nation.brigades) {
    if (b.commanderUnitId) brigadeScopedCommandIds.add(b.commanderUnitId);
    for (const slot of b.slots) {
      for (const id of slot.unitIds) brigadeScopedCommandIds.add(id);
      if (slot.regiment) {
        for (const rSlot of slot.regiment.slots) {
          for (const id of rSlot.unitIds) brigadeScopedCommandIds.add(id);
        }
      }
    }
  }
  const commandUnits = nation.units.filter(
    (u) => u.category === "Command" && !brigadeScopedCommandIds.has(u.id)
  );

  // Total army points, used for points-scaled slot maximums (e.g. Earthworks "1 per 500 pts").
  const lineCost = (unitId: string, variantLabel: string | undefined, qty: number) => {
    const unit = nation.units.find((u) => u.id === unitId);
    return unit ? unitCost(unit, variantLabel) * qty : 0;
  };
  const armyTotalPoints =
    roster.commandItems.reduce((s, l) => s + lineCost(l.unitId, l.variantLabel, l.qty), 0) +
    roster.brigadeInstances.reduce((sum, bi) => {
      let t = bi.commanderLine
        ? lineCost(bi.commanderLine.unitId, bi.commanderLine.variantLabel, bi.commanderLine.qty)
        : 0;
      for (const lines of bi.slotLines) for (const l of lines) t += lineCost(l.unitId, l.variantLabel, l.qty);
      for (const regSlot of bi.regimentSlots ?? []) {
        if (!regSlot) continue;
        for (const reg of regSlot) for (const lines of reg.slotLines) for (const l of lines) t += lineCost(l.unitId, l.variantLabel, l.qty);
      }
      return sum + t;
    }, 0);

  const [pickedBrigadeTypeId, setPickedBrigadeTypeId] = useState<string | null>(
    nation.brigades[0]?.id ?? null
  );

  function handleAddBrigade() {
    const bt = nation.brigades.find((b) => b.id === pickedBrigadeTypeId);
    if (!bt) return;
    const commanderUnit = bt.commanderUnitId
      ? nation.units.find((u) => u.id === bt.commanderUnitId)
      : undefined;
    const instance: RosterBrigadeInstance = {
      key: newKey("brigade"),
      brigadeTypeId: bt.id,
      commanderLine: commanderUnit
        ? {
            key: newKey("cmd"),
            unitId: commanderUnit.id,
            variantLabel: defaultVariantLabel(commanderUnit),
            qty: 1,
          }
        : null,
      slotLines: bt.slots.map(() => []),
      regimentSlots: bt.slots.map((slot) => slot.regiment ? [] : null),
    };
    onChange({ ...roster, brigadeInstances: [...roster.brigadeInstances, instance] });
  }

  function handleRemoveBrigade(key: string) {
    onChange({
      ...roster,
      brigadeInstances: roster.brigadeInstances.filter((bi) => bi.key !== key),
    });
  }

  function handleCloneBrigade(key: string) {
    const source = roster.brigadeInstances.find((bi) => bi.key === key);
    if (!source) return;
    const clone: RosterBrigadeInstance = {
      ...source,
      key: newKey("brigade"),
      commanderLine: source.commanderLine
        ? { ...source.commanderLine, key: newKey("cmd") }
        : null,
      slotLines: source.slotLines.map((slot) =>
        slot.map((line) => ({ ...line, key: newKey("unit") }))
      ),
      regimentSlots: source.regimentSlots.map((regSlot) =>
        regSlot
          ? regSlot.map((reg) => ({
              key: newKey("regiment"),
              slotLines: reg.slotLines.map((lines) =>
                lines.map((line) => ({ ...line, key: newKey("unit") }))
              ),
            }))
          : null
      ),
    };
    onChange({ ...roster, brigadeInstances: [...roster.brigadeInstances, clone] });
  }

  function handleCommanderVariant(instanceKey: string, variantLabel: string) {
    onChange({
      ...roster,
      brigadeInstances: roster.brigadeInstances.map((bi) =>
        bi.key === instanceKey && bi.commanderLine
          ? { ...bi, commanderLine: { ...bi.commanderLine, variantLabel } }
          : bi
      ),
    });
  }

  function handleSlotChange(instanceKey: string, slotIndex: number, lines: RosterBrigadeInstance["slotLines"][number]) {
    onChange({
      ...roster,
      brigadeInstances: roster.brigadeInstances.map((bi) => {
        if (bi.key !== instanceKey) return bi;
        const slotLines = bi.slotLines.slice();
        slotLines[slotIndex] = lines;
        return { ...bi, slotLines };
      }),
    });
  }

  function handleRegimentSlotsChange(instanceKey: string, slotIndex: number, regiments: RosterRegimentInstance[]) {
    onChange({
      ...roster,
      brigadeInstances: roster.brigadeInstances.map((bi) => {
        if (bi.key !== instanceKey) return bi;
        const regimentSlots = bi.regimentSlots.slice();
        regimentSlots[slotIndex] = regiments;
        return { ...bi, regimentSlots };
      }),
    });
  }

  function handleAddRegiment(instanceKey: string, slotIndex: number, subSlotCount: number) {
    const bi = roster.brigadeInstances.find((b) => b.key === instanceKey);
    if (!bi) return;
    const current = bi.regimentSlots[slotIndex] ?? [];
    const newReg: RosterRegimentInstance = {
      key: newKey("regiment"),
      slotLines: Array.from({ length: subSlotCount }, () => []),
    };
    handleRegimentSlotsChange(instanceKey, slotIndex, [...current, newReg]);
  }

  function handleRemoveRegiment(instanceKey: string, slotIndex: number, regKey: string) {
    const bi = roster.brigadeInstances.find((b) => b.key === instanceKey);
    if (!bi) return;
    const current = bi.regimentSlots[slotIndex] ?? [];
    handleRegimentSlotsChange(instanceKey, slotIndex, current.filter((r) => r.key !== regKey));
  }

  function handleRegimentSubSlotChange(
    instanceKey: string,
    slotIndex: number,
    regKey: string,
    subSlotIndex: number,
    lines: RosterBrigadeInstance["slotLines"][number]
  ) {
    const bi = roster.brigadeInstances.find((b) => b.key === instanceKey);
    if (!bi) return;
    const current = (bi.regimentSlots[slotIndex] ?? []).map((reg) => {
      if (reg.key !== regKey) return reg;
      const slotLines = reg.slotLines.slice();
      slotLines[subSlotIndex] = lines;
      return { ...reg, slotLines };
    });
    handleRegimentSlotsChange(instanceKey, slotIndex, current);
  }

  return (
    <Stack gap="md">
      <Paper withBorder p="md" radius="md">
        <Text fw={700} mb="xs">
          1. Army Command
        </Text>
        {commandUnits.length > 0 ? (
          <UnitLineEditor
            eligibleUnits={commandUnits}
            lines={roster.commandItems}
            onChange={(lines) => onChange({ ...roster, commandItems: lines })}
            maxTotal={1}
            highlightLabel="Army Commander"
          />
        ) : (
          <Text size="sm" c="dimmed">
            This nation has no standalone army-level command entries — commanders are attached to
            each brigade below.
          </Text>
        )}
      </Paper>

      <Paper withBorder p="md" radius="md">
        <Text fw={700} mb="xs">
          2. Add a Brigade
        </Text>
        <Text size="xs" c="dimmed" mb="sm">
          Pick a brigade type and add it to the army. Each brigade requires its own Brigade
          Commander (added automatically, shown separately below) plus its unit slots filled
          within the shown limits. Repeat to build up the division.
        </Text>
        <Group gap="xs">
          <Select
            style={{ flex: 1 }}
            data={nation.brigades.map((bt) => ({
              value: bt.id,
              label: bt.name,
            }))}
            value={pickedBrigadeTypeId}
            onChange={setPickedBrigadeTypeId}
            searchable
            allowDeselect={false}
          />
          <Button leftSection={<IconPlus size={16} />} onClick={handleAddBrigade}>
            Add Brigade
          </Button>
        </Group>
      </Paper>

      <Text fw={700}>3. Brigades in this army</Text>
      {roster.brigadeInstances.length === 0 && (
        <Text size="sm" c="dimmed">
          No brigades added yet.
        </Text>
      )}
      {roster.brigadeInstances.map((instance) => {
        const bt = nation.brigades.find((b) => b.id === instance.brigadeTypeId);
        if (!bt) return null;
        const sameTypeIndex =
          roster.brigadeInstances.filter((bi) => bi.brigadeTypeId === bt.id).indexOf(instance) + 1;
        const commanderUnit = bt.commanderUnitId
          ? nation.units.find((u) => u.id === bt.commanderUnitId)
          : undefined;
        return (
          <Paper key={instance.key} withBorder p="md" radius="md">
            <Group justify="space-between" mb={bt.note ? 2 : "sm"}>
              <Group gap="xs">
                <Text fw={600}>{bt.name}</Text>
                <Badge size="sm" variant="light">
                  #{sameTypeIndex}
                </Badge>
              </Group>
              <Group gap={4}>
                {effectiveMax(bt, roster.brigadeInstances) > countByType(roster.brigadeInstances, bt.id) && (
                  <Tooltip label="Clone this brigade">
                    <ActionIcon color="brown" variant="subtle" onClick={() => handleCloneBrigade(instance.key)}>
                      <IconCopy size={16} />
                    </ActionIcon>
                  </Tooltip>
                )}
                <Tooltip label="Remove this brigade">
                  <ActionIcon color="red" variant="subtle" onClick={() => handleRemoveBrigade(instance.key)}>
                    <IconTrash size={16} />
                  </ActionIcon>
                </Tooltip>
              </Group>
            </Group>
            {bt.note && (
              <Text size="xs" c="dimmed" mb="sm">
                {bt.note}
              </Text>
            )}

            {commanderUnit && instance.commanderLine && (
              <Paper withBorder p="xs" radius="sm" mb="sm" bg="var(--mantine-color-brown-0)">
                <Group justify="space-between" wrap="nowrap">
                  <Group gap="xs" wrap="nowrap">
                    <ThemeIcon size="sm" variant="light" color="brown">
                      <IconSword size={14} />
                    </ThemeIcon>
                    <Text size="sm" fw={600}>
                      Brigade Commander (required)
                    </Text>
                  </Group>
                  <Group gap={6} wrap="nowrap">
                    {(commanderUnit.variants?.length ?? 0) > 0 ? (
                      <Select
                        size="xs"
                        w={170}
                        data={commanderUnit.variants!.map((v) => ({
                          value: v.label,
                          label: `${v.label} (${v.cost} pts)`,
                        }))}
                        value={instance.commanderLine.variantLabel}
                        onChange={(v) => v && handleCommanderVariant(instance.key, v)}
                        allowDeselect={false}
                      />
                    ) : (
                      <Text size="xs">{commanderUnit.name}</Text>
                    )}
                    <Badge size="sm" variant="filled" color="brown">
                      {unitCost(commanderUnit, instance.commanderLine.variantLabel)} pts
                    </Badge>
                  </Group>
                </Group>
              </Paper>
            )}

            <Stack gap="sm">
              {bt.slots.map((slot, slotIndex) => {
                // Regiment-based slot
                if (slot.regiment) {
                  const regDef = slot.regiment;
                  const regiments = instance.regimentSlots?.[slotIndex] ?? [];
                  return (
                    <Stack key={slotIndex} gap="xs">
                      {/* Regiment header row */}
                      <Group justify="space-between">
                        <Group gap="xs">
                          <Text size="sm" fw={600}>{regDef.label}</Text>
                          <Badge size="sm" variant="light" color={regiments.length >= regDef.min ? "green" : "red"}>
                            {regiments.length} / {regDef.min}-{regDef.max}
                          </Badge>
                        </Group>
                        {regiments.length < regDef.max && (
                          <Button
                            size="compact-xs"
                            variant="light"
                            leftSection={<IconPlus size={12} />}
                            onClick={() => handleAddRegiment(instance.key, slotIndex, regDef.slots.length)}
                          >
                            Add {regDef.label}
                          </Button>
                        )}
                      </Group>

                      {/* Regiment instances */}
                      {regiments.map((reg, regIdx) => (
                        <Paper key={reg.key} withBorder p="sm" radius="sm">
                          <Group justify="space-between" mb="xs">
                            <Text size="sm" fw={500}>{regDef.label} #{regIdx + 1}</Text>
                            <ActionIcon
                              color="red"
                              variant="subtle"
                              size="sm"
                              onClick={() => handleRemoveRegiment(instance.key, slotIndex, reg.key)}
                            >
                              <IconTrash size={14} />
                            </ActionIcon>
                          </Group>
                          <Stack gap="sm">
                            {regDef.slots.map((subSlot, subSlotIdx) => {
                              const eligibleUnits = nation.units.filter((u) => subSlot.unitIds.includes(u.id));
                              const subComputeMax = subSlot.unitLimits
                                ? (subLines: typeof reg.slotLines[number]) => {
                                    const presentIds = [...new Set(subLines.filter((l) => l.qty > 0).map((l) => l.unitId))];
                                    if (presentIds.length === 0) return subSlot.max;
                                    return Math.max(
                                      ...presentIds.map((id) => {
                                        const lim = subSlot.unitLimits!.find((u) => u.unitId === id);
                                        return lim ? lim.max : subSlot.max;
                                      })
                                    );
                                  }
                                : undefined;
                              return (
                                <UnitLineEditor
                                  key={subSlotIdx}
                                  label={subSlot.label}
                                  min={subSlot.min}
                                  max={subSlot.max}
                                  computeMax={subComputeMax}
                                  eligibleUnits={eligibleUnits}
                                  lines={reg.slotLines[subSlotIdx] ?? []}
                                  onChange={(lines) =>
                                    handleRegimentSubSlotChange(instance.key, slotIndex, reg.key, subSlotIdx, lines)
                                  }
                                />
                              );
                            })}
                          </Stack>
                        </Paper>
                      ))}
                    </Stack>
                  );
                }

                // Flat slot (no regiment)
                const eligibleUnits = nation.units.filter((u) => slot.unitIds.includes(u.id));
                const slotMax = slot.maxPerPoints
                  ? Math.floor(armyTotalPoints / slot.maxPerPoints.perPoints)
                  : slot.max;
                const hasDynamicMax = !!(slot.dynamicUnitLimits || slot.unitLimits);
                return (
                  <UnitLineEditor
                    key={slotIndex}
                    label={slot.label}
                    min={slot.min}
                    max={slotMax}
                    computeMax={hasDynamicMax ? (lines) => effectiveSlotMax(slot, lines, instance) : undefined}
                    eligibleUnits={eligibleUnits}
                    lines={instance.slotLines[slotIndex] ?? []}
                    onChange={(lines) => handleSlotChange(instance.key, slotIndex, lines)}
                  />
                );
              })}
            </Stack>
          </Paper>
        );
      })}
    </Stack>
  );
}
