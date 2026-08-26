"use client";

import { Alert, List, Text } from "@mantine/core";
import { IconInfoCircle } from "@tabler/icons-react";
import type { Nation } from "@/data/types";

export function ForceOrgNotes({ nation }: { nation: Nation }) {
  return (
    <Alert
      variant="light"
      color="yellow"
      title="Force organisation reference"
      icon={<IconInfoCircle />}
    >
      <Text size="sm" mb="xs">
        Brigade and slot minimums/maximums are enforced above. The extra conditions below (troop
        ratios, &ldquo;only if N brigades taken&rdquo;, per-1000-points scaling, etc.) are not
        structurally checked — verify these against the book before playing.
      </Text>
      <List size="sm" spacing={4}>
        {nation.notes.map((note, i) => (
          <List.Item key={i}>{note}</List.Item>
        ))}
      </List>
    </Alert>
  );
}
