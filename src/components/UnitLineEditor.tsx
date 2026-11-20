"use client";

import { useState } from "react";
import { ActionIcon, Badge, Button, Group, NumberInput, Select, Stack, Text } from "@mantine/core";
import { IconPlus, IconTrash } from "@tabler/icons-react";
import type { UnitEntry } from "@/data/types";
import type { RosterUnitLine } from "@/types/army";
import { defaultVariantLabel, unitCost } from "@/lib/units";
import { newKey } from "@/lib/id";
import { limitBadge } from "@/lib/limitBadge";

interface Props {
  eligibleUnits: UnitEntry[];
  lines: RosterUnitLine[];
  onChange: (lines: RosterUnitLine[]) => void;
  label?: string;
  min?: number;
  max?: number;
  /**
   * Optional callback returning the effective max for the CURRENT contents of this slot.
   * Used for dynamic caps (e.g. regimental artillery "1 per 2 battalions", or Foreign regiment
   * dropping to 1 when Rhinbund is selected). When provided, it overrides the static `max` for
   * the badge display and range check.
   */
  computeMax?: (lines: RosterUnitLine[]) => number | undefined;
  /** Once total qty across all lines reaches this, the picker/add controls are hidden entirely
   * (rather than just disabled) — e.g. capping the free-standing Army Command slot at one commander. */
  maxTotal?: number;
  /** When set (implies maxTotal), the picked line is shown in a highlighted card with this label,
   * matching the Brigade Commander box style, instead of a plain row. */
  highlightLabel?: string;
}

export function UnitLineEditor({
  eligibleUnits,
  lines,
  onChange,
  label,
  min,
  max,
  computeMax,
  maxTotal,
  highlightLabel,
}: Props) {
  const [pickedUnitId, setPickedUnitId] = useState<string | null>(eligibleUnits[0]?.id ?? null);
  const pickedUnit = eligibleUnits.find((u) => u.id === pickedUnitId);
  const [pickedVariant, setPickedVariant] = useState<string | undefined>(
    pickedUnit ? defaultVariantLabel(pickedUnit) : undefined
  );

  const total = lines.reduce((s, l) => s + l.qty, 0);
  const effectiveMaxValue = computeMax ? computeMax(lines) : max;
  const hasConstraint = min !== undefined || effectiveMaxValue !== undefined;
  const atMaxTotal = maxTotal !== undefined && total >= maxTotal;
  // Once the slot is full there's nothing more to add, so the picker goes away
  const isFull = effectiveMaxValue !== undefined && total >= effectiveMaxValue;
  const badge = limitBadge(total, min, effectiveMaxValue);
  // A slot that takes only one kind of unit needs a button, not a one-item dropdown
  const onlyUnit = eligibleUnits.length === 1 ? eligibleUnits[0] : undefined;

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

  function handleVariant(key: string, variantLabel: string) {
    onChange(lines.map((l) => (l.key === key ? { ...l, variantLabel } : l)));
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
            <Badge size="sm" color={badge.color} variant="light" tt="none">
              {badge.label}
            </Badge>
          )}
        </Group>
      )}

      {lines.length > 0 && (
        <Stack gap={8}>
          {lines.map((line) => {
            const unit = eligibleUnits.find((u) => u.id === line.unitId);
            if (!unit) return null;
            const cost = unitCost(unit, line.variantLabel);
            const row = (
              <Stack gap={2}>
                <Group justify="space-between" wrap="nowrap">
                  <Text size="sm" style={{ flex: 1, minWidth: 0 }} truncate>
                    {unit.name}
                    {line.variantLabel && !(maxTotal !== undefined && (unit.variants?.length ?? 0) > 0)
                      ? ` (${line.variantLabel})`
                      : ""}
                  </Text>
                  <Group gap={4} wrap="nowrap">
                    {maxTotal !== undefined ? (
                      (unit.variants?.length ?? 0) > 0 && (
                        <Select
                          size="xs"
                          w={150}
                          data={unit.variants!.map((v) => ({ value: v.label, label: `${v.label} (${v.cost} pts)` }))}
                          value={line.variantLabel}
                          onChange={(v) => v && handleVariant(line.key, v)}
                          allowDeselect={false}
                        />
                      )
                    ) : (
                      <NumberInput
                        size="xs"
                        w={60}
                        min={1}
                        max={99}
                        value={line.qty}
                        onChange={(v) => handleQty(line.key, Number(v) || 1)}
                      />
                    )}
                    <Text size="xs" c="dimmed" w={56} ta="right">
                      {cost} pts
                    </Text>
                    <ActionIcon color="red" variant="subtle" size="sm" onClick={() => handleRemove(line.key)}>
                      <IconTrash size={14} />
                    </ActionIcon>
                  </Group>
                </Group>
                {unit.special && unit.special.length > 0 && (
                  <Text size="xs" c="dimmed" fs="italic" style={{ lineHeight: 1.4 }}>
                    {unit.special.join(" • ")}
                  </Text>
                )}
              </Stack>
            );

            if (!highlightLabel) return <div key={line.key}>{row}</div>;

            return (
              // Labelled like the brigade commanders' rows, without a box of its own inside the card
              <Stack key={line.key} gap={4}>
                <Text size="sm" fw={600}>
                  {highlightLabel}
                </Text>
                {row}
              </Stack>
            );
          })}
        </Stack>
      )}

      {!atMaxTotal && !isFull && (
        <>
          <Group gap={6} wrap="nowrap">
            {onlyUnit ? (
              (onlyUnit.variants?.length ?? 0) > 0 && (
                <Select
                  size="xs"
                  w={170}
                  aria-label={`${onlyUnit.name} option`}
                  data={onlyUnit.variants!.map((v) => ({ value: v.label, label: `${v.label} (${v.cost})` }))}
                  value={pickedVariant}
                  onChange={(v) => v && setPickedVariant(v)}
                  allowDeselect={false}
                />
              )
            ) : (
              <>
                <Select
                  size="xs"
                  style={{ flex: 1 }}
                  placeholder="Choose unit"
                  aria-label={label ? `${label}: unit` : "Unit"}
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
                    aria-label={`${pickedUnit.name} option`}
                    data={pickedUnit.variants!.map((v) => ({ value: v.label, label: `${v.label} (${v.cost})` }))}
                    value={pickedVariant}
                    onChange={(v) => v && setPickedVariant(v)}
                    allowDeselect={false}
                  />
                )}
              </>
            )}
            <Button
              size="xs"
              variant={onlyUnit ? "light" : "filled"}
              leftSection={<IconPlus size={14} />}
              onClick={handleAdd}
              disabled={!pickedUnit}
              style={onlyUnit ? { minWidth: 0 } : undefined}
            >
              {onlyUnit ? <span className="add-unit-label">Add {onlyUnit.name}</span> : "Add"}
            </Button>
          </Group>
          {/* The picked unit's rules, unless they're already shown on a line above */}
          {pickedUnit?.special && pickedUnit.special.length > 0 && !lines.some((l) => l.unitId === pickedUnit.id) && (
            <Text size="xs" c="dimmed" fs="italic" style={{ lineHeight: 1.4 }}>
              {pickedUnit.special.join(" • ")}
            </Text>
          )}
        </>
      )}
    </Stack>
  );
}
