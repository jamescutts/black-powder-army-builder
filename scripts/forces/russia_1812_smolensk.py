"""
Writes Smolensk (src/data/battles/smolensk.json): Napoleon's assault on the walled city, 16–18 August 1812.

    python3 scripts/forces/russia_1812_smolensk.py && npm run check:forces

The formations are those Nafziger gives for the Grande Armée of 15 August (812HDA) and at Borodino (812ICA, 812ICB), with
his order of battle for Smolensk (812HBM) and Wikipedia for who fought where. Summaries are our own words.
"""

import copy
import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from russia_1812 import ru_jager_regiment, ru_regiment
from russia_1812_autumn import DUFOUR, EUGEN, KAPSEVICH, LIKHACHEV, PONIATOWSKI_16, PONIATOWSKI_18, naf
from russia_1812_centre import KOLUBAKIN, KONOVNITSYN, PASKEVICH
from russia_1812_north import fr_regiment
from russia_1812_valutino import GUDIN, LEDRU, MARCHAND, RAZOUT

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
FR, RU = "france", "russia"


def again(f, summary, formation=None, command=None, name=None):
    g = copy.deepcopy(f)
    g["id"] = "smolensk-" + f["id"].split("-", 1)[1]
    g["summary"] = summary
    if formation:
        g["formation"] = formation
    if command:
        g["command"] = [command]
    if name:
        g["name"] = name
    if g["side"] in ("Polish", "Italian"):
        g["side"] = "French"
    if f["nationId"] == "grand-duchy-of-warsaw":
        # In August the Polish corps hadn't yet been worn down at Borodino
        for br in g["brigades"]:
            for x in br.get("units", []) + [x for r in br.get("regiments", []) for x in r["units"]]:
                x.pop("options", None)
        g["notes"] = ["After Nafziger's order of battle for Borodino, three weeks later."] + [n for n in g["notes"] if "After Borodino" not in n and "wounded at Borodino" not in n and "After Nafziger" not in n]
    g["notes"] = [n for n in g["notes"] if "Borodino, six weeks" not in n] + (
        ["After Nafziger's order of battle for Borodino, three weeks later; the division was stronger at Smolensk."] if f["nationId"] == RU else [])
    return g


MORAND = force("smolensk-morand", FR, "Morand's Division", "1st Division, I Corps (Davout)", "French",
               "Davout's leading division, which stormed the suburbs before the eastern walls on the 17th and fought for them until dark under fire from the ramparts.",
               [bde("fr-infantry-brigade", "d'Alton's Brigade", "Gén. de Brigade d'Alton", regiments=[fr_regiment("13th Léger", 5, light=True)]),
                bde("fr-infantry-brigade", "Gratien's Brigade", "Gén. de Brigade Gratien", regiments=[fr_regiment("17th Line", 5)]),
                bde("fr-infantry-brigade", "Bonamy's Brigade", "Gén. de Brigade Bonamy", regiments=[fr_regiment("30th Line", 5)]),
                bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "1/7th Foot Artillery"), u("fr-horse-arty", "7/1st Horse Artillery")])],
               command=[cmd("fr-div-cmd", "Gén. de Division Morand")],
               notes=["After Nafziger's order of battle for Borodino.", "The horse battery, without three cavalry regiments in the force, shows as a historical departure."])

NEVEROVSKY = force("smolensk-neverovsky", RU, "Neverovsky's 27th Division", "27th Division, 2nd Army of the West", "Russian",
                   "Fresh from its fighting retreat at Krasnoi on the 14th, where its squares had held off Murat's cavalry for a day, it joined Raevsky in the defence of the suburbs on the 16th.",
                   [bde("ru-infantry-brigade", "Knyazhnin's Brigade", "Col Knyazhnin", regiments=[ru_regiment("Vilna"), ru_regiment("Simbirsk")]),
                    bde("ru-infantry-brigade", "Stavitsky's Brigade", "Col Stavitsky", regiments=[ru_regiment("Odessa"), ru_regiment("Tarnopol")]),
                    bde("ru-jager-brigade", "Voeikov's Brigade", "Col Voeikov", regiments=[ru_jager_regiment("49th"), ru_jager_regiment("50th")])],
                   command=[cmd("ru-div-cmd", "Maj-Gen Neverovsky")],
                   notes=["After Nafziger's order of battle for Borodino. A new division of recruits; it had lost a quarter of its men at Krasnoi, and its guns there.",
                          "Nafziger gives it no artillery of its own; add a Light Battery if you like."])

SMOLENSK = {
    "id": "smolensk", "name": "Smolensk", "date": "16–18 August 1812", "campaign": "russia-1812",
    "summary": "Napoleon, hoping at last to bring the Russian armies to battle, closed on the walled city of Smolensk. Raevsky held its suburbs on the 16th while Bagration came up; on the 17th Ney, Davout and Poniatowski stormed the suburbs against Dokhturov's corps and the walls, but could not break into the city. That night the Russians fired it and withdrew across the Dnieper, and the French entered a burning ruin.",
    "sources": [naf("812HBM", "Battle of Smolensk, 17 August 1812"), naf("812HDA", "French Grande Armée, 15 August 1812"),
                naf("812ICA", "French Army, Battle of Borodino, 5–7 September 1812"), naf("812ICB", "Russian Army, Battle of Borodino, 5–7 September 1812"),
                {"label": "Battle of Smolensk (1812) (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Smolensk_(1812)"}],
    "forces": [
        again(RAZOUT, "Ney's corps attacked the citadel and the western suburbs on the 16th and again on the 17th, without breaking in."),
        again(LEDRU, "Beside Razout's in Ney's attacks on the suburbs and the citadel."),
        again(MARCHAND, "The Württembergers fought in Ney's assault on the suburbs on the 17th."),
        MORAND,
        again(DUFOUR, "Davout's centre division in the assault on the eastern suburbs on the 17th.", formation="2nd Division, I Corps (Davout)",
              command={"unit": "fr-cmd-friant"}, name="Friant's Division"),
        again(GUDIN, "Davout's third division, which carried the Malakhov suburb in the evening of the 17th."),
        again(PONIATOWSKI_16, "Poniatowski's Poles attacked the eastern suburbs by the Dnieper and set their guns on the bridges."),
        again(PONIATOWSKI_18, "Beside the 16th in the Polish attack on the right."),
        again(KOLUBAKIN, "Raevsky's corps held the suburbs and the walls on the 16th against Ney's first attacks, buying time for Bagration's army to come up.", formation="12th Division, VII Corps (Raevsky)"),
        again(PASKEVICH, "Held the old citadel and the suburbs beside it under Raevsky on the 16th."),
        NEVEROVSKY,
        again(KAPSEVICH, "Dokhturov's corps took over the defence on the night of the 16th and held the suburbs and walls all through the 17th."),
        again(LIKHACHEV, "Dokhturov's second division, fighting in the eastern suburbs against Davout's and Poniatowski's attacks."),
        again(KONOVNITSYN, "Sent into the city on the 17th to reinforce Dokhturov, it held the Malakhov gate as the suburbs fell."),
        again(EUGEN, "Prince Eugen's division reinforced the defence of the walls on the 17th."),
    ],
}
for f in SMOLENSK["forces"]:
    if f["id"] == "smolensk-dufour":
        f["id"] = "smolensk-friant"
        f["notes"] = ["Friant is the book's named commander."] + [n for n in f["notes"] if "Friant was wounded" not in n]


if __name__ == "__main__":
    art = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
    for b in (SMOLENSK,):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in art:
            b["art"] = art[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
