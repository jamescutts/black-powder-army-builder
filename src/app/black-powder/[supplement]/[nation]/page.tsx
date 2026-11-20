"use client";

import { Suspense, useEffect, useMemo, useRef, useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import {
  Anchor,
  Breadcrumbs,
  Button,
  Container,
  Grid,
  Group,
  Menu,
  Select,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { IconChevronDown, IconCopy, IconEraser, IconFolder, IconPlus, IconTrash } from "@tabler/icons-react";
import { supplements, getSupplement, getNation, getNationsForSupplement } from "@/data";
import type { RosterState } from "@/types/army";
import { emptyRoster } from "@/types/army";
import { BrigadeBoard } from "@/components/BrigadeBoard";
import { RosterBar, RosterPanel } from "@/components/RosterPanel";
import { ForceOrgNotes } from "@/components/ForceOrgNotes";
import {
  deleteList,
  duplicateList,
  listHref,
  listSaved,
  listSavedFor,
  loadList,
  newListId,
  saveList,
  type SavedList,
} from "@/lib/storage";
import { rosterTotal } from "@/lib/points";
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

  // Reads which saved list to open from the address (?list=...)
  return (
    <Suspense>
      <BuilderContent nationId={params.nation} />
    </Suspense>
  );
}

function BuilderContent({ nationId }: { nationId: string }) {
  const router = useRouter();

  const nation = useMemo(() => getNation(nationId)!, [nationId]);

  const listParam = useSearchParams().get("list");

  const [roster, setRoster] = useState<RosterState>(() => emptyRoster(nationId));
  // Which saved list is open. Until one has been read back from the browser, nothing is saved, so the
  // empty starting army can't overwrite the real one.
  const [listId, setListId] = useState<string | null>(null);

  // The list is driven by the address: the one it names, else this nation's most recently changed list,
  // else a new one. Read after mount, as localStorage isn't available while rendering on the server.
  useEffect(() => {
    let id = listParam;
    if (!id) {
      id = listSavedFor(nation.id)[0]?.id ?? newListId();
      router.replace(listHref(nation.supplementId, nation.id, id), { scroll: false });
    } else {
      // A list from another nation (an edited or old link) opens on its own nation's page
      const elsewhere = listSaved().find((l) => l.id === id && l.roster.nationId !== nation.id);
      const other = elsewhere && getNation(elsewhere.roster.nationId);
      if (other) {
        router.replace(listHref(other.supplementId, other.id, id));
        return;
      }
    }
    setRoster(loadList(nation, id) ?? emptyRoster(nation.id));
    setListId(id);
  }, [nation, listParam, router]);

  useEffect(() => {
    if (!listId || roster.nationId !== nationId) return;
    saveList(listId, roster);
  }, [roster, listId, nationId]);

  // The roster card follows you down the page, shown in full. While it fits the window it sticks 16px
  // from the top; once it's taller, it sticks by its foot instead (a negative top), so it scrolls with the
  // page until its status and buttons reach the bottom of the window, and stays there.
  const stickyRef = useRef<HTMLDivElement>(null);
  const [stickyTop, setStickyTop] = useState(16);
  useEffect(() => {
    const el = stickyRef.current;
    if (!el) return;
    const fit = () => setStickyTop(Math.min(16, window.innerHeight - el.offsetHeight - 16));
    // Called once on observing, then whenever the card grows or shrinks
    const observer = new ResizeObserver(fit);
    observer.observe(el);
    window.addEventListener("resize", fit);
    return () => {
      observer.disconnect();
      window.removeEventListener("resize", fit);
    };
  }, [listId]);

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

  // Clearing or deleting throws the army away, so both ask first. Switching nation doesn't need asking:
  // the list is saved, and is in the Lists menu and My armies.
  const hasUnits = roster.commandItems.length > 0 || roster.brigadeInstances.length > 0;
  const isSaved = hasUnits || !!roster.armyName.trim();
  const [confirming, setConfirming] = useState<"clear" | "delete" | null>(null);
  // This nation's other saved lists, for the Lists menu; read when it opens
  const [otherLists, setOtherLists] = useState<SavedList[]>([]);

  function handleNationChange(value: string | null) {
    if (!value) return;
    router.replace(`/black-powder/${supplement.id}/${value}`, { scroll: false });
  }

  const openList = (id: string) => router.push(listHref(supplement.id, nationId, id), { scroll: false });

  // Clearing empties the list but keeps its name
  function handleClear() {
    setRoster({ ...emptyRoster(nationId), armyName: roster.armyName });
    setConfirming(null);
  }

  // Deleting removes the list and opens this nation's next most recent one (or a new one)
  function handleDelete() {
    if (listId) deleteList(listId);
    setConfirming(null);
    setListId(null);
    const next = listSavedFor(nationId)[0]?.id ?? newListId();
    router.replace(listHref(supplement.id, nationId, next), { scroll: false });
  }

  function handleDuplicate() {
    if (!listId) return;
    saveList(listId, roster);
    const copy = duplicateList(listId);
    if (copy) openList(copy);
  }

  return (
    <>
      <ConfirmModal
        opened={confirming === "clear"}
        title="Clear this army?"
        confirmLabel="Clear army"
        onConfirm={handleClear}
        onCancel={() => setConfirming(null)}
      >
        This removes every unit and brigade from {roster.armyName.trim() || "this army"}, keeping its name. It
        can&apos;t be undone.
      </ConfirmModal>
      <ConfirmModal
        opened={confirming === "delete"}
        title="Delete this list?"
        confirmLabel="Delete list"
        onConfirm={handleDelete}
        onCancel={() => setConfirming(null)}
      >
        This deletes {roster.armyName.trim() || "this army"} from this browser. It can&apos;t be undone.
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
            {/* Switching and clearing sit together: both change which army you're working on */}
            <Group gap="xs" align="flex-end" wrap="nowrap">
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
              {/* Everything about the list itself: start another, open another, copy, clear or delete it */}
              <Menu
                position="bottom-end"
                width={260}
                shadow="md"
                onOpen={() => setOtherLists(listSavedFor(nationId).filter((l) => l.id !== listId))}
              >
                <Menu.Target>
                  <Button variant="default" size="sm" h={36} rightSection={<IconChevronDown size={16} />}>
                    Lists
                  </Button>
                </Menu.Target>
                <Menu.Dropdown>
                  <Menu.Item leftSection={<IconPlus size={16} />} onClick={() => openList(newListId())}>
                    New {nation.name} list
                  </Menu.Item>
                  <Menu.Item leftSection={<IconCopy size={16} />} onClick={handleDuplicate} disabled={!isSaved}>
                    Duplicate this list
                  </Menu.Item>
                  {otherLists.length > 0 && (
                    <>
                      <Menu.Divider />
                      <Menu.Label>Your other {nation.name} lists</Menu.Label>
                      {otherLists.slice(0, 6).map((l) => (
                        <Menu.Item
                          key={l.id}
                          onClick={() => openList(l.id)}
                          rightSection={
                            <Text size="xs" c="dimmed">
                              {rosterTotal(nation, l.roster)} pts
                            </Text>
                          }
                        >
                          <Text size="sm" truncate maw={170}>
                            {l.roster.armyName.trim() || "Unnamed army"}
                          </Text>
                        </Menu.Item>
                      ))}
                    </>
                  )}
                  <Menu.Divider />
                  <Menu.Item leftSection={<IconFolder size={16} />} component={Link} href="/armies">
                    All my armies
                  </Menu.Item>
                  <Menu.Divider />
                  <Menu.Item
                    color="red"
                    leftSection={<IconEraser size={16} />}
                    onClick={() => setConfirming("clear")}
                    disabled={!hasUnits}
                  >
                    Clear army
                  </Menu.Item>
                  <Menu.Item
                    color="red"
                    leftSection={<IconTrash size={16} />}
                    onClick={() => setConfirming("delete")}
                    disabled={!isSaved}
                  >
                    Delete list
                  </Menu.Item>
                </Menu.Dropdown>
              </Menu>
            </Group>
          </Group>
        </Stack>
      </Container>

      {/* Held back until the saved army is read, so it doesn't flash up empty first */}
      {listId && roster.nationId === nationId && (
        <Container size="xl" py="lg">
          <Grid gap="lg">
            <Grid.Col span={{ base: 12, md: 7 }}>
              <BrigadeBoard key={listId} nation={nation} roster={roster} onChange={setRoster} />
            </Grid.Col>
            <Grid.Col span={{ base: 12, md: 5 }}>
              {/* An invisible copy of the "Army command" heading, so on wide screens the roster card's top
                  lines up with the command box beside it rather than with the heading */}
              <div className="roster-align" aria-hidden>
                <Title order={2} className="builder-heading">
                  &nbsp;
                </Title>
              </div>
              {/* Only the roster follows you down the page; the reference notes sit below the builder */}
              <div ref={stickyRef} style={{ position: "sticky", top: stickyTop }}>
                <RosterPanel
                  nation={nation}
                  roster={roster}
                  onRename={(armyName) => setRoster({ ...roster, armyName })}
                />
                <Text size="xs" c="dimmed" mt="xs" ta="center">
                  Saved as you go, in this browser on this device only.{" "}
                  <Anchor component={Link} href="/armies" inherit c="brown.7">
                    My armies
                  </Anchor>
                </Text>
              </div>
            </Grid.Col>
          </Grid>

          <div className="list-notes-wrap">
            <ForceOrgNotes nation={nation} />
          </div>
          <RosterBar nation={nation} roster={roster} />
        </Container>
      )}
    </>
  );
}
