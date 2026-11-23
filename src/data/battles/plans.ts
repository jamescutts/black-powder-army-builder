// Period maps of each battle, shown on its page in a viewer that pans and zooms over the scan. Keyed by battle
// id, and kept apart from the battles' files so the generators that write those can't overwrite them.
//
// Each plan is a public-domain or openly licensed scan on Wikimedia Commons. The viewer shows a lighter copy
// (`preview`, one of Commons' standard thumbnail widths) until it's zoomed in past it, then the full scan.

export interface BattlePlan {
  /** e.g. "Johnston, 1848", the plan's name on its tab */
  label: string;
  /** The plan's own title, e.g. "Battle of Bautzen, 20 & 21 May 1813" */
  title: string;
  /** Who drew, engraved or published it */
  maker: string;
  /** e.g. "1848", "c. 1824" */
  date: string;
  /** The collection the scan comes from */
  collection: string;
  /** The scan's Commons page, for its full description and licence */
  page: string;
  licence: string;
  /** The full scan, and its size in pixels */
  src: string;
  width: number;
  height: number;
  /** A lighter copy, shown until the viewer is zoomed in past its detail */
  preview: { src: string; width: number };
  /** The part of the scan the viewer opens on and keeps within, in the full scan's pixels: [left, top, right,
   *  bottom]. Leaves out the binding, margins and blank paper round the map itself. */
  crop?: [number, number, number, number];
  /** Degrees to turn the scan counter-clockwise, for one photographed a little askew on its page; the crop is of
   *  the scan as turned */
  rotate?: number;
  /** Anything the reader should know: what it covers, which way is north */
  note?: string;
}

const commons = (path: string) => `https://upload.wikimedia.org/wikipedia/commons/${path}`;

// The Boston Public Library's IIIF image server: a region of a scan, at a width, cut out by the server
const bpl = (id: string, [x, y, w, h]: [number, number, number, number], width = "full") =>
  `https://iiif.digitalcommonwealth.org/iiif/2/commonwealth:${id}/${x},${y},${w},${h}/${width === "full" ? "full" : `${width},`}/0/default.jpg`;

// The French campaign sheet no. 1 of 1813, cut to its inset plan of Lützen
const LUTZEN_INSET: [number, number, number, number] = [270, 325, 1890, 1405];

export const battlePlans: Record<string, BattlePlan[]> = {
  mockern: [
    {
      label: "Modern map, after Friederich",
      title: "Gefechte bei Möckern, 5. April 1813",
      maker: "Drawn by Memnon335bc after the sketch in Rudolf Friederich's Die Befreiungskriege 1813–1815 (1911)",
      date: "2010",
      collection: "Drawn for Wikipedia",
      page: "https://commons.wikimedia.org/wiki/File:Karte_-_Gefechte_bei_M%C3%B6ckern_(5._April_1813).png",
      licence: "CC BY-SA 3.0",
      src: commons("b/bf/Karte_-_Gefechte_bei_M%C3%B6ckern_%285._April_1813%29.png"),
      width: 1582,
      height: 925,
      preview: { src: commons("b/bf/Karte_-_Gefechte_bei_M%C3%B6ckern_%285._April_1813%29.png"), width: 1582 },
      note: "A modern map: no plan of the April fight from the time is to be found online. The three fights at Dannigkow, Vehlitz and Zeddenick east of Magdeburg; French red, allies blue. North is at the top.",
    },
  ],
  lutzen: [
    {
      label: "Johnston, 1848",
      title: "Battle of Lutzen, 2nd May 1813",
      maker: "Alexander Keith Johnston, for the Atlas to Alison's History of Europe (William Blackwood and Sons)",
      date: "1848",
      collection: "David Rumsey Map Collection",
      page: "https://commons.wikimedia.org/wiki/File:Battle_of_Lutzen,_2_May_1813._A.K._Johnston_F.R.G.S._William_Blackwood_and_Sons,_Edinburgh_and_London._(to_accompany)_Atlas_to_(IA_dr_battle-of-lutzen-2-may-1813-ak-johnston-frgs-william-blackwood-and-13200091).jpg",
      licence: "Public domain",
      src: commons(
        "f/fe/Battle_of_Lutzen%2C_2_May_1813._A.K._Johnston_F.R.G.S._William_Blackwood_and_Sons%2C_Edinburgh_and_London._%28to_accompany%29_Atlas_to_%28IA_dr_battle-of-lutzen-2-may-1813-ak-johnston-frgs-william-blackwood-and-13200091%29.jpg"
      ),
      width: 6125,
      height: 4822,
      preview: {
        src: commons(
          "thumb/f/fe/Battle_of_Lutzen%2C_2_May_1813._A.K._Johnston_F.R.G.S._William_Blackwood_and_Sons%2C_Edinburgh_and_London._%28to_accompany%29_Atlas_to_%28IA_dr_battle-of-lutzen-2-may-1813-ak-johnston-frgs-william-blackwood-and-13200091%29.jpg/1920px-thumbnail.jpg"
        ),
        width: 1920,
      },
      // Photographed askew like Bautzen's, from the same atlas: the border drops 37px across 3,300
      rotate: 0.65,
      crop: [800, 915, 4982, 3972],
      note: "Ney's villages south of Lützen, Gross- and Klein-Görschen, Rahna and Kaja, and the allied attack on them; French blue, allies red. North is at the top.",
    },
    {
      label: "Bataille de Lutzen, 1813",
      title: "Situation des armées françaises depuis le 10 mars jusqu'à la bataille de Wurtchen (Campagne de 1813), no. 1",
      maker: "Published in Paris by Lenormant",
      date: "1813",
      collection: "Norman B. Leventhal Map & Education Center, Boston Public Library",
      page: "https://collections.leventhalmap.org/search/commonwealth:6w924q50f",
      licence: "No known copyright restrictions",
      src: bpl("6w924q51q", LUTZEN_INSET),
      width: LUTZEN_INSET[2],
      height: LUTZEN_INSET[3],
      preview: { src: bpl("6w924q51q", LUTZEN_INSET, "1280"), width: 1280 },
      crop: [8, 8, 1882, 1397],
      note: "The French view, published the year of the battle, from the inset in the corner of the first sheet of the 1813 campaign: the whole country from Naumburg and Weissenfels to Leipzig, with the armies' marches before and after the battle; French blue, allies green. North is at the top.",
    },
  ],
  bautzen: [
    {
      label: "Johnston, 1848",
      title: "Battle of Bautzen, 20 & 21 May 1813",
      maker: "Alexander Keith Johnston, for the Atlas to Alison's History of Europe (William Blackwood and Sons)",
      date: "1848",
      collection: "David Rumsey Map Collection",
      page: "https://commons.wikimedia.org/wiki/File:Battle_of_Bautzen,_20_%26_21_May_1813._A.K._Johnston_F.R.G.S._William_Blackwood_and_Sons,_Edinburgh_and_London._(to_accompany)_Atlas_(IA_dr_battle-of-bautzen-20-21-may-1813-ak-johnston-frgs-william-blackwo-13200092).jpg",
      licence: "Public domain",
      src: commons(
        "4/41/Battle_of_Bautzen%2C_20_%26_21_May_1813._A.K._Johnston_F.R.G.S._William_Blackwood_and_Sons%2C_Edinburgh_and_London._%28to_accompany%29_Atlas_%28IA_dr_battle-of-bautzen-20-21-may-1813-ak-johnston-frgs-william-blackwo-13200092%29.jpg"
      ),
      width: 6087,
      height: 4782,
      preview: {
        src: commons(
          "thumb/4/41/Battle_of_Bautzen%2C_20_%26_21_May_1813._A.K._Johnston_F.R.G.S._William_Blackwood_and_Sons%2C_Edinburgh_and_London._%28to_accompany%29_Atlas_%28IA_dr_battle-of-bautzen-20-21-may-1813-ak-johnston-frgs-william-blackwo-13200092%29.jpg/1920px-thumbnail.jpg"
        ),
        width: 1920,
      },
      // The page was photographed a little clockwise of square: the map's border drops 36px across 3,300
      rotate: 0.65,
      crop: [782, 818, 4882, 3952],
      note: "Both days of the battle: the positions of the 20th coloured light, of the 21st dark; French blue, allies red. North is at the top.",
    },
    {
      label: "Bataille de Wurtchen, 1813",
      title: "Bataille de Wurtchen et tableau des opérations militaires jusqu'au mois d'octobre (Campagne de 1813), no. 2",
      maker: "Published in Paris by Magimel, Goujon and Bance",
      date: "1813",
      collection: "Bibliothèque nationale de France",
      page: "https://commons.wikimedia.org/wiki/File:Bataille_de_Wurtchen_et_tableau_des_op%C3%A9rations_militaires_jusqu%27au_mois_d%27octobre_(campagne_de_1813),_n%C2%B0_2_-_btv1b53047128n_(4_of_7).jpg",
      licence: "Public domain",
      src: commons(
        "9/9d/Bataille_de_Wurtchen_et_tableau_des_op%C3%A9rations_militaires_jusqu%27au_mois_d%27octobre_%28campagne_de_1813%29%2C_n%C2%B0_2_-_btv1b53047128n_%284_of_7%29.jpg"
      ),
      width: 6909,
      height: 5861,
      preview: {
        src: commons(
          "thumb/9/9d/Bataille_de_Wurtchen_et_tableau_des_op%C3%A9rations_militaires_jusqu%27au_mois_d%27octobre_%28campagne_de_1813%29%2C_n%C2%B0_2_-_btv1b53047128n_%284_of_7%29.jpg/1920px-Bataille_de_Wurtchen_et_tableau_des_op%C3%A9rations_militaires_jusqu%27au_mois_d%27octobre_%28campagne_de_1813%29%2C_n%C2%B0_2_-_btv1b53047128n_%284_of_7%29.jpg"
        ),
        width: 1920,
      },
      crop: [590, 1030, 3160, 3140],
      note: "The French view, published the year of the battle: the inset plan of the whole field from the corner of a sheet of the 1813 campaign, Bautzen and the Spree on the left, Würschen, which gave the battle its French name, on the right, with both armies' positions in colour.",
    },
    {
      label: "Brügner and Jäck, c. 1824 (right sheet)",
      title: "Die Schlacht von Bautzen den 21ten May 1813",
      maker: "Drawn by Carl Brügner, engraved by Carl Jäck, printed by J. D. Hampe",
      date: "c. 1824",
      collection: "Leibniz-Institut für Länderkunde, Leipzig",
      page: "https://commons.wikimedia.org/wiki/File:Die_Schlacht_von_Bautzen_den_21ten_May_1813.jpg",
      licence: "CC0",
      src: commons("3/3c/Die_Schlacht_von_Bautzen_den_21ten_May_1813.jpg"),
      width: 3256,
      height: 7122,
      preview: {
        src: commons("thumb/3/3c/Die_Schlacht_von_Bautzen_den_21ten_May_1813.jpg/1280px-Die_Schlacht_von_Bautzen_den_21ten_May_1813.jpg"),
        width: 1280,
      },
      crop: [370, 790, 2910, 6930],
      note: "The second day, with the troops' positions in colour. Only the right-hand sheet of the two is in this copy, and the left, with Bautzen itself, isn't to be found online: the northern flank, from Brösa and Gotta south to Gröditz, where Ney and Lauriston came round the allied right, with an inset of the country round Königswartha. North-west is at the top.",
    },
  ],
};
