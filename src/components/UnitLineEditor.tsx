"use client";

import { useState, type ReactNode } from "react";
import { ActionIcon, Badge, Button, Chip, Group, Select, Stack, Text, Tooltip, UnstyledButton } from "@mantine/core";
import { IconLock, IconPlus, IconTrash } from "@tabler/icons-react";
import type { BrigadeType, Nation, UnitEntry } from "@/data/types";
import type { RosterBrigadeInstance, RosterUnitLine } from "@/types/army";
import { defaultVariantLabel, unitCost } from "@/lib/units";
import { newKey } from "@/lib/id";
import { InlineName } from "@/components/InlineName";
import { limitBadge } from "@/lib/limitBadge";
import { optionDelta, optionsForUnit, resolveLine, signedPoints, toggleLineOption, unitOptionBlocked } from "@/lib/options";

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
  /**
   * The brigade the slot belongs to, so each unit can take that brigade's upgrades and downgrades.
   * Without it (the army command slot) units are shown without options.
   */
  brigade?: { nation: Nation; bt: BrigadeType; instance: RosterBrigadeInstance; regimentOptions?: string[] };
  /** Marks the slot as one group within a regiment, with a bar of its own down its left side */
  grouped?: boolean;
  /** Anything more to show under a unit's name, e.g. which brigade an army battery is attached to */
  extraInfo?: (line: RosterUnitLine) => ReactNode;
  /**
   * Why one more of a unit can't be added here right now (a per-unit, army-wide or ratio limit), or
   * null if it can. Units it names stay in the picker, greyed out with the reason.
   */
  unitBlocked?: (unitId: string) => string | null;
  /** Why nothing can be added to the slot yet (e.g. it needs 6 battalions first), or null */
  lockedReason?: string | null;
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
  brigade,
  grouped,
  extraInfo,
  unitBlocked,
  lockedReason,
}: Props) {
  const [pickedUnitId, setPickedUnitId] = useState<string | null>(eligibleUnits[0]?.id ?? null);
  const [pickedVariant, setPickedVariant] = useState<string | undefined>(
    eligibleUnits[0] ? defaultVariantLabel(eligibleUnits[0]) : undefined
  );
  const blockedReason = (id: string) => unitBlocked?.(id) ?? null;
  // A picked unit that's since become unavailable gives way to the first one that isn't
  const firstAvailable = eligibleUnits.find((u) => !blockedReason(u.id));
  const chosen = eligibleUnits.find((u) => u.id === pickedUnitId);
  const pickedUnit = chosen && !blockedReason(chosen.id) ? chosen : firstAvailable;
  // The option picked for it (weapon, battery size), or its first when the fallback unit is showing
  const variant =
    pickedUnit && pickedUnit.id === pickedUnitId ? pickedVariant : pickedUnit ? defaultVariantLabel(pickedUnit) : undefined;

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

  // Every unit gets a line of its own, so each can take its own upgrades
  function handleAdd() {
    if (!pickedUnit) return;
    onChange([...lines, { key: newKey("line"), unitId: pickedUnit.id, variantLabel: variant, qty: 1 }]);
  }

  // Swapping the army commander for another (a Divisional Commander for Marshal Davout, say)
  function handleSwapUnit(key: string, unitId: string) {
    const u = eligibleUnits.find((x) => x.id === unitId);
    if (!u) return;
    onChange(lines.map((l) => (l.key === key ? { ...l, unitId, variantLabel: defaultVariantLabel(u), options: undefined } : l)));
  }

  function handleRename(key: string, name: string | undefined) {
    onChange(lines.map((l) => (l.key === key ? { ...l, name } : l)));
  }

  function handleVariant(key: string, variantLabel: string) {
    onChange(lines.map((l) => (l.key === key ? { ...l, variantLabel } : l)));
  }

  function handleRemove(key: string) {
    onChange(lines.filter((l) => l.key !== key));
  }

  function handleToggleOption(key: string, optionId: string) {
    if (!brigade) return;
    onChange(lines.map((l) => (l.key === key ? toggleLineOption(brigade.bt, l, optionId) : l)));
  }

  return (
    <Stack gap={6} className={grouped ? "slot-group" : undefined}>
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
        <Stack gap={0} className="unit-rows">
          {lines.map((line) => {
            const unit = eligibleUnits.find((u) => u.id === line.unitId);
            if (!unit) return null;
            const resolved = brigade
              ? resolveLine(brigade.nation, line, { bt: brigade.bt, regimentOptions: brigade.regimentOptions })
              : null;
            const cost = (resolved?.cost ?? unitCost(unit, line.variantLabel)) * line.qty;
            const special = resolved?.special ?? unit.special ?? [];
            const options = brigade ? optionsForUnit(brigade.bt, unit.id) : [];
            const showVariantInName = line.variantLabel && !(maxTotal !== undefined && (unit.variants?.length ?? 0) > 0);
            const name = resolved?.unit.name ?? unit.name;

            const chips = brigade && options.length > 0 && (
              <Group gap={4} wrap="nowrap" className="unit-row-chips" role="group" aria-label={`${name} upgrades`}>
                {options.map((o) => {
                  const active = !!line.options?.includes(o.id);
                  const blocked = unitOptionBlocked(
                    brigade.nation,
                    brigade.bt,
                    o,
                    line,
                    brigade.instance,
                    brigade.regimentOptions
                  );
                  const delta = signedPoints(optionDelta(brigade.nation, o, unit));
                  const chip = (
                    <Chip
                      size="xs"
                      variant="outline"
                      color="brown"
                      checked={active}
                      disabled={!!blocked}
                      onChange={() => handleToggleOption(line.key, o.id)}
                    >
                      {o.label}
                      {delta && <span className="unit-option-cost"> {delta}</span>}
                    </Chip>
                  );
                  return blocked ? (
                    <Tooltip key={o.id} label={blocked} withArrow multiline maw={240}>
                      {/* A disabled control fires no hover, so the reason hangs on a wrapper */}
                      <span tabIndex={0} className="unit-option-blocked">
                        {chip}
                      </span>
                    </Tooltip>
                  ) : (
                    <span key={o.id}>{chip}</span>
                  );
                })}
              </Group>
            );

            // One line per unit: its name and rules, then its upgrades, points and remove. In a narrow
            // card the upgrades drop to a line of their own under the name.
            const row = (
              <div className={highlightLabel ? "unit-row unit-row-plain" : "unit-row"}>
                <div className="unit-row-info">
                  {maxTotal !== undefined && eligibleUnits.length > 1 ? (
                    // A single-choice slot (the army commander) changes its pick in place
                    <Select
                      size="xs"
                      maw={260}
                      aria-label={highlightLabel ?? "Unit"}
                      data={eligibleUnits.map((u) => ({ value: u.id, label: u.name }))}
                      value={line.unitId}
                      onChange={(v) => v && handleSwapUnit(line.key, v)}
                      allowDeselect={false}
                      searchable
                    />
                  ) : brigade ? (
                    // The unit's own name, typed in place; once it has one, its type follows
                    <Text size="sm" span>
                      <InlineName
                        value={line.name}
                        placeholder={`${name}${showVariantInName ? ` (${line.variantLabel})` : ""}`}
                        onChange={(n) => handleRename(line.key, n)}
                        label={`Name for this ${name}`}
                      />
                      {line.name?.trim() && (
                        <Text span size="xs" c="dimmed" className="unit-row-type">
                          {name}
                          {showVariantInName ? ` (${line.variantLabel})` : ""}
                        </Text>
                      )}
                    </Text>
                  ) : (
                    <Text size="sm" span>
                      {name}
                      {showVariantInName ? ` (${line.variantLabel})` : ""}
                    </Text>
                  )}
                  {special.length > 0 && (
                    <Text size="xs" c="dimmed" fs="italic" span className="unit-row-special">
                      {special.join(" \u2022 ")}
                    </Text>
                  )}
                  {extraInfo?.(line)}
                </div>
                {chips}
                <Group gap={4} wrap="nowrap" className="unit-row-meta">
                  {maxTotal !== undefined && (unit.variants?.length ?? 0) > 0 && (
                    <Select
                      size="xs"
                      w={150}
                      aria-label={`${unit.name} option`}
                      data={unit.variants!.map((v) => ({ value: v.label, label: `${v.label} (${v.cost} pts)` }))}
                      value={line.variantLabel}
                      onChange={(v) => v && handleVariant(line.key, v)}
                      allowDeselect={false}
                    />
                  )}
                  <Text size="xs" c="dimmed" w={48} ta="right">
                    {cost} pts
                  </Text>
                  <ActionIcon
                    color="red"
                    variant="subtle"
                    size="sm"
                    aria-label={`Remove ${name}`}
                    onClick={() => handleRemove(line.key)}
                  >
                    <IconTrash size={14} />
                  </ActionIcon>
                </Group>
              </div>
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

      {/* Adding: a dashed row at the foot of the group, the same "space waiting to be filled" as the
          Add another brigade box, smaller. When nothing can be added yet, the row stays, greyed, and
          says why. */}
      {!atMaxTotal && !isFull && (() => {
        if (lockedReason) {
          return (
            <div className="add-row" data-blocked>
              <IconLock size={13} aria-hidden />
              <span>{lockedReason}</span>
            </div>
          );
        }
        const pickedRules =
          pickedUnit?.special?.length && !lines.some((l) => l.unitId === pickedUnit.id)
            ? pickedUnit.special.join(" \u2022 ")
            : null;

        // One kind of unit with no options to choose: the whole row is the button
        if (onlyUnit && !(onlyUnit.variants?.length ?? 0)) {
          return pickedUnit ? (
            <UnstyledButton className="add-row" onClick={handleAdd}>
              <IconPlus size={14} aria-hidden />
              <span className="add-unit-label">Add {onlyUnit.name}</span>
              {pickedRules && <span className="add-row-rules">{pickedRules}</span>}
            </UnstyledButton>
          ) : (
            <div className="add-row" data-blocked>
              <IconPlus size={14} aria-hidden />
              <span className="add-unit-label">Add {onlyUnit.name}</span>
              <span className="add-row-reason">{blockedReason(onlyUnit.id)}</span>
            </div>
          );
        }

        return (
          <div className="add-row add-row-picker">
            <Group gap={6} wrap="nowrap" style={{ flex: 1, minWidth: 0 }}>
              {onlyUnit ? (
                <>
                  <Text size="xs" fw={600} className="add-unit-label">
                    {onlyUnit.name}
                  </Text>
                  <Select
                    size="xs"
                    w={170}
                    aria-label={`${onlyUnit.name} option`}
                    data={onlyUnit.variants!.map((v) => ({ value: v.label, label: `${v.label} (${v.cost} pts)` }))}
                    value={variant}
                    onChange={(v) => v && setPickedVariant(v)}
                    allowDeselect={false}
                  />
                </>
              ) : (
                <>
                  <Select
                    size="xs"
                    style={{ flex: 1, minWidth: 0 }}
                    placeholder="Choose unit"
                    aria-label={label ? `${label}: unit` : "Unit"}
                    data={eligibleUnits.map((u) => {
                      const why = blockedReason(u.id);
                      return { value: u.id, label: why ? `${u.name} (${why})` : u.name, disabled: !!why };
                    })}
                    value={pickedUnit?.id ?? null}
                    onChange={handlePickUnit}
                    searchable
                    allowDeselect={false}
                  />
                  {pickedUnit && (pickedUnit.variants?.length ?? 0) > 0 && (
                    <Select
                      size="xs"
                      w={150}
                      aria-label={`${pickedUnit.name} option`}
                      data={pickedUnit.variants!.map((v) => ({ value: v.label, label: `${v.label} (${v.cost} pts)` }))}
                      value={variant}
                      onChange={(v) => {
                        if (!v) return;
                        // Choosing an option for the fallback unit makes it the picked one
                        setPickedUnitId(pickedUnit.id);
                        setPickedVariant(v);
                      }}
                      allowDeselect={false}
                    />
                  )}
                </>
              )}
              <Button size="xs" variant="light" leftSection={<IconPlus size={14} />} onClick={handleAdd} disabled={!pickedUnit}>
                Add
              </Button>
            </Group>
            {!pickedUnit ? (
              <span className="add-row-reason add-row-below">
                {onlyUnit ? blockedReason(onlyUnit.id) : "Nothing more can be added here right now"}
              </span>
            ) : (
              pickedRules && <span className="add-row-rules add-row-below">{pickedRules}</span>
            )}
          </div>
        );
      })()}
    </Stack>
  );
}
