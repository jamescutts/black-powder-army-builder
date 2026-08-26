"use client";

import { useEffect, useMemo, useState } from "react";
import {
  ActionIcon,
  Anchor,
  Container,
  Grid,
  Group,
  Select,
  Stack,
  Text,
  Title,
  Tooltip,
} from "@mantine/core";
import { IconTrash } from "@tabler/icons-react";
import { supplements, nations, getSupplement, getNation, getNationsForSupplement } from "@/data";
import type { RosterState } from "@/types/army";
import { emptyRoster } from "@/types/army";
import { BrigadeBoard } from "@/components/BrigadeBoard";
import { RosterPanel } from "@/components/RosterPanel";
import { ForceOrgNotes } from "@/components/ForceOrgNotes";
import { loadRoster, saveRoster, clearRoster } from "@/lib/storage";

const SUPPLEMENT_OPTIONS = supplements.map((s) => ({ value: s.id, label: s.name }));

export default function HomePage() {
  const [roster, setRoster] = useState<RosterState>(emptyRoster(nations[0].id));
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const saved = loadRoster();
    if (saved) setRoster(saved);
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    saveRoster(roster);
  }, [roster, hydrated]);

  const nation = useMemo(() => getNation(roster.nationId) ?? nations[0], [roster.nationId]);
  const supplement = useMemo(
    () => getSupplement(nation.supplementId) ?? supplements[0],
    [nation.supplementId]
  );
  const nationOptionsForSupplement = useMemo(
    () => getNationsForSupplement(supplement.id).map((n) => ({ value: n.id, label: n.name })),
    [supplement.id]
  );

  function handleSupplementChange(value: string | null) {
    if (!value) return;
    const firstNation = getNationsForSupplement(value)[0];
    if (!firstNation) return;
    setRoster(emptyRoster(firstNation.id));
  }

  function handleNationChange(value: string | null) {
    if (!value) return;
    setRoster(emptyRoster(value));
  }

  function handleClear() {
    setRoster(emptyRoster(roster.nationId));
    clearRoster();
  }

  return (
    <Container size="xl" py="lg">
      <Stack gap="lg">
        <Group justify="space-between" align="flex-end" wrap="wrap">
          <Stack gap={0}>
            <Title
              order={1}
              fz={56}
              fw={700}
              c="brown.7"
              style={{ fontFamily: "var(--font-script), cursive", lineHeight: 1.1 }}
            >
              Black Powder Army Builder
            </Title>
            <Text c="dimmed" size="sm">
              Points calculator for{" "}
              <Anchor href="https://www.warlordgames.com" target="_blank" rel="noreferrer" c="brown.7">
                Black Powder
              </Anchor>{" "}
              supplement army lists.
            </Text>
          </Stack>
          <Group align="flex-end">
            <Select
              label="Supplement"
              data={SUPPLEMENT_OPTIONS}
              value={supplement.id}
              onChange={handleSupplementChange}
              w={200}
              allowDeselect={false}
            />
            <Select
              label="Nation"
              data={nationOptionsForSupplement}
              value={roster.nationId}
              onChange={handleNationChange}
              w={260}
              allowDeselect={false}
            />
            <Tooltip label="Clear army">
              <ActionIcon
                color="red"
                variant="light"
                size="lg"
                onClick={handleClear}
                aria-label="Clear army"
              >
                <IconTrash size={18} />
              </ActionIcon>
            </Tooltip>
          </Group>
        </Group>

        <Text size="sm" c="dimmed">
          {supplement.blurb} — {nation.blurb}
        </Text>

        <Grid gutter="lg">
          <Grid.Col span={{ base: 12, md: 7 }}>
            <BrigadeBoard key={nation.id} nation={nation} roster={roster} onChange={setRoster} />
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 5 }}>
            <Stack gap="md">
              <RosterPanel nation={nation} roster={roster} />
              <ForceOrgNotes nation={nation} />
            </Stack>
          </Grid.Col>
        </Grid>
      </Stack>
    </Container>
  );
}
