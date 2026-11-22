// Campaign maps: where each battle was fought, the towns that frame its theatre, and the armies' main
// movements, keyed by battle and campaign id. Kept apart from the battles' own files so a battle can be
// written without touching its map, and a map drawn without touching its battles. Positions are
// [latitude, longitude]; routes are approximate, drawn through the towns the armies passed.

export type LatLng = [number, number];

/** Which side of its marker a label sits, so labels of nearby battles don't overlap */
export type LabelSide = "top" | "bottom" | "left" | "right";

export interface BattlePlace {
  at: LatLng;
  /** Roughly how many men of both sides were engaged, which sizes its mark against its campaign's others */
  engaged: number;
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
  /** How many pixels to the right of their direction of travel its routes run (3 if not given), so two
   * sides on the same road run side by side */
  lane?: number;
}

export interface MapRoute {
  side: string;
  name: string;
  dates: string;
  note: string;
  path: LatLng[];
  /** A main army's march, drawn heavier so it can be followed through the rest */
  main?: boolean;
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
  /** The basemap: physical (relief and land cover) for a wide theatre, shaded relief for one close enough
   * to need finer tiles than the physical map has */
  tiles?: "physical" | "relief";
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
  mir: { at: [53.45, 26.47], engaged: 7000, label: "right" },
  romanov: { at: [53.06, 27.23], engaged: 7000, label: "bottom" },
  eckau: { at: [56.55, 24.2], engaged: 11000, label: "right", nudge: [0, 5] },
  saltanovka: { at: [53.8, 30.35], engaged: 45000, label: "bottom" },
  ostrovno: { at: [55.35, 29.85], engaged: 50000, label: "bottom" },
  klyastitsy: { at: [55.88, 28.6], engaged: 50000, label: "top" },
  gorodechno: { at: [52.22, 24.53], engaged: 58000, label: "bottom" },
  kobrin: { at: [52.21, 24.36], engaged: 22000, label: "top" },
  smolensk: { at: [54.78, 32.04], engaged: 120000, label: "bottom" },
  polotsk: { at: [55.49, 28.7], engaged: 57000, label: "left" },
  valutino: { at: [54.87, 32.4], engaged: 55000, label: "top" },
  dahlenkirchen: { at: [56.88, 24.32], engaged: 8000, label: "right", nudge: [0, -5] },
  borodino: { at: [55.52, 35.82], engaged: 255000, label: "top" },
  mesoten: { at: [56.43, 24.05], engaged: 15000, label: "bottom" },
  tarutino: { at: [55.18, 36.98], engaged: 62000, label: "right" },
  "polotsk-2": { at: [55.49, 28.86], engaged: 67000, label: "right" },
  maloyaroslavets: { at: [55.01, 36.47], engaged: 50000, label: "bottom" },
  vyazma: { at: [55.21, 34.3], engaged: 62000, label: "top" },
  krasnoi: { at: [54.56, 31.43], engaged: 130000, label: "left" },
  berezina: { at: [54.33, 28.35], engaged: 110000, label: "bottom" },

  // The Hundred Days
  ligny: { at: [50.51, 4.58], engaged: 152000, label: "right" },
  "quatre-bras": { at: [50.57, 4.45], engaged: 56000, label: "left" },
  waterloo: { at: [50.68, 4.41], engaged: 190000, label: "left" },
  wavre: { at: [50.72, 4.61], engaged: 50000, label: "right" },

  // The Peninsular War
  "medina-de-rioseco": { at: [41.88, -5.04], engaged: 36000, label: "top" },
  bailen: { at: [38.09, -3.78], engaged: 50000, label: "right" },
  rolica: { at: [39.32, -9.18], engaged: 18000, label: "right" },
  vimeiro: { at: [39.18, -9.32], engaged: 33000, label: "left" },
  somosierra: { at: [41.13, -3.58], engaged: 20000, label: "right" },
  corunna: { at: [43.37, -8.4], engaged: 31000, label: "right" },
  talavera: { at: [39.96, -4.83], engaged: 100000, label: "bottom" },
  ocana: { at: [39.96, -3.5], engaged: 85000, label: "bottom" },
  bussaco: { at: [40.35, -8.37], engaged: 115000, label: "right" },
  "fuentes-de-onoro": { at: [40.59, -6.81], engaged: 85000, label: "top" },
  albuera: { at: [38.72, -6.82], engaged: 59000, label: "bottom" },
  salamanca: { at: [40.91, -5.6], engaged: 102000, label: "top" },
  vitoria: { at: [42.85, -2.67], engaged: 136000, label: "bottom" },
  sorauren: { at: [42.86, -1.62], engaged: 60000, label: "right" },
  nivelle: { at: [43.36, -1.6], engaged: 144000, label: "left" },
  orthez: { at: [43.49, -0.77], engaged: 80000, label: "right" },
  toulouse: { at: [43.6, 1.44], engaged: 92000, label: "right" },
  // The sieges
  saragossa: { at: [41.66, -0.93], engaged: 26000, label: "left" },
  "saragossa-2": { at: [41.64, -0.83], engaged: 80000, label: "right" },
  gerona: { at: [41.98, 2.82], engaged: 44000, label: "left" },
  almeida: { at: [40.73, -6.9], engaged: 19000, label: "left" },
  tarragona: { at: [41.12, 1.25], engaged: 38000, label: "left" },
  "ciudad-rodrigo": { at: [40.6, -6.53], engaged: 40000, label: "bottom" },
  badajoz: { at: [38.88, -6.97], engaged: 32000, label: "left" },
  burgos: { at: [42.34, -3.7], engaged: 37000, label: "left" },
  "san-sebastian": { at: [43.32, -1.98], engaged: 21000, label: "left" },
  pamplona: { at: [42.81, -1.64], engaged: 14000, label: "bottom" },
};

const FRENCH_1812: MapSide = { id: "french", label: "Grande Armée", colour: "#2b4a7e" };
// The flanking corps, which fought campaigns of their own under their own commanders
const PRUSSIAN_1812: MapSide = { id: "prussian", label: "Prussian corps (Riga)", colour: "#2e2b28", dash: "12 4 2 4" };
const AUSTRIAN_1812: MapSide = { id: "austrian", label: "Austrians and Saxons", colour: "#b4561a", dash: "2 7" };
const RUSSIAN_1812: MapSide = { id: "russian", label: "Russian armies", colour: "#2f6b3a", dash: "8 6", lane: 8 };

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
        main: true,
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
        main: true,
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
        name: "Jérôme pursues Bagration",
        dates: "July 1812",
        note: "King Jérôme's right wing followed Bagration from Grodno by Novogrudok, its Polish cavalry pressing ahead into Platov's ambushes at Mir and Romanovo.",
        path: [
          [53.68, 23.83],
          [53.6, 25.83],
          [53.45, 26.47],
          [53.22, 26.68],
          [53.06, 27.23],
        ],
      },
      {
        side: "prussian",
        name: "Yorck's Prussians close on Riga",
        dates: "August 1812",
        note: "After Eckau the Prussian corps pushed its outposts up to the Dvina before Riga, where Essen's garrison struck at them at Dahlenkirchen.",
        path: [
          [56.55, 24.2],
          [56.75, 24.3],
          [56.88, 24.32],
        ],
      },
      {
        side: "prussian",
        name: "Yorck turns on Steinheil",
        dates: "September–October 1812",
        note: "When Steinheil's corps marched south from Riga, Yorck drew the Prussians together from Mitau and threw it back around Mesoten.",
        path: [
          [56.65, 23.72],
          [56.5, 23.95],
          [56.43, 24.05],
        ],
      },
      {
        side: "austrian",
        name: "Reynier's Saxons in the south",
        dates: "July 1812",
        note: "Reynier's Saxon VII Corps came south from Slonim to watch Tormasov across the Pripet marshes, leaving Klengel's brigade at Kobrin, where Tormasov fell on it and forced it to surrender.",
        path: [
          [53.09, 25.32],
          [52.56, 24.3],
          [52.21, 24.36],
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
        note: "From Vilna to the camp at Drissa, then east by Polotsk and Vitebsk, Ostermann-Tolstoy's rearguard holding Murat at Ostrovno, to join Bagration at Smolensk.",
        path: [
          [54.69, 25.28],
          [55.14, 26.16],
          [55.78, 27.97],
          [55.49, 28.7],
          [55.35, 29.85],
          [55.19, 30.2],
          [54.78, 32.04],
        ],
      },
      {
        side: "russian",
        name: "Bagration's Second Army escapes",
        dates: "June – August 1812",
        note: "Cut off in the south, Bagration marched by Mir, Nesvizh, Romanovo, Slutsk and Bobruisk, his Cossacks turning on the pursuit at Mir and Romanovo; he tried to break through at Saltanovka, and slipped round by Mstislavl to Smolensk.",
        path: [
          [53.16, 24.45],
          [53.45, 26.47],
          [53.22, 26.68],
          [53.06, 27.23],
          [53.02, 27.55],
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
        name: "Lewis marches out of Riga",
        dates: "July 1812",
        note: "General Lewis led a detachment of Essen's Riga garrison south to Eckau to meet Macdonald's advance, and fell back to Riga when the Prussians drove it off.",
        path: [
          [56.95, 24.11],
          [56.75, 24.12],
          [56.55, 24.2],
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

  "hundred-days": {
    theatre: "Belgium, June 1815",
    tiles: "relief",
    sides: [
      { id: "french", label: "Armée du Nord", colour: "#2b4a7e" },
      { id: "allied", label: "Wellington's Anglo-allied army", colour: "#a3322a", dash: "8 6" },
      { id: "prussian", label: "Blücher's Prussians", colour: "#2e2b28", dash: "12 4 2 4" },
    ],
    places: [
      { name: "Brussels", at: [50.85, 4.35], label: "right", city: true },
      { name: "Charleroi", at: [50.41, 4.44], label: "left", city: true },
      { name: "Namur", at: [50.47, 4.87], label: "right", city: true },
      { name: "Mons", at: [50.45, 3.95], label: "left" },
      { name: "Nivelles", at: [50.6, 4.33], label: "left" },
      { name: "Genappe", at: [50.61, 4.45], label: "right" },
      { name: "Gembloux", at: [50.56, 4.69], label: "right" },
      { name: "Fleurus", at: [50.48, 4.55], label: "bottom" },
      { name: "Hal", at: [50.73, 4.23], label: "left" },
      { name: "Beaumont", at: [50.24, 4.24], label: "top" },
      { name: "Philippeville", at: [50.2, 4.54], label: "right" },
    ],
    borders: [
      // France's northern frontier as the Treaty of Paris left it in 1814, with Beaumont and Philippeville French
      [
        [50.42, 3.6],
        [50.36, 3.85],
        [50.31, 4.05],
        [50.3, 4.22],
        [50.29, 4.36],
        [50.25, 4.5],
        [50.24, 4.66],
        [50.17, 4.8],
        [50.08, 4.87],
        [49.97, 4.95],
      ],
    ],
    regions: [
      { name: "France", at: [50.15, 4.05], kind: "state" },
      { name: "United Netherlands", at: [50.8, 4.98], kind: "state" },
      { name: "Brabant", at: [50.8, 4.05], kind: "province" },
      { name: "Hainaut", at: [50.52, 4.08], kind: "province" },
    ],
    routes: [
      {
        side: "french",
        name: "Napoleon crosses into Belgium",
        dates: "15 June 1815",
        note: "The Armée du Nord, gathered in secret behind the frontier around Beaumont, crossed the Sambre at Charleroi to strike between the allied armies before they could join.",
        start: "Crosses the frontier\n15 June",
        startLabel: "right",
        path: [
          [50.24, 4.24],
          [50.33, 4.36],
          [50.41, 4.44],
        ],
      },
      {
        side: "french",
        name: "Napoleon's right wing against Blücher",
        dates: "15–16 June 1815",
        note: "Napoleon took the right wing and the reserve by Fleurus against the Prussians gathering along the Ligny brook.",
        path: [
          [50.41, 4.44],
          [50.48, 4.55],
          [50.51, 4.58],
        ],
      },
      {
        side: "french",
        name: "Ney's left wing on the Brussels road",
        dates: "15–16 June 1815",
        note: "Ney led the left wing up the Brussels road by Gosselies and Frasnes to the crossroads at Quatre Bras.",
        path: [
          [50.41, 4.44],
          [50.47, 4.43],
          [50.55, 4.44],
          [50.57, 4.45],
        ],
      },
      {
        side: "french",
        name: "Napoleon follows Wellington",
        dates: "17–18 June 1815",
        note: "From Ligny Napoleon joined Ney and followed Wellington's retreat up the Brussels road in the rain, through Genappe to La Belle Alliance.",
        path: [
          [50.51, 4.58],
          [50.54, 4.53],
          [50.57, 4.45],
          [50.61, 4.45],
          [50.66, 4.42],
        ],
      },
      {
        side: "french",
        name: "Grouchy's pursuit",
        dates: "17–18 June 1815",
        note: "Sent after the Prussians with a third of the army, Grouchy went by Gembloux and Sart-à-Walhain and fought their rearguard at Wavre while the rest marched to Waterloo.",
        path: [
          [50.51, 4.58],
          [50.56, 4.69],
          [50.63, 4.65],
          [50.71, 4.62],
        ],
      },
      {
        side: "allied",
        name: "Wellington gathers at Quatre Bras",
        dates: "15–16 June 1815",
        note: "From Brussels, and from cantonments around Nivelles, Wellington's divisions marched through the night and the day to the crossroads Perponcher's Dutch-Belgians were holding.",
        path: [
          [50.85, 4.35],
          [50.715, 4.4],
          [50.61, 4.45],
          [50.57, 4.45],
        ],
      },
      {
        side: "allied",
        name: "Back to Mont-Saint-Jean",
        dates: "17 June 1815",
        note: "With the Prussians beaten at Ligny, Wellington fell back up the Brussels road to the ridge at Mont-Saint-Jean, Uxbridge's cavalry covering the retreat through Genappe.",
        path: [
          [50.57, 4.45],
          [50.61, 4.45],
          [50.69, 4.41],
        ],
      },
      {
        side: "prussian",
        name: "The Prussians gather at Ligny",
        dates: "15–16 June 1815",
        note: "Zieten's corps fell back from Charleroi while Pirch and Thielmann came in from Namur to stand along the Ligny brook.",
        path: [
          [50.47, 4.87],
          [50.5, 4.72],
          [50.51, 4.6],
        ],
      },
      {
        side: "prussian",
        name: "Retreat to Wavre",
        dates: "16–17 June 1815",
        note: "Beaten but unbroken, the Prussians fell back north by Tilly and Mont-Saint-Guibert, not east towards their own lines, so they could still join Wellington.",
        path: [
          [50.51, 4.58],
          [50.56, 4.55],
          [50.63, 4.61],
          [50.71, 4.6],
        ],
      },
      {
        side: "prussian",
        name: "Blücher marches to Waterloo",
        dates: "18 June 1815",
        note: "Leaving Thielmann to hold Wavre, Bülow, Pirch and Zieten marched by Chapelle-Saint-Lambert to fall on Napoleon's flank at Plancenoit.",
        path: [
          [50.72, 4.6],
          [50.7, 4.51],
          [50.66, 4.44],
        ],
      },
    ],
  },
  "peninsular-war": {
    theatre: "Spain, Portugal and southern France, 1808–1814",
    sides: [
      { id: "french", label: "French armies", colour: "#2b4a7e" },
      { id: "allied", label: "British and Portuguese", colour: "#a3322a", dash: "8 6" },
      { id: "spanish", label: "Spanish armies", colour: "#b4561a", dash: "2 7" },
    ],
    places: [
      { name: "Madrid", at: [40.42, -3.7], label: "right", city: true },
      { name: "Lisbon", at: [38.72, -9.14], label: "right", city: true },
      { name: "Cádiz", at: [36.53, -6.29], label: "right", city: true },
      { name: "Oporto", at: [41.15, -8.61], label: "right", city: true },
      { name: "Bayonne", at: [43.49, -1.47], label: "top", city: true },
      { name: "Seville", at: [37.39, -5.98], label: "right" },
      { name: "Burgos", at: [42.34, -3.7], label: "right" },
      { name: "Valladolid", at: [41.65, -4.72], label: "right" },
      { name: "Badajoz", at: [38.88, -6.97], label: "right" },
      { name: "Ciudad Rodrigo", at: [40.6, -6.53], label: "bottom" },
      { name: "Torres Vedras", at: [39.09, -9.26], label: "right" },
      { name: "Coimbra", at: [40.21, -8.43], label: "right" },
      { name: "Pamplona", at: [42.81, -1.64], label: "right" },
      { name: "Saragossa", at: [41.65, -0.88], label: "right" },
      { name: "Valencia", at: [39.47, -0.38], label: "left" },
      { name: "Córdoba", at: [37.88, -4.78], label: "bottom" },
      { name: "Astorga", at: [42.46, -6.06], label: "right" },
      { name: "Lugo", at: [43.01, -7.56], label: "right" },
      { name: "Sahagún", at: [42.37, -5.03], label: "right" },
    ],
    borders: [
      // Spain and Portugal, from the Minho to the Guadiana
      [
        [41.87, -8.87],
        [42.05, -8.2],
        [41.95, -7.9],
        [41.88, -7.2],
        [41.97, -6.6],
        [41.6, -6.25],
        [41.03, -6.85],
        [40.6, -6.84],
        [40.25, -6.9],
        [39.65, -7.0],
        [39.45, -7.3],
        [39.2, -7.25],
        [38.9, -7.05],
        [38.5, -7.3],
        [38.2, -7.0],
        [37.95, -7.25],
        [37.55, -7.5],
        [37.18, -7.42],
      ],
      // Spain and France, along the Pyrenees
      [
        [43.37, -1.79],
        [43.25, -1.5],
        [43.05, -1.3],
        [42.95, -0.8],
        [42.82, -0.3],
        [42.7, 0.6],
        [42.6, 1.4],
        [42.45, 2.0],
        [42.43, 3.17],
      ],
    ],
    regions: [
      { name: "Spain", at: [38.8, -2.6], kind: "state" },
      { name: "Portugal", at: [38.35, -8.25], kind: "state" },
      { name: "France", at: [44.05, 0.4], kind: "state" },
      { name: "Galicia", at: [42.7, -7.9], kind: "province" },
      { name: "Old Castile", at: [41.9, -3.9], kind: "province" },
      { name: "Estremadura", at: [39.25, -6.2], kind: "province" },
      { name: "Andalusia", at: [37.55, -4.4], kind: "province" },
      { name: "Aragon", at: [41.2, -1.2], kind: "province" },
      { name: "Catalonia", at: [41.85, 1.5], kind: "province" },
      { name: "Bay of Biscay", at: [44.2, -4.5], kind: "sea" },
      { name: "Atlantic Ocean", at: [38.0, -10.6], kind: "sea" },
      { name: "Mediterranean", at: [38.6, 1.4], kind: "sea" },
    ],
    routes: [
      {
        side: "french",
        name: "Dupont into Andalusia",
        dates: "May–July 1808",
        note: "Dupont's corps marched south from Madrid over the Sierra Morena to sack Córdoba, then fell back on Andújar and was trapped at Bailén.",
        path: [
          [40.42, -3.7],
          [39.4, -3.5],
          [38.28, -3.62],
          [37.88, -4.78],
          [38.04, -4.05],
          [38.09, -3.78],
        ],
      },
      {
        side: "french",
        name: "Napoleon marches on Madrid",
        dates: "November–December 1808",
        note: "Napoleon came over the Pyrenees himself with the Grande Armée's veterans, through Vitoria and Burgos, forced the pass of Somosierra and took Madrid.",
        path: [
          [43.49, -1.47],
          [42.85, -2.67],
          [42.34, -3.7],
          [41.13, -3.58],
          [40.42, -3.7],
        ],
      },
      {
        side: "french",
        name: "Soult pursues Moore",
        dates: "December 1808 – January 1809",
        note: "Soult followed Moore's army over the Galician mountains through the winter, catching it at Corunna as it waited for the fleet.",
        path: [
          [42.37, -5.03],
          [42.0, -5.68],
          [42.46, -6.06],
          [43.01, -7.56],
          [43.37, -8.4],
        ],
      },
      {
        side: "french",
        name: "Masséna invades Portugal",
        dates: "July–October 1810",
        note: "Masséna's Army of Portugal took Ciudad Rodrigo and Almeida, was thrown back at Bussaco, and followed Wellington to the Lines of Torres Vedras, where it starved through the winter.",
        path: [
          [40.6, -6.53],
          [40.73, -6.9],
          [40.66, -7.91],
          [40.35, -8.37],
          [40.21, -8.43],
          [39.6, -8.8],
          [39.12, -9.15],
        ],
      },
      {
        side: "allied",
        name: "Wellesley lands in Portugal",
        dates: "August 1808",
        note: "Sir Arthur Wellesley's expedition landed at Mondego Bay and marched south on Lisbon, driving Delaborde from Roliça and beating Junot at Vimeiro.",
        start: "Lands at Mondego Bay\nAug 1808",
        startLabel: "left",
        path: [
          [40.15, -8.86],
          [39.74, -8.81],
          [39.32, -9.18],
          [39.18, -9.32],
        ],
      },
      {
        side: "allied",
        name: "Moore's retreat to Corunna",
        dates: "December 1808 – January 1809",
        note: "Moore struck from Salamanca at Soult's corps at Sahagún, then, with Napoleon closing in, retreated over the Galician mountains in the snow to Corunna and the fleet.",
        path: [
          [40.96, -5.66],
          [41.52, -5.39],
          [42.37, -5.03],
          [42.0, -5.68],
          [42.46, -6.06],
          [43.01, -7.56],
          [43.37, -8.4],
        ],
      },
      {
        side: "allied",
        name: "Wellesley's Talavera campaign",
        dates: "June–July 1809",
        note: "From Abrantes Wellesley marched up the Tagus by Plasencia to join Cuesta's Spanish army and fight Joseph and Victor at Talavera.",
        path: [
          [39.46, -8.2],
          [39.9, -7.3],
          [40.03, -6.09],
          [39.96, -4.83],
        ],
      },
      {
        side: "allied",
        name: "Beresford against Soult",
        dates: "April–May 1811",
        note: "Beresford's Anglo-Portuguese corps crossed the Guadiana to besiege Badajoz and turned to meet Soult's relief at Albuera.",
        path: [
          [38.88, -7.16],
          [38.88, -6.97],
          [38.72, -6.82],
        ],
      },
      {
        side: "allied",
        name: "The Salamanca campaign",
        dates: "June–August 1812",
        note: "After storming Ciudad Rodrigo and Badajoz, Wellington advanced on Salamanca, broke Marmont's army there, and entered Madrid.",
        path: [
          [40.6, -6.53],
          [40.91, -5.6],
          [40.7, -4.7],
          [40.42, -3.7],
        ],
      },
      {
        side: "allied",
        name: "Wellington's advance to Vitoria",
        dates: "May–June 1813",
        note: "Wellington swung north of the Douro and round the French flank by Toro and Palencia, turning every line they tried to hold until he caught Joseph at Vitoria.",
        path: [
          [40.62, -6.9],
          [40.96, -5.66],
          [41.52, -5.39],
          [42.01, -4.53],
          [42.6, -3.9],
          [42.85, -2.67],
        ],
      },
      {
        side: "allied",
        name: "Over the Pyrenees to Toulouse",
        dates: "July 1813 – April 1814",
        note: "Wellington held Soult's counter-stroke at Sorauren, crossed the Bidassoa into France, stormed the Nivelle lines, beat Soult again at Orthez and followed him to Toulouse.",
        path: [
          [42.85, -2.67],
          [42.86, -1.62],
          [43.33, -1.75],
          [43.36, -1.6],
          [43.49, -0.77],
          [43.6, 1.44],
        ],
      },
      {
        side: "spanish",
        name: "Castaños traps Dupont",
        dates: "July 1808",
        note: "Castaños's Army of Andalusia marched up the Guadalquivir from Seville and closed round Dupont's corps on the road at Bailén.",
        path: [
          [37.39, -5.98],
          [37.7, -4.6],
          [38.0, -3.95],
          [38.09, -3.78],
        ],
      },
      {
        side: "spanish",
        name: "Blake and Cuesta in Old Castile",
        dates: "July 1808",
        note: "Blake's Army of Galicia came down from the mountains to join Cuesta, and both were routed by Bessières at Medina de Rioseco.",
        path: [
          [43.01, -7.56],
          [42.46, -6.06],
          [41.88, -5.04],
        ],
      },
      {
        side: "spanish",
        name: "Areizaga marches on Madrid",
        dates: "November 1809",
        note: "The Spanish Army of La Mancha marched north from the Sierra Morena to retake Madrid and was destroyed on the plain at Ocaña.",
        path: [
          [38.28, -3.62],
          [39.2, -3.4],
          [39.96, -3.5],
        ],
      },
    ],
  },
};
