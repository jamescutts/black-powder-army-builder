"""
Writes more of the Peninsular War's historical forces: Corunna, Talavera, Salamanca and Vitoria
(src/data/battles/{corunna,talavera,salamanca,vitoria}.json), with the builders from peninsular.py.

    python3 scripts/forces/peninsular_more.py && npm run check:forces

Sources (see each battle's SOURCES): Wikipedia's orders of battle for the four battles, which cite Glover,
Oman, Lipscombe, Muir and Fletcher, and History of War. Summaries are our own words; ratings.py sets Staff
Ratings as each battle is written.
"""

import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from peninsular import (
    ART, OUT, PB, PF, SP, ARTILLERY, highland, light, line, pb_battery, pb_bde, pf_battery, pf_bde, pf_cav, pf_regiment,
    portuguese, pt_line, sp_regiment,
)

AP = "Anglo-Portuguese"
AL = "Anglo-Allied"


def wiki(slug, label):
    return {"label": f"{label} (Wikipedia)", "url": f"https://en.wikipedia.org/wiki/{slug}"}


def pt_bde(name, commander, regiments, cacadores=None):
    units = [pt_line(r) for r in regiments]
    if cacadores:
        units.append(u("pb-cacadores", cacadores))
    return portuguese(name, commander, units)


def rifles(name="5/60th Rifles (company)"):
    return u("pb-rifle-coy", name)


def kgl(name):
    return u("pb-light-dragoon-hussar", name, options=["kgl"])


def fr_div(id_, name, formation, commander, brigades, summary, notes=(), battery="Foot Battery"):
    return force(id_, PF, name, formation, "French", summary,
                 [pf_bde(n, c, regs) for n, c, regs in brigades] + [pf_battery(battery)],
                 command=[cmd("pf-div-cmd", commander)], notes=list(notes))


def R(num, n, kind="Ligne"):
    return pf_regiment(num, n, kind)


# ================================================================ Corunna, 16 January 1809

FR3 = "No source gives the battalions of each regiment; the corps' 39 battalions in thirteen regiments suggests three each, which is how they're shown."

CORUNNA = {
    "id": "corunna", "name": "Corunna", "date": "16 January 1809", "campaign": "peninsular-war",
    "summary": "At the end of a terrible winter retreat across Galicia, Moore's army turned on the heights above Corunna to hold off Soult while the fleet waited to take it off. The French attacks on the village of Elviña and round the British right were beaten back, and the army embarked; Moore was killed by a round shot at the moment of victory.",
    "sources": [wiki("Battle_of_Corunna_order_of_battle", "Battle of Corunna order of battle"), wiki("Battle_of_Corunna", "Battle of Corunna"),
                {"label": "Battle of Corunna (History of War)", "url": "https://www.historyofwar.org/articles/battles_corunna.html"}],
    "forces": [
        force("corunna-baird", PB, "Baird's 1st Division", "Moore's army", AP,
              "Held the right of the British line around Elviña, where Bentinck's brigade, the 42nd and 50th among it, fought for the village all afternoon; Moore fell beside it.",
              [bde("pb-guards-brigade", "Warde's Guards Brigade", "Maj-Gen Henry Warde", [u("pb-foot-guard", "1/1st Foot Guards"), u("pb-foot-guard", "2/1st Foot Guards")]),
               pb_bde("Bentinck's Brigade", "Maj-Gen Lord William Bentinck", [line("1/4th Foot"), highland("1/42nd Highlanders"), line("1/50th Foot")]),
               pb_bde("Manningham's Brigade", "Maj-Gen Coote Manningham", [line("3/1st Foot (Royal Scots)"), line("1/26th Foot"), line("2/81st Foot")]),
               pb_battery("Truscott's Battery")],
              command=[cmd("pb-div-cmd", "Lt-Gen Sir David Baird")],
              notes=["Truscott's and Wilmot's were the only guns kept ashore, nine in all; one battery goes to each of Baird's and Hope's divisions."]),
        force("corunna-hope", PB, "Hope's 2nd Division", "Moore's army", AP,
              "Held the left of the line above the Mero, facing Delaborde's half-hearted attack; Hope took command when Moore fell and Baird was wounded.",
              [pb_bde("Leith's Brigade", "Maj-Gen James Leith", [line("51st Foot"), line("2/59th Foot"), line("2/76th Foot")]),
               pb_bde("Hill's Brigade", "Maj-Gen Rowland Hill", [line("2nd Foot"), line("1/5th Foot"), line("2/14th Foot"), line("1/32nd Foot")]),
               pb_bde("Craufurd's Brigade", "Brig-Gen Catlin Craufurd", [line("1/36th Foot"), highland("1/71st Highlanders"), highland("1/92nd Highlanders")]),
               pb_battery("Wilmot's Battery")],
              command=[cmd("pb-div-cmd", "Lt-Gen the Hon John Hope")],
              notes=["Craufurd's brigade had two Highland battalions, the 71st and 92nd, where the list allows one in four, which shows as a historical departure."]),
        force("corunna-paget", PB, "Paget's Reserve", "Moore's army", AP,
              "The army's rearguard through the retreat, it came forward round the British right to meet Mermet's flanking brigade and the French cavalry and drove them back.",
              [pb_bde("Anstruther's Brigade", "Brig-Gen Robert Anstruther", [line("20th Foot"), light("1/52nd Light Infantry"), u("pb-rifle-coys", "1/95th Rifles")]),
               pb_bde("Disney's Brigade", "Brig-Gen Moore Disney", [line("1/28th Foot"), highland("1/91st Highlanders")])],
              command=[cmd("pb-div-cmd", "Maj-Gen the Hon Edward Paget")],
              notes=["The 1/95th, worn down by the retreat, is the list's Small Rifle Companies."]),
        force("corunna-fraser", PB, "Fraser's 3rd Division", "Moore's army", AP,
              "Posted on the heights of Santa Lucia behind the right, covering the town and the way to the ships; it was hardly engaged.",
              [pb_bde("Beresford's Brigade", "Maj-Gen William Carr Beresford", [line("1/6th Foot"), line("1/9th Foot"), line("2/23rd Foot"), light("2/43rd Light Infantry")]),
               pb_bde("Fane's Brigade", "Brig-Gen Henry Fane", [line("1/38th Foot"), highland("1/79th Highlanders"), line("1/82nd Foot")])],
              command=[cmd("pb-div-cmd", "Lt-Gen Alexander Fraser")]),
        fr_div("corunna-merle", "Merle's Division", "1st Division, II Corps (Soult)", "Gén. de Division Merle",
               [("Reynaud's Brigade", "Gén. de Brigade Reynaud", [R("2e", 3, "Léger"), R("36e", 3)]),
                ("Sarrut's Brigade", "Gén. de Brigade Sarrut", [R("4e", 3, "Léger")]),
                ("Thomières's Brigade", "Gén. de Brigade Thomières", [R("15e", 3)])],
               "In the French centre, its columns pressed the attack on Elviña and the heights beyond alongside Mermet's.", [FR3]),
        fr_div("corunna-mermet", "Mermet's Division", "2nd Division, II Corps (Soult)", "Gén. de Division Mermet",
               [("Gaulois's Brigade", "Gén. de Brigade Gaulois", [R("122e", 3)]),
                ("Jardon's Brigade", "Gén. de Brigade Jardon", [R("31e", 3, "Léger"), R("47e", 3)]),
                ("Lefebvre's Brigade", "Gén. de Brigade Lefebvre", [R("2e", 3, "Suisse"), R("3e", 3, "Suisse")])],
               "Led the main French attack: two brigades stormed Elviña against Bentinck while the third swung round the British right. Gaulois was killed and Lefebvre wounded.",
               [FR3, "The Swiss regiments may have had fewer battalions; the sources don't say."]),
        fr_div("corunna-delaborde", "Delaborde's Division", "3rd Division, II Corps (Soult)", "Gén. de Division Delaborde",
               [("Foy's Brigade", "Gén. de Brigade Foy", [R("70e", 3), R("86e", 3)]),
                ("Arnaud's Brigade", "Gén. de Brigade Arnaud", [R("17e", 3, "Léger"), R("4e", 3, "Suisse")])],
               "Still coming up as the battle began, it made only a weak attack on the British left late in the day.", [FR3]),
        force("corunna-cavalry", PF, "Soult's Cavalry", "Lahoussaye's and Franceschi's divisions", "French",
              "Sent round the British right with Mermet's flanking brigade, the dragoons and light horse were held off by Paget's reserve in the broken ground.",
              [pf_cav("Lahoussaye's Dragoons", "Gén. de Division Lahoussaye", [("17e", "Dragons"), ("18e", "Dragons"), ("19e", "Dragons"), ("27e", "Dragons")]),
               pf_cav("Franceschi's Light Cavalry", "Gén. de Division Franceschi",
                      [("1er", "Hussards"), ("22e", "Chasseurs"), ("Hanoverian", "Chasseurs"), ("8e", "Dragons")]),
               pf_battery("Horse Battery", "pf-horse-arty")],
              command=[cmd("pf-div-cmd", "Gén. de Division Lahoussaye")],
              notes=["Cavalry without the infantry brigades it's allowed by shows as a historical departure. Lorge's dragoon division, also with the corps, is left out."]),
    ],
}

# ================================================================ Talavera, 27–28 July 1809

TALAVERA = {
    "id": "talavera", "name": "Talavera", "date": "27–28 July 1809", "campaign": "peninsular-war",
    "summary": "Wellesley and Cuesta's Anglo-Spanish army held the line from Talavera to the Cerro de Medellín against King Joseph, Jourdan and Victor. A night attack on the Medellín was thrown back, and on the 28th the British line broke the French assaults, though the Guards pursued too far, and the 23rd Light Dragoons rode into a hidden ravine. The French withdrew; it won Wellesley his title.",
    "sources": [wiki("Battle_of_Talavera_order_of_battle", "Battle of Talavera order of battle"), wiki("Battle_of_Talavera", "Battle of Talavera"),
                {"label": "Battle of Talavera (History of War)", "url": "https://www.historyofwar.org/articles/battles_talavera.html"}],
    "forces": [
        force("talavera-sherbrooke", PB, "Sherbrooke's 1st Division", "Wellesley's army", AP,
              "Held the centre. On the 28th its Guards and King's German Legion threw back Lapisse's columns but followed them too far, and only the 48th's arrival stopped the counter-attack breaking the line; Langwerth was killed.",
              [bde("pb-guards-brigade", "Campbell's Guards Brigade", "Brig-Gen Henry Campbell",
                   [u("pb-foot-guard", "1/Coldstream Guards"), u("pb-foot-guard", "1/3rd Foot Guards"), rifles()]),
               pb_bde("Cameron's Brigade", "Brig-Gen Alan Cameron", [line("1/61st Foot"), line("2/83rd Foot")]),
               bde("pb-kgl-brigade", "Langwerth's KGL Brigade", "Brig-Gen von Langwerth", [line("1st Line Bn KGL"), line("2nd Line Bn KGL")]),
               bde("pb-kgl-brigade", "Löw's KGL Brigade", "Brig-Gen von Löw", [line("5th Line Bn KGL"), line("7th Line Bn KGL")]),
               pb_battery("Sillery's Battery")],
              command=[cmd("pb-div-cmd", "Maj-Gen John Sherbrooke")],
              notes=["Two KGL brigades where the list takes one show as a historical departure. Two companies of the 1st KGL Light are left out."]),
        force("talavera-hill", PB, "Hill's 2nd Division", "Wellesley's army", AP,
              "Held the Cerro de Medellín, the key to the position, and threw Ruffin's night attack off it; next day it beat off Ruffin again, and the 1/48th came down to save the centre.",
              [pb_bde("Tilson's Brigade", "Maj-Gen Christopher Tilson", [line("1/3rd Foot (Buffs)"), line("2/48th Foot"), line("2/66th Foot"), rifles()]),
               pb_bde("Stewart's Brigade", "Brig-Gen Richard Stewart",
                      [line("29th Foot"), line("1/48th Foot"), line("1st Bn of Detachments", options=["detachments"])]),
               pb_battery("Heise's Battery KGL")],
              command=[{"unit": "pb-cmd-wellington"}],
              notes=["Wellesley directed the battle from the Medellín, so the book's named Wellington leads here; Hill commanded the division."]),
        force("talavera-mackenzie", PB, "Mackenzie's 3rd Division", "Wellesley's army", AP,
              "Caught by surprise at the Casa de Salinas the day before, it held the left centre on the 28th and fought off the attack on the redoubt; Mackenzie was killed.",
              [pb_bde("Mackenzie's Brigade", "Maj-Gen John Mackenzie", [line("2/24th Foot"), line("2/31st Foot"), line("1/45th Foot")]),
               pb_bde("Donkin's Brigade", "Col Rufane Donkin", [line("2/87th Foot"), line("1/88th Foot"), u("pb-rifle-coys", "5/60th Rifles (five companies)")]),
               pb_battery("Rettberg's Battery KGL")],
              command=[cmd("pb-div-cmd", "Maj-Gen John Mackenzie")]),
        force("talavera-campbell", PB, "Campbell's 4th Division", "Wellesley's army", AP,
              "Joined to the Spanish at the Pajar de Vergara redoubt, it threw back Leval's Germans and took their guns.",
              [pb_bde("Campbell's Brigade", "Brig-Gen Alexander Campbell", [line("2/7th Foot"), line("2/53rd Foot"), rifles()]),
               pb_bde("Kemmis's Brigade", "Col James Kemmis",
                      [line("1/40th Foot"), line("97th Foot"), line("2nd Bn of Detachments", options=["detachments"])]),
               pb_battery("Lawson's Battery")],
              command=[cmd("pb-div-cmd", "Brig-Gen Alexander Campbell")],
              notes=["Lawson's battery had 3-pounders, lighter than the list's guns."]),
        force("talavera-payne", PB, "Payne's Cavalry", "Wellesley's army", AP,
              "Held behind the line and in the northern valley; Anson's brigade charged the French there, and the 23rd Light Dragoons rode into a hidden ravine and on into the French, losing half their men.",
              [bde("pb-heavy-cavalry-brigade", "Fane's Brigade", "Brig-Gen Henry Fane", [u("pb-dragoon-guards", "3rd Dragoon Guards"), u("pb-dragoon-guards", "4th Dragoons")]),
               bde("pb-light-cavalry-brigade", "Cotton's Brigade", "Maj-Gen Stapleton Cotton",
                   [u("pb-light-dragoon-hussar", "14th Light Dragoons"), u("pb-light-dragoon-hussar", "16th Light Dragoons")]),
               bde("pb-light-cavalry-brigade", "Anson's Brigade", "Brig-Gen George Anson",
                   [u("pb-light-dragoon-hussar", "23rd Light Dragoons"), kgl("1st Hussars KGL")])],
              command=[cmd("pb-div-cmd", "Lt-Gen William Payne")],
              notes=["Cavalry on its own has no infantry brigades for its brigades to go with, which shows as a historical departure."]),
        fr_div("talavera-ruffin", "Ruffin's Division", "1st Division, I Corps (Victor)", "Gén. de Division Ruffin",
               [("First Brigade", "", [R("9e", 3, "Léger"), R("24e", 3)]), ("Second Brigade", "", [R("96e", 3)])],
               "Made the night attack on the Medellín on the 27th and attacked it again at dawn and in the evening of the 28th, each time thrown back by Hill.",
               ["The order of battle gives the regiments but not their brigades or battalions; three battalions each, the usual for Victor's corps, in two brigades."]),
        fr_div("talavera-lapisse", "Lapisse's Division", "2nd Division, I Corps (Victor)", "Gén. de Division Lapisse",
               [("First Brigade", "", [R("16e", 3, "Léger"), R("8e", 3)]), ("Second Brigade", "", [R("45e", 3), R("54e", 3)])],
               "Attacked Sherbrooke's centre on the 28th and was thrown back, then turned on the pursuing Guards and Germans; Lapisse was killed.",
               ["The order of battle gives the regiments but not their brigades or battalions; three battalions each, in two brigades."]),
        fr_div("talavera-villatte", "Villatte's Division", "3rd Division, I Corps (Victor)", "Gén. de Division Villatte",
               [("First Brigade", "", [R("27e", 3, "Léger"), R("63e", 3)]), ("Second Brigade", "", [R("94e", 3), R("95e", 3)])],
               "Victor's reserve, sent into the northern valley at the end of the day, where it formed squares against Anson's charge.",
               ["The order of battle gives the regiments but not their brigades or battalions; three battalions each, in two brigades."]),
        force("talavera-sebastiani", PF, "Sebastiani's Division", "1st Division, IV Corps", "French",
              "Attacked the British left centre and the junction with the Spanish, and was beaten back with heavy loss.",
              [pf_bde("First Brigade", "", [R("28e", 3), R("32e", 3)]), pf_bde("Second Brigade", "", [R("58e", 3), R("75e", 3)]),
               pf_battery("Foot Battery")],
              command=[{"unit": "pf-cmd-sebastiani"}],
              notes=["Liger-Belair led the division for Sebastiani, who commanded IV Corps; the book's named Sebastiani leads it here.",
                     "Its four regiments, three battalions each, are split into two brigades as the order of battle doesn't give them."]),
        force("talavera-leval", PF, "Leval's and Valence's Divisions", "IV Corps", "French",
              "Leval's German and Dutch battalions attacked the Pajar de Vergara redoubt and were broken by Campbell's division, losing their guns; Valence's Poles were held in support.",
              [pf_bde("Nassau and Baden", "", [R("Nassau", 2, "Infantry"), R("Baden", 2, "Infantry")]),
               pf_bde("Hesse, Holland and Frankfurt", "", [R("Hesse-Darmstadt", 2, "Infantry"), R("Holland", 2, "Infantry"), R("Frankfurt", 1, "Infantry")]),
               pf_bde("Valence's Poles", "Gén. de Division Valence", [R("4th Polish", 2, "Infantry")]),
               pf_battery("Foot Battery")],
              command=[cmd("pf-div-cmd", "Gén. de Division Leval")],
              notes=["The list has no German, Dutch or Polish allies, so they're the list's Line battalions."]),
        force("talavera-dragoons", PF, "Latour-Maubourg's and Milhaud's Dragoons", "Reserve cavalry", "French",
              "The French heavy cavalry, held behind the infantry through both days.",
              [pf_cav("Latour-Maubourg's First Brigade", "", [("1er", "Dragons"), ("2e", "Dragons"), ("4e", "Dragons")]),
               pf_cav("Latour-Maubourg's Second Brigade", "", [("9e", "Dragons"), ("14e", "Dragons"), ("26e", "Dragons")]),
               pf_cav("Milhaud's Brigade", "Gén. de Division Milhaud", [("5e", "Dragons"), ("12e", "Dragons"), ("16e", "Dragons")]),
               pf_cav("Milhaud's Second Brigade", "", [("20e", "Dragons"), ("21e", "Dragons"), ("3rd Dutch", "Hussards")])],
              command=[cmd("pf-div-cmd", "Gén. de Division Latour-Maubourg")],
              notes=["Four brigades where the list takes three, and no infantry for them to go with, show as historical departures."]),
        force("talavera-light-cav", PF, "Beaumont's and Merlin's Light Cavalry", "I and IV Corps", "French",
              "The corps' light horse, including the Polish lancers and Westphalian chevau-légers who met Anson's charge in the northern valley.",
              [pf_cav("Beaumont's Brigade", "Gén. de Brigade Beaumont", [("2e", "Hussards"), ("5e", "Chasseurs")]),
               pf_cav("Merlin's Brigade", "Gén. de Brigade Merlin",
                      [("10e", "Chasseurs"), ("26e", "Chasseurs"), ("Polish", "Lanciers"), ("Westphalian Chevau-légers", "Chasseurs")]),
               pf_battery("Horse Battery", "pf-horse-arty")],
              command=[cmd("pf-div-cmd", "Gén. de Brigade Merlin")],
              notes=["Cavalry without the infantry brigades it's allowed by shows as a historical departure."]),
    ],
}

# ================================================================ Salamanca, 22 July 1812

PT2 = "The order of battle gives the Portuguese regiments but not their battalions; each is one of the list's regiments."
SALAMANCA = {
    "id": "salamanca", "name": "Salamanca", "date": "22 July 1812", "campaign": "peninsular-war",
    "summary": "After weeks of manoeuvring side by side, Marmont stretched his army out to the west to cut Wellington off from Portugal. Wellington saw the gap open, sent Pakenham's 3rd Division into the head of the French column and Leith's 5th and Le Marchant's heavy dragoons after it, and broke the Army of Portugal in an afternoon; Clausel's counter-attack was stopped and the French were routed.",
    "sources": [wiki("Battle_of_Salamanca_order_of_battle", "Battle of Salamanca order of battle"), wiki("Battle_of_Salamanca", "Battle of Salamanca"),
                {"label": "Battle of Salamanca (History of War)", "url": "https://www.historyofwar.org/articles/battles_salamanca.html"}],
    "forces": [
        force("salamanca-pakenham", PB, "Pakenham's 3rd Division", "Wellington's army", AP,
              "Sent by Wellington himself to cut across the head of the French column, it fell on Thomières's division on the march and broke it, opening the battle.",
              [pb_bde("Wallace's Brigade", "Lt-Col Alexander Wallace",
                      [line("1/45th Foot"), highland("74th Highlanders"), line("1/88th Connaught Rangers"), u("pb-rifle-coys", "5/60th Rifles (three companies)")]),
               pb_bde("Campbell's Brigade", "Lt-Col James Campbell", [line("1/5th Foot"), line("2/5th Foot"), line("2/83rd Foot"), line("94th Foot")]),
               pt_bde("Power's Portuguese Brigade", "Col Manley Power", ["9th Line", "21st Line"], "12th Caçadores"),
               pb_battery("Douglas's Battery")],
              command=[{"unit": "pb-cmd-wellington"}],
              notes=["Wellington gave Pakenham his orders in person, so the book's named Wellington leads it here; Pakenham commanded the division.", PT2,
                     "Batteries are spread among the divisions; the order of battle lists them under the army's artillery without saying which served with which."]),
        force("salamanca-leith", PB, "Leith's 5th Division", "Wellington's army", AP,
              "Advanced in two lines over the crest against Maucune's division, which had formed square against the cavalry, and broke it with a volley and the bayonet; Leith was wounded.",
              [pb_bde("Greville's Brigade", "Lt-Col James Greville",
                      [line("3/1st Foot (Royal Scots)"), line("1/9th Foot"), line("1/38th Foot"), line("2/38th Foot"), u("pb-brunswick-oels-coy", "Brunswick Oels (company)")]),
               pb_bde("Pringle's Brigade", "Maj-Gen William Pringle", [line("1/4th Foot"), line("2/4th Foot"), line("2/30th Foot"), line("2/44th Foot")]),
               pt_bde("Spry's Portuguese Brigade", "Brig-Gen William Spry", ["3rd Line", "15th Line"], "8th Caçadores"),
               pb_battery("Lawson's Battery")],
              command=[cmd("pb-div-cmd", "Lt-Gen James Leith")],
              notes=[PT2, "Each brigade had a company of the Brunswick Oels; one is shown, the list allowing one in an army."]),
        force("salamanca-cole", PB, "Cole's 4th Division", "Wellington's army", AP,
              "Attacked Clausel and Bonet in the centre and was thrown back by Clausel's counter-attack; Cole was wounded.",
              [pb_bde("Anson's Brigade", "Maj-Gen William Anson", [line("3/27th Foot"), line("1/40th Foot"), rifles()]),
               pb_bde("Ellis's Brigade", "Lt-Col Henry Ellis", [line("1/7th Fusiliers"), line("1/23rd Royal Welch Fusiliers"), line("1/48th Foot")]),
               pt_bde("Stubbs's Portuguese Brigade", "Col George Stubbs", ["11th Line", "23rd Line"], "7th Caçadores"),
               pb_battery("Sympher's Battery KGL")],
              command=[cmd("pb-div-cmd", "Lt-Gen Sir Lowry Cole")],
              notes=[PT2, "Ellis's company of the Brunswick Oels is left out."]),
        force("salamanca-clinton", PB, "Clinton's 6th Division", "Wellington's army", AP,
              "Wellington's reserve, sent in to stop Clausel's counter-attack; it held, at heavy cost, and drove on against Ferey's rearguard as night fell.",
              [pb_bde("Hulse's Brigade", "Maj-Gen Richard Hulse", [line("1/11th Foot"), line("2/53rd Foot"), line("1/61st Foot"), rifles()]),
               pb_bde("Hinde's Brigade", "Col Samuel Hinde", [line("2nd Foot"), line("1/32nd Foot"), line("1/36th Foot")]),
               pt_bde("Rezende's Portuguese Brigade", "Brig-Gen Conde de Rezende", ["8th Line", "12th Line"], "9th Caçadores"),
               pb_battery("Greene's Battery")],
              command=[cmd("pb-div-cmd", "Maj-Gen Sir Henry Clinton")],
              notes=[PT2]),
        force("salamanca-campbell", PB, "Campbell's 1st Division", "Wellington's army", AP,
              "Held the allied left near the Lesser Arapile and joined the pursuit late in the day.",
              [bde("pb-guards-brigade", "Fermor's Guards Brigade", "Col Thomas Fermor", [u("pb-foot-guard", "1/Coldstream Guards"), u("pb-foot-guard", "1/3rd Foot Guards"), rifles()]),
               pb_bde("Wheatley's Brigade", "Maj-Gen William Wheatley", [line("2/24th Foot"), highland("1/42nd Highlanders"), line("2/58th Foot"), highland("1/79th Highlanders")]),
               bde("pb-kgl-brigade", "Löw's KGL Brigade", "Maj-Gen von Löw", [line("1st Line Bn KGL"), line("2nd Line Bn KGL"), line("5th Line Bn KGL")]),
               pb_battery("Gardiner's Battery")],
              command=[cmd("pb-div-cmd", "Maj-Gen Henry Campbell")],
              notes=["Wheatley's brigade had two Highland battalions, the 42nd and 79th, where the list allows one in four, which shows as a historical departure."]),
        force("salamanca-hope", PB, "Hope's 7th Division", "Wellington's army", AP,
              "In reserve behind the allied left, with the King's German Legion and Brunswick light troops.",
              [bde("pb-kgl-light-brigade", "Halkett's Brigade", "Col Colin Halkett",
                   [u("pb-kgl-light", "1st Light Bn KGL"), u("pb-kgl-light", "2nd Light Bn KGL"), u("pb-brunswick-light", "Brunswick Oels (seven companies)")]),
               pb_bde("De Bernewitz's Brigade", "Maj-Gen de Bernewitz",
                      [light("51st Light Infantry"), light("68th Light Infantry"), u("pb-line", "Chasseurs Britanniques", options=["chasseurs"])]),
               pt_bde("Collins's Portuguese Brigade", "Col Richard Collins", ["7th Line", "19th Line"], "2nd Caçadores"),
               pb_battery("May's Battery")],
              command=[cmd("pb-div-cmd", "Maj-Gen John Hope")],
              notes=["De Bernewitz's brigade had two Light battalions in three where the list allows one in four, which shows as a historical departure.", PT2]),
        force("salamanca-light", PB, "The Light Division", "Wellington's army", AP,
              "On the far left, facing Foy, it pressed the French right as the army broke and harried the retreat.",
              [bde("pb-light-brigade", "Barnard's Brigade", "Lt-Col Andrew Barnard",
                   [u("pb-light-inf", "1/43rd Light Infantry"), u("pb-cacadores", "1st Caçadores"), u("pb-rifle-coys", "2/95th and 3/95th Rifles (four companies)")]),
               bde("pb-light-brigade", "Vandeleur's Brigade", "Maj-Gen John Vandeleur",
                   [u("pb-light-inf", "1/52nd Light Infantry"), u("pb-cacadores", "3rd Caçadores"), u("pb-rifle-bn", "1/95th Rifles")]),
               bde("pb-horse-artillery", "Ross's Troop RHA", units=[u("pb-royal-horse-arty", "Ross's Troop RHA")])],
              command=[cmd("pb-div-cmd", "Maj-Gen Charles Alten")],
              notes=["Two Light Brigades where the list takes one show as a historical departure."]),
        force("salamanca-portuguese", PB, "Pack's and Bradford's Portuguese", "Independent brigades", AP,
              "Pack's brigade stormed the Greater Arapile and was thrown off it by Bonet's men; Bradford's came in on the right with Leith.",
              [pt_bde("Pack's Brigade", "Brig-Gen Denis Pack", ["1st Line", "16th Line"], "4th Caçadores"),
               pt_bde("Bradford's Brigade", "Brig-Gen Thomas Bradford", ["13th Line", "24th Line"], "5th Caçadores"),
               pb_battery("Arriaga's Portuguese Battery", "pb-portuguese-arty")],
              command=[cmd("pb-div-cmd", "Brig-Gen Denis Pack")],
              notes=[PT2, "Without British brigades for the Portuguese ones to go with, the list's ratio shows as a historical departure."]),
        force("salamanca-heavy", PB, "Le Marchant's and Bock's Heavy Dragoons", "Cotton's cavalry", AP,
              "Le Marchant's brigade rode into Maucune's and Brenier's broken battalions and destroyed eight of them in the most successful British cavalry charge of the war; Le Marchant was killed at its head.",
              [bde("pb-heavy-cavalry-brigade", "Le Marchant's Brigade", "Maj-Gen John Le Marchant",
                   [u("pb-dragoon-guards", "5th Dragoon Guards"), u("pb-dragoon-guards", "3rd Dragoons"), u("pb-dragoon-guards", "4th Dragoons")]),
               bde("pb-heavy-cavalry-brigade", "Bock's Brigade", "Maj-Gen von Bock",
                   [u("pb-dragoon-guards", "1st Dragoons KGL", options=["kgl"]), u("pb-dragoon-guards", "2nd Dragoons KGL", options=["kgl"])]),
               bde("pb-horse-artillery", "Bull's Troop RHA", units=[u("pb-royal-horse-arty", "Bull's Troop RHA")])],
              command=[cmd("pb-div-cmd", "Lt-Gen Sir Stapleton Cotton")],
              notes=["Cavalry on its own has no infantry brigades for its brigades to go with, which shows as a historical departure."]),
        force("salamanca-light-cav", PB, "Anson's, Alten's and D'Urban's Cavalry", "Cotton's cavalry", AP,
              "D'Urban's Portuguese and the 14th Light Dragoons led the attack on the head of the French column with Pakenham; Anson's light dragoons covered the left.",
              [bde("pb-light-cavalry-brigade", "Anson's Brigade", "Maj-Gen George Anson",
                   [u("pb-light-dragoon-hussar", "11th Light Dragoons"), u("pb-light-dragoon-hussar", "12th Light Dragoons"), u("pb-light-dragoon-hussar", "16th Light Dragoons")]),
               bde("pb-light-cavalry-brigade", "Alten's Brigade", "Maj-Gen Victor von Alten", [u("pb-light-dragoon-hussar", "14th Light Dragoons"), kgl("1st Hussars KGL")]),
               bde("pb-portuguese-cavalry-brigade", "D'Urban's Portuguese", "Brig-Gen Benjamin D'Urban",
                   [u("pb-portuguese-cavalry", "1st Dragoons"), u("pb-portuguese-cavalry", "11th Dragoons")]),
               bde("pb-horse-artillery", "McDonald's Troop RHA", units=[u("pb-royal-horse-arty", "McDonald's Troop RHA")])],
              command=[cmd("pb-div-cmd", "Lt-Gen Sir Stapleton Cotton")],
              notes=["Cavalry on its own has no infantry brigades for its brigades to go with, which shows as a historical departure."]),
        fr_div("salamanca-thomieres", "Thomières's Division", "7th Division, Army of Portugal", "Gén. de Brigade Thomières",
               [("Bonté's Brigade", "Gén. de Brigade Bonté", [R("1er", 3), R("62e", 2)]), ("Second Brigade", "", [R("101e", 3)])],
               "Leading the French march west, it was caught strung out on the road by Pakenham and D'Urban and broken; Thomières was killed.",
               ["The 23rd Léger, its other regiment, was absent."]),
        fr_div("salamanca-maucune", "Maucune's Division", "5th Division, Army of Portugal", "Gén. de Division Maucune",
               [("Arnaud's Brigade", "Gén. de Brigade Arnaud", [R("15e", 3), R("66e", 2)]), ("Montfort's Brigade", "Gén. de Brigade Montfort", [R("82e", 2), R("86e", 2)])],
               "Formed square against the British cavalry, it was broken by Leith's volley and then ridden down by Le Marchant's dragoons."),
        fr_div("salamanca-brenier", "Brenier's Division", "6th Division, Army of Portugal", "Gén. de Division Brenier",
               [("Taupin's Brigade", "Gén. de Brigade Taupin", [R("17e", 2, "Léger"), R("65e", 3)]),
                ("Second Brigade", "", [R("22e", 3), {"name": "Régiment de Prusse", "units": [u("pf-line", "Régiment de Prusse (remnants)", options=["small"])]}])],
               "Coming up to support Maucune, it was caught by Le Marchant's charge as it formed and swept away.",
               ["The Régiment de Prusse, only remnants by then, is a Small battalion."]),
        fr_div("salamanca-clausel", "Clausel's Division", "2nd Division, Army of Portugal", "Gén. de Division Clausel",
               [("Berlier's Brigade", "Gén. de Brigade Berlier", [R("25e", 3, "Léger"), R("27e", 2)]),
                ("Barbot's Brigade", "Gén. de Brigade Barbot", [R("50e", 3), R("59e", 2)])],
               "Clausel took command of the army when Marmont and Bonet were wounded, and his division led the counter-attack that threw back Cole and Pack before Clinton's 6th Division stopped it."),
        fr_div("salamanca-bonet", "Bonet's Division", "8th Division, Army of Portugal", "Gén. de Division Bonet",
               [("Gautier's Brigade", "Gén. de Brigade Gautier", [R("118e", 3), R("119e", 3)]), ("Second Brigade", "", [R("120e", 3), R("122e", 3)])],
               "Held the Greater Arapile, throwing Pack's Portuguese off it, and joined Clausel's counter-attack; Bonet was wounded."),
        fr_div("salamanca-ferey", "Ferey's Division", "3rd Division, Army of Portugal", "Gén. de Division Ferey",
               [("Menne's Brigade", "Gén. de Brigade Menne", [R("31e", 2, "Léger"), R("26e", 2)]), ("Second Brigade", "", [R("47e", 3), R("70e", 2)])],
               "Formed the rearguard as the army broke, standing in line against Clinton's division until nightfall to cover the retreat; Ferey was killed."),
        fr_div("salamanca-sarrut", "Sarrut's Division", "4th Division, Army of Portugal", "Gén. de Division Sarrut",
               [("Fririon's Brigade", "Gén. de Brigade Fririon", [R("2e", 3, "Léger"), R("36e", 3)]), ("Second Brigade", "", [R("4e", 3, "Léger")])],
               "Following behind Thomières and Maucune, it came up too late to help them and joined the retreat.",
               ["The 130th Ligne, its other regiment, was absent."]),
        fr_div("salamanca-foy", "Foy's Division", "1st Division, Army of Portugal", "Gén. de Division Foy",
               [("Chemineau's Brigade", "Gén. de Brigade Chemineau", [R("6e", 2, "Léger"), R("69e", 2)]),
                ("Desgraviers's Brigade", "Gén. de Brigade Desgraviers-Berthelot", [R("39e", 2), R("76e", 2)])],
               "On the French right facing the Light Division, it held together through the rout and covered the retreat to the Tormes."),
        force("salamanca-cavalry", PF, "Curto's and Boyer's Cavalry", "Army of Portugal", "French",
              "Curto's light horse was scattered with Thomières's division; Boyer's dragoons tried to cover the retreat.",
              [pf_cav("Curto's First Brigade", "Gén. de Brigade Curto", [("3e", "Hussards"), ("22e", "Chasseurs"), ("26e", "Chasseurs"), ("28e", "Chasseurs")]),
               pf_cav("Curto's Second Brigade", "", [("13e", "Chasseurs"), ("14e", "Chasseurs")]),
               pf_cav("Boyer's Dragoons", "Gén. de Brigade Boyer", [("6e", "Dragons"), ("11e", "Dragons"), ("15e", "Dragons"), ("25e", "Dragons")]),
               pf_battery("Horse Battery", "pf-horse-arty")],
              command=[cmd("pf-div-cmd", "Gén. de Brigade Boyer")],
              notes=["Several of these regiments had only one or two squadrons; the 28th Chasseurs (one squadron) could be Small. Cavalry without the infantry brigades it's allowed by shows as a historical departure."]),
    ],
}

# ================================================================ Vitoria, 21 June 1813

FR2 = "No source gives the battalions of each French regiment in 1813; two each, as the divisions' strengths suggest, is how they're shown."
VITORIA = {
    "id": "vitoria", "name": "Vitoria", "date": "21 June 1813", "campaign": "peninsular-war",
    "summary": "Wellington caught King Joseph's three armies in the basin of Vitoria with their backs to the Pyrenees. Hill attacked over the La Puebla heights in the south, the centre columns crossed the Zadorra by its bridges, and Graham came down on the French line of retreat from the north. The French broke, abandoning their guns, their baggage and the treasure of a kingdom, and fled for France.",
    "sources": [wiki("Battle_of_Vitoria_order_of_battle", "Battle of Vitoria order of battle"), wiki("Battle_of_Vitoria", "Battle of Vitoria")],
    "forces": [
        force("vitoria-stewart", PB, "Stewart's 2nd Division", "Right Column (Hill)", AL,
              "Opened the battle on the right, storming the heights of La Puebla with Morillo's Spaniards and holding them against Gazan's counter-attacks.",
              [pb_bde("Cadogan's Brigade", "Col the Hon Henry Cadogan", [line("1/50th Foot"), highland("1/71st Highland Light Infantry"), highland("1/92nd Highlanders"), rifles()]),
               pb_bde("Byng's Brigade", "Maj-Gen John Byng", [line("1/3rd Foot (Buffs)"), line("1/57th Foot"), line("1st Provisional Bn (2/31st, 2/66th)")]),
               pb_bde("O'Callaghan's Brigade", "Col the Hon Robert O'Callaghan", [line("1/28th Foot"), line("2/34th Foot"), line("1/39th Foot")]),
               pt_bde("Ashworth's Portuguese Brigade", "Brig-Gen Charles Ashworth", ["6th Line", "18th Line"], "6th Caçadores"),
               pb_battery("Maxwell's Battery")],
              command=[cmd("pb-div-cmd", "Lt-Gen Sir William Stewart")],
              notes=["Cadogan's brigade had two Highland battalions, the 71st and 92nd, where the list allows one in four, which shows as a historical departure. Cadogan was killed on the heights.",
                     "Each brigade had a company of the 5/60th; one is shown, the list allowing one in an army."]),
        force("vitoria-silveira", PB, "Silveira's Portuguese Division", "Right Column (Hill)", AL,
              "Hill's Portuguese division, following the 2nd Division along the Puebla heights and the valley below.",
              [pt_bde("Da Costa's Brigade", "Brig-Gen Hippolita da Costa", ["2nd Line", "14th Line"]),
               pt_bde("Campbell's Brigade", "Brig-Gen Archibald Campbell", ["4th Line", "10th Line"], "10th Caçadores"),
               pb_battery("Portuguese Battery", "pb-portuguese-arty")],
              command=[cmd("pb-div-cmd", "Maj-Gen Francisco Silveira")],
              notes=["Without British brigades for its Portuguese ones to go with, the list's ratio shows as a historical departure. Tulloh's two Portuguese batteries are shown as one."]),
        force("vitoria-morillo", SP, "Morillo's Spanish Division", "Right Column (Hill)", "Spanish",
              "Led the climb onto the heights of La Puebla and fought for them all morning; Morillo was wounded.",
              [bde("sp-infantry-brigade", "First Brigade", "", regiments=[sp_regiment("León"), sp_regiment("Unión"), sp_regiment("Legión")]),
               bde("sp-infantry-brigade", "Second Brigade", "", regiments=[sp_regiment("Bailén"), sp_regiment("Victoria"), sp_regiment("2nd Jaén")])],
              command=[cmd("sp-div-cmd", "Maj-Gen Pablo Morillo")],
              notes=["The order of battle lists the division's regiments without brigades or battalion counts; one battalion each, in two brigades."]),
        force("vitoria-cole", PB, "Cole's 4th Division", "Right Centre Column (Cole)", AL,
              "Crossed the Zadorra at Nanclares and pushed into the French centre around Ariñez as the line gave way.",
              [pb_bde("Anson's Brigade", "Maj-Gen William Anson", [line("3/27th Foot"), line("1/40th Foot"), line("1/48th Foot"), line("2nd Provisional Bn (2nd, 2/53rd)"), rifles()]),
               pb_bde("Skerrett's Fusilier Brigade", "Maj-Gen John Skerrett", [line("1/7th Fusiliers"), line("20th Foot"), line("1/23rd Royal Welch Fusiliers")]),
               pt_bde("Stubbs's Portuguese Brigade", "Col George Stubbs", ["11th Line", "23rd Line"], "7th Caçadores"),
               pb_battery("Sympher's Battery KGL")],
              command=[cmd("pb-div-cmd", "Lt-Gen Sir Lowry Cole")],
              notes=["Skerrett's company of the Brunswick Oels is left out, the list allowing one such company in an army."]),
        force("vitoria-light", PB, "The Light Division", "Right Centre Column (Cole)", AL,
              "Guided over the unguarded bridge at Tres Puentes, it got across the Zadorra behind the French centre and opened the way for the rest.",
              [bde("pb-light-brigade", "Kempt's Brigade", "Maj-Gen James Kempt",
                   [u("pb-light-inf", "1/43rd Light Infantry"), u("pb-cacadores", "3rd Caçadores"), u("pb-rifle-bn", "1/95th Rifles"), u("pb-rifle-coys", "3/95th Rifles (five companies)")]),
               bde("pb-light-brigade", "Vandeleur's Brigade", "Maj-Gen John Vandeleur",
                   [u("pb-light-inf", "1/52nd Light Infantry"), u("pb-cacadores", "1st Caçadores"), u("pb-rifle-coys", "2/95th Rifles (six companies)"), pt_line("17th Portuguese Line")]),
               bde("pb-horse-artillery", "Ross's Troop RHA", units=[u("pb-royal-horse-arty", "Ross's Troop RHA")])],
              command=[{"unit": "pb-cmd-wellington"}],
              notes=["Wellington rode with the centre, so the book's named Wellington leads it here; Alten commanded the division.",
                     "Two Light Brigades where the list takes one show as a historical departure. The order of battle names no commander for the 1st Brigade; Kempt led it at the bridge."]),
        force("vitoria-picton", PB, "Picton's 3rd Division", "Left Centre Column (Dalhousie)", AL,
              "Tired of waiting for Dalhousie, Picton led his division over the bridge of Mendoza and into the French centre, carrying the knoll of Ariñez.",
              [pb_bde("Brisbane's Brigade", "Maj-Gen Thomas Brisbane",
                      [line("1/45th Foot"), highland("74th Highlanders"), line("1/88th Connaught Rangers"), u("pb-rifle-coys", "5/60th Rifles (three companies)")]),
               pb_bde("Colville's Brigade", "Maj-Gen Charles Colville", [line("1/5th Foot"), line("2/83rd Foot"), line("2/87th Foot"), line("94th Foot")]),
               pt_bde("Power's Portuguese Brigade", "Maj-Gen Manley Power", ["9th Line", "21st Line"], "11th Caçadores"),
               pb_battery("Douglas's Battery")],
              command=[{"unit": "pb-cmd-picton"}],
              notes=["Picton is the book's named commander."]),
        force("vitoria-dalhousie", PB, "Dalhousie's 7th Division", "Left Centre Column (Dalhousie)", AL,
              "Came up late through the hills and crossed the Zadorra behind Picton to join the attack on the French centre.",
              [pb_bde("Barnes's Brigade", "Maj-Gen Edward Barnes",
                      [line("1/6th Foot"), line("3rd Provisional Bn (2/24th, 2/58th)"), u("pb-brunswick-light", "Brunswick Oels (seven companies)")]),
               pb_bde("Grant's Brigade", "Col William Grant",
                      [light("51st Light Infantry"), light("68th Light Infantry"), line("1/82nd Foot"), u("pb-line", "Chasseurs Britanniques", options=["chasseurs"])]),
               pt_bde("Le Cor's Portuguese Brigade", "Maj-Gen Frederico Le Cor", ["7th Line", "19th Line"], "2nd Caçadores"),
               pb_battery("Cairnes's Battery")],
              command=[cmd("pb-div-cmd", "Lt-Gen the Earl of Dalhousie")],
              notes=["Grant's brigade had two Light battalions in four where the list allows one, which shows as a historical departure."]),
        force("vitoria-howard", PB, "Howard's 1st Division", "Left Column (Graham)", AL,
              "With Graham's column, which came down on the French right and the Bayonne road, their line of retreat, around Gamarra.",
              [bde("pb-guards-brigade", "Stopford's Guards Brigade", "Maj-Gen the Hon Edward Stopford",
                   [u("pb-foot-guard", "1/Coldstream Guards"), u("pb-foot-guard", "1/3rd Foot Guards"), rifles()]),
               bde("pb-kgl-brigade", "Halkett's KGL Brigade", "Col Colin Halkett",
                   [line("1st Line Bn KGL"), line("2nd Line Bn KGL"), line("5th Line Bn KGL"), u("pb-kgl-light", "1st Light Bn KGL"), u("pb-kgl-light", "2nd Light Bn KGL")]),
               pb_battery("Dubourdieu's Battery")],
              command=[cmd("pb-div-cmd", "Maj-Gen Kenneth Howard")],
              notes=["The Guards Brigade comes with two British or KGL brigades in the list, and here there's one, which shows as a historical departure."]),
        force("vitoria-oswald", PB, "Oswald's 5th Division", "Left Column (Graham)", AL,
              "Stormed the village of Gamarra Mayor and fought for its bridge against Reille's Army of Portugal, closing the road to France.",
              [pb_bde("First Brigade", "", [line("3/1st Foot (Royal Scots)"), line("1/9th Foot"), line("1/38th Foot"), u("pb-brunswick-oels-coy", "Brunswick Oels (company)")]),
               pb_bde("Robinson's Brigade", "Maj-Gen Frederick Robinson", [line("1/4th Foot"), line("2/47th Foot"), line("2/59th Foot")]),
               pt_bde("Spry's Portuguese Brigade", "Brig-Gen William Spry", ["3rd Line", "15th Line"], "8th Caçadores"),
               pb_battery("Lawson's Battery")],
              command=[cmd("pb-div-cmd", "Maj-Gen John Oswald")],
              notes=["Robinson's company of the Brunswick Oels is left out, the list allowing one such company in an army."]),
        force("vitoria-portuguese", PB, "Pack's and Bradford's Portuguese", "Left Column (Graham)", AL,
              "Graham's two independent Portuguese brigades, which led the attack on the heights before Gamarra and Abechuco.",
              [pt_bde("Pack's Brigade", "Maj-Gen Denis Pack", ["1st Line", "16th Line"], "4th Caçadores"),
               pt_bde("Bradford's Brigade", "Maj-Gen Thomas Bradford", ["13th Line", "24th Line"], "5th Caçadores")],
              command=[cmd("pb-div-cmd", "Lt-Gen Sir Thomas Graham")],
              notes=["Without British brigades for the Portuguese ones to go with, the list's ratio shows as a historical departure."]),
        force("vitoria-longa", SP, "Longa's Spanish Division", "Left Column (Graham)", "Spanish",
              "Longa's Cantabrians seized the bridge at Durana on the Bayonne road, cutting the French off from their best line of retreat.",
              [bde("sp-infantry-brigade", "First Brigade", "", regiments=[sp_regiment("1st Iberia"), sp_regiment("2nd Iberia")]),
               bde("sp-infantry-brigade", "Second Brigade", "", regiments=[sp_regiment("3rd Iberia"), sp_regiment("4th Iberia"), sp_regiment("Guardias Nacionales")])],
              command=[cmd("sp-div-cmd", "Col Francisco de Longa")],
              notes=["One battalion each, in two brigades; the Húsares de Iberia and Salcedo's guerrillas are left out."]),
        force("vitoria-heavy", PB, "The Heavy Cavalry", "Hill's Household, Ponsonby's, Fane's and Bock's brigades", AL,
              "Waiting through the morning for the infantry to open the way, the heavy brigades crossed the Zadorra in the afternoon and pressed the French as they broke.",
              [bde("pb-heavy-cavalry-brigade", "Hill's Household Brigade", "Lt-Col Robert Hill",
                   [u("pb-household-cavalry", "1st Life Guards"), u("pb-household-cavalry", "2nd Life Guards"), u("pb-household-cavalry", "Royal Horse Guards")]),
               bde("pb-heavy-cavalry-brigade", "Ponsonby's Brigade", "Maj-Gen William Ponsonby",
                   [u("pb-dragoon-guards", "5th Dragoon Guards"), u("pb-dragoon-guards", "3rd Dragoons"), u("pb-dragoon-guards", "4th Dragoons")]),
               bde("pb-heavy-cavalry-brigade", "Fane's Brigade", "Maj-Gen Henry Fane", [u("pb-dragoon-guards", "3rd Dragoon Guards"), u("pb-dragoon-guards", "1st Dragoons")]),
               bde("pb-heavy-cavalry-brigade", "Bock's Brigade", "Maj-Gen von Bock",
                   [u("pb-dragoon-guards", "1st Dragoons KGL", options=["kgl"]), u("pb-dragoon-guards", "2nd Dragoons KGL", options=["kgl"])]),
               bde("pb-horse-artillery", "Ramsay's Troop RHA", units=[u("pb-royal-horse-arty", "Ramsay's Troop RHA")])],
              command=[cmd("pb-div-cmd", "Lt-Gen Sir Stapleton Cotton")],
              notes=["The Household brigade had no Dragoon regiments, which the list's heavy brigade needs, and cavalry alone has no infantry brigades for its brigades to go with; these show as historical departures."]),
        force("vitoria-light-cav", PB, "The Light Cavalry", "Grant's, Alten's, Anson's and D'Urban's brigades", AL,
              "Grant's hussars and the light dragoons pursued the broken French past Vitoria, where many stopped to plunder the abandoned baggage train.",
              [bde("pb-light-cavalry-brigade", "Grant's Hussar Brigade", "Col Colquhoun Grant",
                   [u("pb-light-dragoon-hussar", "10th Hussars"), u("pb-light-dragoon-hussar", "15th Hussars"), u("pb-light-dragoon-hussar", "18th Hussars")]),
               bde("pb-light-cavalry-brigade", "Alten's Brigade", "Maj-Gen Victor von Alten", [u("pb-light-dragoon-hussar", "14th Light Dragoons"), kgl("1st Hussars KGL")]),
               bde("pb-light-cavalry-brigade", "Anson's Brigade", "Maj-Gen George Anson", [u("pb-light-dragoon-hussar", "12th Light Dragoons"), u("pb-light-dragoon-hussar", "16th Light Dragoons")]),
               bde("pb-portuguese-cavalry-brigade", "D'Urban's Portuguese", "Brig-Gen Benjamin D'Urban",
                   [u("pb-portuguese-cavalry", "1st Dragoons"), u("pb-portuguese-cavalry", "11th Dragoons"), u("pb-portuguese-cavalry", "12th Dragoons")]),
               bde("pb-horse-artillery", "Gardiner's Troop RHA", units=[u("pb-royal-horse-arty", "Gardiner's Troop RHA")])],
              command=[cmd("pb-div-cmd", "Col Colquhoun Grant")],
              notes=["Cavalry on its own has no infantry brigades for its brigades to go with, which shows as a historical departure."]),
        # ---- French
        fr_div("vitoria-leval", "Leval's Division", "1st Division, Army of the South (Gazan)", "Gén. de Division Leval",
               [("Mocquery's Brigade", "Gén. de Brigade Mocquery", [R("9e", 2, "Léger"), R("24e", 2)]), ("Morgan's Brigade", "Gén. de Brigade Morgan", [R("88e", 2), R("96e", 2)])],
               "Held the French front line south of the Zadorra until the centre was turned, and fell back with the Army of the South.", [FR2]),
        fr_div("vitoria-villatte", "Villatte's Division", "3rd Division, Army of the South (Gazan)", "Gén. de Division Villatte",
               [("Rignoux's Brigade", "Gén. de Brigade Rignoux", [R("27e", 2, "Léger"), R("63e", 2)]), ("Lefol's Brigade", "Gén. de Brigade Lefol", [R("94e", 2), R("95e", 2)])],
               "Fought Hill's corps for the heights of La Puebla through the morning, then covered the retreat.", [FR2]),
        fr_div("vitoria-conroux", "Conroux's Division", "4th Division, Army of the South (Gazan)", "Gén. de Division Conroux",
               [("Rey's Brigade", "Gén. de Brigade Rey", [R("32e", 2), R("43e", 2)]), ("Schwiter's Brigade", "Gén. de Brigade Schwiter", [R("55e", 2), R("58e", 2)])],
               "Gazan's left, facing Hill along the road below the Puebla heights.", [FR2]),
        fr_div("vitoria-darricau", "Darricau's Division", "6th Division, Army of the South (Gazan)", "Gén. de Division Darricau",
               [("Saint-Pol's Brigade", "Gén. de Brigade Saint-Pol", [R("21e", 2, "Léger"), R("100e", 2)]), ("Remond's Brigade", "Gén. de Brigade Remond", [R("28e", 2, "Léger"), R("103e", 2)]),
                ("Maransin's Brigade", "Gén. de Brigade Maransin", [R("12e", 2, "Léger"), R("45e", 2)])],
               "Held the centre at Ariñez against the British crossing the Zadorra; Maransin's brigade, detached from the 5th Division, fought beside it at Subijana.",
               [FR2, "Maransin's brigade, the 5th Division's only one present, is added as a third brigade."]),
        force("vitoria-south-cav", PF, "The Army of the South's Cavalry", "Soult's, Tilly's and Digeon's divisions", "French",
              "Gazan's cavalry, which covered the army's retreat as its infantry broke.",
              [pf_cav("Soult's Light Cavalry", "Gén. de Division Pierre Soult", [("2e", "Hussards"), ("21e", "Chasseurs"), ("5e", "Chasseurs"), ("10e", "Chasseurs")]),
               pf_cav("Tilly's Dragoons", "Gén. de Division Tilly", [("2e", "Dragons"), ("4e", "Dragons"), ("14e", "Dragons"), ("26e", "Dragons")]),
               pf_cav("Digeon's Dragoons", "Gén. de Division Digeon", [("5e", "Dragons"), ("12e", "Dragons"), ("16e", "Dragons"), ("21e", "Dragons")]),
               pf_battery("Horse Battery", "pf-horse-arty")],
              command=[cmd("pf-div-cmd", "Gén. de Division Tilly")],
              notes=["Each division's two brigades are shown as one. Cavalry without the infantry brigades it's allowed by shows as a historical departure."]),
        fr_div("vitoria-darmagnac", "Darmagnac's Division", "1st Division, Army of the Centre (d'Erlon)", "Gén. de Division Darmagnac",
               [("Chassé's Brigade", "Gén. de Brigade Chassé", [R("28e", 2), R("75e", 2)]),
                ("Neuenstein's German Brigade", "Gén. de Brigade Neuenstein", [R("2nd Nassau", 2, "Infantry"), R("4th Baden", 2, "Infantry"), R("Frankfurt", 1, "Infantry")])],
               "Held the line of the Zadorra opposite Dalhousie's column and fell back across the plain when the centre broke.",
               [FR2, "The list has no German allies, so the Nassau, Baden and Frankfurt battalions are the list's Line battalions."]),
        fr_div("vitoria-cassagne", "Cassagne's Division", "2nd Division, Army of the Centre (d'Erlon)", "Gén. de Division Cassagne",
               [("Braun's Brigade", "Col Joseph Braun", [R("16e", 2, "Léger"), R("8e", 2)]), ("Blondeau's Brigade", "Gén. de Brigade Blondeau", [R("51e", 2), R("54e", 2)])],
               "D'Erlon's second division, in the second line behind the centre.", [FR2]),
        fr_div("vitoria-sarrut", "Sarrut's Division", "4th Division, Army of Portugal (Reille)", "Gén. de Division Sarrut",
               [("Fririon's Brigade", "Gén. de Brigade Fririon", [R("2e", 2, "Léger"), R("36e", 2)]), ("Menne's Brigade", "Gén. de Brigade Menne", [R("4e", 2, "Léger"), R("65e", 2)])],
               "Fought Graham's column for the villages and bridges of the upper Zadorra, holding the road to France until the rest of the army had gone; Sarrut was mortally wounded.", [FR2]),
        fr_div("vitoria-lamartiniere", "Lamartinière's Division", "6th Division, Army of Portugal (Reille)", "Gén. de Division Lamartinière",
               [("First Brigade", "", [R("118e", 2), R("119e", 2)]), ("Second Brigade", "", [R("120e", 2), R("122e", 2)])],
               "Defended Gamarra Mayor and its bridge against Oswald's 5th Division in some of the hardest fighting of the day.", [FR2]),
        force("vitoria-reille-cav", PF, "Reille's and d'Erlon's Cavalry", "Armies of Portugal and the Centre", "French",
              "The cavalry of the two northern armies, which covered Reille's withdrawal from the Zadorra.",
              [pf_cav("Curto's Brigade", "Gén. de Brigade Curto", [("13e", "Chasseurs"), ("22e", "Chasseurs")]),
               pf_cav("Mermet's Second Brigade", "Gén. de Division Mermet", [("3e", "Hussards"), ("14e", "Chasseurs"), ("26e", "Chasseurs")]),
               pf_cav("Boyer's Dragoons", "Gén. de Brigade Boyer", [("6e", "Dragons"), ("11e", "Dragons"), ("15e", "Dragons"), ("25e", "Dragons")]),
               pf_battery("Horse Battery", "pf-horse-arty")],
              command=[cmd("pf-div-cmd", "Gén. de Division Mermet")],
              notes=["Trelliard's and Avy's divisions of the Army of the Centre are left out. Cavalry without the infantry brigades it's allowed by shows as a historical departure."]),
    ],
}

# Departures the forces' own notes don't already explain
SMALL_BRIGADE = ("The list allows one Highland or Light battalion in four, so a brigade of three may have none; "
                 "where one had a Highland or Light regiment, that shows as a historical departure.")
HORSE_GUNS = "The list allows horse artillery by the cavalry taken, so a horse troop with an infantry division shows as a historical departure."
EXTRA_NOTES = {
    "corunna-baird": [SMALL_BRIGADE], "corunna-paget": [SMALL_BRIGADE], "corunna-fraser": [SMALL_BRIGADE],
    "salamanca-pakenham": [SMALL_BRIGADE], "vitoria-picton": [SMALL_BRIGADE],
    "talavera-mackenzie": [ARTILLERY], "talavera-campbell": [ARTILLERY],
    "salamanca-light": [HORSE_GUNS], "vitoria-light": [HORSE_GUNS],
}

PERIODS = {"corunna": "middle", "talavera": "middle", "salamanca": None, "vitoria": "late"}

for b in (CORUNNA, TALAVERA, SALAMANCA, VITORIA):
    for f in b["forces"]:
        # Moore's army and Wellesley's at Talavera were British, without Portuguese (Cuesta's Spanish are left out)
        if b["id"] in ("corunna", "talavera") and f["side"] == AP:
            f["side"] = "British"
        f.setdefault("notes", [])
        f["notes"][:0] = EXTRA_NOTES.get(f["id"], [])
        # Salamanca is 1812: the British list's Middle period and the French list's Late
        if b["id"] == "salamanca":
            f["period"] = "middle" if f["nationId"] == PB else "late"
        else:
            f["period"] = PERIODS[b["id"]]


if __name__ == "__main__":
    for b in (CORUNNA, TALAVERA, SALAMANCA, VITORIA):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in ART:
            b["art"] = ART[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
