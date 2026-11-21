"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Badge, Group, Kbd, Loader, Modal, Stack, Text, TextInput, UnstyledButton } from "@mantine/core";
import { buildIndex, search, type SearchEntry, type SearchKind } from "@/lib/search";
import { listHref, listSaved, LISTS_CHANGED_EVENT, type SavedList } from "@/lib/storage";
import { edited } from "@/lib/edited";

const KIND_LABEL: Record<SearchKind, string> = {
  army: "Your army",
  rules: "Rules",
  supplement: "Supplement",
  nation: "Army list",
  historical: "Historical",
};

// Each kind of result in its own colour, so they're told apart at a glance: your own armies solid, the
// rest light
const KIND_BADGE: Record<SearchKind, { variant: "filled" | "light"; color: string }> = {
  army: { variant: "filled", color: "brown.7" },
  nation: { variant: "light", color: "brown" },
  supplement: { variant: "light", color: "yellow" },
  rules: { variant: "light", color: "green" },
  historical: { variant: "light", color: "blue" },
};

// Fetched once per visit, the first time search opens
let indexPromise: Promise<ReturnType<typeof buildIndex>> | null = null;
const loadIndex = () =>
  (indexPromise ??= fetch("/search-index.json")
    .then((r) => r.json() as Promise<SearchEntry[]>)
    .then(buildIndex)
    .catch((e) => {
      indexPromise = null;
      throw e;
    }));

function MagnifierIcon() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.2"
      strokeLinecap="round"
      aria-hidden
    >
      <circle cx="11" cy="11" r="7" />
      <path d="m20 20-3.5-3.5" />
    </svg>
  );
}

/** How many of your latest armies show before anything is typed */
const RECENT = 5;

/**
 * Your saved armies as search entries, each found by its name and its army list's and book's. They're
 * described with the army list from the search data (the header doesn't carry the lists themselves), so
 * one whose list isn't in the data (a community list that's switched off) is left out, as in My armies.
 */
function savedEntries(lists: SavedList[], nations: SearchEntry[]): SearchEntry[] {
  return lists.flatMap((list) => {
    const nation = nations.find((n) => n.h.endsWith(`/${list.roster.nationId}`));
    if (!nation) return [];
    const [, , supplementId, nationId] = nation.h.split("/");
    return [
      {
        k: "army",
        t: list.roster.armyName.trim() || "Unnamed army",
        d: `${nation.t} · ${edited(list.updatedAt)}`,
        h: listHref(supplementId, nationId, list.id),
        x: `${nation.t} ${nation.d}`,
      },
    ];
  });
}

/**
 * A search button for the header; opens a box that finds your saved armies, rule sets, supplements and
 * army lists as you type, and shows your latest armies before you do
 */
export function SiteSearch() {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [index, setIndex] = useState<ReturnType<typeof buildIndex> | null>(null);
  const [failed, setFailed] = useState(false);
  const [active, setActive] = useState(0);
  const listRef = useRef<HTMLDivElement>(null);
  // Your saved armies, read from the device each time search opens (and kept up to date while it's open)
  const [saved, setSaved] = useState<SavedList[]>([]);

  // "/" or Ctrl/⌘+K opens search from anywhere, unless typing in a field
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const typing =
        e.target instanceof HTMLElement &&
        (e.target.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName));
      if ((e.key === "k" && (e.metaKey || e.ctrlKey)) || (e.key === "/" && !typing)) {
        e.preventDefault();
        setOpen(true);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  useEffect(() => {
    if (!open || index) return;
    setFailed(false);
    loadIndex().then(setIndex, () => setFailed(true));
  }, [open, index]);

  useEffect(() => {
    if (!open) return;
    const refresh = () => setSaved(listSaved());
    refresh();
    window.addEventListener(LISTS_CHANGED_EVENT, refresh);
    return () => window.removeEventListener(LISTS_CHANGED_EVENT, refresh);
  }, [open]);

  const armies = useMemo(
    () => (index ? savedEntries(saved, index.filter((e) => e.k === "nation")) : []),
    [index, saved]
  );
  const everything = useMemo(() => (index ? [...buildIndex(armies), ...index] : []), [index, armies]);
  // Before anything's typed, your latest armies (newest first, as listSaved gives them)
  const results = useMemo(
    () => (query.trim() ? search(everything, query) : armies.slice(0, RECENT)),
    [everything, armies, query]
  );
  useEffect(() => setActive(0), [query]);

  // Keep the highlighted result in view as the arrow keys move it
  useEffect(() => {
    listRef.current?.querySelector(`[data-index="${active}"]`)?.scrollIntoView({ block: "nearest" });
  }, [active]);

  const close = () => {
    setOpen(false);
    setQuery("");
  };
  const go = (e: SearchEntry) => {
    close();
    router.push(e.h);
  };

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (!results.length) return;
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive((a) => (a + 1) % results.length);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive((a) => (a - 1 + results.length) % results.length);
    } else if (e.key === "Enter") {
      e.preventDefault();
      go(results[active]);
    }
  };

  return (
    <>
      <UnstyledButton
        className="site-search-button"
        onClick={() => setOpen(true)}
        aria-label="Search your armies, rule sets, supplements and army lists"
      >
        <MagnifierIcon />
        <Text span size="sm" visibleFrom="sm">
          Search
        </Text>
        {/* The "/" shortcut's hint: a website convention, so not in the installed app */}
        <Kbd size="xs" visibleFrom="md" className="site-search-kbd app-hidden">
          /
        </Kbd>
      </UnstyledButton>

      <Modal
        opened={open}
        onClose={close}
        withCloseButton={false}
        padding={0}
        size="lg"
        yOffset="10vh"
        radius="md"
        title={null}
        aria-label="Search"
        zIndex={1200}
      >
        <TextInput
          data-autofocus
          size="md"
          variant="unstyled"
          px="md"
          py={6}
          placeholder="Search your armies, rule sets and army lists"
          value={query}
          onChange={(e) => setQuery(e.currentTarget.value)}
          onKeyDown={onKeyDown}
          leftSection={<MagnifierIcon />}
          rightSection={!index && !failed ? <Loader size="xs" color="brown" /> : undefined}
          aria-controls="site-search-results"
          aria-activedescendant={results.length ? `site-search-${active}` : undefined}
          className="site-search-input"
        />
        <div ref={listRef} id="site-search-results" role="listbox" className="site-search-results">
          {failed && (
            <Text size="sm" c="dimmed" p="md">
              Search couldn&apos;t load. Check your connection and try again.
            </Text>
          )}
          {index && query.trim() && results.length === 0 && (
            <Text size="sm" c="dimmed" p="md">
              Nothing found for &ldquo;{query.trim()}&rdquo;.
            </Text>
          )}
          {!query.trim() && (
            <Text size="sm" c="dimmed" p="md" pb={results.length ? "xs" : "md"}>
              Type one of your armies&apos; names, or a rule set, supplement or army list, e.g. Black Powder,
              Hundred Days or Prussia.
            </Text>
          )}
          {!query.trim() && results.length > 0 && (
            <Text size="xs" fw={600} c="dimmed" tt="uppercase" px="md" pb={4} className="site-search-group">
              Your latest armies
            </Text>
          )}
          {results.map((r, i) => (
            <UnstyledButton
              key={r.h}
              id={`site-search-${i}`}
              data-index={i}
              role="option"
              aria-selected={i === active}
              className="site-search-result"
              data-active={i === active || undefined}
              onMouseEnter={() => setActive(i)}
              onClick={() => go(r)}
            >
              <Group gap="sm" wrap="nowrap" align="flex-start">
                <Badge
                  size="xs"
                  variant={KIND_BADGE[r.k].variant}
                  color={KIND_BADGE[r.k].color}
                  w={78}
                  mt={3}
                  style={{ flexShrink: 0 }}
                >
                  {KIND_LABEL[r.k]}
                </Badge>
                <Stack gap={0} style={{ minWidth: 0 }}>
                  <Text size="sm" fw={600} truncate>
                    {r.t}
                  </Text>
                  <Text size="xs" c="dimmed" truncate>
                    {r.d}
                  </Text>
                </Stack>
              </Group>
            </UnstyledButton>
          ))}
        </div>
      </Modal>
    </>
  );
}
