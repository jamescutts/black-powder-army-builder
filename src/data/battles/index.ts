import type { HistoricalBattle, HistoricalCampaign, HistoricalForce } from "../types";
import { getNation } from "../index";
import campaignCommanders from "./campaign-commanders.json";
import albuera from "./albuera.json";
import bailen from "./bailen.json";
import berezina from "./berezina.json";
import borodino from "./borodino.json";
import bussaco from "./bussaco.json";
import corunna from "./corunna.json";
import dahlenkirchen from "./dahlenkirchen.json";
import eckau from "./eckau.json";
import fuentesDeOnoro from "./fuentes-de-onoro.json";
import gorodechno from "./gorodechno.json";
import klyastitsy from "./klyastitsy.json";
import krasnoi from "./krasnoi.json";
import kobrin from "./kobrin.json";
import bautzen from "./bautzen.json";
import grossbeeren from "./grossbeeren.json";
import wartenburg from "./wartenburg.json";
import hagelberg from "./hagelberg.json";
import hanau from "./hanau.json";
import ligny from "./ligny.json";
import lutzen from "./lutzen.json";
import mockern from "./mockern.json";
import medinaDeRioseco from "./medina-de-rioseco.json";
import maloyaroslavets from "./maloyaroslavets.json";
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
import smolensk from "./smolensk.json";
import sorauren from "./sorauren.json";
import saltanovka from "./saltanovka.json";
import talavera from "./talavera.json";
import tarutino from "./tarutino.json";
import valutino from "./valutino.json";
import vimeiro from "./vimeiro.json";
import vitoria from "./vitoria.json";
import vyazma from "./vyazma.json";
import waterloo from "./waterloo.json";
import wavre from "./wavre.json";
import {
  nivelle,
  ocana,
  somosierra,
  toulouse,
  almeida,
  arcis,
  badajoz,
  brienne,
  chateauThierry,
  champaubert,
  craonne,
  dennewitz,
  dresden,
  fereChampenoise,
  gohrde,
  katzbach,
  kulm,
  laon,
  laRothiere,
  leipzig,
  montereau,
  montmirail,
  paris,
  reims,
  vauchamps,
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
  rippach,
  reichenbach,
  haynau,
  luckau,
  kitzen,
  lowenberg,
  goldberg,
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
  wertingen,
  haslach,
  elchingen,
  ulm,
  amstetten,
  durenstein,
  schongrabern,
  austerlitz,
  schleiz,
  saalfeld,
  jena,
  auerstedt,
  halle,
  prenzlau,
  lubeck,
  czarnowo,
  pultusk,
  golymin,
  mohrungen,
  eylau,
  ostroleka,
  danzig1807,
  guttstadt,
  heilsberg,
  friedland,
  teugenHausen,
  abensberg,
  landshut,
  eckmuhl,
  regensburg,
  neumarkt,
  ebelsberg,
  aspernEssling,
  raab,
  wagram,
  znaim,
} from "./planned";

const FRANCE = { name: "France", src: "/flags/france.svg" };

/**
 * Campaigns, in the order they were fought, each with its battles in order, whose historical forces can be opened
 * as new lists. To add a battle, write src/data/battles/<battle-id>.json (a HistoricalBattle naming its
 * campaign's id) and import it here. Run `npm run check:forces` to see that every force builds and what
 * it breaks of its list's rules.
 */
const allCampaigns: HistoricalCampaign[] = [
  // Army lists: A Clash of Eagles' 1812 lists stand in for every army of 1805 (France, Bavaria, Württemberg,
  // Austria and Russia); there is no list of the 1805 Austrians or Russians of its own.
  {
    id: "ulm-austerlitz-1805",
    name: "The Ulm and Austerlitz Campaign",
    dates: "September–December 1805",
    sides: [
      { name: "France and her allies", flags: [FRANCE, { name: "Bavaria", src: "/flags/bavaria.svg" }, { name: "Württemberg", src: "/flags/wurttemberg.svg" }, { name: "Baden", src: "/flags/baden.svg" }] },
      { name: "The Third Coalition", flags: [{ name: "Austria", src: "/flags/austria.svg" }, { name: "Russia", src: "/flags/russia.svg" }] },
    ],
    summary:
      "The Grande Armée marched from the Channel coast to the Rhine and wheeled round behind Mack's Austrians in Bavaria before the Russians could join them, shutting him into Ulm after Wertingen, Haslach and Elchingen, where he surrendered his army. Napoleon followed Kutuzov's Russians down the Danube past Amstetten, Dürenstein and Schöngrabern, took Vienna, and in December beat the Tsar's and the Emperor Francis's armies together at Austerlitz.",
  },
  // Army lists: the community Prussia (1806) list covers the Prussians; A Clash of Eagles' 1812 lists stand in
  // for the French and the Saxons.
  {
    id: "jena-1806",
    name: "The Jena Campaign",
    dates: "October–November 1806",
    art: {
      src: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Charles_Meynier_-_Entr%C3%A9e_de_Napol%C3%A9on_%C3%A0_Berlin._27_octobre_1806.jpg/960px-Charles_Meynier_-_Entr%C3%A9e_de_Napol%C3%A9on_%C3%A0_Berlin._27_octobre_1806.jpg",
      title: "Napoleon's Entry into Berlin, 27 October 1806",
      artist: "Charles Meynier",
      date: "1810",
      page: "https://commons.wikimedia.org/wiki/File:Charles_Meynier_-_Entr%C3%A9e_de_Napol%C3%A9on_%C3%A0_Berlin._27_octobre_1806.jpg",
    },
    sides: [
      { name: "France", flags: [FRANCE] },
      { name: "The Fourth Coalition", flags: [{ name: "Prussia", src: "/flags/prussia.png" }, { name: "Saxony", src: "/flags/saxony.svg" }] },
    ],
    summary:
      "Prussia went to war alone against Napoleon, and the Grande Armée came north through the Thuringian Forest in three columns, brushing aside the Prussians at Schleiz and Saalfeld. On one day in October Napoleon beat Hohenlohe at Jena while Davout's single corps beat the main Prussian army at Auerstedt, and in the pursuit that followed, through Halle, Prenzlau and Lübeck, the old army of Frederick the Great was hunted down and its fortresses gave up one after another.",
  },
  // Army lists: the community Prussia (1806) list covers the Prussians; A Clash of Eagles' 1812 lists stand in
  // for the French, the Russians, the Poles and the Saxons.
  {
    id: "poland-1807",
    name: "The Polish Campaign",
    dates: "December 1806 – June 1807",
    sides: [
      { name: "France and her allies", flags: [FRANCE, { name: "Poland", src: "/flags/poland.svg" }, { name: "Saxony", src: "/flags/saxony.svg" }] },
      { name: "The Fourth Coalition", flags: [{ name: "Russia", src: "/flags/russia.svg" }, { name: "Prussia", src: "/flags/prussia.png" }] },
    ],
    summary:
      "With Prussia beaten, Napoleon marched into Poland to meet the Russians coming to its aid, and the war went on through the winter in mud and snow, from Czarnowo, Pułtusk and Golymin to the frozen slaughter of Eylau, where neither army could claim to have won. In the spring Lefebvre took Danzig, and in June, after Guttstadt and Heilsberg, Napoleon caught Bennigsen's army with its back to the Alle at Friedland and broke it, and the Tsar made peace at Tilsit.",
  },
  // Army lists: A Clash of Eagles' 1812 lists stand in for every army of 1809: the French, the Confederation of
  // the Rhine, Bavaria, Saxony, Württemberg, the Kingdom of Italy and Austria.
  {
    id: "danube-1809",
    name: "The Danube Campaign",
    dates: "April–July 1809",
    sides: [
      { name: "France and her allies", flags: [FRANCE, { name: "Bavaria", src: "/flags/bavaria.svg" }, { name: "Saxony", src: "/flags/saxony.svg" }, { name: "Württemberg", src: "/flags/wurttemberg.svg" }, { name: "Kingdom of Italy", src: "/flags/italy-napoleonic.png" }] },
      { name: "The Fifth Coalition", flags: [{ name: "Austria", src: "/flags/austria.svg" }] },
    ],
    summary:
      "With Napoleon's best troops in Spain, Austria struck first, Archduke Charles crossing into Bavaria in April. Napoleon came up and in five days of fighting, at Teugen-Hausen, Abensberg, Landshut, Eckmühl and Regensburg, threw him back over the Danube, and marched down the river to Vienna. His first crossing of the Danube was beaten at Aspern-Essling, but in July, joined by Eugène's army from Italy, victor at Raab, he crossed again and won at Wagram, and after Znaim Austria sought an armistice.",
  },
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
    sides: [
      { name: "France", flags: [{ name: "France", src: "/flags/france.svg" }] },
      { name: "The allies", flags: [{ name: "Britain", src: "/flags/britain.svg" }, { name: "Spain", src: "/flags/spain.svg" }] },
    ],
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
    sides: [
      { name: "The Grande Armée", flags: [{ name: "France", src: "/flags/france.svg" }, { name: "Grand Duchy of Warsaw", src: "/flags/grand-duchy-warsaw.svg" }, { name: "Austria", src: "/flags/austria.svg" }, { name: "Prussia", src: "/flags/prussia.png" }, { name: "Saxony", src: "/flags/saxony.svg" }] },
      { name: "Russia", flags: [{ name: "Russia", src: "/flags/russia.svg" }] },
    ],
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
    sides: [
      { name: "France and her allies", flags: [{ name: "France", src: "/flags/france.svg" }, { name: "Saxony", src: "/flags/saxony.svg" }, { name: "Grand Duchy of Warsaw", src: "/flags/grand-duchy-warsaw.svg" }, { name: "Kingdom of Italy", src: "/flags/italy-napoleonic.png" }, { name: "Westphalia", src: "/flags/westphalia.svg" }] },
      { name: "The Sixth Coalition", flags: [{ name: "Russia", src: "/flags/russia.svg" }, { name: "Prussia", src: "/flags/prussia.png" }, { name: "Austria", src: "/flags/austria.svg" }, { name: "Sweden", src: "/flags/sweden.svg" }, { name: "Britain", src: "/flags/britain.svg" }] },
    ],
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
    sides: [
      { name: "France", flags: [{ name: "France", src: "/flags/france.svg" }] },
      { name: "The Sixth Coalition", flags: [{ name: "Russia", src: "/flags/russia.svg" }, { name: "Prussia", src: "/flags/prussia.png" }, { name: "Austria", src: "/flags/austria.svg" }, { name: "Bavaria", src: "/flags/bavaria.svg" }, { name: "Württemberg", src: "/flags/wurttemberg.svg" }] },
    ],
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
    sides: [
      { name: "France", flags: [{ name: "France", src: "/flags/france.svg" }] },
      { name: "The Seventh Coalition", flags: [{ name: "Britain", src: "/flags/britain.svg" }, { name: "United Netherlands", src: "/flags/netherlands.svg" }, { name: "Brunswick", src: "/flags/brunswick.svg" }, { name: "Nassau", src: "/flags/nassau.svg" }, { name: "Prussia", src: "/flags/prussia.png" }] },
    ],
    summary:
      "Napoleon's return from Elba ended in four days in Belgium. He struck between Wellington's Anglo-allied army and Blücher's Prussians, beating the Prussians at Ligny while Ney held Wellington at Quatre Bras; two days later the allies joined to defeat him at Waterloo, while Grouchy fought the Prussian rearguard at Wavre.",
  },
];

// Each campaign with its chief commanders' portraits, written by scripts/forces/commanders.py
// Campaigns hidden until they're ready to show (paintings and forces still to come), with their battles; their
// data stays here. Remove an id to show it.
const HIDDEN_CAMPAIGNS = new Set(["ulm-austerlitz-1805", "poland-1807", "danube-1809"]);

export const campaigns: HistoricalCampaign[] = allCampaigns.filter((c) => !HIDDEN_CAMPAIGNS.has(c.id)).map((c) => ({
  ...c,
  commanders: (campaignCommanders as Record<string, HistoricalCampaign["commanders"]>)[c.id],
}));

// Every battle, in the order fought: those with forces written, and those still to come (planned.ts)
const allBattles: HistoricalBattle[] = [
  // The Ulm and Austerlitz Campaign
  wertingen,
  haslach,
  elchingen,
  ulm,
  amstetten,
  durenstein,
  schongrabern,
  austerlitz,
  // The Jena Campaign
  schleiz,
  saalfeld,
  jena,
  auerstedt,
  halle,
  prenzlau,
  lubeck,
  // The Polish Campaign
  czarnowo,
  pultusk,
  golymin,
  mohrungen,
  eylau,
  ostroleka,
  danzig1807,
  guttstadt,
  heilsberg,
  friedland,
  // The Danube Campaign
  teugenHausen,
  abensberg,
  landshut,
  eckmuhl,
  regensburg,
  neumarkt,
  ebelsberg,
  aspernEssling,
  raab,
  wagram,
  znaim,
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
  smolensk as HistoricalBattle,
  polotsk as HistoricalBattle,
  valutino as HistoricalBattle,
  dahlenkirchen as HistoricalBattle,
  borodino as HistoricalBattle,
  mesoten as HistoricalBattle,
  tarutino as HistoricalBattle,
  polotsk2 as HistoricalBattle,
  maloyaroslavets as HistoricalBattle,
  vyazma as HistoricalBattle,
  krasnoi as HistoricalBattle,
  berezina as HistoricalBattle,
  // The War of Liberation
  danzig,
  luneburg,
  mockern as HistoricalBattle,
  rippach,
  lutzen as HistoricalBattle,
  bautzen as HistoricalBattle,
  reichenbach,
  haynau,
  luckau,
  kitzen,
  lowenberg,
  grossbeeren as HistoricalBattle,
  goldberg,
  katzbach,
  dresden,
  hagelberg as HistoricalBattle,
  plagwitz,
  kulm,
  dennewitz,
  gohrde,
  altenburg,
  wartenburg as HistoricalBattle,
  liebertwolkwitz,
  mockernLeipzig,
  leipzig,
  torgau,
  hanau as HistoricalBattle,
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

const schedule = allBattles.filter((b) => !HIDDEN_CAMPAIGNS.has(b.campaign));

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

/** What a campaign's card shows, small enough for the home page to be sent without the battles */
export type CampaignSummary = Pick<HistoricalCampaign, "id" | "art" | "name" | "dates" | "summary" | "sides"> & {
  /** Its forces, across every battle written so far */
  forces: number;
  /** No battles listed yet, so the card has no link and says it's coming */
  soon: boolean;
};

export function campaignSummary(c: HistoricalCampaign): CampaignSummary {
  const fought = battlesIn(c.id);
  return {
    id: c.id,
    art: c.art,
    name: c.name,
    dates: c.dates,
    summary: c.summary,
    sides: c.sides,
    forces: fought.reduce((n, b) => n + b.forces.length, 0),
    soon: fought.length === 0 && scheduleIn(c.id).length === 0,
  };
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
