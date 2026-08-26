import type { Nation, Supplement } from "./types";

// --- A Clash of Eagles (Black Powder, Russia 1812) ---
// Nation JSON files carry no id back to their supplement — that link comes purely from folder
// placement (src/data/supplements/<supplement-id>/nations/*.json) and the grouping below.
import clashOfEaglesSupplement from "./supplements/clash-of-eagles/supplement.json";
import coeRussia from "./supplements/clash-of-eagles/nations/russia.json";
import coeFrance from "./supplements/clash-of-eagles/nations/france.json";
import coeFrenchImperialGuard from "./supplements/clash-of-eagles/nations/french-imperial-guard.json";
import coeVistulaLegion from "./supplements/clash-of-eagles/nations/vistula-legion.json";
import coeGrandDuchyOfWarsaw from "./supplements/clash-of-eagles/nations/grand-duchy-of-warsaw.json";
import coeConfederationOfTheRhine from "./supplements/clash-of-eagles/nations/confederation-of-the-rhine.json";
import coeAustria from "./supplements/clash-of-eagles/nations/austria.json";
import coeItaly from "./supplements/clash-of-eagles/nations/italy.json";
import coeNaples from "./supplements/clash-of-eagles/nations/naples.json";
import coePrussia from "./supplements/clash-of-eagles/nations/prussia.json";

// --- Albion Triumphant: The Peninsular Campaign ---
import albionTriumphant1Supplement from "./supplements/albion-triumphant-1/supplement.json";
import at1PeninsularBritish from "./supplements/albion-triumphant-1/nations/peninsular-british.json";
import at1PeninsularFrench from "./supplements/albion-triumphant-1/nations/peninsular-french.json";
import at1Spanish from "./supplements/albion-triumphant-1/nations/spanish.json";

// --- Albion Triumphant: The Hundred Days ---
import albionTriumphant2Supplement from "./supplements/albion-triumphant-2/supplement.json";
import at2AngloNetherlandsBritish from "./supplements/albion-triumphant-2/nations/anglo-netherlands-british.json";
import at2Brunswick from "./supplements/albion-triumphant-2/nations/brunswick.json";
import at2DutchBelgianNassau from "./supplements/albion-triumphant-2/nations/dutch-belgian-nassau.json";
import at2FrenchArmyCorps from "./supplements/albion-triumphant-2/nations/french-army-corps.json";
import at2FrenchImperialGuard from "./supplements/albion-triumphant-2/nations/french-imperial-guard-1815.json";
import at2Prussians from "./supplements/albion-triumphant-2/nations/prussians-1815.json";

type NationSource = Omit<Nation, "supplementId">;

function withSupplement(supplementId: string, list: NationSource[]): Nation[] {
  return list.map((n) => ({ ...n, supplementId }));
}

/**
 * To add a new supplement:
 * 1. Create src/data/supplements/<supplement-id>/supplement.json ({ id, name, blurb })
 * 2. Create src/data/supplements/<supplement-id>/nations/<nation-id>.json for each army list
 *    (no supplement reference needed inside the file — the folder is the source of truth)
 * 3. Import the supplement.json and each nation file here, then add a `withSupplement(...)`
 *    block below and append its result to `nations`.
 */

export const supplements: Supplement[] = [
  clashOfEaglesSupplement as Supplement,
  albionTriumphant1Supplement as Supplement,
  albionTriumphant2Supplement as Supplement,
];

const clashOfEaglesNations = withSupplement("clash-of-eagles", [
  coeRussia,
  coeFrance,
  coeFrenchImperialGuard,
  coeVistulaLegion,
  coeGrandDuchyOfWarsaw,
  coeConfederationOfTheRhine,
  coeAustria,
  coeItaly,
  coeNaples,
  coePrussia,
] as NationSource[]);

const albionTriumphant1Nations = withSupplement("albion-triumphant-1", [
  at1PeninsularBritish,
  at1PeninsularFrench,
  at1Spanish,
] as NationSource[]);

const albionTriumphant2Nations = withSupplement("albion-triumphant-2", [
  at2AngloNetherlandsBritish,
  at2Brunswick,
  at2DutchBelgianNassau,
  at2FrenchArmyCorps,
  at2FrenchImperialGuard,
  at2Prussians,
] as NationSource[]);

export const nations: Nation[] = [
  ...clashOfEaglesNations,
  ...albionTriumphant1Nations,
  ...albionTriumphant2Nations,
];

export function getSupplement(id: string): Supplement | undefined {
  return supplements.find((s) => s.id === id);
}

export function getNation(id: string): Nation | undefined {
  return nations.find((n) => n.id === id);
}

export function getNationsForSupplement(supplementId: string): Nation[] {
  return nations.filter((n) => n.supplementId === supplementId);
}
