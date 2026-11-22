"""
Writes the cavalry fights of Bagration's retreat in July 1812 (src/data/battles/{mir,romanov}.json): Platov's
Cossack rearguard against Rożniecki's Polish light cavalry of Latour-Maubourg's reserve cavalry corps.

    python3 scripts/forces/russia_1812_cavalry.py && npm run check:forces

Sources (see SOURCES): Nafziger's orders of battle for both actions (812FAA, 812GAB), with Wikipedia's article
on Mir and Russian Wikipedia's on Romanovo (after Kharkevich, 1901) for who fought when. Summaries are our own
words. Staff Ratings are set by ratings.py: 8 unless a commander is one of the book's named ones.
"""

import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
NAFZIGER_MIR = {"label": "French and Russian Forces, Battle of Mir, 27–28 June 1812 (Nafziger Collection 812FAA)",
                "url": "https://www.napoleon-series.org/nafzigger/812FAA.pdf"}
NAFZIGER_ROMANOV = {"label": "French & Russian Forces, Battle of Romanov, 14 July 1812 (Nafziger Collection 812GAB)",
                    "url": "https://www.napoleon-series.org/nafzigger/812GAB.pdf"}
KHARKEVICH = {"label": "V. Kharkevich, Platov's actions in the rearguard of Bagration in 1812: the cavalry fights at Mir and Romanovo (1901)"}

FR, RU = "france", "russia"
POLISH_LIST = ("Rożniecki's division served in Latour-Maubourg's reserve cavalry corps of the Grande Armée, so it is built "
               "from the French list, whose light cavalry brigades take Polish Uhlans; the Grand Duchy of Warsaw's list "
               "allows only two regiments a brigade.")
CAVALRY_ONLY = "A cavalry force on its own has none of the list's Infantry Brigades, which shows as a historical departure."


def don(name, **kw):
    return u("ru-mounted-cossack", f"{name} Cossacks", **kw)


def irregular(name, **kw):
    return u("ru-irregular-mounted-cossack", name, **kw)


def vasilchikov(regiments, horse=True):
    """The regular cavalry lent from Raevsky's VII Corps, with the Don horse battery"""
    return bde("ru-light-cavalry-brigade", "Vasilchikov's Cavalry", "Maj-Gen Vasilchikov",
               regiments + ([u("ru-horse-arty", "2nd Don Horse Battery")] if horse else []))


# ---------------------------------------------------------------- Mir, 9–10 July 1812

MIR_POLES = force("mir-rozniecki", FR, "Rożniecki's Polish Lancers", "4th Light Cavalry Division, IV Reserve Cavalry Corps (Latour-Maubourg)",
                  "Polish",
                  "The lancers of the Grande Armée's right wing, riding ahead of Jérôme's army after Bagration. They came on brigade by brigade down the road to Mir, into an ambush: Turno's brigade was drawn in on the first day, and on the second the rest of the division was fed in piecemeal, surrounded by Cossacks and driven back, until Tyszkiewicz's brigade covered the retreat.",
                  [bde("fr-light-cavalry-brigade", "Dziewanowski's Brigade", "Gén. de Brigade Dziewanowski",
                       [u("fr-polish-uhlan", "2nd Uhlans"), u("fr-polish-uhlan", "7th Uhlans"), u("fr-polish-uhlan", "11th Uhlans")]),
                   bde("fr-light-cavalry-brigade", "Turno's Brigade", "Gén. de Brigade Turno",
                       [u("fr-polish-uhlan", "3rd Uhlans"), u("fr-polish-uhlan", "15th Uhlans"), u("fr-polish-uhlan", "16th Uhlans")])],
                  command=[cmd("fr-div-cmd", "Gén. de Division Rożniecki")],
                  notes=[POLISH_LIST,
                         "The two brigades of three regiments each, three squadrons apiece, about 4,000 men, follow Nafziger. Wikipedia adds the 12th Uhlans, the 4th Chasseurs and a horse battery, and Tyszkiewicz's brigade, which covered the retreat; add them if you like.",
                         CAVALRY_ONLY + " So do its two Light Cavalry Brigades without the two Infantry Brigades each needs."])

MIR_RUSSIANS = force("mir-platov", RU, "Platov's Rearguard", "Rearguard of the 2nd Army of the West (Bagration)", "Russian",
                     "Platov's Cossacks covered Bagration's retreat. He left a thin screen at Mir with ambushes on either side of the road, let the Polish lancers ride in, and fell on them from all sides; on the second day Vasilchikov's hussars and dragoons came up and the fighting ran on for six hours to Simiakovo before the Poles broke.",
                     [bde("ru-cossack-brigade", "Krasnov's Detachment", "Maj-Gen Krasnov",
                          [don("Sysoev's"), don("Ilovaisky's"), irregular("Stavropol Kalmyks"), irregular("Perekop Tatars"),
                           don("Ataman", options=["small-cavalry"])]),
                      bde("ru-cossack-brigade", "Kuteinikov's Brigade", "Maj-Gen Kuteinikov",
                          [irregular("Simferopol Tatars"), don("Balabin's"), don("Grekov's"), don("Ataman", options=["small-cavalry"])]),
                      vasilchikov([u("ru-hussar", "Akhtyrka Hussars"), u("ru-dragoon", "Kiev Dragoons")])],
                     command=[{"unit": "ru-cmd-platov"}],
                     notes=["Platov is the book's named commander.",
                            "After Nafziger: Krasnov's and Kuteinikov's Cossacks, each with half the Ataman regiment (four sotnias, so Small), and the Akhtyrka Hussars and Kiev Dragoons with the 2nd Don Horse Battery from Raevsky's VII Corps. The Tatar and Kalmyk regiments are the list's Irregular Cossacks.",
                            "Wikipedia's figures (about 8,500 men, 3,500 on the first day) add the New Russia Dragoons, the Lithuanian Uhlans and the 5th Jäger, who came up on the second day; add them as reinforcements if you like.",
                            "Two Cossack Brigades, where the list allows one, and no Infantry Brigade, show as historical departures."])

MIR = {"id": "mir", "name": "Mir", "date": "9–10 July 1812", "campaign": "russia-1812",
       "summary": "The first cavalry fight of the invasion. Platov's Cossacks, covering Bagration's retreat, drew Rożniecki's Polish lancers into an ambush around the town of Mir: they let the leading brigade ride through a thin screen and fell on it from all sides, and next day, reinforced by regular cavalry, beat the rest of the division as it came up, driving it back with heavy loss.",
       "sources": [NAFZIGER_MIR, {"label": "Battle of Mir (1812) (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Mir_(1812)"}, KHARKEVICH],
       "forces": [MIR_POLES, MIR_RUSSIANS]}


# ---------------------------------------------------------------- Romanovo, 14 July 1812

ROMANOV_POLES = force("romanov-przebendowski", FR, "Przebendowski's Chasseurs", "From Rożniecki's division, IV Reserve Cavalry Corps (Latour-Maubourg)",
                      "Polish",
                      "Sent to seize the crossing of the Moroch at Romanovo, the regiment halted before the village and reported the Cossacks ahead, but its messenger said 500 for 5,000. Platov, seeing how few came on, attacked: three charges were beaten off by carbine fire from squadrons drawn up in echelon, the fourth broke the regiment, and a squadron of the 12th Uhlans and two of Sułkowski's guns checked the pursuit.",
                      [bde("fr-light-cavalry-brigade", "Przebendowski's Command", "Col Przebendowski",
                           [u("fr-chasseur-a-cheval", "1st Polish Chasseurs à Cheval"), u("fr-polish-uhlan", "Squadron, 12th Uhlans", options=["small-cavalry"])])],
                      command=[cmd("fr-div-cmd", "Gén. de Division Latour-Maubourg")],
                      notes=[POLISH_LIST,
                             "About 800 horse: the 1st Polish Chasseurs à Cheval under Colonel Przebendowski, with a squadron of the 12th Uhlans (Small). Nafziger gives the French 1st Chasseurs à Cheval under Colonel Méda, 950 men; the Russian accounts, after Kharkevich, make it the Polish regiment, as here.",
                             "Rożniecki's and Kamieński's divisions, with Tyszkiewicz's brigade and a horse battery, came up only after the fight, when Platov had crossed the river and burned the bridge.",
                             CAVALRY_ONLY + " So does its Light Cavalry Brigade without the two Infantry Brigades it needs."])

ROMANOV_RUSSIANS = force("romanov-platov", RU, "Platov's Rearguard", "Rearguard of the 2nd Army of the West (Bagration)", "Russian",
                         "Ordered to hold Romanovo until the next evening so Bagration's baggage could get away to Mozyr, Platov hid four Cossack regiments across the Moroch, then struck the Polish chasseurs when they came on alone. The fourth charge broke them, taking some 350 prisoners, and when Latour-Maubourg's divisions came up Platov was back over the river with the bridge burned.",
                         [bde("ru-cossack-brigade", "Kuteinikov's Brigade", "Maj-Gen Kuteinikov",
                              [irregular("Simferopol Tatars"), don("Balabin's"), don("Grekov's"), don("Ataman")]),
                          bde("ru-cossack-brigade", "Krasnov's Detachment", "Maj-Gen Krasnov",
                              [don("Ilovaisky's"), don("Karpov's")]),
                          vasilchikov([u("ru-hussar", "Akhtyrka Hussars"), u("ru-uhlan", "Lithuanian Uhlans"), u("ru-dragoon", "Kiev Dragoons")]),
                          bde("ru-jager-brigade", "5th Jäger", "", regiments=[{"name": "5th Jäger", "units": [u("ru-jager", "1st Bn, 5th Jäger"), u("ru-jager", "2nd Bn, 5th Jäger")]}])],
                         command=[{"unit": "ru-cmd-platov"}],
                         notes=["Platov is the book's named commander.",
                                "Nafziger gives Platov's whole rearguard, as here. The Russian accounts put five Cossack regiments, about 2,500 horse, in the fight itself, and send Karpov's two regiments off towards Timkovichi earlier in the day; for the fight, take Kuteinikov's brigade and one more Cossack regiment.",
                                "Vasilchikov's regulars and the 5th Jäger held the river line, the Jäger's fire covering the crossing as the Polish divisions came up.",
                                "Two Cossack Brigades where the list allows one, and a Jäger Brigade with one regiment where it needs two, show as historical departures."])

ROMANOV = {"id": "romanov", "name": "Romanovo", "date": "14 July 1812", "campaign": "russia-1812",
           "summary": "Platov's second blow at the Polish cavalry following Bagration. At the crossing of the Moroch at Romanovo, south of Slutsk, a single regiment of Polish chasseurs came on ahead of Latour-Maubourg's corps, misled by a report that made 5,000 Cossacks 500. It beat off three charges in good order before the fourth broke it, and Platov was back across the river, the bridge burning, before the Polish divisions arrived.",
           "sources": [NAFZIGER_ROMANOV, {"label": "Бой при Романово (Russian Wikipedia)", "url": "https://ru.wikipedia.org/wiki/%D0%91%D0%BE%D0%B9_%D0%BF%D1%80%D0%B8_%D0%A0%D0%BE%D0%BC%D0%B0%D0%BD%D0%BE%D0%B2%D0%BE_(1812)"}, KHARKEVICH],
           "forces": [ROMANOV_POLES, ROMANOV_RUSSIANS]}


if __name__ == "__main__":
    art = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
    for b in (MIR, ROMANOV):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in art:
            b["art"] = art[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
