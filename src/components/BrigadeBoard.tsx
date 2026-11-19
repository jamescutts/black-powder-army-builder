"use client";

import { useEffect, useState } from "react";
import {
  ActionIcon,
  Badge,
  Button,
  Group,
  Notification,
  Paper,
  Select,
  Stack,
  Text,
  ThemeIcon,
  Title,
  Tooltip,
} from "@mantine/core";
import { IconCopy, IconPlus, IconTrash, IconSword } from "@tabler/icons-react";
import type { Nation } from "@/data/types";
import type { RosterBrigadeInstance, RosterRegimentInstance, RosterState } from "@/types/army";
import { UnitLineEditor } from "./UnitLineEditor";
import { defaultVariantLabel, unitCost } from "@/lib/units";
import { newKey } from "@/lib/id";
import { countByType, effectiveMax, effectiveSlotMax, requirementLabel, requirementMet } from "@/lib/brigadeLimits";

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
  const brigadePoints = (bi: RosterBrigadeInstance) => {
    let t = bi.commanderLine
      ? lineCost(bi.commanderLine.unitId, bi.commanderLine.variantLabel, bi.commanderLine.qty)
      : 0;
    for (const lines of bi.slotLines) for (const l of lines) t += lineCost(l.unitId, l.variantLabel, l.qty);
    for (const regSlot of bi.regimentSlots ?? []) {
      if (!regSlot) continue;
      for (const reg of regSlot) for (const lines of reg.slotLines) for (const l of lines) t += lineCost(l.unitId, l.variantLabel, l.qty);
    }
    return t;
  };
  const armyTotalPoints =
    roster.commandItems.reduce((s, l) => s + lineCost(l.unitId, l.variantLabel, l.qty), 0) +
    roster.brigadeInstances.reduce((sum, bi) => sum + brigadePoints(bi), 0);

  // Brigade types that can't be added right now (at their limit, or waiting on another brigade type)
  // stay in the picker, greyed out with the reason, so the list still shows everything the army can take.
  const brigadeOptions = nation.brigades.map((bt) => {
    const max = effectiveMax(bt, roster.brigadeInstances);
    const atMax = countByType(roster.brigadeInstances, bt.id) >= max;
    const blocked = !requirementMet(bt, roster.brigadeInstances);
    const ratioCapped = bt.maxRatio && max < bt.max;
    const ratioNames = bt.maxRatio?.brigadeTypeIds
      .map((id) => nation.brigades.find((b) => b.id === id)?.name ?? id)
      .join("/");
    const reason = blocked
      ? requirementLabel(bt, nation.brigades)?.replace(/^Requires/, "needs")
      : atMax
        ? ratioCapped
          ? `1 per ${bt.maxRatio!.ratio} × ${ratioNames}`
          : `limit of ${max} reached`
        : null;
    return { value: bt.id, label: reason ? `${bt.name} (${reason})` : bt.name, disabled: !!reason };
  });

  // After a brigade or regiment is removed, a notice offers to put it back. It re-inserts the removed
  // piece into whatever the roster is by then, so other edits made meanwhile aren't lost.
  const [undo, setUndo] = useState<{ message: string; restore: (r: RosterState) => RosterState } | null>(null);
  useEffect(() => {
    if (!undo) return;
    const t = setTimeout(() => setUndo(null), 8000);
    return () => clearTimeout(t);
  }, [undo]);

  const [pickedBrigadeTypeId, setPickedBrigadeTypeId] = useState<string | null>(
    nation.brigades[0]?.id ?? null
  );

  const pickedIsAvailable = brigadeOptions.some((o) => o.value === pickedBrigadeTypeId && !o.disabled);

  function handleAddBrigade() {
    const bt = nation.brigades.find((b) => b.id === pickedBrigadeTypeId);
    if (!bt || !pickedIsAvailable) return;
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
    const index = roster.brigadeInstances.findIndex((bi) => bi.key === key);
    if (index < 0) return;
    const removed = roster.brigadeInstances[index];
    const name = nation.brigades.find((b) => b.id === removed.brigadeTypeId)?.name ?? "Brigade";
    onChange({
      ...roster,
      brigadeInstances: roster.brigadeInstances.filter((bi) => bi.key !== key),
    });
    setUndo({
      message: `${name} removed`,
      restore: (r) => {
        const brigadeInstances = r.brigadeInstances.slice();
        brigadeInstances.splice(Math.min(index, brigadeInstances.length), 0, removed);
        return { ...r, brigadeInstances };
      },
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

  function handleRemoveRegiment(instanceKey: string, slotIndex: number, regKey: string, label: string) {
    const bi = roster.brigadeInstances.find((b) => b.key === instanceKey);
    if (!bi) return;
    const current = bi.regimentSlots[slotIndex] ?? [];
    const index = current.findIndex((r) => r.key === regKey);
    if (index < 0) return;
    const removed = current[index];
    handleRegimentSlotsChange(instanceKey, slotIndex, current.filter((r) => r.key !== regKey));
    setUndo({
      message: `${label} removed`,
      // Only if its brigade is still there; otherwise there's nothing to put it back into
      restore: (r) => ({
        ...r,
        brigadeInstances: r.brigadeInstances.map((b) => {
          if (b.key !== instanceKey) return b;
          const regimentSlots = b.regimentSlots.slice();
          const regs = (regimentSlots[slotIndex] ?? []).slice();
          regs.splice(Math.min(index, regs.length), 0, removed);
          regimentSlots[slotIndex] = regs;
          return { ...b, regimentSlots };
        }),
      }),
    });
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
    <Stack gap="xl">
      <Stack gap="sm">
        <Title order={2} className="builder-heading">
          Army command
        </Title>
        <Paper withBorder p="md" radius="md">
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
              This army has no separate army commander. Each brigade below comes with its own.
            </Text>
          )}
        </Paper>
      </Stack>

      <Stack gap="sm">
        <Title order={2} className="builder-heading">
          Brigades{" "}
          {roster.brigadeInstances.length > 0 && (
            <Text span c="dimmed" fz="md" ff="body" fw={400}>
              {roster.brigadeInstances.length}
            </Text>
          )}
        </Title>
        {roster.brigadeInstances.map((instance) => {
          const bt = nation.brigades.find((b) => b.id === instance.brigadeTypeId);
          if (!bt) return null;
          const commanderUnit = bt.commanderUnitId
            ? nation.units.find((u) => u.id === bt.commanderUnitId)
            : undefined;
          return (
            <Paper key={instance.key} withBorder p="md" radius="md" className="brigade-card">
              <Group justify="space-between" wrap="nowrap" mb={bt.note ? 2 : "sm"}>
                <Title order={3} className="brigade-card-title">
                  {bt.name}{" "}
                  <Text span c="dimmed" fz="sm" ff="body" fw={400}>
                    {brigadePoints(instance)} pts
                  </Text>
                </Title>
                <Group gap={4}>
                  {effectiveMax(bt, roster.brigadeInstances) > countByType(roster.brigadeInstances, bt.id) && (
                    <Tooltip label="Clone this brigade">
                      <ActionIcon color="brown" variant="subtle" aria-label={`Clone ${bt.name}`} onClick={() => handleCloneBrigade(instance.key)}>
                        <IconCopy size={16} />
                      </ActionIcon>
                    </Tooltip>
                  )}
                  <Tooltip label="Remove this brigade">
                    <ActionIcon color="red" variant="subtle" aria-label={`Remove ${bt.name}`} onClick={() => handleRemoveBrigade(instance.key)}>
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
                                aria-label={`Remove ${regDef.label} ${regIdx + 1}`}
                                onClick={() => handleRemoveRegiment(instance.key, slotIndex, reg.key, regDef.label)}
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

        <Paper p="md" radius="md" className="add-brigade">
          <Text fw={600} mb={4}>
            {roster.brigadeInstances.length === 0 ? "Add your first brigade" : "Add another brigade"}
          </Text>
          <Text size="xs" c="dimmed" mb="sm">
            Each brigade comes with its own commander. Fill its slots within the limits shown.
          </Text>
          <Group gap="xs" wrap="nowrap">
            <Select
              style={{ flex: 1, minWidth: 0 }}
              aria-label="Brigade type"
              data={brigadeOptions}
              value={pickedBrigadeTypeId}
              onChange={setPickedBrigadeTypeId}
              searchable
              allowDeselect={false}
            />
            <Button leftSection={<IconPlus size={16} />} onClick={handleAddBrigade} disabled={!pickedIsAvailable}>
              Add brigade
            </Button>
          </Group>
        </Paper>
      </Stack>

      {undo && (
        <div className="undo-toast" role="status">
          <Notification withBorder withCloseButton onClose={() => setUndo(null)} color="brown">
            <Group justify="space-between" wrap="nowrap" gap="md">
              <Text size="sm">{undo.message}</Text>
              <Button
                size="compact-sm"
                variant="light"
                onClick={() => {
                  onChange(undo.restore(roster));
                  setUndo(null);
                }}
              >
                Undo
              </Button>
            </Group>
          </Notification>
        </div>
      )}
    </Stack>
  );
}
