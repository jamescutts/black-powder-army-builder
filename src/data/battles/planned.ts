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


// Paintings for the Russian campaign's battles still to come

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

export const dresden = planned("dresden", "Dresden", "26–27 August 1813", L,
  "Schwarzenberg's Army of Bohemia attacked Dresden just as Napoleon reached it with the Guard. Next day, in pouring rain, Murat's cavalry broke the Austrian left cut off by the flooded Weisseritz: Napoleon's last great victory in Germany.");
export const kulm = planned("kulm", "Kulm", "29–30 August 1813", L,
  "Vandamme's corps, pressing down from the mountains to cut off the allies retreating from Dresden, was held at Kulm by Ostermann-Tolstoy and the Russian Guard, then taken in the rear by Kleist's Prussians coming over the hills behind; Vandamme and most of his corps were captured.");
export const gohrde = planned("gohrde", "The Göhrde", "16 September 1813", L,
  "In the forests of the Göhrde, east of Lüneburg, Wallmoden's army of Russians, Hanoverians, the King's German Legion and Lützow's Free Corps surrounded and broke Pécheux's division of Davout's corps. Eleonore Prochaska, serving disguised as a man with Lützow's infantry, was mortally wounded there.");
export const leipzig = planned("leipzig", "Leipzig", "16–19 October 1813", L,
  "The Battle of the Nations: four allied armies closed on Napoleon round Leipzig, at Wachau, Möckern and Lindenau on the 16th, and on the 18th from every side, as the Saxons went over. In the retreat on the 19th the Elster bridge was blown too soon, Poniatowski drowned, and the rearguard was lost.");

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

// More of 1813: the smaller actions and the sieges
export const danzig = planned("danzig", "Siege of Danzig", "16 January – 29 November 1813", L,
  "Rapp held the Vistula fortress with the frozen remnants of the Grande Armée and a garrison of a dozen nations through the whole of 1813, beating off Russian and Prussian besiegers until hunger and disease forced him to terms in November.");
export const luneburg = planned("luneburg", "Lüneburg", "2 April 1813", L,
  "Dörnberg's and Chernyshev's flying columns stormed Lüneburg, held by Morand's small division, and took most of it prisoner after the townspeople helped them in: the first allied victory of the war in Germany.");
export const haynau = planned("haynau", "Haynau", "26 May 1813", L,
  "Blücher laid an ambush for the French advance guard in Silesia: Maison's division, marching carelessly through Haynau, was charged by Prussian cavalry hidden behind a ridge and lost its guns and hundreds of prisoners.");
export const kitzen = planned("kitzen", "Kitzen", "17 June 1813", L,
  "During the armistice Lützow's Free Corps, marching back to Prussian lines, was surrounded at Kitzen by French and Württemberg cavalry who held it was outside the truce, and cut to pieces; the poet Theodor Körner was among the wounded.");
export const lowenberg = planned("lowenberg", "Löwenberg", "21 August 1813", L,
  "As the armistice ended Napoleon came at Blücher on the Bober with the Guard and three corps; Blücher, under orders to avoid a battle with the Emperor himself, fought and fell back.");
export const goldberg = planned("goldberg", "Goldberg", "23 August 1813", L,
  "Macdonald's corps attacked Blücher's army around Goldberg, taking the Wolfsberg after a fight in which the Prussian infantry and Russian Jäger held on until ordered back.");
export const altenburg = planned("altenburg", "Altenburg", "28 September 1813", L,
  "Thielmann's and Platov's raiders surprised Lefebvre-Desnouettes's cavalry at Altenburg behind the French lines and drove it back with heavy loss.");
export const liebertwolkwitz = planned("liebertwolkwitz", "Liebertwolkwitz", "14 October 1813", L,
  "Two days before Leipzig, Murat's cavalry met Wittgenstein's and Pahlen's on the open plain south of the city in the greatest cavalry battle of the wars, charge and counter-charge through the day with nothing decided.");
export const torgau = planned("torgau", "Siege of Torgau", "18 October 1813 – 10 January 1814", L,
  "The Elbe fortress, crowded with sick and wounded from Leipzig and swept by typhus, was besieged by Tauentzien's Prussians and surrendered in January.");
export const hamburg = planned("hamburg", "Siege of Hamburg", "3 December 1813 – 27 May 1814", L,
  "Davout held Hamburg against Bennigsen's Russians through the winter, turning out thousands of townspeople and firing the suburbs, and only gave the city up weeks after Napoleon's abdication.");
export const sehested = planned("sehested", "Sehested", "10 December 1813", L,
  "Napoleon's Danish allies, retreating into Holstein before Bernadotte's army, broke through Wallmoden's corps at Sehested to reach the fortress of Rendsburg; Denmark made peace a month later.");

// More of 1814
export const mormant = planned("mormant", "Mormant", "17 February 1814", F,
  "Turning back south after the Six Days, Napoleon's cavalry and Gérard's infantry caught Pahlen's Russian advance guard in the open at Mormant and cut it to pieces.");
export const barSurAube = planned("bar-sur-aube", "Bar-sur-Aube", "27 February 1814", F,
  "Schwarzenberg turned on Oudinot's and Macdonald's rearguard at Bar-sur-Aube and drove it back over the Aube; Wittgenstein was wounded leading the attack.");
export const laubressel = planned("laubressel", "Laubressel", "3 March 1814", F,
  "The allied army of Bohemia followed up its success at Bar-sur-Aube and beat Macdonald and Oudinot again at Laubressel, east of Troyes.");
export const soissons = planned("soissons", "Soissons", "3 March 1814", F,
  "With Blücher's army trapped against the Aisne, Moreau's small garrison gave up Soissons and its bridge to Bülow and Winzingerode, letting the Army of Silesia across; Napoleon called it the worst blow of the campaign.");
export const limonest = planned("limonest", "Limonest", "20 March 1814", F,
  "Augereau's army, which had held the Rhône valley against the Austrians since January, was beaten before Lyon at Limonest by the Prince of Hesse-Homburg, and Lyon fell next day.");
export const saintDizier = planned("saint-dizier", "Saint-Dizier", "26 March 1814", F,
  "Napoleon, striking at the allies' communications, turned on Winzingerode's cavalry screen at Saint-Dizier and routed it, then learned it had been sent to deceive him while the allied armies marched on Paris: his last victory.");

// Paintings for 1813 and 1814
dresden.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/90/Napoleon.Dresden.jpg/960px-Napoleon.Dresden.jpg",
  "title": "The Battle of Dresden, 27 August 1813",
  "artist": "Carle Vernet and Jacques-François Swebach",
  "page": "https://commons.wikimedia.org/wiki/File:Napoleon.Dresden.jpg"
};
kulm.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ad/Battle_of_Kulm_by_Kotsebu.jpg/960px-Battle_of_Kulm_by_Kotsebu.jpg",
  "title": "The Battle of Kulm",
  "artist": "Alexander von Kotzebue",
  "date": "1843",
  "page": "https://commons.wikimedia.org/wiki/File:Battle_of_Kulm_by_Kotsebu.jpg"
};
leipzig.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/58/Sauerweid_A.I._Battle_of_Leipzig%2C_from_2_to_7_october_1813.jpg/960px-Sauerweid_A.I._Battle_of_Leipzig%2C_from_2_to_7_october_1813.jpg",
  "title": "The Battle of Leipzig",
  "artist": "Alexander Sauerweid",
  "date": "1844",
  "page": "https://commons.wikimedia.org/wiki/File:Sauerweid_A.I._Battle_of_Leipzig,_from_2_to_7_october_1813.jpg"
};
brienne.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/19/Bataille_de_Brienne_%281814%29%2C_Sim%C3%A9on_Fort.jpg/960px-Bataille_de_Brienne_%281814%29%2C_Sim%C3%A9on_Fort.jpg",
  "title": "The Battle of Brienne",
  "artist": "Jean-Antoine-Siméon Fort",
  "date": "c. 1850",
  "page": "https://commons.wikimedia.org/wiki/File:Bataille_de_Brienne_(1814),_Sim%C3%A9on_Fort.jpg"
};
laRothiere.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/bd/Wigand_%28circle%29_Schlacht_bei_Rothiere_1814.jpg/960px-Wigand_%28circle%29_Schlacht_bei_Rothiere_1814.jpg",
  "title": "The Battle of La Rothière",
  "artist": "circle of Balthasar Wigand",
  "date": "c. 1830",
  "page": "https://commons.wikimedia.org/wiki/File:Wigand_(circle)_Schlacht_bei_Rothiere_1814.jpg"
};
champaubert.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/62/Combat_de_Champaubert%2C_10_f%C3%A9vrier_1814%2C_dans_la_soir%C3%A9e.jpg/960px-Combat_de_Champaubert%2C_10_f%C3%A9vrier_1814%2C_dans_la_soir%C3%A9e.jpg",
  "title": "Champaubert, the evening of 10 February 1814",
  "artist": "Jean-Antoine-Siméon Fort",
  "page": "https://commons.wikimedia.org/wiki/File:Combat_de_Champaubert,_10_f%C3%A9vrier_1814,_dans_la_soir%C3%A9e.jpg"
};
montmirail.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b7/The_battle_of_Montmirail_in_1814_%281822%29%2C_by_Horace_Vernet.jpg/960px-The_battle_of_Montmirail_in_1814_%281822%29%2C_by_Horace_Vernet.jpg",
  "title": "The Battle of Montmirail",
  "artist": "Horace Vernet",
  "date": "1822",
  "page": "https://commons.wikimedia.org/wiki/File:The_battle_of_Montmirail_in_1814_(1822),_by_Horace_Vernet.jpg"
};
chateauThierry.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1f/Combat_de_Ch%C3%A2teau-Thierry%2C_12_f%C3%A9vrier_1814%2C_%C3%A0_3_ou_4_heures_du_soir.jpg/960px-Combat_de_Ch%C3%A2teau-Thierry%2C_12_f%C3%A9vrier_1814%2C_%C3%A0_3_ou_4_heures_du_soir.jpg",
  "title": "Château-Thierry, 12 February 1814",
  "artist": "Jean-Antoine-Siméon Fort",
  "date": "1842–43",
  "page": "https://commons.wikimedia.org/wiki/File:Combat_de_Ch%C3%A2teau-Thierry,_12_f%C3%A9vrier_1814,_%C3%A0_3_ou_4_heures_du_soir.jpg"
};
vauchamps.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/ea/Battle_of_Etoges_%28Vauchamps%29%2C_14_January_1813_%28R._Knotel%29.jpg/960px-Battle_of_Etoges_%28Vauchamps%29%2C_14_January_1813_%28R._Knotel%29.jpg",
  "title": "Prussian infantry at Étoges, during Vauchamps",
  "artist": "Richard Knötel",
  "date": "1901",
  "page": "https://commons.wikimedia.org/wiki/File:Battle_of_Etoges_(Vauchamps),_14_January_1813_(R._Knotel).jpg"
};
montereau.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ad/Bataille_de_Montereau%2C_18_f%C3%A9vrier_1814.jpg/960px-Bataille_de_Montereau%2C_18_f%C3%A9vrier_1814.jpg",
  "title": "The Battle of Montereau",
  "artist": "Jean-Charles Langlois",
  "date": "1840",
  "page": "https://commons.wikimedia.org/wiki/File:Bataille_de_Montereau,_18_f%C3%A9vrier_1814.jpg"
};
craonne.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9f/Jung_theodore.jpg/960px-Jung_theodore.jpg",
  "title": "The Battle of Craonne",
  "artist": "Théodore Jung",
  "page": "https://commons.wikimedia.org/wiki/File:Jung_theodore.jpg"
};
laon.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7d/Battle_of_Laon._The_Neumark_Dragoon_Regiment_ambushes_the_fleeing_enemy_near_Athies_on_the_night_of_March_9-10%2C_1814.png/960px-Battle_of_Laon._The_Neumark_Dragoon_Regiment_ambushes_the_fleeing_enemy_near_Athies_on_the_night_of_March_9-10%2C_1814.png",
  "title": "The Neumark Dragoons at Athies, Laon",
  "artist": "Richard Knötel",
  "date": "1901",
  "page": "https://commons.wikimedia.org/wiki/File:Battle_of_Laon._The_Neumark_Dragoon_Regiment_ambushes_the_fleeing_enemy_near_Athies_on_the_night_of_March_9-10,_1814.png"
};
reims.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f7/Szeptycki_capture_des_Prussiens_%C3%A0_Reims_%281814%29.jpg/960px-Szeptycki_capture_des_Prussiens_%C3%A0_Reims_%281814%29.jpg",
  "title": "Szeptycki's Lancers Taking Prussians at Reims",
  "artist": "Juliusz Kossak",
  "date": "1882",
  "page": "https://commons.wikimedia.org/wiki/File:Szeptycki_capture_des_Prussiens_%C3%A0_Reims_(1814).jpg"
};
arcis.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1d/Battle_of_Arcis-sur-Aube._Austrian_battle_for_possession_of_the_village_of_Grand-Torcy_on_March_20%2C_1814.png/960px-Battle_of_Arcis-sur-Aube._Austrian_battle_for_possession_of_the_village_of_Grand-Torcy_on_March_20%2C_1814.png",
  "title": "Austrians at Grand-Torcy, Arcis-sur-Aube",
  "artist": "Richard Knötel",
  "date": "1901",
  "page": "https://commons.wikimedia.org/wiki/File:Battle_of_Arcis-sur-Aube._Austrian_battle_for_possession_of_the_village_of_Grand-Torcy_on_March_20,_1814.png"
};
fereChampenoise.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/59/A.I.Dmitriev-Mamonov-Fere-Champenoise.jpg/960px-A.I.Dmitriev-Mamonov-Fere-Champenoise.jpg",
  "title": "The Battle of Fère-Champenoise",
  "artist": "Alexander Dmitriev-Mamonov",
  "date": "before 1836",
  "page": "https://commons.wikimedia.org/wiki/File:A.I.Dmitriev-Mamonov-Fere-Champenoise.jpg"
};
paris.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/56/Battle_of_Paris_1814_by_Villevalde.jpg/960px-Battle_of_Paris_1814_by_Villevalde.jpg",
  "title": "The Battle of Paris",
  "artist": "Bogdan Willewalde",
  "date": "1834",
  "page": "https://commons.wikimedia.org/wiki/File:Battle_of_Paris_1814_by_Villevalde.jpg"
};
danzig.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d7/Die_Russen_belagern_Danzig.jpg/960px-Die_Russen_belagern_Danzig.jpg",
  "title": "The Russian Lines before Danzig, Winter 1813",
  "artist": "Johann Michael Voltz",
  "date": "c. 1820",
  "page": "https://commons.wikimedia.org/wiki/File:Die_Russen_belagern_Danzig.jpg"
};
luneburg.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c1/L%C3%BCneburg_Schlacht_1813.jpg/960px-L%C3%BCneburg_Schlacht_1813.jpg",
  "title": "The Fight at Lüneburg, 2 April 1813",
  "artist": "F. A. Frenzel",
  "page": "https://commons.wikimedia.org/wiki/File:L%C3%BCneburg_Schlacht_1813.jpg"
};
goldberg.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/73/Das_Gefecht_bei_Goldberg%2C_den_23.n_August_1813_-_estampe_-_btv1b6953922v.jpg/960px-Das_Gefecht_bei_Goldberg%2C_den_23.n_August_1813_-_estampe_-_btv1b6953922v.jpg",
  "title": "The Fight at Goldberg, 23 August 1813",
  "artist": "unknown artist",
  "page": "https://commons.wikimedia.org/wiki/File:Das_Gefecht_bei_Goldberg,_den_23.n_August_1813_-_estampe_-_btv1b6953922v.jpg"
};
liebertwolkwitz.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b5/Grenadiers_%C3%A0_cheval_fran%C3%A7ais_contre_cuirassiers_prussiens_au_combat_de_Liebertwolkwitz%2C_le_14_octobre_1813.jpg/960px-Grenadiers_%C3%A0_cheval_fran%C3%A7ais_contre_cuirassiers_prussiens_au_combat_de_Liebertwolkwitz%2C_le_14_octobre_1813.jpg",
  "title": "French Horse Grenadiers against Prussian Cuirassiers at Liebertwolkwitz",
  "artist": "Carl Röchling",
  "date": "before 1920",
  "page": "https://commons.wikimedia.org/wiki/File:Grenadiers_%C3%A0_cheval_fran%C3%A7ais_contre_cuirassiers_prussiens_au_combat_de_Liebertwolkwitz,_le_14_octobre_1813.jpg"
};
sehested.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f1/J%C3%B8rgen_V_Sonne%2C_Slaget_ved_Sehested%2C_KMS42%2C_Statens_Museum_for_Kunst.jpg/960px-J%C3%B8rgen_V_Sonne%2C_Slaget_ved_Sehested%2C_KMS42%2C_Statens_Museum_for_Kunst.jpg",
  "title": "The Battle of Sehested",
  "artist": "Jørgen Sonne",
  "date": "1822",
  "page": "https://commons.wikimedia.org/wiki/File:J%C3%B8rgen_V_Sonne,_Slaget_ved_Sehested,_KMS42,_Statens_Museum_for_Kunst.jpg"
};
gohrde.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/04/Carl_R%C3%B6chling_-_Eleonore_Prochaska.jpg/960px-Carl_R%C3%B6chling_-_Eleonore_Prochaska.jpg",
  "title": "Eleonore Prochaska at the Göhrde",
  "artist": "Carl Röchling",
  "date": "1900",
  "page": "https://commons.wikimedia.org/wiki/File:Carl_R%C3%B6chling_-_Eleonore_Prochaska.jpg"
};
mormant.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/af/Combat_de_Mormant_le_17_f%C3%A9vrier_1814%2C_%C3%A0_dix_heures_du_matin_%28d%C3%A9tail%29.jpg/960px-Combat_de_Mormant_le_17_f%C3%A9vrier_1814%2C_%C3%A0_dix_heures_du_matin_%28d%C3%A9tail%29.jpg",
  "title": "Mormant, 17 February 1814, at Ten in the Morning",
  "artist": "Jean-Antoine-Siméon Fort",
  "page": "https://commons.wikimedia.org/wiki/File:Combat_de_Mormant_le_17_f%C3%A9vrier_1814,_%C3%A0_dix_heures_du_matin_(d%C3%A9tail).jpg"
};
barSurAube.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3f/Johann_Lorenz_Rugendas_Schlacht_bei_Bar-sur-Aube.jpg/960px-Johann_Lorenz_Rugendas_Schlacht_bei_Bar-sur-Aube.jpg",
  "title": "The Battle of Bar-sur-Aube",
  "artist": "Johann Lorenz Rugendas",
  "date": "c. 1814",
  "page": "https://commons.wikimedia.org/wiki/File:Johann_Lorenz_Rugendas_Schlacht_bei_Bar-sur-Aube.jpg"
};
laubressel.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/29/Combat_de_Laubressel_Jean_Charles_Langlois_%28d%C3%A9tail%29.jpg/960px-Combat_de_Laubressel_Jean_Charles_Langlois_%28d%C3%A9tail%29.jpg",
  "title": "The Fight at Laubressel",
  "artist": "Jean-Charles Langlois",
  "page": "https://commons.wikimedia.org/wiki/File:Combat_de_Laubressel_Jean_Charles_Langlois_(d%C3%A9tail).jpg"
};
limonest.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4b/Charge_du_13e_r%C3%A9giment_de_cuirassiers_%C3%A0_la_bataille_de_Limonest%2C_20_mars_1814.png/960px-Charge_du_13e_r%C3%A9giment_de_cuirassiers_%C3%A0_la_bataille_de_Limonest%2C_20_mars_1814.png",
  "title": "An Episode of the Battle of Limonest",
  "artist": "Théodore Jung",
  "page": "https://commons.wikimedia.org/wiki/File:Charge_du_13e_r%C3%A9giment_de_cuirassiers_%C3%A0_la_bataille_de_Limonest,_20_mars_1814.png"
};
saintDizier.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/84/Charge_des_dragons_de_l%27Imp%C3%A9ratrice_%C3%A0_Saint-Dizier%2C_1814.jpg/960px-Charge_des_dragons_de_l%27Imp%C3%A9ratrice_%C3%A0_Saint-Dizier%2C_1814.jpg",
  "title": "The Guard Dragoons' Charge at Saint-Dizier",
  "artist": "Édouard Detaille",
  "page": "https://commons.wikimedia.org/wiki/File:Charge_des_dragons_de_l%27Imp%C3%A9ratrice_%C3%A0_Saint-Dizier,_1814.jpg",
  "focus": "50% 30%"
};
haynau.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/84/Combat_d%27Haynau%2C_26_mai_1813.jpg/960px-Combat_d%27Haynau%2C_26_mai_1813.jpg",
  "title": "Prussian Cavalry against Maison's Infantry at Haynau",
  "artist": "Richard Knötel",
  "page": "https://commons.wikimedia.org/wiki/File:Combat_d%27Haynau,_26_mai_1813.jpg"
};
lowenberg.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9a/Pierwsza_bitwa_nad_Bobrem.png/960px-Pierwsza_bitwa_nad_Bobrem.png",
  "title": "The First Battle on the Bober, 21 August 1813",
  "artist": "unknown artist",
  "date": "1813",
  "page": "https://commons.wikimedia.org/wiki/File:Pierwsza_bitwa_nad_Bobrem.png"
};

// The Ulm and Austerlitz Campaign, 1805
const U = "ulm-austerlitz-1805";

export const wertingen = planned("wertingen", "Wertingen", "8 October 1805", U,
  "As the Grande Armée swung across the Danube behind Mack, Murat's dragoons and Oudinot's grenadiers caught Auffenberg's Austrian column on the march at Wertingen and broke its squares.");
export const haslach = planned("haslach", "Haslach-Jungingen", "11 October 1805", U,
  "Dupont's lone division, left on the north bank before Ulm, ran into a great part of Mack's army trying to break out, and held it off all day before slipping away in the dark.");
export const elchingen = planned("elchingen", "Elchingen", "14 October 1805", U,
  "Ney's corps rebuilt the broken bridge under fire and stormed the abbey heights of Elchingen from Riesch's Austrians, closing the ring around Ulm; it later made him Duke of Elchingen.");
export const ulm = planned("ulm", "Ulm", "15–20 October 1805", U,
  "Shut into Ulm once Ney had taken the Michelsberg heights above it, Mack gave up the city and the 25,000 men with him: a whole Austrian army taken with hardly a battle.");
export const amstetten = planned("amstetten", "Amstetten", "5 November 1805", U,
  "Kutuzov's Russians, falling back down the Danube towards Vienna, left Bagration and Miloradovich to hold Murat's cavalry and Oudinot's grenadiers in the woods at Amstetten.");
export const durenstein = planned("durenstein", "Dürenstein", "11 November 1805", U,
  "Kutuzov crossed to the north bank and turned on Mortier's corps strung out along the river under the ruined castle of Dürenstein; Gazan's division was surrounded and fought its way out until Dupont came up.");
export const schongrabern = planned("schongrabern", "Schöngrabern", "16 November 1805", U,
  "Bagration's rearguard stood at Schöngrabern, by Hollabrunn, against Murat and Lannes, holding them a whole day so that Kutuzov could get away to join Buxhowden, and then broke out by night.");
export const austerlitz = planned("austerlitz", "Austerlitz", "2 December 1805", U,
  "Napoleon drew the Russian and Austrian armies onto his weakened right, where Davout held them in the villages of the Goldbach, then stormed the Pratzen heights in their centre with Soult's corps and cut their army in two: the Battle of the Three Emperors.");

// The Jena Campaign, 1806
const J = "jena-1806";

export const schleiz = planned("schleiz", "Schleiz", "9 October 1806", J,
  "Coming north out of the Thuringian Forest, Murat and Bernadotte's leading division drove Tauentzien's Prussians and Saxons out of Schleiz in the first fight of the war.");
export const saalfeld = planned("saalfeld", "Saalfeld", "10 October 1806", J,
  "Prince Louis Ferdinand stood with the advance guard before Saalfeld against Lannes's corps and was overwhelmed; the prince himself was cut down by a French quartermaster of hussars.");
export const jena = planned("jena", "Jena", "14 October 1806", J,
  "Lannes's corps climbed the Landgrafenberg by night, and at dawn Napoleon's army came down off the heights onto Hohenlohe's Prussians and Saxons, who stood in the open and were shot to pieces before Rüchel's corps came up too late to save them.");
export const auerstedt = planned("auerstedt", "Auerstedt", "14 October 1806", J,
  "On the same day, Davout's lone corps met the main Prussian army under Brunswick and the King at Auerstedt, formed square after square as Blücher's cavalry came on, and beat an army twice its size.");
export const halle = planned("halle", "Halle", "17 October 1806", J,
  "Bernadotte's corps stormed the bridges and gates of Halle against Eugen of Württemberg's reserve, the one Prussian corps not yet beaten, and drove it off towards the Elbe.");
export const prenzlau = planned("prenzlau", "Prenzlau", "28 October 1806", J,
  "Murat's cavalry, riding hard across Brandenburg, caught Hohenlohe's column at Prenzlau, short of the Oder, and talked him into surrendering what was left of his army.");
export const lubeck = planned("lubeck", "Lübeck", "6 November 1806", J,
  "Blücher's column, the last Prussian force in the field, was cornered in neutral Lübeck by Bernadotte, Soult and Murat, who stormed the city's gates and sacked it; Blücher surrendered next day at Ratekau.");

// The Polish Campaign, 1806–07
const Pl = "poland-1807";

export const czarnowo = planned("czarnowo", "Czarnowo", "23–24 December 1806", Pl,
  "Davout's corps forced the crossing of the Wkra at Czarnowo against Ostermann-Tolstoy's Russians in a night attack, opening Napoleon's winter offensive beyond the Vistula.");
export const pultusk = planned("pultusk", "Pułtusk", "26 December 1806", Pl,
  "Lannes's corps attacked Bennigsen's army at Pułtusk across mud and snow, with too few men to beat it; both sides claimed the day, and the Russians drew off in the night.");
export const golymin = planned("golymin", "Golymin", "26 December 1806", Pl,
  "On the same day, Golitsyn's Russians held Augereau, Davout's leading division and Murat's cavalry at Golymin, in the mud, until dark let them escape the trap.");
export const mohrungen = planned("mohrungen", "Mohrungen", "25 January 1807", Pl,
  "When Bennigsen struck west in the snow at the French winter quarters, Bernadotte turned on Markov's advance guard at Mohrungen and drove it back, though Cossacks took his baggage.");
export const eylau = planned("eylau", "Eylau", "7–8 February 1807", Pl,
  "Two days of slaughter in a snowstorm: Augereau's corps lost its way and was destroyed before the Russian guns, Murat's great charge of eighty squadrons saved the centre, and Lestocq's Prussians came in to stop Davout; both armies were left shattered on the field.");
export const ostroleka = planned("ostroleka", "Ostrołęka", "16 February 1807", Pl,
  "On the Narew, Savary, with Oudinot's grenadiers and Gazan's division, beat Essen's Russian corps as it tried to push through to Ostrołęka.");
export const danzig1807 = planned("danzig-1807", "Siege of Danzig", "19 March – 24 May 1807", Pl,
  "Lefebvre's corps of French, Poles, Saxons and Badeners besieged the great Prussian fortress on the Vistula, held by Kalckreuth; a Russian relief force came by sea and was beaten off, and the city gave up on terms.");
export const guttstadt = planned("guttstadt", "Guttstadt", "5–6 June 1807", Pl,
  "Bennigsen opened the summer campaign by falling on Ney's corps, isolated round Guttstadt, which fought its way back over the Passarge in good order.");
export const heilsberg = planned("heilsberg", "Heilsberg", "10 June 1807", Pl,
  "Murat, Soult and Lannes attacked Bennigsen's entrenched camp on the Alle at Heilsberg head-on, and were thrown back with heavy loss, though the Russians fell back next day.");
export const friedland = planned("friedland", "Friedland", "14 June 1807", Pl,
  "Bennigsen crossed the Alle to catch Lannes's corps alone at Friedland, and Lannes held him until Napoleon came up; Ney's corps then drove into the Russian left, and Sénarmont's guns, pushed close in, broke the army against the river. The Treaty of Tilsit followed.");

// The Danube Campaign, 1809
const Dn = "danube-1809";

export const teugenHausen = planned("teugen-hausen", "Teugen-Hausen", "19 April 1809", Dn,
  "Davout's corps, marching up the Danube from Regensburg to join Napoleon, met Hohenzollern's Austrian corps in the wooded hills between Teugen and Hausen and fought its way through.");
export const abensberg = planned("abensberg", "Abensberg", "20 April 1809", Dn,
  "Napoleon, with Lannes, the Bavarians and the Württembergers, broke through the thinly held Austrian centre about Abensberg and split Hiller's wing off from Archduke Charles.");
export const landshut = planned("landshut", "Landshut", "21 April 1809", Dn,
  "Pursuing Hiller's wing south, Lannes and Masséna's troops stormed the burning bridge over the Isar into Landshut and took the Austrian trains.");
export const eckmuhl = planned("eckmuhl", "Eckmühl", "22 April 1809", Dn,
  "Archduke Charles turned on Davout and Lefebvre at Eckmühl, until Napoleon came up from Landshut on his left flank; the French and allied cavalry fought it out in the dusk, and the Austrians fell back over the Danube.");
export const regensburg = planned("regensburg", "Regensburg", "23 April 1809", Dn,
  "Lannes stormed the walls of Regensburg, seizing a ladder himself when his grenadiers hung back, to cover the Archduke's crossing; Napoleon was struck in the foot outside the city.");
export const neumarkt = planned("neumarkt", "Neumarkt", "24 April 1809", Dn,
  "Hiller, rallied south of the Danube, turned on Bessières's pursuing corps of Bavarians and French at Neumarkt-Sankt Veit and drove it back before resuming his retreat.");
export const ebelsberg = planned("ebelsberg", "Ebelsberg", "3 May 1809", Dn,
  "Masséna's corps stormed the long bridge over the Traun and the burning town and castle of Ebelsberg against Hiller's rearguard, at great cost, opening the road to Vienna.");
export const aspernEssling = planned("aspern-essling", "Aspern-Essling", "21–22 May 1809", Dn,
  "Napoleon crossed the Danube below Vienna by the island of Lobau, and Archduke Charles attacked his bridgehead before it could fill; the villages of Aspern and Essling changed hands again and again, and with the bridge broken Napoleon fell back to the island, his first defeat in a decade. Lannes was mortally wounded.");
export const raab = planned("raab", "Raab", "14 June 1809", Dn,
  "Eugène's Army of Italy, come up through the Alps, caught Archduke John and the Hungarian noble levy before Raab and beat them, so that they could not join the Archduke Charles on the Marchfeld.");
export const wagram = planned("wagram", "Wagram", "5–6 July 1809", Dn,
  "Napoleon crossed from the Lobau in force and fought Archduke Charles over two days on the Marchfeld; Masséna's corps held the left against the Austrian counter-attack, Macdonald's great column broke the centre, and Davout turned the Austrian left, and Charles drew off in good order.");
export const znaim = planned("znaim", "Znaim", "10–11 July 1809", Dn,
  "Marmont and then Masséna caught up with the retreating Austrians at Znaim, in Moravia, and fought them through the town and its vineyards until the Archduke sought the armistice that ended the war.");

// Paintings for the Jena campaign
jena.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e6/Bataille_d%27I%C3%A9na%2C_14_octobre_1806_%28Vernet%29.jpg/960px-Bataille_d%27I%C3%A9na%2C_14_octobre_1806_%28Vernet%29.jpg",
  "title": "The Battle of Jena, 14 October 1806",
  "artist": "Horace Vernet",
  "date": "1836",
  "page": "https://commons.wikimedia.org/wiki/File:Bataille_d%27I%C3%A9na,_14_octobre_1806_(Vernet).jpg",
  "focus": "50% 35%"
};
schleiz.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/28/Bataille_de_Schleiz.jpg/960px-Bataille_de_Schleiz.jpg",
  "title": "The Battle of Schleiz",
  "artist": "Benjamin Zix",
  "date": "1806",
  "page": "https://commons.wikimedia.org/wiki/File:Bataille_de_Schleiz.jpg"
};
saalfeld.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Heldentod_der_Prinzen_Louis_Ferdinand_bei_Saalfeld.jpg",
  "title": "The Death of Prince Louis Ferdinand at Saalfeld",
  "artist": "Richard Knötel",
  "page": "https://commons.wikimedia.org/wiki/File:Heldentod_der_Prinzen_Louis_Ferdinand_bei_Saalfeld.jpg"
};
halle.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/ef/Per_Krafft_d.y._-_The_Battle_of_Halle%2C_October_17th_1806_-_NM_4782_-_Nationalmuseum.jpg/960px-Per_Krafft_d.y._-_The_Battle_of_Halle%2C_October_17th_1806_-_NM_4782_-_Nationalmuseum.jpg",
  "title": "The Battle of Halle, 17 October 1806",
  "artist": "Per Krafft the Younger",
  "date": "1821",
  "page": "https://commons.wikimedia.org/wiki/File:Per_Krafft_d.y._-_The_Battle_of_Halle,_October_17th_1806_-_NM_4782_-_Nationalmuseum.jpg"
};
auerstedt.art = {
  "src": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Bataille_d%27Auerstaedt%2C_14_octobre_1806.jpg",
  "title": "French Squares against the Prussian Cavalry at Auerstedt",
  "artist": "Michelet",
  "page": "https://commons.wikimedia.org/wiki/File:Bataille_d%27Auerstaedt,_14_octobre_1806.jpg"
};
prenzlau.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/12/Combat_de_Prenzlau%2C_28_octobre_1806.jpg/960px-Combat_de_Prenzlau%2C_28_octobre_1806.jpg",
  "title": "Prussian Grenadiers at Prenzlau",
  "artist": "Richard Knötel",
  "page": "https://commons.wikimedia.org/wiki/File:Combat_de_Prenzlau,_28_octobre_1806.jpg"
};
lubeck.art = {
  "src": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/87/Bl%C3%BCcher%27s_capitulation_at_Ratekau%2C_7_November_1806.jpg/960px-Bl%C3%BCcher%27s_capitulation_at_Ratekau%2C_7_November_1806.jpg",
  "title": "Blücher's Capitulation at Ratekau, after Lübeck",
  "artist": "Carl Röchling",
  "date": "1901",
  "page": "https://commons.wikimedia.org/wiki/File:Bl%C3%BCcher%27s_capitulation_at_Ratekau,_7_November_1806.jpg"
};
