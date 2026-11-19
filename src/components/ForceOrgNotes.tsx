"use client";

import type { ReactNode } from "react";
import Link from "next/link";
import { Anchor, Grid, List, Paper, Stack, Text, Title } from "@mantine/core";
import { IconFlag, IconListDetails, IconStar } from "@tabler/icons-react";
import type { AlliesRule, Nation } from "@/data/types";
import { getNation } from "@/data";

function joinNodes(nodes: ReactNode[], sep: string): ReactNode {
  return nodes.flatMap((node, i) => (i === 0 ? [node] : [sep, node]));
}

function AllyRuleItem({ rule }: { rule: AlliesRule }) {
  const names = (rule.nationIds ?? [])
    .map((id) => getNation(id))
    .filter((ally): ally is Nation => ally !== undefined)
    .map((ally) => (
      <Anchor
        key={ally.id}
        component={Link}
        href={`/black-powder/${ally.supplementId}/${ally.id}`}
        c="brown.7"
      >
        {ally.name}
      </Anchor>
    ));

  return (
    <List.Item>
      Up to {rule.maxPercent}% of points from{" "}
      {names.length > 0 ? joinNodes(names, " or ") : rule.note}
      {names.length > 0 && rule.note && <> ({rule.note})</>}.
    </List.Item>
  );
}

type Tone = "org" | "rules" | "allies";

/** A notes card whose heading sits on a strip tinted for its topic, so each one is easy to pick out */
function NoteCard({ tone, icon, title, children }: { tone: Tone; icon: ReactNode; title: string; children: ReactNode }) {
  return (
    <Paper withBorder radius="md" className="note-card" data-tone={tone}>
      <div className="note-card-head">
        <span className="note-card-icon" aria-hidden>
          {icon}
        </span>
        <Title order={3} className="notes-subhead">
          {title}
        </Title>
      </div>
      <div className="note-card-body">{children}</div>
    </Paper>
  );
}

/**
 * Reference notes for the army list, below the builder: each topic in a card with a tinted heading
 * strip, echoing the colours of the boxes they replaced, and what the builder doesn't model yet in a
 * pale aside.
 */
export function ForceOrgNotes({ nation }: { nation: Nation }) {
  const hasSpecial = !!nation.specialRules?.length;
  const hasAllies = !!nation.alliesRules?.length;
  const notModelled = [
    "unit upgrades and downgrades (Veteran, Tough Fighters, Large and Small units, half batteries and so on)",
    ...(nation.supplementId === "albion-triumphant-1"
      ? ["the Early, Middle and Late campaign periods"]
      : []),
  ];

  return (
    <Stack
      gap="md"
      component="section"
      aria-labelledby="list-notes-heading"
      className="list-notes"
    >
      <Title order={2} className="builder-heading" id="list-notes-heading">
        About this army list
      </Title>

      <aside className="builder-wip">
        <Text size="sm">
          <strong>Not modelled yet:</strong> {notModelled.join(", or ")}. Apply
          these from the book when you finalise your list.
        </Text>
      </aside>

      <Grid gap="xl">
        <Grid.Col span={{ base: 12, md: hasSpecial || hasAllies ? 7 : 12 }}>
          <NoteCard tone="org" icon={<IconListDetails size={16} />} title="Force organisation">
            <Text size="sm" c="dimmed" mb="xs">
              The builder checks brigade and slot limits as you go. These
              conditions aren&rsquo;t checked, so confirm them against the book.
            </Text>
            {nation.notes.length > 0 && (
              <List size="sm" spacing={6}>
                {nation.notes.map((note, i) => (
                  <List.Item key={i}>{note}</List.Item>
                ))}
              </List>
            )}
          </NoteCard>
        </Grid.Col>

        {(hasSpecial || hasAllies) && (
          <Grid.Col span={{ base: 12, md: 5 }}>
            <Stack gap="lg">
              {hasSpecial && (
                <NoteCard tone="rules" icon={<IconStar size={16} />} title="National special rules">
                  <List size="sm" spacing={6}>
                    {nation.specialRules!.map((rule, i) => (
                      <List.Item key={i}>{rule}</List.Item>
                    ))}
                  </List>
                </NoteCard>
              )}
              {hasAllies && (
                <NoteCard tone="allies" icon={<IconFlag size={16} />} title="Allied contingents">
                  <List size="sm" spacing={6} mb="xs">
                    {nation.alliesRules!.map((rule, i) => (
                      <AllyRuleItem key={i} rule={rule} />
                    ))}
                  </List>
                  <Text size="sm" c="dimmed">
                    Allied brigades can&rsquo;t be added here yet. Build the
                    allied part as its own list and add the totals together.
                  </Text>
                </NoteCard>
              )}
            </Stack>
          </Grid.Col>
        )}
      </Grid>
    </Stack>
  );
}
