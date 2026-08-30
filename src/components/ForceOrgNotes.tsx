"use client";

import type { ReactNode } from "react";
import Link from "next/link";
import { Alert, Anchor, List, Text } from "@mantine/core";
import { IconInfoCircle, IconAlertTriangle, IconStar, IconFlag } from "@tabler/icons-react";
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

export function ForceOrgNotes({ nation }: { nation: Nation }) {
  return (
    <>
      {nation.specialRules && nation.specialRules.length > 0 && (
        <Alert
          variant="light"
          color="brown"
          title="National special rules"
          icon={<IconStar />}
        >
          <List size="sm" spacing={4}>
            {nation.specialRules.map((rule, i) => (
              <List.Item key={i}>{rule}</List.Item>
            ))}
          </List>
        </Alert>
      )}
      {nation.alliesRules && nation.alliesRules.length > 0 && (
        <Alert
          variant="light"
          color="gray"
          title="Allied contingents"
          icon={<IconFlag />}
        >
          <Text size="sm" mb="xs">
            Adding allied brigades isn&rsquo;t supported yet — build the allied portion as its own
            roster and combine the totals manually.
          </Text>
          <List size="sm" spacing={4}>
            {nation.alliesRules.map((rule, i) => (
              <AllyRuleItem key={i} rule={rule} />
            ))}
          </List>
        </Alert>
      )}
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
