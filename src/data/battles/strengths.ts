// Each battle's strengths, as historians give them: men and guns on each side, with cavalry where the source
// splits it out, shown across the foot of the battle page's header in place of the forces' unit counts. Keyed by
// battle id, and kept apart from the battles' files so the generators that write those can't overwrite them.
//
// Figures are those of each battle's Wikipedia infobox (its Strength row), read in November 2026, kept as ranges
// where it gives them. Where it gives both an army's total and the part engaged, the part engaged is shown.

export interface SideStrength {
  /** The side, or sides together, as the battle names them (or as the source does, for one with no forces here) */
  label: string;
  men: string;
  guns?: string;
  cavalry?: string;
  /** Only part of the army fought: the men shown are those engaged */
  engaged?: boolean;
  /** Anything else the source counts separately, e.g. "and 20,000 Cossacks" */
  extra?: string;
}

export const battleStrengths: Record<string, SideStrength[]> = {
  // The Peninsular War
  rolica: [
    { label: "Anglo-Portuguese", men: "14,800–15,700", guns: "20" },
    { label: "French", men: "4,000–4,930", guns: "5" },
  ],
  "medina-de-rioseco": [
    { label: "French", men: "13,500–14,000", guns: "32", cavalry: "950–1,200" },
    { label: "Spanish", men: "21,900–22,600", guns: "20", cavalry: "600" },
  ],
  bailen: [
    { label: "French", men: "20,000–24,430" },
    { label: "Spanish", men: "29,770–30,000" },
  ],
  vimeiro: [
    { label: "Anglo-Portuguese", men: "17,000–20,500", guns: "18–19" },
    { label: "French", men: "13,000–14,000", guns: "23–24" },
  ],
  corunna: [
    { label: "British", men: "16,000", guns: "9–12", cavalry: "1,000" },
    { label: "French", men: "15,200", guns: "20", cavalry: "3,200" },
  ],
  talavera: [
    { label: "British", men: "20,641", guns: "30" },
    { label: "Spanish", men: "34,993", guns: "30" },
    { label: "French", men: "46,138", guns: "80" },
  ],
  bussaco: [
    { label: "French", men: "45,774–58,000" },
    { label: "Anglo-Portuguese", men: "32,000–35,765" },
  ],
  "fuentes-de-onoro": [
    { label: "Anglo-Portuguese", men: "34,850–38,000", guns: "48", cavalry: "1,850–2,000" },
    { label: "French", men: "44,500–47,000", guns: "38", cavalry: "4,500–5,000" },
  ],
  albuera: [
    { label: "Anglo-Portuguese and Spanish", men: "35,284" },
    { label: "French", men: "24,260" },
  ],
  salamanca: [
    { label: "Anglo-Portuguese", men: "46,000–51,949" },
    { label: "French", men: "42,000–49,647" },
  ],
  vitoria: [
    { label: "Anglo-Allied and Spanish", men: "81,000–90,000", guns: "96" },
    { label: "French", men: "57,000–60,000", guns: "153" },
  ],
  sorauren: [
    { label: "French", men: "30,000" },
    { label: "Anglo-Portuguese", men: "24,000" },
  ],
  orthez: [
    { label: "French", men: "34,993", guns: "48" },
    { label: "Anglo-Portuguese", men: "44,000", guns: "54" },
  ],

  // The Russian Campaign
  mir: [
    { label: "Polish", men: "3,600", guns: "3" },
    { label: "Russian", men: "8,500", guns: "12" },
  ],
  eckau: [
    { label: "Prussian", men: "7,000", guns: "32" },
    { label: "Russian", men: "3,000–4,000", guns: "10" },
  ],
  saltanovka: [
    { label: "French", men: "21,500–28,000", guns: "55", cavalry: "6,000" },
    { label: "Russian", men: "17,000–20,000", guns: "90" },
  ],
  ostrovno: [
    { label: "French", men: "23,000" },
    { label: "Russian", men: "14,000", guns: "66" },
  ],
  kobrin: [
    { label: "Saxon", men: "2,600", guns: "8", engaged: true },
    { label: "Russian", men: "12,000", guns: "36", engaged: true },
  ],
  klyastitsy: [
    { label: "French", men: "20,000", guns: "114", engaged: true },
    { label: "Russian", men: "17,000", guns: "108" },
  ],
  gorodechno: [
    { label: "Austrian and Saxon", men: "40,000" },
    { label: "Russian", men: "18,000" },
  ],
  smolensk: [
    { label: "French", men: "45,000", engaged: true },
    { label: "Russian", men: "30,000", engaged: true },
  ],
  polotsk: [
    { label: "French and Bavarian", men: "18,000–19,000", guns: "150", engaged: true },
    { label: "Russian", men: "17,000–22,000", guns: "98" },
  ],
  valutino: [
    { label: "French", men: "35,000" },
    { label: "Russian", men: "25,000" },
  ],
  dahlenkirchen: [
    { label: "Prussian", men: "1,500", guns: "8" },
    { label: "Russian", men: "6,000" },
  ],
  borodino: [
    { label: "French", men: "103,000–135,000" },
    { label: "Russian", men: "125,000–160,000" },
  ],
  mesoten: [
    { label: "Prussian", men: "16,000" },
    { label: "Russian", men: "22,000" },
  ],
  tarutino: [
    { label: "French", men: "20,000–26,000" },
    { label: "Russian", men: "36,000", engaged: true },
  ],
  "polotsk-2": [
    { label: "French and Bavarian", men: "23,000–27,000" },
    { label: "Russian", men: "40,000", extra: "and 9,000 militia" },
  ],
  maloyaroslavets: [
    { label: "French", men: "24,000" },
    { label: "Russian", men: "24,000" },
  ],
  vyazma: [
    { label: "French", men: "25,000", engaged: true },
    { label: "Russian", men: "27,000", guns: "80" },
  ],
  krasnoi: [
    { label: "French", men: "41,500", extra: "and 35,000 stragglers" },
    { label: "Russian", men: "50,000–60,000", guns: "500–600", extra: "and 20,000 Cossacks" },
  ],
  berezina: [
    { label: "French", men: "36,000", guns: "250–300", extra: "and 40,000 stragglers" },
    { label: "Russian", men: "61,500–64,000" },
  ],

  // The War of Liberation
  mockern: [
    { label: "French", men: "37,000–50,000", cavalry: "up to 4,000" },
    { label: "Russian and Prussian", men: "20,000–24,000", cavalry: "up to 5,000" },
  ],
  lutzen: [
    { label: "French", men: "78,000–145,000", guns: "372" },
    { label: "Russian and Prussian", men: "70,000–96,000", guns: "552" },
  ],
  bautzen: [
    { label: "French", men: "100,000–200,000" },
    { label: "Russian and Prussian", men: "96,000–97,000" },
  ],
  grossbeeren: [
    { label: "Saxon and French", men: "18,000", guns: "68" },
    { label: "Prussian", men: "32,000", guns: "82" },
  ],
  hanau: [
    { label: "French", men: "17,000–30,000" },
    { label: "Bavarian, Austrian and Russian", men: "43,000" },
  ],
  wartenburg: [
    { label: "French", men: "13,000–15,000", guns: "24" },
    { label: "Prussian", men: "16,000", guns: "64" },
  ],

  // The Hundred Days
  ligny: [
    { label: "French", men: "62,882", guns: "210" },
    { label: "Prussian", men: "83,417", guns: "224" },
  ],
  "quatre-bras": [
    { label: "French", men: "20,000–21,000" },
    { label: "Anglo-allied", men: "32,000–36,000" },
  ],
  waterloo: [
    { label: "Anglo-allied", men: "68,000", guns: "156" },
    { label: "French", men: "72,000–73,000", guns: "246–252", cavalry: "14,390–15,765" },
    { label: "Prussian", men: "50,000", guns: "126" },
  ],
  wavre: [
    { label: "French", men: "32,000–33,000", guns: "80" },
    { label: "Prussian", men: "17,000–24,000", guns: "48" },
  ],
};
