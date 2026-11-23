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
  /** Anything the reader should know: what it covers, which way is north */
  note?: string;
}

const commons = (path: string) => `https://upload.wikimedia.org/wikipedia/commons/${path}`;

export const battlePlans: Record<string, BattlePlan[]> = {
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
      crop: [790, 790, 4880, 3960],
      note: "Both days of the battle: the positions of the 20th coloured light, of the 21st dark; French blue, allies red. North is at the top.",
    },
    {
      label: "Brügner and Jäck, c. 1824",
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
      note: "The second day, with the troops' positions in colour. Only the right-hand sheet of the two survives in this copy: the northern flank, from Brösa and Gotta south to Gröditz, where Ney and Lauriston came round the allied right, with an inset of the country round Königswartha. North-west is at the top.",
    },
  ],
};
