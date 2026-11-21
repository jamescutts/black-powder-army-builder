"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ActionIcon, Alert, Badge, Button, Card, Container, Group, Menu, SimpleGrid, Stack, Text, Title } from "@mantine/core";
import { IconArrowRight, IconCopy, IconDeviceDesktop, IconDots, IconPlus, IconTrash } from "@tabler/icons-react";
import { getNation, getSupplement } from "@/data";
import { deleteList, duplicateList, listHref, listSaved, LISTS_CHANGED_EVENT, type SavedList } from "@/lib/storage";
import { rosterTotal, unitCount } from "@/lib/points";
import { ConfirmModal } from "@/components/ConfirmModal";
import { edited } from "@/lib/edited";

const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;

/**
 * Every army list saved in this browser, most recently changed first, to open, copy or delete. Lists live
 * only in this browser (lib/storage.ts), so the page says so first.
 */
export function MyArmies() {
  // Null until read from the browser after mount, so the server's page and the first render agree
  const [lists, setLists] = useState<SavedList[] | null>(null);
  const [deleting, setDeleting] = useState<SavedList | null>(null);

  useEffect(() => {
    const refresh = () => setLists(listSaved());
    refresh();
    // Kept up to date when lists change here or in another tab
    window.addEventListener(LISTS_CHANGED_EVENT, refresh);
    window.addEventListener("storage", refresh);
    return () => {
      window.removeEventListener(LISTS_CHANGED_EVENT, refresh);
      window.removeEventListener("storage", refresh);
    };
  }, []);

  // Lists for armies this build doesn't show (such as community lists, when they're switched off) are
  // kept, just not listed
  const shown = (lists ?? []).flatMap((list) => {
    const nation = getNation(list.roster.nationId);
    const supplement = nation && getSupplement(nation.supplementId);
    return nation && supplement ? [{ list, nation, supplement }] : [];
  });

  return (
    <Container size="xl" py="lg">
      <ConfirmModal
        opened={!!deleting}
        title="Delete this list?"
        confirmLabel="Delete list"
        onConfirm={() => {
          if (deleting) deleteList(deleting.id);
          setDeleting(null);
        }}
        onCancel={() => setDeleting(null)}
      >
        This deletes {deleting?.roster.armyName.trim() || "this army"} from this browser. It can&apos;t be undone.
      </ConfirmModal>

      <Stack gap="lg">
        <Group justify="space-between" align="flex-end" gap="md">
          <Stack gap={4}>
            <Title order={1} className="army-title">
              My armies
            </Title>
            <Text size="sm" c="dimmed">
              Every army you&apos;ve built, most recently changed first.
            </Text>
          </Stack>
          <Button component={Link} href="/black-powder" color="brown" leftSection={<IconPlus size={16} />}>
            New army
          </Button>
        </Group>

        <Alert
          color="yellow"
          variant="light"
          icon={<IconDeviceDesktop size={20} />}
          title="Saved in this browser only"
          className="saved-here-note"
        >
          <Text size="sm" style={{ lineHeight: 1.55 }}>
            Your armies are kept in this browser, on this device. They won&apos;t appear on your phone, another
            computer or another browser, and clearing this browser&apos;s history and site data deletes them. An
            installed copy of Army Builder keeps its own armies, separate from the browser&apos;s. To keep an army
            safe, print it or download it as a PDF.
          </Text>
        </Alert>

        {lists !== null && shown.length === 0 && (
          <Card withBorder radius="md" padding="xl">
            <Stack gap="sm" align="center" ta="center">
              <Text ff="heading" fw={600} fz="lg" c="brown.8">
                No saved armies yet
              </Text>
              <Text size="sm" c="dimmed" maw={420}>
                Armies save themselves as you build them, and appear here.
              </Text>
              <Button component={Link} href="/black-powder" color="brown" rightSection={<IconArrowRight size={16} />}>
                Start a Black Powder army
              </Button>
            </Stack>
          </Card>
        )}

        {shown.length > 0 && (
          <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="md">
            {shown.map(({ list, nation, supplement }) => {
              const flag = nation.flagFile ?? nation.flagFiles?.[0];
              const name = list.roster.armyName.trim();
              const href = listHref(supplement.id, nation.id, list.id);
              return (
                <Card key={list.id} withBorder radius="md" padding="md" className="picker-card saved-list-card">
                  <Group justify="space-between" align="flex-start" wrap="nowrap" gap="sm">
                    <Group gap="sm" wrap="nowrap" align="flex-start" style={{ minWidth: 0 }}>
                      {flag && (
                        <span className="army-flag saved-list-flag">
                          <img src={flag} alt="" />
                        </span>
                      )}
                      <Stack gap={2} style={{ minWidth: 0 }}>
                        {/* The card's link: it covers the whole card (see .saved-list-link) */}
                        <Link href={href} className="saved-list-link">
                          <Text ff="heading" fw={600} fz="lg" lh={1.25} c={name ? "brown.8" : "dimmed"} truncate>
                            {name || "Unnamed army"}
                          </Text>
                        </Link>
                        <Text size="sm" lh={1.35}>
                          {nation.name}
                        </Text>
                        <Text size="xs" c="dimmed">
                          {supplement.name}
                        </Text>
                      </Stack>
                    </Group>
                    <Menu position="bottom-end" shadow="md" width={180}>
                      <Menu.Target>
                        <ActionIcon variant="subtle" color="gray" className="saved-list-menu" aria-label={`Options for ${name || "this army"}`}>
                          <IconDots size={18} />
                        </ActionIcon>
                      </Menu.Target>
                      <Menu.Dropdown>
                        <Menu.Item leftSection={<IconCopy size={16} />} onClick={() => duplicateList(list.id)}>
                          Duplicate
                        </Menu.Item>
                        <Menu.Item color="red" leftSection={<IconTrash size={16} />} onClick={() => setDeleting(list)}>
                          Delete
                        </Menu.Item>
                      </Menu.Dropdown>
                    </Menu>
                  </Group>

                  <Group justify="space-between" align="center" mt="md" gap="xs">
                    <Text size="xs" c="dimmed">
                      {plural(unitCount(list.roster), "unit", "units")} ·{" "}
                      {plural(list.roster.brigadeInstances.length, "brigade", "brigades")} · {edited(list.updatedAt)}
                    </Text>
                    <Badge color="brown" variant="filled" size="lg">
                      {rosterTotal(nation, list.roster)} pts
                    </Badge>
                  </Group>
                </Card>
              );
            })}
          </SimpleGrid>
        )}
      </Stack>
    </Container>
  );
}
