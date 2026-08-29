"use client";

import { Alert, List, Text } from "@mantine/core";
import { IconInfoCircle, IconAlertTriangle } from "@tabler/icons-react";
import type { Nation } from "@/data/types";

export function ForceOrgNotes({ nation }: { nation: Nation }) {
  return (
    <>
      <Alert
        variant="light"
        color="orange"
        title="Upgrades/downgrades not yet supported"
        icon={<IconAlertTriangle />}
      >
        <Text size="sm">
          This builder does not yet model the book&rsquo;s point-modifier unit upgrades and
          downgrades (Veteran status, Tough Fighters, Large/Small units, half batteries, etc.).
          Apply these manually per the book when finalising a list.
        </Text>
      </Alert>
      {nation.supplementId === "albion-triumphant-1" && (
        <Alert
          variant="light"
          color="orange"
          title="Early/Middle/Late periods not yet supported"
          icon={<IconAlertTriangle />}
        >
          <Text size="sm">
            This builder does not yet restrict options by the book&rsquo;s Early/Middle/Late
            campaign periods. Check the book for which units and options are available in your
            chosen period.
          </Text>
        </Alert>
      )}
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
        {nation.notes.length > 0 && (
          <List size="sm" spacing={4}>
            {nation.notes.map((note, i) => (
              <List.Item key={i}>{note}</List.Item>
            ))}
          </List>
        )}
      </Alert>
    </>
  );
}
