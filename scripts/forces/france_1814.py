"""
Writes the forces of the Campaign in France (src/data/battles/*.json): Brienne's and La Rothière's French
forces from Nafziger's orders of battle, with the allies still to come; and the other battles' armies, every side's
still to come, as Wikipedia's pages on them give their corps and divisions.

    python3 scripts/forces/france_1814.py && npm run check:forces

There are no 1814 army lists, so every force borrows the nearest, as 1813's do: A Clash of Eagles' 1812 lists for
the French and the Imperial Guard. Each force's notes say so. Summaries are our own words. Staff Ratings are set
by ratings.py.
"""

import copy
import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from liberation_1813 import (AU, BAV, CAV_ONLY, FIG, FR, LIST_RU, WT, bns, MARINES, NAF, PR15, PR_GROUPED, PR_LIST, PR_SUB, PR_WHOLE, RU,
                             bn_list, marine, pc, pi, pres, regt, ru_regt)

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
ART = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
RU_FLAG = "/flags/russia.svg"

LIST_FR = ("Built from A Clash of Eagles' French 1812 list, the nearest to 1814: there is no list for the army Napoleon "
           "fought with in France, of the veterans of 1813, conscripts called up that winter and battalions drawn from "
           "depots across the Empire.")
LIST_FIG = "Built from A Clash of Eagles' Imperial Guard 1812 list, the nearest to 1814."
WEAK = ("Its battalions were well below strength, a few hundred men each; they are shown at full size, and the list's "
        "Small upgrade would suit many of them.")
NEW_YG = ("Its regiments were newly raised that winter, largely of conscripts under a cadre of veterans; they are the "
          "list's Young Guard, as it rates them.")
V_CAV_ARTY = ("The corps' two horse batteries, of four 6-pdrs and two howitzers each, are one in its divisional artillery "
              "and one in its reserve, as the list takes them.")


def battle(id_, name, date, summary, sources, forces, to_come, alliances=()):
    b = {"id": id_, "name": name, "date": date, "campaign": "france-1814", "summary": summary,
         "sources": sources, "forces": forces, "toCome": to_come, "alliances": [list(a) for a in alliances]}
    # A battle with nothing still to come, or no allies fighting apart, leaves those out
    return {k: v for k, v in b.items() if v or k not in ("toCome", "alliances")}


def write(b):
    ratings.apply(b)
    commanders.apply(b)
    if b["id"] in ART:
        b["art"] = ART[b["id"]]
    # Keep the file's keys in the order the others have them
    order = ["id", "name", "date", "campaign", "art", "sides", "alliances", "summary", "sources", "forces", "toCome"]
    out = {k: b[k] for k in order if k in b}
    (OUT / f"{b['id']}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(f"{b['name']}: {len(b['forces'])} forces, {len(b.get('toCome', []))} to come")


def bn(unit, label):
    """One battalion of a regiment as its own regiment: "1/24th Léger" in the 24th Léger"""
    reg = label.split("/", 1)[1]
    return regt(reg, [u(unit, label)])


def yg(reg, n=2):
    """A Young Guard regiment of voltigeurs or tirailleurs, "1/1st Voltigeurs" and on"""
    unit = "fig-yg-voltigeurs" if "Voltigeur" in reg else "fig-yg-tirailleurs"
    return regt(reg, [u(unit, f"{i}/{reg}") for i in range(1, n + 1)])


def ru(name, formation, summary, side="Russian", flag=RU_FLAG):
    return {"side": side, "name": name, "formation": formation, "summary": summary, "flag": flag}


def again(f, id_, summary, notes, formation=None):
    """A force from another battle, as it fought here, with its own summary and notes"""
    g = copy.deepcopy(f)
    g["id"], g["summary"], g["notes"] = id_, summary, notes
    if formation:
        g["formation"] = formation
    g.pop("missing", None)
    return g


def one(unit, name):
    """A regiment of one battalion whose number the return does not give, as "139th Line" """
    return regt(name, [u(unit, name)])


# ================================================================ Brienne, 29 January 1814

BR_FR = {"label": "French Army under Napoleon at Châlons, 25 January 1814 (Nafziger Collection 814ABH)", "url": NAF + "814ABH.pdf"}
BR_WIKI = {"label": "Battle of La Rothière order of battle (Wikipedia, after Nafziger and Petre)",
           "url": "https://en.wikipedia.org/wiki/Battle_of_La_Rothi%C3%A8re_order_of_battle"}
BR_BATTLE = {"label": "Battle of Brienne (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Brienne"}
BR_NOTE = "After Nafziger's return of the army under Napoleon at Châlons on 25 January, four days before the battle."
II_ARTY = ("Nafziger gives the II Corps' batteries together, not by division: four 6-pdr foot batteries, a 12-pdr battery and "
           "three horse batteries. One of the 6-pdr foot batteries is with each division here.")

BR_DUHESME = force(
    "brienne-duhesme", FR, "Duhesme's Division", "1st Division, II Corps (Victor)", "French",
    "Victor's leading division, which reached the field at half past three and attacked Olsufiev's Russians in the town, "
    "fighting them to a standstill for an hour. With no cavalry on its flank it was ridden over by Pahlen's and "
    "Vasilchikov's squadrons and lost eight guns; but after dark Huguet-Chateau led four hundred men of the 37th and 56th "
    "up an unguarded road into the château, and nearly took Blücher and Gneisenau there.",
    [bde("fr-infantry-brigade", "Duhesme's First Brigade",
         regiments=[bn("fr-light-infantry", "1/24th Léger"), bn("fr-line-infantry", "1/19th Line")]),
     bde("fr-infantry-brigade", "Huguet-Chateau's Brigade", "Gén. de Brigade Huguet-Chateau",
         regiments=[bn("fr-line-infantry", "1/37th Line"), bn("fr-line-infantry", "1/56th Line")]),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "7/2nd Foot Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Duhesme")],
    notes=[LIST_FR, BR_NOTE,
           "Each regiment had a single battalion here, of five to nine hundred men; each is shown as its one battalion.",
           "Nafziger gives the division without its brigades. Huguet-Chateau's brigade of the 37th and 56th, which took the "
           "château, is from Petre; the 24th Léger and 19th Line are the other, whose commander isn't known.",
           II_ARTY, "Its foot battery, with four battalions where the list wants six for one, shows as a historical departure."])

BR_FORESTIER = force(
    "brienne-forestier", FR, "Forestier's Division", "2nd Division, II Corps (Victor)", "French",
    "Victor's second division, which came up behind Duhesme's into the fight for the town. Forestier was mortally wounded, "
    "and the 26th Line was cut to pieces.",
    [bde("fr-infantry-brigade", "Forestier's First Brigade",
         regiments=[bn("fr-line-infantry", "1/26th Line"), bn_list("fr-line-infantry", "18th Line", ["1", "2", "4"])]),
     bde("fr-infantry-brigade", "Forestier's Second Brigade",
         regiments=[bn("fr-line-infantry", "1/46th Line"), bn_list("fr-line-infantry", "93rd Line", ["1", "2"])]),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "19/2nd Foot Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Forestier")],
    notes=[LIST_FR, BR_NOTE, WEAK,
           "Nafziger gives the division's battalions without its brigades or their commanders; they are split into two "
           "brigades here, in his order.",
           II_ARTY])

BR_MEUNIER = force(
    "brienne-meunier", FIG, "Meunier's Division", "1st Young Guard (1st Voltigeur) Division (Ney)", "French",
    "One of Ney's two new divisions of the Young Guard, which Napoleon sent with Decouz's against the town after dark. "
    "The night assault failed in the streets, against Sacken's Russians coming up from Lesmont.",
    [bde("fig-young-guard-brigade", "Lacoste's Brigade", "Gén. de Brigade Lacoste",
         units=[u("fig-yg-foot-arty", "Young Guard Foot Battery")],
         regiments=[yg("1st Voltigeurs"), yg("2nd Voltigeurs")]),
     bde("fig-young-guard-brigade", "Rousseau's Brigade", "Gén. de Brigade Rousseau",
         regiments=[yg("3rd Voltigeurs"), yg("4th Voltigeurs")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Meunier")],
    notes=[LIST_FIG, BR_NOTE, NEW_YG,
           "Each regiment had two battalions of three to six hundred men; they are shown at full size.",
           "Nafziger gives the division a few guns, with 129 gunners and train, shown as a Young Guard foot battery; with four battalions in its brigade, where the list wants six for one, it shows as a historical departure."])

BR_DECOUZ = force(
    "brienne-decouz", FIG, "Decouz's Division", "2nd Young Guard (2nd Voltigeur) Division (Ney)", "French",
    "Ney's second Young Guard division, which reached the field between four and five and was put in on Duhesme's right, "
    "pushing deep into the town until Ney halted it. In the night assault Decouz was mortally wounded and Rear Admiral "
    "Baste, who took his place, was killed; Pelet took command.",
    [bde("fig-young-guard-brigade", "Pelet's Brigade", "Gén. de Brigade Pelet",
         units=[u("fig-yg-foot-arty", "Young Guard Foot Battery")],
         regiments=[yg("5th Voltigeurs"), yg("6th Voltigeurs")]),
     bde("fig-young-guard-brigade", "Bigarré's Brigade", "Gén. de Brigade Bigarré",
         regiments=[yg("7th Voltigeurs"), yg("8th Voltigeurs")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Decouz")],
    notes=[LIST_FIG, BR_NOTE, NEW_YG,
           "Each regiment had two battalions of about three hundred and fifty men; they are shown at full size, and the "
           "list's Small upgrade would suit them.",
           "Nafziger gives the division a few guns, with 140 gunners and train, shown as a Young Guard foot battery; with four battalions in its brigade, where the list wants six for one, it shows as a historical departure."])

BR_GUARD_CAV = force(
    "brienne-guard-cavalry", FIG, "Lefebvre-Desnouettes's Guard Cavalry", "Guard Cavalry Division (Ney)", "French",
    "The Guard horse marching with Ney, which joined in the cavalry fight on the plain north-east of the town, where "
    "Lefebvre-Desnouettes was wounded, and supported the Young Guard's night assault.",
    [bde("fig-heavy-cavalry-brigade", "Guard Heavy Cavalry",
         units=[u("fig-grenadiers-a-cheval-regt", "Grenadiers à Cheval"), u("fig-empress-dragoons", "Dragoons of the Guard"),
                u("fig-og-horse-arty", "Guard Horse Battery")]),
     bde("fig-light-cavalry-brigade", "Guard Chasseurs", units=[u("fig-chasseurs-a-cheval", "Chasseurs à Cheval")]),
     bde("fig-light-cavalry-brigade", "Polish Lancers", units=[u("fig-polish-lancers", "1st (Polish) Chevau-légers Lanciers")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Lefebvre-Desnouettes")],
    notes=[LIST_FIG, BR_NOTE,
           "Each Guard regiment had four to six hundred men here; each is shown as one unit.",
           "Nafziger gives the division without brigades; its regiments are brigaded here as the list takes them.",
           "Nafziger gives the horse artillery as three hundred gunners and train, shown as one battery."])
BR_GUARD_CAV["missing"] = [{"name": "2nd Éclaireurs", "reason": "A regiment of Guard scouts raised that winter, three hundred strong, which the 1812 list doesn't have."}]

BR_V_CAVALRY = force(
    "brienne-v-cavalry", FR, "Milhaud's Cavalry", "V Cavalry Corps, under Grouchy", "French",
    "The army's advance guard, Piré's light horse leading, which drove Shcherbatov's Cossacks out of Maizières."
    " Grouchy brought up the rest of the corps and pressed Pahlen's cavalry back through Brienne, until L'Héritier's "
    "and Briche's dragoons were stopped by the Russian Jäger in square. That night Grouchy sent L'Héritier's dragoons into "
    "the town itself, to no purpose.",
    [bde("fr-light-cavalry-brigade", "Subervie's Brigade", "Gén. de Brigade Subervie",
         units=[u("fr-hussar-regt", "3rd Hussars"), u("fr-chasseur-a-cheval", "26th Chasseurs à Cheval")]),
     bde("fr-light-cavalry-brigade", "Pac's Brigade", "Gén. de Brigade Pac",
         units=[u("fr-chasseur-a-cheval", "14th Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "27th Chasseurs à Cheval")]),
     bde("fr-heavy-cavalry-brigade", "Montélégier's Brigade", "Gén. de Brigade Montélégier",
         units=[u("fr-dragoon", "2nd Dragoons"), u("fr-dragoon", "6th Dragoons"), u("fr-dragoon", "11th Dragoons")]),
     bde("fr-heavy-cavalry-brigade", "Ludot's Brigade", "Gén. de Brigade Ludot",
         units=[u("fr-dragoon", "13th Dragoons"), u("fr-dragoon", "15th Dragoons")]),
     bde("fr-heavy-cavalry-brigade", "Lamotte's Brigade", "Gén. de Brigade Lamotte",
         units=[u("fr-dragoon", "18th Dragoons"), u("fr-dragoon", "19th Dragoons"), u("fr-dragoon", "20th Dragoons")]),
     bde("fr-heavy-cavalry-brigade", "Mermet's Brigade", "Col. Mermet",
         units=[u("fr-dragoon", "22nd Dragoons"), u("fr-dragoon", "25th Dragoons")]),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-horse-arty", "4/2nd Horse Artillery")]),
     bde("fr-artillery-brigade", "Corps Artillery (Etchegoyen)", units=[u("fr-horse-arty", "2/3rd Horse Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Milhaud")],
    notes=[LIST_FR, BR_NOTE,
           "Piré's 9th Light Cavalry Division is the two light brigades, Briche's 5th Heavy Division Montélégier's and Ludot's "
           "dragoons, and L'Héritier's 6th Heavy Division Lamotte's and Mermet's. Grouchy, who commanded the army's cavalry, "
           "led them on the day.",
           "Its regiments were weak, a hundred and fifty to four hundred men each; they are shown at full size, and the "
           "list's Small upgrade would suit many of them.",
           "The dragoon divisions were veterans brought from Spain that winter.",
           V_CAV_ARTY,
           "Four heavy cavalry brigades, where the list takes one, and more heavy cavalry than its half of the army for "
           "corps support, show as historical departures.",
           CAV_ONLY])

BRIENNE = battle(
    "brienne", "Brienne", "29 January 1814",
    "Napoleon took the field at the end of January to strike Blücher before he could join Schwarzenberg, and found him at "
    "Brienne, where the Emperor had been a cadet. Grouchy's cavalry drove in the Russian horse in the afternoon; Victor's "
    "and Ney's infantry then attacked Olsufiev's corps in the town as Sacken's came up from Lesmont. Russian cavalry rode "
    "down Duhesme's division on the open left, and Cossacks nearly took Napoleon himself; but after dark a party of "
    "Victor's men slipped into the château and nearly took Blücher. The Young Guard's night assault on the town failed, "
    "Decouz was mortally wounded, and the fighting went on until midnight. Blücher drew off before dawn, leaving the field "
    "to the French but free to join Schwarzenberg for La Rothière three days later.",
    [BR_FR, BR_WIKI, BR_BATTLE],
    [BR_DUHESME, BR_FORESTIER, BR_MEUNIER, BR_DECOUZ, BR_GUARD_CAV, BR_V_CAVALRY],
    [ru("Olsufiev's Corps", "IX Infantry Corps, Langeron's corps, Army of Silesia",
        "Udom's 9th and Kornilov's 15th Divisions, about six thousand infantry, which held Brienne town through the afternoon "
        "and failed to retake the château at night."),
     ru("Sacken's Corps", "Army of Silesia",
        "Lieven's XI and Shcherbatov's VI Infantry Corps, recalled from Lesmont, which reached the field from mid-afternoon "
        "and drove the Young Guard out of most of the town that night."),
     ru("Vasilchikov's Cavalry", "Sacken's corps, Army of Silesia",
        "Lanskoy's 2nd Hussar Division and Panchulidzev's dragoons, which with Pahlen's squadrons, forty in all, rode down "
        "Duhesme's division and took eight of its guns."),
     ru("Pahlen's Cavalry", "Wittgenstein's VI Corps, Army of Bohemia",
        "Pahlen's three thousand horse, ahead of Wittgenstein's corps, with Shcherbatov's Cossacks and the 4th and 34th Jäger, "
        "which gave ground before Grouchy across the plain until the Jäger's squares stopped the French dragoons.")])


# ================================================================ La Rothière, 1 February 1814

RO_FR = {"label": "French Forces, Battle of La Rothière, 1 February 1814 (Nafziger Collection 814BAD)", "url": NAF + "814BAD.pdf"}
RO_BATTLE = {"label": "Battle of La Rothière (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_La_Rothi%C3%A8re"}
RO_NOTE = "After Nafziger's order of battle for La Rothière, from Koch's and Damitz's histories of the campaign and the French archives."
RO_25 = "Battalion numbers and brigades his La Rothière return leaves out are from his return of 25 January, a week before."
AT_FLAG, WT_FLAG, BAV_FLAG = "/flags/austria.svg", "/flags/wurttemberg.svg", "/flags/bavaria.svg"
GARDES = ("The Gardes d'Honneur, raised in 1813 from young men of means who equipped themselves and rode dressed as "
          "hussars, are the list's Hussars.")

RO_DUFOUR = force(
    "la-rothiere-dufour", FR, "Dufour's Division", "1st Division, Paris Reserve (Gérard), with Piquet's cavalry", "French",
    "Gérard's division on the far right, holding Dienville and its bridge over the Aube. Gyulai's Austrians took the bridge "
    "and lost it again, and attacked the village from both banks in turn; Gérard held it until the army drew off, and "
    "gave it up only at midnight. Piquet's cavalry stood to its left, towards La Rothière.",
    [bde("fr-infantry-brigade", "Jarry's Brigade", "Gén. de Brigade Jarry",
         regiments=[bn("fr-line-infantry", "8/32nd Line"), bn("fr-line-infantry", "6/58th Line"),
                    bn("fr-light-infantry", "7/12th Léger"), bn("fr-light-infantry", "6/29th Léger")]),
     bde("fr-infantry-brigade", "Bellair's Brigade", "Gén. de Brigade de Bellair",
         regiments=[bn("fr-light-infantry", "7/2nd Léger"), bn("fr-light-infantry", "6/4th Léger"), bn("fr-line-infantry", "3/135th Line"),
                    one("fr-line-infantry", "139th Line"), one("fr-line-infantry", "155th Line")]),
     bde("fr-infantry-brigade", "Bourmont's Brigade", "Gén. de Brigade Bourmont", regiments=[bn_list("fr-line-infantry", "113th Line", ["1", "3", "4"])]),
     bde("fr-light-cavalry-brigade", "Piquet's Brigade", "Gén. de Brigade Piquet",
         units=[u("fr-hussar-regt", "10th Hussars"), u("fr-hussar-regt", "1st Gardes d'Honneur")]),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "Foot Battery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Dufour")],
    notes=[LIST_FR, RO_NOTE, RO_25,
           "Its battalions were from the depots of a dozen regiments, mostly one from each, put together in brigades that "
           "winter; each is shown as a regiment of its one battalion. The 113th, raised in Tuscany, was the one whole regiment.",
           "Piquet's brigade, the cavalry of Gérard's wing, is with the division here. " + GARDES,
           "Nafziger gives the division's artillery as three hundred gunners and train, shown as one foot battery.",
           "Jarry's four regiments and Bellair's five, where the list's brigade takes three, and four light battalions, where "
           "it allows one light regiment in the division, show as historical departures."])

RO_RICARD = force(
    "la-rothiere-ricard", FR, "Ricard's Division", "1st Division, VI Corps (Marmont), under Gérard", "French",
    "The remnant of Ricard's division of 1813, lent from Marmont's corps to Gérard, which stood with Dufour's round Dienville "
    "on the right through the Austrian attacks.",
    [bde("fr-infantry-brigade", "Fournier's Brigade", "Gén. de Brigade Fournier",
         regiments=[bn("fr-light-infantry", "3/2nd Léger"), bn_list("fr-light-infantry", "4th Léger", ["2", "3"]),
                    bn("fr-light-infantry", "2/6th Léger"), bn("fr-light-infantry", "3/9th Léger"), bn("fr-light-infantry", "2/16th Léger"),
                    bn("fr-line-infantry", "3/40th Line"), bn("fr-line-infantry", "2/50th Line")]),
     bde("fr-infantry-brigade", "Boudin's Brigade", "Gén. de Brigade Boudin de Roville",
         regiments=[bn("fr-line-infantry", "1/136th Line"), bn("fr-line-infantry", "1/138th Line"), bn("fr-line-infantry", "1/142nd Line"),
                    bn("fr-line-infantry", "1/144th Line"), bn("fr-line-infantry", "1/145th Line")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Ricard")],
    notes=[LIST_FR, RO_NOTE,
           "Its thirteen battalions were what was left of whole regiments after Leipzig, a hundred to six hundred men each; on 25 "
           "January the division counted 2,300 men. They are shown at full size; the list's Small upgrade would suit them all.",
           "Nafziger gives the battalions as one brigade under Fournier and Boudin together. They are split between them here, "
           "the light battalions and the 40th and 50th Line with Fournier and the regiments raised in 1813 with Boudin, as "
           "Wikipedia's order of battle, after Nafziger's history, has them.",
           "Fournier's seven regiments and Boudin's five, where the list's brigade takes three, and five light battalions, "
           "where it allows one light regiment in the division, show as historical departures. Nafziger gives the division no guns."])

RO_DUHESME = again(
    BR_DUHESME, "la-rothiere-duhesme",
    "The one division of Victor's corps in the centre, with a brigade in La Rothière itself and the other behind it. At four "
    "Sacken's Russians came on with the bayonet, their muskets wet with snow; after a hard fight Duhesme's men were driven "
    "out, but some held on in the houses at the north end, and Colbert's Guard cavalry threw back every attempt to come "
    "out of the village.",
    [LIST_FR, RO_NOTE,
     "Each regiment had a single battalion; each is shown as its one battalion. Its brigades and battery are as at Brienne, "
     "from his return of 25 January: Nafziger's La Rothière return gives none.",
     II_ARTY, "Its foot battery, with four battalions where the list wants six for one, shows as a historical departure."])
RO_DUHESME["missing"] = [{"name": "Giberie's detachment, 1,900 infantry",
                          "reason": "Victor's other infantry, holding La Giberie, Petit-Mesnil and the Beaulieu Wood; Nafziger couldn't identify its battalions."}]

RO_LAGRANGE = force(
    "la-rothiere-lagrange", FR, "Lagrange's Division", "3rd Division, VI Corps (Marmont)", "French",
    "Marmont's infantry on the left wing, in Morvilliers, with a battalion out east at La Chaise. Wrede's Austrians and "
    "Bavarians cleared it out of La Chaise and the Bois d'Ajou in the afternoon and took Chaumesnil on its right; Marmont "
    "held Morvilliers into the night and covered the army's retreat.",
    [bde("fr-infantry-brigade", "Joubert's Brigade", "Gén. de Brigade Joubert",
         regiments=[bn("fr-line-infantry", "3/23rd Line"), bn_list("fr-light-infantry", "37th Léger", ["1", "2", "3", "4"]), marine("1st Marine Regiment", 2)]),
     bde("fr-infantry-brigade", "Pelleport's Brigade", "Gén. de Brigade Pelleport",
         regiments=[marine("2nd Marine Regiment", 4), marine("3rd Marine Regiment", 3), marine("4th Marine Regiment", 2)]),
     bde("fr-infantry-brigade", "Lefol's Brigade",
         regiments=[bn("fr-line-infantry", "4/1st Line"), bn("fr-line-infantry", "3/15th Line"), one("fr-line-infantry", "132nd Line")]),
     bde("fr-infantry-brigade", "Clavel's Brigade", "Gén. de Brigade Clavel",
         regiments=[bn("fr-line-infantry", "4/16th Line"), one("fr-line-infantry", "62nd Line"), bn("fr-line-infantry", "2/70th Line"),
                    one("fr-line-infantry", "121st Line")]),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "6/3rd Foot Artillery")]),
     bde("fr-artillery-brigade", "VI Corps Artillery", units=[u("fr-foot-arty", "25/3rd Foot Artillery"), u("fr-foot-arty", "26/3rd Foot Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Lagrange")],
    notes=[LIST_FR, RO_NOTE, RO_25, MARINES,
           "Nafziger gives the division as one brigade under Joubert and Pelleport, with Lefol's division taken into it. Its "
           "regiments are brigaded here as Wikipedia's order of battle, after Nafziger's history, has them: Joubert's and "
           "Pelleport's of Lagrange's own division, and the two of Lefol's, the first of which has no known commander.",
           "Nafziger gives the 37th Line, but it is the 37th Léger, which served in the division at Leipzig; the 37th Line was "
           "in Duhesme's division.",
           "Its battalions were very weak: the division had 4,600 men in twenty-one battalions. They are shown at full size, "
           "and the list's Small upgrade would suit them all.",
           "Marmont's artillery is from the 25 January return: three companies of the 3rd Foot Artillery, one with the "
           "division and two in the corps artillery, as the list takes them. Clavel's four regiments, where the list's brigade "
           "takes three, show as a historical departure."])
RO_LAGRANGE["missing"] = [
    {"name": "13/ and 16/5th Foot Artillery", "reason": "The rest of Marmont's foot companies, more batteries than the list takes."},
    {"name": "2/1st Horse Artillery", "reason": "Marmont's horse company, with no cavalry in the division to allow it."}]

RO_DOUMERC = force(
    "la-rothiere-doumerc", FR, "Doumerc's Cavalry", "I Cavalry Corps, with Marmont", "French",
    "The cavalry of Marmont's wing, supporting his battalion at La Chaise and covering the open ground towards Chaumesnil, "
    "outnumbered by Wrede's horse.",
    [bde("fr-light-cavalry-brigade", "Doumerc's Division",
         units=[u("fr-hussar-regt", "1st Provisional Hussars"), u("fr-chasseur-a-cheval", "2nd Provisional Chasseurs"),
                u("fr-chasseur-a-cheval", "3rd Provisional Chasseurs"), u("fr-chasseur-a-cheval", "4th Provisional Chasseurs")]),
     bde("fr-divisional-artillery", "Corps Artillery", units=[u("fr-horse-arty", "3/1st Horse Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Doumerc")],
    notes=[LIST_FR, RO_NOTE,
           "The provisional regiments were made up from the squadrons left at the depots of many regiments; they had three to "
           "six hundred men each.",
           "Wikipedia's order of battle, after Nafziger's history, gives the 3rd and 4th Provisional as cuirassiers and dragoons; "
           "they are the chasseurs of his returns here.",
           "The horse battery's number is from Wikipedia's order of battle.", CAV_ONLY])

RO_GUARD_CAV = force(
    "la-rothiere-guard-cavalry", FIG, "Nansouty's Guard Cavalry", "Colbert's, Lefebvre-Desnouettes's and Guyot's divisions, Guard Cavalry", "French",
    "The Guard horse, between La Rothière and Petit-Mesnil in the centre. Its first charge was beaten back by Sacken's guns; "
    "its second drove off Lanskoy's hussars, but as it came on the Russian infantry it was struck by Panchulidzev's dragoons "
    "and broken, losing the Guard's horse batteries. In the evening Colbert's squadrons held the Russians in La Rothière, "
    "and Guyot's rode with Meunier's division against Chaumesnil.",
    [bde("fig-heavy-cavalry-brigade", "Guard Heavy Cavalry",
         units=[u("fig-grenadiers-a-cheval-regt", "Grenadiers à Cheval"), u("fig-empress-dragoons", "Empress Dragoons"),
                u("fig-og-horse-arty", "Guard Horse Battery")]),
     bde("fig-light-cavalry-brigade", "Guard Chasseurs", units=[u("fig-chasseurs-a-cheval", "Chasseurs à Cheval"), u("fig-og-horse-arty", "Guard Horse Battery")]),
     bde("fig-light-cavalry-brigade", "Polish Lancers", units=[u("fig-polish-lancers", "1st (Polish) Chevau-légers Lanciers")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Nansouty")],
    notes=[LIST_FIG, RO_NOTE,
           "Nafziger gives Colbert's and Lefebvre-Desnouettes's divisions with squadrons of the same regiments, and Guyot's "
           "service squadrons drawn from both; each regiment's squadrons are shown together as one unit, as at Hanau. The three "
           "divisions had about two thousand men.",
           "Nansouty, who commanded the Guard cavalry, is from Wikipedia's account; Nafziger gives the divisions on their own.",
           "Two horse batteries, one with each division, are here; the Guard lost twenty-four horse guns in the fight."])
RO_GUARD_CAV["missing"] = [{"name": "2nd Éclaireurs", "reason": "A regiment of Guard scouts raised that winter, with squadrons in both divisions, which the 1812 list doesn't have."}]

RO_V_CAVALRY = again(
    BR_V_CAVALRY, "la-rothiere-v-cavalry",
    "Grouchy's horsemen, posted between Petit-Mesnil and Chaumesnil to fill the gap between Victor's villages and "
    "Marmont's. As the Crown Prince of Württemberg's corps took La Giberie and Petit-Mesnil and Wrede's cavalry came round "
    "past the French squares, they could not hold the open ground against the allied horse.",
    [LIST_FR, RO_NOTE, RO_25,
     "Piré's 9th Light Cavalry Division is the two light brigades, Briche's 5th Heavy Division Montélégier's and Ludot's "
     "dragoons, and L'Héritier's 6th Heavy Division Lamotte's and Collaert's.",
     "Its regiments were weak, about two hundred men each; they are shown at full size, and the list's Small upgrade would "
     "suit many of them.",
     "The dragoon divisions were veterans brought from Spain that winter.",
     V_CAV_ARTY.replace("two horse batteries", "first two horse batteries"),
     "Four heavy cavalry brigades, where the list takes one, and more heavy cavalry than its half of the army for "
     "corps support, show as historical departures.",
     CAV_ONLY])
for b in RO_V_CAVALRY["brigades"]:
    if b["name"] == "Mermet's Brigade":
        b["name"], b["commander"] = "Collaert's Brigade", {"name": "Gén. de Brigade Collaert"}
RO_V_CAVALRY["missing"] = [{"name": "1/2nd Horse Artillery", "reason": "The corps' third horse battery, more than the list takes."}]

RO_ROTHEMBOURG = force(
    "la-rothiere-rothembourg", FIG, "Rothembourg's Division", "5th Young Guard (2nd Tirailleur) Division (Ney)", "French",
    "Ney's nearest Young Guard division, called up from Brienne-la-Vieille. As the army made ready to withdraw, Napoleon sent "
    "it to retake La Rothière: its first brigade took the village and was thrown out by Olsufiev's Russians, and its second "
    "took it again before Grimmer's Austrians and Paskevich's grenadiers drove it out. It re-formed north of the village "
    "at eight, and covered the retreat in the snowstorm.",
    [bde("fig-young-guard-brigade", "Rothembourg's First Brigade",
         units=[u("fig-yg-foot-arty", "Young Guard Foot Battery")],
         regiments=[yg("1st Tirailleurs"), yg("5th Tirailleurs"), yg("6th Tirailleurs")]),
     bde("fig-young-guard-brigade", "Rothembourg's Second Brigade",
         units=[u("fig-yg-foot-arty", "Young Guard Foot Battery")],
         regiments=[yg("7th Tirailleurs"), yg("8th Tirailleurs"), yg("Flanqueurs-Chasseurs")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Rothembourg")],
    notes=[LIST_FIG, RO_NOTE, NEW_YG,
           "Each regiment had two battalions of about four hundred men; they are shown at full size.",
           "Nafziger gives the division without its brigades; its six regiments are split between two here, in his order. The "
           "Flanqueurs-Chasseurs, the Young Guard's light infantry, are the list's Tirailleurs.",
           "Its two foot companies are one battery with each brigade."])

RO_MEUNIER = again(
    BR_MEUNIER, "la-rothiere-meunier",
    "Ney's first Young Guard division, called back from towards Lesmont. When Wrede took Chaumesnil in the late afternoon, "
    "Napoleon sent it with Guyot's Guard cavalry to retake the village; it attacked again and again without getting it back, "
    "and at seven Wrede's cavalry got past its squares and took the guns behind them.",
    [LIST_FIG, RO_NOTE, RO_25, NEW_YG] + BR_MEUNIER["notes"][3:])

RO_DECOUZ = again(
    BR_DECOUZ, "la-rothiere-decouz",
    "Ney's second Young Guard division, much weakened at Brienne, which was called back from towards Lesmont with Meunier's "
    "and stood in reserve.",
    [LIST_FIG, RO_NOTE, RO_25, NEW_YG,
     "Nafziger still names Decouz, mortally wounded at Brienne three days before; Pelet had taken the division over.",
     "The division had 1,800 men in eight battalions after Brienne; they are shown at full size, and the list's Small upgrade "
     "would suit them all."] + BR_DECOUZ["notes"][4:])

RO_DEFRANCE = force(
    "la-rothiere-defrance", FR, "Defrance's Gardes d'Honneur", "Cavalry Division, Guard Reserve (Ney)", "French",
    "Two regiments of the Gardes d'Honneur, attached to the Guard, which Nafziger gives with Ney's reserve behind the centre.",
    [bde("fr-light-cavalry-brigade", "Ségur's Brigade", "Gén. de Brigade Ségur",
         units=[u("fr-hussar-regt", "3rd Gardes d'Honneur"), u("fr-hussar-regt", "4th Gardes d'Honneur")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Defrance")],
    notes=[LIST_FR, RO_NOTE, RO_25,
           GARDES + " The Guard list has no Gardes d'Honneur but the Italian, so they are built from the French one.",
           "Each regiment had nine squadrons and about a thousand men on 25 January; each is shown as one unit.", CAV_ONLY])

LA_ROTHIERE = battle(
    "la-rothiere", "La Rothière", "1 February 1814",
    "Three days after Brienne, Blücher, joined by much of Schwarzenberg's army, came on at noon against Napoleon's army "
    "strung out over seven miles of villages from Dienville to Morvilliers, the gaps between them held by cavalry, in "
    "falling snow that made the roads mud and the guns almost useless. Sacken's Russians attacked La Rothière in the centre "
    "and took it with the bayonet, as Nansouty's Guard cavalry was broken in front of it; Gérard held Dienville against "
    "Gyulai's Austrians, but the Crown Prince of Württemberg took La Giberie and Petit-Mesnil and Wrede took Chaumesnil. "
    "Rothembourg's Young Guard retook La Rothière twice in the evening before being driven out, and under cover of the "
    "storm the French drew off towards Lesmont, leaving some fifty guns: Napoleon's first defeat on French soil.",
    [RO_FR, BR_FR, BR_WIKI, RO_BATTLE],
    [RO_DUFOUR, RO_RICARD, RO_DUHESME, RO_GUARD_CAV, RO_V_CAVALRY, RO_LAGRANGE, RO_DOUMERC, RO_ROTHEMBOURG, RO_MEUNIER,
     RO_DECOUZ, RO_DEFRANCE],
    [ru("Lieven's Corps", "XI Infantry Corps, Sacken's corps, Army of Silesia",
        "Eight thousand infantry of the 10th and 27th Divisions, Sacken's left column, which stormed La Rothière at four with the bayonet."),
     ru("Shcherbatov's Corps", "VI Infantry Corps, Sacken's corps, Army of Silesia",
        "Eight thousand infantry of the 7th and 18th Divisions, Sacken's right column, beside Lieven's in the attack on La Rothière."),
     ru("Olsufiev's Corps", "IX Infantry Corps, Army of Silesia",
        "Five thousand infantry following Sacken's columns, which threw Rothembourg's first brigade out of La Rothière in the evening."),
     ru("Vasilchikov's Cavalry", "Sacken's corps, Army of Silesia",
        "Lanskoy's hussars, Panchulidzev's dragoons and Karpov's Cossacks; the dragoons broke Nansouty's Guard cavalry and took its horse guns."),
     ru("Paskevich's Grenadiers", "2nd Grenadier Division, Russian Reserve",
        "The one division of Barclay's reserve to reach the fight, which helped drive the Young Guard out of La Rothière at the last."),
     ru("Gyulai's Corps", "III Corps, Army of Bohemia",
        "Gyulai's Austrians, who attacked Dienville and its bridge from both banks of the Aube without taking it, and sent Grimmer's "
        "brigade to help at La Rothière.", side="Austrian", flag=AT_FLAG),
     ru("The Crown Prince of Württemberg's Corps", "IV Corps, Army of Bohemia",
        "The Württembergers, who took the Beaulieu Wood, La Giberie and Petit-Mesnil from Victor's infantry.", side="Württemberg", flag=WT_FLAG),
     ru("Wrede's Corps", "V Corps, Army of Bohemia",
        "Wrede's Bavarians and Austrians on the allied right, who drove Marmont from La Chaise and the Bois d'Ajou, held "
        "Chaumesnil against Meunier, and took twenty-one guns in a charge at dusk.", side="Bavarian", flag=BAV_FLAG)],
    alliances=(("Russian", "Austrian", "Württemberg", "Bavarian"),))


# The planned battles' names, dates and summaries, now written with their armies still to come
PLANNED = {
    'champaubert': ('Champaubert', '10 February 1814',
        "The first of the Six Days: marching north through the mud, Napoleon fell on Olsufiev's isolated Russian corps strung out along Blücher's line of march, and destroyed it; Olsufiev was taken."),
    'montmirail': ('Montmirail', '11 February 1814',
        "Napoleon turned west on Sacken's Russians and the leading brigades of Yorck's Prussians, coming back towards Montmirail; Ney and the Guard stormed the farm of Marchais, and the allies were driven north towards the Marne."),
    'chateau-thierry': ('Château-Thierry', '12 February 1814',
        "Pursuing Sacken and Yorck to the Marne, the Guard cavalry and Ney's infantry caught their rearguards before Château-Thierry and drove them over the river, but the bridge was burnt behind them."),
    'vauchamps': ('Vauchamps', '14 February 1814',
        "Blücher, coming on with Kleist's and Kapzevich's corps against Marmont, met Napoleon instead; Grouchy's cavalry rode round the retreating allied squares, which fought their way back through the French horsemen to Étoges with heavy loss."),
    'mormant': ('Mormant', '17 February 1814',
        "Turning back south after the Six Days, Napoleon's cavalry and Gérard's infantry caught Pahlen's Russian advance guard in the open at Mormant and cut it to pieces."),
    'montereau': ('Montereau', '18 February 1814',
        "Turning south on Schwarzenberg's army, Napoleon attacked the Crown Prince of Württemberg's corps holding the heights before Montereau; Pajol's cavalry charged down the road and over the bridges before they could be blown, and Napoleon himself laid guns, saying the ball that would kill him had not been cast."),
    'bar-sur-aube': ('Bar-sur-Aube', '27 February 1814',
        "Schwarzenberg turned on Oudinot's and Macdonald's rearguard at Bar-sur-Aube and drove it back over the Aube; Wittgenstein was wounded leading the attack."),
    'laubressel': ('Laubressel', '3 March 1814',
        'The allied army of Bohemia followed up its success at Bar-sur-Aube and beat Macdonald and Oudinot again at Laubressel, east of Troyes.'),
    'craonne': ('Craonne', '7 March 1814',
        "Napoleon attacked Vorontsov's and Sacken's Russians on the narrow Chemin des Dames plateau; Ney and Victor's Young Guard came on in costly frontal assaults until the Russians withdrew in good order, one of the bloodiest days of the campaign."),
    'laon': ('Laon', '9–10 March 1814',
        "Blücher, with twice Napoleon's numbers, held the hill of Laon against him; on the night of the 9th Yorck and Kleist fell on Marmont's corps at Athies and routed it, and Napoleon, attacking again next day to no purpose, withdrew."),
    'reims': ('Reims', '13 March 1814',
        "Napoleon fell on Saint-Priest's Russian and Prussian corps, which had taken Reims; Saint-Priest, an émigré Frenchman in Russian service, was mortally wounded, and the city was retaken."),
    'limonest': ('Limonest', '20 March 1814',
        "Augereau's army, which had held the Rhône valley against the Austrians since January, was beaten before Lyon at Limonest by the Prince of Hesse-Homburg, and Lyon fell next day."),
    'arcis-sur-aube': ('Arcis-sur-Aube', '20–21 March 1814',
        "Expecting a rearguard, Napoleon found Schwarzenberg's whole army before Arcis; the Guard held on through two days, Napoleon riding over a smoking shell, before the French crossed back over the Aube and he turned east against the allies' communications."),
    'fere-champenoise': ('Fère-Champenoise', '25 March 1814',
        "The allied cavalry, marching on Paris, rode down Marmont's and Mortier's corps on the plain, and then Pacthod's and Amey's National Guard divisions, which formed squares and fought on until the Tsar himself rode in to accept their surrender."),
    'saint-dizier': ('Saint-Dizier', '26 March 1814',
        "Napoleon, striking at the allies' communications, turned on Winzingerode's cavalry screen at Saint-Dizier and routed it, then learned it had been sent to deceive him while the allied armies marched on Paris: his last victory."),
    'paris': ('Paris', '30 March 1814',
        'The allied armies attacked the heights of Belleville, Romainville and Montmartre, held by Marmont and Mortier with conscripts, National Guards and the pupils of the École Polytechnique; that night Marmont signed the capitulation, and the allies entered the city next day.'),
}


# ================================================================ The rest of the campaign: the armies, still to come
#
# Each side's corps and divisions as Wikipedia's pages on the battles give them, ahead of their forces. Summaries are
# our own words.

FR_FLAG, PR_FLAG = "/flags/france.svg", "/flags/prussia.png"


def wiki(title, path):
    return {"label": f"{title} (Wikipedia)", "url": "https://en.wikipedia.org/wiki/" + path}


def fr(name, formation, summary):
    return ru(name, formation, summary, side="French", flag=FR_FLAG)


def pr(name, formation, summary):
    return ru(name, formation, summary, side="Prussian", flag=PR_FLAG)


def at(name, formation, summary):
    return ru(name, formation, summary, side="Austrian", flag=AT_FLAG)


def wt(name, formation, summary):
    return ru(name, formation, summary, side="Württemberg", flag=WT_FLAG)


def bav(name, formation, summary):
    return ru(name, formation, summary, side="Bavarian", flag=BAV_FLAG)


def armies(id_, sources, to_come, alliances=()):
    name, date, summary = PLANNED[id_]
    return battle(id_, name, date, summary, sources, [], to_come, alliances)


SIX_DAYS = wiki("Six Days' Campaign order of battle", "Six_Days%27_Campaign_order_of_battle")

# ---------------------------------------------------------------- Champaubert, 10 February 1814, written

CH_FR = {"label": "French and Russian Forces, Battle of Champaubert, 9 February 1814 (Nafziger Collection 814BAB)", "url": NAF + "814BAB.pdf"}
CH_NOTE = ("After Nafziger's order of battle for Champaubert, from Bogdanovich's history of the campaign and the French "
           "archives; its strengths are of 1 February.")
CH_DEPOTS = ("Each brigade was made up of squadrons from the depots of many regiments: Nafziger names their parent regiments "
             "but not their strengths. They are grouped here as one unit for each kind of horse in a brigade, or two where a "
             "brigade had many, as they were formed into provisional regiments.")


def fought(id_, sources, forces, to_come, alliances=()):
    """A battle from the planned list, now with forces written"""
    name, date, summary = PLANNED[id_]
    return battle(id_, name, date, summary, sources, forces, to_come, alliances)


def brigade_of(f, name):
    return next(b for b in f["brigades"] if b["name"] == name)


CH_LAGRANGE = again(
    RO_LAGRANGE, "champaubert-lagrange",
    "Marmont's leading division, which crossed the Petit Morin at Saint-Prix behind Ricard's. Its first attacks on the "
    "Russian right stalled until the Guard's guns came up; then Pelleport's brigade took Bannay.",
    [LIST_FR, CH_NOTE, MARINES,
     "Nafziger gives the division as one brigade; its regiments are brigaded here as at La Rothière, after Nafziger's "
     "history as Wikipedia's order of battle has it. Battalion numbers he leaves out, and the division's artillery, are from "
     "his returns of 25 January and La Rothière.",
     "Nafziger gives the 37th Line, but it is the 37th Léger, which served in the division at Leipzig; the 37th Line was "
     "in Duhesme's division of Victor's corps.",
     "The division had 4,868 men in twenty-one battalions; they are shown at full size, and the list's Small upgrade would "
     "suit them all.",
     "Marmont's artillery: three companies of the 3rd Foot Artillery, one with the division and two in the corps artillery, "
     "as the list takes them. Clavel's four regiments, where the list's brigade takes three, show as a historical departure."])
brigade_of(CH_LAGRANGE, "Joubert's Brigade")["regiments"][1] = bn_list("fr-light-infantry", "37th Léger", ["1", "3"])
brigade_of(CH_LAGRANGE, "Pelleport's Brigade")["regiments"][2] = marine("4th Marine Regiment", 3)
brigade_of(CH_LAGRANGE, "Lefol's Brigade")["regiments"].pop()   # no 132nd Line here
CH_LAGRANGE["missing"] = RO_LAGRANGE["missing"]

CH_RICARD = force(
    "champaubert-ricard", FR, "Ricard's Division", "8th Division, VI Corps (Marmont)", "French",
    "Marmont's other division, which led the way over the Petit Morin, took Baye and then fought its way into "
    "Champaubert itself, with a squadron of lancers under Piquet beside it.",
    [bde("fr-infantry-brigade", "Fournier's Brigade", "Gén. de Brigade Fournier",
         regiments=[bn("fr-light-infantry", "2/2nd Léger"), bn("fr-light-infantry", "7/4th Léger"), bn("fr-light-infantry", "2/6th Léger"),
                    one("fr-light-infantry", "9th Léger"), one("fr-light-infantry", "16th Léger"), one("fr-line-infantry", "22nd Line"),
                    bn("fr-line-infantry", "2/40th Line"), bn("fr-line-infantry", "1/50th Line"), one("fr-line-infantry", "69th Line")]),
     bde("fr-infantry-brigade", "Boudin's Brigade", "Gén. de Brigade Boudin de Roville",
         regiments=[bn("fr-line-infantry", "1/136th Line"), bn("fr-line-infantry", "1/138th Line"), bn("fr-line-infantry", "1/142nd Line"),
                    bn("fr-line-infantry", "1/144th Line"), bn("fr-line-infantry", "1/145th Line")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Ricard")],
    notes=[LIST_FR, CH_NOTE,
           "Its fourteen battalions were what was left of whole regiments after Leipzig, 2,917 men in all, a couple of hundred "
           "each. They are shown at full size; the list's Small upgrade would suit them all.",
           "Nafziger gives the division without its brigades. Its battalions are split between Fournier and Boudin as at La "
           "Rothière: the light battalions and the older line regiments with Fournier, the regiments raised in 1813 with Boudin.",
           "Fournier's nine regiments and Boudin's five, where the list's brigade takes three, and five light battalions, where "
           "it allows one light regiment in the division, show as historical departures. Nafziger gives the division no guns."])

CH_BORDESOULLE = force(
    "champaubert-bordesoulle", FR, "Bordesoulle's Cavalry", "I Cavalry Corps", "French",
    "The cavalry of Marmont's column. Bordesoulle's cuirassiers rode round the Russian right and split Olsufiev's corps "
    "in two, while horse went round its left to close the high road at Fromentières, so that few of the Russians got away.",
    [bde("fr-light-cavalry-brigade", "Wathier's Brigade", "Gén. de Brigade Wathier",
         units=[u("fr-hussar-regt", "Hussar detachments (6th, 7th and 8th Hussars)"),
                u("fr-lancer", "Chevau-léger detachments (1st, 3rd, 5th, 7th and 8th Chevau-légers)")]),
     bde("fr-light-cavalry-brigade", "Guyon's Brigade", "Gén. de Brigade Guyon",
         units=[u("fr-chasseur-a-cheval", "Chasseur detachments (1st, 2nd, 3rd and 6th Chasseurs)"),
                u("fr-chasseur-a-cheval", "Chasseur detachments (8th, 9th, 16th and 25th Chasseurs)")]),
     bde("fr-heavy-cavalry-brigade", "Thiry's Brigade", "Gén. de Brigade Thiry",
         units=[u("fr-cuirassier", "Cuirassier detachments (2nd, 3rd and 6th Cuirassiers)"),
                u("fr-cuirassier", "Cuirassier detachments (9th, 11th and 12th Cuirassiers)")]),
     bde("fr-heavy-cavalry-brigade", "Laville's Brigade", "Gén. de Brigade Laville",
         units=[u("fr-cuirassier", "Cuirassier detachments (4th, 7th and 14th Cuirassiers)"),
                u("fr-dragoon", "Dragoon detachments (7th, 23rd, 28th and 30th Dragoons)")]),
     bde("fr-divisional-artillery", "Corps Artillery", units=[u("fr-horse-arty", "3/1st Horse Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Bordesoulle")],
    notes=[LIST_FR, CH_NOTE,
           "Merlin's 1st Light Cavalry Division is Wathier's and Guyon's brigades; Bordesoulle's own 2nd Heavy Cavalry Division, "
           "about twelve hundred men, Thiry's and Laville's.",
           CH_DEPOTS,
           "Nafziger names Bordesoulle as the corps' commander; Wikipedia's account has Doumerc leading the horse that went round "
           "the Russian left.",
           "Two heavy cavalry brigades, where the list takes one, and cuirassiers and dragoons in one brigade show as "
           "historical departures.",
           CAV_ONLY])
CH_BORDESOULLE["missing"] = [{"name": "1/6th Horse Artillery", "reason": "The corps' second horse battery, detached on the day."}]

CH_MEUNIER = again(
    RO_MEUNIER, "champaubert-meunier",
    "Ney's first Young Guard division, which came up behind Marmont's while the fight went on; its guns joined the "
    "bombardment of Bannay.",
    [LIST_FIG, CH_NOTE, NEW_YG,
     "The division had 4,133 men in eight battalions; they are shown at full size.",
     "Battalion numbers, brigades and guns, which this return leaves out, are as at La Rothière.",
     "Its foot battery, with four battalions in its brigade, where the list wants six for one, shows as a historical departure."])

CH_DECOUZ = again(
    RO_DECOUZ, "champaubert-decouz",
    "Ney's second Young Guard division, which came up with Meunier's behind Marmont's.",
    [LIST_FIG, CH_NOTE, NEW_YG,
     "Nafziger still names Decouz, mortally wounded at Brienne; Wikipedia's order of battle has Pelet leading the division "
     "on the 10th and 11th, and Curial taking it over.",
     "The division had 2,840 men in eight battalions; they are shown at full size, and the list's Small upgrade would suit them.",
     "Battalion numbers, brigades and guns, which this return leaves out, are as at La Rothière.",
     "Its foot battery, with four battalions in its brigade, where the list wants six for one, shows as a historical departure."])

CH_OLSUFIEV = force(
    "champaubert-olsufiev", RU, "Olsufiev's Corps", "IX Infantry Corps, Langeron's corps, Army of Silesia", "Russian",
    "About four thousand men and twenty-four guns, strung out along Blücher's line of march and left without cavalry, "
    "which Napoleon fell on out of the marshes of Saint-Gond. Udom's division held Baye and Bannay until Marmont's men "
    "took them; the corps was then cut off by the French cavalry, and most of it was killed or taken, Olsufiev and "
    "Poltoratsky among them. Kornilov brought some fifteen hundred away through the woods.",
    [bde("ru-infantry-brigade", "Poltoratsky's Brigade", "Maj-Gen Poltoratsky", units=[u("ru-light-arty", "Light Battery #13")],
         regiments=[ru_regt("Apsheron Infantry", 1), ru_regt("Nasheburg Infantry", 1)]),
     bde("ru-infantry-brigade", "Yushkov's Brigade", "Maj-Gen Yushkov II",
         regiments=[ru_regt("Ryazhsk Infantry", 1), ru_regt("Yakutsk Infantry", 1)]),
     bde("ru-jager-brigade", "Melnik's Brigade", "Maj Melnik", regiments=[ru_regt("10th Jäger", 1, "ru-jager"), ru_regt("38th Jäger", 1, "ru-jager")]),
     bde("ru-infantry-brigade", "Anensur's Brigade", "Lt-Col Anensur", units=[u("ru-light-arty", "Light Battery #29")],
         regiments=[ru_regt("Vitebsk Infantry", 1), ru_regt("Kozlov Infantry", 1)]),
     bde("ru-infantry-brigade", "Musin-Pushkin's Brigade", "Maj-Gen Musin-Pushkin",
         regiments=[ru_regt("Kolyvan Infantry", 1), ru_regt("Kura Infantry", 1)]),
     bde("ru-jager-brigade", "Tikhanovsky's Brigade", "Col Tikhanovsky", regiments=[ru_regt("12th Jäger", 1, "ru-jager"), ru_regt("22nd Jäger", 1, "ru-jager")])],
    command=[cmd("ru-div-cmd", "Gen-Lt Olsufiev")],
    notes=[LIST_RU, CH_NOTE,
           "Udom's 9th Division (the first three brigades) and Kornilov's 15th (the last three). Each regiment had a single "
           "battalion of three to six hundred men; each is shown as its one battalion.",
           "Nafziger gives two light batteries and a position battery he thinks probably wasn't there; the light batteries are "
           "with the brigades, as the list takes them.",
           "Four infantry brigades and two Jäger brigades, where the list allows three and one, show as historical departures."])
CH_OLSUFIEV["missing"] = [{"name": "Position Battery #15", "reason": "Nafziger thinks it probably wasn't present."}]

CHAMPAUBERT = fought("champaubert", [CH_FR, SIX_DAYS, wiki("Battle of Champaubert", "Battle_of_Champaubert")],
    [CH_LAGRANGE, CH_RICARD, CH_BORDESOULLE, CH_MEUNIER, CH_DECOUZ, CH_OLSUFIEV], [])

# ---------------------------------------------------------------- Montmirail, 11 February 1814, written

MM_FR = {"label": "Allied and French Forces, Battle of Montmirail, 11 February 1814 (Nafziger Collection 814BAA)", "url": NAF + "814BAA.pdf"}
MM_NOTE = ("After Nafziger's order of battle for Montmirail, from Damitz's, Plotho's and Sporschil's histories and the "
           "French archives; its strengths are of 1 February.")
GUARD_ARTY = ("Nafziger gives the Guard artillery together, seven foot and four horse batteries, not by division; the "
              "batteries here are those the list's brigades take.")


def og(reg, unit):
    """A Guard regiment of two battalions, as "1/1st Chasseurs à Pied" and "2/1st Chasseurs à Pied" """
    return regt(reg, [u(unit, f"{i}/{reg}") for i in (1, 2)])


MM_RICARD = force(
    "montmirail-ricard", FR, "Ricard's Division", "8th Division, VI Corps (Marmont)", "French",
    "The one division of Marmont's corps with Napoleon, which fought for the farm of Marchais through the day against "
    "Sacken's Russians, taking it and losing it again, with two battalions holding the Bois de Bailly.",
    [bde("fr-infantry-brigade", "Fournier's Brigade", "Gén. de Brigade Fournier",
         regiments=[bn("fr-light-infantry", "2/2nd Léger"), bn("fr-light-infantry", "7/4th Léger"), bn("fr-light-infantry", "2/6th Léger"),
                    one("fr-light-infantry", "9th Léger"), one("fr-light-infantry", "16th Léger"), one("fr-line-infantry", "22nd Line"),
                    bn("fr-line-infantry", "2/40th Line"), bn("fr-line-infantry", "2/50th Line"), bn("fr-line-infantry", "3/65th Line")]),
     bde("fr-infantry-brigade", "Boudin's Brigade", "Gén. de Brigade Boudin de Roville",
         regiments=[bn("fr-line-infantry", "1/136th Line"), bn("fr-line-infantry", "1/138th Line"), bn("fr-line-infantry", "1/142nd Line"),
                    bn("fr-line-infantry", "1/144th Line"), bn("fr-line-infantry", "1/145th Line")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Ricard")],
    notes=[LIST_FR, MM_NOTE, CH_RICARD["notes"][2], CH_RICARD["notes"][3], CH_RICARD["notes"][4]])

MM_MEUNIER = again(
    CH_MEUNIER, "montmirail-meunier",
    "Ney's first Young Guard division, which joined Ricard's in the fight for Marchais.",
    [LIST_FIG, MM_NOTE] + CH_MEUNIER["notes"][2:])

MM_CURIAL = again(
    CH_DECOUZ, "montmirail-curial",
    "Ney's second Young Guard division, now Curial's, which stood behind Ricard's division through the fight for Marchais.",
    [LIST_FIG, MM_NOTE, NEW_YG,
     "Nafziger now names Curial as the division's commander; Wikipedia's order of battle has Pelet leading it on the 10th and 11th."]
    + CH_DECOUZ["notes"][4:])
MM_CURIAL["name"] = "Curial's Division"
MM_CURIAL["command"] = [cmd("fig-div-cmd", "Gén. de Division Curial")]

MM_FRIANT = force(
    "montmirail-friant", FIG, "Friant's Old Guard", "1st Old Guard Division, Old Guard (Mortier)", "French",
    "The Old Guard's grenadiers and chasseurs, held in reserve behind Marchais until the afternoon, when Friant's "
    "battalions went forward against the farm of Haute-Épine and broke the Russian centre. Two battalions of the Chasseurs "
    "à Pied under Marshal Lefebvre took L'Épine-aux-Bois.",
    [bde("fig-old-guard-brigade", "Chasseurs à Pied",
         units=[u("fig-og-foot-arty", "Old Guard Foot Battery")],
         regiments=[og("1st Chasseurs à Pied", "fig-old-guard-chasseurs"), og("2nd Chasseurs à Pied", "fig-middle-guard-chasseurs")]),
     bde("fig-old-guard-brigade", "Cambronne's Brigade", "Gén. de Division Cambronne",
         units=[u("fig-og-foot-arty", "Old Guard Foot Battery")],
         regiments=[og("1st Grenadiers à Pied", "fig-old-guard-grenadiers"), og("2nd Grenadiers à Pied", "fig-middle-guard-grenadiers")]),
     bde("fig-marines-brigade", "Attached", units=[u("fig-marines", "3/Marines of the Guard")]),
     bde("fig-artillery-reserve", "Guard Artillery", units=[u("fig-og-heavy-foot-arty", "Old Guard 12-pdr Foot Battery")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Friant")],
    notes=[LIST_FIG, MM_NOTE,
           "The division had 4,796 men in eight battalions. The 1st Chasseurs and Grenadiers à Pied are the list's Old Guard, and "
           "the 2nd, raised in 1811, its Middle Guard.",
           "Nafziger gives Michel as the commander of the chasseurs' brigade as well as of the 2nd Old Guard Division; the brigade "
           "is shown here without him.",
           GUARD_ARTY])
MM_FRIANT["missing"] = [
    {"name": "Guard Sappers (three companies) and engineer train", "reason": "Too small for a unit of their own; the list's one engineer or marine battalion is the marines."},
    {"name": "The rest of the Guard artillery", "reason": "Four more foot and four horse batteries, more than the Guard's brigades here take."}]

MM_MICHEL = force(
    "montmirail-michel", FIG, "Michel's Division", "2nd Old Guard Division, Old Guard (Mortier)", "French",
    "The Guard's second division, the flanqueurs, fusiliers and vélites, which came up in the afternoon and counter-"
    "attacked beside Friant's; Michel was wounded leading it.",
    [bde("fig-young-guard-brigade", "Chasseur Brigade",
         regiments=[og("Flanqueurs-Chasseurs", "fig-yg-tirailleurs"), og("Fusilier-Chasseurs", "fig-fusilier-chasseurs")]),
     bde("fig-young-guard-brigade", "Grenadier Brigade",
         regiments=[og("Flanqueurs-Grenadiers", "fig-yg-tirailleurs"), og("Fusilier-Grenadiers", "fig-fusilier-grenadiers")]),
     bde("fig-italian-brigade", "Vélites", units=[u("fig-velites-florence", "Vélites of Florence"), u("fig-velites-turin", "Vélites of Turin")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Michel")],
    notes=[LIST_FIG, MM_NOTE,
           "The division had 3,878 men. Nafziger gives it without brigades: the chasseur and grenadier regiments are brigaded "
           "here as the list takes them, flanqueurs with fusiliers, and the vélites as its Italian brigade.",
           "The Flanqueurs-Chasseurs and Flanqueurs-Grenadiers, the Young Guard's light infantry, are the list's Tirailleurs.",
           GUARD_ARTY])

MM_COLBERT = force(
    "montmirail-colbert", FIG, "Colbert's Guard Cavalry", "1st Guard Cavalry Division (Nansouty)", "French",
    "One of Nansouty's three Guard cavalry divisions, which charged down the high road at the Russian centre as Friant's "
    "infantry broke it; the Polish lancers pushed on to Viels-Maisons.",
    [bde("fig-heavy-cavalry-brigade", "Guard Heavy Cavalry",
         units=[u("fig-grenadiers-a-cheval-regt", "Grenadiers à Cheval"), u("fig-empress-dragoons", "Empress Dragoons"),
                u("fig-og-horse-arty", "Guard Horse Battery")]),
     bde("fig-light-cavalry-brigade", "Guard Chasseurs", units=[u("fig-chasseurs-a-cheval", "Chasseurs à Cheval")]),
     bde("fig-light-cavalry-brigade", "Polish Lancers", units=[u("fig-polish-lancers", "1st (Polish) Chevau-légers Lanciers")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Colbert")],
    notes=[LIST_FIG, MM_NOTE,
           "The division had 2,582 men. Each Guard cavalry regiment had squadrons in each of the three divisions; each division's "
           "are shown as one unit of each regiment.",
           "Nafziger gives the division without brigades; its regiments are brigaded here as the list takes them."])
MM_COLBERT["missing"] = [
    {"name": "2nd Éclaireurs", "reason": "A regiment of Guard scouts raised that winter, which the 1812 list doesn't have."},
    {"name": "Guyot's escort squadrons", "reason": "One squadron each of the Polish lancers, chasseurs, grenadiers and dragoons, riding with Napoleon; they turned the Russian left."}]

MM_LEFEBVRE = force(
    "montmirail-lefebvre-desnouettes", FIG, "Lefebvre-Desnouettes's Guard Cavalry", "2nd Guard Cavalry Division (Nansouty)", "French",
    "The largest of the Guard's cavalry divisions, with Nansouty's other two in the charges against the Russian centre and left.",
    [bde("fig-heavy-cavalry-brigade", "Guard Heavy Cavalry",
         units=[u("fig-grenadiers-a-cheval-regt", "Grenadiers à Cheval (6 squadrons)"), u("fig-empress-dragoons", "Dragoons of the Guard (6 squadrons)")]),
     bde("fig-light-cavalry-brigade", "Old Guard Chasseurs",
         units=[u("fig-chasseurs-a-cheval", "Chasseurs à Cheval (6 squadrons)"), u("fig-gendarmes-elite", "Gendarmes d'Élite (2 squadrons)")]),
     bde("fig-light-cavalry-brigade", "Guard Lancers", units=[u("fig-polish-lancers", "1st Chevau-légers Lanciers (7 squadrons)")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Lefebvre-Desnouettes")],
    notes=[LIST_FIG, MM_NOTE,
           "Its strengths are of 28 January: some 3,300 men, the grenadiers about nine hundred and the other regiments six to "
           "seven hundred each.",
           "Nafziger gives the division without brigades; its regiments are brigaded here as the list takes them, the Gendarmes "
           "d'Élite as the small unit the chasseurs' brigade may have with it."])

MM_LAFERRIERE = force(
    "montmirail-laferriere", FIG, "Laferrière's Guard Cavalry", "3rd Guard Cavalry Division (Nansouty)", "French",
    "The Guard's third cavalry division, which charged down the high road with Colbert's at the Russian centre.",
    [bde("fig-heavy-cavalry-brigade", "Letort's Brigade", "Gén. de Brigade Letort",
         units=[u("fig-grenadiers-a-cheval-regt", "Grenadiers à Cheval"), u("fig-empress-dragoons", "Empress Dragoons")]),
     bde("fig-light-cavalry-brigade", "Lion's Brigade", "Gén. de Brigade Lion", units=[u("fig-chasseurs-a-cheval", "Chasseurs à Cheval")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Laferrière")],
    notes=[LIST_FIG, MM_NOTE,
           "Lion's brigade was the chasseurs, about five hundred, and the Empress Dragoons, about seven hundred; Letort's the "
           "grenadiers, about eight hundred and fifty. The dragoons are with Letort's grenadiers here, as the list's heavy "
           "brigade takes them."])

MM_DEFRANCE = force(
    "montmirail-defrance", FR, "Defrance's Gardes d'Honneur", "Cavalry Division, attached to the Guard", "French",
    "The Gardes d'Honneur, who charged west of the ravine and cut up the Russian brigades caught there; seven of their "
    "squadrons supported Friant's right.",
    [bde("fr-light-cavalry-brigade", "Piquet's Brigade", "Gén. de Brigade Piquet",
         units=[u("fr-hussar-regt", "10th Hussars"), u("fr-hussar-regt", "1st Gardes d'Honneur")]),
     bde("fr-light-cavalry-brigade", "Ségur's Brigade", "Gén. de Brigade Ségur",
         units=[u("fr-hussar-regt", "2nd Gardes d'Honneur"), u("fr-hussar-regt", "3rd Gardes d'Honneur"), u("fr-hussar-regt", "4th Gardes d'Honneur")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Defrance")],
    notes=[LIST_FR, MM_NOTE, GARDES,
           "The division had only 896 men in five regiments; they are shown at full size, and the list's Small upgrade would suit them.",
           "Nafziger gives the division without brigades. Piquet's brigade of the 10th Hussars and the 1st Gardes d'Honneur, and "
           "Ségur's of the 3rd and 4th, are as at La Rothière; the 2nd Gardes d'Honneur are with Ségur's here, three hussar "
           "regiments where the list's brigade takes two, a historical departure.", CAV_ONLY])

MM_RU_BN = ("Its regiments had one or two field battalions each, a few hundred men; each is shown at full size, and the "
            "list's Small upgrade would suit them.")

MM_LIEVEN = force(
    "montmirail-lieven", RU, "Lieven's Corps", "XI Infantry Corps, Sacken's corps, Army of Silesia", "Russian",
    "Sacken's right, north of the high road, marching back east to rejoin Blücher when it found Napoleon across its path. "
    "It joined the fight for Marchais and was driven north with the rest of the corps when Friant's Old Guard broke the centre.",
    [bde("ru-infantry-brigade", "Sokolovsky's Brigade", "Maj-Gen Sokolovsky", units=[u("ru-position-arty", "Position Battery #18")],
         regiments=[ru_regt("Yaroslavl Infantry", 1), ru_regt("Kursk Infantry", 1), ru_regt("Belozersk Infantry", 2)]),
     bde("ru-jager-brigade", "Achlestyshev's Brigade", "Col Achlestyshev", regiments=[ru_regt("8th Jäger", 1, "ru-jager"), ru_regt("39th Jäger", 1, "ru-jager")]),
     bde("ru-infantry-brigade", "Selivanov's Brigade", "Lt-Col Selivanov",
         regiments=[ru_regt("Kamchatka Infantry", 1), ru_regt("Okhotsk Infantry", 1)]),
     bde("ru-infantry-brigade", "Levandovsky's Brigade", "Col Levandovsky", units=[u("ru-light-arty", "Light Battery #34")],
         regiments=[ru_regt("Odessa Infantry", 1), ru_regt("Vilna Infantry", 1)]),
     bde("ru-infantry-brigade", "Alexeyev's Brigade", "Col Alexeyev", units=[u("ru-light-arty", "Light Battery #35")],
         regiments=[ru_regt("Simbirsk Infantry", 1), ru_regt("Tarnopol Infantry", 1)]),
     bde("ru-jager-brigade", "Kalogrivov's Brigade", "Col Kalogrivov", regiments=[ru_regt("49th Jäger", 1, "ru-jager"), ru_regt("50th Jäger", 1, "ru-jager")])],
    command=[cmd("ru-div-cmd", "Maj-Gen Lieven III")],
    notes=[LIST_RU, MM_NOTE,
           "Zass's 10th Division (the first two brigades), Selivanov's brigade of the 16th, and Stavitsky's 27th (the last three).",
           MM_RU_BN, "The corps' three batteries are with the brigades, as the list takes them.",
           "Four infantry brigades and two Jäger brigades, where the list allows three and one, and three regiments in "
           "Sokolovsky's brigade, where it takes two, show as historical departures."])

MM_TALYZIN = force(
    "montmirail-talyzin", RU, "Talyzin's Corps", "VI Infantry Corps, Sacken's corps, Army of Silesia", "Russian",
    "Sacken's left, south of the high road, under Talyzin while Shcherbatov was sick. Its brigades took Marchais in the "
    "morning and lost it again; Defrance's Gardes d'Honneur cut up Dieterich's and Blagoveshchensky's men west of the ravine, "
    "and the Sophia regiment had to fight its way out.",
    [bde("ru-infantry-brigade", "Krichinikov's Brigade", "Col Krichinikov", units=[u("ru-position-arty", "Position Battery #10")],
         regiments=[ru_regt("Pskov Infantry", 1), ru_regt("Moscow Infantry", 1)]),
     bde("ru-infantry-brigade", "Augustov's Brigade", "Col Augustov", regiments=[ru_regt("Sophia Infantry", 1), ru_regt("Libau Infantry", 1)]),
     bde("ru-jager-brigade", "Dieterich's Brigade", "Col Dieterich", regiments=[ru_regt("11th Jäger", 1, "ru-jager"), ru_regt("36th Jäger", 1, "ru-jager")]),
     bde("ru-infantry-brigade", "Blagoveshchensky's Brigade", "Lt-Col Blagoveshchensky", units=[u("ru-light-arty", "Light Battery #19")],
         regiments=[ru_regt("Vladimir Infantry", 1), ru_regt("Dnieper Infantry", 1)]),
     bde("ru-infantry-brigade", "Heidenreich's Brigade", "Maj-Gen Heidenreich", units=[u("ru-light-arty", "Light Battery #24")],
         regiments=[ru_regt("Tambov Infantry", 1), ru_regt("Kostroma Infantry", 1)]),
     bde("ru-jager-brigade", "Metcherinov's Brigade", "Maj-Gen Metcherinov", regiments=[ru_regt("28th Jäger", 1, "ru-jager"), ru_regt("32nd Jäger", 1, "ru-jager")])],
    command=[cmd("ru-div-cmd", "Gen-Lt Talyzin II")],
    notes=[LIST_RU, MM_NOTE,
           "Prince Shcherbatov's 7th Division (the first three brigades) and Bernodessov's 18th (the last three). Nafziger names "
           "Talyzin as the corps' commander; Wikipedia's account has Shcherbatov sick and Talyzin acting for him.",
           "Each regiment had a single battalion; each is shown as its one battalion, at full size.",
           "The corps' three batteries are with the brigades, as the list takes them.",
           "Four infantry brigades and two Jäger brigades, where the list allows three and one, show as historical departures."])

MM_VASILCHIKOV = force(
    "montmirail-vasilchikov", RU, "Vasilchikov's Cavalry", "Cavalry Corps, Sacken's corps", "Russian",
    "Sacken's hussars and dragoons, which counter-attacked Nansouty's Guard cavalry and covered the corps' retreat north "
    "towards the Marne.",
    [bde("ru-light-cavalry-brigade", "Vodbolsky's Brigade", "Maj-Gen Vodbolsky",
         units=[u("ru-hussar", "Akhtyrka Hussars (6 squadrons)"), u("ru-hussar", "Mariupol Hussars (5 squadrons)"), u("ru-horse-arty", "Horse Battery #6")]),
     bde("ru-light-cavalry-brigade", "Vasilchikov's Brigade", "Col Vasilchikov",
         units=[u("ru-hussar", "White Russia Hussars (4 squadrons)"), u("ru-hussar", "Alexandria Hussars (5 squadrons)"), u("ru-horse-arty", "Horse Battery #7")]),
     bde("ru-heavy-cavalry-brigade", "Ushakov's Brigade", "Maj-Gen Ushakov", units=[u("ru-dragoon", "Smolensk Dragoons"), u("ru-dragoon", "Courland Dragoons")]),
     bde("ru-heavy-cavalry-brigade", "Umanets's Brigade", "Maj-Gen Umanets",
         units=[u("ru-dragoon", "Tver Dragoons"), u("ru-dragoon", "Kinburn Dragoons"), u("ru-horse-arty", "Horse Battery #18")])],
    command=[cmd("ru-div-cmd", "Gen-Lt Vasilchikov")],
    notes=[LIST_RU, MM_NOTE,
           "Lanskoy's 2nd Hussar Division (the light brigades) and Panchulidzev's 3rd Dragoon Division (the dragoons), with "
           "its three horse batteries.",
           "Two light and two heavy cavalry brigades, where the list allows one of each, three horse batteries, where it allows "
           "two for eight regiments, and cavalry with no infantry brigade to allow it, show as historical departures."])

MM_KARPOV = force(
    "montmirail-karpov", RU, "Karpov's Cossacks", "Cossacks, Sacken's corps", "Russian",
    "Sacken's Cossacks, driven out of Montmirail early on the 11th as Napoleon's army came up.",
    [bde("ru-cossack-brigade", "Karpov's Brigade", "Maj-Gen Karpov II",
         units=[u("ru-mounted-cossack", "Karpov #2 Don Cossacks"), u("ru-mounted-cossack", "Semenchikov #4 Don Cossacks"),
                u("ru-mounted-cossack", "Lukovkin #2 Don Cossacks"), u("ru-mounted-cossack", "Kuteinikov #4 Don Cossacks")]),
     bde("ru-cossack-brigade", "Karpov's Other Regiments", "",
         units=[u("ru-mounted-cossack", "Grekov #1 Don Cossacks"), u("ru-irregular-mounted-cossack", "St Petersburg Opolchenie Cossacks"),
                u("ru-mounted-cossack", "4th Ukrainian Cossacks"), u("ru-irregular-mounted-cossack", "2nd Kalmyk Regiment")])],
    command=[cmd("ru-div-cmd", "Maj-Gen Karpov II")],
    notes=[LIST_RU, MM_NOTE,
           "Nafziger gives Karpov's eight regiments as one brigade; they are split into two here, the Don regiments first, as "
           "the list's brigades take four. The St Petersburg Opolchenie Cossacks and the Kalmyks are the list's Irregular Cossacks.",
           "Two Cossack brigades, where the list allows one, and Cossacks with no infantry brigade to allow them, show as "
           "historical departures."])

MM_YORCK = force(
    "montmirail-yorck", PR15, "Yorck's Corps", "Pirch II's and Horn's brigades, I Corps, Army of Silesia", "Prussian",
    "The part of Yorck's corps that came up late from Château-Thierry to help Sacken. Pirch's brigade attacked the Bois de "
    "Bailly and the woods round Plénois and was thrown back, Pirch wounded; Horn's brigade came up behind it at Fontenelle "
    "and covered the retreat.",
    [pi("1st Brigade (Pirch II)", "Gen-Maj von Pirch II",
        [("Grenadier Battalions", [("M", "1st East Prussian Grenadier Battalion"), ("M", "Silesian Grenadier Battalion")]),
         ("Grenadier Battalions (Leib and West Prussian)", [("M", "Leib Grenadier Battalion"), ("M", "West Prussian Grenadier Battalion")]),
         ("13th Silesian Landwehr", [("L", f"{i}/13th Silesian Landwehr") for i in ("I", "II", "III", "IV")])],
        [u("pr15-mounted-landwehr-attached", "East Prussian National Cavalry (4 squadrons, with volunteer Jäger)"),
         u("pr15-foot-arty", "6-pdr Foot Battery #2")]),
     pi("7th Brigade (Horn)", "Gen-Maj von Horn",
        [("Leib Infantry", [("M", "I/Leib Infantry"), ("M", "II/Leib Infantry"), ("F", "F/Leib Infantry")]),
         ("4th Silesian Landwehr", [("L", "I/4th Silesian Landwehr"), ("L", "II/4th Silesian Landwehr")]),
         ("15th Silesian Landwehr", [("L", "I/15th Silesian Landwehr"), ("L", "II/15th Silesian Landwehr")])],
        [u("pr15-hussar-attached", "Brandenburg Hussars (with volunteer Jäger)"), u("pr15-foot-arty", "6-pdr Foot Battery #3")])],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Yorck")],
    notes=[PR_LIST, MM_NOTE, PR_GROUPED, PR_SUB,
           "Only these two of Yorck's brigades are on Nafziger's return. Its four grenadier battalions, each of a different "
           "regiment, are grouped in pairs as regiments, as the list takes them; they have its Veteran upgrade.",
           "The East Prussian National Cavalry, a volunteer regiment, is the list's small Landwehr cavalry regiment, and the "
           "Brandenburg Hussars its small hussar regiment, each attached to its brigade.",
           "Each brigade's battalions are shown at full size, though most were well under strength by now.",
           "The 13th Silesian Landwehr's four battalions, where the list's Landwehr regiment takes three, show as a historical departure."])

MONTMIRAIL = fought("montmirail", [MM_FR, SIX_DAYS, wiki("Battle of Montmirail", "Battle_of_Montmirail")],
    [MM_RICARD, MM_MEUNIER, MM_CURIAL, MM_FRIANT, MM_MICHEL, MM_COLBERT, MM_LEFEBVRE, MM_LAFERRIERE, MM_DEFRANCE,
     MM_LIEVEN, MM_TALYZIN, MM_VASILCHIKOV, MM_KARPOV, MM_YORCK], [],
    alliances=(("Russian", "Prussian"),))

# ---------------------------------------------------------------- Château-Thierry, 12 February 1814, written

CT_NOTE = ("Built from Nafziger's order of battle for Montmirail the day before; he has none for Château-Thierry. Who was "
           "engaged is from Wikipedia's account of the battle.")


def next_day(f, id_, summary, extra=()):
    """A Montmirail force as it fought the next day, its notes the same but for their source"""
    notes = [CT_NOTE if n == MM_NOTE else n for n in f["notes"]]
    return again(f, id_, summary, notes[:2] + list(extra) + notes[2:])


CT_CHRISTIANI = next_day(
    MM_MICHEL, "chateau-thierry-christiani",
    "The Guard's second division, under Christiani now that Michel had been wounded, which led Mortier's pursuit up the "
    "high road towards the Marne and came on head on at the allied rearguard.",
    ["Michel was wounded at Montmirail; Christiani led the division from the next day, as Wikipedia's account has it."])
CT_CHRISTIANI["name"] = "Christiani's Division"
CT_CHRISTIANI["command"] = [cmd("fig-div-cmd", "Gén. de Division Christiani")]

CT_MEUNIER = next_day(MM_MEUNIER, "chateau-thierry-meunier",
    "Ney's first Young Guard division, which followed Christiani's up the high road behind the allied rearguard.")

CT_FRIANT = next_day(MM_FRIANT, "chateau-thierry-friant",
    "The Old Guard's first division, which followed the pursuit; two battalions of its Chasseurs à Pied, with Guyot's "
    "duty squadrons, fell on Katzler's Prussians at Viffort, and two hundred grenadiers took Petite-Noue.")

CT_COLBERT = next_day(MM_COLBERT, "chateau-thierry-colbert",
    "Ney led the Guard's cavalry after the allied rearguard; Colbert's division rode with Laferrière's and "
    "Lefebvre-Desnouettes's against the Prussian columns.")

CT_LEFEBVRE = next_day(MM_LEFEBVRE, "chateau-thierry-lefebvre-desnouettes",
    "With the rest of the Guard's cavalry under Ney in the pursuit to the Marne.")

CT_LAFERRIERE = next_day(MM_LAFERRIERE, "chateau-thierry-laferriere",
    "The division that did most in the pursuit: its Guard dragoons rode at the Prussian columns, and Letort's squadrons "
    "broke Horn's brigade before the town and took its guns.")

CT_DEFRANCE = next_day(MM_DEFRANCE, "chateau-thierry-defrance",
    "The Gardes d'Honneur, who charged the Prussian columns with Laferrière's dragoons.")

CT_YORCK = next_day(MM_YORCK, "chateau-thierry-yorck",
    "Yorck's brigades, covering Sacken's crossing of the Marne. Katzler's advance guard held Montfaucon and Viffort until "
    "the Guard drove it in; Horn's brigade, blocking the high road, was broken before the town by Letort's squadrons, and "
    "two East Prussian battalions were cut off and taken.")
CT_YORCK["formation"] = "I Corps, Army of Silesia"
CT_YORCK["missing"] = [{"name": "Katzler's advance guard and Jürgass's reserve cavalry",
                        "reason": "Not on Nafziger's Montmirail return, which this is built from; Wikipedia's account has them in the fight."}]

CT_LIEVEN = next_day(MM_LIEVEN, "chateau-thierry-lieven",
    "Lieven's corps, already beaten at Montmirail, falling back over the Marne at Château-Thierry behind Yorck's rearguard.")
CT_TALYZIN = next_day(MM_TALYZIN, "chateau-thierry-talyzin",
    "Talyzin's corps, falling back over the Marne behind Yorck's rearguard; Heidenreich's brigade, with the Tambov and "
    "Kostroma regiments, was overrun and mostly taken.")
CT_VASILCHIKOV = next_day(MM_VASILCHIKOV, "chateau-thierry-vasilchikov",
    "Sacken's horse, covering the retreat to the Marne; a dragoon regiment was routed by the Guard cavalry.")

CHATEAU_THIERRY = fought("chateau-thierry", [MM_FR, SIX_DAYS, wiki("Battle of Château-Thierry (1814)", "Battle_of_Ch%C3%A2teau-Thierry_(1814)")],
    [CT_CHRISTIANI, CT_MEUNIER, CT_FRIANT, CT_COLBERT, CT_LEFEBVRE, CT_LAFERRIERE, CT_DEFRANCE, CT_YORCK, CT_LIEVEN, CT_TALYZIN, CT_VASILCHIKOV], [],
    alliances=(("Prussian", "Russian"),))

# ---------------------------------------------------------------- Vauchamps, 14 February 1814, written

VC_FR = {"label": "French and Allied Forces, Battle of Vauchamps, 14 February 1814 (Nafziger Collection 814BAC)", "url": NAF + "814BAC.pdf"}
VC_NOTE = ("After Nafziger's order of battle for Vauchamps, from the French archives and Clerc's history of Soult's "
           "campaign; its strengths are of 1 February.")
VC_VI = "Nafziger notes that Ricard's and Lagrange's divisions together had only about three thousand men by now."
VC_CAV = "Nafziger gives the I and II Cavalry Corps together about 3,600 men."


def at_vauchamps(f, id_, summary, keep_from=2, extra=()):
    """A force from the Six Days' earlier battles, as Nafziger gives it again at Vauchamps"""
    return again(f, id_, summary, [f["notes"][0], VC_NOTE] + list(extra) + f["notes"][keep_from:])


VC_RICARD = at_vauchamps(
    MM_RICARD, "vauchamps-ricard",
    "Marmont's division, which led the counter-attack on Zieten's brigade in Vauchamps as Blücher's advance ran into the "
    "Emperor's army, and followed it back along the road.", extra=[VC_VI])

VC_LAGRANGE = at_vauchamps(
    CH_LAGRANGE, "vauchamps-lagrange",
    "Marmont's other division, which followed the allied retreat along the high road through the afternoon and took "
    "Étoges after dark.", extra=[VC_VI])
brigade_of(VC_LAGRANGE, "VI Corps Artillery")["units"] = [u("fr-foot-arty", "23/3rd Foot Artillery"), u("fr-foot-arty", "25/3rd Foot Artillery")]
VC_LAGRANGE["notes"] = [n.replace("three companies of the 3rd Foot Artillery, one with the division and two in the corps artillery",
                                  "three companies of the 3rd Foot Artillery from Nafziger's Vauchamps return, one with the division and two in the corps artillery")
                        for n in VC_LAGRANGE["notes"]]
VC_LAGRANGE["missing"] = [
    {"name": "Eight more foot companies and three horse companies",
     "reason": "The rest of Marmont's corps artillery on Nafziger's return, the companies of the 2nd, 4th and 5th Foot and of three horse regiments, a few dozen gunners each."}]

VC_LEVAL = force(
    "vauchamps-leval", FR, "Leval's Division", "7th Division, attached to Marmont", "French",
    "Veterans brought from Soult's army in the Pyrenees that winter, just arrived and lent to Marmont, which moved out to "
    "come round the allied flank as Grouchy's cavalry did.",
    [bde("fr-infantry-brigade", "Pinoteau's Brigade", "Gén. de Brigade Pinoteau",
         regiments=[one("fr-light-infantry", "10th Léger"), one("fr-line-infantry", "3rd Line"), one("fr-line-infantry", "45th Line")]),
     bde("fr-infantry-brigade", "Montfort's Brigade", "Gén. de Brigade Montfort",
         regiments=[one("fr-light-infantry", "17th Léger"), bn_list("fr-line-infantry", "101st Line", ["1", "2"]),
                    bn_list("fr-line-infantry", "105th Line", ["1", "2"])]),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "Foot Battery")]),
     bde("fr-artillery-brigade", "Attached Artillery", units=[u("fr-foot-arty", "Foot Battery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Leval")],
    notes=[LIST_FR, VC_NOTE,
           "The division had about 4,500 men in eight battalions, among the best in the army.",
           "Nafziger gives the division two foot batteries and a horse battery; the second foot battery is in the reserve "
           "artillery here, as the list takes it.",
           "Two light regiments, where the list allows one in the division, show as a historical departure. How far the "
           "division came into action isn't clear from Wikipedia's account."])
VC_LEVAL["missing"] = [{"name": "Horse Battery", "reason": "With no cavalry in the division to allow it."}]

VC_BORDESOULLE = at_vauchamps(
    CH_BORDESOULLE, "vauchamps-bordesoulle",
    "Grouchy's heavy horse, which came up late and joined in the last charges on the allied squares; in the night "
    "Doumerc's cuirassiers surprised Udom's Russians at Étoges.",
    extra=[VC_CAV])
VC_BORDESOULLE["notes"] = [n for n in VC_BORDESOULLE["notes"] if "round the Russian left" not in n]

VC_ST_GERMAIN = force(
    "vauchamps-saint-germain", FR, "Saint-Germain's Cavalry", "II Cavalry Corps, under Grouchy", "French",
    "Grouchy's leading horse, which rode round Zieten's flank, cut off his brigade's retreat, and then charged again and "
    "again at the Prussian and Russian squares as they fell back along the road to Étoges.",
    [bde("fr-light-cavalry-brigade", "Dommanget's Brigade", "Gén. de Brigade Dommanget",
         units=[u("fr-hussar-regt", "5th Hussars"), u("fr-hussar-regt", "9th Hussars"), u("fr-chasseur-a-cheval", "11th Chasseurs à Cheval"),
                u("fr-chasseur-a-cheval", "12th Chasseurs à Cheval"), u("fr-lancer", "2nd Chevau-légers"), u("fr-lancer", "4th Chevau-légers")]),
     bde("fr-light-cavalry-brigade", "Jamin's Brigade", "Gén. de Brigade Jamin",
         units=[u("fr-hussar-regt", "10th Hussars"), u("fr-lancer", "6th Chevau-légers"), u("fr-chasseur-a-cheval", "7th Chasseurs à Cheval"),
                u("fr-chasseur-a-cheval", "20th Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "23rd Chasseurs à Cheval"),
                u("fr-chasseur-a-cheval", "24th Chasseurs à Cheval")]),
     bde("fr-heavy-cavalry-brigade", "Blancard's Brigade", "Gén. de Brigade Blancard",
         units=[u("fr-carabinier", "1st Carabiniers"), u("fr-carabinier", "2nd Carabiniers"), u("fr-cuirassier", "1st Cuirassiers")]),
     bde("fr-heavy-cavalry-brigade", "Sopransy's Brigade", "Gén. de Brigade Sopransy",
         units=[u("fr-cuirassier", "5th Cuirassiers"), u("fr-cuirassier", "8th Cuirassiers"), u("fr-cuirassier", "10th Cuirassiers"),
                u("fr-cuirassier", "13th Cuirassiers")]),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-horse-arty", "Horse Battery")]),
     bde("fr-artillery-brigade", "Corps Artillery", units=[u("fr-horse-arty", "Horse Battery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Saint-Germain")],
    notes=[LIST_FR, VC_NOTE, VC_CAV,
           "Berckheim's 2nd Light Cavalry Division is Dommanget's and Jamin's brigades, and Saint-Germain's own 2nd Heavy "
           "Division Blancard's and Sopransy's. They were the regiments of Sébastiani's corps of 1813, a hundred or so men "
           "each by now; each is shown as one unit at full size, and the list's Small upgrade would suit them all.",
           "The chevau-légers lanciers are the list's Lancers. Its two horse batteries are one in its divisional artillery and "
           "one in its reserve, as the list takes them.",
           "Light brigades of six regiments and a heavy brigade of four, where the list's take four and three, and two heavy "
           "brigades, where it takes one, show as historical departures.",
           CAV_ONLY])

VC_LEFEBVRE = at_vauchamps(
    MM_LEFEBVRE, "vauchamps-lefebvre-desnouettes",
    "With Laferrière's division under Nansouty, it pressed Zieten's left as Grouchy came round his right.",
    extra=["Nafziger gives the two Guard cavalry divisions together about 3,500 men."])

VC_LAFERRIERE = at_vauchamps(
    MM_LAFERRIERE, "vauchamps-laferriere",
    "With Lefebvre-Desnouettes's division under Nansouty, it pressed Zieten's left as Grouchy came round his right.",
    extra=["Nafziger gives the two Guard cavalry divisions together about 3,500 men."])

VC_FRIANT = at_vauchamps(
    MM_FRIANT, "vauchamps-friant",
    "The Old Guard, marched up behind the cavalry from Château-Thierry and held in reserve; only one of its battalions "
    "came into action.",
    extra=["Nafziger notes that the Guard infantry, his order of battle's other three divisions with it, wasn't seriously engaged."])

# --- Vauchamps: the allies

VC_KLEIST = force(
    "vauchamps-kleist", PR15, "Kleist's Corps", "II Corps, Army of Silesia", "Prussian",
    "Blücher's leading corps, marching west on Montmirail to fall on Marmont, which met Napoleon's whole army instead. "
    "Zieten's brigade, ahead at Vauchamps, was broken and lost two thousand prisoners; the rest of the corps fell back "
    "along the high road to Étoges in squares, with Grouchy's horsemen riding round and through them, and Kleist and "
    "Prince August were nearly taken.",
    [pi("10th Brigade (Pirch I)", "Gen-Maj von Pirch I",
        [("2nd West Prussian Infantry", [("M", "I/2nd West Prussian Infantry"), ("M", "II/2nd West Prussian Infantry"), ("M", "III/2nd West Prussian Infantry")]),
         ("7th Reserve Infantry", [("M", "I/7th Reserve Infantry"), ("M", "II/7th Reserve Infantry"), ("M", "III/7th Reserve Infantry")])],
        [u("pr15-mounted-landwehr-attached", "8th Silesian Landwehr Cavalry (5 squadrons)"), u("pr15-foot-arty", "6-pdr Foot Battery #8")]),
     pi("11th Brigade (Zieten)", "Gen-Maj von Zieten",
        [("1st Silesian Infantry", [("M", "I/1st Silesian Infantry"), ("M", "II/1st Silesian Infantry"), ("F", "F/1st Silesian Infantry")]),
         ("10th Reserve Infantry", [("M", "I/10th Reserve Infantry"), ("M", "II/10th Reserve Infantry"), ("F", "F/10th Reserve Infantry")])],
        [u("pr15-schutzen", "Silesian Schützen (2 companies)"), u("pr15-hussar-attached", "1st Silesian Hussars (4 squadrons)"),
         u("pr15-foot-arty", "6-pdr Foot Battery #9")]),
     pi("12th Brigade (Prince August)", "Gen-Maj Prince August of Prussia",
        [("2nd Silesian Infantry", [("M", "I/2nd Silesian Infantry"), ("M", "II/2nd Silesian Infantry"), ("F", "F/2nd Silesian Infantry")]),
         ("11th Reserve Infantry", [("M", "I/11th Reserve Infantry"), ("M", "II/11th Reserve Infantry")])],
        [u("pr15-mounted-landwehr-attached", "7th Silesian Landwehr Cavalry (4 squadrons)"), u("pr15-foot-arty", "6-pdr Foot Battery #21")]),
     pc("Reserve Cavalry (Hacke)", "Col von Hacke",
        [u("pr15-dragoon", "Silesian Cuirassiers"), u("pr15-uhlan", "Silesian Uhlans"), u("pr15-horse-arty", "6-pdr Horse Battery #8")]),
     pc("Reserve Cavalry (Röder)", "Gen-Maj von Röder",
        [u("pr15-dragoon", "East Prussian Cuirassiers"), u("pr15-dragoon", "Brandenburg Cuirassiers")]),
     pres(u("pr15-heavy-arty", "12-pdr Foot Battery #3"), u("pr15-heavy-arty", "12-pdr Foot Battery #6"),
          u("pr15-foot-arty", "6-pdr Foot Battery #11"), u("pr15-foot-arty", "6-pdr Foot Battery #13"),
          u("pr15-horse-arty", "6-pdr Horse Battery #9"), u("pr15-horse-arty", "6-pdr Horse Battery #10"),
          u("pr15-foot-arty", "Howitzer Battery #1"))],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Kleist")],
    notes=[PR_LIST, VC_NOTE, PR_WHOLE, PR_GROUPED, PR_SUB,
           "Nafziger gives the corps 13,500 men. The 7th Reserve Infantry's third battalion was taken whole in the retreat.",
           "Each brigade's cavalry regiment, Landwehr or hussars, is attached to it as the list's small regiment. The list has no "
           "cuirassiers: the Silesian, East Prussian and Brandenburg Cuirassiers are its Dragoons, its only heavy cavalry.",
           "Braun's reserve artillery is the list's: the 12-pdr batteries its Heavy Artillery, and the howitzer battery its Foot Artillery.",
           "Nafziger numbers the 2nd West Prussian's battalions 1 to 3, without a fusilier battalion; all three are Musketeers here. "
           "Pirch's two regiments of three musketeer battalions, where the list's take two, brigades without Landwehr "
           "infantry, and more reserve artillery or cavalry brigades than the list allows for the corps, show as historical "
           "departures."])

VC_KAPTSEVICH = force(
    "vauchamps-kaptsevich", RU, "Kaptsevich's Corps", "X Infantry Corps, Army of Silesia", "Russian",
    "Langeron's corps marching with Kleist's, about 6,500 men, which fell back beside the Prussians in squares along the "
    "high road. Urusov's division, left at Étoges as a rearguard, was surprised there after dark and taken with eight guns.",
    [bde("ru-infantry-brigade", "Schenschin's Brigade", "Col Schenschin", units=[u("ru-position-arty", "Position Battery #39")],
         regiments=[ru_regt("Arkhangelsk Infantry", 2), ru_regt("Schlüsselburg Infantry", 2), ru_regt("Old Ingermanland Infantry", 2)]),
     bde("ru-jager-brigade", "Suthof's Brigade", "Col Suthof", regiments=[ru_regt("7th Jäger", 2, "ru-jager"), ru_regt("37th Jäger", 1, "ru-jager")]),
     bde("ru-infantry-brigade", "Shapskoy's Brigade", "Maj-Gen Shapskoy", units=[u("ru-light-arty", "Light Battery #3")],
         regiments=[ru_regt("Olonets Infantry", 1), ru_regt("Vyatka Infantry", 2), ru_regt("Staroskol Infantry", 1)]),
     bde("ru-jager-brigade", "Vasilchikov's Brigade", "Maj-Gen Vasilchikov", units=[u("ru-light-arty", "Light Battery #56")],
         regiments=[ru_regt("29th Jäger", 1, "ru-jager"), ru_regt("45th Jäger", 1, "ru-jager")])],
    command=[cmd("ru-div-cmd", "Gen-Lt Kaptsevich")],
    notes=[LIST_RU, VC_NOTE,
           "Urusov's 8th Division (the first two brigades) and Turchaninov's 22nd (the last two). Its regiments had one or two "
           "battalions each, a few hundred men; each is shown at full size, and the list's Small upgrade would suit them.",
           "Its three batteries, a position and two light, are with the brigades, as the list takes them.",
           "Three infantry regiments in a brigade, where the list takes two, and two Jäger brigades, where it allows one, show "
           "as historical departures."])

VAUCHAMPS = fought("vauchamps", [VC_FR, SIX_DAYS, wiki("Battle of Vauchamps", "Battle_of_Vauchamps")],
    [VC_RICARD, VC_LAGRANGE, VC_LEVAL, VC_ST_GERMAIN, VC_BORDESOULLE, VC_LEFEBVRE, VC_LAFERRIERE, VC_FRIANT, VC_KLEIST, VC_KAPTSEVICH], [
    ru("Udom's Division", "9th Division, IX Infantry Corps",
       "The fifteen hundred who had got away from Champaubert, made up into three or four combined battalions with a single "
       "battery, and surprised at Étoges after dark by Doumerc's cuirassiers; Nafziger notes their organisation isn't known.")],
    alliances=(("Prussian", "Russian"),))

# ---------------------------------------------------------------- Mormant and Montereau, 17 and 18 February 1814, written

MT_FR = {"label": "French Order of Battle, Montereau, 17/18 February 1814 (Nafziger Collection 814BDI)", "url": NAF + "814BDI.pdf"}
MT_NOTE = ("After Nafziger's order of battle for the army on 17 and 18 February, from the French archives; Victor's corps is "
           "as of 15 February and the cavalry corps as of 9 February.")
MT_ONE_BN = "Each regiment had one or two battalions here; each is shown as its battalions."
II_NO_ARTY = "Nafziger gives the corps no artillery on this return; it is left out."
GERARD_ARTY = ("Nafziger gives Gérard's artillery as four foot companies; one is with each division here, the others in its "
               "missing units.")


def mt_force(id_, name, formation, summary, brigades, commander, notes, nation=FR):
    return force(id_, nation, name, formation, "French", summary, brigades, command=[commander], notes=notes)


def chateau(id_, summary):
    return mt_force(id_, "Chateau's Division", "1st Division, II Corps (Victor)", summary,
        [bde("fr-infantry-brigade", "Chateau's First Brigade",
             regiments=[bn("fr-light-infantry", "1/24th Léger"), bn("fr-line-infantry", "1/19th Line"), bn("fr-line-infantry", "1/37th Line")]),
         bde("fr-infantry-brigade", "Chateau's Second Brigade",
             regiments=[bn("fr-line-infantry", "1/2nd Line"), bn("fr-line-infantry", "1/56th Line"), bn("fr-light-infantry", "1/11th Léger")])],
        cmd("fr-div-cmd", "Gén. de Division Huguet-Chateau"),
        [LIST_FR, MT_NOTE, MT_ONE_BN, "Nafziger names neither brigade's commander.", II_NO_ARTY,
         "Two light regiments, where the list allows one in the division, show as a historical departure."])


def duhesme(id_, summary):
    return mt_force(id_, "Duhesme's Division", "2nd Division, II Corps (Victor)", summary,
        [bde("fr-infantry-brigade", "Duhesme's First Brigade",
             regiments=[bn("fr-light-infantry", "1/26th Léger"), bn_list("fr-line-infantry", "4th Line", ["1", "2"]),
                        bn_list("fr-line-infantry", "18th Line", ["1", "2"])]),
         bde("fr-infantry-brigade", "Duhesme's Second Brigade",
             regiments=[bn_list("fr-line-infantry", "46th Line", ["1", "2"]), bn("fr-line-infantry", "1/72nd Line"), bn("fr-line-infantry", "1/93rd Line")])],
        cmd("fr-div-cmd", "Gén. de Division Duhesme"),
        [LIST_FR, MT_NOTE, MT_ONE_BN, "Nafziger names neither brigade's commander.", II_NO_ARTY])


def dufour(id_, summary):
    f = mt_force(id_, "Dufour's Division", "1st Division, Paris Reserve (Gérard)", summary,
        [bde("fr-infantry-brigade", "Dufour's First Brigade",
             regiments=[bn("fr-light-infantry", "3/12th Léger"), bn("fr-light-infantry", "6/29th Léger"),
                        bn("fr-line-infantry", "8/32nd Line"), bn("fr-line-infantry", "6/58th Line")]),
         bde("fr-infantry-brigade", "Dufour's Second Brigade",
             regiments=[bn("fr-line-infantry", "3/135th Line"), bn("fr-light-infantry", "7/15th Léger"), bn("fr-light-infantry", "2/5th Léger")]),
         bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "10/6th Foot Artillery")])],
        cmd("fr-div-cmd", "Gén. de Division Dufour"),
        [LIST_FR, MT_NOTE,
         "Its battalions were from the depots of a dozen regiments, mostly one from each; each is shown as a regiment of its one "
         "battalion. Nafziger names neither the division's commander nor its brigades'; Dufour is from Wikipedia's account.",
         GERARD_ARTY,
         "A brigade of four regiments, where the list takes three, and four light battalions, where it allows one light "
         "regiment in the division, show as historical departures."])
    f["missing"] = [{"name": "Two more foot companies", "reason": "The 24/9th and another company of Gérard's artillery, more than the list takes."}]
    return f


def hamelinaye(id_, summary):
    return mt_force(id_, "Hamelinaye's Division", "2nd Division, Paris Reserve (Gérard)", summary,
        [bde("fr-infantry-brigade", "Hamelinaye's First Brigade",
             regiments=[bn("fr-line-infantry", "4/26th Line"), one("fr-line-infantry", "86th Line"), one("fr-line-infantry", "82nd Line")]),
         bde("fr-infantry-brigade", "Hamelinaye's Second Brigade",
             regiments=[one("fr-line-infantry", "121st Line"), bn("fr-line-infantry", "3/122nd Line"), bn("fr-line-infantry", "2/142nd Line")]),
         bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "8/9th Foot Artillery")])],
        cmd("fr-div-cmd", "Gén. de Division La Hamelinaye"),
        [LIST_FR, MT_NOTE, MT_ONE_BN,
         "Nafziger names neither the division's commander nor its brigades'; La Hamelinaye is from Wikipedia's account.",
         GERARD_ARTY])


MO_CHATEAU = chateau("mormant-chateau",
    "Victor's first division, which advanced on Mormant at dawn on the right of the road and closed on Pahlen's infantry "
    "as the cavalry broke it.")
MO_DUHESME = duhesme("mormant-duhesme",
    "Victor's second division, which advanced on the left of the road beside Chateau's.")
MO_DUFOUR = dufour("mormant-dufour",
    "Gérard's first division, which went on with him to Valjouan in the afternoon against Wrede's Bavarians and Austrians.")
MO_HAMELINAYE = hamelinaye("mormant-hamelinaye",
    "Gérard's second division, which stormed Villeneuve and Grand-Maison at Valjouan and routed Lamotte's Bavarians.")

MO_V_CAVALRY = again(
    RO_V_CAVALRY, "mormant-v-cavalry",
    "Piré's chasseurs and hussars broke Pahlen's cavalry in the open, and Briche's dragoons rode into the Russian squares "
    "and closed the road at Grandpuits; L'Héritier's dragoons routed the Cossacks.",
    [LIST_FR, MT_NOTE,
     "Piré's light division is Subervie's and Du Coëtlosquet's brigades, Briche's heavy division Montélégier's and Ludot's "
     "dragoons, and L'Héritier's Lamotte's and Collaert's. Nafziger names L'Héritier as the corps' commander on 9 February; "
     "Wikipedia's account has Milhaud leading it at Mormant, with L'Héritier's division under Kellermann.",
     "The dragoon divisions were veterans brought from Spain that winter.",
     "Its two horse batteries are from Nafziger's return of 25 January, one in its divisional artillery and one in its "
     "reserve, as the list takes them.",
     "Four heavy cavalry brigades, where the list takes one, and more heavy cavalry than its half of the army for corps "
     "support, show as historical departures.", CAV_ONLY])
for b in MO_V_CAVALRY["brigades"]:
    if b["name"] == "Pac's Brigade":
        b["name"], b["commander"] = "Du Coëtlosquet's Brigade", {"name": "Gén. de Brigade Du Coëtlosquet"}

MO_TRELLIARD = mt_force("mormant-trelliard", "Trelliard's Dragoons", "5th Heavy Cavalry Division, VI Cavalry Corps (Kellermann)",
    "Dragoons brought from Spain, which rode with L'Héritier's division under Kellermann against Pahlen's horse and the Cossacks.",
    [bde("fr-heavy-cavalry-brigade", "Ismert's Brigade", "Gén. de Brigade Ismert",
         units=[u("fr-dragoon", "4th Dragoons"), u("fr-dragoon", "14th Dragoons"), u("fr-dragoon", "16th Dragoons")]),
     bde("fr-heavy-cavalry-brigade", "Ormancy's Brigade", "Gén. de Brigade Ormancy",
         units=[u("fr-dragoon", "17th Dragoons"), u("fr-dragoon", "24th Dragoons"), u("fr-dragoon", "27th Dragoons")])],
    cmd("fr-div-cmd", "Gén. de Division Trelliard"),
    [LIST_FR, MT_NOTE,
     "Veteran regiments of the army in Spain, sent to Napoleon that winter.",
     "What it did at Mormant is from Wikipedia's account, which doesn't say.",
     "Two heavy cavalry brigades, where the list takes one, more heavy cavalry than its half of the army for corps "
     "support, and a cavalry force with no infantry, show as historical departures. Play it alongside infantry, or agree "
     "it with your opponent."])

MORMANT = fought("mormant", [MT_FR, wiki("Battle of Mormant", "Battle_of_Mormant")],
    [MO_CHATEAU, MO_DUHESME, MO_DUFOUR, MO_HAMELINAYE, MO_V_CAVALRY, MO_TRELLIARD], [
    fr("Bordesoulle's Detachment", "I Cavalry Corps",
       "About five hundred horse, which with Gérard's infantry mauled the Bavarians and Austrians at Valjouan."),
    fr("The Guard Artillery", "Drouot",
       "Thirty-six guns pushed up into the front line; the Guard's infantry and cavalry were kept back."),
    ru("Pahlen's Advance Guard", "Wittgenstein's VI Corps, Army of Bohemia",
       "Pahlen's hussars and Cossacks with a few battalions of the 3rd, 4th and 14th Divisions, caught in the open at Mormant; "
       "the cavalry was broken and the infantry's squares ridden over."),
    at("Hardegg's Division", "1st Austrian Division, Wrede's V Corps",
       "Fell back through Nangis and was mauled at Valjouan."),
    bav("Lamotte's Division", "3rd Bavarian Division, Wrede's V Corps",
        "Routed at Valjouan by Gérard's infantry and Bordesoulle's horse.")],
    alliances=(("Russian", "Austrian", "Bavarian"),))

MT_CHATEAU = chateau("montereau-chateau",
    "Victor's first division, whose attacks on the heights before Montereau stalled in the morning; Napoleon gave Victor's "
    "command to Gérard.")
MT_DUHESME = duhesme("montereau-duhesme",
    "Victor's second division, in the morning's failed attacks on the heights and then under Gérard in the afternoon's.")
MT_DUFOUR = dufour("montereau-dufour",
    "Gérard's first division, which led the afternoon's assaults up the heights and took Les Ormeaux and Surville.")
MT_HAMELINAYE = hamelinaye("montereau-hamelinaye",
    "Gérard's second division, beside Dufour's in the assaults on the heights.")

MT_PAJOL = mt_force("montereau-pajol", "Pajol's Cavalry", "Provisional Cavalry Corps", 
    "Detachments from the depots, which charged down the Paris road as the allied line broke and seized the bridges "
    "over the Seine and the Yonne before they could be blown, cutting off the Württembergers' retreat.",
    [bde("fr-light-cavalry-brigade", "Delort's Brigade", "Gén. de Brigade Delort",
         units=[u("fr-chasseur-a-cheval", "Chasseur detachments (5th, 10th, 11th, 13th, 21st and 29th Chasseurs)")]),
     bde("fr-light-cavalry-brigade", "Du Coëtlosquet's Brigade", "Gén. de Brigade Du Coëtlosquet",
         units=[u("fr-hussar-regt", "Hussar detachments (2nd, 4th and 12th Hussars)")]),
     bde("fr-heavy-cavalry-brigade", "Grouvel's Brigade", "Gén. de Brigade Grouvel",
         units=[u("fr-dragoon", "Dragoon detachments (12th, 16th, 21st, 24th, 26th and 29th Dragoons)")])],
    cmd("fr-div-cmd", "Gén. de Division Pajol"),
    [LIST_FR, MT_NOTE,
     "Each brigade was squadrons from the depots of many regiments, four to five hundred men; each is shown as one unit.",
     "Some of the regiments' numbers are hard to read on Nafziger's return.",
     "A cavalry force with no infantry shows as a historical departure. Play it alongside Gérard's or Victor's infantry, "
     "or agree it with your opponent."])
MT_PAJOL["missing"] = [{"name": "2nd Garde Nationale de Cherbourg", "reason": "A detachment of National Guard infantry with the corps."}]

MONTEREAU = fought("montereau", [MT_FR, wiki("Battle of Montereau", "Battle_of_Montereau")],
    [MT_CHATEAU, MT_DUHESME, MT_DUFOUR, MT_HAMELINAYE, MT_PAJOL], [
    fr("Pacthod's National Guards", "About three thousand National Guards, with eight hundred gendarmes",
       "Made no impression on the allied line."),
    fr("The Guard", "Friant's Old Guard and Ney's Young Guard divisions, Nansouty's Guard cavalry and the Guard artillery",
       "The Guard's forty guns were decisive in the afternoon; how far its infantry fought is not clear."),
    wt("The Crown Prince of Württemberg's Corps", "Koch's infantry and Prince Adam's cavalry divisions, IV Corps, Army of Bohemia",
       "Held the heights on the north bank before Montereau, with four batteries, until the line broke in the afternoon; "
       "Jett's cavalry brigade covered the retreat."),
    at("Schäffer's Brigade", "Attached to the IV Corps",
       "Four Austrian infantry regiments and the Archduke Ferdinand Hussars, which held the park of Surville; Schäffer was taken.")],
    alliances=(("Württemberg", "Austrian"),))

# ---------------------------------------------------------------- Bar-sur-Aube and Laubressel, 27 February and 3 March 1814, written

TR_FR = {"label": "French Army before Troyes under Macdonald, 2 March 1814 (Nafziger Collection 814CAD)", "url": NAF + "814CAD.pdf"}
TR_VI = {"label": "French II & VI Corps, 12 March 1814 (Nafziger Collection 814CZA)", "url": NAF + "814CZA.pdf"}
TR_NOTE = ("After Nafziger's return of Macdonald's army before Troyes on 2 March, from Koch's history and the French archives; "
           "its strengths are of 1 to 10 March.")
TR_II_NOTE = ("Gérard's corps isn't on Nafziger's return of 2 March; it is from his return of the II Corps on 12 March, nine "
              "days after Laubressel.")
TR_NG = ("Its National Guards, raised that winter from the departments, are shown as Line; the list's Wavering or Morale 5 "
         "would suit them better.")


def ones(unit, *names):
    return [one(unit, n) for n in names]


LB_DUHESME = force(
    "laubressel-duhesme", FR, "Duhesme's Division", "1st Division, II Corps (Gérard)", "French",
    "Gérard's division at the bridge of La Guillotière on the Barse, which held it until it was turned and lost two guns and "
    "four hundred men.",
    [bde("fr-infantry-brigade", "Dornier's Brigade", "Gén. de Brigade Dornier",
         regiments=ones("fr-light-infantry", "26th Léger") + ones("fr-line-infantry", "72nd Line", "93rd Line", "2nd Line", "37th Line", "56th Line")),
     bde("fr-infantry-brigade", "Matesse's Brigade", "Gén. de Brigade Matesse",
         regiments=ones("fr-light-infantry", "11th Léger", "24th Léger") + ones("fr-line-infantry", "4th Line", "18th Line", "46th Line", "Bataillon de l'Aisne")),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "9/2nd Foot Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Duhesme")],
    notes=[LIST_FR, TR_II_NOTE,
           "Its twelve battalions had twenty to three hundred and fifty men each, 1,900 or so in all; each regiment is shown as "
           "one battalion at full size, and the list's Small upgrade would suit them all.",
           "The corps' artillery, four foot companies and a horse company, is one with each division here.",
           "Brigades of six regiments, where the list's take three, and three light regiments, where it allows one in the "
           "division, show as historical departures."])

LB_HAMELINAYE = force(
    "laubressel-hamelinaye", FR, "Hamelinaye's Division", "2nd Division, II Corps (Gérard)", "French",
    "Gérard's other division, linking Duhesme's to Rottembourg's. Bellair's brigade was routed; Jarry's covered Duhesme's left "
    "and drew off in order, and Gérard fell back into Troyes.",
    [bde("fr-infantry-brigade", "Jarry's Brigade", "Gén. de Brigade Jarry",
         regiments=ones("fr-light-infantry", "12th Léger", "29th Léger", "5th Léger", "15th Léger") + ones("fr-line-infantry", "32nd Line", "58th Line", "135th Line", "155th Line")),
     bde("fr-infantry-brigade", "Bellair's Brigade", "Gén. de Brigade Bellair",
         regiments=ones("fr-line-infantry", "26th Line", "82nd Line", "86th Line", "122nd Line", "142nd Line")),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "10/6th Foot Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division La Hamelinaye")],
    notes=[LIST_FR, TR_II_NOTE,
           "Nafziger names it Hamelinaye's or Dufour's division. Its thirteen battalions had fifty to two hundred men each, some "
           "1,600 in all; each regiment is shown as one battalion at full size, and the list's Small upgrade would suit them all.",
           "The corps' artillery is one company with each division here.",
           "Brigades of eight and five regiments, where the list's take three, and four light regiments, where it allows one in "
           "the division, show as historical departures."])
LB_HAMELINAYE["missing"] = [{"name": "22/8th, 17/5th and 2/9th Foot and 6/3rd Horse Artillery", "reason": "The rest of Gérard's corps artillery."}]

LB_ROTTEMBOURG = force(
    "laubressel-rottembourg", FIG, "Rottembourg's Division", "5th Young Guard Division, VII Corps (Oudinot)", "French",
    "Oudinot's Young Guard on the plateau of Laubressel, which held it until Wittgenstein's Russians came round its flank and "
    "forced it back.",
    [bde("fig-young-guard-brigade", "Charrière's Brigade", "Gén. de Brigade Charrière", regiments=[yg("5th Voltigeurs"), yg("6th Voltigeurs")]),
     bde("fig-young-guard-brigade", "Baudin's Brigade", "Gén. de Brigade Baudin",
         units=[u("fig-yg-foot-arty", "11th Young Guard Foot Company")],
         regiments=[yg("7th Voltigeurs", 3), yg("8th Voltigeurs", 3)])],
    command=[cmd("fig-div-cmd", "Gén. de Division Rottembourg")],
    notes=[LIST_FIG, TR_NOTE, NEW_YG,
           "The division had some seven hundred men in ten battalions by 5 March; they are shown at full size, and the list's "
           "Small upgrade would suit them all. Its regiments are voltigeurs now, where at La Rothière they were tirailleurs.",
           "Its foot company, five 6-pdrs and two howitzers, is with Baudin's brigade.",
           "Regiments of three battalions, where the list's take two, show as historical departures."])

LB_LEVAL = force(
    "laubressel-leval", FR, "Leval's Division", "7th Division, VII Corps (Oudinot)", "French",
    "Veterans from Spain, the strongest division of Oudinot's corps, which fell back on Troyes with it as Wittgenstein "
    "turned the plateau.",
    [bde("fr-infantry-brigade", "Pinoteau's Brigade", "Gén. de Brigade Pinoteau",
         regiments=[bn_list("fr-light-infantry", "10th Léger", ["1", "6"]), bn("fr-line-infantry", "1/3rd Line"), bn("fr-line-infantry", "1/15th Line"),
                    bn_list("fr-line-infantry", "130th Line", ["1", "2"])]),
     bde("fr-infantry-brigade", "Montfort's Brigade", "Gén. de Brigade Montfort",
         regiments=[bn("fr-light-infantry", "1/17th Léger"), bn("fr-line-infantry", "1/101st Line"), bn_list("fr-line-infantry", "105th Line", ["1", "2"]),
                    bn("fr-line-infantry", "6/118th Line")]),
     bde("fr-infantry-brigade", "Chassé's Brigade", "Gén. de Brigade Chassé",
         regiments=[bn("fr-light-infantry", "1/16th Léger"), bn("fr-line-infantry", "1/8th Line"), bn_list("fr-line-infantry", "28th Line", ["1", "3", "6"]),
                    bn("fr-line-infantry", "1/54th Line")]),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "19/1st Foot Artillery")]),
     bde("fr-artillery-brigade", "Attached Artillery", units=[u("fr-foot-arty", "22/5th Foot Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Leval")],
    notes=[LIST_FR, TR_NOTE,
           "The division had some 5,800 men in seventeen battalions, three to nine hundred each. Nafziger gives Chassé's brigade "
           "as its third on 5 March, and as the 9th Division's on 1 March; Wikipedia's account has Chassé leading a division.",
           "Its foot company of eight 6-pdrs and four howitzers is its divisional artillery, and the 9th Division's company is in "
           "its reserve.",
           "Brigades of four regiments, where the list's take three, and three light regiments, where it allows one in the "
           "division, show as historical departures."])

LB_PACTHOD = force(
    "laubressel-pacthod", FR, "Pacthod's National Guards", "National Guard Division, VII Corps (Oudinot)", "French",
    "National Guards raised that winter in the departments, which marched with Oudinot's corps and fell back on Troyes with it.",
    [bde("fr-infantry-brigade", "Rost's Brigade", "Gén. de Brigade Rost",
         regiments=ones("fr-line-infantry", "1st Sarthe", "3rd Indre-et-Loire")),
     bde("fr-infantry-brigade", "Bonté's Brigade", "Gén. de Brigade Bonté",
         regiments=ones("fr-line-infantry", "2nd Loir-et-Cher", "5th Seine-et-Marne")),
     bde("fr-infantry-brigade", "Konzinsky's Brigade", "Gén. de Brigade Konzinsky", regiments=ones("fr-line-infantry", "4th Maine-et-Loire")),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "26/6th Foot Artillery")]),
     bde("fr-artillery-brigade", "Reserve Artillery",
         units=[u("fr-heavy-foot-arty", "24/6th Foot Artillery (12-pdrs)"), u("fr-foot-arty", "12/8th Foot Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Pacthod")],
    notes=[LIST_FR, TR_NOTE, TR_NG,
           "The division had some 3,900 men in five regiments, three to a thousand men each; each regiment is shown as one "
           "unit.",
           "Its own foot company and the VII Corps' reserve companies are with it here; the reserve's horse company is left out.",
           "With five units of infantry, the division's battery and its reserve batteries show as historical departures."])

LB_ALBERT = force(
    "laubressel-albert", FR, "Albert's Division", "XI Corps (Molitor)", "French",
    "Macdonald's corps, which fell back on Troyes without being pressed while Oudinot's and Gérard's were beaten.",
    [bde("fr-infantry-brigade", "Schaeffer's Brigade", "Gén. de Brigade Schaeffer",
         regiments=[bn("fr-line-infantry", "3/139th Line"), bn_list("fr-line-infantry", "1st Regiment of Brest", ["1", "2"])]),
     bde("fr-infantry-brigade", "Albert's Second Brigade",
         regiments=[bn("fr-line-infantry", "1/140th Line"), bn_list("fr-line-infantry", "Regiment of Rochefort", ["1", "2"])]),
     bde("fr-light-cavalry-brigade", "Corps Cavalry", units=[u("fr-hussar-regt", "13th Hussars (2 squadrons)")]),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "15/4th Foot Artillery")]),
     bde("fr-artillery-brigade", "Attached Artillery", units=[u("fr-foot-arty", "18/6th Foot Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Albert")],
    notes=[LIST_FR, TR_NOTE,
           "The division had some 3,200 men; the regiments of Brest and Rochefort, National Guards of the naval ports, had three "
           "to eight hundred a battalion. " + TR_NG,
           "The XI Corps' cavalry, two squadrons of the 13th Hussars, is with the division here.",
           "With six battalions, the second foot battery shows as a historical departure; the division's horse company is left out."])

LB_AMEY = force(
    "laubressel-amey", FR, "Amey's Division", "XI Corps (Molitor)", "French",
    "A small division of Macdonald's corps, which fell back on Troyes without being pressed.",
    [bde("fr-infantry-brigade", "Amey's Brigade",
         regiments=[bn_list("fr-line-infantry", "149th Line", ["1", "2"]), one("fr-line-infantry", "1st Battalion of Calvados"),
                    one("fr-line-infantry", "1st Battalion of La Manche")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Amey")],
    notes=[LIST_FR, TR_NOTE,
           "The division had about seven hundred men in four battalions. The battalions of Calvados and La Manche were National "
           "Guards. " + TR_NG])
LB_AMEY["missing"] = [{"name": "6/4th Horse Artillery", "reason": "Four 8-pdrs and a howitzer, with no cavalry in the division to allow them."}]

LB_BRAYER = force(
    "laubressel-brayer", FR, "Brayer's Division", "XI Corps (Molitor)", "French",
    "The third division of Macdonald's corps, which fell back on Troyes without being pressed.",
    [bde("fr-infantry-brigade", "Brayer's First Brigade",
         regiments=[bn_list("fr-light-infantry", "19th Léger", ["2", "6"]), bn("fr-line-infantry", "3/5th Line"), bn("fr-line-infantry", "3/11th Line")]),
     bde("fr-infantry-brigade", "Brayer's Second Brigade",
         regiments=[bn("fr-line-infantry", "7/107th Line"), bn_list("fr-line-infantry", "Garde Nationale du Nord", ["1", "2"])]),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "6/1st Foot Artillery")]),
     bde("fr-artillery-brigade", "Attached Artillery", units=[u("fr-foot-arty", "19/2nd Foot Artillery"), u("fr-foot-arty", "20/5th Foot Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Brayer")],
    notes=[LIST_FR, TR_NOTE,
           "The division had about 2,000 men in seven battalions; by the end of March they were Guye's brigade of Boyer de "
           "Rébeval's division at Paris. " + TR_NG,
           "Its three foot companies are one in its divisional artillery and two in its reserve; with seven battalions, where "
           "the list wants eight for each reserve battery, the two show as a historical departure."])

LB_ST_GERMAIN = again(
    VC_ST_GERMAIN, "laubressel-saint-germain",
    "Maurin's light horse retook most of the artillery park Pahlen's cavalry had overrun at Thennelières.",
    [LIST_FR, TR_NOTE,
     "Maurin's 2nd Light Cavalry Division is Dommanget's and Jamin's brigades, and Delort's 2nd Cuirassier Division Blancard's "
     "and Sopransy's: the regiments of Sébastiani's corps of 1813, fifty to a hundred and fifty men each by now. Each is shown "
     "as one unit at full size, and the list's Small upgrade would suit them all.",
     "The chevau-légers lanciers are the list's Lancers. Its two horse detachments are one in its divisional artillery and "
     "one in its reserve.",
     "Light brigades of six and five regiments and a heavy brigade of four, where the list's take four and three, and two "
     "heavy brigades, where it takes one, show as historical departures.", CAV_ONLY])
brigade_of(LB_ST_GERMAIN, "Jamin's Brigade")["units"] = [u for u in brigade_of(LB_ST_GERMAIN, "Jamin's Brigade")["units"] if u["name"] != "10th Hussars"]
LB_ST_GERMAIN["formation"] = "II Cavalry Corps"
LB_ST_GERMAIN["missing"] = [{"name": "10th Hussars", "reason": "Detached."}]

LB_V_CAVALRY = again(
    MO_V_CAVALRY, "laubressel-v-cavalry",
    "Milhaud's corps, which fell back with the infantry without being engaged.",
    [LIST_FR, TR_NOTE,
     "Piré's light division, 1,421 men, is Subervie's and the second light brigades; Briche's dragoons, 1,700, Montélégier's and "
     "Ludot's; and L'Héritier's, 1,269, Lamotte's and Collaert's. Their regiments had a hundred to four hundred men; they are "
     "shown at full size.",
     "Its three horse companies are one in its divisional artillery and one in its reserve, as the list takes them.",
     "Four heavy cavalry brigades, where the list takes one, and more heavy cavalry than its half of the army for corps "
     "support, show as historical departures.", CAV_ONLY])
brigade_of(LB_V_CAVALRY, "Du Coëtlosquet's Brigade").update(name="Piré's Second Brigade")
brigade_of(LB_V_CAVALRY, "Piré's Second Brigade").pop("commander", None)
LB_V_CAVALRY["missing"] = [{"name": "8/6th Horse Artillery", "reason": "The corps' third horse company, more than the list takes."}]

LB_TRELLIARD = again(
    MO_TRELLIARD, "laubressel-trelliard",
    "Trelliard's dragoons from Spain, which counter-attacked the Russians at Thennelières.",
    [LIST_FR, TR_NOTE,
     "Its strengths are of 7 March: each regiment had three or four battalion-sized squadrons, a hundred to five hundred men "
     "in all; each is shown as one unit.",
     "Its horse company is its divisional artillery.",
     "Two heavy cavalry brigades, where the list takes one, more heavy cavalry than its half of the army for corps support, "
     "and a cavalry force with no infantry, show as historical departures. Play it alongside infantry, or agree it with your "
     "opponent."])
LB_TRELLIARD["brigades"].append(bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-horse-arty", "6/2nd Horse Artillery")]))

LAUBRESSEL = fought("laubressel", [TR_FR, TR_VI, wiki("Battle of Laubressel", "Battle_of_Laubressel")],
    [LB_DUHESME, LB_HAMELINAYE, LB_ROTTEMBOURG, LB_LEVAL, LB_PACTHOD, LB_ALBERT, LB_AMEY, LB_BRAYER, LB_ST_GERMAIN,
     LB_V_CAVALRY, LB_TRELLIARD], [
    fr("Jacquinot's Division", "VI Cavalry Corps (Kellermann)",
       "Light horse that stampeded at La Chapelle-Saint-Luc; it isn't on Nafziger's return."),
    ru("Wittgenstein's Corps", "Gorchakov's I and Eugen of Württemberg's II Infantry Corps and Pahlen's cavalry, VI Corps",
       "About fourteen thousand men, who took Bouranton and the Laubressel plateau while Pahlen's horse raided the French artillery park."),
    bav("Wrede's Corps", "Three Bavarian and two Austrian divisions, V Corps",
        "About twenty thousand men, whose guns opened the attack; they pushed on towards Troyes."),
    wt("The Crown Prince of Württemberg's Corps", "Koch's and Döring's divisions and Prince Adam's cavalry, IV Corps",
       "About fifteen thousand men on the allied left, who followed Macdonald towards Sens."),
    at("Gyulai's Corps", "Crenneville's, Fresnel's and Hohenlohe's divisions, III Corps",
       "About ten thousand Austrians, who attacked at Silvarouvres.")],
    alliances=(("Russian", "Bavarian", "Württemberg", "Austrian"),))

BA_NOTE = ("Nafziger has no order of battle for Bar-sur-Aube. Wikipedia's account names Oudinot's and Gérard's corps; their "
           "divisions are from Nafziger's returns of 2 and 12 March, a few days after the battle.")


def at_bar(f, id_, summary):
    return again(f, id_, summary, [f["notes"][0], BA_NOTE] + [n for n in f["notes"][2:]])


BA_LEVAL = at_bar(LB_LEVAL, "bar-sur-aube-leval",
    "Oudinot's strongest division, on the heights before Bar-sur-Aube, which took the weight of Wittgenstein's attack and "
    "was driven back over the Aube.")
BA_ROTTEMBOURG = at_bar(LB_ROTTEMBOURG, "bar-sur-aube-rottembourg",
    "Oudinot's Young Guard, beside Leval's on the heights before the town.")
BA_DUHESME = at_bar(LB_DUHESME, "bar-sur-aube-duhesme",
    "Gérard's leading division, with Oudinot's before the town; much of Macdonald's army, and most of its guns, were on the "
    "far side of the Aube and could take no part.")
BA_HAMELINAYE = at_bar(LB_HAMELINAYE, "bar-sur-aube-hamelinaye",
    "Gérard's other division, with Duhesme's before Bar-sur-Aube.")

BAR_SUR_AUBE = fought("bar-sur-aube", [TR_FR, TR_VI, wiki("Battle of Bar-sur-Aube", "Battle_of_Bar-sur-Aube")],
    [BA_LEVAL, BA_ROTTEMBOURG, BA_DUHESME, BA_HAMELINAYE], [
    ru("Wittgenstein's Corps", "VI Corps, Army of Bohemia",
       "Attacked Oudinot's position; Wittgenstein was wounded leading it."),
    bav("Wrede's Corps", "V Corps, Army of Bohemia",
        "Wrede's Bavarians and Austrians, who came on against Oudinot beside Wittgenstein's Russians.")],
    alliances=(("Russian", "Bavarian"),))

# ---------------------------------------------------------------- Craonne, 7 March 1814, written

CR_FR = {"label": "French Forces, Battle of Craone, 7 March 1814 (Nafziger Collection 814CAB)", "url": NAF + "814CAB.pdf"}
CR_NOTE = "After Nafziger's order of battle for Craonne, from Koch's history of the campaign and the French archives."


def at_craonne(f, id_, summary, extra):
    return again(f, id_, summary, [f["notes"][0], CR_NOTE] + list(extra) + [n for n in f["notes"][2:] if "full size" not in n and "men in" not in n])


CR_MEUNIER = at_craonne(MM_MEUNIER, "craonne-meunier",
    "Ney's first Young Guard division, which had taken the abbey of Vauclair the day before and went up onto the plateau "
    "beside Boyer's men in the afternoon.",
    ["The division was down to 865 men; its eight battalions are shown at full size, and the list's Small upgrade would suit them all."])

CR_CURIAL = at_craonne(MM_CURIAL, "craonne-curial",
    "Ney's second Young Guard division, which pressed the last attack on the Russian lines beside Friant's Old Guard.",
    ["The division was down to 1,022 men; its eight battalions are shown at full size, and the list's Small upgrade would suit them all."])
CR_CURIAL["notes"] = [n for n in CR_CURIAL["notes"] if "Pelet" not in n]

CR_BOYER_DE_REBEVAL = force(
    "craonne-boyer-de-rebeval", FR, "Boyer de Rébeval's Division", "9th Division, Victor's corps", "French",
    "Victor's left, which took the Bois Marion at noon and was thrown out of it by a Russian dragoon charge; Victor was "
    "wounded early in the day, and both brigadiers were hit.",
    [bde("fr-infantry-brigade", "Gruyère's Brigade", "Gén. de Brigade Gruyère",
         regiments=[bn_list("fr-light-infantry", "2nd Léger", ["1", "2", "6"]), bn("fr-line-infantry", "1/24th Line"),
                    bn("fr-line-infantry", "6/36th Line"), bn_list("fr-line-infantry", "122nd Line", ["1", "4"])]),
     bde("fr-infantry-brigade", "Chassé's Brigade", "Gén. de Brigade Chassé",
         regiments=[bn("fr-light-infantry", "1/16th Léger"), bn("fr-line-infantry", "1/8th Line"),
                    bn_list("fr-line-infantry", "28th Line", ["1", "3"]), bn("fr-line-infantry", "1/54th Line")]),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "22/5th Foot Artillery")]),
     bde("fr-artillery-brigade", "Attached Artillery", units=[u("fr-foot-arty", "10/8th Foot Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Boyer de Rébeval")],
    notes=[LIST_FR, CR_NOTE,
           "The division had 3,800 men in eleven battalions.",
           "Nafziger gives these line battalions to Boyer de Rébeval as Victor's 9th Division, and Pierre Boyer a division of "
           "unknown battalions under Ney. Wikipedia's account has it the other way about: Pierre Boyer's 9th Division with "
           "Ney, and Boyer de Rébeval a provisional Young Guard division of conscripts with Victor. This follows Nafziger.",
           "Its two foot batteries, eight 6-pdrs and four howitzers, are one in its divisional artillery and one in its reserve, "
           "as the list takes them.",
           "Brigades of four regiments, where the list's take three, and two light regiments, where it allows one in the "
           "division, show as historical departures."])

def yg3(*bns_):
    """Third battalions of two Young Guard regiments, grouped as one regiment as the list takes them"""
    units = [u("fig-yg-voltigeurs" if "Voltigeur" in b else "fig-yg-tirailleurs", b) for b in bns_]
    return regt(" and ".join(b.split("/", 1)[1] for b in bns_), units)


CR_CHARPENTIER = force(
    "craonne-charpentier", FIG, "Charpentier's Division", "7th Young Guard Division, Victor's corps", "French",
    "Victor's Young Guard, which came up late on the right of his line and took the Bois des Quatre Heures in the early "
    "afternoon.",
    [bde("fig-young-guard-brigade", "Charpentier's First Brigade",
         regiments=[yg3("3/3rd Tirailleurs", "3/3rd Voltigeurs"), yg3("3/4th Tirailleurs", "3/4th Voltigeurs"),
                    yg3("3/5th Voltigeurs", "3/6th Voltigeurs")]),
     bde("fig-young-guard-brigade", "Charpentier's Second Brigade",
         regiments=[yg3("3/10th Tirailleurs", "3/11th Tirailleurs"), yg3("3/12th Tirailleurs", "3/7th Voltigeurs"),
                    yg3("3/8th Voltigeurs", "3/11th Voltigeurs")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Charpentier")],
    notes=[LIST_FIG, CR_NOTE, NEW_YG,
           "The division was twelve third battalions of the Young Guard's regiments, 3,600 men. Nafziger gives them without "
           "brigades; they are paired here as regiments of two battalions, in his order, and split into two brigades, as the "
           "list takes them. Nafziger gives the division no guns."])

CR_ROUSSEL = force(
    "craonne-roussel", FR, "Roussel d'Hurbal's Dragoons", "6th Heavy Cavalry Division, under Grouchy", "French",
    "Dragoons from Spain, which charged with Grouchy at the Russian centre: Sparre's brigade drove off the Pavlograd Hussars "
    "and cut down a Russian battery before it was forced back. The division was then moved to the left.",
    [bde("fr-heavy-cavalry-brigade", "Sparre's Brigade", "Gén. de Brigade Sparre",
         units=[u("fr-dragoon", "5th Dragoons"), u("fr-dragoon", "12th Dragoons")]),
     bde("fr-heavy-cavalry-brigade", "Rigaud's Brigade", "Gén. de Brigade Rigaud",
         units=[u("fr-dragoon", "21st Dragoons"), u("fr-dragoon", "26th Dragoons")]),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-horse-arty", "3/3rd Horse Artillery")]),
     bde("fr-artillery-brigade", "Attached Artillery", units=[u("fr-horse-arty", "3/2nd Horse Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Roussel d'Hurbal")],
    notes=[LIST_FR, CR_NOTE,
           "The division had 2,200 men in four regiments, veterans of the army in Spain sent to Napoleon that winter.",
           "Its two horse batteries are one in its divisional artillery and one in its reserve, as the list takes them.",
           "Two heavy cavalry brigades, where the list takes one, more heavy cavalry than its half of the army for corps "
           "support, and a cavalry force with no infantry, show as historical departures. Play it alongside infantry, or agree "
           "it with your opponent."])

CR_PAC = force(
    "craonne-pac", FR, "Nansouty's Cavalry", "Left Wing (Nansouty)", "French",
    "Nansouty's horse on the far right of the Russian line, which went up the Paissy spur and drove back Benckendorff's "
    "hussars and Cossacks until the Russian guns stopped it.",
    [bde("fr-light-cavalry-brigade", "Pac's Brigade", "Gén. de Brigade Pac",
         units=[u("fr-hussar-regt", "3rd Hussars"), u("fr-chasseur-a-cheval", "14th Chasseurs à Cheval"),
                u("fr-chasseur-a-cheval", "26th Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "27th Chasseurs à Cheval")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Nansouty")],
    notes=[LIST_FR, CR_NOTE,
           "Pac's brigade, 450 men of Piré's old regiments, is the one Nafziger identifies of Nansouty's wing; its four "
           "regiments are shown at full size, and the list's Small upgrade would suit them all.", CAV_ONLY])
CR_PAC["missing"] = [{"name": "Exelmans's division", "reason": "About 1,350 horse, whose regiments Nafziger couldn't identify."}]

CR_LAFERRIERE = at_craonne(MM_LAFERRIERE, "craonne-laferriere",
    "The Guard horse with Grouchy, which charged the Russian centre and its great battery and was driven back by the "
    "squares; Laferrière and Grouchy were both wounded.",
    ["The division had 1,250 men by now; the regiments' strengths that follow are of 1 February."])

CR_FRIANT = at_craonne(MM_FRIANT, "craonne-friant",
    "The Old Guard, in Mortier's reserve, which came up behind the final attack in the afternoon as Drouot's eighty-eight "
    "guns battered the Russian lines.",
    ["The division had 3,800 men in eight battalions. The 1st Chasseurs and Grenadiers à Pied are the list's Old Guard, "
     "and the 2nd, raised in 1811, its Middle Guard."])

CR_COLBERT = at_craonne(MM_COLBERT, "craonne-colbert",
    "The Guard horse in Mortier's reserve, sent to the left in the afternoon and driven off there by the Russian hussars.",
    ["The division had 1,100 men."])

CRAONNE = fought("craonne", [CR_FR, wiki("Battle of Craonne", "Battle_of_Craonne")],
    [CR_MEUNIER, CR_CURIAL, CR_BOYER_DE_REBEVAL, CR_CHARPENTIER, CR_ROUSSEL, CR_LAFERRIERE, CR_PAC, CR_FRIANT, CR_COLBERT], [
    fr("Pierre Boyer's Division", "Ney's wing",
       "About 1,900 men with two foot batteries, whose battalions Nafziger couldn't identify; Wikipedia's account has it "
       "attacking Ailles and taking it by three in the afternoon."),
    fr("Christiani's and Poret de Morvan's Divisions", "2nd Old Guard and Tirailleur Divisions, Mortier's reserve",
       "The fusiliers, flanqueurs and vélites of the Old Guard's second division, and a division of Young Guard tirailleurs, "
       "some eight thousand men who weren't engaged."),
    ru("Vorontsov's Corps", "Vuich's 24th, Laptev's 21st, Khovansky's 12th and Zheltukhin's 13th Divisions, with Krasovsky's Jäger and Benckendorff's brigade",
       "Held the narrow plateau of the Chemin des Dames in lines across it through the day, and withdrew in good order."),
    ru("Vasilchikov's Cavalry", "Lanskoy's 2nd Hussar and Panchulidzev's 3rd Dragoon Divisions, with Karpov's Cossacks",
       "Charged Colbert's and Grouchy's squadrons; Lanskoy was mortally wounded."),
    ru("Sacken's Corps", "Army of Silesia",
       "Its cavalry and Nikitin's guns covered Vorontsov's retreat; its infantry was too far off to fight.")])

# ---------------------------------------------------------------- Laon, 9–10 March 1814, written

LA_FR = {"label": "Abstract, French Army at Battle of Laon, 9–10 March 1814 (Nafziger Collection 814CFK)", "url": NAF + "814CFK.pdf"}
LA_VI = {"label": "French II & VI Corps, 12 March 1814 (Nafziger Collection 814CZA)", "url": NAF + "814CZA.pdf"}
LA_NOTE = ("Nafziger's Laon return gives only the army's divisions; their units are from his Craonne return two days "
           "before, and Marmont's from his return of the VI Corps on 12 March.")
LA_VI_NOTE = ("After Nafziger's return of Marmont's corps on 12 March, two days after Laon and the rout at Athies, from the "
              "French archives.")


def at_laon(f, id_, summary):
    notes = [LA_NOTE if n == CR_NOTE else n for n in f["notes"]]
    return again(f, id_, summary, notes)


LA_MEUNIER = at_laon(CR_MEUNIER, "laon-meunier",
    "Ney's first Young Guard division, under eight hundred men after Craonne, in the attacks on the hill of Laon from the "
    "south-west on the 9th and 10th.")
LA_CURIAL = at_laon(CR_CURIAL, "laon-curial",
    "Ney's second Young Guard division, about a thousand men, in the attacks on the hill of Laon.")
LA_BOYER_DE_REBEVAL = at_laon(CR_BOYER_DE_REBEVAL, "laon-boyer-de-rebeval",
    "The division of Victor's corps, now without Victor, in the attacks on Laon from the south-west.")
LA_CHARPENTIER = at_laon(CR_CHARPENTIER, "laon-charpentier",
    "Victor's Young Guard, with the main army in the attacks on the hill of Laon on the 9th and 10th.")
LA_ROUSSEL = at_laon(CR_ROUSSEL, "laon-roussel",
    "Grouchy's dragoons from Spain, with the main army before Laon.")
LA_LAFERRIERE = at_laon(CR_LAFERRIERE, "laon-laferriere",
    "The Guard's third cavalry division, now without Laferrière, who had been wounded at Craonne.")
LA_FRIANT = at_laon(CR_FRIANT, "laon-friant",
    "The Old Guard, in Mortier's reserve before Laon.")
LA_COLBERT = at_laon(CR_COLBERT, "laon-colbert",
    "The Guard horse with Mortier's reserve before Laon.")
LA_PAC = at_laon(CR_PAC, "laon-pac",
    "Nansouty's horse, with the main army before Laon.")

LA_CHRISTIANI = force(
    "laon-christiani", FIG, "Christiani's Division", "2nd Old Guard Division, Mortier's reserve", "French",
    "The Guard's fusiliers, flanqueurs and vélites, held back at Craonne, with Mortier's reserve before Laon.",
    [bde("fig-young-guard-brigade", "Fusilier Brigade",
         regiments=[og("Fusilier-Chasseurs", "fig-fusilier-chasseurs"), og("Fusilier-Grenadiers", "fig-fusilier-grenadiers")]),
     bde("fig-young-guard-brigade", "Gros's Brigade", "Gén. de Division Gros",
         regiments=[og("Flanqueurs-Chasseurs", "fig-yg-tirailleurs"), og("Flanqueurs-Grenadiers", "fig-yg-tirailleurs")]),
     bde("fig-italian-brigade", "Vélites", units=[u("fig-velites-turin", "Vélites of Turin"), u("fig-velites-florence", "Vélites of Florence")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Christiani")],
    notes=[LIST_FIG, LA_NOTE,
           "The division had 3,300 men at Craonne. Nafziger gives its regiments without their battalions; each has two here, "
           "as at Montmirail.",
           "Nafziger brigades the fusiliers together, each with a vélite battalion, and the flanqueurs with Gros; the vélites are "
           "the list's Italian brigade here. The Flanqueurs-Chasseurs and Flanqueurs-Grenadiers are the list's Tirailleurs.",
           "A fusilier brigade with no Young Guard regiment, which the list's brigade wants, shows as a historical departure."])
LA_CHRISTIANI["missing"] = [{"name": "25/3rd Foot Artillery and 2/7th Horse Artillery",
                             "reason": "Line artillery companies with the division, which the Guard list can't take."}]

LA_PORET = force(
    "laon-poret-de-morvan", FIG, "Poret de Morvan's Division", "Tirailleur Division, Young Guard, Mortier's reserve", "French",
    "A division of Young Guard tirailleurs, newly come up and held back at Craonne, with Mortier's reserve before Laon.",
    [bde("fig-young-guard-brigade", "Poret de Morvan's First Brigade", regiments=[yg("2nd Tirailleurs"), yg("3rd Tirailleurs")]),
     bde("fig-young-guard-brigade", "Poret de Morvan's Second Brigade", regiments=[yg("4th Tirailleurs"), yg("12th Voltigeurs")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Poret de Morvan")],
    notes=[LIST_FIG, LA_NOTE, NEW_YG,
           "The division had 4,800 men in eight battalions. Nafziger gives it without brigades; its regiments are split "
           "between two here, in his order. He gives it no guns."])

LA_RICARD = force(
    "laon-ricard", FR, "Ricard's Division", "8th Division, VI Corps (Marmont)", "French",
    "Marmont's division on the Berry-au-Bac road, which came up to Athies on the 9th. In the night Yorck's and Kleist's "
    "Prussians fell on Marmont's bivouacs and routed the corps, taking forty-five guns; Fabvier's men and an Old Guard "
    "escort kept the road back open.",
    [bde("fr-infantry-brigade", "Ricard's Light Battalions",
         regiments=[one("fr-light-infantry", "2nd Léger"), one("fr-light-infantry", "4th Léger"), bn("fr-light-infantry", "3/9th Léger"),
                    bn("fr-light-infantry", "2/16th Léger")]),
     bde("fr-infantry-brigade", "Ricard's Line Battalions",
         regiments=[one("fr-line-infantry", "136th Line"), one("fr-line-infantry", "138th Line"), one("fr-line-infantry", "144th Line")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Ricard")],
    notes=[LIST_FR, LA_VI_NOTE,
           "After Athies the division had about 650 men in seven battalions, fifty to a hundred and sixty each. They are shown at "
           "full size; the list's Small upgrade would suit them all.",
           "Nafziger gives the battalions without brigades; they are split here, light and line, as the list takes them.",
           "A brigade of four light battalions, where the list takes three regiments and one light regiment in the division, "
           "shows as a historical departure."])

LA_LAGRANGE = again(
    CH_LAGRANGE, "laon-lagrange",
    "Marmont's other division, with Ricard's at Athies when the Prussians fell on the corps in the night of the 9th; Marmont "
    "lost forty-five guns and the corps fell back in disorder.",
    [LIST_FR, LA_VI_NOTE, MARINES] + CH_LAGRANGE["notes"][3:5] +
    ["After Athies the division had about 1,400 men in twenty-one battalions; they are shown at full size, and the list's "
     "Small upgrade would suit them all.",
     "Nafziger gives Marmont's artillery on this return only as a foot and a horse company of January; the batteries here "
     "are those of the 25 January return. Clavel's four regiments, where the list's brigade takes three, show as a historical "
     "departure."])
brigade_of(LA_LAGRANGE, "Lefol's Brigade")["regiments"].append(one("fr-line-infantry", "132nd Line"))
LA_LAGRANGE["missing"] = [{"name": "The rest of Marmont's guns", "reason": "Forty-five of them were lost at Athies."}]

LA_ARRIGHI = force(
    "laon-arrighi", FR, "Arrighi's Command", "Paris Reserve division and provisional cavalry, with Marmont", "French",
    "Depot battalions from Paris and the provisional horse of the I Cavalry Corps, which marched with Marmont to Athies and "
    "were swept up in the night rout.",
    [bde("fr-infantry-brigade", "Arrighi's First Brigade",
         regiments=[bn("fr-line-infantry", "3/65th Line"), bn("fr-line-infantry", "4/66th Line"), bn("fr-line-infantry", "2/70th Line"),
                    bn_list("fr-line-infantry", "85th Line", ["2", "4", "6"])]),
     bde("fr-infantry-brigade", "Arrighi's Second Brigade",
         regiments=[bn_list("fr-line-infantry", "43rd Line", ["3", "4"]), bn_list("fr-line-infantry", "50th Line", ["2", "4"]),
                    bn("fr-line-infantry", "4/7th Line"), bn("fr-line-infantry", "3/88th Line")]),
     bde("fr-light-cavalry-brigade", "Provisional Cavalry Brigade",
         units=[u("fr-hussar-regt", "1st Provisional Regiment"), u("fr-chasseur-a-cheval", "2nd Provisional Regiment"),
                u("fr-chasseur-a-cheval", "3rd Provisional Regiment"), u("fr-chasseur-a-cheval", "4th Provisional Regiment")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Arrighi")],
    notes=[LIST_FR, LA_VI_NOTE,
           "Nafziger's Laon return gives Arrighi the I Cavalry Corps and the 2nd Paris Reserve Division; his 12 March return "
           "calls it the 1st Division of the Paris Reserve, with a provisional cavalry brigade of the I Cavalry Corps.",
           "The division had about 1,800 men in twelve battalions, and the cavalry about 1,600 in four provisional regiments. "
           "Nafziger gives the infantry without brigades; it is split between two here, in his order.",
           "The provisional regiments are as at La Rothière, a hussar regiment and three of chasseurs, made up from the squadrons "
           "left at the depots of many regiments.",
           "Brigades of four regiments, where the list's take three, show as historical departures."])

LAON = fought("laon", [LA_FR, CR_FR, LA_VI, wiki("Battle of Laon", "Battle_of_Laon")],
    [LA_MEUNIER, LA_CURIAL, LA_BOYER_DE_REBEVAL, LA_CHARPENTIER, LA_ROUSSEL, LA_LAFERRIERE, LA_FRIANT, LA_CHRISTIANI,
     LA_PORET, LA_COLBERT, LA_PAC, LA_RICARD, LA_LAGRANGE, LA_ARRIGHI], [
    fr("Pierre Boyer's Division", "Ney's corps", "About 1,900 men at Craonne, whose battalions Nafziger couldn't identify."),
    pr("Bülow's Corps", "III Corps, Army of the North", "Held Laon itself."),
    pr("Yorck's and Kleist's Corps", "I and II Corps, Army of Silesia",
       "Held the eastern wing, and routed Marmont at Athies in the night of the 9th."),
    ru("Winzingerode's Corps", "Army of the North", "Covered Blücher's western wing."),
    ru("Langeron's and Sacken's Corps", "Army of Silesia", "In reserve.")],
    alliances=(("Prussian", "Russian"),))

# ---------------------------------------------------------------- Reims, 13 March 1814, written

RE_AISNE = {"label": "French Army under Napoleon on the Aisne, 17 March 1814 (Nafziger Collection 814CAE)", "url": NAF + "814CAE.pdf"}
RE_NOTE = ("Nafziger has no order of battle for Reims. Marmont's infantry is from his VI Corps return of 12 March, the day "
           "before; Bordesoulle's cavalry from his return of the army on the Aisne of 17 March; and the Guard and Defrance's "
           "Gardes d'Honneur, which marched with Napoleon, from his returns for Craonne and Montmirail.")


def at_reims(f, id_, summary, extra=()):
    keep = [n for n in f["notes"][2:] if n not in (LA_NOTE, LA_VI_NOTE, CR_NOTE, MM_NOTE)]
    return again(f, id_, summary, [f["notes"][0], RE_NOTE] + list(extra) + keep)


RE_RICARD = at_reims(LA_RICARD, "reims-ricard",
    "Marmont's leading infantry, which crossed the ravine of La Muire and took the heights of Sainte-Geneviève before the "
    "town; Pelleport's brigade overwhelmed the Prussian Landwehr in the cemetery at Ormes. Its attack on the Soissons gate "
    "failed until the Guard's guns blew it in.",
    ["On Nafziger's return of 17 March the division had 940 men, in Pelleport's and Clavel's brigades; its battalions here "
     "are those of 12 March."])
RE_LAGRANGE = at_reims(LA_LAGRANGE, "reims-lagrange",
    "Marmont's other division, which followed Ricard's on the road from Berry-au-Bac and joined the attack on the town.",
    ["On Nafziger's return of 17 March the division had 2,060 men, in Joubert's and Fournier's brigades; its battalions here "
     "are those of 12 March, as its brigades are of February."])
RE_ARRIGHI = at_reims(LA_ARRIGHI, "reims-arrighi",
    "Arrighi's depot battalions from Paris, which marched on Reims with Marmont's corps.",
    ["On Nafziger's return of 17 March the infantry had 2,080 men, in Lucotte's brigade and another; its battalions here "
     "are those of 12 March."])
RE_ARRIGHI["brigades"] = [b for b in RE_ARRIGHI["brigades"] if b["type"] != "fr-light-cavalry-brigade"]
RE_ARRIGHI["notes"] = [n for n in RE_ARRIGHI["notes"] if "provisional regiments are" not in n and "I Cavalry Corps" not in n
                      and "four provisional regiments" not in n] + [
    "On 12 March the division had about 1,800 men in twelve battalions. Nafziger gives them without brigades; they are split "
    "between two here, in his order, the first under Lucotte as on his return of 17 March. The provisional cavalry Nafziger "
    "gives Arrighi at Laon is with Bordesoulle's here."]
RE_ARRIGHI["notes"] = RE_ARRIGHI["notes"][:-2] + RE_ARRIGHI["notes"][-1:] + RE_ARRIGHI["notes"][-2:-1]
brigade_of(RE_ARRIGHI, "Arrighi's First Brigade").update(name="Lucotte's Brigade", commander={"name": "Gén. de Brigade Lucotte"})
RE_ARRIGHI["name"], RE_ARRIGHI["formation"] = "Arrighi's Division", "Paris Reserve division, with Marmont"

RE_BORDESOULLE = again(
    CH_BORDESOULLE, "reims-bordesoulle",
    "The cavalry of Marmont's column, which caught the Prussian horse at Rosnay on the way to Reims; Merlin's division led "
    "the thrust towards Bezannes as the infantry attacked the town.",
    [LIST_FR, RE_NOTE,
     "Merlin's light division is the first two brigades, Bordesoulle's own heavy division Thiry's and Laville's.",
     CH_DEPOTS,
     "On 17 March each of these detachments had fifty to a hundred and twenty men, about 2,400 in all; they are shown at full "
     "size, and the list's Small upgrade would suit them all.",
     "Two heavy cavalry brigades, where the list takes one, and cuirassiers and dragoons in one brigade show as "
     "historical departures.", CAV_ONLY])
brigade_of(RE_BORDESOULLE, "Guyon's Brigade").update(name="Latour-Foissac's Brigade", commander={"name": "Gén. de Brigade Latour-Foissac"})
brigade_of(RE_BORDESOULLE, "Wathier's Brigade").pop("commander", None)
brigade_of(RE_BORDESOULLE, "Wathier's Brigade")["name"] = "Merlin's Hussars and Chevau-légers"
RE_BORDESOULLE["missing"] = []

RE_DEFRANCE = at_reims(MM_DEFRANCE, "reims-defrance",
    "The Gardes d'Honneur, which led the assault on the town with Ricard's division; Piquet's brigade cut down the "
    "Prussians at Ormes, and Ségur's, with the 3rd Gardes d'Honneur, was trapped in the streets and largely destroyed.")
RE_COLBERT = at_reims(CR_COLBERT, "reims-colbert",
    "The Guard horse under Sébastiani, which advanced on Ricard's flanks as the infantry went in.")
RE_FRIANT = at_reims(CR_FRIANT, "reims-friant",
    "The Old Guard, marched from Soissons, which reached Reims at four in the afternoon and was held in reserve.")
RE_BOYER_DE_REBEVAL = at_reims(CR_BOYER_DE_REBEVAL, "reims-boyer-de-rebeval",
    "The division that had been Victor's, held in reserve with Friant's Old Guard.")

REIMS = fought("reims", [LA_VI, RE_AISNE, CR_FR, MM_FR, wiki("Battle of Reims (1814)", "Battle_of_Reims_(1814)")],
    [RE_RICARD, RE_LAGRANGE, RE_ARRIGHI, RE_BORDESOULLE, RE_DEFRANCE, RE_COLBERT, RE_FRIANT, RE_BOYER_DE_REBEVAL], [
    fr("Exelmans's Division", "Guard cavalry, under Sébastiani",
       "Advanced on Ricard's flanks with Colbert's, crossed the Vesle by the bridging train and led the pursuit; Nafziger "
       "doesn't identify its regiments."),
    fr("Ney's Infantry", "Ney's corps", "Reached Reims before four in the afternoon; no return of it for March has been found."),
    ru("Saint-Priest's Corps", "Gurgalov's 11th and Pillar's 17th Divisions, with Emmanuel's dragoons, VIII Infantry Corps",
       "About eight thousand men, who had taken Reims the day before. Saint-Priest was mortally wounded by a shell, and the corps "
       "fell back through the town in disorder."),
    pr("Jagow's Brigade", "Pomeranian, Kurmark and Neumark Landwehr",
       "About five thousand men, surprised and broken at Gueux, Muizon and Thillois.")],
    alliances=(("Russian", "Prussian"),))

LIMONEST = armies("limonest", [wiki("Battle of Limonest", "Battle_of_Limonest")], [
    fr("Musnier's Division", "1st Division, Army of the Rhône (Augereau)", "Withdrew when the Austrians got behind it."),
    fr("Pannetier's Division", "2nd Division, Army of the Rhône",
       "Held Dardilly, and gave it up when its flank was turned, losing its six guns."),
    fr("Bardet's Division", "3rd Division, Army of the Rhône", "On the east bank of the Saône; it covered the retreat."),
    fr("Digeon's Division", "Cavalry Division, Army of the Rhône",
       "The army's cavalry, with infantry besides, covering Grange-Blanche and the withdrawal."),
    fr("Rémond's Reserve", "Army of the Rhône", "National Guards, three and a half thousand with nine guns."),
    at("Bianchi's Column", "Army of the South",
       "Advanced to La Tour-de-Salvagny; Wied-Runkel's division attacked Pannetier's and drove back Beurmann's brigade."),
    at("Wimpffen's Column", "Army of the South",
       "Pressed on Limonest; Mumb's brigade took the heights, Mont Thoux among them."),
    at("Hardegg's Column", "Army of the South", "On the east bank of the Saône; its hussars charged near Caluire and were driven off."),
    at("Hesse-Homburg's Reserve", "Army of the South", "Hessians and Austrians, moving up from Les Chères to Dommartin.")])

ARCIS = armies("arcis-sur-aube", [wiki("Battle of Arcis-sur-Aube", "Battle_of_Arcis-sur-Aube")], [
    fr("Ney's Infantry", "Friant's Old Guard, Henrion's Provisional Guard, Janssens's and Boyer's divisions",
       "Held Arcis and Torcy against Wrede's attacks; Janssens was wounded on the first day."),
    fr("Sébastiani's Cavalry", "Colbert's, Lefebvre-Desnouettes's and Letort's Guard divisions, Defrance's Gardes d'Honneur, and Exelmans's and Berckheim's divisions",
       "Fought the allied horse on the plain: Kaisarov's Cossacks drove back Colbert and Exelmans on the 20th, and on the 21st Sébastiani struck Pahlen's cavalry."),
    fr("Oudinot's Corps", "Leval's division of the VII Corps, with Saint-Germain's II Cavalry Corps",
       "Came up for the second day and covered the crossing back over the Aube; Leval was wounded in the retreat."),
    bav("Wrede's Corps", "Bavarian and Austrian divisions with Choglokov's Russian grenadiers, V Corps, Army of Bohemia",
        "Attacked Torcy-le-Grand again and again on the 20th."),
    at("Gyulai's Corps", "III Corps, Army of Bohemia", "Crenneville's and Fresnel's divisions and Nostitz's cavalry."),
    wt("The Crown Prince of Württemberg's Corps", "IV Corps, with Duka's Russian cuirassiers",
       "Took part in the second day's attack."),
    ru("Raevsky's Corps", "Gorchakov's and Eugen of Württemberg's infantry corps and Pahlen's cavalry, VI Corps",
       "Pahlen's cavalry was struck by Sébastiani's on the 21st."),
    ru("Barclay's Reserve and the Russian Guard", "Grenadiers, cuirassiers and the Guard infantry and cavalry",
       "With Kaisarov's and Seslavin's Cossacks, who drove back Colbert's and Exelmans's horse on the 20th."),
    pr("The Prussian Guard", "Alvensleben's infantry and LaRoche's cavalry", "In the allied reserve.")],
    alliances=(("Bavarian", "Austrian", "Württemberg", "Russian", "Prussian"),))

FERE_CHAMPENOISE = armies("fere-champenoise", [wiki("Battle of Fère-Champenoise", "Battle_of_F%C3%A8re-Champenoise")], [
    fr("Marmont's Corps", "Ricard's, Lagrange's and Arrighi's divisions, with Bordesoulle's and Merlin's cavalry",
       "Caught on the open plain by the allied cavalry marching on Paris, and driven back with heavy loss; Bordesoulle's horse was routed."),
    fr("Mortier's Corps", "Christiani's, Curial's and Charpentier's Guard divisions, with Roussel d'Hurbal's and Ghigny's cavalry",
       "Fell back beside Marmont's under the allied charges; Belliard's horse pushed Pahlen's aside."),
    fr("Pacthod's National Guards", "Pacthod's and Amey's divisions",
       "About five thousand eight hundred men and sixteen guns, escorting a convoy, who formed squares and fought on until surrounded; "
       "Pacthod, Amey and their brigadiers were taken."),
    ru("The Russian Guard Cavalry", "Grand Duke Constantine",
       "The Guard cuirassiers and light cavalry, with Depreradovich's 1st Cuirassier Division, which made the decisive charge."),
    ru("Pahlen's Cavalry", "VI Corps, Army of Bohemia", "Some three thousand five hundred horse, with Ilovaisky's Cossacks and Kretov's 2nd Cuirassier Division."),
    ru("Korff's and Vasilchikov's Cavalry", "Army of Silesia", "The cavalry of Langeron's and Sacken's corps, with Seslavin's Cossacks."),
    at("Nostitz's Cuirassiers", "Austrian Cuirassier Division", "About three thousand seven hundred, with Desfours's brigade."),
    wt("The Crown Prince of Württemberg's Cavalry", "Prince Adam of Württemberg", "About two thousand horse of the IV Corps.")],
    alliances=(("Russian", "Austrian", "Württemberg"),))

SAINT_DIZIER = armies("saint-dizier", [wiki("Battle of Saint-Dizier", "Battle_of_Saint-Dizier")], [
    fr("Napoleon's Army", "Napoleon, with Macdonald",
       "Turned back on the allies' communications; its cavalry, ten thousand or more, crossed the Marne and drove Winzingerode's "
       "horse away, taking eighteen guns."),
    ru("Winzingerode's Cavalry", "Army of the North",
       "Some eight to ten thousand men, mostly cavalry, left to screen the allies' march on Paris. Driven out of Saint-Dizier, "
       "it fell back on Bar-le-Duc that evening."),
    ru("Tettenborn's Advance Guard", "Hussars and Cossacks",
       "About a thousand horse, which charged the massed French cavalry and got away to Vitry.")])

# ---------------------------------------------------------------- Paris, 30 March 1814, written

PA_FR = {"label": "French Army, Battle of Paris, 30 March 1814 (Nafziger Collection 814CAG)", "url": NAF + "814CAG.pdf"}
PA_NOTE = ("After Nafziger's order of battle for Paris at seven in the morning of the 30th, from Koch's and Rapetti's "
           "histories and the French archives; most of its strengths are of early April.")
PA_TINY = ("Its battalions had a few dozen to a couple of hundred men each; they are shown at full size, and the list's Small "
           "upgrade would suit them all.")


def pa(f, id_, summary, notes):
    return again(f, id_, summary, [f["notes"][0], PA_NOTE] + notes)


PA_ARRIGHI = force(
    "paris-arrighi", FR, "Arrighi's Division", "VI Corps (Marmont), right wing", "French",
    "Lucotte's brigade of depot and veteran battalions, which held Montreuil and covered Bagnolet on the Malassise plateau "
    "on Marmont's right; the Russians took Montreuil and Bagnolet as the day went on.",
    [bde("fr-infantry-brigade", "Lucotte's Brigade", "Gén. de Brigade Lucotte",
         regiments=[one("fr-line-infantry", "1st Veteran Battalion"), one("fr-line-infantry", "2nd Veteran Battalion"),
                    bn("fr-line-infantry", "2/45th Line"), bn("fr-line-infantry", "2/50th Line"), bn("fr-line-infantry", "1/65th Line"),
                    bn("fr-line-infantry", "1/66th Line"), bn("fr-line-infantry", "1/72nd Line"), bn("fr-line-infantry", "3/85th Line"),
                    bn("fr-line-infantry", "1/88th Line")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Arrighi")],
    notes=[LIST_FR, PA_NOTE,
           "The brigade had 1,250 men. The 1st Veteran Battalion had over six hundred; the other battalions a few dozen to a "
           "hundred and sixty. They are shown at full size, and the list's Small upgrade would suit most of them.",
           "The veteran battalions are shown as Line.",
           "Nine battalions in one brigade, where the list's takes three regiments, show as a historical departure."])

PA_RICARD = force(
    "paris-ricard", FR, "Ricard's Division", "8th Division, VI Corps (Marmont)", "French",
    "Marmont's reserve, massed by battalions before the Tourelles ridge behind the line from Romainville to Belleville.",
    [bde("fr-infantry-brigade", "Pelleport's Brigade", "Gén. de Brigade Pelleport",
         regiments=[one("fr-light-infantry", "6th Léger"), one("fr-line-infantry", "4th Line"), one("fr-line-infantry", "6th Line"),
                    one("fr-line-infantry", "136th Line")]),
     bde("fr-infantry-brigade", "Clavel's Brigade", "Gén. de Brigade Clavel",
         regiments=[one("fr-light-infantry", "19th Léger"), one("fr-line-infantry", "138th Line"), one("fr-line-infantry", "144th Line")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Ricard")],
    notes=[LIST_FR, PA_NOTE,
           "The division had 726 men in seven battalions. " + PA_TINY,
           "Nafziger lists the 6th Léger in both brigades; it is shown once, with Pelleport's.",
           "A brigade of four regiments, where the list's takes three, and two light regiments, where it allows one in the "
           "division, show as historical departures."])

PA_LAGRANGE = force(
    "paris-lagrange", FR, "Lagrange's Division", "3rd Division, VI Corps (Marmont)", "French",
    "Marmont's centre, its two brigades either side of the road from Belleville to Romainville, holding the heights against "
    "Raevsky's Russians until Marmont asked for terms in the afternoon.",
    [bde("fr-infantry-brigade", "Fournier's Brigade", "Gén. de Brigade Fournier",
         regiments=[one("fr-line-infantry", "1st Line"), one("fr-line-infantry", "62nd Line"), one("fr-line-infantry", "132nd Line"),
                    marine("1st Marine Regiment", 2), marine("2nd Marine Regiment", 4), marine("3rd Marine Regiment", 3),
                    marine("4th Marine Regiment", 3)]),
     bde("fr-infantry-brigade", "Joubert's Brigade", "Gén. de Brigade Joubert",
         regiments=[one("fr-light-infantry", "23rd Léger"), one("fr-light-infantry", "37th Léger"), one("fr-line-infantry", "15th Line"),
                    one("fr-line-infantry", "16th Line"), one("fr-line-infantry", "70th Line"), one("fr-line-infantry", "121st Line")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Lagrange")],
    notes=[LIST_FR, PA_NOTE, MARINES,
           "The division had 1,395 men. " + PA_TINY,
           "Nafziger gives the regiments without their battalions; the marine regiments' are those of his 12 March return, and "
           "the others are one battalion each.",
           "Brigades of seven and six regiments, where the list's take three, fifteen battalions in Fournier's, where it takes "
           "ten, and two light regiments, where it allows one in the division, show as historical departures. Nafziger gives "
           "the division no guns."])

PA_BORDESOULLE = again(
    CH_BORDESOULLE, "paris-bordesoulle",
    "The remnant of the I Cavalry Corps, in a second line behind the road to Montreuil on Marmont's right.",
    [LIST_FR, PA_NOTE,
     "Merlin's light division, 850 men, is Hubert's and Foissac-Latour's brigades; Bordesoulle's heavy division, 895 men, "
     "Thiry's and Laville's. Their strengths are of 5 April.",
     CH_DEPOTS,
     "Each detachment had a few dozen men, the 8th Chasseurs and 4th Cuirassiers over a hundred; they are shown at full "
     "size, and the list's Small upgrade would suit them all.",
     "Two heavy cavalry brigades, where the list takes one, cuirassiers and dragoons in one brigade, and more heavy "
     "cavalry than its half of the army for corps support, show as historical departures. Nafziger gives the corps no guns.",
     CAV_ONLY])
PA_BORDESOULLE["brigades"] = [
    bde("fr-light-cavalry-brigade", "Hubert's Brigade", "Gén. de Brigade Hubert",
        units=[u("fr-hussar-regt", "Hussar detachments (6th, 7th and 8th Hussars)"),
               u("fr-lancer", "Chevau-léger detachments (1st, 3rd, 5th and 7th Chevau-légers)")]),
    bde("fr-light-cavalry-brigade", "Foissac-Latour's Brigade", "Gén. de Brigade Foissac-Latour",
        units=[u("fr-chasseur-a-cheval", "Chasseur detachments (1st, 3rd and 8th Chasseurs)"),
               u("fr-chasseur-a-cheval", "Chasseur detachments (9th and 16th Chasseurs)")]),
    bde("fr-heavy-cavalry-brigade", "Thiry's Brigade", "Gén. de Brigade Thiry",
        units=[u("fr-cuirassier", "Cuirassier detachments (2nd, 3rd and 6th Cuirassiers)"),
               u("fr-cuirassier", "Cuirassier detachments (9th, 11th and 12th Cuirassiers)")]),
    bde("fr-heavy-cavalry-brigade", "Laville's Brigade", "Gén. de Brigade Laville",
        units=[u("fr-cuirassier", "Cuirassier detachments (4th, 7th and 14th Cuirassiers)"),
               u("fr-dragoon", "Dragoon detachments (7th, 23rd, 28th and 30th Dragoons)")])]
PA_BORDESOULLE["missing"] = []

PA_BOYER_DE_REBEVAL = force(
    "paris-boyer-de-rebeval", FR, "Boyer de Rébeval's Division", "Provisional Corps (Compans)", "French",
    "Part deployed and part massed before the village of Pré-Saint-Gervais, on the left of Marmont's line, where the "
    "allied attacks on the plain came in.",
    [bde("fr-infantry-brigade", "Guye's Brigade", "Gén. de Brigade Guye",
         regiments=[bn_list("fr-light-infantry", "19th Léger", ["2", "6"]), bn("fr-line-infantry", "3/5th Line"), bn("fr-line-infantry", "3/11th Line")]),
     bde("fr-infantry-brigade", "Boyer de Rébeval's Second Brigade",
         regiments=[bn("fr-line-infantry", "7/107th Line"), bn_list("fr-line-infantry", "Garde Nationale du Nord", ["1", "2"])]),
     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "6/1st Foot Artillery")]),
     bde("fr-artillery-brigade", "Attached Artillery", units=[u("fr-foot-arty", "19/2nd Foot Artillery"), u("fr-foot-arty", "20/5th Foot Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Boyer de Rébeval")],
    notes=[LIST_FR, PA_NOTE,
           "Guye's brigade had 1,850 men. The National Guards of the Nord are shown as Line.",
           "Its three foot batteries are one in its divisional artillery and two in its reserve, as the list takes them; with "
           "seven battalions, where the list wants eight for each reserve battery, the two show as a historical departure.",
           "This is a different division from the one Nafziger gives Boyer de Rébeval at Craonne."])

PA_CHARPENTIER = force(
    "paris-charpentier", FIG, "Charpentier's Division", "7th Young Guard Division, Guard Corps (Mortier)", "French",
    "Mortier's reserve on the left, massed at the foot of the Chaumont ridge behind the line from Pantin to La Villette.",
    [bde("fig-young-guard-brigade", "Charpentier's First Brigade",
         regiments=[regt(f"{n} Voltigeurs", [u("fig-yg-voltigeurs", f"{n} Voltigeurs")]) for n in ("1st", "2nd", "3rd", "4th", "5th", "7th")]),
     bde("fig-young-guard-brigade", "Le Capitaine's Brigade", "Gén. de Brigade Le Capitaine",
         regiments=[regt(f"{n} Voltigeurs", [u("fig-yg-voltigeurs", f"{n} Voltigeurs")]) for n in ("10th", "11th", "14th", "15th")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Charpentier")],
    notes=[LIST_FIG, PA_NOTE, NEW_YG,
           "The division had 1,500 men, the regiments seventy-five to two hundred and seventy each; each is shown as one "
           "battalion at full size, and the list's Small upgrade would suit them all.",
           "Nafziger names the first brigade's commander as Lagrange, from a return of 15 April; it is shown here without him.",
           "Brigades of six and four regiments, where the list's take three, show as historical departures."])
PA_CHARPENTIER["missing"] = [{"name": "Cadres of the 12th and 13th Voltigeurs", "reason": "Thirty men or so each, too few for units of their own."}]

PA_CURIAL = force(
    "paris-curial", FIG, "Curial's Division", "2nd Young Guard Division, Guard Corps (Mortier)", "French",
    "Bigarré's brigade, massed in reserve behind Pantin, ready to support Sécrétant's Guard depot battalions holding the village.",
    [bde("fig-young-guard-brigade", "Bigarré's Brigade", "Gén. de Brigade Bigarré",
         regiments=[regt("5th Voltigeurs", [u("fig-yg-voltigeurs", "5th Voltigeurs")]), regt("6th Voltigeurs", [u("fig-yg-voltigeurs", "6th Voltigeurs")]),
                    regt("7th Voltigeurs", [u("fig-yg-voltigeurs", "7th Voltigeurs")]),
                    regt("Converged 8th Voltigeurs", [u("fig-yg-voltigeurs", "4th Voltigeurs"), u("fig-yg-voltigeurs", "8th Voltigeurs")]),
                    regt("Third and Second Battalions", [u("fig-yg-voltigeurs", "3/3rd Voltigeurs"), u("fig-yg-voltigeurs", "3/14th Voltigeurs"),
                                                          u("fig-yg-voltigeurs", "2/11th Voltigeurs")]),
                    regt("9th Tirailleurs", [u("fig-yg-tirailleurs", "9th Tirailleurs")])])],
    command=[cmd("fig-div-cmd", "Gén. de Division Curial")],
    notes=[LIST_FIG, PA_NOTE, NEW_YG,
           "Bigarré's brigade had 1,820 men. The third and second battalions of other regiments that served in it are grouped "
           "as one regiment here; each unit is shown at full size.",
           "Six regiments in one brigade, where the list's takes three, and one of three battalions, where it takes two, show "
           "as historical departures."])

PA_CHRISTIANI = again(
    LA_CHRISTIANI, "paris-christiani",
    "Gros's brigade of the Guard's fusiliers, flanqueurs and vélites, massed in reserve between La Villette and La Chapelle "
    "to support Robert's Guard depot battalions.",
    [LIST_FIG, PA_NOTE,
     "The brigade had 1,630 men. Nafziger gives all six of its corps in one brigade under Gros; they are brigaded here as at "
     "Laon, the fusiliers and the flanqueurs, with the vélites as the list's Italian brigade. Each regiment has two battalions, "
     "as at Montmirail.",
     "The Flanqueurs-Chasseurs and Flanqueurs-Grenadiers are the list's Tirailleurs.",
     "A fusilier brigade with no Young Guard regiment, which the list's brigade wants, shows as a historical departure."])

PA_ROUSSEL = pa(CR_ROUSSEL, "paris-roussel",
    "Belliard's dragoons on Mortier's far left, out on the plain between the road to Saint-Denis and the Maillot gate.",
    ["The division had 1,900 men, with two march regiments besides.",
     "Its two horse batteries are one in its divisional artillery and one in its reserve, as the list takes them.",
     "Two heavy cavalry brigades, where the list takes one, more heavy cavalry than its half of the army for corps support, "
     "and a cavalry force with no infantry, show as historical departures. Play it alongside infantry, or agree it with your "
     "opponent."])
PA_ROUSSEL["missing"] = [{"name": "Two march regiments", "reason": "Regiments of drafts with Rigaud's brigade, whose make-up isn't known."}]

PARIS = fought("paris", [PA_FR, wiki("Battle of Paris (1814)", "Battle_of_Paris_(1814)")],
    [PA_ARRIGHI, PA_RICARD, PA_LAGRANGE, PA_BORDESOULLE, PA_BOYER_DE_REBEVAL, PA_CHARPENTIER, PA_CURIAL, PA_CHRISTIANI, PA_ROUSSEL], [
    fr("Compans's and Ledru des Essarts's Divisions", "Provisional Corps (Compans)",
       "Chabert's brigade, 2,200 men, in skirmish order in the Romainville woods, and Bongars's, 1,600, on the Beauregard ridge; "
       "Nafziger doesn't know their battalions."),
    fr("Chastel's Cavalry", "Provisional Cavalry Corps (Compans)",
       "Vincent's brigade, 1,600 horse, in line between Charonne and Montreuil; its regiments aren't known."),
    fr("Michel's Guard Depots", "Mortier's wing",
       "Four thousand men from the Guard's depots, Sécrétant's brigade behind Pantin and Robert's before Aubervilliers."),
    fr("Belliard's Other Cavalry and Ornano's", "Cavalry Corps (Belliard)",
       "Ghigny's, Christophe's and Leclerc's brigades, along the old entrenchments between the road to Saint-Denis and the "
       "Maillot gate, and Dautencourt's 320 Guard horse on the far left; their regiments aren't known."),
    fr("Moncey's National Guard", "Paris Guard (Marshal Moncey)",
       "Some six thousand National Guards on the heights from Montmartre round to the Bercy, with 780 gunners of veteran "
       "battalions and the École Polytechnique on the city walls, and naval gunners serving the batteries at Pré-Saint-Gervais."),
    ru("Raevsky's Corps", "VI Corps, Army of Bohemia", "Took Montreuil."),
    ru("The Russian Guard and Reserve", "Barclay de Tolly", "Yermolov's Guard came up late; the Russians took Bagnolet and Charonne."),
    ru("Langeron's and Vorontsov's Corps", "Army of Silesia", "Came on by Le Bourget on Blücher's wing."),
    pr("Yorck's and Kleist's Corps", "I and II Corps, Army of Silesia", "Took La Villette, Kleist's corps storming La Chapelle."),
    pr("The Prussian Guard", "Army of Bohemia", "Thrown back at Pantin, then took the French guns there."),
    wt("The Crown Prince of Württemberg's Corps", "IV Corps, with the Austrian grenadiers",
       "Took the bridges of Saint-Maur and Charenton, and Saint-Mandé."),
    at("Gyulai's Corps", "III Corps, Army of Bohemia", "Sent against the forest of Vincennes.")],
    alliances=(("Russian", "Prussian", "Württemberg", "Austrian"),))

ARMIES_TO_COME = (CHAMPAUBERT, MONTMIRAIL, CHATEAU_THIERRY, VAUCHAMPS, MORMANT, MONTEREAU, BAR_SUR_AUBE, LAUBRESSEL, CRAONNE,
                  LAON, REIMS, LIMONEST, ARCIS, FERE_CHAMPENOISE, SAINT_DIZIER, PARIS)


# ================================================================ The allies of La Rothière, Laubressel and Bar-sur-Aube

RO_AL = {"label": "Battle of La Rothière order of battle: the Coalition army (Wikipedia, after Nafziger)",
         "url": "https://en.wikipedia.org/wiki/Battle_of_La_Rothi%C3%A8re_order_of_battle"}
RO_AL_NOTE = "After Wikipedia's order of battle for La Rothière, from Nafziger's history of the campaign."
LIST_AU14 = "Built from A Clash of Eagles' Austrian 1812 list, the nearest to 1814."
LIST_BAV14 = "Built from A Clash of Eagles' Bavarian 1812 list, the nearest to 1814; Bavaria had joined the allies in October."
LIST_WT14 = "Built from A Clash of Eagles' Württemberg 1812 list, the nearest to 1814; Württemberg had joined the allies in November."
LW_BAV = ("The Landwehr battalions, national field battalions raised from the districts' militia, are shown as Line. Brigades "
          "of single battalions of several regiments have more regiments than the list's brigade takes, which shows as a "
          "historical departure.")
BAV_ARTY = ("Each division's cavalry battery, light 6-pdrs with the gunners riding, is the list's Light Artillery, with its "
            "chevau-légers; its 6-pdr battery is its Foot Battery, and one of the corps' four 12-pdr batteries is with each "
            "division as its Position Battery.")


def ru_again(f, id_, summary, notes):
    g = again(f, id_, summary, notes)
    return g


RO_LIEVEN = ru_again(MM_LIEVEN, "la-rothiere-lieven",
    "Sacken's left column, eight thousand infantry, which came on at four against La Rothière with the bayonet, its muskets "
    "wet with snow, and drove Duhesme's men out of the village.",
    [LIST_RU, RO_AL_NOTE] + MM_LIEVEN["notes"][2:])
RO_SHCHERBATOV = ru_again(MM_TALYZIN, "la-rothiere-shcherbatov",
    "Sacken's right column, beside Lieven's in the attack on La Rothière.",
    [LIST_RU, RO_AL_NOTE, "Talyzin's 7th Division (the first three brigades) and Bernodessov's 18th (the last three)."] + MM_TALYZIN["notes"][3:])
RO_SHCHERBATOV["name"], RO_SHCHERBATOV["command"] = "Shcherbatov's Corps", [cmd("ru-div-cmd", "Gen-Lt Prince Shcherbatov")]
RO_OLSUFIEV = ru_again(CH_OLSUFIEV, "la-rothiere-olsufiev",
    "Five thousand infantry following Sacken's columns, which threw Rottembourg's first brigade out of La Rothière in the evening.",
    [LIST_RU, RO_AL_NOTE] + CH_OLSUFIEV["notes"][2:])
RO_OLSUFIEV["missing"] = []
RO_VASILCHIKOV = ru_again(MM_VASILCHIKOV, "la-rothiere-vasilchikov",
    "Sacken's horse. Lanskoy's hussars were driven off by Nansouty's Guard cavalry, but Panchulidzev's dragoons, coming up, "
    "broke the French horsemen as they reached the Russian infantry and took twenty-four of the Guard's horse guns.",
    [LIST_RU, RO_AL_NOTE] + MM_VASILCHIKOV["notes"][2:])
RO_KARPOV = ru_again(MM_KARPOV, "la-rothiere-karpov",
    "Sacken's Cossacks, which with Biron's Prussians covered the gap between Sacken's corps and the Württembergers.",
    [LIST_RU, RO_AL_NOTE] + MM_KARPOV["notes"][2:])

RO_PASKEVICH = force(
    "la-rothiere-paskevich", RU, "Paskevich's Grenadiers", "2nd Grenadier Division, Raevsky's Grenadier Corps", "Russian",
    "The one division of Barclay's reserve that reached the fight, sent with Grimmer's Austrians to help drive Rottembourg's "
    "Young Guard out of La Rothière at the last.",
    [bde("ru-grenadier-brigade", "Pisarev's Brigade", "Maj-Gen Pisarev",
         regiments=[ru_regt("Kiev Grenadiers", 2, "ru-grenadier"), ru_regt("Moscow Grenadiers", 2, "ru-grenadier")]),
     bde("ru-grenadier-brigade", "Damas's Brigade", "Maj-Gen Damas",
         regiments=[ru_regt("Astrakhan Grenadiers", 1, "ru-grenadier"), ru_regt("Fanagoria Grenadiers", 1, "ru-grenadier")]),
     bde("ru-grenadier-brigade", "Paskevich's Third Brigade",
         regiments=[ru_regt("Siberia Grenadiers", 2, "ru-grenadier"), ru_regt("Little Russia Grenadiers", 2, "ru-grenadier"),
                    ru_regt("Emperor Grenadiers", 1, "ru-grenadier")])],
    command=[cmd("ru-div-cmd", "Maj-Gen Paskevich")],
    notes=[LIST_RU, RO_AL_NOTE,
           "The order of battle doesn't name the third brigade's commander.",
           "Three grenadier brigades, where the list allows one, three regiments in one of them, where it takes two, and "
           "grenadiers with no infantry brigade to allow them, show as historical departures.",
           "The corps' three batteries are left out: the order of battle gives them to Raevsky's corps as a whole."])

RO_GYULAI = force(
    "la-rothiere-gyulai", AU, "Gyulai's Corps", "III Corps, Army of Bohemia", "Austrian",
    "Twelve thousand Austrian infantry on the allied left, which came into action only at four. Fresnel's division crossed "
    "the Aube to attack Dienville and its bridge from the west bank and was thrown back, and Hohenlohe's attacked from the "
    "east bank and was repulsed; Gyulai's 12-pdrs bombarded the village, and Grimmer's brigade was sent to help at La "
    "Rothière. The Austrians only took Dienville at midnight, after Gérard had gone.",
    [bde("at-advanced-guard-brigade", "Haecht's Brigade", "Gen-Maj Haecht",
         units=[u("at-grenz", "I/St George Grenz (IR 6)"), u("at-chevauleger", "Klenau Chevau-légers (7 squadrons)"), u("at-cavalry-arty", "Cavalry Battery")]),
     bde("at-advanced-guard-brigade", "Trenck's Brigade", "Gen-Maj Trenck",
         units=[u("at-grenz", "II/St George Grenz (IR 6)"), u("at-dragoon", "Rosenberg Dragoons (6 squadrons)")]),
     bde("at-line-infantry-brigade", "Pflüger's Brigade", "Gen-Maj Pflüger",
         units=[u("at-6pdr-brigade-battery", "6-pdr Brigade Battery")],
         regiments=[regt("Archduke Ludwig Infantry (IR 8)", bns("at-infantry-german", "Archduke Ludwig", 4)),
                    regt("Würzburg Infantry (IR 7)", bns("at-infantry-german", "Würzburg", 3))]),
     bde("at-line-infantry-brigade", "Csollich's Brigade", "Gen-Maj Csollich",
         units=[u("at-6pdr-brigade-battery", "6-pdr Brigade Battery")],
         regiments=[regt("Kottulinsky Infantry (IR 41)", bns("at-infantry-german", "Kottulinsky", 3)),
                    regt("Kaiser Infantry (IR 1)", bns("at-infantry-german", "Kaiser", 2))]),
     bde("at-line-infantry-brigade", "Splény's Brigade", "Gen-Maj Splény",
         units=[u("at-6pdr-brigade-battery", "6-pdr Brigade Battery")],
         regiments=[regt("Mariassy Infantry (IR 37)", bns("at-infantry-hungarian", "Mariassy", 2)),
                    regt("Ignaz Gyulai Infantry (IR 60)", bns("at-infantry-hungarian", "Ignaz Gyulai", 2))]),
     bde("at-line-infantry-brigade", "Grimmer's Brigade", "Gen-Maj Grimmer",
         units=[u("at-6pdr-brigade-battery", "6-pdr Brigade Battery")],
         regiments=[regt("Kollowrat Infantry (IR 36)", bns("at-infantry-german", "Kollowrat", 2)),
                    regt("Frölich Infantry (IR 28)", bns("at-infantry-german", "Frölich", 3))]),
     bde("at-reserve-artillery", "Corps Artillery", units=[u("at-position-battery", "12-pdr Position Battery"), u("at-position-battery", "6-pdr Position Battery")])],
    command=[cmd("at-inf-div-cmd", "FZM Gyulai")],
    notes=[LIST_AU14, RO_AL_NOTE,
           "Crenneville's light division is Haecht's and Trenck's brigades, Fresnel's Pflüger's and Csollich's, and Prince Hohenlohe's "
           "Splény's and Grimmer's. The St George Grenz regiment's two battalions are one with each of Crenneville's brigades.",
           "The Mariassy and Ignaz Gyulai regiments, recruited in Hungary, are the list's Hungarian infantry.",
           "Regiments of three and four battalions, where the list takes two Large ones, two advanced guard brigades, where it "
           "allows one, and four brigade batteries and two position batteries, where it allows three and one, show as "
           "historical departures."])
RO_GYULAI["missing"] = [{"name": "A second 6-pdr Position Battery", "reason": "The corps' third reserve battery, more than the list takes."}]

RO_WURTTEMBERG = force(
    "la-rothiere-wurttemberg", WT, "The Crown Prince of Württemberg's Corps", "IV Corps, Army of Bohemia", "Württemberg",
    "Twelve thousand infantry and 2,500 horse on the allied right, which took the Beaulieu wood and La Giberie, lost it to "
    "Victor's infantry and took it again at five, with Petit-Mesnil soon after.",
    [bde("wt-light-infantry-brigade", "Stockmayer's Brigade", "Gen-Maj von Stockmayer",
         units=[u("wt-light-infantry", "I/9th (King's) Jäger"), u("wt-light-infantry", "II/9th (King's) Jäger"), u("wt-light-infantry", "10th Light")]),
     bde("wt-infantry-brigade", "Döring's Brigade", "Gen-Maj von Döring",
         regiments=[regt("2nd Line (Duke Wilhelm)", bns("wt-line-infantry", "2nd Line", 2)), regt("3rd Line", bns("wt-line-infantry", "3rd Line", 2)),
                    regt("7th Line", bns("wt-line-infantry", "7th Line", 2))]),
     bde("wt-infantry-brigade", "Hohenlohe-Kirchberg's Brigade", "Gen-Maj Prince Hohenlohe-Kirchberg",
         regiments=[regt("4th Line", bns("wt-line-infantry", "4th Line", 2)), regt("6th Line", bns("wt-line-infantry", "6th Line", 2))]),
     bde("wt-cavalry-brigade", "Alvensleben's Brigade", "Gen-Maj von Alvensleben",
         units=[u("wt-jager-cavalry", "2nd Jäger zu Pferde (Duke Louis)"), u("wt-chevauleger", "3rd Dragoons (Crown Prince)"),
                u("wt-horse-arty", "1st Horse Battery")]),
     bde("wt-cavalry-brigade", "Jett's Brigade", "Gen-Maj von Jett",
         units=[u("wt-jager-cavalry", "4th Jäger zu Pferde (Prince Adam)"), u("wt-horse-arty", "2nd Horse Battery")]),
     bde("wt-divisional-artillery", "Divisional Artillery",
         units=[u("wt-light-arty", "1st Foot Battery"), u("wt-light-arty", "2nd Foot Battery")])],
    command=[cmd("wt-div-cmd", "Crown Prince of Württemberg")],
    notes=[LIST_WT14, RO_AL_NOTE,
           "Koch's infantry division is the three infantry brigades, Prince Adam's cavalry division the two cavalry brigades.",
           "The horse chasseur regiments are the list's Jäger zu Pferde, and the Crown Prince's dragoons its Chevau-légers.",
           "Each foot battery, four 6-pdrs and two howitzers, is the list's Light Artillery.",
           "Two cavalry brigades, where the list allows one for the infantry, three regiments in Döring's brigade and three light "
           "battalions in Stockmayer's, where the list's take two, and two foot batteries, where it allows one, show as "
           "historical departures."])

RO_WREDE_AU = force(
    "la-rothiere-wrede-austrians", AU, "Wrede's Austrians", "Hardegg's and Splény's divisions, V Corps (Wrede)", "Austrian",
    "The Austrian half of Wrede's corps on the extreme allied right. Its horse got past the French squares about seven in the "
    "evening and took twenty-one guns.",
    [bde("at-advanced-guard-brigade", "Geramb's Brigade", "Col Geramb",
         units=[u("at-grenz", "I/1st Szekler Grenz (IR 14)"), u("at-grenz", "II/1st Szekler Grenz (IR 14)"),
                u("at-hussar", "Archduke Joseph Hussars (6 squadrons)"), u("at-cavalry-arty", "Cavalry Battery")]),
     bde("at-advanced-guard-brigade", "Mengen's Brigade", "Col Mengen",
         units=[u("at-jager", "3rd Jäger Battalion"), u("at-uhlan", "Schwarzenberg Uhlans (6 squadrons)")]),
     bde("at-line-infantry-brigade", "Splény's Infantry",
         regiments=[regt("Jordis Infantry (IR 59)", bns("at-infantry-german", "Jordis", 4)),
                    regt("Archduke Rudolph Infantry (IR 14)", bns("at-infantry-german", "Archduke Rudolph", 4))]),
     bde("at-light-cavalry-brigade", "Minutillo's Brigade", "Gen-Maj Minutillo",
         units=[u("at-hussar", "Szekler Hussars (6 squadrons)"), u("at-dragoon", "Knesevich Dragoons (6 squadrons)"), u("at-cavalry-arty", "Cavalry Battery")]),
     bde("at-reserve-artillery", "Reserve Artillery (Stwrtnik)", units=[u("at-position-battery", "12-pdr Position Battery"), u("at-position-battery", "6-pdr Position Battery")])],
    command=[cmd("at-inf-div-cmd", "FML Count Hardegg")],
    notes=[LIST_AU14, RO_AL_NOTE,
           "Hardegg's 1st Division is Geramb's and Mengen's brigades, and Splény's 2nd Division the infantry, whose brigadier "
           "isn't known, and Minutillo's cavalry. They were the same regiments as at Hanau.",
           "Regiments of four battalions, where the list takes two Large ones, one line brigade where the list wants two for "
           "the force's points, two advanced guard brigades, where it allows one, a cavalry battery with Minutillo's two "
           "regiments, where it wants three, and two position batteries with eight line battalions, show as historical "
           "departures."])

def bav_bn(name):
    return regt(name, [u("bav-line-infantry", name)])


RO_RECHBERG = force(
    "la-rothiere-rechberg", BAV, "Rechberg's Division", "1st Bavarian Division, V Corps (Wrede)", "Bavarian",
    "Wrede's leading division, with his corps as it reached La Chaise at two, cleared Marmont's men out of the Bois d'Ajou "
    "at four, and took Chaumesnil and held it against Meunier's Young Guard.",
    [bde("bav-infantry-brigade", "Prince Karl's Brigade", "Gen-Maj Prince Karl of Bavaria",
         units=[u("bav-light-infantry", "3rd Light Battalion")],
         regiments=[regt("1st Line", bns("bav-line-infantry", "1st Line", 2)), bav_bn("I/3rd Line"), bav_bn("I/Oberdonau Landwehr")]),
     bde("bav-infantry-brigade", "Maillot's Brigade", "Gen-Maj Maillot de la Treille",
         units=[u("bav-light-infantry", "2nd Light Battalion")],
         regiments=[bav_bn("III/1st Line"), bav_bn("I/2nd Line"), bav_bn("II/Oberdonau Landwehr")]),
     bde("bav-cavalry-brigade", "Vieregg's Brigade", "Gen-Maj von Vieregg",
         units=[u("bav-chevau-leger", "1st Chevau-légers"), u("bav-chevau-leger", "2nd Chevau-légers"), u("bav-chevau-leger", "7th Chevau-légers"),
                u("bav-light-arty", "Cavalry Battery")]),
     bde("bav-divisional-artillery", "Divisional Artillery", units=[u("bav-foot-arty", "6-pdr Battery"), u("bav-position-battery", "12-pdr Battery")])],
    command=[cmd("bav-div-cmd", "Gen-Lt von Rechberg")],
    notes=[LIST_BAV14, RO_AL_NOTE, LW_BAV, BAV_ARTY,
           "The 1st Line's battalion in Maillot's brigade is unnumbered in the order of battle; it is shown as the third. Three "
           "chevau-léger regiments in Vieregg's brigade, where the list's takes two, show as a historical departure."])

RO_BECKERS = force(
    "la-rothiere-beckers", BAV, "Beckers's Division", "2nd Bavarian Division, V Corps (Wrede)", "Bavarian",
    "Wrede's second division, following Rechberg's against Chaumesnil on the extreme right of the allied line.",
    [bde("bav-infantry-brigade", "Pappenheim's Brigade", "Gen-Maj Graf Pappenheim",
         units=[u("bav-light-infantry", "4th Light Battalion")],
         regiments=[regt("4th Line", bns("bav-line-infantry", "4th Line", 2)), bav_bn("Salzach Landwehr"), bav_bn("I/Regen Landwehr")]),
     bde("bav-infantry-brigade", "Zoller's Brigade", "Gen-Maj Freiherr von Zoller",
         units=[u("bav-light-infantry", "1st Light Battalion")],
         regiments=[regt("6th Line", bns("bav-line-infantry", "6th Line", 2)), bav_bn("I/Rezat Landwehr")]),
     bde("bav-cavalry-brigade", "Elbracht's Brigade", "Gen-Maj von Elbracht",
         units=[u("bav-chevau-leger", "3rd Chevau-légers"), u("bav-chevau-leger", "6th Chevau-légers"), u("bav-light-arty", "Cavalry Battery")]),
     bde("bav-divisional-artillery", "Divisional Artillery", units=[u("bav-foot-arty", "6-pdr Battery"), u("bav-position-battery", "12-pdr Battery")])],
    command=[cmd("bav-div-cmd", "Gen-Lt Beckers zu Westerstetten")],
    notes=[LIST_BAV14, RO_AL_NOTE, LW_BAV, BAV_ARTY])

RO_LAMOTTE = force(
    "la-rothiere-lamotte", BAV, "Lamotte's Division", "3rd Bavarian Division, V Corps (Wrede)", "Bavarian",
    "Wrede's third division, with his corps on the extreme allied right; in the dark the Bavarian and Württemberg horse "
    "charged each other by mistake, which stopped the pursuit.",
    [bde("bav-infantry-brigade", "Habermann's Brigade", "Gen-Maj von Habermann",
         regiments=[regt("11th Line", bns("bav-line-infantry", "11th Line", 2)), bav_bn("I/7th Line"), bav_bn("I/Unterdonau Landwehr"),
                    bav_bn("I/Iller Landwehr")]),
     bde("bav-infantry-brigade", "Deroy's Brigade", "Gen-Maj von Deroy",
         regiments=[bav_bn("I/5th Line"), bav_bn("I/8th Line"), bav_bn("I/9th Line"), bav_bn("II/Iller Landwehr"), bav_bn("I/Isar Landwehr")]),
     bde("bav-cavalry-brigade", "Lamotte's Cavalry",
         units=[u("bav-chevau-leger", "4th Chevau-légers"), u("bav-chevau-leger", "5th Chevau-légers"), u("bav-light-arty", "Cavalry Battery")]),
     bde("bav-divisional-artillery", "Divisional Artillery", units=[u("bav-foot-arty", "6-pdr Battery"), u("bav-position-battery", "12-pdr Battery")])],
    command=[cmd("bav-div-cmd", "Gen-Lt Freiherr von Lamotte")],
    notes=[LIST_BAV14, RO_AL_NOTE, LW_BAV, BAV_ARTY,
           "The order of battle is unsure of the cavalry brigade's commander, naming Elbracht with a query; it is shown without him."])
RO_LAMOTTE["missing"] = [{"name": "The fourth 12-pdr battery", "reason": "One of the corps' four, more than one to each division."}]

RO_BIRON = force(
    "la-rothiere-biron", PR15, "Biron's Cavalry", "Prussian detachment, with Sacken", "Prussian",
    "A small Prussian brigade which, with Karpov's Cossacks, covered the gap between Sacken's corps and the Württembergers.",
    [pc("Biron's Brigade", "Gen-Maj Prince Biron of Courland",
        [u("pr15-hussar", "2nd Silesian Hussars (2 squadrons)"), u("pr15-hussar", "Silesian National Cavalry (2 squadrons)"),
         u("pr15-dragoon", "Neumark Dragoons (1 squadron)")])],
    command=[cmd("pr15-corps-cmd", "Gen-Maj Prince Biron of Courland")],
    notes=[PR_LIST, RO_AL_NOTE,
           "Five squadrons in all, with a detachment of Cossacks; each regiment's squadrons are shown as one unit. The Silesian "
           "National Cavalry, a volunteer regiment, is shown as Hussars, the list's cavalry brigade taking no Landwehr.",
           "A cavalry brigade with no infantry brigade shows as a historical departure."])

LA_ROTHIERE["forces"] += [RO_LIEVEN, RO_SHCHERBATOV, RO_OLSUFIEV, RO_VASILCHIKOV, RO_KARPOV, RO_PASKEVICH, RO_GYULAI,
                          RO_WURTTEMBERG, RO_WREDE_AU, RO_RECHBERG, RO_BECKERS, RO_LAMOTTE, RO_BIRON]
LA_ROTHIERE["sources"].append(RO_AL)
LA_ROTHIERE["toCome"] = [ru("Barclay's Other Reserves", "Choglokov's 1st Grenadier Division and Golitsyn's cuirassiers, Russian Reserve",
                            "Marched back and forth through the day without coming into action.")]
LA_ROTHIERE["alliances"] = [["Russian", "Austrian", "Württemberg", "Bavarian", "Prussian"]]

# --- Laubressel and Bar-sur-Aube: the corps of La Rothière, a month on

LB_AL_NOTE = ("After Wikipedia's order of battle for La Rothière, a month before; Laubressel's own order of battle gives the "
              "allied corps only by division.")


def a_month_on(f, id_, summary, note=LB_AL_NOTE):
    return again(f, id_, summary, [f["notes"][0], note] + f["notes"][2:])


LB_GYULAI = a_month_on(RO_GYULAI, "laubressel-gyulai",
    "Gyulai's Austrians, about ten thousand, on the allied left, which attacked the French at Silvarouvres.")
LB_WURTTEMBERG = a_month_on(RO_WURTTEMBERG, "laubressel-wurttemberg",
    "About fifteen thousand Württembergers on the allied left: Prince Adam's cavalry stood idle, and Koch's and Döring's "
    "infantry followed Macdonald towards Sens.")
LB_WREDE = [a_month_on(f, f["id"].replace("la-rothiere", "laubressel"), summ) for f, summ in (
    (RO_WREDE_AU, "Hardegg's Austrians, who led Wrede's corps towards Montiéramey while its guns opened the attack."),
    (RO_RECHBERG, "Rechberg's Bavarians, who attacked towards Courteranges and Troyes."),
    (RO_BECKERS, "Beckers's Bavarians, with the rest of Wrede's corps in the advance on Troyes."),
    (RO_LAMOTTE, "Lamotte's Bavarians, with the rest of Wrede's corps in the advance on Troyes."))]
LAUBRESSEL["forces"] += LB_WREDE + [LB_WURTTEMBERG, LB_GYULAI]
LAUBRESSEL["sources"].append(RO_AL)
LAUBRESSEL["toCome"] = [t for t in LAUBRESSEL["toCome"] if t["side"] in ("French", "Russian")]

BA_AL_NOTE = ("After Wikipedia's order of battle for La Rothière, four weeks before; Bar-sur-Aube's account names Wrede's "
              "corps but gives none of its own.")
BA_WREDE = [a_month_on(f, f["id"].replace("la-rothiere", "bar-sur-aube"), summ, BA_AL_NOTE) for f, summ in (
    (RO_WREDE_AU, "Wrede's Austrians, who came on against Oudinot beside Wittgenstein's Russians."),
    (RO_RECHBERG, "Wrede's leading Bavarian division in the attack on Oudinot's position."),
    (RO_BECKERS, "Wrede's second Bavarian division in the attack on Oudinot's position."),
    (RO_LAMOTTE, "Wrede's third Bavarian division in the attack on Oudinot's position."))]
BAR_SUR_AUBE["forces"] += BA_WREDE
BAR_SUR_AUBE["sources"].append(RO_AL)
BAR_SUR_AUBE["toCome"] = [t for t in BAR_SUR_AUBE["toCome"] if t["side"] == "Russian"]
BAR_SUR_AUBE["alliances"] = [["Russian", "Bavarian", "Austrian"]]


# ================================================================ Arcis-sur-Aube, 20–21 March 1814, written

AR_BAV = {"label": "Bavarian Army Corps, Battle of Arcis-sur-Aube, 20–21 March 1814 (Nafziger Collection 814CAA)", "url": NAF + "814CAA.pdf"}
AR_FR15 = {"label": "French Army, 15 March 1814 (Nafziger Collection 814CZD)", "url": NAF + "814CZD.pdf"}
AR_NOTE = ("Nafziger has no French order of battle for Arcis. The divisions Wikipedia's account names are built from his "
           "nearest returns: the Guard's of February and March, and Oudinot's of early March.")
AR_AL_NOTE = ("After Wikipedia's order of battle for La Rothière, seven weeks before; Arcis's own order of battle gives the "
              "allied corps only by division.")
AR_BAV_NOTE = "After Nafziger's order of battle for Wrede's Bavarians at Arcis, from the Bavarian war archives."


def at_arcis(f, id_, summary, note=AR_NOTE, extra=()):
    return again(f, id_, summary, [f["notes"][0], note] + list(extra) + f["notes"][2:])


AR_FRIANT = at_arcis(MM_FRIANT, "arcis-friant",
    "The Old Guard under Ney, which held the town of Arcis and the bridge behind it through the two days, and covered the "
    "crossing back over the Aube.")
AR_HENRION = force(
    "arcis-henrion", FIG, "Henrion's Division", "2nd Young Guard Division, under Ney", "French",
    "The Young Guard under Ney, which held Torcy and the ground before Arcis against Wrede's attacks on the 20th.",
    [bde("fig-young-guard-brigade", "Henrion's Voltigeurs", units=[u("fig-yg-foot-arty", "10th Young Guard Foot Company")],
         regiments=[regt("8th Voltigeurs", [u("fig-yg-voltigeurs", "8th Voltigeurs")]), yg("9th Voltigeurs")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Henrion")],
    notes=[LIST_FIG, "After Nafziger's return of the army on 15 March, five days before.", NEW_YG,
           "On 15 March the 8th Voltigeurs had 165 men and the 9th nearly seven hundred, shown as one and two battalions. "
           "Wikipedia's account gives Henrion a provisional Guard division of 4,500 to 5,500 men; the rest of it isn't known.",
           "Its foot company, with three battalions where the list wants six for one, shows as a historical departure."])
AR_HENRION["missing"] = [{"name": "Régiment de Marche", "reason": "A march regiment of about five hundred drafts, whose make-up isn't known."}]
AR_COLBERT = at_arcis(MM_COLBERT, "arcis-colbert",
    "The Guard horse under Sébastiani, out on the plain before Arcis; on the 20th Kaisarov's Cossacks drove it back with "
    "Exelmans's.")
AR_LEFEBVRE = at_arcis(MM_LEFEBVRE, "arcis-lefebvre-desnouettes",
    "The largest of the Guard cavalry divisions, some two thousand men, with Sébastiani on the plain before Arcis.")
AR_LETORT = at_arcis(MM_LAFERRIERE, "arcis-letort",
    "The Guard's third cavalry division, now Letort's, with Sébastiani on the plain; Curély's brigade covered its pontoon train.")
AR_LETORT["name"], AR_LETORT["command"] = "Letort's Guard Cavalry", [cmd("fig-div-cmd", "Gén. de Division Letort")]
AR_DEFRANCE = at_arcis(MM_DEFRANCE, "arcis-defrance",
    "The Gardes d'Honneur, with Sébastiani's cavalry on the plain before Arcis.")
AR_LEVAL = at_arcis(LB_LEVAL, "arcis-leval",
    "Oudinot's strongest division, which came up for the second day and covered the crossing back over the Aube; Leval was "
    "wounded in the retreat.")
AR_ROTTEMBOURG = at_arcis(LB_ROTTEMBOURG, "arcis-rottembourg",
    "Oudinot's Young Guard, which came up for the second day with Leval's.")
AR_ST_GERMAIN = at_arcis(LB_ST_GERMAIN, "arcis-saint-germain",
    "Oudinot's cavalry, Maurin's and Delort's divisions, which came up for the second day and struck Pahlen's horse with "
    "Sébastiani's.")

def bav_regt(name, *bns_):
    return regt(name, [u("bav-line-infantry", b) for b in bns_])


AR_RECHBERG = force(
    "arcis-rechberg", BAV, "Rechberg's Division", "1st Bavarian Division, V Corps (Wrede)", "Bavarian",
    "Wrede's leading Bavarians, which attacked Torcy-le-Grand again and again on the 20th, Prince Karl of Bavaria leading "
    "a brigade, without taking it.",
    [bde("bav-infantry-brigade", "Prince Karl's Brigade", "Gen-Maj Prince Karl of Bavaria",
         units=[u("bav-light-infantry", "3rd Jäger Battalion")],
         regiments=[bav_regt("1st Line", "I/1st Line", "II/1st Line"), bav_regt("3rd Line", "I/3rd Line"), bav_regt("10th National Field Battalion", "10th National Field Battalion")]),
     bde("bav-infantry-brigade", "Spreti's Brigade", "Gen-Maj Graf Spreti",
         regiments=[bav_regt("2nd Line", "II/2nd Line"), bav_regt("10th Line", "I/10th Line"),
                    bav_regt("National Field Battalions", "11th National Field Battalion", "15th National Field Battalion")]),
     bde("bav-cavalry-brigade", "Vieregg's Brigade", "Gen-Maj Freiherr von Vieregg",
         units=[u("bav-chevau-leger", "1st Chevau-légers (4 squadrons)"), u("bav-chevau-leger", "2nd Chevau-légers (4 squadrons)"),
                u("bav-chevau-leger", "7th Chevau-légers (3 squadrons)"), u("bav-light-arty", "4th Wurst Battery")]),
     bde("bav-divisional-artillery", "Divisional Artillery", units=[u("bav-foot-arty", "5th 6-pdr Foot Battery"), u("bav-position-battery", "3rd 12-pdr Foot Battery")])],
    command=[cmd("bav-div-cmd", "Gen-Lt von Rechberg")],
    notes=[LIST_BAV14, AR_BAV_NOTE,
           "The national field battalions, raised from the districts' militia, are shown as Line; the Wurst battery is the list's "
           "Light Artillery, with the chevau-légers.",
           "One of Ulmer's four 12-pdr batteries is with each division as its Position Battery.",
           "Three regiments in each brigade, where the list's takes two, and three chevau-léger regiments in Vieregg's, show as "
           "historical departures."])
AR_LAMOTTE = force(
    "arcis-lamotte", BAV, "Lamotte's Division", "3rd Bavarian Division, V Corps (Wrede)", "Bavarian",
    "Wrede's other Bavarian division, in the attacks on Torcy-le-Grand and the second day's advance on Arcis.",
    [bde("bav-infantry-brigade", "Stockh's Brigade", "Gen-Maj von der Stockh",
         regiments=[bav_regt("11th Line", "I/11th Line", "II/11th Line"), bav_regt("7th Line", "I/7th Line"),
                    bav_regt("Kreis Battalions", "1st Iller Kreis Battalion", "1st Unter-Donau Kreis Battalion")]),
     bde("bav-infantry-brigade", "Deroy's Brigade", "Gen-Maj von Deroy",
         regiments=[bav_regt("5th Line", "I/5th Line"), bav_regt("8th Line", "I/8th Line"), bav_regt("9th Line", "I/9th Line"),
                    bav_regt("National Field Battalions", "5th National Field Battalion", "6th National Field Battalion")]),
     bde("bav-cavalry-brigade", "Diez's Brigade", "Col Diez",
         units=[u("bav-chevau-leger", "4th Chevau-légers (3 squadrons)"), u("bav-chevau-leger", "5th Chevau-légers (3 squadrons)"),
                u("bav-light-arty", "1st Wurst Battery")]),
     bde("bav-divisional-artillery", "Divisional Artillery", units=[u("bav-foot-arty", "9th 6-pdr Foot Battery"), u("bav-position-battery", "8th 12-pdr Foot Battery")])],
    command=[cmd("bav-div-cmd", "Gen-Lt Freiherr von Lamotte")],
    notes=[LIST_BAV14, AR_BAV_NOTE,
           "The Kreis and national field battalions are shown as Line; the Wurst battery is the list's Light Artillery.",
           "One of Ulmer's four 12-pdr batteries is with each division as its Position Battery.",
           "Three and four regiments in a brigade, where the list's takes two, show as historical departures."])
AR_LAMOTTE["missing"] = [{"name": "The rest of Ulmer's reserve", "reason": "A mortar battery, a 6-pdr battery and two more 12-pdr batteries."}]

AR_WREDE_AU = at_arcis(RO_WREDE_AU, "arcis-wrede-austrians",
    "The Austrian divisions of Wrede's corps; Volkmann's brigade attacked Torcy-le-Grand three times on the 20th.", AR_AL_NOTE)
AR_GYULAI = at_arcis(RO_GYULAI, "arcis-gyulai",
    "Gyulai's Austrians, part of the allied army that closed on Arcis for the second day.", AR_AL_NOTE)
AR_WURTTEMBERG = at_arcis(RO_WURTTEMBERG, "arcis-wurttemberg",
    "The Württembergers, who joined the second day's attack, with Duka's Russian cuirassiers.", AR_AL_NOTE)
AR_CHOGLOKOV = force(
    "arcis-choglokov", RU, "Choglokov's Grenadiers", "1st Grenadier Division, with Wrede", "Russian",
    "A division of Russian grenadiers attached to Wrede's corps for the attacks on Torcy and Arcis.",
    [bde("ru-grenadier-brigade", "Knyazhnin's Brigade", "Maj-Gen Knyazhnin II",
         regiments=[ru_regt("Arakcheyev Grenadiers", 2, "ru-grenadier"), ru_regt("Ekaterinoslav Grenadiers", 2, "ru-grenadier")]),
     bde("ru-grenadier-brigade", "Yemelyanov's Brigade", "Col Yemelyanov",
         regiments=[ru_regt("Tauride Grenadiers", 1, "ru-grenadier"), ru_regt("St Petersburg Grenadiers", 2, "ru-grenadier")]),
     bde("ru-grenadier-brigade", "Sulima's Brigade", "Col Sulima",
         regiments=[ru_regt("Kexholm Grenadiers", 2, "ru-grenadier"), ru_regt("Pernau Grenadiers", 2, "ru-grenadier")])],
    command=[cmd("ru-div-cmd", "Maj-Gen Choglokov")],
    notes=[LIST_RU, AR_AL_NOTE,
           "Three grenadier brigades, where the list allows one, and grenadiers with no infantry brigade to allow them, show "
           "as historical departures."])

ARCIS.update(fought("arcis-sur-aube", [AR_FR15, MM_FR, CR_FR, TR_FR, AR_BAV, RO_AL, wiki("Battle of Arcis-sur-Aube", "Battle_of_Arcis-sur-Aube")],
    [AR_FRIANT, AR_HENRION, AR_COLBERT, AR_LEFEBVRE, AR_LETORT, AR_DEFRANCE, AR_LEVAL, AR_ROTTEMBOURG, AR_ST_GERMAIN,
     AR_RECHBERG, AR_LAMOTTE, AR_WREDE_AU, AR_CHOGLOKOV, AR_GYULAI, AR_WURTTEMBERG], [
    fr("Janssens's and Boyer's Divisions", "Ney's corps",
       "Two more divisions of Ney's in the fight for Arcis and Torcy; Janssens was wounded on the 20th and Lefol took his "
       "division. No return of them for March has been found."),
    fr("Exelmans's and Berckheim's Divisions", "Cavalry, under Sébastiani",
       "Two more of Sébastiani's cavalry divisions; Exelmans's was driven back with Colbert's by Kaisarov's Cossacks on the 20th. "
       "Their regiments aren't known."),
    ru("Raevsky's Corps", "Gorchakov's and Eugen of Württemberg's infantry corps and Pahlen's cavalry, VI Corps",
       "Pahlen's cavalry was struck by Sébastiani's on the 21st."),
    ru("Barclay's Reserve and the Russian Guard", "Grenadiers, cuirassiers and the Guard infantry and cavalry",
       "With Kaisarov's and Seslavin's Cossacks, who drove back Colbert's and Exelmans's horse on the 20th."),
    pr("The Prussian Guard", "Alvensleben's infantry and LaRoche's cavalry", "In the allied reserve.")],
    alliances=(("Bavarian", "Austrian", "Württemberg", "Russian", "Prussian"),)))


# ================================================================ Fère-Champenoise, 25 March 1814, written

FC_NOTE = ("Nafziger has no order of battle for Fère-Champenoise. Marmont's and Mortier's corps are from his return of the "
           "army on the Aisne on 17 March, eight days before, with Marmont's battalions from his 12 March return.")
FC_AL_NOTE = "After Wikipedia's order of battle for La Rothière; Fère-Champenoise's own gives the allied cavalry only by division."


def at_fere(f, id_, summary, note=FC_NOTE, extra=()):
    keep = [n for n in f["notes"][2:] if n not in (RE_NOTE, LA_NOTE, LA_VI_NOTE, CR_NOTE, MM_NOTE, PA_NOTE)]
    return again(f, id_, summary, [f["notes"][0], note] + list(extra) + keep)


def yg1(name, unit="fig-yg-voltigeurs"):
    return regt(name, [u(unit, name)])


FC_RICARD = at_fere(RE_RICARD, "fere-champenoise-ricard",
    "Marmont's division, caught with the rest of his corps on the open plain by the allied cavalry on its way to Paris, and "
    "driven back with heavy loss.")
FC_LAGRANGE = at_fere(RE_LAGRANGE, "fere-champenoise-lagrange",
    "Marmont's other division, driven back across the plain in squares under the allied cavalry's charges.")
FC_ARRIGHI = at_fere(RE_ARRIGHI, "fere-champenoise-arrighi",
    "Arrighi's division, Marmont's third, which fell back with the corps through the allied charges.")
FC_BORDESOULLE = at_fere(RE_BORDESOULLE, "fere-champenoise-bordesoulle",
    "Marmont's cavalry, Merlin's and Bordesoulle's divisions, which tried to stand against the allied horse and was routed.")

FC_CURIAL = force(
    "fere-champenoise-curial", FIG, "Curial's Division", "Young Guard Division, Mortier's corps", "French",
    "Mortier's Young Guard, which fell back beside Marmont's corps under the allied charges.",
    [bde("fig-young-guard-brigade", "Lagrange's Brigade", "Gén. de Brigade Lagrange",
         regiments=[yg1("1st Voltigeurs"), yg1("2nd Voltigeurs"), yg1("3rd Voltigeurs"), yg1("4th Voltigeurs"),
                    yg1("Converged Tirailleurs (13th and 14th)", "fig-yg-tirailleurs")]),
     bde("fig-young-guard-brigade", "Le Capitaine's Brigade", "Gén. de Brigade Le Capitaine",
         regiments=[yg1("2/14th Tirailleurs", "fig-yg-tirailleurs"), yg1("Converged Tirailleurs (11th and 14th)", "fig-yg-tirailleurs"),
                    yg1("Converged Tirailleurs (3rd, 4th and 10th)", "fig-yg-tirailleurs")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Curial")],
    notes=[LIST_FIG, FC_NOTE, NEW_YG,
           "The division had some 2,800 men. Its voltigeur regiments had a hundred to three hundred men each; the converged "
           "tirailleur battalions, made up from the remnants of several regiments, five hundred or so. Each is shown as one "
           "battalion at full size.",
           "On Nafziger's Paris return of 30 March these brigades are Charpentier's, and Charpentier's here are Curial's; each "
           "battle follows its own return.",
           "Lagrange's five regiments, where the list's brigade takes three, show as a historical departure."])

FC_CHARPENTIER = force(
    "fere-champenoise-charpentier", FIG, "Charpentier's Division", "Young Guard Division, Mortier's corps", "French",
    "Mortier's other Young Guard division, which fell back across the plain with the rest of the two marshals' corps.",
    [bde("fig-young-guard-brigade", "Jamin's Brigade", "Gén. de Brigade Jamin",
         regiments=[yg1("5th Voltigeurs"), yg1("6th Voltigeurs"), yg1("7th Voltigeurs"),
                    regt("Converged 8th Voltigeurs", [u("fig-yg-voltigeurs", "4th Voltigeurs"), u("fig-yg-voltigeurs", "8th Voltigeurs")])]),
     bde("fig-young-guard-brigade", "Bigarré's Brigade", "Gén. de Brigade Bigarré",
         regiments=[yg1("3/3rd Voltigeurs"), yg1("3/14th Voltigeurs"), yg1("2/11th Voltigeurs"), yg1("9th Tirailleurs", "fig-yg-tirailleurs")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Charpentier")],
    notes=[LIST_FIG, FC_NOTE, NEW_YG,
           "The division had some 2,750 men, its battalions a hundred and fifty to five hundred each; each is shown at full size.",
           "On Nafziger's Paris return of 30 March, Bigarré's brigade is Curial's; each battle follows its own return.",
           "Brigades of four regiments, where the list's take three, show as historical departures."])
FC_CHARPENTIER["missing"] = [{"name": "Artillery and sappers", "reason": "Six hundred gunners and train and 150 sappers, whose batteries Nafziger doesn't give."}]

FC_CHRISTIANI = at_fere(LA_CHRISTIANI, "fere-champenoise-christiani",
    "The Guard's fusiliers, flanqueurs and vélites, with Mortier's corps on the plain.",
    extra=["On 17 March the fusilier and flanqueur regiments had four to six hundred men each and the vélites a few dozen."])
FC_ROUSSEL = at_fere(CR_ROUSSEL, "fere-champenoise-roussel",
    "Mortier's cavalry, the dragoons from Spain, with Ghigny's horse; Belliard led the cavalry that pushed Pahlen's aside.",
    extra=["On 17 March its four regiments had three to five hundred men each."])
FC_ROUSSEL["missing"] = [{"name": "Two march regiments", "reason": "Drafts under Colonel Ghigny and another, whose make-up isn't known."}]

FC_VASILCHIKOV = at_fere(MM_VASILCHIKOV, "fere-champenoise-vasilchikov",
    "Sacken's hussars and dragoons, with the Army of Silesia's cavalry, which came on across the plain against the French squares.",
    FC_AL_NOTE.replace("La Rothière", "Montmirail and La Rothière"))
FC_KRETOV = force(
    "fere-champenoise-kretov", RU, "Kretov's Cuirassiers", "2nd Cuirassier Division, Russian Reserve", "Russian",
    "Russian cuirassiers, which with the Guard and the Austrian cuirassiers broke into Marmont's and Mortier's squares on "
    "the plain.",
    [bde("ru-heavy-cavalry-brigade", "Leontyev's Brigade", "Maj-Gen Leontyev",
         units=[u("ru-cuirassier", "Glukhov Cuirassiers (5 squadrons)"), u("ru-cuirassier", "Pskov Cuirassiers (5 squadrons)")]),
     bde("ru-heavy-cavalry-brigade", "Karatheff's Brigade", "Maj-Gen Karatheff",
         units=[u("ru-cuirassier", "Ekaterinoslav Cuirassiers (2 squadrons)"), u("ru-cuirassier", "Astrakhan Cuirassiers (4 squadrons)")])],
    command=[cmd("ru-div-cmd", "Gen-Lt Kretov")],
    notes=[LIST_RU, FC_AL_NOTE,
           "Wikipedia's order of battle gives the division 1,600 men and twelve guns at Fère-Champenoise; its battery isn't named.",
           "Two heavy cavalry brigades, where the list allows one, and cavalry with no infantry brigade to allow it, show as "
           "historical departures."])
FC_WURTTEMBERG_CAV = force(
    "fere-champenoise-wurttemberg", WT, "Prince Adam's Cavalry", "Cavalry Division, IV Corps (Württemberg)", "Württemberg",
    "The Crown Prince of Württemberg's horse, about two thousand, which rode with the allied cavalry against the French corps.",
    [b for b in copy.deepcopy(RO_WURTTEMBERG["brigades"]) if b["type"] == "wt-cavalry-brigade"],
    command=[cmd("wt-div-cmd", "Gen-Lt Prince Adam of Württemberg")],
    notes=[LIST_WT14, FC_AL_NOTE,
           "The horse chasseur regiments are the list's Jäger zu Pferde, and the Crown Prince's dragoons its Chevau-légers.",
           "Two cavalry brigades, and cavalry with no infantry brigade to allow it, show as historical departures."])

FERE_CHAMPENOISE.update(fought("fere-champenoise", [RE_AISNE, LA_VI, RO_AL, wiki("Battle of Fère-Champenoise", "Battle_of_F%C3%A8re-Champenoise")],
    [FC_RICARD, FC_LAGRANGE, FC_ARRIGHI, FC_BORDESOULLE, FC_CURIAL, FC_CHARPENTIER, FC_CHRISTIANI, FC_ROUSSEL,
     FC_VASILCHIKOV, FC_KRETOV, FC_WURTTEMBERG_CAV], [
    fr("Pacthod's National Guards", "Pacthod's and Amey's divisions",
       "About 5,800 men and sixteen guns, escorting a convoy, who formed squares and fought on until surrounded; Pacthod, "
       "Amey and their brigadiers were taken. No return of them for March has been found."),
    ru("The Russian Guard Cavalry", "Grand Duke Constantine",
       "The Guard cuirassiers and light cavalry, with Depreradovich's 1st Cuirassier Division, which made the decisive charge."),
    ru("Pahlen's Cavalry", "VI Corps, Army of Bohemia", "Some three thousand five hundred horse, with Ilovaisky's Cossacks."),
    ru("Korff's Cavalry and Seslavin's Cossacks", "Army of Silesia and Army of Bohemia",
       "The cavalry of Langeron's corps, with Seslavin's Don Cossacks."),
    at("Nostitz's Cuirassiers", "Austrian Cuirassier Division", "About three thousand seven hundred, with Desfours's brigade.")],
    alliances=(("Russian", "Austrian", "Württemberg"),)))


# ================================================================ The allies of Brienne and Mormant

BR_AL_NOTE = ("After Wikipedia's order of battle for La Rothière, three days later, which its page says may be used for "
              "Brienne too.")
MO_AL_NOTE = "After Wikipedia's order of battle for La Rothière, a fortnight before; Mormant's own gives the allies only by division."


def ally_at(f, id_, summary, note):
    return again(f, id_, summary, [f["notes"][0], note] + f["notes"][2:])


BR_OLSUFIEV = ally_at(RO_OLSUFIEV, "brienne-olsufiev",
    "About six thousand infantry, part of Langeron's corps, which held Brienne town through the afternoon and failed to "
    "retake the château at night.", BR_AL_NOTE)
BR_LIEVEN = ally_at(RO_LIEVEN, "brienne-lieven",
    "Half of Sacken's corps, recalled from Lesmont, which reached the field from mid-afternoon and drove the Young Guard out "
    "of most of the town that night.", BR_AL_NOTE)
BR_SHCHERBATOV = ally_at(RO_SHCHERBATOV, "brienne-shcherbatov",
    "The other half of Sacken's corps, which came up from Lesmont with Lieven's and joined the night fighting in the town.", BR_AL_NOTE)
BR_VASILCHIKOV = ally_at(RO_VASILCHIKOV, "brienne-vasilchikov",
    "Lanskoy's hussars and Panchulidzev's dragoons, which with Pahlen's squadrons, forty in all, rode down Duhesme's division "
    "and took eight of its guns.", BR_AL_NOTE)
BRIENNE["forces"] += [BR_OLSUFIEV, BR_LIEVEN, BR_SHCHERBATOV, BR_VASILCHIKOV]
BRIENNE["sources"].append(RO_AL)
BRIENNE["toCome"] = [t for t in BRIENNE["toCome"] if t["name"] == "Pahlen's Cavalry"]

MO_HARDEGG = ally_at(RO_WREDE_AU, "mormant-hardegg",
    "Hardegg's Austrians of Wrede's corps, which fell back through Nangis and were mauled at Valjouan.", MO_AL_NOTE)
MO_HARDEGG["name"], MO_HARDEGG["formation"] = "Hardegg's Division", "1st Austrian Division, V Corps (Wrede)"
MO_HARDEGG["brigades"] = [b for b in MO_HARDEGG["brigades"] if b["name"] in ("Geramb's Brigade", "Mengen's Brigade")]
MO_HARDEGG["notes"] = [n for n in MO_HARDEGG["notes"] if not n.startswith(("Hardegg's 1st Division", "Regiments of four"))] + [
    "The division is Geramb's and Mengen's brigades; Splény's division isn't named at Mormant.",
    "Two advanced guard brigades, where the list allows one, and Grenz battalions, with no line infantry brigade or "
    "battalions to allow them, show as historical departures."]
MO_LAMOTTE = ally_at(RO_LAMOTTE, "mormant-lamotte",
    "Lamotte's Bavarians of Wrede's corps, routed at Valjouan by Gérard's infantry and Bordesoulle's horse.", MO_AL_NOTE)
MORMANT["forces"] += [MO_HARDEGG, MO_LAMOTTE]
MORMANT["sources"].append(RO_AL)
MORMANT["toCome"] = [t for t in MORMANT["toCome"] if t["side"] in ("French", "Russian")]


# ================================================================ Craonne: Vorontsov's Russians

CR_RU = {"label": "Russian Forces, Battle of Craone, 7 March 1814 (Nafziger Collection 814CAC)", "url": NAF + "814CAC.pdf"}
CR_RU_NOTE = "After Nafziger's order of battle for the Russians at Craonne, from Koch's and Bogdanovich's histories."
CR_RU_BN = ("Its regiments had one or two battalions each, a few hundred men; each is shown at full size, and the list's "
            "Small upgrade would suit them.")

CR_VORONTSOV = force(
    "craonne-vorontsov", RU, "Vorontsov's First Line", "Vorontsov's corps, Army of Silesia", "Russian",
    "The first of Vorontsov's lines across the Chemin des Dames, with Benckendorff's horse on the right towards Paissy. "
    "Benckendorff charged Nansouty's cavalry and was overwhelmed; Krasovsky's Jäger held the farm of Heurtebise and then "
    "drew back, and the line gave ground only when ordered.",
    [bde("ru-light-cavalry-brigade", "Benckendorff's Detachment", "Maj-Gen Benckendorff",
         units=[u("ru-hussar", "Pavlograd Hussars (6 squadrons)"), u("ru-mounted-cossack", "Bug Cossacks")]),
     bde("ru-jager-brigade", "Krasovsky's Brigade", "Maj-Gen Krasovsky",
         units=[u("ru-position-arty", "Position Battery #31"), u("ru-light-arty", "Light Battery #21"), u("ru-light-arty", "Light Battery #26")],
         regiments=[ru_regt("14th Jäger", 1, "ru-jager"), ru_regt("15th Jäger", 1, "ru-jager")]),
     bde("ru-infantry-brigade", "Harpe's Brigade", "Maj-Gen Harpe",
         regiments=[ru_regt("Navaginsk Infantry", 2), ru_regt("Converged Grenadiers (9th, 15th and 18th Divisions)", 3)])],
    command=[{"unit": "ru-cmd-vorontsov"}],
    notes=[LIST_RU, CR_RU_NOTE,
           "Vorontsov, one of the list's named commanders, leads it; his corps is split here by its lines, as Nafziger gives it.",
           "Benckendorff's detachment had a thousand men, Krasovsky's brigade 1,250 and Harpe's 2,154; each regiment is shown at "
           "full size.",
           "Nafziger lists the Navaginsk regiment both here and in Poncet's division; it is shown in both, as he gives it.",
           "Two light batteries and a position battery with seven battalions, where the list allows one light battery and no "
           "position battery, show as historical departures."])

CR_VUICH = force(
    "craonne-vuich", RU, "Vuich's Corps", "Left Wing, Vorontsov's first line", "Russian",
    "The left of Vorontsov's first line, about 4,300 infantry, in front of Ailles and the ravines on the plateau's northern "
    "edge, which Ney's men attacked up the slopes from Vauclair.",
    [bde("ru-infantry-brigade", "Swarikin's Brigade", "Gen Swarikin",
         regiments=[regt("Shirvan Infantry", [u("ru-inf-combined-grenadier", "I/Shirvan Infantry"), u("ru-inf-combined-grenadier", "III/Shirvan Infantry")]),
                    regt("Butyrki Infantry", [u("ru-inf-combined-grenadier", "I/Butyrki Infantry"), u("ru-inf-combined-grenadier", "III/Butyrki Infantry")])]),
     bde("ru-jager-brigade", "19th Jäger", regiments=[regt("19th Jäger", [u("ru-jager", "I/19th Jäger"), u("ru-jager", "III/19th Jäger")])]),
     bde("ru-infantry-brigade", "Poncet's Brigade", "Gen Poncet",
         regiments=[regt("Tula Infantry", [u("ru-inf-combined-grenadier", "I/Tula Infantry"), u("ru-inf-combined-grenadier", "III/Tula Infantry")]),
                    regt("Navaginsk Infantry", [u("ru-inf-combined-grenadier", "I/Navaginsk Infantry"), u("ru-inf-combined-grenadier", "III/Navaginsk Infantry")])])],
    command=[cmd("ru-div-cmd", "Gen-Lt Vuich")],
    notes=[LIST_RU, CR_RU_NOTE,
           "Swarikin's 24th Division (the first two brigades) and Poncet's 14th; the 19th Jäger are a brigade of their own here, "
           "as the list takes Jäger.", CR_RU_BN,
           "A Jäger brigade of one regiment, where the list wants two, shows as a historical departure."])

CR_LAPTEV = force(
    "craonne-laptev", RU, "Laptev's Division", "21st Division, Vorontsov's second line", "Russian",
    "Vorontsov's second line, 3,500 infantry and thirty-six guns; its 2nd Jäger fought for Ailles, and Laptev was wounded.",
    [bde("ru-infantry-brigade", "Laptev's First Brigade", units=[u("ru-position-arty", "Position Battery #28")],
         regiments=[ru_regt("Lithuania Infantry", 1), ru_regt("Podolsk Infantry", 1)]),
     bde("ru-infantry-brigade", "Laptev's Second Brigade", units=[u("ru-light-arty", "Light Battery #42")],
         regiments=[ru_regt("Petrovsk Infantry", 1), ru_regt("Neva Infantry", 1)]),
     bde("ru-jager-brigade", "Laptev's Jäger", units=[u("ru-light-arty", "Light Battery #46")],
         regiments=[ru_regt("2nd Jäger", 1, "ru-jager"), ru_regt("44th Jäger", 1, "ru-jager")])],
    command=[cmd("ru-div-cmd", "Maj-Gen Laptev")],
    notes=[LIST_RU, CR_RU_NOTE,
           "Nafziger gives the division's six regiments without brigades; they are brigaded here in pairs, in his order, with "
           "one of its batteries each.", CR_RU_BN,
           "Two light batteries and a position battery with six battalions, where the list allows one light battery and no "
           "position battery, show as historical departures."])

CR_STROGANOV = force(
    "craonne-stroganov", RU, "Stroganov's Third Line", "Khovansky's 12th and Zheltukhin's 13th Divisions", "Russian",
    "Vorontsov's third line under Stroganov, which stood behind the others on the plateau; Khovansky was wounded.",
    [bde("ru-infantry-brigade", "Khovansky's First Brigade", regiments=[ru_regt("Smolensk Infantry", 1), ru_regt("Narva Infantry", 1)]),
     bde("ru-infantry-brigade", "Khovansky's Second Brigade", regiments=[ru_regt("New Ingermanland Infantry", 1), ru_regt("Alexopol Infantry", 1)]),
     bde("ru-jager-brigade", "Khovansky's Jäger", regiments=[ru_regt("6th Jäger", 1, "ru-jager"), ru_regt("41st Jäger", 1, "ru-jager")]),
     bde("ru-infantry-brigade", "Zheltukhin's Division",
         units=[u("ru-position-arty", "Position Battery #53"), u("ru-light-arty", "Light Battery #48"), u("ru-light-arty", "Light Battery #56")],
         regiments=[regt("Saratov Infantry", [u("ru-inf-combined-grenadier", "I/Saratov Infantry"), u("ru-inf-combined-grenadier", "III/Saratov Infantry")]),
                    regt("Penza Infantry", [u("ru-inf-combined-grenadier", "I/Penza Infantry"), u("ru-inf-combined-grenadier", "III/Penza Infantry")])])],
    command=[{"unit": "ru-cmd-stroganov"}],
    notes=[LIST_RU, CR_RU_NOTE,
           "Stroganov, one of the list's named commanders, leads it. Khovansky's division had 1,800 men and Zheltukhin's 3,300; "
           "Nafziger gives Zheltukhin's only two regiments and its three batteries, and Khovansky's regiments without brigades, "
           "brigaded here in pairs.", CR_RU_BN,
           "Two light batteries in Zheltukhin's brigade, where the list allows one, show as a historical departure."])

CR_VASILCHIKOV = again(MM_VASILCHIKOV, "craonne-vasilchikov",
    "Vasilchikov's hussars and dragoons, which charged Colbert's and Grouchy's squadrons; Lanskoy was mortally wounded, and "
    "Ushakov of the dragoons killed.",
    [LIST_RU, CR_RU_NOTE,
     "Lanskoy's 2nd Hussar Division, 1,500 men, is the light brigades, and Panchulidzev's 3rd Dragoon Division, 1,200, the "
     "dragoons.",
     "Two light and two heavy cavalry brigades, where the list allows one of each, and cavalry with no infantry brigade to "
     "allow it, show as historical departures."])
for b in CR_VASILCHIKOV["brigades"]:
    b["units"] = [x for x in b.get("units", []) if x["name"] not in ("Horse Battery #6", "Horse Battery #7")]

CR_KARPOV = force(
    "craonne-karpov", RU, "Karpov's Cossacks", "Cossacks, Army of Silesia", "Russian",
    "Twelve hundred Cossacks with Vorontsov's cavalry on the plateau.",
    [bde("ru-cossack-brigade", "Karpov's Brigade", "Maj-Gen Karpov II",
         units=[u("ru-mounted-cossack", "Karpov #2 Don Cossacks")] + [u("ru-mounted-cossack", "Cossack Regiment (unnamed)") for _ in range(3)])],
    command=[cmd("ru-div-cmd", "Maj-Gen Karpov II")],
    notes=[LIST_RU, CR_RU_NOTE, "Nafziger names only Karpov's own regiment; the other three aren't known.",
           "Cossacks with no infantry brigade to allow them show as a historical departure."])

CRAONNE["forces"] += [CR_VORONTSOV, CR_VUICH, CR_LAPTEV, CR_STROGANOV, CR_VASILCHIKOV, CR_KARPOV]
CRAONNE["sources"].append(CR_RU)
CRAONNE["toCome"] = [t for t in CRAONNE["toCome"] if t["side"] == "French" or t["name"] == "Sacken's Corps"]


# ================================================================ Laon: the Prussians

LA_AL = {"label": "Allied Army, Battle of Laon, 9–10 March 1814 (Nafziger Collection 814CFJ)", "url": NAF + "814CFJ.pdf"}
LA_AL_NOTE = "After Nafziger's order of battle for the allied army at Laon, from Damitz's history and the Prussian archives."
PR_14 = ("Built from Albion Triumphant's Prussian 1815 list, the nearest to 1814: its Prussian Infantry Brigade is the "
         "brigade of 1813 and 1814, the size of another army's division, with line, reserve and Landwehr battalions.")
COMBINED = ("After a month's fighting several brigades had been put together, and their weakest battalions into combined "
            "ones; each combined battalion is shown as one unit.")
PR_CORPS_DEP = ("More cavalry, reserve artillery and Schützen than the list allows for the corps' brigades, regiments of more "
                "battalions than it takes, and brigades without Landwehr, show as historical departures.")

LA_YORCK = force(
    "laon-yorck", PR15, "Yorck's Corps", "I Corps, Army of Silesia", "Prussian",
    "Blücher's eastern wing, which with Kleist's corps fell on Marmont's bivouacs at Athies in the night of the 9th and "
    "routed his corps, Jürgass's horse riding through the camps and taking forty-five guns.",
    [pi("Combined 1st and 7th Brigade (Horn)", "Gen-Maj von Horn",
        [("Combined Grenadiers (Leib and West Prussian)", [("M", "Combined Leib and West Prussian Grenadier Battalion")]),
         ("Combined Grenadiers (Silesian and 1st East Prussian)", [("M", "Combined Silesian and East Prussian Grenadier Battalion")]),
         ("Leib Infantry", [("M", "I/Leib Infantry"), ("M", "II/Leib Infantry"), ("F", "F/Leib Infantry")]),
         ("Combined Landwehr", [("L", "Combined 5th and 13th Silesian Landwehr"), ("L", "Combined 4th and 15th Silesian Landwehr")])],
        [u("pr15-schutzen", "East Prussian Jäger (2 companies)")]),
     pi("Combined 2nd and 8th Brigade (Prince Wilhelm)", "Gen-Maj Prince Wilhelm of Prussia",
        [("1st East Prussian Infantry", [("M", "I/1st East Prussian Infantry"), ("M", "II/1st East Prussian Infantry"), ("F", "F/1st East Prussian Infantry")]),
         ("Brandenburg and 2nd East Prussian Infantry", [("M", "I/Brandenburg Infantry"), ("M", "II/Brandenburg Infantry"), ("M", "II/2nd East Prussian Infantry")]),
         ("12th Reserve Infantry", [("M", "I/12th Reserve Infantry"), ("M", "II/12th Reserve Infantry"), ("F", "Combined Fusiliers (12th Reserve and Brandenburg)")]),
         ("Silesian Landwehr", [("L", "6th Silesian Landwehr"), ("L", "14th Silesian Landwehr")])]),
     pc("Reserve Cavalry (Jürgass)", "Gen-Maj von Jürgass",
        [u("pr15-hussar", "Mecklenburg-Strelitz Hussars"), u("pr15-hussar", "Brandenburg Hussars"), u("pr15-hussar", "2nd Leib Hussars"),
         u("pr15-dragoon", "Lithuanian Dragoons"), u("pr15-dragoon", "1st West Prussian Dragoons"), u("pr15-uhlan", "Brandenburg Uhlans"),
         u("pr15-horse-arty", "6-pdr Horse Battery #1")]),
     pc("Landwehr Cavalry", "", [u("pr15-mounted-landwehr", "East Prussian National Cavalry"), u("pr15-mounted-landwehr", "3rd, 4th and 5th Silesian Landwehr Cavalry"),
                                 u("pr15-horse-arty", "6-pdr Horse Battery #2")], landwehr=True),
     pres(u("pr15-heavy-arty", "12-pdr Foot Battery #1"), u("pr15-heavy-arty", "12-pdr Foot Battery #2"),
          u("pr15-foot-arty", "6-pdr Foot Battery #1"), u("pr15-foot-arty", "6-pdr Foot Battery #2"), u("pr15-foot-arty", "6-pdr Foot Battery #3"),
          u("pr15-foot-arty", "6-pdr Foot Battery #15"), u("pr15-horse-arty", "6-pdr Horse Battery #3"), u("pr15-horse-arty", "6-pdr Horse Battery #12"))],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Yorck")],
    notes=[PR_14, LA_AL_NOTE, PR_WHOLE, PR_GROUPED, PR_SUB, COMBINED,
           "Nafziger gives the 2nd East Prussian's two battalions as one regiment; the one here is grouped with the Brandenburg "
           "regiment, as the list takes three regiments in a brigade. The East Prussian National Cavalry, a volunteer regiment, "
           "and the Silesian Landwehr cavalry are the list's Mounted Landwehr.",
           "Schmidt's corps artillery is the list's reserve, with a horse battery with each cavalry brigade.", PR_CORPS_DEP])

LA_KLEIST = force(
    "laon-kleist", PR15, "Kleist's Corps", "II Corps, Army of Silesia", "Prussian",
    "Blücher's eastern wing with Yorck's, much reduced since Vauchamps, which joined the night attack on Marmont at Athies.",
    [pi("9th Brigade (Klüx)", "Gen-Maj von Klüx",
        [("1st West Prussian Infantry", [("M", "I/1st West Prussian Infantry"), ("M", "II/1st West Prussian Infantry"), ("F", "F/1st West Prussian Infantry")]),
         ("6th Reserve Infantry", [("M", "I/6th Reserve Infantry"), ("F", "F/6th Reserve Infantry")])],
        [u("pr15-schutzen", "Silesian Schützen (2 companies)")]),
     pi("10th Brigade (Pirch I)", "Gen-Maj von Pirch I",
        [("2nd West Prussian Infantry", [("M", "I/2nd West Prussian Infantry"), ("M", "II/2nd West Prussian Infantry"), ("F", "F/2nd West Prussian Infantry")]),
         ("Combined Battalions", [("M", "Combined 2nd and 7th Infantry"), ("M", "Combined Battalion"), ("M", "Combined Battalion"), ("M", "Combined Battalion")])],
        [u("pr15-schutzen", "Silesian Schützen (2 companies)")]),
     pc("Reserve Cavalry (Zieten)", "Gen-Maj von Zieten",
        [u("pr15-dragoon", "East Prussian Cuirassiers"), u("pr15-dragoon", "Brandenburg Cuirassiers"), u("pr15-dragoon", "Silesian Cuirassiers"),
         u("pr15-dragoon", "Neumark Dragoons"), u("pr15-horse-arty", "6-pdr Horse Battery #7")]),
     pc("Light Cavalry", "", [u("pr15-hussar", "1st Silesian Hussars"), u("pr15-hussar", "2nd Silesian Hussars"), u("pr15-uhlan", "Silesian Uhlans"),
                              u("pr15-horse-arty", "6-pdr Horse Battery #8")]),
     pc("Landwehr Cavalry", "", [u("pr15-mounted-landwehr", "Silesian National Cavalry (2 squadrons)"),
                                 u("pr15-mounted-landwehr", "7th and 8th Silesian Landwehr Cavalry (2 squadrons)")], landwehr=True),
     pres(u("pr15-heavy-arty", "12-pdr Foot Battery #3"), u("pr15-heavy-arty", "12-pdr Foot Battery #6"), u("pr15-foot-arty", "7-pdr Howitzer Battery #1"),
          u("pr15-foot-arty", "6-pdr Foot Battery #7"), u("pr15-foot-arty", "6-pdr Foot Battery #8"), u("pr15-foot-arty", "6-pdr Foot Battery #9"),
          u("pr15-horse-arty", "6-pdr Horse Battery #9"))],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Kleist")],
    notes=[PR_14, LA_AL_NOTE, PR_WHOLE, PR_GROUPED, PR_SUB, COMBINED,
           "Nafziger gives only the 9th and 10th Brigades; the 11th and 12th, broken at Vauchamps, are not on his return. The "
           "6th Reserve's third battalion was at Erfurt. The 10th Brigade's three combined battalions aren't named.",
           "Zieten's cuirassiers and dragoons are the list's Dragoons, its only heavy cavalry; his light regiments are a brigade "
           "of their own here. The Silesian National Cavalry and Landwehr cavalry are the list's Mounted Landwehr.",
           "Braun's corps artillery is the list's reserve, with a horse battery with each regular cavalry brigade.", PR_CORPS_DEP])

LA_BULOW = force(
    "laon-bulow", PR15, "Bülow's Corps", "III Corps, Army of the North", "Prussian",
    "The corps that held the hill and town of Laon itself through both days, against Ney's and Mortier's attacks from the "
    "south-west.",
    [pi("3rd Brigade (Hesse-Homburg)", "Gen-Maj Prince of Hesse-Homburg",
        [("3rd East Prussian Infantry", [("M", "I/3rd East Prussian Infantry"), ("M", "II/3rd East Prussian Infantry"), ("F", "F/3rd East Prussian Infantry")]),
         ("4th Reserve Infantry", [("M", "I/4th Reserve Infantry"), ("M", "II/4th Reserve Infantry"), ("F", "F/4th Reserve Infantry")]),
         ("2nd East Prussian Grenadiers", [("M", "2nd East Prussian Grenadier Battalion")])]),
     pi("4th Brigade (Thümen)", "Gen-Maj von Thümen",
        [("4th East Prussian Infantry", [("M", "I/4th East Prussian Infantry"), ("M", "II/4th East Prussian Infantry"), ("F", "F/4th East Prussian Infantry")]),
         ("5th Reserve Infantry", [("M", "II/5th Reserve Infantry"), ("M", "III/5th Reserve Infantry")])]),
     pi("6th Brigade (Krafft)", "Col von Krafft",
        [("Colberg Infantry", [("M", "I/Colberg Infantry"), ("M", "II/Colberg Infantry"), ("F", "F/Colberg Infantry")]),
         ("9th Reserve Infantry", [("M", "I/9th Reserve Infantry"), ("M", "II/9th Reserve Infantry"), ("F", "F/9th Reserve Infantry")]),
         ("1st Neumark Landwehr", [("L", "I/1st Neumark Landwehr"), ("L", "III/1st Neumark Landwehr")])]),
     pc("Reserve Cavalry (Oppen)", "Gen-Maj von Oppen",
        [u("pr15-dragoon", "Queen's Dragoons (with volunteer Jäger)"), u("pr15-dragoon", "2nd West Prussian Dragoons"),
         u("pr15-dragoon", "Prince Wilhelm Dragoons (2 squadrons)"), u("pr15-horse-arty", "6-pdr Horse Battery #11")]),
     pc("Landwehr Cavalry", "", [u("pr15-mounted-landwehr", "1st Pomeranian Landwehr Cavalry"), u("pr15-mounted-landwehr", "2nd Pomeranian Landwehr Cavalry")], landwehr=True),
     pres(u("pr15-heavy-arty", "12-pdr Foot Battery #4"), u("pr15-heavy-arty", "12-pdr Foot Battery #5"),
          u("pr15-foot-arty", "6-pdr Foot Battery #5"), u("pr15-foot-arty", "6-pdr Foot Battery #6"), u("pr15-foot-arty", "6-pdr Foot Battery #19"))],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Bülow")],
    notes=[PR_14, LA_AL_NOTE, PR_WHOLE, PR_GROUPED, PR_SUB,
           "Holzendorf's corps artillery is the list's reserve; the two Russian 12-pdr batteries with it are left out.",
           "The 2nd East Prussian Grenadier Battalion has the list's Veteran upgrade.", PR_CORPS_DEP])
LA_BULOW["missing"] = [{"name": "Two Russian 12-pdr batteries", "reason": "Russian guns with the corps, which a force from the Prussian list can't take."}]

LAON["forces"] += [LA_YORCK, LA_KLEIST, LA_BULOW]
LAON["sources"].append(LA_AL)
LAON["toCome"] = [t for t in LAON["toCome"] if t["side"] != "Prussian"]


if __name__ == "__main__":
    for b in (BRIENNE, LA_ROTHIERE) + ARMIES_TO_COME:
        write(b)
