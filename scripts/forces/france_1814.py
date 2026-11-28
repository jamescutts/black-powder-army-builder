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
from liberation_1813 import (CAV_ONLY, FIG, FR, LIST_RU, MARINES, NAF, PR15, PR_GROUPED, PR_LIST, PR_SUB, PR_WHOLE, RU,
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

CHAMPAUBERT = fought("champaubert", [CH_FR, SIX_DAYS, wiki("Battle of Champaubert", "Battle_of_Champaubert")],
    [CH_LAGRANGE, CH_RICARD, CH_BORDESOULLE, CH_MEUNIER, CH_DECOUZ],
    [ru("Olsufiev's Corps", "Udom's 9th and Kornilov's 15th Divisions, IX Infantry Corps, Army of Silesia",
        "About four thousand men and twenty-four guns, strung out along Blücher's line of march. Most were killed or taken, "
        "Olsufiev and Poltoratsky among them; Kornilov brought some fifteen hundred away through the woods.")])

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

MONTMIRAIL = fought("montmirail", [MM_FR, SIX_DAYS, wiki("Battle of Montmirail", "Battle_of_Montmirail")],
    [MM_RICARD, MM_MEUNIER, MM_CURIAL, MM_FRIANT, MM_MICHEL, MM_COLBERT, MM_LEFEBVRE, MM_LAFERRIERE, MM_DEFRANCE], [
    ru("Sacken's Corps", "Shcherbatov's VI and Lieven's XI Infantry Corps, Army of Silesia",
       "Some eighteen thousand men and eighty to ninety guns, marching back east to join Blücher. It took Marchais and lost it, "
       "and was driven north towards Château-Thierry."),
    ru("Vasilchikov's Cavalry", "Lanskoy's 2nd Hussar and Panchulidzev's 3rd Dragoon Divisions, with Karpov's Cossacks",
       "Counter-attacked Nansouty's horse and covered Sacken's retreat."),
    pr("Yorck's Corps", "Pirch's 1st and Horn's 7th Brigades, I Corps, Army of Silesia",
       "Reached Viffort late in the day. Pirch's brigade attacked the Bois de Bailly and was thrown back, Pirch wounded.")],
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

CHATEAU_THIERRY = fought("chateau-thierry", [MM_FR, SIX_DAYS, wiki("Battle of Château-Thierry (1814)", "Battle_of_Ch%C3%A2teau-Thierry_(1814)")],
    [CT_CHRISTIANI, CT_MEUNIER, CT_FRIANT, CT_COLBERT, CT_LEFEBVRE, CT_LAFERRIERE, CT_DEFRANCE], [
    pr("Yorck's Corps", "Katzler's advance guard, Horn's 7th Brigade and Jürgass's reserve cavalry, I Corps, Army of Silesia",
       "Covered Sacken's crossing of the Marne. Horn's brigade was broken before Château-Thierry, and two East Prussian "
       "battalions were cut off and taken."),
    ru("Sacken's Corps", "Army of Silesia",
       "Already beaten at Montmirail, it got back over the Marne at Château-Thierry; Heidenreich's brigade was overrun and mostly taken.")],
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

BAR_SUR_AUBE = armies("bar-sur-aube", [wiki("Battle of Bar-sur-Aube", "Battle_of_Bar-sur-Aube")], [
    fr("Oudinot's Corps", "VII Corps",
       "Holding the heights before Bar-sur-Aube for Macdonald's army, it took the weight of Schwarzenberg's attack and was "
       "driven back over the Aube."),
    fr("Gérard's Corps", "II Corps",
       "With Oudinot's before the town; much of Macdonald's army, and most of its guns, were on the far side of the Aube and "
       "could take no part."),
    ru("Wittgenstein's Corps", "VI Corps, Army of Bohemia",
       "Attacked Oudinot's position; Wittgenstein was wounded leading it."),
    bav("Wrede's Corps", "V Corps, Army of Bohemia",
        "Wrede's Bavarians and Austrians, who came on against Oudinot beside Wittgenstein's Russians.")],
    alliances=(("Russian", "Bavarian"),))

LAUBRESSEL = armies("laubressel", [wiki("Battle of Laubressel", "Battle_of_Laubressel")], [
    fr("Gérard's Corps", "Duhesme's and Hamelinaye's divisions and Jarry's brigade, II Corps",
       "Held the bridge of La Guillotière, where Duhesme lost two guns and four hundred men; Bellair's brigade of Hamelinaye's "
       "division was routed, and Gérard drew back into Troyes."),
    fr("Oudinot's Corps", "Rothembourg's, Leval's, Chassé's and Pacthod's divisions, VII Corps",
       "Rothembourg's Young Guard held the plateau of Laubressel until Wittgenstein's Russians came round its flank."),
    fr("Macdonald's Corps", "Albert's, Brayer's and Amey's divisions, XI Corps (Molitor)",
       "Fell back on Troyes without being pressed."),
    fr("Saint-Germain's Cavalry", "Maurin's and Delort's divisions, II Cavalry Corps",
       "Maurin's horse retook most of the artillery park Pahlen's cavalry had overrun at Thennelières."),
    fr("Milhaud's Cavalry", "Piré's, Briche's and L'Héritier's divisions, V Cavalry Corps",
       "Fell back with the infantry without being engaged."),
    fr("Kellermann's Cavalry", "Jacquinot's and Trelliard's divisions, VI Cavalry Corps",
       "Trelliard's dragoons counter-attacked the Russians at Thennelières; Jacquinot's division stampeded at La Chapelle-Saint-Luc."),
    ru("Wittgenstein's Corps", "Gorchakov's I and Eugen of Württemberg's II Infantry Corps and Pahlen's cavalry, VI Corps",
       "About fourteen thousand men, who took Bouranton and the Laubressel plateau while Pahlen's horse raided the French artillery park."),
    bav("Wrede's Corps", "Three Bavarian and two Austrian divisions, V Corps",
        "About twenty thousand men, whose guns opened the attack; they pushed on towards Troyes."),
    wt("The Crown Prince of Württemberg's Corps", "Koch's and Döring's divisions and Prince Adam's cavalry, IV Corps",
       "About fifteen thousand men on the allied left, who followed Macdonald towards Sens."),
    at("Gyulai's Corps", "Crenneville's, Fresnel's and Hohenlohe's divisions, III Corps",
       "About ten thousand Austrians, who attacked at Silvarouvres.")],
    alliances=(("Russian", "Bavarian", "Württemberg", "Austrian"),))

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
    "squares; Laferrière lost a leg and Grouchy was wounded.",
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

LAON = armies("laon", [wiki("Battle of Laon", "Battle_of_Laon")], [
    fr("Napoleon's Army", "The Guard, with Ney's and Mortier's infantry",
       "Some forty thousand men, who attacked the hill of Laon from the south-west on the 9th and again on the 10th without carrying it."),
    fr("Marmont's Corps", "VI Corps",
       "About ten thousand men, coming up the Berry-au-Bac road to Athies. Yorck's and Kleist's Prussians fell on it in the night "
       "and routed it, taking forty-five guns; Fabvier's men and an Old Guard escort held open its road back."),
    pr("Bülow's Corps", "III Corps, Army of the North", "Held Laon itself."),
    pr("Yorck's and Kleist's Corps", "I and II Corps, Army of Silesia",
       "Held the eastern wing, and routed Marmont at Athies in the night of the 9th."),
    ru("Winzingerode's Corps", "Army of the North", "Covered Blücher's western wing."),
    ru("Langeron's and Sacken's Corps", "Army of Silesia", "In reserve.")],
    alliances=(("Prussian", "Russian"),))

REIMS = armies("reims", [wiki("Battle of Reims (1814)", "Battle_of_Reims_(1814)")], [
    fr("Marmont's Corps", "Ricard's division and Pelleport's brigade, VI Corps, with Bordesoulle's I Cavalry Corps",
       "Led the march on Reims, catching Prussian cavalry at Rosnay and Jagow's Landwehr at Ormes; Ricard's division took the "
       "Sainte-Geneviève heights before the town and failed to storm the Soissons gate."),
    fr("Defrance's Gardes d'Honneur", "Cavalry Division, with Piquet's and Ségur's brigades",
       "Led the assault with Ricard's division; Ségur's brigade, with the 3rd Gardes d'Honneur, was trapped and largely destroyed."),
    fr("Sébastiani's Guard Cavalry", "Exelmans's and Colbert's divisions",
       "Advanced on Ricard's flanks; Exelmans's division crossed the Vesle and led the pursuit."),
    fr("The Guard and Ney's Infantry", "Friant's Old Guard and Boyer de Rébeval's divisions",
       "Came up in the afternoon and were held back; sixteen of the Guard's guns blew in the Soissons gate."),
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

PARIS = armies("paris", [wiki("Battle of Paris (1814)", "Battle_of_Paris_(1814)")], [
    fr("Marmont's Wing", "Arrighi's, Ricard's and Lagrange's divisions, Compans's, Ledru des Essarts's and Boyer de Rébeval's provisional divisions, and Bordesoulle's, Merlin's and Chastel's cavalry",
       "Held the heights of Romainville and Belleville on the right; Arrighi's division held Bagnolet and Montreuil."),
    fr("Mortier's Wing", "Michel's Guard depots, Charpentier's and Curial's Young Guard and Christiani's Old Guard divisions, with Ornano's and Roussel d'Hurbal's cavalry",
       "Held the plain on the left, from Pantin and Aubervilliers to La Villette and La Chapelle."),
    fr("Moncey's National Guard", "The National Guard of Paris", "About twelve thousand men, under Marshal Moncey."),
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


if __name__ == "__main__":
    for b in (BRIENNE, LA_ROTHIERE) + ARMIES_TO_COME:
        write(b)
