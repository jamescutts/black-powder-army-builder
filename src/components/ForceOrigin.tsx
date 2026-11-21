"use client";

import Link from "next/link";
import { useState } from "react";
import { Anchor, Button, Collapse, Group, List, Paper, Stack, Text, UnstyledButton } from "@mantine/core";
import { IconBook2, IconChevronDown, IconRestore } from "@tabler/icons-react";
import type { HistoricalBattle, HistoricalForce } from "@/data/types";

/**
 * Above a list started from a historical force: which force and battle, what it did, how it was built
 * (its notes) and where from, with a way to put it back as it fought.
 */
export function ForceOrigin({
  force,
  battle,
  onReset,
}: {
  force: HistoricalForce;
  battle: HistoricalBattle;
  onReset: () => void;
}) {
  const [open, setOpen] = useState(false);
  return (
    <Paper withBorder radius="md" p="md" className="force-origin">
      <Group justify="space-between" align="flex-start" gap="sm" wrap="wrap">
        <Group gap="sm" align="flex-start" wrap="nowrap" style={{ flex: "1 1 320px", minWidth: 0 }}>
          <IconBook2 size={20} aria-hidden className="force-origin-icon" />
          <Stack gap={2} style={{ minWidth: 0 }}>
            <Text size="xs" tt="uppercase" fw={600} c="dimmed" lts={0.5}>
              Historical force ·{" "}
              <Anchor component={Link} href={`/black-powder/battles#${battle.id}`} inherit c="brown.7">
                {battle.name}, {battle.date}
              </Anchor>
            </Text>
            <Text ff="heading" fw={600} fz="lg" c="brown.8" lh={1.25}>
              {force.name}
              {force.formation && (
                <Text span size="sm" c="dimmed" fw={400} ff="body">
                  {" "}
                  · {force.formation}
                </Text>
              )}
            </Text>
            <Text size="sm" style={{ lineHeight: 1.55 }}>
              {force.summary}
            </Text>
          </Stack>
        </Group>
        <Button variant="default" size="xs" leftSection={<IconRestore size={14} />} onClick={onReset}>
          Reset to historical
        </Button>
      </Group>

      <UnstyledButton className="force-origin-toggle" onClick={() => setOpen((o) => !o)} aria-expanded={open} mt="xs">
        <IconChevronDown size={14} aria-hidden style={{ transform: open ? "rotate(180deg)" : undefined }} />
        How it&apos;s built and sources
      </UnstyledButton>
      <Collapse expanded={open}>
        <Stack gap="xs" mt="xs" pl={28}>
          {force.notes && force.notes.length > 0 && (
            <List size="sm" spacing={4}>
              {force.notes.map((n, i) => (
                <List.Item key={i}>{n}</List.Item>
              ))}
            </List>
          )}
          <Text size="xs" c="dimmed">
            Built from:{" "}
            {battle.sources.map((s, i) => (
              <span key={i}>
                {i > 0 && "; "}
                {s.url ? (
                  <Anchor href={s.url} target="_blank" rel="noreferrer" inherit c="brown.7">
                    {s.label}
                  </Anchor>
                ) : (
                  s.label
                )}
              </span>
            ))}
            . This list is yours to change: anything you add or take away is checked as usual.
          </Text>
        </Stack>
      </Collapse>
    </Paper>
  );
}
