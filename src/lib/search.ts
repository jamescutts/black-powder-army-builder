// Site search: matching typed words against rule sets, supplements and army lists in the browser, and
// the armies saved on this device.

export type SearchKind = "army" | "rules" | "supplement" | "nation";

/** One searchable page: kind, title, description, address and other words that should find it */
export interface SearchEntry {
  k: SearchKind;
  t: string;
  d: string;
  h: string;
  x?: string;
}

interface Indexed extends SearchEntry {
  title: string;
  words: string[];
}

/** Lower case, without accents or punctuation, so "Württemberg" and "wurttemberg" match */
export const normalise = (s: string) =>
  s
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();

export function buildIndex(entries: SearchEntry[]): Indexed[] {
  return entries.map((e) => {
    const title = normalise(e.t);
    return { ...e, title, words: `${title} ${normalise(e.x ?? "")}`.split(" ").filter(Boolean) };
  });
}

// Your own armies first when they match equally well, as they're most likely what you're after; then rule
// sets before supplements before army lists, as there are far fewer of them
const KIND_ORDER: Record<SearchKind, number> = { army: 0, rules: 1, supplement: 2, nation: 3 };

/** Entries where every typed word starts a word in the title or other words, best matches first */
export function search(index: Indexed[], query: string, limit = 12): SearchEntry[] {
  const q = normalise(query);
  if (!q) return [];
  const tokens = q.split(" ");
  const scored: { e: Indexed; score: number }[] = [];
  for (const e of index) {
    if (!tokens.every((t) => e.words.some((w) => w.startsWith(t)))) continue;
    // Best: the title is the query or starts with it; then every word is in the title; then other words
    const titleWords = e.title.split(" ");
    const score =
      e.title === q
        ? 0
        : ` ${e.title}`.includes(` ${q}`) // the query as a phrase starting a word of the title
          ? 1
          : tokens.every((t) => titleWords.some((w) => w.startsWith(t)))
            ? 2
            : 3;
    scored.push({ e, score });
  }
  // Then shorter titles first, except your armies, which keep the order they came in (newest first)
  scored.sort(
    (a, b) =>
      a.score - b.score ||
      KIND_ORDER[a.e.k] - KIND_ORDER[b.e.k] ||
      (a.e.k === "army" ? 0 : a.e.t.length - b.e.t.length)
  );
  return scored.slice(0, limit).map((s) => s.e);
}
