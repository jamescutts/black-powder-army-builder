"""
Writes Valutino (src/data/battles/valutino.json): Ney's III Corps and Gudin's division against the Russian rearguard
east of Smolensk.

    python3 scripts/forces/russia_1812_valutino.py && npm run check:forces

Sources (see SOURCES): Nafziger's Grande Armée of 15 August (812HDA) and Russian armies of 1812 (812XBA), with Wikipedia
for the course of the battle, which names the Russian III and IV Corps as the troops sent to reinforce Tuchkov.
"""

import copy
import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from russia_1812_centre import BAKHMETEV, CHOGLOKOV, KONOVNITSYN, RU_ORDER
from russia_1812_north import fr_regiment

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
FR, WT, RU = "france", "wurttemberg", "russia"
FR_ORDER = "After Nafziger's order of battle for the Grande Armée on 15 August, four days before the battle."


def naf(code, title):
    return {"label": f"{title} (Nafziger Collection {code})", "url": f"https://www.napoleon-series.org/nafzigger/{code}.pdf"}


def foreign(name, n, unit="fr-portuguese-infantry"):
    return {"name": name, "units": [u(unit, f"{['I', 'II'][i]}/{name}" if n > 1 else name) for i in range(n)]}


def guns(*regs):
    return [u("fr-regimental-battery" if four else "fr-regimental-arty-section", f"{n} Artillery Company") for n, four in regs]


def div_arty(foot, horse):
    return bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", foot), u("fr-horse-arty", horse)])


HORSE = "The horse battery, without three cavalry regiments in the force, shows as a historical departure."

GUDIN = force("valutino-gudin", FR, "Gudin's Division", "3rd Division, I Corps (Davout)", "French",
              "Lent to Ney for the attack, it led the final assault across the Stragan towards the crest in the evening; Gudin had both legs shattered by a round shot at its head and died three days later.",
              [bde("fr-infantry-brigade", "Desailly's Brigade", "Gén. de Brigade Desailly", units=guns(("7th Léger", True), ("12th Line", True)),
                   regiments=[fr_regiment("7th Léger", 5, light=True), fr_regiment("12th Line", 5)]),
               bde("fr-infantry-brigade", "Leclerc's Brigade", "Gén. de Brigade Leclerc", units=guns(("127th Line", False), ("21st Line", True)),
                   regiments=[fr_regiment("127th Line", 2), fr_regiment("21st Line", 5), foreign("Mecklenburg-Strelitz Battalion", 1, "fr-rheinbund-infantry")]),
               div_arty("3/7th Foot Artillery", "4/3rd Horse Artillery")],
              command=[cmd("fr-div-cmd", "Gén. de Division Gudin")],
              notes=[FR_ORDER, "Each regiment had its own two or four 3-pdrs, shown as Regimental Artillery.",
                     "Leclerc's brigade mixes a regimental battery with a section, and ten line battalions in a brigade is the list's limit; with the Mecklenburgers it has more. " + HORSE])

RAZOUT = force("valutino-razout", FR, "Razout's Division", "11th Division, III Corps (Ney)", "French",
               "Ney's leading division, which crossed the Stragan under the Russian guns in the afternoon and fought its way up towards the crest of the plateau.",
               [bde("fr-infantry-brigade", "Joubert's Brigade", "Gén. de Brigade Joubert", units=guns(("4th Line", False), ("18th Line", False)),
                    regiments=[fr_regiment("4th Line", 4), fr_regiment("18th Line", 4)]),
                bde("fr-infantry-brigade", "Compère's Brigade", "Gén. de Brigade Compère", regiments=[foreign("2nd Portuguese", 2)]),
                bde("fr-infantry-brigade", "d'Henin's Brigade", "Gén. de Brigade d'Henin", units=guns(("93rd Line", False)), regiments=[fr_regiment("93rd Line", 4)]),
                div_arty("18/5th Foot Artillery", "6/5th Horse Artillery")],
               command=[cmd("fr-div-cmd", "Gén. de Division Razout")],
               notes=[FR_ORDER, "The 2nd Portuguese, of the Portuguese Legion, is shown as the list's Portuguese infantry.", HORSE])

LEDRU = force("valutino-ledru", FR, "Ledru's Division", "10th Division, III Corps (Ney)", "French",
              "Beside Razout's, in the attacks across the stream and up the slopes through the afternoon.",
              [bde("fr-infantry-brigade", "Gengoult's Brigade", "Gén. de Brigade Gengoult", units=guns(("24th Line", False)),
                   regiments=[fr_regiment("24th Line", 4), foreign("1st Portuguese", 2)]),
               bde("fr-infantry-brigade", "Marion's Brigade", "Gén. de Brigade Marion", units=guns(("46th Line", False)), regiments=[fr_regiment("46th Line", 4)]),
               bde("fr-infantry-brigade", "Bruny's Brigade", "Gén. de Brigade Bruny", units=guns(("72nd Line", False)), regiments=[fr_regiment("72nd Line", 4)]),
               div_arty("12/5th Foot Artillery", "5/6th Horse Artillery")],
              command=[cmd("fr-div-cmd", "Gén. de Division Ledru")],
              notes=[FR_ORDER, "The 1st Portuguese, of the Portuguese Legion, is shown as the list's Portuguese infantry.", HORSE])


def wt_reg(name):
    return {"name": name, "units": [u("wt-line-infantry", f"{r}/{name}", options=["small-infantry"]) for r in ("I", "II")]}


MARCHAND = force("valutino-marchand", WT, "Marchand's Württembergers", "25th Division, III Corps (Ney)", "Württemberg",
                 "The Württemberg division, worn down by the march, which supported Ney's attacks and helped storm the crest at the end of the day.",
                 [bde("wt-infantry-brigade", "Hügel's Brigade", "Gen-Maj von Hügel", regiments=[wt_reg("1st Line 'Prinz Paul'"), wt_reg("4th Line")]),
                  bde("wt-infantry-brigade", "Koch's Brigade", "Gen-Maj Koch", regiments=[wt_reg("2nd Line 'Herzog Wilhelm'"), wt_reg("6th Line 'Kronprinz'")]),
                  bde("wt-light-infantry-brigade", "Brusselle's Light Brigade", "Gen-Maj von Brusselle",
                      [u("wt-light-infantry", "1st Light Bn", options=["small-infantry"]), u("wt-light-infantry", "2nd Light Bn", options=["small-infantry"]),
                       u("wt-jagers", "1st Jäger Bn 'König'", options=["small-infantry"]), u("wt-jagers", "2nd Jäger Bn", options=["small-infantry"])]),
                  bde("wt-divisional-artillery", "Divisional Artillery",
                      units=[u("wt-light-arty", "1st Foot Battery"), u("wt-light-arty", "2nd Foot Battery"), u("wt-heavy-arty", "12-pdr Foot Battery")])],
                 command=[{"unit": "fr-cmd-marchand"}],
                 notes=["Marchand, who had taken over from the Crown Prince, is the book's named commander.", FR_ORDER,
                        "Nafziger's return gives each two-battalion regiment between 400 and 850 men, so every battalion is Small.",
                        "Two foot batteries, where the list allows one for this many battalions, show as a historical departure."])

STROGANOV = force("valutino-stroganov", RU, "Stroganov's Grenadiers", "1st Grenadier Division, III Corps (Tuchkov)", "Russian",
                  "Sent up by Yermolov with the rest of the III Corps to reinforce Tuchkov's rearguard, the grenadiers held the crest above the Stragan against the evening attacks.",
                  [bde("ru-grenadier-brigade", "Tsvilenev's Brigade", "Maj-Gen Tsvilenev", units=[u("ru-position-arty", "1st Position Battery")],
                       regiments=[{"name": f"{r} Grenadiers", "units": [u("ru-grenadier", f"I/{r} Grenadiers"), u("ru-grenadier", f"II/{r} Grenadiers")]} for r in ("Pavlovsky", "Ekaterinoslav")]),
                   bde("ru-grenadier-brigade", "Zheltukhin's Brigade", "Maj-Gen Zheltukhin", units=[u("ru-light-arty", "1st Light Battery")],
                       regiments=[{"name": f"{r} Grenadiers", "units": [u("ru-grenadier", f"I/{r} Grenadiers"), u("ru-grenadier", f"II/{r} Grenadiers")]} for r in ("Arakcheyev", "Leib")]),
                   bde("ru-grenadier-brigade", "Fock's Brigade", "Maj-Gen Fock", units=[u("ru-light-arty", "2nd Light Battery")],
                       regiments=[{"name": f"{r} Grenadiers", "units": [u("ru-grenadier", f"I/{r} Grenadiers"), u("ru-grenadier", f"II/{r} Grenadiers")]} for r in ("St Petersburg", "Tauride")])],
                  command=[{"unit": "ru-cmd-stroganov"}],
                  notes=["Stroganov is the book's named commander.", RU_ORDER, "Three Grenadier Brigades where the list takes one show as a historical departure."])


def again(f, id_, formation, summary):
    g = copy.deepcopy(f)
    g["id"], g["formation"], g["summary"] = id_, formation, summary
    return g


VALUTINO = {
    "id": "valutino", "name": "Valutino", "date": "19 August 1812", "campaign": "russia-1812",
    "summary": "Ney, pushing east from burning Smolensk, ran into the Russian rearguard on the plateau beyond the Stragan stream at Lubino, covering Barclay's army as it struggled onto the Moscow road. All afternoon the French attacked across the marshy ground while Junot's corps, close on the Russian flank, never moved. In the evening Gudin's division carried the crest, Gudin falling at its head, but Barclay's army had got clear.",
    "sources": [naf("812HDA", "French Grande Armée, 15 August 1812"), naf("812XBA", "Russian Armies at the beginning of the 1812 Campaign"),
                {"label": "Battle of Valutino (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Valutino"}],
    "forces": [
        GUDIN, RAZOUT, LEDRU, MARCHAND,
        again(KONOVNITSYN, "valutino-konovnitsyn", "3rd Division, III Corps (Tuchkov)",
              "Part of the III Corps that Yermolov sent to Tuchkov's rearguard; it held the line of the Stragan through the afternoon."),
        STROGANOV,
        again(CHOGLOKOV, "valutino-choglokov", "11th Division, IV Corps (Ostermann-Tolstoy)",
              "Sent up with Ostermann's IV Corps to hold the crest as Ney's attacks grew stronger in the evening."),
        again(BAKHMETEV, "valutino-bakhmetev", "23rd Division, IV Corps (Ostermann-Tolstoy)",
              "The other half of Ostermann's corps, in the line on the plateau as the last French assault came in."),
    ],
}
for f in VALUTINO["forces"]:
    if f["side"] == "Württemberg":
        f["side"] = "French"


if __name__ == "__main__":
    art = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
    for b in (VALUTINO,):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in art:
            b["art"] = art[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
