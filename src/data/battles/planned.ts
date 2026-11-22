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
export const valutino = planned("valutino", "Valutino", "19 August 1812", R,
  "Ney and Junot caught the Russian rearguard east of Smolensk at Lubino and fought it to a standstill, while Barclay's army got clear.");
export const borodino = planned("borodino", "Borodino", "7 September 1812", R,
  "Kutuzov's stand before Moscow: a day of assaults on the flèches and the Great Redoubt, the bloodiest single day of the wars, after which the Russians withdrew and Moscow fell.");
export const tarutino = planned("tarutino", "Tarutino", "18 October 1812", R,
  "Bennigsen surprised Murat's advance guard in its camp on the Chernishnya, the blow that helped decide Napoleon to leave Moscow.");
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
export const nivelle = planned("nivelle", "Nivelle", "10 November 1813", P,
  "Wellington stormed Soult's fortified lines along the Nivelle, carrying the war into France.");
export const toulouse = planned("toulouse", "Toulouse", "10 April 1814", P,
  "The war's last battle, fought for the heights east of the city before news came that Napoleon had already abdicated.");

// Paintings for the Peninsular War's battles still to come
ocana.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Bataille_d%27Oca%C3%B1a%2C_19_novembre_1809.jpg/960px-Bataille_d%27Oca%C3%B1a%2C_19_novembre_1809.jpg",
  "title": "The Battle of Ocaña",
  "artist": "after Adolphe Roehn",
  "page": "https://commons.wikimedia.org/wiki/File:Bataille_d%27Oca%C3%B1a%2C_19_novembre_1809.jpg"
};
nivelle.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Bataille_de_la_Nivelle.jpg/960px-Bataille_de_la_Nivelle.jpg",
  "title": "The Battle of the Nivelle",
  "artist": "William Heath and James Jenkins",
  "date": "1831",
  "page": "https://commons.wikimedia.org/wiki/File:Bataille_de_la_Nivelle.jpg"
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

const L = "liberation-1813";

export const lutzen = planned("lutzen", "Lützen", "2 May 1813", L,
  "Wittgenstein and Blücher fell on Ney's corps in its villages south of Lützen; Napoleon's young conscripts held Gross-Görschen and Kaja through the day until the Guard and the converging corps drove the allies off. Scharnhorst was mortally wounded.");
export const bautzen = planned("bautzen", "Bautzen", "20–21 May 1813", L,
  "Napoleon forced the Spree at Bautzen and next day attacked the allies' fortified line on the heights behind it, while Ney marched round their right; Ney came on too late and too cautiously, and the allies got away to Silesia. An armistice followed in June.");
export const grossbeeren = planned("grossbeeren", "Großbeeren", "23 August 1813", L,
  "Oudinot's march on Berlin, the first blow after the armistice, ran into Bülow's Prussians in the rain south of the city; they stormed Großbeeren from Reynier's Saxons, and Oudinot fell back on Wittenberg.");
export const katzbach = planned("katzbach", "The Katzbach", "26 August 1813", L,
  "Macdonald's army, crossing the swollen Katzbach and Wütende Neisse in a downpour, was caught by Blücher on the plateau beyond, muskets too wet to fire; driven back over flooded streams, it lost tens of thousands of men in the days after.");
export const dresden = planned("dresden", "Dresden", "26–27 August 1813", L,
  "Schwarzenberg's Army of Bohemia attacked Dresden just as Napoleon reached it with the Guard. Next day, in pouring rain, Murat's cavalry broke the Austrian left cut off by the flooded Weisseritz: Napoleon's last great victory in Germany.");
export const kulm = planned("kulm", "Kulm", "29–30 August 1813", L,
  "Vandamme's corps, pressing down from the mountains to cut off the allies retreating from Dresden, was held at Kulm by Ostermann-Tolstoy and the Russian Guard, then taken in the rear by Kleist's Prussians coming over the hills behind; Vandamme and most of his corps were captured.");
export const dennewitz = planned("dennewitz", "Dennewitz", "6 September 1813", L,
  "Ney, sent in Oudinot's place to take Berlin, marched across the front of Bülow's and Tauentzien's Prussians, and his corps were drawn into the fight one at a time; when Oudinot's moved to the wrong flank the line broke, and the Saxons and Bavarians began to waver in their allegiance.");
export const gohrde = planned("gohrde", "The Göhrde", "16 September 1813", L,
  "In the forests of the Göhrde, east of Lüneburg, Wallmoden's army of Russians, Hanoverians, the King's German Legion and Lützow's Free Corps surrounded and broke Pécheux's division of Davout's corps. Eleonore Prochaska, serving disguised as a man with Lützow's infantry, was mortally wounded there.");
export const wartenburg = planned("wartenburg", "Wartenburg", "3 October 1813", L,
  "Yorck's corps crossed the Elbe on pontoons in the river's bend at Wartenburg and assaulted Bertrand's corps, posted in the village behind dikes and marshes; Horn's brigade waded through the mud to take it, opening the way for Blücher's march to join the northern army before Leipzig.");
export const leipzig = planned("leipzig", "Leipzig", "16–19 October 1813", L,
  "The Battle of the Nations: four allied armies closed on Napoleon round Leipzig, at Wachau, Möckern and Lindenau on the 16th, and on the 18th from every side, as the Saxons went over. In the retreat on the 19th the Elster bridge was blown too soon, Poniatowski drowned, and the rearguard was lost.");
export const hanau = planned("hanau", "Hanau", "30–31 October 1813", L,
  "Wrede's Bavarians and Austrians, changed sides a fortnight before, stood across Napoleon's road home at Hanau with a river at their backs. Drouot massed the Guard's guns, the Guard cavalry broke the Bavarian left, and the Grande Armée's remnant marched on to the Rhine.");

const F = "france-1814";

export const brienne = planned("brienne", "Brienne", "29 January 1814", F,
  "Napoleon caught Blücher at Brienne, where he had been a cadet at the military school; Ney's infantry stormed the town and château by night, and Blücher, nearly taken, fell back on the Aube.");
export const laRothiere = planned("la-rothiere", "La Rothière", "1 February 1814", F,
  "Blücher, joined by much of Schwarzenberg's army, attacked Napoleon's outnumbered army at La Rothière in the snow; the village changed hands until nightfall, and the French drew off to Troyes, the first defeat on French soil.");
export const champaubert = planned("champaubert", "Champaubert", "10 February 1814", F,
  "The first of the Six Days: marching north through the mud, Napoleon fell on Olsufiev's isolated Russian corps strung out along Blücher's line of march, and destroyed it; Olsufiev was taken.");
export const montmirail = planned("montmirail", "Montmirail", "11 February 1814", F,
  "Napoleon turned west on Sacken's Russians and the leading brigades of Yorck's Prussians, coming back towards Montmirail; Ney and the Guard stormed the farm of Marchais, and the allies were driven north towards the Marne.");
export const chateauThierry = planned("chateau-thierry", "Château-Thierry", "12 February 1814", F,
  "Pursuing Sacken and Yorck to the Marne, the Guard cavalry and Ney's infantry caught their rearguards before Château-Thierry and drove them over the river, but the bridge was burnt behind them.");
export const vauchamps = planned("vauchamps", "Vauchamps", "14 February 1814", F,
  "Blücher, coming on with Kleist's and Kapzevich's corps against Marmont, met Napoleon instead; Grouchy's cavalry rode round the retreating allied squares, which fought their way back through the French horsemen to Étoges with heavy loss.");
export const montereau = planned("montereau", "Montereau", "18 February 1814", F,
  "Turning south on Schwarzenberg's army, Napoleon attacked the Crown Prince of Württemberg's corps holding the heights before Montereau; Pajol's cavalry charged down the road and over the bridges before they could be blown, and Napoleon himself laid guns, saying the ball that would kill him had not been cast.");
export const craonne = planned("craonne", "Craonne", "7 March 1814", F,
  "Napoleon attacked Vorontsov's and Sacken's Russians on the narrow Chemin des Dames plateau; Ney and Victor's Young Guard came on in costly frontal assaults until the Russians withdrew in good order, one of the bloodiest days of the campaign.");
export const laon = planned("laon", "Laon", "9–10 March 1814", F,
  "Blücher, with twice Napoleon's numbers, held the hill of Laon against him; on the night of the 9th Yorck and Kleist fell on Marmont's corps at Athies and routed it, and Napoleon, attacking again next day to no purpose, withdrew.");
export const reims = planned("reims", "Reims", "13 March 1814", F,
  "Napoleon fell on Saint-Priest's Russian and Prussian corps, which had taken Reims; Saint-Priest, an émigré Frenchman in Russian service, was mortally wounded, and the city was retaken.");
export const arcis = planned("arcis-sur-aube", "Arcis-sur-Aube", "20–21 March 1814", F,
  "Expecting a rearguard, Napoleon found Schwarzenberg's whole army before Arcis; the Guard held on through two days, Napoleon riding over a smoking shell, before the French crossed back over the Aube and he turned east against the allies' communications.");
export const fereChampenoise = planned("fere-champenoise", "Fère-Champenoise", "25 March 1814", F,
  "The allied cavalry, marching on Paris, rode down Marmont's and Mortier's corps on the plain, and then Pacthod's and Amey's National Guard divisions, which formed squares and fought on until the Tsar himself rode in to accept their surrender.");
export const paris = planned("paris", "Paris", "30 March 1814", F,
  "The allied armies attacked the heights of Belleville, Romainville and Montmartre, held by Marmont and Mortier with conscripts, National Guards and the pupils of the École Polytechnique; that night Marmont signed the capitulation, and the allies entered the city next day.");
