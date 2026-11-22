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

// Paintings for the Peninsular War's battles still to come
ocana.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Bataille_d%27Oca%C3%B1a%2C_19_novembre_1809.jpg/960px-Bataille_d%27Oca%C3%B1a%2C_19_novembre_1809.jpg",
  "title": "The Battle of Ocaña",
  "artist": "after Adolphe Roehn",
  "page": "https://commons.wikimedia.org/wiki/File:Bataille_d%27Oca%C3%B1a%2C_19_novembre_1809.jpg"
};
fuentesDeOnoro.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Battle_of_Fuentes_d%27Onoro%2C_1811.jpg/960px-Battle_of_Fuentes_d%27Onoro%2C_1811.jpg",
  "title": "The Battle of Fuentes de Oñoro",
  "artist": "George Bryant Campion",
  "page": "https://commons.wikimedia.org/wiki/File:Battle_of_Fuentes_d%27Onoro%2C_1811.jpg"
};
sorauren.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Sorauren._Field_of_battle._1824._Edward_Hawke_Locker.jpg/960px-Sorauren._Field_of_battle._1824._Edward_Hawke_Locker.jpg",
  "title": "The field of Sorauren",
  "artist": "Edward Hawke Locker",
  "date": "1824",
  "page": "https://commons.wikimedia.org/wiki/File:Sorauren._Field_of_battle._1824._Edward_Hawke_Locker.jpg"
};
nivelle.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Bataille_de_la_Nivelle.jpg/960px-Bataille_de_la_Nivelle.jpg",
  "title": "The Battle of the Nivelle",
  "artist": "William Heath and James Jenkins",
  "date": "1831",
  "page": "https://commons.wikimedia.org/wiki/File:Bataille_de_la_Nivelle.jpg"
};
orthez.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Denis_Dighton_Battle_of_Orthez.jpg/960px-Denis_Dighton_Battle_of_Orthez.jpg",
  "title": "The final charge of the British cavalry at Orthez",
  "artist": "Denis Dighton",
  "date": "1815",
  "page": "https://commons.wikimedia.org/wiki/File:Denis_Dighton_Battle_of_Orthez.jpg"
};

toulouse.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Battle_of_Toulouse.jpg/960px-Battle_of_Toulouse.jpg",
  "title": "The Battle of Toulouse",
  "artist": "Henri Louis Dupray",
  "date": "c. 1890",
  "page": "https://commons.wikimedia.org/wiki/File:Battle_of_Toulouse.jpg"
};

// The Peninsular War's sieges: the storms of the breaches were fights of their own
export const saragossa = planned("saragossa", "First Siege of Saragossa", "15 June – 14 August 1808", P,
  "Palafox's citizens and soldiers held the walled city street by street against Verdier's assaults, until news of Bailén drew the French off.");
export const saragossa2 = planned("saragossa-2", "Second Siege of Saragossa", "20 December 1808 – 20 February 1809", P,
  "Lannes's corps came back and took the city house by house in two months of mining and street fighting, as fever and fire killed tens of thousands within its walls.");
export const gerona = planned("gerona", "Siege of Gerona", "6 May – 10 December 1809", P,
  "Álvarez de Castro's garrison beat off assault after assault on the Catalan fortress for seven months, until starvation and disease forced its surrender.");
export const almeida = planned("almeida", "Siege of Almeida", "25 July – 28 August 1810", P,
  "Masséna's siege of the Portuguese border fortress ended in a day, when a shell touched off the magazine and the explosion levelled the castle.");
export const tarragona = planned("tarragona", "Siege of Tarragona", "5 May – 29 June 1811", P,
  "Suchet's Army of Aragon besieged the great Catalan port and stormed its walls, sacking the city and winning his marshal's baton.");
export const ciudadRodrigo = planned("ciudad-rodrigo", "Ciudad Rodrigo", "7–19 January 1812", P,
  "Wellington took the border fortress in midwinter in twelve days, storming its two breaches by night; Craufurd was killed at the lesser breach.");
export const badajoz = planned("badajoz", "Badajoz", "16 March – 6 April 1812", P,
  "The bloodiest storm of the war: the Light and 4th Divisions failed again and again at the breaches while Picton's 3rd Division took the castle by escalade and Leith's 5th the San Vicente bastion.");
export const burgos = planned("burgos", "Siege of Burgos", "19 September – 21 October 1812", P,
  "Wellington's attempt on the castle of Burgos, with too few guns, failed after five assaults, and began the retreat from Burgos.");
export const sanSebastian = planned("san-sebastian", "San Sebastián", "7 July – 8 September 1813", P,
  "Graham's besiegers stormed the breach at the second attempt, under covering fire shot over their heads, and the town burned in the sack that followed.");
export const pamplona = planned("pamplona", "Siege of Pamplona", "26 June – 31 October 1813", P,
  "Blockaded by Spanish troops after Vitoria, the fortress was the aim of Soult's counter-offensive in the Pyrenees, and held out until starved into surrender.");

// Paintings for the sieges
saragossa.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Girardet-Siege_of_Saragossa.jpg/960px-Girardet-Siege_of_Saragossa.jpg",
  "title": "The Siege of Saragossa",
  "artist": "Jules Girardet",
  "date": "1906",
  "page": "https://commons.wikimedia.org/wiki/File:Girardet-Siege_of_Saragossa.jpg"
};
saragossa2.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Siege_of_Saragossa.jpg/960px-Siege_of_Saragossa.jpg",
  "title": "The Siege of Saragossa",
  "artist": "Horace Vernet",
  "date": "1819",
  "page": "https://commons.wikimedia.org/wiki/File:Siege_of_Saragossa.jpg",
  "focus": "50% 45%"
};
gerona.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/b/bb/Des1809-Girona-Pronostich1847.jpg",
  "title": "The Siege of Gerona, 1809",
  "artist": "unknown artist",
  "date": "c. 1846",
  "page": "https://commons.wikimedia.org/wiki/File:Des1809-Girona-Pronostich1847.jpg"
};
tarragona.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/2/20/Remond_-_Prise_de_Tarragone_en_Catalogne_par_le_g%C3%A9n%C3%A9ral_en_chef_Suchet%2C_le_28_juin_1811.jpg",
  "title": "The Taking of Tarragona by Suchet",
  "artist": "Jean-Charles-Joseph Rémond",
  "date": "1837",
  "page": "https://commons.wikimedia.org/wiki/File:Remond_-_Prise_de_Tarragone_en_Catalogne_par_le_g%C3%A9n%C3%A9ral_en_chef_Suchet%2C_le_28_juin_1811.jpg"
};
ciudadRodrigo.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/P427_STORMING_OF_THE_FORTRESS_CIUDAD_RODRIGO_BY_THE_ENGLISH_UNDER_LORD_WELLINGTON_1812.jpg/960px-P427_STORMING_OF_THE_FORTRESS_CIUDAD_RODRIGO_BY_THE_ENGLISH_UNDER_LORD_WELLINGTON_1812.jpg",
  "title": "The Storming of Ciudad Rodrigo",
  "artist": "from Cassell's history",
  "date": "1865",
  "page": "https://commons.wikimedia.org/wiki/File:P427_STORMING_OF_THE_FORTRESS_CIUDAD_RODRIGO_BY_THE_ENGLISH_UNDER_LORD_WELLINGTON_1812.jpg",
  "focus": "50% 40%"
};
badajoz.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Siege_of_Badajoz%2C_by_Richard_Caton_Woodville_Jr.jpg/960px-Siege_of_Badajoz%2C_by_Richard_Caton_Woodville_Jr.jpg",
  "title": "The Storming of Badajoz",
  "artist": "Richard Caton Woodville Jr.",
  "date": "1908",
  "page": "https://commons.wikimedia.org/wiki/File:Siege_of_Badajoz%2C_by_Richard_Caton_Woodville_Jr.jpg"
};
burgos.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Siege_of_burgos_1812_heim.jpg",
  "title": "The Siege of Burgos",
  "artist": "François Joseph Heim",
  "date": "1813",
  "page": "https://commons.wikimedia.org/wiki/File:Siege_of_burgos_1812_heim.jpg"
};
sanSebastian.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Asalto_a_San_Sebasti%C3%A1n_el_25_de_julio_de_1813.jpg/960px-Asalto_a_San_Sebasti%C3%A1n_el_25_de_julio_de_1813.jpg",
  "title": "The Assault on San Sebastián",
  "artist": "Denis Dighton",
  "date": "1813",
  "page": "https://commons.wikimedia.org/wiki/File:Asalto_a_San_Sebasti%C3%A1n_el_25_de_julio_de_1813.jpg"
};
