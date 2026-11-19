// Site search: matching typed words against rule sets, supplements and army lists in the browser.

export type SearchKind = "rules" | "supplement" | "nation";

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

// Rule sets before supplements before army lists when they match equally well: there are far fewer of them
const KIND_ORDER: Record<SearchKind, number> = { rules: 0, supplement: 1, nation: 2 };

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
  scored.sort((a, b) => a.score - b.score || KIND_ORDER[a.e.k] - KIND_ORDER[b.e.k] || a.e.t.length - b.e.t.length);
  return scored.slice(0, limit).map((s) => s.e);
}
