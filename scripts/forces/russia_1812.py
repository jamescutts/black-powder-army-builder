"""
Writes the 1812 Russian campaign's historical forces (src/data/battles/{eckau,mesoten}.json), starting with
the battles of the Prussian Auxiliary Corps on the Riga front.

    python3 scripts/forces/russia_1812.py && npm run check:forces

Sources (see SOURCES): the Prussian corps' order of battle is the Weltseele wiki's, of 12 March 1812, with
German Wikipedia's account of where its regiments went; the Russian units are from Wikipedia's Russian
order of battle for 1812 and its Siege of Riga article; strengths and the course of each action from
Riehn's Napoleon's Russian Campaign, German Wikipedia and Mark Conrad's translations. Summaries are our own
words. Staff Ratings are set by ratings.py: 8 unless a commander is one of the book's named ones.
"""

import json
from pathlib import Path

import ratings
from hundred_days import bde, cmd, force, u

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
SOURCES = [
    {"label": "Königlich Preussisches Hülfscorps, Russian Campaign of 1812 (Weltseele)",
     "url": "https://weltseele.miraheze.org/wiki/Orders_of_Campaign_and_Battle_(Prussia)/K%C3%B6niglich_Preussisches_H%C3%BClfscorps_(Russian_Campaign_of_1812)"},
    {"label": "Preußischer Feldzug von 1812 (German Wikipedia)", "url": "https://de.wikipedia.org/wiki/Preu%C3%9Fischer_Feldzug_von_1812"},
    {"label": "Order of battle of the Imperial Russian Army, 1812 (Wikipedia)",
     "url": "https://en.wikipedia.org/wiki/Order_of_battle_of_the_Imperial_Russian_Army_(1812)"},
    {"label": "Siege of Riga, 1812 (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Siege_of_Riga_(1812)"},
    {"label": "Richard Riehn, Napoleon's Russian Campaign, ch. 14 (Summer and autumn in Latvia)"},
    {"label": "The fight at Gross-Eckau, from Russkaya Starina, 1912 (Mark Conrad's translation)",
     "url": "https://marksrussianmilitaryhistory.info/GrossEckau.htm"},
]

# ---------------------------------------------------------------- The Prussian Auxiliary Corps (Prussia 1812)

PR = "prussia"


def combined(num, battalions):
    """A combined infantry regiment: (kind, parent) battalions, kind M (musketeer) or F (fusilier)"""
    unit = {"M": "pr-musketeer", "F": "pr-fusilier"}
    return {"name": f"{num} Combined Infantry Regiment", "units": [u(unit[k], name) for k, name in battalions]}


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


BELOW = bde("pr-infantry-brigade", "1st Brigade (Below)", "Col von Below",
            units=[u("pr-foot-arty", "6-pdr Foot Battery")],
            regiments=[combined("1st", [("M", "II/1st East Prussian"), ("F", "F/1st East Prussian"), ("M", "I/2nd East Prussian")]),
                       combined("2nd", [("M", "I/3rd East Prussian"), ("M", "I/4th East Prussian"), ("F", "F/4th East Prussian")])])
HORN = bde("pr-infantry-brigade", "2nd Brigade (Horn)", "Lt-Col von Horn",
           units=[u("pr-foot-arty", "6-pdr Foot Battery")],
           regiments=[combined("3rd", [("M", "I/Colberg"), ("M", "II/Pomeranian"), ("F", "F/Pomeranian")]),
                      combined("4th", [("M", "I/Leib Infantry"), ("M", "II/Leib Infantry"), ("F", "III/Leib Infantry")])])
RAUMER = bde("pr-infantry-brigade", "3rd Brigade (Raumer)", "Col von Raumer",
             units=[u("pr-jager", "East Prussian Jäger Bn"), u("pr-foot-arty", "6-pdr Foot Battery")],
             regiments=[combined("5th", [("M", "I/1st West Prussian"), ("M", "II/2nd West Prussian"), ("F", "F/2nd West Prussian")]),
                        combined("6th", [("M", "II/1st Silesian"), ("M", "II/2nd Silesian"), ("F", "F/2nd Silesian")])])
JEANNERET = bde("pr-cavalry-brigade", "Jeanneret's Brigade", "Col von Jeanneret",
                [u("pr-hussars", "3rd Combined Hussars (1st & 2nd Silesian)"), u("pr-horse-arty", "6-pdr Horse Battery")])
HUNERBEIN = bde("pr-cavalry-brigade", "Hünerbein's Brigade", "Col von Hünerbein",
                [u("pr-dragoon", "1st Combined Dragoons (Lithuanian, 2nd W. Prussian)"),
                 u("pr-dragoon", "2nd Combined Dragoons (1st W. Prussian, Brandenburg)")])
CORPS_ARTILLERY = bde("pr-army-artillery", "Corps Artillery",
                      units=[u("pr-foot-arty", "6-pdr Foot Battery"), u("pr-heavy-arty", "12-pdr Half Battery", options=["half-battery"])])

CORPS_NOTES = [
    "Each combined regiment drew its three battalions from two parent regiments, as named; each combined cavalry regiment two squadrons from each of two. The 4th's third Leib battalion is taken as its Fusiliers.",
    "The Leib Hussars (1st Combined Hussars) served with Grandjean's division rather than the corps, and the 2nd Combined Hussars and the Uhlans went to the main army, so they're left out.",
    "Kleist commanded the corps' infantry and Massenbach its cavalry under the corps commander; add them as Subordinate Commanders if you like.",
]


def prussian_corps(battle, commander, summary, notes=()):
    return force(f"{battle}-prussian-corps", PR, "The Prussian Auxiliary Corps", "27th Division, X Corps (Macdonald)", "Prussian", summary,
                 [BELOW, HORN, RAUMER, JEANNERET, HUNERBEIN, CORPS_ARTILLERY],
                 command=[cmd("pr-div-cmd", commander)],
                 notes=[*notes, *CORPS_NOTES])


# ---------------------------------------------------------------- Russia 1812-15

RU = "russia"


def ru_regiment(name, n=2, jager=None, jager_n=2):
    """A Russian infantry regiment's battalions, with a Jäger regiment attached, as the list builds them"""
    units = [u("ru-inf-combined-grenadier", f"{['1st', '2nd', '3rd'][i]} Bn, {name}") for i in range(n)]
    if jager:
        units += [u("ru-jager", f"{['1st', '2nd', '3rd'][i]} Bn, {jager} Jäger") for i in range(jager_n)]
    return {"name": f"{name} Infantry" + (f" with {jager} Jäger" if jager else ""), "units": units}


def ru_jager_regiment(name, n=2, small=False):
    opts = {"options": ["small"]} if small else {}
    return {"name": f"{name} Jäger", "units": [u("ru-jager", f"{['1st', '2nd', '3rd'][i]} Bn, {name} Jäger", **opts) for i in range(n)]}


def alexeyev(battle, summary):
    return force(f"{battle}-alexeyev", RU, "Alexeyev's Division", "21st Infantry Division, Finland Corps (Steinheil)", "Russian", summary,
                 [bde("ru-infantry-brigade", "1st Brigade", "",
                      units=[u("ru-position-arty", "21st Position Battery")],
                      regiments=[ru_regiment("Petrovsk", jager="2nd"), ru_regiment("Podolia")]),
                  bde("ru-infantry-brigade", "2nd Brigade", "",
                      units=[u("ru-light-arty", "40th Light Battery")],
                      regiments=[ru_regiment("Neva"), ru_regiment("Lithuania")]),
                  bde("ru-light-cavalry-brigade", "Cavalry", "",
                      [u("ru-dragoon", "Finland Dragoons", options=["small-cavalry"]), u("ru-mounted-cossack", "Loshchilin's Cossacks")])],
                 command=[cmd("ru-div-cmd", "Maj-Gen Alexeyev")],
                 notes=["The division's own 2nd Jäger is attached to the Petrovsk regiment, as the list takes a Jäger regiment; its other Jäger regiment, the 44th, was detached on Åland.",
                        "Battalion counts aren't certain: one account gives these regiments three battalions, the order of battle none. Two field battalions each are shown, the usual for 1812.",
                        "Riehn gives the division '9,000 infantry, only 200 cavalry and twelve guns' at Mesoten, so the Finland Dragoons (three squadrons) are Small.",
                        "Staff Ratings are our judgement, all at 7: the list lets at most half the brigade commanders be rated higher."])


def rachmanov(battle, summary):
    return force(f"{battle}-rachmanov", RU, "Rachmanov's Division", "6th Infantry Division, Finland Corps (Steinheil)", "Russian", summary,
                 [bde("ru-infantry-brigade", "Azov and Nizov", "",
                      units=[u("ru-light-arty", "11th Light Battery")],
                      regiments=[ru_regiment("Azov", jager="3rd"), ru_regiment("Nizov", jager="35th")])],
                 command=[cmd("ru-div-cmd", "Maj-Gen Rachmanov")],
                 notes=["The Azov and Nizov regiments with the 3rd and 35th Jäger, each Jäger regiment taken as the list's attached Jäger. One account adds the Uglich regiment, the Russian order of battle the Bryansk, which was on Åland; neither is included.",
                        "Two field battalions per regiment are shown, the usual for 1812; the sources don't give counts. At Lautschkrug two battalions of the 3rd Jäger were caught forming square by Prussian cavalry and taken.",
                        "Staff Ratings are our judgement, at 7."])


def lowis(battle, summary):
    return force(f"{battle}-lowis", RU, "Löwis's Detachment", "From the Riga garrison (Essen)", "Russian", summary,
                 [bde("ru-jager-brigade", "Depot Jäger", "",
                      units=[u("ru-light-arty", "Foot Battery")],
                      regiments=[ru_jager_regiment("4th", small=True), ru_jager_regiment("20th", small=True), ru_jager_regiment("21st", small=True)]),
                  bde("ru-light-cavalry-brigade", "Cossacks", "", [u("ru-mounted-cossack", "Selivanov's Cossacks")])],
                 command=[cmd("ru-div-cmd", "Maj-Gen Löwis of Menar")],
                 notes=["The depot (second) battalions of three Jäger regiments, two each, with a Cossack regiment and a battery. Strengths differ: one account gives the detachment 2,000 men, another 3,000–4,000 and ten guns; the battalions are Small.",
                        "On its own it has none of the list's Infantry Brigades, which shows as a historical departure.",
                        "A staff-captain of the 4th Jäger was killed here; the church records of Gross-Eckau name him.",
                        "Staff Ratings are our judgement, at 7."])


# ---------------------------------------------------------------- Battles

def battle(id_, name, date, summary, forces):
    return {"id": id_, "name": name, "date": date, "campaign": "russia-1812", "summary": summary, "sources": SOURCES, "forces": forces}


ECKAU = battle(
    "eckau", "Eckau", "19 July 1812",
    "Macdonald's X Corps opened its campaign against Riga by driving the Russians out of Courland. At Eckau, south of Riga, Grawert's Prussians met the detachment Essen had sent out under Löwis: artillery and dragoons fixed it in front while Kleist's infantry came in from the east in the evening, and the Russians fell back on Riga.",
    [
        prussian_corps("eckau", "Gen-Lt von Grawert",
                       "The corps' first fight of the war. Grawert's guns opened in the morning and his dragoons charged, taking a standard before a counter-attack threw them back; in the evening Kleist's infantry turned the Russian flank and broke the defence of the manor at Eckau.",
                       ["About 7,000 men and 32 guns of the corps fought, under Grawert with Kleist leading the infantry; the sources don't say which battalions, so the whole corps is here. Take about half its infantry, with Hünerbein's dragoons."]),
        lowis("eckau", "Depot battalions and Cossacks sent out from Riga to hold the line of the Eckau. They held the manor and the crossing through the day until outflanked, and lost several hundred men, many taken, before falling back to Riga."),
    ],
)

MESOTEN = battle(
    "mesoten", "Mesoten", "29 September – 1 October 1812",
    "Reinforced by Steinheil's corps from Finland, the Russians came out of Riga in strength and pushed the Prussians back across Courland. Yorck turned on them: in three days of fighting along the Aa, at Mesoten, Gräfenthal, Lautschkrug and the Garosse, the Prussians threw the Finland Corps back with heavy losses in prisoners, and Steinheil withdrew to Riga.",
    [
        prussian_corps("mesoten", "Gen-Lt von Yorck",
                       "Yorck, now in command, gathered the corps and counter-attacked. On the 29th it crossed the Aa at Mesoten and drove Alexeyev's division back, while his 2nd and 3rd Brigades routed part of Rachmanov's at Gräfenthal; next day the cavalry caught Russian Jäger forming square at Lautschkrug, and on 1 October Jeanneret's advance guard pushed on over the Garosse.",
                       ["Riehn gives the corps 12,000 men and 16 guns at Lautschkrug, and about 16,000 for the whole series of actions; the corps is shown complete."]),
        alexeyev("mesoten", "The larger of Steinheil's two divisions, which had pushed south from Riga along the Aa. Attacked at Mesoten on the 29th, it fought hard along the river before falling back, and was driven on over the following days."),
        rachmanov("mesoten", "Steinheil's second division. Part of it was caught and routed at Gräfenthal on the 29th, and at Lautschkrug next day its Jäger were ridden down by Prussian cavalry, losing two battalions as prisoners."),
    ],
)


if __name__ == "__main__":
    for b in (ECKAU, MESOTEN):
        ratings.apply(b)
        art = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
        if b["id"] in art:
            b["art"] = art[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
