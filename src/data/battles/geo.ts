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
}

export interface CampaignMap {
  /** The theatre's name, shown on the map's key */
  theatre: string;
  sides: MapSide[];
  /** Towns named on the map for bearings, not battles */
  places: { name: string; at: LatLng; label?: LabelSide }[];
  routes: MapRoute[];
}

/** Every battle's position on its campaign's map */
export const battlePlaces: Record<string, BattlePlace> = {
  // The Russian Campaign
  mir: { at: [53.45, 26.47], label: "left" },
  romanov: { at: [53.03, 26.45], label: "right" },
  eckau: { at: [56.55, 24.2], label: "right", nudge: [0, 5] },
  saltanovka: { at: [53.8, 30.35], label: "bottom" },
  ostrovno: { at: [55.35, 29.85], label: "top" },
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
  krasnoi: { at: [54.56, 31.43], label: "bottom" },
  berezina: { at: [54.33, 28.35], label: "bottom" },
};

const FRENCH_1812: MapSide = { id: "french", label: "Grande Armée and allies", colour: "#2b4a7e" };
const RUSSIAN_1812: MapSide = { id: "russian", label: "Russian armies", colour: "#2f6b3a", dash: "8 6" };

/** Each campaign's map */
export const campaignMaps: Record<string, CampaignMap> = {
  "russia-1812": {
    theatre: "Western Russia, 1812",
    sides: [FRENCH_1812, RUSSIAN_1812],
    places: [
      { name: "Moscow", at: [55.75, 37.62], label: "right" },
      { name: "Kovno", at: [54.9, 23.9], label: "left" },
      { name: "Vilna", at: [54.69, 25.28], label: "bottom" },
      { name: "Riga", at: [56.95, 24.11], label: "top" },
      { name: "Minsk", at: [53.9, 27.56], label: "bottom" },
      { name: "Vitebsk", at: [55.19, 30.2], label: "right" },
      { name: "Mogilev", at: [53.9, 30.33], label: "right" },
      { name: "Brest", at: [52.1, 23.7], label: "left" },
      { name: "Tilsit", at: [55.08, 21.88], label: "bottom" },
    ],
    routes: [
      {
        side: "french",
        name: "The Grande Armée marches on Moscow",
        dates: "24 June – 14 September 1812",
        note: "Across the Niemen at Kovno, through Vilna and Vitebsk to Smolensk, then up the old post road past Vyazma to Borodino and Moscow.",
        path: [
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
        side: "french",
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
        side: "french",
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
