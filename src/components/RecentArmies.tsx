"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Button, Stack, Text, Title } from "@mantine/core";
import { IconChevronRight, IconPlus } from "@tabler/icons-react";
import { getNation, getSupplement } from "@/data";
import { listHref, listSaved, LISTS_CHANGED_EVENT, type SavedList } from "@/lib/storage";
import { rosterTotal } from "@/lib/points";
import { edited } from "@/lib/edited";

const SHOWN = 3;

/**
 * The app home page's "Your armies": the armies most recently changed, to carry on with, and a button
 * to all of them in My armies; or, with none yet, a way to start the first. Loaded only in the app (see
 * AppHome), as it needs every army list to add up points.
 */
export default function RecentArmies() {
  // Null until read from the device after mount
  const [lists, setLists] = useState<SavedList[] | null>(null);

  useEffect(() => {
    const refresh = () => setLists(listSaved());
    refresh();
    window.addEventListener(LISTS_CHANGED_EVENT, refresh);
    window.addEventListener("storage", refresh);
    return () => {
      window.removeEventListener(LISTS_CHANGED_EVENT, refresh);
      window.removeEventListener("storage", refresh);
    };
  }, []);

  if (lists === null) return null;

  // Armies this build doesn't show are kept, just not listed (as in My armies)
  const shown = lists.flatMap((list) => {
    const nation = getNation(list.roster.nationId);
    const supplement = nation && getSupplement(nation.supplementId);
    return nation && supplement ? [{ list, nation, supplement }] : [];
  });

  return (
    <Stack gap="xs" component="section" aria-labelledby="app-home-armies">
      <Title order={2} id="app-home-armies" className="app-home-heading">
        Your armies
      </Title>

      {shown.length === 0 ? (
        <div className="app-list app-list-empty">
          <Text size="sm" c="dimmed" mb="sm">
            Armies save themselves on this device as you build them, and appear here.
          </Text>
          <Button component={Link} href="/black-powder" color="brown" leftSection={<IconPlus size={16} />}>
            Start your first army
          </Button>
        </div>
      ) : (
        <div className="app-list">
          {shown.slice(0, SHOWN).map(({ list, nation, supplement }) => {
            const flag = nation.flagFile ?? nation.flagFiles?.[0];
            const name = list.roster.armyName.trim();
            return (
              <Link key={list.id} href={listHref(supplement.id, nation.id, list.id)} className="app-list-row">
                {flag && (
                  <span className="army-flag app-list-flag">
                    <img src={flag} alt="" />
                  </span>
                )}
                <span className="app-list-text">
                  <Text ff="heading" fw={600} lh={1.25} c={name ? "brown.8" : "dimmed"} truncate>
                    {name || "Unnamed army"}
                  </Text>
                  <Text size="xs" c="dimmed" truncate>
                    {nation.name} · {edited(list.updatedAt)}
                  </Text>
                </span>
                <span className="app-list-points">{rosterTotal(nation, list.roster)} pts</span>
                <IconChevronRight size={18} className="app-list-chevron" aria-hidden />
              </Link>
            );
          })}
          {/* Every army, beyond the latest few, and where to copy or delete them: the list's last row */}
          <Link href="/armies" className="app-list-row app-list-more">
            <span className="app-list-text">View my armies</span>
            <IconChevronRight size={18} className="app-list-chevron" aria-hidden />
          </Link>
        </div>
      )}
    </Stack>
  );
}
