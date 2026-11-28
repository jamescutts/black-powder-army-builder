"""
Writes the forces of the Campaign in France (src/data/battles/{brienne}.json): the French, from Nafziger's orders
of battle, with the allies still to come.

    python3 scripts/forces/france_1814.py && npm run check:forces

There are no 1814 army lists, so every force borrows the nearest, as 1813's do: A Clash of Eagles' 1812 lists for
the French and the Imperial Guard. Each force's notes say so. Summaries are our own words. Staff Ratings are set
by ratings.py.
"""

import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from liberation_1813 import CAV_ONLY, FIG, FR, NAF, bn_list, regt

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


def ru(name, formation, summary):
    return {"side": "Russian", "name": name, "formation": formation, "summary": summary, "flag": RU_FLAG}


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


if __name__ == "__main__":
    for b in (BRIENNE,):
        write(b)
