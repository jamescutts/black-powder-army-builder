"use client";

import { useEffect, useState } from "react";
import {
  ActionIcon,
  Badge,
  Button,
  Chip,
  Collapse,
  Group,
  Notification,
  Paper,
  Select,
  Stack,
  Text,
  TextInput,
  Title,
  Tooltip,
  UnstyledButton,
} from "@mantine/core";
import { IconAlertTriangle, IconChevronDown, IconCopy, IconPencil, IconPlus, IconTrash } from "@tabler/icons-react";
import type { Nation, RegimentDef } from "@/data/types";
import type { RosterBrigadeInstance, RosterRegimentInstance, RosterState } from "@/types/army";
import { UnitLineEditor } from "./UnitLineEditor";
import { defaultVariantLabel, unitCost } from "@/lib/units";
import { brigadeTotal, lineTotal, rosterTotal } from "@/lib/points";
import { regimentBlockedReason, slotLockedReason, unitBlockedInRegimentSlot, unitBlockedInSlot } from "@/lib/availability";
import {
  attachTargets,
  batteriesIn,
  brigadeUnitLines,
  optionsForRegiment,
  regimentOptionBlocked,
  regimentOptionCost,
  resolveLine,
  toggleRegimentOption,
} from "@/lib/options";
import { newKey } from "@/lib/id";
import { limitBadge } from "@/lib/limitBadge";
import { brigadeDisplayName, brigadeIssueText, brigadeLabel, REVEAL_BRIGADE_EVENT, validateRoster } from "@/lib/validate";
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
  const brigadePoints = (bi: RosterBrigadeInstance) => brigadeTotal(nation, bi);
  const armyTotalPoints = rosterTotal(nation, roster);

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

  // Brigades folded down to a one-line summary, so a big army stays easy to scan. Everything starts
  // open, and new brigades are added open.
  const [collapsed, setCollapsed] = useState<Set<string>>(() => new Set());
  const toggleCollapsed = (key: string) =>
    setCollapsed((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  // Each brigade's own problems, shown on its card (the roster panel links here): what breaks the rules
  // in red, and what it still needs calmly, leaving out needs its slot badges already show
  const issuesByBrigade = new Map<string, { errors: string[]; todos: { text: string; onSlot: boolean }[] }>();
  for (const issue of validateRoster(nation, roster)) {
    if (!issue.brigadeKey) continue;
    const bi = roster.brigadeInstances.find((b) => b.key === issue.brigadeKey);
    const name = nation.brigades.find((b) => b.id === bi?.brigadeTypeId)?.name ?? "";
    const entry = issuesByBrigade.get(issue.brigadeKey) ?? { errors: [], todos: [] };
    const text = brigadeIssueText(issue.message, name);
    if (issue.level === "error") entry.errors.push(text);
    else entry.todos.push({ text, onSlot: !!issue.shownOnSlot });
    issuesByBrigade.set(issue.brigadeKey, entry);
  }

  // The roster's "fix this" links open the brigade if it's folded, then bring it into view
  useEffect(() => {
    function reveal(e: Event) {
      const key = (e as CustomEvent<string>).detail;
      setCollapsed((prev) => {
        if (!prev.has(key)) return prev;
        const next = new Set(prev);
        next.delete(key);
        return next;
      });
      requestAnimationFrame(() => {
        const el = document.getElementById(`brigade-${key}`);
        el?.scrollIntoView({ behavior: "smooth", block: "start" });
        el?.focus({ preventScroll: true });
      });
    }
    window.addEventListener(REVEAL_BRIGADE_EVENT, reveal);
    return () => window.removeEventListener(REVEAL_BRIGADE_EVENT, reveal);
  }, []);

  const allCollapsed =
    roster.brigadeInstances.length > 0 && roster.brigadeInstances.every((bi) => collapsed.has(bi.key));

  /**
   * What a folded brigade still shows: its commander, then its units totalled by type across every
   * slot and regiment, e.g. "2 regiments: 6× French Line Infantry · 1× Foot Artillery Section".
   */
  const brigadeSummary = (bi: RosterBrigadeInstance) => {
    const commanderUnit = bi.commanderLine ? nation.units.find((u) => u.id === bi.commanderLine!.unitId) : undefined;
    const commander = commanderUnit
      ? `${commanderUnit.name}${bi.commanderLine!.variantLabel ? ` (${bi.commanderLine!.variantLabel})` : ""}`
      : null;

    const bt = nation.brigades.find((b) => b.id === bi.brigadeTypeId);
    const counts = new Map<string, number>();
    for (const { line: l, regiment } of brigadeUnitLines(bi)) {
      const resolved = resolveLine(nation, l, { bt, regimentOptions: regiment?.options });
      if (!resolved) continue;
      const name = l.variantLabel && resolved.unit === resolved.base ? `${resolved.name} (${l.variantLabel})` : resolved.name;
      counts.set(name, (counts.get(name) ?? 0) + l.qty);
    }
    const units = [...counts].map(([name, qty]) => `${qty}× ${name}`).join(" · ");
    const regiments = (bi.regimentSlots ?? []).reduce((n, r) => n + (r?.length ?? 0), 0);
    const regimentsLabel = regiments > 0 ? `${regiments} regiment${regiments === 1 ? "" : "s"}: ` : "";
    return { commander, units: units ? regimentsLabel + units : "No units yet" };
  };

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

  // The brigade whose name is being edited in its title, if any
  const [renamingKey, setRenamingKey] = useState<string | null>(null);

  function handleRenameBrigade(key: string, name: string) {
    setRenamingKey(null);
    onChange({
      ...roster,
      brigadeInstances: roster.brigadeInstances.map((bi) =>
        bi.key === key ? { ...bi, name: name.trim() || undefined } : bi
      ),
    });
  }

  function handleRemoveBrigade(key: string) {
    const index = roster.brigadeInstances.findIndex((bi) => bi.key === key);
    if (index < 0) return;
    const removed = roster.brigadeInstances[index];
    const name = brigadeLabel(removed, nation.brigades.find((b) => b.id === removed.brigadeTypeId)?.name ?? "Brigade");
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
      // A copy gets the same units but not the same name
      name: undefined,
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
              options: reg.options,
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

  /**
   * The "Attached to" picker under a battery whose brigade attaches its batteries to others (Prussian
   * Army Artillery). Brigades already holding their limit are listed but can't be picked.
   */
  function attachPicker(instance: RosterBrigadeInstance, slotIndex: number, bt: (typeof nation.brigades)[number]) {
    const rule = bt.attachBatteries;
    if (!rule) return undefined;
    const targets = attachTargets(nation, roster.brigadeInstances);
    return function BatteryAttachPicker(line: RosterBrigadeInstance["slotLines"][number][number]) {
      if (!rule.batteryUnitIds.includes(line.unitId)) return null;
      const data = [
        { value: "none", label: "Not attached" },
        ...targets.map((t) => {
          const count = batteriesIn(nation, roster.brigadeInstances, t.key);
          const full = count >= rule.maxPerBrigade && line.attachedTo !== t.key;
          return {
            value: t.key,
            label: `${brigadeDisplayName(nation, roster, t.key)}${full ? ` (has ${count} batteries)` : ""}`,
            disabled: full,
          };
        }),
      ];
      return (
        <Select
          size="xs"
          mt={6}
          maw={280}
          label="Attached to"
          aria-label="Brigade this battery is attached to"
          data={data}
          value={line.attachedTo && targets.some((t) => t.key === line.attachedTo) ? line.attachedTo : "none"}
          onChange={(v) =>
            handleSlotChange(
              instance.key,
              slotIndex,
              (instance.slotLines[slotIndex] ?? []).map((l) =>
                l.key === line.key ? { ...l, attachedTo: v && v !== "none" ? v : undefined } : l
              )
            )
          }
          allowDeselect={false}
          comboboxProps={{ withinPortal: true }}
          classNames={{ label: "attach-label" }}
        />
      );
    };
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

  // A new regiment starts with the battalions it must have (e.g. 1 Musketeer), as an empty one is
  // never legal; more are added, or swapped, from there
  function handleAddRegiment(instanceKey: string, slotIndex: number, regDef: RegimentDef) {
    const bi = roster.brigadeInstances.find((b) => b.key === instanceKey);
    if (!bi) return;
    const current = bi.regimentSlots[slotIndex] ?? [];
    const newReg: RosterRegimentInstance = {
      key: newKey("regiment"),
      slotLines: regDef.slots.map((sub) => {
        const unit = nation.units.find((u) => u.id === sub.unitIds[0]);
        if (!unit || sub.min <= 0) return [];
        return Array.from({ length: sub.min }, () => ({
          key: newKey("line"),
          unitId: unit.id,
          variantLabel: defaultVariantLabel(unit),
          qty: 1,
        }));
      }),
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
        {/* Topped with the brigades' rule, a shade darker as it outranks them. No inline warning here: a
            missing commander is just the starting state, and the roster panel already lists it. */}
        <Paper withBorder p="md" radius="md" className="command-card">
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
        <Group justify="space-between" align="baseline">
          <Title order={2} className="builder-heading">
            Brigades{" "}
            {roster.brigadeInstances.length > 0 && (
              <Text span c="dimmed" fz="md" ff="body" fw={400}>
                {roster.brigadeInstances.length}
              </Text>
            )}
          </Title>
          {roster.brigadeInstances.length > 1 && (
            <Button
              size="compact-sm"
              variant="subtle"
              onClick={() =>
                setCollapsed(allCollapsed ? new Set() : new Set(roster.brigadeInstances.map((bi) => bi.key)))
              }
            >
              {allCollapsed ? "Expand all" : "Collapse all"}
            </Button>
          )}
        </Group>
        {roster.brigadeInstances.map((instance) => {
          const bt = nation.brigades.find((b) => b.id === instance.brigadeTypeId);
          if (!bt) return null;
          const commanderUnit = bt.commanderUnitId
            ? nation.units.find((u) => u.id === bt.commanderUnitId)
            : undefined;
          return (
            <Paper
              key={instance.key}
              withBorder
              p="md"
              radius="md"
              className="brigade-card"
              id={`brigade-${instance.key}`}
              tabIndex={-1}
              data-collapsed={collapsed.has(instance.key) || undefined}
              data-issues={(issuesByBrigade.get(instance.key)?.errors.length ?? 0) > 0 || undefined}
            >
              <Group justify="space-between" wrap="nowrap">
                {renamingKey === instance.key ? (
                  // Renaming: the title becomes a field. Enter or leaving it saves, Escape cancels, and
                  // an empty name goes back to the brigade's type.
                  <TextInput
                    className="brigade-name-input"
                    aria-label={`Name for this ${bt.name}`}
                    placeholder={bt.name}
                    defaultValue={instance.name ?? ""}
                    maxLength={60}
                    autoFocus
                    onFocus={(e) => e.currentTarget.select()}
                    onBlur={(e) => handleRenameBrigade(instance.key, e.currentTarget.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") e.currentTarget.blur();
                      if (e.key === "Escape") setRenamingKey(null);
                    }}
                    description={`${bt.name} · leave empty to use the type`}
                    style={{ flex: 1, minWidth: 0 }}
                  />
                ) : (
                  /* The title is the fold toggle; the heading wraps the button so it stays a heading */
                  <Title order={3} className="brigade-card-title">
                    <UnstyledButton
                      className="brigade-toggle"
                      onClick={() => toggleCollapsed(instance.key)}
                      aria-expanded={!collapsed.has(instance.key)}
                      aria-controls={`brigade-body-${instance.key}`}
                    >
                      <IconChevronDown size={18} className="brigade-chevron" aria-hidden />
                      <span>
                        {brigadeLabel(instance, bt.name)}{" "}
                        <Text span c="dimmed" fz="sm" ff="body" fw={400}>
                          {/* A named brigade still says what type it is */}
                          {instance.name?.trim() ? `${bt.name} · ` : ""}
                          {brigadePoints(instance)} pts
                        </Text>
                      </span>
                    </UnstyledButton>
                  </Title>
                )}
                <Group gap={4} wrap="nowrap">
                  <Tooltip label="Rename this brigade">
                    <ActionIcon
                      color="brown"
                      variant="subtle"
                      aria-label={`Rename ${brigadeLabel(instance, bt.name)}`}
                      onClick={() => setRenamingKey(instance.key)}
                    >
                      <IconPencil size={16} />
                    </ActionIcon>
                  </Tooltip>
                  {effectiveMax(bt, roster.brigadeInstances) > countByType(roster.brigadeInstances, bt.id) && (
                    <Tooltip label="Clone this brigade">
                      <ActionIcon color="brown" variant="subtle" aria-label={`Clone ${brigadeLabel(instance, bt.name)}`} onClick={() => handleCloneBrigade(instance.key)}>
                        <IconCopy size={16} />
                      </ActionIcon>
                    </Tooltip>
                  )}
                  <Tooltip label="Remove this brigade">
                    <ActionIcon color="red" variant="subtle" aria-label={`Remove ${brigadeLabel(instance, bt.name)}`} onClick={() => handleRemoveBrigade(instance.key)}>
                      <IconTrash size={16} />
                    </ActionIcon>
                  </Tooltip>
                </Group>
              </Group>
              {/* What breaks the rules in this brigade, shown whether it's open or folded */}
              {(issuesByBrigade.get(instance.key)?.errors.length ?? 0) > 0 && (
                <div className="brigade-issues">
                  <IconAlertTriangle size={15} aria-hidden className="brigade-issues-icon" />
                  <ul>
                    {issuesByBrigade.get(instance.key)!.errors.map((text, i) => (
                      <li key={i}>{text}</li>
                    ))}
                  </ul>
                </div>
              )}
              {/* What it still needs: only what no slot badge shows while it's open, everything when folded */}
              {(() => {
                const folded = collapsed.has(instance.key);
                const todos = (issuesByBrigade.get(instance.key)?.todos ?? []).filter((t) => folded || !t.onSlot);
                if (todos.length === 0) return null;
                return (
                  <div className="brigade-todos">
                    <span className="brigade-todos-label">Still to add:</span>{" "}
                    {todos.map((t) => t.text.replace(/^Needs at least /, "")).join("; ")}
                  </div>
                );
              })()}

              {collapsed.has(instance.key) &&
                (() => {
                  const summary = brigadeSummary(instance);
                  return (
                    <div className="brigade-summary">
                      {summary.commander && (
                        <Text size="xs" c="brown.6" fs="italic">
                          ★ {summary.commander}
                        </Text>
                      )}
                      <Text size="xs" c={summary.units === "No units yet" ? "dimmed" : undefined}>
                        {summary.units}
                      </Text>
                    </div>
                  );
                })()}

              <Collapse expanded={!collapsed.has(instance.key)} id={`brigade-body-${instance.key}`}>
              <div className="brigade-body">
              {bt.note && (
                <Text size="xs" c="dimmed" mb="sm">
                  {bt.note}
                </Text>
              )}

              {commanderUnit && instance.commanderLine && (
                // A plain row between rules, rather than a box within the card
                <div className="commander-row">
                  <Group justify="space-between" wrap="nowrap">
                    <Text size="sm" fw={600}>
                      Brigade Commander
                    </Text>
                    <Group gap={6} wrap="nowrap">
                      {(commanderUnit.variants?.length ?? 0) > 0 ? (
                        <Select
                          size="xs"
                          w={170}
                          data={commanderUnit.variants!.map((v) => ({
                            value: v.label,
                            // A free commander just shows its rating; "(0 pts)" adds nothing
                            label: v.cost ? `${v.label} (${v.cost} pts)` : v.label,
                          }))}
                          value={instance.commanderLine.variantLabel}
                          onChange={(v) => v && handleCommanderVariant(instance.key, v)}
                          allowDeselect={false}
                        />
                      ) : (
                        <Text size="xs">{commanderUnit.name}</Text>
                      )}
                      {unitCost(commanderUnit, instance.commanderLine.variantLabel) > 0 && (
                        <Text size="xs" c="dimmed" w={56} ta="right">
                          {unitCost(commanderUnit, instance.commanderLine.variantLabel)} pts
                        </Text>
                      )}
                    </Group>
                  </Group>
                </div>
              )}

              <Stack gap="sm">
                {bt.slots.map((slot, slotIndex) => {
                  // Regiment-based slot
                  if (slot.regiment) {
                    const regDef = slot.regiment;
                    const regiments = instance.regimentSlots?.[slotIndex] ?? [];
                  const regimentBadge = limitBadge(regiments.length, regDef.min, regDef.max);
                    return (
                      <Stack key={slotIndex} gap="xs">
                        {/* Regiment header row */}
                        <Group justify="space-between">
                          <Group gap="xs">
                            <Text size="sm" fw={600}>{regDef.label}</Text>
                            <Badge size="sm" variant="light" color={regimentBadge.color} tt="none">
                              {regimentBadge.label}
                            </Badge>
                          </Group>
                          {regiments.length < regDef.max &&
                            (() => {
                              // Greyed out, with the reason, when another rule (the brigade's 3 regiments,
                              // 1 Light Regiment per division) says no
                              const why = regimentBlockedReason({ nation, roster, bt, instance, slotIndex });
                              const button = (
                                <Button
                                  size="compact-xs"
                                  variant="light"
                                  leftSection={<IconPlus size={12} />}
                                  disabled={!!why}
                                  onClick={() => handleAddRegiment(instance.key, slotIndex, regDef)}
                                >
                                  Add {regDef.label}
                                </Button>
                              );
                              return why ? (
                                <Tooltip label={why} withArrow>
                                  <span tabIndex={0} className="unit-option-blocked">{button}</span>
                                </Tooltip>
                              ) : (
                                button
                              );
                            })()}
                        </Group>

                        {/* Regiment instances */}
                        {regiments.map((reg, regIdx) => {
                          const regimentOptions = optionsForRegiment(bt, regDef.slots.flatMap((s) => s.unitIds));
                          return (
                          // A rule down the left side, as Fleet marks a group within a section, not a box
                        <div key={reg.key} className="regiment-block">
                            {/* The regiment's name on the left; its points, upgrades (Guard status) and remove on the right,
                                as on each battalion's row */}
                            <Group justify="space-between" align="center" wrap="nowrap" gap="xs" mb="xs">
                              <Text size="sm" fw={600}>{regDef.label} #{regIdx + 1}</Text>
                              <Group gap={6} wrap="wrap" justify="flex-end" className="regiment-options" role="group" aria-label={`${regDef.label} ${regIdx + 1} upgrades`}>
                                {regimentOptions.map((o) => {
                                  const blocked = regimentOptionBlocked(o, reg, instance);
                                  const chip = (
                                    <Chip
                                      size="xs"
                                      variant="outline"
                                      color="brown"
                                      checked={!!reg.options?.includes(o.id)}
                                      disabled={!!blocked}
                                      onChange={() =>
                                        handleRegimentSlotsChange(
                                          instance.key,
                                          slotIndex,
                                          regiments.map((r) => (r.key === reg.key ? toggleRegimentOption(bt, r, o.id) : r))
                                        )
                                      }
                                    >
                                      {o.label}
                                      {regimentOptionCost(nation, o) && (
                                        <span className="unit-option-cost"> {regimentOptionCost(nation, o)}</span>
                                      )}
                                    </Chip>
                                  );
                                  return blocked ? (
                                    <Tooltip key={o.id} label={blocked} withArrow>
                                      <span tabIndex={0} className="unit-option-blocked">{chip}</span>
                                    </Tooltip>
                                  ) : (
                                    <span key={o.id}>{chip}</span>
                                  );
                                })}
                                <Text size="xs" c="dimmed" ta="right" style={{ whiteSpace: "nowrap" }}>
                                  {reg.slotLines.flat().reduce(
                                    (s, l) => s + lineTotal(nation, l, { bt, regimentOptions: reg.options }),
                                    0
                                  )}{" "}
                                  pts
                                </Text>
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
                                    brigade={{ nation, bt, instance, regimentOptions: reg.options }}
                                    grouped
                                    unitBlocked={(unitId) =>
                                      unitBlockedInRegimentSlot(
                                        { nation, roster, bt, instance, slotIndex },
                                        subSlot,
                                        reg.slotLines[subSlotIdx] ?? [],
                                        unitId
                                      )
                                    }
                                  />
                                );
                              })}
                            </Stack>
                          </div>
                          );
                        })}
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
                      brigade={{ nation, bt, instance }}
                      extraInfo={attachPicker(instance, slotIndex, bt)}
                      lockedReason={slotLockedReason({ nation, roster, bt, instance, slotIndex }, slot)}
                      unitBlocked={(unitId) =>
                        unitBlockedInSlot(
                          { nation, roster, bt, instance, slotIndex },
                          slot,
                          instance.slotLines[slotIndex] ?? [],
                          unitId
                        )
                      }
                    />
                  );
                })}
              </Stack>
              </div>
              </Collapse>
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
