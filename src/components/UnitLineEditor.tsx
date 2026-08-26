"use client";

import { useState } from "react";
import { ActionIcon, Badge, Button, Group, NumberInput, Select, Stack, Text } from "@mantine/core";
import { IconPlus, IconTrash } from "@tabler/icons-react";
import type { UnitEntry } from "@/data/types";
import type { RosterUnitLine } from "@/types/army";
import { defaultVariantLabel, unitCost } from "@/lib/units";
import { newKey } from "@/lib/id";

interface Props {
  eligibleUnits: UnitEntry[];
  lines: RosterUnitLine[];
  onChange: (lines: RosterUnitLine[]) => void;
  label?: string;
  min?: number;
  max?: number;
}

export function UnitLineEditor({ eligibleUnits, lines, onChange, label, min, max }: Props) {
  const [pickedUnitId, setPickedUnitId] = useState<string | null>(eligibleUnits[0]?.id ?? null);
  const pickedUnit = eligibleUnits.find((u) => u.id === pickedUnitId);
  const [pickedVariant, setPickedVariant] = useState<string | undefined>(
    pickedUnit ? defaultVariantLabel(pickedUnit) : undefined
  );

  const total = lines.reduce((s, l) => s + l.qty, 0);
  const hasConstraint = min !== undefined || max !== undefined;
  const inRange = (min === undefined || total >= min) && (max === undefined || total <= max);

  function handlePickUnit(id: string | null) {
    setPickedUnitId(id);
    const u = eligibleUnits.find((x) => x.id === id);
    setPickedVariant(u ? defaultVariantLabel(u) : undefined);
  }

  function handleAdd() {
    if (!pickedUnit) return;
    const existing = lines.find(
      (l) => l.unitId === pickedUnit.id && l.variantLabel === pickedVariant
    );
    if (existing) {
      onChange(
        lines.map((l) => (l.key === existing.key ? { ...l, qty: l.qty + 1 } : l))
      );
    } else {
      onChange([
        ...lines,
        { key: newKey("line"), unitId: pickedUnit.id, variantLabel: pickedVariant, qty: 1 },
      ]);
    }
  }

  function handleQty(key: string, qty: number) {
    if (qty <= 0) {
      onChange(lines.filter((l) => l.key !== key));
      return;
    }
    onChange(lines.map((l) => (l.key === key ? { ...l, qty } : l)));
  }

  function handleRemove(key: string) {
    onChange(lines.filter((l) => l.key !== key));
  }

  return (
    <Stack gap={6}>
      {(label || hasConstraint) && (
        <Group gap="xs">
          {label && (
            <Text size="sm" fw={600}>
              {label}
            </Text>
          )}
          {hasConstraint && (
            <Badge size="sm" color={inRange ? "green" : "red"} variant="light">
              {total}
              {min !== undefined || max !== undefined
                ? ` / ${min ?? 0}${max !== undefined && max !== min ? `-${max}` : ""}`
                : ""}
            </Badge>
          )}
        </Group>
      )}

      {lines.length > 0 && (
        <Stack gap={4}>
          {lines.map((line) => {
            const unit = eligibleUnits.find((u) => u.id === line.unitId);
            if (!unit) return null;
            const cost = unitCost(unit, line.variantLabel);
            return (
              <Group key={line.key} justify="space-between" wrap="nowrap">
                <Text size="sm" style={{ flex: 1, minWidth: 0 }} truncate>
                  {unit.name}
                  {line.variantLabel ? ` (${line.variantLabel})` : ""}
                </Text>
                <Group gap={4} wrap="nowrap">
                  <Text size="xs" c="dimmed" w={56} ta="right">
                    {cost} pts
                  </Text>
                  <NumberInput
                    size="xs"
                    w={60}
                    min={1}
                    max={99}
                    value={line.qty}
                    onChange={(v) => handleQty(line.key, Number(v) || 1)}
                  />
                  <ActionIcon color="red" variant="subtle" size="sm" onClick={() => handleRemove(line.key)}>
                    <IconTrash size={14} />
                  </ActionIcon>
                </Group>
              </Group>
            );
          })}
        </Stack>
      )}

      <Group gap={6} wrap="nowrap">
        <Select
          size="xs"
          style={{ flex: 1 }}
          placeholder="Choose unit"
          data={eligibleUnits.map((u) => ({ value: u.id, label: u.name }))}
          value={pickedUnitId}
          onChange={handlePickUnit}
          searchable
          allowDeselect={false}
        />
        {pickedUnit && (pickedUnit.variants?.length ?? 0) > 0 && (
          <Select
            size="xs"
            w={150}
            data={pickedUnit.variants!.map((v) => ({ value: v.label, label: `${v.label} (${v.cost})` }))}
            value={pickedVariant}
            onChange={(v) => v && setPickedVariant(v)}
            allowDeselect={false}
          />
        )}
        <Button size="xs" leftSection={<IconPlus size={14} />} onClick={handleAdd} disabled={!pickedUnit}>
          Add
        </Button>
      </Group>
    </Stack>
  );
}
