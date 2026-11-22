"""
Writes three more of the Peninsular War's battles (src/data/battles/{fuentes-de-onoro,sorauren,orthez}.json).

    python3 scripts/forces/peninsular_late.py && npm run check:forces

Sources (see each battle's sources): Nafziger's orders of battle (811ESAG, 811ESAH, 813GSAT, 814ASAB, 814ASAD), after
Oman, Koch, Fortescue, Batty, Dumas and Clerc, with Wikipedia for the course of each battle. Summaries are our own
words; ratings.py sets Staff Ratings as each battle is written.
"""

import copy
import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from peninsular import ART, OUT, PB, PF, ARTILLERY, highland, light, line, pb_battery, pb_bde, pf_battery, pf_bde, pf_cav, pf_regiment
from peninsular_more import AP, R, fr_div, pt_bde, rifles, wiki
from peninsular_early import naf

FR_STRENGTH = "Nafziger gives each regiment's strength but not its battalions; about one battalion per 700 men is shown."
FR_JAN = "After Nafziger's return of 16 January 1814, six weeks before the battle; the divisions had sent men to Napoleon since, so they were smaller."
AL_JAN = "After Nafziger's return of 1 January 1814; the brigades had changed little since the summer, but battalions were weaker."
PT = "Each Portuguese line regiment's two battalions are shown as one, as the list builds them."
CAVALRY_ONLY = "Cavalry on its own has no infantry brigades for its brigades to go with, which shows as a historical departure."
TWO_LIGHT = "Two Light regiments in a brigade, where the list allows one, show as a historical departure."


def kgl_bde(name, commander, battalions):
    return bde("pb-kgl-brigade", name, commander, [u("pb-line", b) for b in battalions])


def light_bde(name, commander, light_inf, cacadores, rifle_units):
    return bde("pb-light-brigade", name, commander, [u("pb-light-inf", l) for l in light_inf] + [u("pb-cacadores", cacadores)] + rifle_units)


# ================================================================ Fuentes de Oñoro, 3–5 May 1811

FUENTES_AL = [
    force("fuentes-spencer", PB, "Spencer's 1st Division", "Wellington's army", AP,
          "Held the ridge behind the village; on 5 May, as Wellington swung his right back, its Highland battalions were sent down into Fuentes de Oñoro to clear it of the French.",
          [bde("pb-guards-brigade", "Stopford's Guards Brigade", "Maj-Gen Edward Stopford", [u("pb-foot-guard", "1/Coldstream Guards"), u("pb-foot-guard", "1/3rd Guards"), rifles()]),
           pb_bde("Nightingall's Brigade", "Maj-Gen Miles Nightingall", [line("2/24th Foot"), highland("1/42nd Highlanders"), highland("1/79th Highlanders"), rifles()]),
           pb_bde("Howard's Brigade", "Maj-Gen Kenneth Howard", [line("1/50th Foot"), highland("71st Highland Light Infantry"), highland("92nd Highlanders"), rifles("3/95th Rifles (company)")]),
           kgl_bde("Löwe's KGL Brigade", "Maj-Gen von Löwe", ["1st Line Bn KGL", "2nd Line Bn KGL", "5th Line Bn KGL", "7th Line Bn KGL"]),
           pb_battery("Lawson's Battery")],
          command=[cmd("pb-div-cmd", "Lt-Gen Sir Brent Spencer")],
          notes=["After Nafziger.", "Highland battalions beyond the list's one in four, and a KGL brigade of four battalions, show as historical departures."]),
    force("fuentes-picton", PB, "Picton's 3rd Division", "Wellington's army", AP,
          "Sent battalions down into the village through the fighting; on the 5th the 88th charged down its streets and drove the French out.",
          [pb_bde("Mackinnon's Brigade", "Col Henry Mackinnon", [line("1/45th Foot"), line("74th Foot"), line("2/88th Connaught Rangers"), rifles("5/60th Rifles (three companies)")]),
           pb_bde("Colville's Brigade", "Maj-Gen Charles Colville", [line("2/5th Foot"), line("2/83rd Foot"), line("1/88th Connaught Rangers"), line("94th Foot")]),
           pt_bde("Power's Brigade", "Col Manley Power", ["9th Line", "21st Line"])],
          command=[{"unit": "pb-cmd-picton"}],
          notes=["Picton is the book's named commander.", PT]),
    force("fuentes-houston", PB, "Houston's 7th Division", "Wellington's army", AP,
          "New to the army and posted out on the right at Poço Velho, it was caught there on 5 May by Montbrun's cavalry and the 6th Corps, and only got back with the Light Division's help, the Chasseurs Britanniques beating off the horsemen from behind a wall.",
          [pb_bde("Sontag's Brigade", "Maj-Gen John Sontag",
                  [light("51st Light Infantry"), light("85th Light Infantry"), u("pb-line", "Chasseurs Britanniques", options=["chasseurs"]), u("pb-brunswick-light", "Brunswick Oels (eight companies)")]),
           pt_bde("Doyle's Brigade", "Col John Doyle", ["7th Line", "19th Line"], "2nd Caçadores")],
          command=[cmd("pb-div-cmd", "Maj-Gen John Houston")],
          notes=["After Nafziger.", PT, "Two Light battalions in a brigade of three show as a historical departure."]),
    force("fuentes-light", PB, "Craufurd's Light Division", "Wellington's army", AP,
          "Back with the army that morning, Craufurd took the division out to bring the 7th home, and retired it across two miles of open plain in squares with Montbrun's cavalry riding round them, a march that became famous.",
          [light_bde("Beckwith's Brigade", "Lt-Col Sidney Beckwith", ["1/43rd Light Infantry"], "3rd Caçadores", [u("pb-rifle-coys", "2/95th Rifles (four companies)")]),
           light_bde("Drummond's Brigade", "Col George Drummond", ["1/52nd Light Infantry", "2/52nd Light Infantry"], "1st Caçadores", [u("pb-rifle-coys", "1/95th Rifles (four companies)")]),
           bde("pb-horse-artillery", "Ross's Troop RHA", units=[u("pb-royal-horse-arty", "Ross's Troop RHA")])],
          command=[{"unit": "pb-cmd-craufurd"}],
          notes=["Craufurd is the book's named commander.", "Nafziger puts the Caçadores in a brigade of their own; one goes with each Light brigade, as the list builds them.",
                 "Two Light Brigades, the second Light battalion in Drummond's, and a horse troop with an infantry division, show as historical departures."]),
    force("fuentes-cavalry", PB, "Cotton's Cavalry", "Wellington's army", AP,
          "Fewer than 1,900 sabres against Montbrun's 3,500, it covered the retreat of the 7th and Light Divisions on 5 May, charging again and again to hold off the French dragoons.",
          [bde("pb-heavy-cavalry-brigade", "Slade's Brigade", "Maj-Gen John Slade", [u("pb-dragoon-guards", "1st Royal Dragoons"), u("pb-light-dragoon-hussar", "14th Light Dragoons")]),
           bde("pb-light-cavalry-brigade", "Arentschildt's Brigade", "Col von Arentschildt", [u("pb-light-dragoon-hussar", "16th Light Dragoons"), u("pb-light-dragoon-hussar", "1st Hussars KGL", options=["kgl"])]),
           bde("pb-portuguese-cavalry-brigade", "Barbacena's Brigade", "Brig-Gen Barbacena", [u("pb-portuguese-cavalry", "4th Portuguese Dragoons", options=["small"]), u("pb-portuguese-cavalry", "10th Portuguese Dragoons", options=["small"])]),
           bde("pb-horse-artillery", "Bull's Troop RHA", units=[u("pb-royal-horse-arty", "Bull's Troop RHA")])],
          command=[cmd("pb-div-cmd", "Lt-Gen Sir Stapleton Cotton")],
          notes=["After Nafziger. Barbacena's Portuguese were barely 300 men, so Small.", "Slade's heavy brigade, with one heavy regiment where it needs two, and cavalry without infantry, show as historical departures."]),
]

FUENTES_FR = [
    fr_div("fuentes-ferey", "Ferey's Division", "3rd Division, VI Corps (Loison)", "Gén. de Brigade Ferey",
           [("Simon's Brigade", "Gén. de Brigade Simon", [R("32e", 1, "Léger"), pf_regiment("Légion du Midi", 1), pf_regiment("Hanoverian Legion", 2), R("26e", 3)]),
            ("Ferey's Brigade", "Gén. de Brigade Ferey", [R("66e", 3), R("82e", 3)])],
           "Loison's old division, under Ferey: it stormed into Fuentes de Oñoro on 3 May and fought for its walled lanes all afternoon, and on the 5th came at it again.",
           ["After Nafziger, whose return gives Simon's battalions as very weak, barely 600 men in all; mark them Small if you like.", "The Légion du Midi and the Hanoverian Legion are shown as Line.",
            "Four regiments in Simon's brigade, where the list takes three, show as a historical departure."]),
    fr_div("fuentes-marchand", "Marchand's Division", "1st Division, VI Corps (Loison)", "Gén. de Division Marchand",
           [("Maucune's Brigade", "Gén. de Brigade Maucune", [R("6e", 2, "Léger"), R("69e", 3)]), ("Marcognet's Brigade", "Gén. de Brigade Marcognet", [R("39e", 3), R("76e", 3)])],
           "Attacked out of the woods at Poço Velho on 5 May, driving the 7th Division back, and then fed into the village fight.", ["After Nafziger."]),
    fr_div("fuentes-mermet", "Mermet's Division", "2nd Division, VI Corps (Loison)", "Gén. de Division Mermet",
           [("Bardet's Brigade", "Gén. de Brigade Bardet", [R("25e", 2, "Léger"), R("27e", 3)]), ("Labassée's Brigade", "Gén. de Brigade Labassée", [R("50e", 3), R("59e", 3)])],
           "Followed Marchand round the southern flank on the 5th, pressing the 7th and Light Divisions as they fell back.", ["After Nafziger."]),
    force("fuentes-conroux", PF, "Conroux's Division", "2nd Division, IX Corps (d'Erlon)", "French",
          "Two provisional regiments of fourth battalions from the regiments in Spain, which d'Erlon sent into Fuentes de Oñoro on 5 May; they took most of the village before the 71st, 79th and 88th threw them out.",
          [pf_bde("Gérard's Brigade", "Gén. de Brigade Gérard",
                  [{"name": "1st Provisional", "units": [u("pf-line", "IV/8e Ligne"), u("pf-line", "IV/24e Ligne"), u("pf-line", "IV/45e Ligne")]},
                   {"name": "2nd Provisional", "units": [u("pf-line", "IV/94e Ligne"), u("pf-line", "IV/95e Ligne"), u("pf-line", "IV/96e Ligne")]}]),
           pf_battery("Foot Battery")],
          command=[cmd("pf-div-cmd", "Gén. de Division Conroux")],
          notes=["After Nafziger. The provisional regiments were made of single battalions from six regiments, three to each."]),
    force("fuentes-montbrun", PF, "Montbrun's Cavalry", "Reserve Cavalry and IX Corps cavalry", "French",
          "Massena's dragoons and d'Erlon's chasseurs, which swept round the open southern flank on 5 May, overran the 7th Division's outposts and rode round the Light Division's squares all the way back to the ridge.",
          [pf_cav("Cavrois's Brigade", "Gén. de Brigade Cavrois", [("3e", "Dragons"), ("10e", "Dragons"), ("15e", "Dragons")]),
           pf_cav("Ornano's Brigade", "Gén. de Brigade Ornano", [("6e", "Dragons"), ("11e", "Dragons"), ("25e", "Dragons")]),
           pf_cav("Fournier's Brigade", "Gén. de Brigade Fournier", [("7e", "Chasseurs"), ("18e", "Chasseurs"), ("20e", "Chasseurs")]),
           pf_battery("6/2nd Horse Artillery", "pf-horse-arty")],
          command=[cmd("pf-div-cmd", "Gén. de Division Montbrun")],
          notes=["After Nafziger, whose return gives the dragoons only a few hundred men each, as Koch had them; other accounts make them stronger. Nafziger repeats the 15th in Ornano's brigade, so the 11th is shown there.",
                 CAVALRY_ONLY]),
    force("fuentes-guard", PF, "Lepic's Guard Cavalry", "Reserve, Army of Portugal", "French",
          "Eight hundred Grenadiers à Cheval of the Guard under Lepic, which stood ready to charge the retreating Light Division and were held back, Bessières refusing to commit them without orders.",
          [bde("pf-guard-cavalry-brigade", "Lepic's Brigade", "Gén. de Brigade Lepic", [u("pf-guard-grenadier-a-cheval", "Grenadiers à Cheval of the Guard")])],
          command=[cmd("pf-div-cmd", "Gén. de Brigade Lepic")],
          notes=["After Nafziger: one regiment of eight squadrons, with two guns.", "Guard cavalry without the infantry and cavalry brigades it needs shows as a historical departure."]),
]

FUENTES = {
    "id": "fuentes-de-onoro", "name": "Fuentes de Oñoro", "date": "3–5 May 1811", "campaign": "peninsular-war",
    "summary": "Masséna came back to relieve Almeida and found Wellington across his road at the village of Fuentes de Oñoro. Two days of fighting in its walled lanes left it in British hands; on the 5th Masséna swung round the open southern flank, and the 7th and Light Divisions fell back across the plain in squares through Montbrun's cavalry. Wellington held the shortened line, and Masséna withdrew: 'if Boney had been there, we should have been beat'.",
    "sources": [naf("811ESAG", "Anglo-Portuguese Army at Fuentes de Onoro, 3–5 May 1811"), naf("811ESAH", "French Army at Fuentes de Onoro, 3–5 May 1811"),
                wiki("Battle_of_Fuentes_de_O%C3%B1oro", "Battle of Fuentes de Oñoro")],
    "forces": FUENTES_AL + FUENTES_FR,
}


# ================================================================ Sorauren, 28–30 July 1813

def bn(strength):
    return 1 if strength <= 900 else 2 if strength <= 1500 else 3


def S(num, strength, kind="Ligne"):
    return pf_regiment(num, bn(strength), kind)


SORAUREN_FR = [
    fr_div("sorauren-conroux", "Conroux's Division", "4th Division, Left Wing (Clausel)", "Gén. de Division Conroux",
           [("Rey's Brigade", "Gén. de Brigade Rey", [S("12e", 1121, "Léger"), S("22e", 1561), S("43e", 1149)]),
            ("Schwitter's Brigade", "Gén. de Brigade Schwitter", [S("45e", 887), S("55e", 931), S("58e", 996)])],
           "Clausel's leading division, which climbed the steep slope at Sorauren against Cole's ridge on 28 July and was thrown back by Ross's brigade, again and again.", [FR_STRENGTH]),
    fr_div("sorauren-vandermaesen", "Vandermaesen's Division", "5th Division, Left Wing (Clausel)", "Gén. de Division Vandermaesen",
           [("Barbot's Brigade", "Gén. de Brigade Barbot", [S("25e", 503, "Léger"), S("27e", 564), S("50e", 832)]),
            ("Rouget's Brigade", "Gén. de Brigade Rouget", [S("59e", 865), S("130e", 1167)])],
           "Attacked the left of Cole's line, where Campbell's Portuguese held the knoll; on the 30th it held the village of Sorauren as the army began to withdraw.", [FR_STRENGTH]),
    fr_div("sorauren-taupin", "Taupin's Division", "8th Division, Left Wing (Clausel)", "Gén. de Division Taupin",
           [("Stordegrave's Brigade", "Gén. de Brigade Stordegrave", [S("31e", 610, "Léger"), S("26e", 778), S("47e", 1272)]),
            ("Lecamus's Brigade", "Gén. de Brigade Lecamus", [S("36e", 1159, "Léger"), S("70e", 860), S("88e", 667)])],
           "Clausel's third division, which went up the spur on the right of the attack and was met by Anson's brigade with the bayonet.", [FR_STRENGTH]),
    fr_div("sorauren-foy", "Foy's Division", "1st Division, Right Wing (Reille)", "Gén. de Division Foy",
           [("Berlier's Brigade", "Gén. de Brigade Berlier", [S("6e", 603, "Léger"), S("36e", 985), S("39e", 676)]),
            ("Fririon's Brigade", "Gén. de Brigade Fririon", [S("65e", 941), S("69e", 1356), S("76e", 667)])],
           "Reille's flank division, out on the right on the 28th; when the army retreated on the 30th it was cut off and got away by a mountain road.", [FR_STRENGTH]),
    fr_div("sorauren-maucune", "Maucune's Division", "3rd Division, Right Wing (Reille)", "Gén. de Division Maucune",
           [("Pinoteau's Brigade", "Gén. de Brigade Pinoteau", [S("17e", 755, "Léger"), S("15e", 886), S("66e", 556)]),
            ("Montfort's Brigade", "Gén. de Brigade Montfort", [S("82e", 478), S("84e", 737)])],
           "Reille's second division, which faced the Spanish and Byng's brigade on the heights across the valley.",
           [FR_STRENGTH, "Nafziger lists a 36th Line here as well as in Foy's division; it is left out."]),
    fr_div("sorauren-lamartiniere", "Lamartinière's Division", "9th Division, Right Wing (Reille)", "Gén. de Division Lamartinière",
           [("Gauthier's Brigade", "Gén. de Brigade Gauthier", [S("2e", 418, "Léger"), S("118e", 1212), S("119e", 966)]),
            ("Menne's Brigade", "Gén. de Brigade Menne", [S("120e", 1863), S("122e", 1443)])],
           "Attacked the Spanish regiments holding the end of the ridge at Oricain, the 120th and 122nd taking and losing the hill.", [FR_STRENGTH]),
]

SORAUREN_AL = [
    force("sorauren-cole", PB, "Cole's 4th Division", "Wellington's army", AP,
          "Held the ridge above Sorauren on 28 July against the whole of Clausel's attack, Ross's and Anson's brigades charging down on the French as each column reached the crest.",
          [pb_bde("Anson's Brigade", "Maj-Gen William Anson", [line("3/27th Foot"), line("1/40th Foot"), line("1/48th Foot"), line("2nd Provisional Bn (2nd and 53rd)"), rifles("5/60th Rifles (two companies)")]),
           pb_bde("Ross's Brigade", "Maj-Gen Robert Ross", [line("1/7th Fusiliers"), line("1/20th Foot"), line("1/23rd Royal Welch Fusiliers"), rifles("Brunswick Oels (company)")]),
           pt_bde("Stubbs's Brigade", "Col George Stubbs", ["11th Line", "23rd Line"], "7th Caçadores"),
           pb_battery("Sympher's KGL Battery")],
          command=[cmd("pb-div-cmd", "Lt-Gen Sir Lowry Cole")],
          notes=[AL_JAN, PT, "Four line battalions in Anson's brigade is the list's limit; the rifle company makes five, which shows as a historical departure."]),
    force("sorauren-pack", PB, "Pack's 6th Division", "Wellington's army", AP,
          "Came up on the morning of 28 July, just in time, into the valley on Cole's left, and beat off Clausel's attempt to turn the ridge; Pack was wounded at its head.",
          [pb_bde("Stirling's Highland Brigade", "Col James Stirling", [highland("1/42nd Highlanders"), highland("1/79th Highlanders"), highland("1/91st Highlanders"), rifles("5/60th Rifles (two companies)")]),
           pb_bde("Lambert's Brigade", "Maj-Gen John Lambert", [line("1/11th Foot"), line("1/32nd Foot"), line("1/36th Foot"), line("1/61st Foot")]),
           pt_bde("Madden's Brigade", "Brig-Gen Madden", ["8th Line", "12th Line"], "9th Caçadores"),
           pb_battery("Brandreth's Battery")],
          command=[cmd("pb-div-cmd", "Maj-Gen Denis Pack")],
          notes=[AL_JAN, PT, "Three Highland battalions where the list allows one in four show as a historical departure."]),
    force("sorauren-picton", PB, "Picton's 3rd Division", "Wellington's army", AP,
          "Held the right of the line beyond the Arga; on 30 July it struck at the retreating French and helped drive them from the field.",
          [pb_bde("Brisbane's Brigade", "Maj-Gen Thomas Brisbane", [line("1/45th Foot"), line("1/74th Foot"), line("1/88th Connaught Rangers"), rifles("5/60th Rifles (four companies)")]),
           pb_bde("Keane's Brigade", "Maj-Gen John Keane", [line("1/5th Foot"), line("2/83rd Foot"), line("2/87th Foot"), line("1/94th Foot")]),
           pt_bde("Power's Brigade", "Maj-Gen Manley Power", ["9th Line", "21st Line"], "11th Caçadores"),
           pb_battery("Douglas's Battery")],
          command=[{"unit": "pb-cmd-picton"}],
          notes=["Picton is the book's named commander.", AL_JAN, PT]),
    force("sorauren-byng", PB, "Byng's and Campbell's Brigades", "Detached, Wellington's army", AP,
          "Byng's British brigade and Campbell's Portuguese, which had fought their way back from Roncesvalles with Cole, held the knoll and the left of the ridge beside the Spanish.",
          [pb_bde("Byng's Brigade", "Maj-Gen John Byng", [line("1/3rd Foot (Buffs)"), line("1/57th Foot"), line("1st Provisional Bn (31st and 66th)"), rifles("5/60th Rifles (two companies)")]),
           pt_bde("Campbell's Brigade", "Brig-Gen Archibald Campbell", ["1st Line", "16th Line"], "4th Caçadores")],
          command=[cmd("pb-div-cmd", "Maj-Gen John Byng")],
          notes=[AL_JAN, PT, "Spanish regiments of O'Donnell's and Morillo's commands also held the ridge; they aren't included."]),
]

SORAUREN = {
    "id": "sorauren", "name": "Sorauren", "date": "28–30 July 1813", "campaign": "peninsular-war",
    "summary": "Soult's counter-offensive through the Pyrenees to relieve Pamplona drove the allied covering troops back down the passes to the ridge above Sorauren, a few miles short of the city. There, on 28 July, Clausel's divisions climbed the steep slope again and again and were thrown back by Cole's men with the bayonet, the 6th Division coming up in time. Two days later Wellington attacked in turn, and Soult's army went back over the mountains with heavy loss.",
    "sources": [naf("813GSAT", "French Army of the Pyrenees, 16 July 1813"), naf("814ASAB", "Anglo-Portuguese Army, 1 January 1814"),
                wiki("Battle_of_Sorauren", "Battle of Sorauren")],
    "forces": SORAUREN_FR + SORAUREN_AL,
}


# ================================================================ Orthez, 27 February 1814

ORTHEZ_FR = [
    fr_div("orthez-taupin", "Taupin's Division", "Reille's Wing", "Gén. de Division Taupin",
           [("Rey's Brigade", "Gén. de Brigade Rey", [R("12e", 2, "Léger"), R("32e", 2), R("43e", 2)]),
            ("Béchaud's Brigade", "Gén. de Brigade Béchaud", [pf_regiment("45e and 47e", 2), pf_regiment("55e and 58e", 2)])],
           "Held the village and church of St Boès on the right of the French ridge, where Ross's brigade attacked it four times in the morning and was beaten off each time.",
           [FR_JAN, "Béchaud's four single-battalion regiments are shown as two regiments of two battalions."]),
    fr_div("orthez-rouget", "Rouget's Division", "Reille's Wing", "Gén. de Brigade Rouget",
           [("Barbot's Brigade", "Gén. de Brigade Barbot", [R("4e", 1, "Léger"), R("40e", 2), R("50e", 1)]),
            ("Rouget's Brigade", "Gén. de Brigade Rouget", [R("27e", 1), R("59e", 1), R("130e", 2)])],
           "Maransin's old division, beside Taupin's, which fought for the narrow ridge behind St Boès until the 52nd's attack broke the French centre.",
           [FR_JAN, "The 34th Line, which Nafziger also lists in Harispe's division, is left out."]),
    fr_div("orthez-foy", "Foy's Division", "D'Erlon's Wing", "Gén. de Division Foy",
           [("Fririon's Brigade", "Gén. de Brigade Fririon", [R("6e", 1, "Léger"), R("69e", 2), R("76e", 1)]),
            ("Berlier's Brigade", "Gén. de Brigade Berlier", [R("36e", 2), R("39e", 1), R("65e", 2)])],
           "Held the centre of the ridge above the Dax road against Picton; Foy was badly wounded, and his division broke as the line gave way.", [FR_JAN]),
    fr_div("orthez-darmagnac", "Darmagnac's Division", "D'Erlon's Wing", "Gén. de Division Darmagnac",
           [("Chassé's Brigade", "Gén. de Brigade Chassé", [R("16e", 1, "Léger"), R("28e", 2), pf_regiment("8e and 54e", 2)]),
            ("Gruardet's Brigade", "Gén. de Brigade Gruardet", [R("31e", 2, "Léger"), R("51e", 1), R("75e", 2)])],
           "Beside Foy's, it held the ridge against the 6th Division and fell back with the centre.",
           [FR_JAN, "The 8th and 54th, a battalion each, are shown together as one regiment."]),
    fr_div("orthez-harispe", "Harispe's Division", "Clausel's Wing", "Gén. de Division Harispe",
           [("Dauture's Brigade", "Gén. de Brigade Dauture", [R("9e", 2, "Léger"), R("34e", 2)]),
            ("Paris's Brigade", "Gén. de Brigade Paris", [R("10e", 2), R("81e", 2), pf_regiment("114e and 8th Neapolitan", 2)]),
            ("Baurot's Brigade", "Gén. de Brigade Baurot", [R("25e", 2, "Léger"), R("115e", 2), {"name": "117e Ligne (four companies)", "units": [u("pf-line", "117e Ligne", options=["small"])]}])],
           "Held Orthez itself and the bridge on the left, against Hill; when Hill forced the fords above the town Harispe's men were pushed back, and the whole army had to retire.",
           [FR_JAN, "Two companies of the 114th and the 8th Neapolitan battalion are shown as one regiment, the 117th's four companies as a Small battalion."]),
    force("orthez-cavalry", PF, "Pierre Soult's Cavalry", "1st Cavalry Division", "French",
          "The army's only cavalry division by then, which covered the retreat from the ridge as the 7th Hussars charged into the rearguard.",
          [pf_cav("Berton's Brigade", "Gén. de Brigade Berton", [("2e", "Hussards"), ("13e", "Chasseurs"), ("21e", "Chasseurs")]),
           pf_cav("Vial's Brigade", "Gén. de Brigade Vial", [("5e", "Chasseurs"), ("10e", "Chasseurs"), ("15e", "Chasseurs"), ("22e", "Chasseurs")]),
           pf_cav("Sparre's Brigade", "Gén. de Brigade Sparre", [("5e", "Dragons"), ("12e", "Dragons")]),
           pf_battery("Horse Battery", "pf-horse-arty")],
          command=[cmd("pf-div-cmd", "Gén. de Division Pierre Soult")],
          notes=[FR_JAN, CAVALRY_ONLY]),
]

ORTHEZ_AL = [
    force("orthez-cole", PB, "Cole's 4th Division", "Beresford's column", AP,
          "Led the attack on the French right at St Boès, where Ross's brigade stormed the village and was thrown back four times; Ross was wounded.",
          copy.deepcopy(SORAUREN_AL[0]["brigades"]), command=[cmd("pb-div-cmd", "Lt-Gen Sir Lowry Cole")], notes=[AL_JAN, PT]),
    force("orthez-walker", PB, "Walker's 7th Division", "Beresford's column", AP,
          "Came up beside the 4th Division against St Boès and the ridge behind it, and joined the final advance as the French line broke.",
          [pb_bde("Gardiner's Brigade", "Col Gardiner", [line("1/6th Foot"), line("3rd Provisional Bn (24th and 58th)"), u("pb-brunswick-light", "Brunswick Oels (nine companies)")]),
           pb_bde("Inglis's Brigade", "Maj-Gen William Inglis", [light("1/51st Light Infantry"), light("1/68th Light Infantry"), line("1/82nd Foot"), u("pb-line", "Chasseurs Britanniques", options=["chasseurs"])]),
           pt_bde("Doyle's Brigade", "Col John Doyle", ["7th Line", "19th Line"], "2nd Caçadores"),
           pb_battery("Cairnes's Battery")],
          command=[cmd("pb-div-cmd", "Maj-Gen George Walker")],
          notes=[AL_JAN, PT, "Two Light battalions in Inglis's brigade show as a historical departure."]),
    force("orthez-picton", PB, "Picton's 3rd Division", "Picton's column", AP,
          "Attacked the French centre up the spurs from the Dax road, held at first, then pushed on to the crest as the 52nd broke through on its left.",
          copy.deepcopy(SORAUREN_AL[2]["brigades"]), command=[{"unit": "pb-cmd-picton"}], notes=["Picton is the book's named commander.", AL_JAN, PT]),
    force("orthez-clinton", PB, "Clinton's 6th Division", "Picton's column", AP,
          "Beside Picton's, against Darmagnac's division on the ridge.",
          copy.deepcopy(SORAUREN_AL[1]["brigades"]), command=[cmd("pb-div-cmd", "Lt-Gen Sir Henry Clinton")],
          notes=[AL_JAN, PT, "Three Highland battalions where the list allows one in four show as a historical departure."]),
    force("orthez-light", PB, "Alten's Light Division", "Wellington's reserve", AP,
          "In reserve until the attack on St Boès stalled, when Wellington sent the 52nd up the marshy hollow between the two French wings; its advance broke the French line in two.",
          [bde("pb-light-brigade", "Kempt's Brigade", "Maj-Gen James Kempt",
               [u("pb-light-inf", "1/43rd Light Infantry"), u("pb-cacadores", "1st Caçadores"), u("pb-rifle-bn", "1/95th Rifles"), u("pb-rifle-bn", "3/95th Rifles")]),
           bde("pb-light-brigade", "Barnard's Brigade", "Col Andrew Barnard",
               [u("pb-light-inf", "1/52nd Light Infantry"), u("pb-cacadores", "3rd Caçadores"), u("pb-rifle-bn", "2/95th Rifles"), u("pb-portuguese-line", "17th Portuguese Line")]),
           bde("pb-horse-artillery", "Ross's Troop RHA", units=[u("pb-royal-horse-arty", "Ross's Troop RHA")])],
          command=[cmd("pb-div-cmd", "Maj-Gen Charles Alten")],
          notes=[AL_JAN, "Nafziger puts the 17th Portuguese and the Caçadores in a brigade of their own; they're shared between the Light brigades, as the list builds them.",
                 "Two Light Brigades, and a horse troop with an infantry division, show as historical departures."]),
    force("orthez-hill", PB, "Stewart's 2nd Division", "Hill's column", AP,
          "With Hill on the right, it forced the fords of the Gave above Orthez and turned the French left, threatening Soult's line of retreat.",
          [pb_bde("Barnes's Brigade", "Maj-Gen Edward Barnes", [line("1/50th Foot"), highland("1/71st Highland Light Infantry"), highland("1/92nd Highlanders"), rifles("5/60th Rifles (two companies)")]),
           pb_bde("Byng's Brigade", "Maj-Gen John Byng", [line("1/3rd Foot (Buffs)"), line("1/57th Foot"), line("1st Provisional Bn (31st and 66th)"), rifles("5/60th Rifles (two companies)")]),
           pb_bde("Pringle's Brigade", "Maj-Gen William Pringle", [line("1/28th Foot"), line("2/34th Foot"), line("1/39th Foot"), rifles("5/60th Rifles (two companies)")]),
           pt_bde("Ashworth's Brigade", "Col Charles Ashworth", ["6th Line", "18th Line"], "6th Caçadores"),
           pb_battery("Maxwell's Battery")],
          command=[cmd("pb-div-cmd", "Lt-Gen Sir William Stewart")],
          notes=[AL_JAN, PT, "Nafziger gives Barnes's brigade the 51st; it was the 50th, with the 71st and 92nd. Two Highland battalions in a brigade of three show as a historical departure."]),
    force("orthez-hussars", PB, "Somerset's and Vivian's Hussars", "Cotton's cavalry", AP,
          "Followed the broken French army off the ridge; the 7th Hussars charged into the rearguard near Sallespisse and took several hundred prisoners.",
          [bde("pb-light-cavalry-brigade", "Somerset's Brigade", "Maj-Gen Lord Edward Somerset", [u("pb-light-dragoon-hussar", "7th Hussars"), u("pb-light-dragoon-hussar", "10th Hussars"), u("pb-light-dragoon-hussar", "15th Hussars")]),
           bde("pb-light-cavalry-brigade", "Vivian's Brigade", "Maj-Gen Hussey Vivian", [u("pb-light-dragoon-hussar", "18th Hussars"), u("pb-light-dragoon-hussar", "1st Hussars KGL", options=["kgl"])]),
           bde("pb-horse-artillery", "Gardiner's Troop RHA", units=[u("pb-royal-horse-arty", "Gardiner's Troop RHA")])],
          command=[cmd("pb-div-cmd", "Lt-Gen Sir Stapleton Cotton")],
          notes=[AL_JAN, "Cavalry on its own, without infantry brigades for its brigades to go with, shows as a historical departure."]),
]

ORTHEZ = {
    "id": "orthez", "name": "Orthez", "date": "27 February 1814", "campaign": "peninsular-war",
    "summary": "Soult made a stand on the ridge north of the Gave de Pau above Orthez. Beresford's attack on St Boès at the French right was beaten back again and again, and Picton's in the centre stalled, until Wellington sent the 52nd up the marshy hollow between them and broke the French line in two, while Hill forced the river upstream. Soult's army fell back in growing disorder towards Toulouse.",
    "sources": [naf("814ASAD", "French Army of the Pyrenees, 16 January 1814"), naf("814ASAB", "Anglo-Portuguese Army, 1 January 1814"),
                wiki("Battle_of_Orthez", "Battle of Orthez")],
    "forces": ORTHEZ_FR + ORTHEZ_AL,
}

# Periods: 1811 is the lists' Middle period, 1813–14 their Late
for f in FUENTES["forces"]:
    f["period"] = "middle"
for f in SORAUREN["forces"] + ORTHEZ["forces"]:
    f["period"] = "late"


if __name__ == "__main__":
    for b in (FUENTES, SORAUREN, ORTHEZ):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in ART:
            b["art"] = ART[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
