import type { HistoricalBattle } from "../types";

// Battles still to come: listed in their campaign, in order, as cards saying so, with no page of their own
// until their forces are written. Summaries are our own words.

const planned = (id: string, name: string, date: string, campaign: string, summary: string): HistoricalBattle => ({
  id,
  name,
  date,
  campaign,
  summary,
  sources: [],
  forces: [],
});

const R = "russia-1812";

export const smolensk = planned("smolensk", "Smolensk", "16–18 August 1812", R,
  "Napoleon assaulted the walled city, held by Raevsky and then Dokhturov while the Russian armies withdrew; it burned before they left it.");
export const polotsk = planned("polotsk", "First Polotsk", "17–18 August 1812", R,
  "Saint-Cyr, taking over from the wounded Oudinot, beat Wittgenstein's attack and won his marshal's baton.");
export const valutino = planned("valutino", "Valutino", "19 August 1812", R,
  "Ney and Junot caught the Russian rearguard east of Smolensk at Lubino and fought it to a standstill, while Barclay's army got clear.");
export const borodino = planned("borodino", "Borodino", "7 September 1812", R,
  "Kutuzov's stand before Moscow: a day of assaults on the flèches and the Great Redoubt, the bloodiest single day of the wars, after which the Russians withdrew and Moscow fell.");
export const tarutino = planned("tarutino", "Tarutino", "18 October 1812", R,
  "Bennigsen surprised Murat's advance guard in its camp on the Chernishnya, the blow that helped decide Napoleon to leave Moscow.");
export const polotsk2 = planned("polotsk-2", "Second Polotsk", "18–20 October 1812", R,
  "Reinforced, Wittgenstein stormed Polotsk and drove Saint-Cyr out, threatening the Grande Armée's line of retreat.");
export const maloyaroslavets = planned("maloyaroslavets", "Maloyaroslavets", "24 October 1812", R,
  "Eugène's corps and Dokhturov's fought all day for the burning town, which changed hands again and again; Napoleon turned back onto the ruined Smolensk road.");
export const vyazma = planned("vyazma", "Vyazma", "3 November 1812", R,
  "Miloradovich fell on the French rearguard of Davout, Eugène and Ney during the retreat, cutting at its columns before they got through.");
export const krasnoi = planned("krasnoi", "Krasnoi", "15–18 November 1812", R,
  "Kutuzov's army struck the retreating columns as they passed; the Young Guard fought to keep the road open, and Ney's cut-off rearguard escaped across the Dnieper.");
export const berezina = planned("berezina", "Berezina", "26–29 November 1812", R,
  "Eblé's pontonniers bridged the river at Studienka while Oudinot and Victor held off the converging Russian armies on both banks, and the Grande Armée's remnant crossed.");

// Paintings for the Russian campaign's battles still to come
smolensk.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Smolensk_by_hess.jpg/960px-Smolensk_by_hess.jpg",
  "title": "The Battle of Smolensk",
  "artist": "Peter von Hess",
  "date": "1846",
  "page": "https://commons.wikimedia.org/wiki/File:Smolensk_by_hess.jpg"
};
polotsk.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Battle_of_Polotsk.Print_by_Jean_Charles_Langlois.1838.png/960px-Battle_of_Polotsk.Print_by_Jean_Charles_Langlois.1838.png",
  "title": "The Battle of Polotsk, 18 August 1812",
  "artist": "Jean-Charles Langlois",
  "date": "1838",
  "page": "https://commons.wikimedia.org/wiki/File:Battle_of_Polotsk.Print_by_Jean_Charles_Langlois.1838.png"
};
valutino.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Battle_of_Valutino.jpg/960px-Battle_of_Valutino.jpg",
  "title": "The Battle of Valutino",
  "artist": "Peter von Hess",
  "page": "https://commons.wikimedia.org/wiki/File:Battle_of_Valutino.jpg"
};
borodino.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Battle_of_Borodino_on_26_August_%287_September%29_1812_%28by_Peter_von_Hess%2C_original_colors_version%29.jpg/960px-Battle_of_Borodino_on_26_August_%287_September%29_1812_%28by_Peter_von_Hess%2C_original_colors_version%29.jpg",
  "title": "The Battle of Borodino",
  "artist": "Peter von Hess",
  "date": "1843",
  "page": "https://commons.wikimedia.org/wiki/File:Battle_of_Borodino_on_26_August_%287_September%29_1812_%28by_Peter_von_Hess%2C_original_colors_version%29.jpg"
};
tarutino.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Tarutino.jpg/960px-Tarutino.jpg",
  "title": "The Battle of Tarutino",
  "artist": "Peter von Hess",
  "date": "1847",
  "page": "https://commons.wikimedia.org/wiki/File:Tarutino.jpg"
};
polotsk2.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/%D0%A8%D1%82%D1%83%D1%80%D0%BC_%D0%9F%D0%BE%D0%BB%D0%BE%D1%86%D0%BA%D0%B0_%28%D0%BB%D0%B8%D1%82%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F_%D0%9D.%D0%A1._%D0%A1%D0%B0%D0%BC%D0%BE%D0%BA%D0%B8%D1%88%D0%B0%29.jpg/960px-%D0%A8%D1%82%D1%83%D1%80%D0%BC_%D0%9F%D0%BE%D0%BB%D0%BE%D1%86%D0%BA%D0%B0_%28%D0%BB%D0%B8%D1%82%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F_%D0%9D.%D0%A1._%D0%A1%D0%B0%D0%BC%D0%BE%D0%BA%D0%B8%D1%88%D0%B0%29.jpg",
  "title": "The Storming of Polotsk",
  "artist": "Nikolai Samokysh",
  "page": "https://commons.wikimedia.org/wiki/File:%D0%A8%D1%82%D1%83%D1%80%D0%BC_%D0%9F%D0%BE%D0%BB%D0%BE%D1%86%D0%BA%D0%B0_%28%D0%BB%D0%B8%D1%82%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F_%D0%9D.%D0%A1._%D0%A1%D0%B0%D0%BC%D0%BE%D0%BA%D0%B8%D1%88%D0%B0%29.jpg"
};
maloyaroslavets.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Hess_maloyaroslavets.jpg/960px-Hess_maloyaroslavets.jpg",
  "title": "The Battle of Maloyaroslavets",
  "artist": "Peter von Hess",
  "page": "https://commons.wikimedia.org/wiki/File:Hess_maloyaroslavets.jpg"
};
vyazma.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Battle_vyazma.jpg/960px-Battle_vyazma.jpg",
  "title": "The Battle of Vyazma",
  "artist": "Peter von Hess",
  "page": "https://commons.wikimedia.org/wiki/File:Battle_vyazma.jpg"
};
krasnoi.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Krasnoi.jpg/960px-Krasnoi.jpg",
  "title": "The Battle of Krasnoi",
  "artist": "Peter von Hess",
  "date": "1849",
  "page": "https://commons.wikimedia.org/wiki/File:Krasnoi.jpg"
};
berezina.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Crossing_the_Berezina_River%2C_by_Peter_von_Hess.jpg/960px-Crossing_the_Berezina_River%2C_by_Peter_von_Hess.jpg",
  "title": "The Crossing of the Berezina",
  "artist": "Peter von Hess",
  "date": "1844",
  "page": "https://commons.wikimedia.org/wiki/File:Crossing_the_Berezina_River%2C_by_Peter_von_Hess.jpg"
};

const P = "peninsular-war";

export const medinaDeRioseco = planned("medina-de-rioseco", "Medina de Rioseco", "14 July 1808", P,
  "Bessières routed the Spanish armies of Cuesta and Blake in Old Castile, opening the road to Madrid for King Joseph.");
export const bailen = planned("bailen", "Bailén", "16–19 July 1808", P,
  "Castaños's Spanish army trapped Dupont's corps in the heat of Andalusia and forced it to surrender, the first great defeat of a French army in the field.");
export const somosierra = planned("somosierra", "Somosierra", "30 November 1808", P,
  "The Polish light horse of the Guard charged up the mountain pass through the Spanish batteries, opening the way to Madrid.");
// Battles still to come can have their painting already
somosierra.art = {
  src: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Louis-Fran%C3%A7ois_Lejeune_-_Battle_of_Somosierra%2C_November_30%2C_1808.jpg/960px-Louis-Fran%C3%A7ois_Lejeune_-_Battle_of_Somosierra%2C_November_30%2C_1808.jpg",
  title: "The Battle of Somosierra",
  artist: "Louis-François Lejeune",
  date: "1810",
  page: "https://commons.wikimedia.org/wiki/File:Louis-Fran%C3%A7ois_Lejeune_-_Battle_of_Somosierra,_November_30,_1808.jpg",
};
export const ocana = planned("ocana", "Ocaña", "19 November 1809", P,
  "Areizaga's Spanish army was broken on the plain south of Aranjuez by Soult and Mortier, its largest defeat of the war.");
export const bussaco = planned("bussaco", "Bussaco", "27 September 1810", P,
  "Masséna's corps climbed the long ridge of Bussaco against Wellington's Anglo-Portuguese line and were thrown back down it.");
export const fuentesDeOnoro = planned("fuentes-de-onoro", "Fuentes de Oñoro", "3–5 May 1811", P,
  "Masséna's attempt to relieve Almeida, fought out in the village's streets and on the open plain to its south.");
export const sorauren = planned("sorauren", "Sorauren", "28–30 July 1813", P,
  "Soult's drive through the Pyrenees to relieve Pamplona was stopped on the heights above Sorauren.");
export const nivelle = planned("nivelle", "Nivelle", "10 November 1813", P,
  "Wellington stormed Soult's fortified lines along the Nivelle, carrying the war into France.");
export const orthez = planned("orthez", "Orthez", "27 February 1814", P,
  "Wellington turned Soult out of his position on the ridge above Orthez and drove him east.");
export const toulouse = planned("toulouse", "Toulouse", "10 April 1814", P,
  "The war's last battle, fought for the heights east of the city before news came that Napoleon had already abdicated.");
