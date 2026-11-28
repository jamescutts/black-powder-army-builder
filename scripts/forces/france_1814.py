"""
Writes the forces of the Campaign in France (src/data/battles/{brienne,la-rothiere}.json): the French, from Nafziger's orders
of battle, with the allies still to come.

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
from liberation_1813 import CAV_ONLY, FIG, FR, MARINES, NAF, bn_list, marine, regt

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
           "Nafziger gives the horse artillery as three hundred gunners and train, shown as one battery.",
           CAV_ONLY])
BR_GUARD_CAV["missing"] = [{"name": "2nd Éclaireurs", "reason": "A regiment of Guard scouts raised that winter, three hundred strong, which the 1812 list doesn't have."}]

BR_V_CAVALRY = force(
    "brienne-v-cavalry", FR, "Milhaud's Cavalry", "V Cavalry Corps, under Grouchy", "French",
    "The army's advance guard, Piré's light horse leading, which drove Shcherbatov's Cossacks out of Maizières."
    " Grouchy brought up the rest of the corps and pressed Pahlen's cavalry back through Brienne, until L'Héritier's "
    "and Briche's dragoons were stopped by the Russian Jäger in square. That night Grouchy sent L'Héritier's dragoons into "
    "the town itself, to no purpose.",
    [bde("fr-light-cavalry-brigade", "Subervie's Brigade", "Gén. de Brigade Subervie",
         units=[u("fr-hussar-regt", "3rd Hussars"), u("fr-chasseur-a-cheval", "26th Chasseurs à Cheval")]),
     bde("fr-light-cavalry-brigade", "Pacz's Brigade", "Gén. de Brigade Pacz",
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
           "Two horse batteries, one with each division, are here; the Guard lost twenty-four horse guns in the fight.",
           CAV_ONLY])
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


if __name__ == "__main__":
    for b in (BRIENNE, LA_ROTHIERE):
        write(b)
