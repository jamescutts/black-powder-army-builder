// Campaign maps: where each battle was fought, the towns that frame its theatre, and the armies' main
// movements, keyed by battle and campaign id. Kept apart from the battles' own files so a battle can be
// written without touching its map, and a map drawn without touching its battles. Positions are
// [latitude, longitude]; routes are approximate, drawn through the towns the armies passed.

export type LatLng = [number, number];

/** Which side of its marker a label sits, so labels of nearby battles don't overlap */
export type LabelSide = "top" | "bottom" | "left" | "right";

export interface BattlePlace {
  at: LatLng;
  label?: LabelSide;
  /** Pixels to move the label by, beyond its side, where battles are close together */
  nudge?: [number, number];
}

export interface MapSide {
  id: string;
  label: string;
  colour: string;
  /** A dash pattern, so the sides can be told apart without colour */
  dash?: string;
}

export interface MapRoute {
  side: string;
  name: string;
  dates: string;
  note: string;
  path: LatLng[];
  /** A name for where the route begins, shown beside its start; a line break as "\n" */
  start?: string;
  startLabel?: LabelSide;
}

export interface MapPlace {
  name: string;
  at: LatLng;
  label?: LabelSide;
  /** A capital or great city, named larger, and kept on a phone's map before it's zoomed in */
  city?: boolean;
}

export interface MapRegion {
  name: string;
  at: LatLng;
  /** A state's name in large spaced capitals, a province's smaller, a sea's in italics */
  kind: "state" | "province" | "sea";
}

export interface CampaignMap {
  /** The theatre's name, shown on the map's key */
  theatre: string;
  sides: MapSide[];
  /** Towns named on the map for bearings, not battles; their names as they were then */
  places: MapPlace[];
  /** The frontiers of the time, as lines, approximate */
  borders: LatLng[][];
  /** States, provinces and seas named across the map */
  regions: MapRegion[];
  routes: MapRoute[];
}

/** Every battle's position on its campaign's map */
export const battlePlaces: Record<string, BattlePlace> = {
  // The Russian Campaign
  mir: { at: [53.45, 26.47], label: "right" },
  romanov: { at: [53.03, 26.45], label: "right" },
  eckau: { at: [56.55, 24.2], label: "right", nudge: [0, 5] },
  saltanovka: { at: [53.8, 30.35], label: "bottom" },
  ostrovno: { at: [55.35, 29.85], label: "bottom" },
  klyastitsy: { at: [55.88, 28.6], label: "top" },
  gorodechno: { at: [52.22, 24.53], label: "bottom" },
  kobrin: { at: [52.21, 24.36], label: "top" },
  smolensk: { at: [54.78, 32.04], label: "bottom" },
  polotsk: { at: [55.49, 28.7], label: "left" },
  valutino: { at: [54.87, 32.4], label: "top" },
  dahlenkirchen: { at: [56.88, 24.32], label: "right", nudge: [0, -5] },
  borodino: { at: [55.52, 35.82], label: "top" },
  mesoten: { at: [56.43, 24.05], label: "bottom" },
  tarutino: { at: [55.18, 36.98], label: "right" },
  "polotsk-2": { at: [55.49, 28.86], label: "right" },
  maloyaroslavets: { at: [55.01, 36.47], label: "bottom" },
  vyazma: { at: [55.21, 34.3], label: "top" },
  krasnoi: { at: [54.56, 31.43], label: "left" },
  berezina: { at: [54.33, 28.35], label: "bottom" },
};

const FRENCH_1812: MapSide = { id: "french", label: "Grande Armée", colour: "#2b4a7e" };
// The flanking corps, which fought campaigns of their own under their own commanders
const PRUSSIAN_1812: MapSide = { id: "prussian", label: "Prussian corps (Riga)", colour: "#2e2b28", dash: "12 4 2 4" };
const AUSTRIAN_1812: MapSide = { id: "austrian", label: "Austrians and Saxons", colour: "#b4561a", dash: "2 7" };
const RUSSIAN_1812: MapSide = { id: "russian", label: "Russian armies", colour: "#2f6b3a", dash: "8 6" };

/** Each campaign's map */
export const campaignMaps: Record<string, CampaignMap> = {
  "russia-1812": {
    theatre: "Western Russia, 1812",
    sides: [FRENCH_1812, PRUSSIAN_1812, AUSTRIAN_1812, RUSSIAN_1812],
    places: [
      { name: "Moscow", at: [55.75, 37.62], label: "right", city: true },
      { name: "Vilna", at: [54.69, 25.28], label: "bottom", city: true },
      { name: "Riga", at: [56.95, 24.11], label: "left", city: true },
      { name: "Warsaw", at: [52.23, 21.01], label: "bottom", city: true },
      { name: "Königsberg", at: [54.71, 20.51], label: "bottom", city: true },
      { name: "Minsk", at: [53.9, 27.56], label: "bottom" },
      { name: "Kovno", at: [54.9, 23.9], label: "left" },
      { name: "Grodno", at: [53.68, 23.83], label: "right" },
      { name: "Białystok", at: [53.13, 23.16], label: "left" },
      { name: "Brest-Litovsk", at: [52.1, 23.7], label: "left" },
      { name: "Tilsit", at: [55.08, 21.88], label: "bottom" },
      { name: "Mitau", at: [56.65, 23.72], label: "left" },
      { name: "Dünaburg", at: [55.87, 26.53], label: "top" },
      { name: "Drissa", at: [55.78, 27.97], label: "top" },
      { name: "Vitebsk", at: [55.19, 30.2], label: "right" },
      { name: "Velikiye Luki", at: [56.34, 30.53], label: "right" },
      { name: "Mogilev", at: [53.9, 30.33], label: "left" },
      { name: "Orsha", at: [54.51, 30.42], label: "bottom" },
      { name: "Borisov", at: [54.23, 28.5], label: "right" },
      { name: "Bobruisk", at: [53.15, 29.22], label: "right" },
      { name: "Slonim", at: [53.09, 25.32], label: "right" },
      { name: "Pinsk", at: [52.11, 26.1], label: "bottom" },
      { name: "Dorogobuzh", at: [54.92, 33.3], label: "bottom" },
      { name: "Kaluga", at: [54.53, 36.27], label: "bottom" },
    ],
    borders: [
      // The Russian Empire's western frontier: from the Baltic to the Niemen against East Prussia, down the
      // Niemen against the Duchy of Warsaw, round the Białystok district Russia took at Tilsit, and up the Bug
      // past Brest-Litovsk to Austrian Galicia
      [
        [55.9, 21.07],
        [55.6, 21.45],
        [55.35, 21.85],
        [55.15, 22.4],
        [55.08, 22.77],
        [54.97, 23.4],
        [54.9, 23.85],
        [54.6, 24.0],
        [54.4, 24.05],
        [54.1, 24.0],
        [53.95, 23.9],
        [53.82, 23.45],
        [53.65, 23.0],
        [53.48, 22.7],
        [53.2, 22.3],
        [52.95, 22.2],
        [52.67, 22.32],
        [52.4, 22.66],
        [52.25, 23.15],
        [52.08, 23.6],
        [51.85, 23.62],
        [51.55, 23.55],
        [51.2, 23.78],
        [50.86, 24.15],
        [50.5, 24.6],
        [50.15, 25.2],
        [49.9, 25.7],
      ],
      // East Prussia against the Duchy of Warsaw
      [
        [55.08, 22.77],
        [54.75, 22.8],
        [54.35, 22.78],
        [54.1, 22.55],
        [53.8, 22.4],
        [53.45, 21.9],
        [53.25, 21.0],
        [53.15, 20.2],
      ],
      // The Duchy of Warsaw against Austrian Galicia
      [
        [50.86, 24.15],
        [50.6, 23.3],
        [50.5, 22.3],
        [50.65, 21.4],
      ],
    ],
    regions: [
      { name: "Russian Empire", at: [56.3, 33.6], kind: "state" },
      { name: "Duchy of Warsaw", at: [52.75, 21.35], kind: "state" },
      { name: "Prussia", at: [54.15, 21.2], kind: "state" },
      { name: "Austria", at: [50.4, 23.2], kind: "state" },
      { name: "Courland", at: [56.75, 22.6], kind: "province" },
      { name: "Lithuania", at: [55.45, 25.1], kind: "province" },
      { name: "White Russia", at: [54.05, 29.4], kind: "province" },
      { name: "Volhynia", at: [51.2, 26.3], kind: "province" },
      { name: "Livonia", at: [57.45, 26.3], kind: "province" },
      { name: "Baltic Sea", at: [56.4, 20.0], kind: "sea" },
      { name: "Gulf of Riga", at: [57.55, 23.35], kind: "sea" },
    ],
    routes: [
      {
        side: "french",
        name: "The Grande Armée marches on Moscow",
        dates: "24 June – 14 September 1812",
        note: "Gathered in East Prussia and the Duchy of Warsaw, the main army crossed the Niemen at Kovno on 24 June, then marched through Vilna and Vitebsk to Smolensk, and up the old post road past Vyazma to Borodino and Moscow.",
        start: "Crosses the Niemen\n24 June",
        startLabel: "bottom",
        path: [
          [54.65, 23.03],
          [54.9, 23.9],
          [54.69, 25.28],
          [55.14, 27.69],
          [55.05, 29.45],
          [55.35, 29.85],
          [55.19, 30.2],
          [54.78, 32.04],
          [54.87, 32.4],
          [54.92, 33.3],
          [55.21, 34.3],
          [55.55, 35.0],
          [55.52, 35.82],
          [55.75, 37.62],
        ],
      },
      {
        side: "french",
        name: "The retreat from Moscow",
        dates: "19 October – 14 December 1812",
        note: "South to Maloyaroslavets, then, turned back, onto the ruined road by Borodino, Vyazma, Smolensk and Krasnoi, across the Berezina and back to the Niemen.",
        path: [
          [55.75, 37.62],
          [55.38, 36.7],
          [55.01, 36.47],
          [55.21, 36.49],
          [55.5, 36.03],
          [55.52, 35.82],
          [55.21, 34.3],
          [54.92, 33.3],
          [54.78, 32.04],
          [54.56, 31.43],
          [54.51, 30.42],
          [54.23, 28.5],
          [54.33, 28.35],
          [54.31, 26.85],
          [54.69, 25.28],
          [54.9, 23.9],
        ],
      },
      {
        side: "prussian",
        name: "Macdonald's X Corps on Riga",
        dates: "July 1812",
        note: "Macdonald's Prussians and Poles marched north from Tilsit into Courland to threaten Riga, fighting at Eckau and holding the line of the Aa.",
        path: [
          [55.08, 21.88],
          [55.38, 23.12],
          [56.65, 23.72],
          [56.55, 24.2],
        ],
      },
      {
        side: "french",
        name: "Oudinot on the road to St Petersburg",
        dates: "July – August 1812",
        note: "II Corps turned north from Polotsk against Wittgenstein, was checked at Klyastitsy and fell back on Polotsk.",
        path: [
          [55.49, 28.7],
          [55.88, 28.6],
        ],
      },
      {
        side: "austrian",
        name: "Schwarzenberg and Reynier in the south",
        dates: "July – August 1812",
        note: "The Austrian corps and Reynier's Saxons turned south from Slonim against Tormasov, beating him at Gorodechno.",
        path: [
          [53.09, 25.32],
          [52.56, 24.46],
          [52.22, 24.53],
        ],
      },
      {
        side: "russian",
        name: "Barclay's First Army falls back",
        dates: "June – August 1812",
        note: "From Vilna to the camp at Drissa, then east by Polotsk and Vitebsk to join Bagration at Smolensk.",
        path: [
          [54.69, 25.28],
          [55.14, 26.16],
          [55.78, 27.97],
          [55.49, 28.7],
          [55.19, 30.2],
          [54.78, 32.04],
        ],
      },
      {
        side: "russian",
        name: "Bagration's Second Army escapes",
        dates: "June – August 1812",
        note: "Cut off in the south, Bagration marched by Mir, Nesvizh and Bobruisk, tried to break through at Saltanovka, and slipped round by Mstislavl to Smolensk.",
        path: [
          [53.16, 24.45],
          [53.45, 26.47],
          [53.22, 26.68],
          [53.15, 29.22],
          [53.8, 30.35],
          [54.02, 31.73],
          [54.78, 32.04],
        ],
      },
      {
        side: "russian",
        name: "The Russian armies retreat to Borodino",
        dates: "August – September 1812",
        note: "United under Kutuzov, the armies fell back along the Moscow road to stand at Borodino, then through Moscow and round by Podolsk to the camp at Tarutino.",
        path: [
          [54.87, 32.4],
          [55.21, 34.3],
          [55.52, 35.82],
          [55.75, 37.62],
          [55.43, 37.55],
          [55.18, 36.98],
        ],
      },
      {
        side: "russian",
        name: "Kutuzov's parallel march",
        dates: "October – November 1812",
        note: "From Tarutino and Maloyaroslavets, Kutuzov's army shadowed the retreat to the south of the road, striking it at Vyazma and Krasnoi.",
        path: [
          [55.18, 36.98],
          [55.01, 36.47],
          [54.75, 35.0],
          [55.21, 34.3],
          [54.7, 33.2],
          [54.56, 31.43],
        ],
      },
      {
        side: "russian",
        name: "Wittgenstein drives south",
        dates: "October – November 1812",
        note: "Reinforced from Finland and St Petersburg, Wittgenstein stormed Polotsk and pressed on by Chashniki to close the Berezina from the north.",
        path: [
          [55.88, 28.6],
          [55.49, 28.86],
          [54.86, 29.16],
          [54.33, 28.35],
        ],
      },
      {
        side: "russian",
        name: "Tormasov and Chichagov in the south",
        dates: "July – November 1812",
        note: "Tormasov's Third Army marched north from Volhynia to take the Saxons at Kobrin, was beaten at Gorodechno, and was joined by Chichagov's Army of the Danube, which marched north by Minsk to hold the Berezina at Borisov.",
        path: [
          [50.75, 25.33],
          [52.21, 24.36],
          [52.22, 24.53],
          [52.1, 23.7],
          [53.12, 26.0],
          [53.9, 27.56],
          [54.23, 28.5],
        ],
      },
      {
        side: "russian",
        name: "Essen's sortie from Riga",
        dates: "August 1812",
        note: "Essen's garrison struck out across the Dvina against the Prussian outposts at Dahlenkirchen.",
        path: [
          [56.95, 24.11],
          [56.88, 24.32],
        ],
      },
      {
        side: "russian",
        name: "Steinheil marches on Mitau",
        dates: "September 1812",
        note: "Landed at Riga from Finland, Steinheil's corps marched south towards Mitau and met Yorck's Prussians around Mesoten.",
        path: [
          [56.95, 24.11],
          [56.7, 23.9],
          [56.43, 24.05],
        ],
      },
    ],
  },
};
