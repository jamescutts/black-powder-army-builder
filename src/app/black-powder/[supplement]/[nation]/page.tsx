"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
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
import { supplements, getSupplement, getNation, getNationsForSupplement } from "@/data";
import type { RosterState } from "@/types/army";
import { emptyRoster } from "@/types/army";
import { BrigadeBoard } from "@/components/BrigadeBoard";
import { RosterPanel } from "@/components/RosterPanel";
import { ForceOrgNotes } from "@/components/ForceOrgNotes";
import { saveRoster, clearRoster } from "@/lib/storage";

const SUPPLEMENT_OPTIONS = supplements.map((s) => ({ value: s.id, label: s.name }));

function FlagIcon({ src, alt }: { src: string; alt: string }) {
  return (
    <div
      style={{
        position: "relative",
        width: 20,
        height: 14,
        borderRadius: 2,
        overflow: "hidden",
        flexShrink: 0,
      }}
    >
      <img
        src={src}
        alt={alt}
        style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: [
            "radial-gradient(ellipse at center, transparent 40%, rgba(60,30,5,0.35) 100%)",
            "linear-gradient(135deg, rgba(180,130,60,0.18) 0%, rgba(120,70,20,0.22) 100%)",
          ].join(", "),
          mixBlendMode: "multiply",
          pointerEvents: "none",
        }}
      />
    </div>
  );
}

export default function BuilderPage() {
  const params = useParams<{ supplement: string; nation: string }>();
  const router = useRouter();

  const nation = getNation(params.nation);
  const nationValid = !!nation && nation.supplementId === params.supplement;

  useEffect(() => {
    if (!nationValid) {
      router.replace(nation ? `/black-powder/${nation.supplementId}` : "/black-powder");
    }
  }, [nationValid, nation, router]);

  if (!nationValid) return null;

  return <BuilderContent nationId={params.nation} />;
}

function BuilderContent({ nationId }: { nationId: string }) {
  const router = useRouter();

  const [roster, setRoster] = useState<RosterState>(() => emptyRoster(nationId));

  // The nation is always driven by the URL — navigating to a new nation/supplement always
  // starts a fresh army list for that nation.
  useEffect(() => {
    setRoster(emptyRoster(nationId));
  }, [nationId]);

  useEffect(() => {
    saveRoster(roster);
  }, [roster]);

  const nation = useMemo(() => getNation(nationId)!, [nationId]);
  const supplement = useMemo(
    () => getSupplement(nation.supplementId) ?? supplements[0],
    [nation.supplementId]
  );
  const nationOptionsForSupplement = useMemo(
    () => getNationsForSupplement(supplement.id).map((n) => ({
      value: n.id,
      label: n.name,
      flagFile: n.flagFile,
    })),
    [supplement.id]
  );

  function handleSupplementChange(value: string | null) {
    if (!value) return;
    const firstNation = getNationsForSupplement(value)[0];
    if (!firstNation) return;
    router.replace(`/black-powder/${value}/${firstNation.id}`, { scroll: false });
  }

  function handleNationChange(value: string | null) {
    if (!value) return;
    router.replace(`/black-powder/${supplement.id}/${value}`, { scroll: false });
  }

  function handleClear() {
    setRoster(emptyRoster(nationId));
    clearRoster();
  }

  return (
    <Container size="xl" py="lg">
      <Stack gap="lg">
        <Group justify="space-between" align="flex-end" wrap="wrap">
          <Stack gap={0} style={{ userSelect: "none" }}>
            <Anchor component={Link} href="/black-powder" underline="never">
              <Title
                order={1}
                fz={56}
                fw={700}
                c="brown.7"
                style={{ fontFamily: "var(--font-script), cursive", lineHeight: 1.1 }}
              >
                Black Powder Army Builder
              </Title>
            </Anchor>
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
              value={nation.id}
              onChange={handleNationChange}
              w={260}
              allowDeselect={false}
              leftSection={nation.flagFile ? <FlagIcon src={nation.flagFile} alt="" /> : undefined}
              renderOption={({ option }) => {
                const flag = (option as typeof nationOptionsForSupplement[number]).flagFile;
                return (
                  <Group gap="xs" wrap="nowrap">
                    {flag && <FlagIcon src={flag} alt="" />}
                    <span>{option.label}</span>
                  </Group>
                );
              }}
            />
            <Tooltip label="Clear army">
              <ActionIcon
                color="red"
                variant="filled"
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

        <Grid gap="lg">
          <Grid.Col span={{ base: 12, md: 7 }}>
            <BrigadeBoard key={nation.id} nation={nation} roster={roster} onChange={setRoster} />
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 5 }}>
            <Stack gap="md" style={{ position: "sticky", top: 16 }}>
              <RosterPanel nation={nation} roster={roster} />
              <ForceOrgNotes nation={nation} />
            </Stack>
          </Grid.Col>
        </Grid>
      </Stack>
    </Container>
  );
}
