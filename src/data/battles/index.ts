import type { HistoricalBattle, HistoricalCampaign, HistoricalForce } from "../types";
import { getNation } from "../index";
import albuera from "./albuera.json";
import bailen from "./bailen.json";
import bussaco from "./bussaco.json";
import corunna from "./corunna.json";
import dahlenkirchen from "./dahlenkirchen.json";
import eckau from "./eckau.json";
import fuentesDeOnoro from "./fuentes-de-onoro.json";
import gorodechno from "./gorodechno.json";
import klyastitsy from "./klyastitsy.json";
import kobrin from "./kobrin.json";
import ligny from "./ligny.json";
import medinaDeRioseco from "./medina-de-rioseco.json";
import mesoten from "./mesoten.json";
import mir from "./mir.json";
import polotsk from "./polotsk.json";
import polotsk2 from "./polotsk-2.json";
import quatreBras from "./quatre-bras.json";
import orthez from "./orthez.json";
import ostrovno from "./ostrovno.json";
import rolica from "./rolica.json";
import romanov from "./romanov.json";
import salamanca from "./salamanca.json";
import sorauren from "./sorauren.json";
import saltanovka from "./saltanovka.json";
import talavera from "./talavera.json";
import valutino from "./valutino.json";
import vimeiro from "./vimeiro.json";
import vitoria from "./vitoria.json";
import waterloo from "./waterloo.json";
import wavre from "./wavre.json";
import {
  berezina,
  borodino,
  krasnoi,
  maloyaroslavets,
  nivelle,
  ocana,
  smolensk,
  somosierra,
  tarutino,
  toulouse,
  vyazma,
  almeida,
  arcis,
  badajoz,
  bautzen,
  brienne,
  chateauThierry,
  champaubert,
  craonne,
  dennewitz,
  dresden,
  fereChampenoise,
  gohrde,
  grossbeeren,
  hanau,
  katzbach,
  kulm,
  laon,
  laRothiere,
  leipzig,
  lutzen,
  montereau,
  montmirail,
  paris,
  reims,
  vauchamps,
  wartenburg,
  burgos,
  ciudadRodrigo,
  gerona,
  pamplona,
  sanSebastian,
  saragossa,
  saragossa2,
  tarragona,
  danzig,
  luneburg,
  mockern,
  rippach,
  reichenbach,
  haynau,
  luckau,
  kitzen,
  lowenberg,
  goldberg,
  hagelberg,
  plagwitz,
  altenburg,
  liebertwolkwitz,
  mockernLeipzig,
  torgau,
  hamburg,
  sehested,
  mormant,
  barSurAube,
  laubressel,
  soissons,
  limonest,
  saintDizier,
} from "./planned";

/**
 * Campaigns, in the order they were fought, each with its battles in order, whose historical forces can be opened
 * as new lists. To add a battle, write src/data/battles/<battle-id>.json (a HistoricalBattle naming its
 * campaign's id) and import it here. Run `npm run check:forces` to see that every force builds and what
 * it breaks of its list's rules.
 */
const allCampaigns: HistoricalCampaign[] = [
  // Still to come: shown as a card of its own, with no page until it has battles
  {
    id: "peninsular-war",
    name: "The Peninsular War",
    dates: "1808–1814",
    art: {
      src: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Louis-Fran%C3%A7ois_Lejeune_-_Battle_of_Somosierra%2C_November_30%2C_1808.jpg/960px-Louis-Fran%C3%A7ois_Lejeune_-_Battle_of_Somosierra%2C_November_30%2C_1808.jpg",
      title: "The Battle of Somosierra",
      artist: "Louis-François Lejeune",
      date: "1810",
      page: "https://commons.wikimedia.org/wiki/File:Louis-Fran%C3%A7ois_Lejeune_-_Battle_of_Somosierra,_November_30,_1808.jpg",
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
      "Napoleon crossed the Niemen in June with the largest army Europe had seen, drawn from France and half the continent. The Russian armies fell back before it, fighting rearguard actions from Mir and Ostrovno to Smolensk, until Kutuzov stood at Borodino. Napoleon took Moscow but not the peace he sought, and the retreat through the winter, harried at Maloyaroslavets, Vyazma and Krasnoi and across the Berezina, destroyed his army, while on the flanks Austrians, Saxons and Prussians fought campaigns of their own.",
  },
  {
    id: "liberation-1813",
    name: "The War of Liberation",
    dates: "1813",
    art: {
      src: "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/8b/Declaration_of_victory_after_the_Battle_of_Leipzig%2C_1813_%28by_Johann_Peter_Krafft%29.jpg/960px-Declaration_of_victory_after_the_Battle_of_Leipzig%2C_1813_%28by_Johann_Peter_Krafft%29.jpg",
      title: "The Declaration of Victory after the Battle of Leipzig",
      artist: "Johann Peter Krafft",
      date: "1839",
      page: "https://commons.wikimedia.org/wiki/File:Declaration_of_victory_after_the_Battle_of_Leipzig,_1813_(by_Johann_Peter_Krafft).jpg",
    },
    summary:
      "With the Grande Armée lost in Russia, Prussia rose and joined the Tsar. Napoleon came back into Saxony with a new army of conscripts and beat the allies at Lützen and Bautzen, then agreed an armistice that brought Austria and Sweden in against him. In the autumn his marshals were beaten in turn at Großbeeren, the Katzbach, Kulm and Dennewitz while he won at Dresden, until the allied armies closed on him at Leipzig; Bavaria changed sides, and he fought his way home through Hanau to the Rhine, leaving garrisons besieged behind him from Danzig to Hamburg.",
  },
  {
    id: "france-1814",
    name: "The Campaign in France",
    dates: "January–March 1814",
    art: {
      src: "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5e/Jean-Louis-Ernest_Meissonier-Campagne_de_France.jpg/960px-Jean-Louis-Ernest_Meissonier-Campagne_de_France.jpg",
      title: "1814, Campagne de France",
      artist: "Ernest Meissonier",
      date: "1864",
      page: "https://commons.wikimedia.org/wiki/File:Jean-Louis-Ernest_Meissonier-Campagne_de_France.jpg",
    },
    summary:
      "The allies crossed the Rhine in the winter and marched on Paris in two armies, Blücher's along the Marne and Schwarzenberg's along the Seine. Beaten at La Rothière, Napoleon turned on them with a small army of veterans, conscripts and National Guards, and in the Six Days of February broke Blücher's corps one by one at Champaubert, Montmirail, Château-Thierry and Vauchamps, then threw Schwarzenberg back at Montereau. But Craonne, Laon and Arcis-sur-Aube wore him down, and when the allies marched past him on Paris the city fell, and he abdicated at Fontainebleau.",
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

export const campaigns: HistoricalCampaign[] = allCampaigns;

// Every battle, in the order fought: those with forces written, and those still to come (planned.ts)
const allBattles: HistoricalBattle[] = [
  // The Peninsular War
  saragossa,
  medinaDeRioseco as HistoricalBattle,
  bailen as HistoricalBattle,
  rolica as HistoricalBattle,
  vimeiro as HistoricalBattle,
  somosierra,
  saragossa2,
  corunna as HistoricalBattle,
  gerona,
  talavera as HistoricalBattle,
  ocana,
  almeida,
  bussaco as HistoricalBattle,
  fuentesDeOnoro as HistoricalBattle,
  tarragona,
  albuera as HistoricalBattle,
  ciudadRodrigo,
  badajoz,
  salamanca as HistoricalBattle,
  burgos,
  vitoria as HistoricalBattle,
  pamplona,
  sanSebastian,
  sorauren as HistoricalBattle,
  nivelle,
  orthez as HistoricalBattle,
  toulouse,
  // The Russian Campaign
  mir as HistoricalBattle,
  romanov as HistoricalBattle,
  eckau as HistoricalBattle,
  saltanovka as HistoricalBattle,
  ostrovno as HistoricalBattle,
  kobrin as HistoricalBattle,
  klyastitsy as HistoricalBattle,
  gorodechno as HistoricalBattle,
  smolensk,
  polotsk as HistoricalBattle,
  valutino as HistoricalBattle,
  dahlenkirchen as HistoricalBattle,
  borodino,
  mesoten as HistoricalBattle,
  tarutino,
  polotsk2 as HistoricalBattle,
  maloyaroslavets,
  vyazma,
  krasnoi,
  berezina,
  // The War of Liberation
  danzig,
  luneburg,
  mockern,
  rippach,
  lutzen,
  bautzen,
  reichenbach,
  haynau,
  luckau,
  kitzen,
  lowenberg,
  grossbeeren,
  goldberg,
  katzbach,
  dresden,
  hagelberg,
  plagwitz,
  kulm,
  dennewitz,
  gohrde,
  altenburg,
  wartenburg,
  liebertwolkwitz,
  mockernLeipzig,
  leipzig,
  torgau,
  hanau,
  hamburg,
  sehested,
  // The Campaign in France
  brienne,
  laRothiere,
  champaubert,
  montmirail,
  chateauThierry,
  vauchamps,
  mormant,
  montereau,
  barSurAube,
  laubressel,
  soissons,
  craonne,
  laon,
  reims,
  limonest,
  arcis,
  fereChampenoise,
  saintDizier,
  paris,
  // The Hundred Days
  ligny as HistoricalBattle,
  quatreBras as HistoricalBattle,
  waterloo as HistoricalBattle,
  wavre as HistoricalBattle,
];

const schedule = allBattles;

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
