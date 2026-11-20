"use client";

import { useEffect, useState } from "react";
import { ActionIcon, Button, Group, Paper, Stack, Text } from "@mantine/core";
import { IconDownload, IconX } from "@tabler/icons-react";
import type { RosterState } from "@/types/army";
import { useInstallApp } from "@/components/InstallApp";

const DISMISSED_KEY = "ab-install-card-dismissed-at";

// Offered once a list is under way, when keeping it for game day makes sense, rather than on arrival
const MIN_UNITS = 3;

function unitCount(roster: RosterState): number {
  return (
    roster.commandItems.length +
    roster.brigadeInstances.reduce(
      (sum, b) =>
        sum +
        (b.commanderLine ? 1 : 0) +
        b.slotLines.flat().length +
        (b.regimentSlots ?? []).reduce((r, slot) => r + (slot ?? []).reduce((s, reg) => s + reg.slotLines.flat().length, 0), 0),
      0
    )
  );
}

/**
 * "Take it to the table": a small card under the roster, inviting you to install the site so the army is
 * there with no signal. Shown once the list has a few units, only where the browser can install, and
 * never again once closed.
 */
export function InstallCard({ roster }: { roster: RosterState }) {
  const { mode, install, help } = useInstallApp();
  // Starts hidden, so the server's page and the first render in the browser agree
  const [dismissed, setDismissed] = useState(true);

  useEffect(() => {
    try {
      setDismissed(!!localStorage.getItem(DISMISSED_KEY));
    } catch {
      setDismissed(false);
    }
  }, []);

  const dismiss = () => {
    setDismissed(true);
    try {
      localStorage.setItem(DISMISSED_KEY, String(Date.now()));
    } catch {
      // Storage unavailable: it stays closed for this visit
    }
  };

  if (!mode || dismissed || unitCount(roster) < MIN_UNITS) return null;

  return (
    <Paper withBorder p="md" radius="md" className="install-card">
      <Group justify="space-between" align="flex-start" wrap="nowrap" gap="xs">
        <Stack gap={4}>
          <Text ff="heading" fw={600} c="brown.8">
            Take it to the table
          </Text>
          <Text size="sm" c="dimmed" style={{ lineHeight: 1.5 }}>
            Install Army Builder and your armies open like an app, even with no signal at the club.
          </Text>
        </Stack>
        <ActionIcon variant="subtle" color="gray" onClick={dismiss} aria-label="Don't show this again">
          <IconX size={16} />
        </ActionIcon>
      </Group>
      <Button
        mt="sm"
        size="xs"
        color="brown"
        leftSection={<IconDownload size={14} />}
        onClick={install}
      >
        Install the app
      </Button>
      {help}
    </Paper>
  );
}
