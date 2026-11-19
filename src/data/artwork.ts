// Paintings for the home page cards, keyed by rule set or supplement id. All public domain, served by
// Wikimedia Commons (960px copies, plenty for a card); `page` is each painting's Commons page.

export interface Artwork {
  src: string;
  title: string;
  artist: string;
  page: string;
}

export const ARTWORK: Record<string, Artwork> = {
  "black-powder": {
    src: "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/01/Preu%C3%9Fische_Grenadier-Bataillone_schlagen_die_Sachsische_Garde.jpg/960px-Preu%C3%9Fische_Grenadier-Bataillone_schlagen_die_Sachsische_Garde.jpg",
    title: "Prussian grenadiers at Hohenfriedberg, 1745",
    artist: "Carl Röchling",
    page: "https://commons.wikimedia.org/wiki/File:Preu%C3%9Fische_Grenadier-Bataillone_schlagen_die_Sachsische_Garde.jpg",
  },
  "clash-of-eagles": {
    src: "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6d/Peter_von_Hess_002.jpg/960px-Peter_von_Hess_002.jpg",
    title: "The Battle of Borodino",
    artist: "Peter von Hess",
    page: "https://commons.wikimedia.org/wiki/File:Peter_von_Hess_002.jpg",
  },
  "albion-triumphant-1": {
    src: "https://upload.wikimedia.org/wikipedia/commons/1/13/James_Beadle_-_Battle_of_Vitoria%2C_21_June_1813_-_1913.jpg",
    title: "The Battle of Vitoria, 1813",
    artist: "James Prinsep Beadle",
    page: "https://commons.wikimedia.org/wiki/File:James_Beadle_-_Battle_of_Vitoria,_21_June_1813_-_1913.jpg",
  },
  "albion-triumphant-2": {
    src: "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e3/Scotland_Forever%21.jpg/960px-Scotland_Forever%21.jpg",
    title: "Scotland Forever!",
    artist: "Elizabeth Thompson",
    page: "https://commons.wikimedia.org/wiki/File:Scotland_Forever!.jpg",
  },
};
