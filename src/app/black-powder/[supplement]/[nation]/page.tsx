"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";
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
import { loadRoster, saveRoster, clearRoster } from "@/lib/storage";
import { ConfirmModal } from "@/components/ConfirmModal";

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
    clearRoster(nationId);
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
      {/* The army being built, in a tinted band under the site header, like the support band in the footer */}
      <div className="page-band">
        <Container size="xl">
          <Stack gap="sm">
            {/* The army being built on the left, with the pickers to change it centred beside it */}
            <Group justify="space-between" align="center" wrap="wrap">
              {/* Grows to fill the row, so a long nation name wraps beside the pickers instead of pushing them down */}
              <Stack gap={0} style={{ flex: "1 1 320px", minWidth: 0, userSelect: "none" }}>
                {/* Cinzel, the content heading font; the script is kept for the site name in the header */}
                <Title order={1} fz={{ base: 22, sm: 26 }} fw={600} c="brown.7" lh={1.2}>
                  {nation.name}
                </Title>
                {/* The book it comes from: italic and brown, like a title, rather than grey small print */}
                <Text fz="md" fs="italic" c="brown.6" mt={2}>
                  {supplement.name}
                </Text>
              </Stack>
              <Group align="flex-end" wrap="wrap">
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
                <Tooltip label="Clear army">
                  <ActionIcon
                    color="red"
                    variant="filled"
                    size="lg"
                    onClick={() => setConfirmingClear(true)}
                    disabled={!hasUnits}
                    aria-label="Clear army"
                  >
                    <IconTrash size={18} />
                  </ActionIcon>
                </Tooltip>
              </Group>
            </Group>

            <Text size="sm" c="dimmed">
              {supplement.blurb} — {nation.blurb}
              {nation.attribution && (
                <>
                  {" "}
                  (Community list by{" "}
                  {nation.attribution.sourceUrl ? (
                    <Anchor href={nation.attribution.sourceUrl} target="_blank" rel="noreferrer" c="brown.7">
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
        </Container>
      </div>

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
                <RosterPanel nation={nation} roster={roster} />
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
