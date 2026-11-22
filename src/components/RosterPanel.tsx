"use client";

import { Badge, Divider, Group, List, Paper, Stack, Text, TextInput, UnstyledButton } from "@mantine/core";
import { IconAlertTriangle, IconBook2, IconCircleCheck, IconListCheck } from "@tabler/icons-react";
import type { BrigadeType, Nation, UnitEntry } from "@/data/types";
import type { RosterState, RosterUnitLine } from "@/types/army";
import { brigadeTotal, commandTotal as armyCommandTotal, lineTotal, rosterTotal } from "@/lib/points";
import { freeLines, resolveLine, type LineContext } from "@/lib/options";
import { periodText, rosterPeriod } from "@/lib/periods";
import {
  attachedText,
  brigadeDisplayName,
  brigadeIssueText,
  REVEAL_BRIGADE_EVENT,
  validateRoster,
  type ValidationIssue,
} from "@/lib/validate";
import { RosterViewModal } from "@/components/RosterViewModal";
import { InstallCard } from "@/components/InstallCard";
import { armyPortrait } from "@/lib/portraits";

interface Props {
  nation: Nation;
  roster: RosterState;
  /** Renames the list */
  onRename?: (name: string) => void;
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
  ctx,
  roster,
}: {
  nation: Nation;
  lines: RosterUnitLine[];
  commander?: boolean;
  /** The brigade (and regiment) the lines are in, so their upgrades show */
  ctx?: LineContext;
  /** The whole army, to name the brigade a battery is attached to */
  roster?: RosterState;
}) {
  return (
    <Stack gap={2}>
      {lines.map((line) => {
        const unit = nation.units.find((u) => u.id === line.unitId);
        if (!unit) return null;
        const sr = unit.category === "Command" ? getStaffRating(unit, line.variantLabel) : undefined;
        const type = commander ? unit.name : (resolveLine(nation, line, ctx)?.name ?? unit.name);
        // A named unit or commander by its name, with its type after it
        const own = line.name?.trim();
        const name = own ? `${own} \u00b7 ${type}` : type;
        const attached = roster ? attachedText(nation, roster, line.attachedTo) : null;
        return (
          <Group key={line.key} justify="space-between" wrap="nowrap" data-free={ctx?.free?.has(line.key) || undefined}>
            <Text
              size="xs"
              c={commander ? "brown.6" : undefined}
              fs={commander ? "italic" : undefined}
              style={{ flex: 1, minWidth: 0 }}
              truncate
            >
              {commander ? "★ " : ""}
              {line.qty > 1 ? `${line.qty}× ` : ""}
              {name}
              {sr !== undefined ? ` (Staff Rating ${sr})` : ""}
              {attached && (
                <Text span size="xs" c="dimmed" fs="italic">
                  {" "}
                  · {attached}
                </Text>
              )}
            </Text>
            <Text size="xs" c="dimmed">
              {commander ? lineTotal(nation, line) : ctx?.free?.has(line.key) && lineTotal(nation, line, ctx) === 0 ? "free" : lineTotal(nation, line, ctx)}
            </Text>
          </Group>
        );
      })}
    </Stack>
  );
}

/** " · Guard status" for a regiment that's taken regiment upgrades */
export function regimentTags(bt: BrigadeType, options: string[] | undefined): string {
  const labels = (bt.options ?? []).filter((o) => options?.includes(o.id)).map((o) => o.label);
  return labels.length ? ` \u00b7 ${labels.join(", ")}` : "";
}

/**
 * One status block: army-wide issues in full, then a line per brigade that takes you to its card, where
 * its own issues are listed
 */
function IssueBlock({
  nation,
  roster,
  issues,
  state,
  title,
}: {
  nation: Nation;
  roster: RosterState;
  issues: ValidationIssue[];
  state: "error" | "todo" | "historical";
  title: string;
}) {
  const army = issues.filter((i) => !i.brigadeKey);
  const byBrigade = roster.brigadeInstances
    .map((bi) => ({ key: bi.key, count: issues.filter((i) => i.brigadeKey === bi.key).length }))
    .filter((b) => b.count > 0);
  const noun = state === "error" ? "to fix" : "to add";
  // Departures are few and are the point, so each is said in full rather than counted
  if (state === "historical") {
    return (
      <div className="roster-status" data-state={state}>
        <Group gap={6} wrap="nowrap" mb={4}>
          <IconBook2 size={16} aria-hidden />
          <Text size="sm" fw={600}>
            {title}
          </Text>
        </Group>
        <List size="xs" spacing={2} className="roster-status-list">
          {issues.map((i, idx) => {
            if (!i.brigadeKey) return <List.Item key={idx}>{i.message}</List.Item>;
            const type = nation.brigades.find(
              (b) => b.id === roster.brigadeInstances.find((bi) => bi.key === i.brigadeKey)?.brigadeTypeId
            )?.name ?? "";
            return (
              <List.Item key={idx}>
                <UnstyledButton
                  className="roster-status-link"
                  onClick={() => window.dispatchEvent(new CustomEvent(REVEAL_BRIGADE_EVENT, { detail: i.brigadeKey }))}
                >
                  {brigadeDisplayName(nation, roster, i.brigadeKey)}
                </UnstyledButton>
                : {brigadeIssueText(i.message, type)}
              </List.Item>
            );
          })}
        </List>
        <Text size="xs" mt={4} c="dimmed">
          The force breaks these of the list&apos;s rules as it fought. Agree them with your opponent.
        </Text>
      </div>
    );
  }
  return (
    <div className="roster-status" data-state={state}>
      <Group gap={6} wrap="nowrap" mb={4}>
        {state === "error" ? <IconAlertTriangle size={16} aria-hidden /> : <IconListCheck size={16} aria-hidden />}
        <Text size="sm" fw={600}>
          {title}
        </Text>
      </Group>
      <List size="xs" spacing={2} className="roster-status-list">
          {army.map((i, idx) => (
            <List.Item key={idx}>{i.message}</List.Item>
          ))}
          {byBrigade.map(({ key, count }) => (
            <List.Item key={key}>
              <UnstyledButton
                className="roster-status-link"
                onClick={() => window.dispatchEvent(new CustomEvent(REVEAL_BRIGADE_EVENT, { detail: key }))}
              >
                {brigadeDisplayName(nation, roster, key)}: {count === 1 ? "1 thing" : `${count} things`} {noun}
                <span aria-hidden> →</span>
              </UnstyledButton>
            </List.Item>
          ))}
      </List>
    </div>
  );
}

/**
 * On a phone the roster sits below the whole builder, so a bar along the foot of the screen keeps the
 * points and the list's state in view while you build, and takes you to the roster. Hidden on wider
 * screens, where the roster card follows you down the page.
 */
export function RosterBar({ nation, roster }: { nation: Nation; roster: RosterState }) {
  const issues = validateRoster(nation, roster);
  const errors = issues.filter((i) => i.level === "error").length;
  const todos = issues.filter((i) => i.level === "todo").length;
  const historical = issues.filter((i) => i.level === "historical").length;
  const status =
    errors > 0
      ? errors === 1 ? "1 to fix" : `${errors} to fix`
      : todos > 0
        ? todos === 1 ? "1 still to add" : `${todos} still to add`
        : historical > 0
          ? historical === 1 ? "As fought, 1 departure" : `As fought, ${historical} departures`
          : "Within limits";
  return (
    <>
      <div className="roster-bar-spacer" aria-hidden />
      <div className="roster-bar" data-state={errors > 0 ? "error" : todos > 0 ? "todo" : "ok"}>
        <div className="roster-bar-text">
          <span className="roster-bar-points">{rosterTotal(nation, roster)} pts</span>
          <span className="roster-bar-status">
            {errors > 0 ? <IconAlertTriangle size={14} aria-hidden /> : todos === 0 ? <IconCircleCheck size={14} aria-hidden /> : null}
            {status}
          </span>
        </div>
        <UnstyledButton
          className="roster-bar-button"
          onClick={() => document.getElementById("roster-panel")?.scrollIntoView({ behavior: "smooth", block: "start" })}
        >
          Roster <span aria-hidden>↓</span>
        </UnstyledButton>
      </div>
    </>
  );
}

export function RosterPanel({ nation, roster, onRename }: Props) {
  const commandTotal = armyCommandTotal(nation, roster);

  const free = freeLines(nation, roster);
  const brigadeTotals = roster.brigadeInstances.map((instance) => ({
    instance,
    bt: nation.brigades.find((b) => b.id === instance.brigadeTypeId),
    total: brigadeTotal(nation, instance, free),
  }));
  const grandTotal = rosterTotal(nation, roster);
  const period = rosterPeriod(nation, roster);
  const flag = nation.flagFile ?? nation.flagFiles?.[0];
  // A named commander's portrait, or the historical force's, with the flag on its corner, as the force cards have
  const portrait = armyPortrait(roster);

  const issues = validateRoster(nation, roster);
  const errors = issues.filter((i) => i.level === "error");
  const todos = issues.filter((i) => i.level === "todo");
  const historical = issues.filter((i) => i.level === "historical");

  return (
    <Stack gap="md">
      <Paper
        withBorder
        p="md"
        radius="md"
        id="roster-panel"
        className="roster-card"
        data-issues={errors.length > 0 || undefined}
        style={{ scrollMarginTop: 16 }}
      >
        <Group justify="space-between" align="flex-start" wrap="nowrap" mb="sm">
          <Group gap="sm" align="center" wrap="nowrap" style={{ minWidth: 0 }}>
            {portrait ? (
              <span className="force-portrait" title={`${portrait.title}, ${portrait.artist}`}>
                <img
                  src={portrait.src}
                  alt={`${portrait.title}, ${portrait.artist}`}
                  style={{ objectPosition: portrait.focus ?? "50% 20%" }}
                />
                {flag && (
                  <span className="force-portrait-flag">
                    <img src={flag} alt={`${nation.name} flag`} />
                  </span>
                )}
              </span>
            ) : flag && (
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
              {/* The list's own name, typed straight into the heading, with "Name your army" until it has one */}
              <TextInput
                variant="unstyled"
                className="army-name-input"
                aria-label="Army name"
                placeholder="Name your army"
                maxLength={60}
                value={roster.armyName}
                onChange={(e) => onRename?.(e.currentTarget.value)}
                readOnly={!onRename}
              />
              <Text size="xs" c="dimmed">
                {nation.name}
                {period && <> &middot; {periodText(period)}</>}
              </Text>
            </Stack>
          </Group>
          <Badge size="xl" variant="filled" color="brown" style={{ flexShrink: 0 }}>
            {grandTotal} pts
          </Badge>
        </Group>

        {/* Shown in full; the page keeps a long card's foot on screen as you scroll (see the builder page) */}
        <div>
          <Stack gap="sm">
            {roster.commandItems.length > 0 && (
              <div className="roster-group">
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
                <div key={instance.key} className="roster-group">
                  <Group justify="space-between" wrap="nowrap">
                    <Text size="sm" fw={600} style={{ minWidth: 0 }}>
                      {instance.name?.trim() || bt.name}
                      {/* A named brigade still says what type it is */}
                      {instance.name?.trim() && (
                        <Text span size="xs" c="dimmed" fw={400}>
                          {" "}
                          · {bt.name}
                        </Text>
                      )}
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
                        <div key={reg.key} className="roster-regiment">
                          <Text size="xs" fw={600} c="dimmed">
                            {reg.name?.trim()
                              ? `${reg.name.trim()} \u00b7 ${slot.regiment!.label} #${regIdx + 1}`
                              : `${slot.regiment!.label} #${regIdx + 1}`}
                            {regimentTags(bt, reg.options)}
                          </Text>
                          <LineList nation={nation} lines={regLines} ctx={{ bt, regimentOptions: reg.options, free }} />
                        </div>
                      );
                    });
                  })}
                  {/* Flat slot lines */}
                  {flatLines.length > 0 && (
                    <LineList nation={nation} lines={flatLines} ctx={{ bt, free }} roster={roster} />
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
        </div>

        <Divider my="sm" />
        <Group justify="space-between">
          <Text size="sm" c="dimmed">
            {roster.brigadeInstances.length} brigade{roster.brigadeInstances.length === 1 ? "" : "s"}
          </Text>
          <Text fw={700}>{grandTotal} pts total</Text>
        </Group>

        {/* Whether the list is legal, inside the card: what breaks the rules in red, what it still needs
            calmly (an unfinished list isn't a mistake), and a quiet green line once it's done */}
        {errors.length === 0 && todos.length === 0 && historical.length === 0 && (
          <div className="roster-status" data-state="ok">
            <Group gap={6} wrap="nowrap">
              <IconCircleCheck size={16} aria-hidden />
              <Text size="sm">Within every brigade&apos;s limits</Text>
            </Group>
          </div>
        )}
        {errors.length > 0 && (
          <IssueBlock
            nation={nation}
            roster={roster}
            issues={errors}
            state="error"
            title={errors.length === 1 ? "1 thing to fix" : `${errors.length} things to fix`}
          />
        )}
        {todos.length > 0 && (
          <IssueBlock nation={nation} roster={roster} issues={todos} state="todo" title="Still to add" />
        )}
        {historical.length > 0 && (
          <IssueBlock
            nation={nation}
            roster={roster}
            issues={historical}
            state="historical"
            title={historical.length === 1 ? "1 historical departure" : `${historical.length} historical departures`}
          />
        )}
      </Paper>

      <RosterViewModal nation={nation} roster={roster} />

      <InstallCard roster={roster} />
    </Stack>
  );
}
