import type { HistoricalBattle, HistoricalCampaign, HistoricalForce } from "../types";
import { getNation } from "../index";
import eckau from "./eckau.json";
import ligny from "./ligny.json";
import mesoten from "./mesoten.json";
import quatreBras from "./quatre-bras.json";
import waterloo from "./waterloo.json";
import wavre from "./wavre.json";
import {
  albuera,
  bailen,
  berezina,
  borodino,
  bussaco,
  corunna,
  dahlenkirchen,
  fuentesDeOnoro,
  gorodechno,
  klyastitsy,
  krasnoi,
  maloyaroslavets,
  medinaDeRioseco,
  mir,
  nivelle,
  ocana,
  orthez,
  ostrovno,
  polotsk,
  polotsk2,
  rolica,
  salamanca,
  saltanovka,
  smolensk,
  somosierra,
  sorauren,
  talavera,
  tarutino,
  toulouse,
  valutino,
  vimeiro,
  vitoria,
  vyazma,
} from "./planned";

/**
 * Campaigns, in the order they were fought, each with its battles in order, whose historical forces can be opened
 * as new lists. To add a battle, write src/data/battles/<battle-id>.json (a HistoricalBattle naming its
 * campaign's id) and import it here. Run `npm run check:forces` to see that every force builds and what
 * it breaks of its list's rules.
 */
export const campaigns: HistoricalCampaign[] = [
  // Still to come: shown as a card of its own, with no page until it has battles
  {
    id: "peninsular-war",
    name: "The Peninsular War",
    dates: "1808–1814",
    art: {
      src: "https://upload.wikimedia.org/wikipedia/commons/b/b6/Battle_of_Albuhera%2C_by_William_Barnes_Wollen.jpg",
      title: "The Flag, Albuhera, 16 May 1811",
      artist: "William Barnes Wollen",
      date: "c. 1912",
      page: "https://commons.wikimedia.org/wiki/File:Battle_of_Albuhera,_by_William_Barnes_Wollen.jpg",
    },
    summary:
      "Six years of war in Spain and Portugal, as Wellington's British and Portuguese army, the Spanish and the guerrillas fought the French armies across the Peninsula, from Vimeiro and Talavera to Salamanca and Vitoria.",
  },
  {
    id: "russia-1812",
    name: "The Russian Campaign",
    dates: "June–December 1812",
    art: {
      src: "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0a/De_overtocht_over_de_Berezina.jpg/960px-De_overtocht_over_de_Berezina.jpg",
      title: "The Crossing of the Berezina",
      artist: "Jan Hoynck van Papendrecht",
      date: "1908–09",
      page: "https://commons.wikimedia.org/wiki/File:De_overtocht_over_de_Berezina.jpg",
    },
    summary:
      "Napoleon's invasion of Russia with the largest army Europe had seen. On its northern flank Macdonald's X Corps, with the Prussian Auxiliary Corps, marched on Riga, and spent the summer and autumn fighting its garrison and Steinheil's corps from Finland across Courland, until Yorck took the Prussians out of the war at Tauroggen.",
  },
  {
    id: "hundred-days",
    name: "The Hundred Days",
    dates: "June 1815",
    art: {
      src: "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1e/1815-06-18_Adolph_Northen_oil_on_canvas_Die_Verteidigung_des_Meierhofes_La_Haye_Sainte_bei_Waterloo%2C_Historisches_Museum_Hannover.webp/960px-1815-06-18_Adolph_Northen_oil_on_canvas_Die_Verteidigung_des_Meierhofes_La_Haye_Sainte_bei_Waterloo%2C_Historisches_Museum_Hannover.webp",
      title: "The Defence of La Haye Sainte",
      artist: "Adolph Northen",
      page: "https://commons.wikimedia.org/wiki/File:1815-06-18_Adolph_Northen_oil_on_canvas_Die_Verteidigung_des_Meierhofes_La_Haye_Sainte_bei_Waterloo,_Historisches_Museum_Hannover.webp",
    },
    summary:
      "Napoleon's return from Elba ended in four days in Belgium. He struck between Wellington's Anglo-allied army and Blücher's Prussians, beating the Prussians at Ligny while Ney held Wellington at Quatre Bras; two days later the allies joined to defeat him at Waterloo, while Grouchy fought the Prussian rearguard at Wavre.",
  },
];

// Every battle, in the order fought: those with forces written, and those still to come (planned.ts)
const schedule: HistoricalBattle[] = [
  // The Peninsular War
  medinaDeRioseco,
  bailen,
  rolica,
  vimeiro,
  somosierra,
  corunna,
  talavera,
  ocana,
  bussaco,
  fuentesDeOnoro,
  albuera,
  salamanca,
  vitoria,
  sorauren,
  nivelle,
  orthez,
  toulouse,
  // The Russian Campaign
  mir,
  eckau as HistoricalBattle,
  saltanovka,
  ostrovno,
  klyastitsy,
  gorodechno,
  smolensk,
  polotsk,
  valutino,
  dahlenkirchen,
  borodino,
  mesoten as HistoricalBattle,
  tarutino,
  polotsk2,
  maloyaroslavets,
  vyazma,
  krasnoi,
  berezina,
  // The Hundred Days
  ligny as HistoricalBattle,
  quatreBras as HistoricalBattle,
  waterloo as HistoricalBattle,
  wavre as HistoricalBattle,
];

// Only the forces whose army lists this build shows (community lists can be switched off)
const shown = schedule.map((b) => ({ ...b, forces: b.forces.filter((f) => getNation(f.nationId)) }));

/** The battles with forces to open, each with a page of its own */
export const battles: HistoricalBattle[] = shown.filter((b) => b.forces.length > 0);

/** A campaign's battles in order, those still to come (with no forces yet) among them */
export function scheduleIn(campaignId: string): HistoricalBattle[] {
  return shown.filter((b) => b.campaign === campaignId);
}

/** A battle still to come: in its campaign's list, without forces or a page yet */
export function isPlanned(battle: HistoricalBattle): boolean {
  return battle.forces.length === 0;
}

export function getCampaign(id: string): HistoricalCampaign | undefined {
  return campaigns.find((c) => c.id === id);
}

/** The campaigns with battles to list, forces or not, each with a page of its own; the rest are still to come */
export function campaignsWithBattles(): HistoricalCampaign[] {
  return campaigns.filter((c) => scheduleIn(c.id).length > 0);
}

/** A campaign's battles, in the order they were fought */
export function battlesIn(campaignId: string): HistoricalBattle[] {
  return battles.filter((b) => b.campaign === campaignId);
}

/** A campaign's battle, or undefined when it has no such battle */
export function getBattle(campaignId: string, battleId: string): HistoricalBattle | undefined {
  return battlesIn(campaignId).find((b) => b.id === battleId);
}

export function getForce(id: string): HistoricalForce | undefined {
  for (const b of battles) {
    const force = b.forces.find((f) => f.id === id);
    if (force) return force;
  }
  return undefined;
}

export function battleOf(forceId: string): HistoricalBattle | undefined {
  return battles.find((b) => b.forces.some((f) => f.id === forceId));
}

/** One army list's historical forces, with their battles */
export function forcesFor(nationId: string): { battle: HistoricalBattle; force: HistoricalForce }[] {
  return battles.flatMap((battle) =>
    battle.forces.filter((f) => f.nationId === nationId).map((force) => ({ battle, force }))
  );
}
