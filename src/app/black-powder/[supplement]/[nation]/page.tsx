"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import {
  Anchor,
  Breadcrumbs,
  Container,
  Grid,
  Group,
  Select,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { supplements, getSupplement, getNation, getNationsForSupplement } from "@/data";
import type { RosterState } from "@/types/army";
import { emptyRoster } from "@/types/army";
import { BrigadeBoard } from "@/components/BrigadeBoard";
import { RosterPanel } from "@/components/RosterPanel";
import { ForceOrgNotes } from "@/components/ForceOrgNotes";
import { loadRoster, saveRoster, clearRoster } from "@/lib/storage";
import { ConfirmModal } from "@/components/ConfirmModal";

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

  const nation = useMemo(() => getNation(nationId)!, [nationId]);

  const [roster, setRoster] = useState<RosterState>(() => emptyRoster(nationId));
  // Which nation's saved army has been read back from the browser. Until it has, nothing is saved,
  // so the empty starting army can't overwrite the real one.
  const [loadedFor, setLoadedFor] = useState<string | null>(null);

  // The nation is driven by the URL. Each nation keeps its own saved army, read back after mount
  // (localStorage isn't available while rendering on the server).
  useEffect(() => {
    setRoster(loadRoster(nation) ?? emptyRoster(nation.id));
    setLoadedFor(nation.id);
  }, [nation]);

  useEffect(() => {
    if (loadedFor !== nationId || roster.nationId !== nationId) return;
    saveRoster(roster);
  }, [roster, loadedFor, nationId]);

  const supplement = useMemo(
    () => getSupplement(nation.supplementId) ?? supplements[0],
    [nation.supplementId]
  );
  const nationOptionsForSupplement = useMemo(
    () => getNationsForSupplement(supplement.id).map((n) => ({
      value: n.id,
      label: n.name,
      flagFile: n.flagFile ?? n.flagFiles?.[0],
    })),
    [supplement.id]
  );

  // Clearing throws the army away, so ask first once there's anything in it. Switching nation doesn't
  // need asking: each nation's army is saved separately and is there again on switching back.
  const hasUnits = roster.commandItems.length > 0 || roster.brigadeInstances.length > 0;
  const [confirmingClear, setConfirmingClear] = useState(false);

  function handleNationChange(value: string | null) {
    if (!value) return;
    router.replace(`/black-powder/${supplement.id}/${value}`, { scroll: false });
  }

  // Clearing empties the list but keeps its name
  function handleClear() {
    const cleared = { ...emptyRoster(nationId), armyName: roster.armyName };
    setRoster(cleared);
    if (!cleared.armyName.trim()) clearRoster(nationId);
    setConfirmingClear(false);
  }

  return (
    <>
      <ConfirmModal
        opened={confirmingClear}
        title="Clear this army?"
        confirmLabel="Clear army"
        onConfirm={handleClear}
        onCancel={() => setConfirmingClear(false)}
      >
        This removes every unit and brigade from the army you&apos;ve built for {nation.name}. It can&apos;t be undone.
      </ConfirmModal>
      {/* Fleet-style page head: breadcrumbs, then the army's flag and name as the page title, with only its
          own description under it. Supplement and rule set are in the breadcrumbs, which link back. */}
      <Container size="xl" pt="lg" pb="sm">
        <Stack gap="sm">
          <Breadcrumbs separator="›" className="army-crumbs">
            <Anchor component={Link} href="/black-powder" size="sm" c="brown.7">
              Black Powder
            </Anchor>
            <Anchor component={Link} href={`/black-powder/${supplement.id}`} size="sm" c="brown.7">
              {supplement.name}
            </Anchor>
            <Text size="sm" c="dimmed">
              {nation.name}
            </Text>
          </Breadcrumbs>

          <Group justify="space-between" align="flex-end" wrap="wrap" gap="md">
            <Group gap="md" wrap="nowrap" align="center" style={{ flex: "1 1 360px", minWidth: 0 }}>
              {(nation.flagFile ?? nation.flagFiles?.[0]) && (
                <span className="army-flag">
                  <img src={(nation.flagFile ?? nation.flagFiles?.[0])} alt="" />
                </span>
              )}
              <Stack gap={2} style={{ minWidth: 0 }}>
                <Title order={1} className="army-title">
                  {nation.name}
                </Title>
                <Text size="sm" c="dimmed">
                  {nation.blurb}
                  {nation.attribution && (
                    <>
                      {" "}
                      (Community list by{" "}
                      {nation.attribution.sourceUrl ? (
                        <Anchor href={nation.attribution.sourceUrl} target="_blank" rel="noreferrer" c="brown.7" inherit>
                          {nation.attribution.author}
                        </Anchor>
                      ) : (
                        nation.attribution.author
                      )}
                      )
                    </>
                  )}
                </Text>
              </Stack>
            </Group>
            {/* Other armies from the same book; a different book is a breadcrumb away */}
            <Select
              label="Switch army"
              size="sm"
              data={nationOptionsForSupplement}
              value={nation.id}
              onChange={handleNationChange}
              w={250}
              allowDeselect={false}
              leftSection={
                nation.flagFile || nation.flagFiles?.[0] ? (
                  <FlagIcon src={(nation.flagFile ?? nation.flagFiles?.[0])!} alt="" />
                ) : undefined
              }
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
          </Group>
        </Stack>
      </Container>

      {/* Held back until the saved army is read, so it doesn't flash up empty first */}
      {loadedFor === nationId && (
        <Container size="xl" py="lg">
          <Grid gap="lg">
            <Grid.Col span={{ base: 12, md: 7 }}>
              <BrigadeBoard key={nation.id} nation={nation} roster={roster} onChange={setRoster} />
            </Grid.Col>
            <Grid.Col span={{ base: 12, md: 5 }}>
              {/* Only the roster follows you down the page; the reference notes sit below the builder */}
              <div style={{ position: "sticky", top: 16 }}>
                <RosterPanel
                  nation={nation}
                  roster={roster}
                  onClear={hasUnits ? () => setConfirmingClear(true) : undefined}
                  onRename={(armyName) => setRoster({ ...roster, armyName })}
                />
              </div>
            </Grid.Col>
          </Grid>

          <div className="list-notes-wrap">
            <ForceOrgNotes nation={nation} />
          </div>
        </Container>
      )}
    </>
  );
}
