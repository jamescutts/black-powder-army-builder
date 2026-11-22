"""
Writes the battles of the retreat from Moscow (src/data/battles/{vyazma,krasnoi}.json).

    python3 scripts/forces/russia_1812_retreat.py && npm run check:forces

By November neither army looked much like its order of battle: the French divisions were a few hundred to a few
thousand men, the Russian regiments far below strength. The formations here are those that fought, as Nafziger gives
them earlier in the campaign (812ICA, 812ICB, 812HAB, 812HDA), with Wikipedia for who fought where; each force's notes
say so. Summaries are our own words.
"""

import copy
import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from russia_1812_autumn import BROUSSIER, EUGEN, OLSUFIEV, PINO, PONIATOWSKI_16, naf
from russia_1812_centre import CHOGLOKOV, COMPANS, DESSAIX, KOLUBAKIN, KONOVNITSYN, PASKEVICH
from russia_1812_valutino import RAZOUT, STROGANOV

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
FIG, RU = "french-imperial-guard", "russia"
WASTED = ("By now the French divisions were a fraction of their strength, a few hundred to a few thousand men; "
          "the formation is as Nafziger gives it earlier in the campaign, so mark battalions Small or leave some out to suit.")
WORN = "The Russian regiments too were far below strength; the formation is as Nafziger gives it at Borodino."


def again(f, battle, summary, wasted=WASTED, formation=None):
    g = copy.deepcopy(f)
    g["id"] = f"{battle}-{f['id'].split('-', 1)[1]}"
    g["summary"] = summary
    if formation:
        g["formation"] = formation
    g["notes"] = [wasted] + [n for n in g["notes"] if "After Nafziger" not in n and "Borodino, six weeks" not in n]
    if g["side"] in ("Polish", "Italian"):
        g["side"] = "French"
    return g


# ================================================================ Vyazma, 3 November 1812

PLATOV = force("vyazma-platov", RU, "Platov's Cossacks", "Cossack Corps", "Russian",
               "Platov's Cossacks had dogged Davout's rearguard all the way from Maloyaroslavets; at Vyazma they pressed its rear while Miloradovich struck its flank.",
               [bde("ru-cossack-brigade", "Don Cossacks", "", [u("ru-mounted-cossack", f"{n} Cossacks") for n in ("Ataman", "Ilovaisky V's", "Kharitonov's", "Denisov VII's", "Grekov XVIII's", "Zhirov's")]),
                bde("ru-light-cavalry-brigade", "Don Horse Artillery", "", [u("ru-mounted-cossack", "Platov's escort Cossacks"), u("ru-horse-arty", "2nd Don Horse Battery")])],
               command=[{"unit": "ru-cmd-platov"}],
               notes=["Platov is the book's named commander.", "The regiments are those Nafziger gives Platov at Borodino.",
                      "No Infantry Brigade shows as a historical departure."])

VYAZMA = {
    "id": "vyazma", "name": "Vyazma", "date": "3 November 1812", "campaign": "russia-1812",
    "summary": "Davout's I Corps, the rearguard of the retreating army, had fallen far behind when Miloradovich's advance guard struck the road between it and Eugène's and Ney's corps before Vyazma. Eugène and Poniatowski turned back to open the way, and the French fought their way through to the town; Paskevich's and Choglokov's men stormed into Vyazma behind them as it burned, and the French lost some 6,000 men, and their order.",
    "sources": [naf("812ICB", "Russian Army, Battle of Borodino, 5–7 September 1812"), naf("812ICA", "French Army, Battle of Borodino, 5–7 September 1812"),
                {"label": "Battle of Vyazma (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Vyazma"}],
    "forces": [
        again(COMPANS, "vyazma", "Davout's rearguard division, cut off from the rest of the army when Miloradovich's cavalry came down on the road; it fought its way forward to Vyazma as the Russians pressed on all sides."),
        again(DESSAIX, "vyazma", "Davout's other division in the rearguard, fighting through to the town beside Compans's.", formation="4th Division, I Corps (Davout)"),
        again(BROUSSIER, "vyazma", "Eugène turned back to open the road for Davout, and Broussier's division held off Miloradovich's attacks on the flank."),
        again(PINO, "vyazma", "Pino's Italians, with Broussier's, held the road open for the rearguard to pass."),
        again(PONIATOWSKI_16, "vyazma", "Poniatowski's Poles came back with Eugène to help clear the road and held the heights beside it."),
        again(RAZOUT, "vyazma", "Ney's corps held Vyazma itself and fought as the rearguard in the burning town before taking over the rearguard of the whole army."),
        again(EUGEN, "vyazma", "Miloradovich's advance guard, it came down on the road between Davout and Eugène in the morning and cut the French columns.", wasted=WORN),
        again(OLSUFIEV, "vyazma", "Beside Eugen's division in Miloradovich's attack on the road.", wasted=WORN),
        again(CHOGLOKOV, "vyazma", "Stormed into Vyazma with Paskevich's men in the afternoon, fighting through the burning streets.", wasted=WORN),
        again(PASKEVICH, "vyazma", "Led the storm of the town in the afternoon, driving Ney's rearguard out over the Vyazma river.", wasted=WORN),
        PLATOV,
    ],
}


# ================================================================ Krasnoi, 15–18 November 1812

ROGUET = force("krasnoi-roguet", FIG, "Roguet's Young Guard", "2nd Division, Imperial Guard", "French",
               "With Kutuzov's army closing on the road at Krasnoi, Napoleon sent the Young Guard out in the night of 16 November to attack the Russians at Uvarovo; they drove Golitsyn's men back, and on the 17th stood in the snow before the town to hold the road open for Davout, losing half their strength.",
               [bde("fig-young-guard-brigade", "Lanabère's Brigade", "Gén. de Brigade Lanabère",
                    regiments=[{"name": "1st Tirailleurs", "units": [u("fig-yg-tirailleurs", "I/1st Tirailleurs"), u("fig-yg-tirailleurs", "II/1st Tirailleurs")]},
                               {"name": "1st Voltigeurs", "units": [u("fig-yg-voltigeurs", "I/1st Voltigeurs"), u("fig-yg-voltigeurs", "II/1st Voltigeurs")]}],
                    units=[u("fig-yg-foot-arty", "3rd Young Guard Foot Artillery")]),
                bde("fig-young-guard-brigade", "Boyeldieu's Brigade", "Gén. de Brigade Boyeldieu",
                    regiments=[{"name": "Fusilier-Grenadiers", "units": [u("fig-fusilier-grenadiers", "I/Fusilier-Grenadiers"), u("fig-fusilier-grenadiers", "II/Fusilier-Grenadiers")]},
                               {"name": "Fusilier-Chasseurs", "units": [u("fig-fusilier-chasseurs", "I/Fusilier-Chasseurs"), u("fig-fusilier-chasseurs", "II/Fusilier-Chasseurs")]}],
                    units=[u("fig-yg-foot-arty", "3rd Old Guard Foot Artillery")])],
               command=[cmd("fig-div-cmd", "Gén. de Division Roguet")],
               notes=["After Nafziger's order of battle for Borodino, which gives Roguet's division these four regiments. " + WASTED,
                      "The Guard batteries are shown as Young Guard foot artillery."])

CURIAL = force("krasnoi-curial", FIG, "The Old Guard", "3rd Division, Imperial Guard (Curial)", "French",
               "Napoleon marched with the Old Guard on the 17th to stand beside the Young Guard before Krasnoi, saying he had played the Emperor long enough and must now be the general. The Russians did not press it home.",
               [bde("fig-old-guard-brigade", "Boyer's Brigade", "Gén. de Brigade Boyer",
                    regiments=[{"name": "1st Chasseurs à Pied", "units": [u("fig-old-guard-chasseurs", "I/1st Chasseurs à Pied"), u("fig-old-guard-chasseurs", "II/1st Chasseurs à Pied")]},
                               {"name": "2nd Chasseurs à Pied", "units": [u("fig-middle-guard-chasseurs", "I/2nd Chasseurs à Pied"), u("fig-middle-guard-chasseurs", "II/2nd Chasseurs à Pied")]}],
                    units=[u("fig-og-foot-arty", "2nd Old Guard Foot Artillery")]),
                bde("fig-old-guard-brigade", "Michel's Brigade", "Gén. de Brigade Michel",
                    regiments=[{"name": "1st Grenadiers à Pied", "units": [u("fig-old-guard-grenadiers", "I/1st Grenadiers à Pied"), u("fig-old-guard-grenadiers", "II/1st Grenadiers à Pied")]},
                               {"name": "2nd Grenadiers à Pied", "units": [u("fig-middle-guard-grenadiers", "I/2nd Grenadiers à Pied"), u("fig-middle-guard-grenadiers", "II/2nd Grenadiers à Pied")]},
                               {"name": "3rd Grenadiers à Pied", "units": [u("fig-middle-guard-grenadiers", "I/3rd Grenadiers à Pied"), u("fig-middle-guard-grenadiers", "II/3rd Grenadiers à Pied")]}])],
               command=[cmd("fig-div-cmd", "Gén. de Division Curial")],
               notes=["After Nafziger's order of battle for Borodino. The list takes one Old Guard regiment a brigade; the 2nd Chasseurs and the 2nd and 3rd (Dutch) Grenadiers are shown as its Middle Guard.",
                      "The Old Guard had kept its numbers better than any other corps; it was still some 6,000 strong."])

KRASNOI = {
    "id": "krasnoi", "name": "Krasnoi", "date": "15–18 November 1812", "campaign": "russia-1812",
    "summary": "Four days of running fights as the retreating army passed Krasnoi, west of Smolensk, with Kutuzov's army alongside the road. The Young Guard's night attack at Uvarovo and its stand in the snow on the 17th, with the Old Guard behind it, held the road open for Eugène and Davout; Ney's rearguard, cut off, broke out north across the frozen Dnieper with a few hundred men.",
    "sources": [naf("812ICA", "French Army, Battle of Borodino, 5–7 September 1812"), naf("812ICB", "Russian Army, Battle of Borodino, 5–7 September 1812"),
                {"label": "Battle of Krasnoi (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Krasnoi"}],
    "forces": [
        ROGUET, CURIAL,
        again(COMPANS, "krasnoi", "Davout's corps came through on the 17th under fire from the Russian batteries on the heights, the Young Guard holding the road open for it."),
        again(RAZOUT, "krasnoi", "Ney's rearguard, a day behind, found the road blocked on the 18th; after a failed attack it slipped away north in the night and crossed the frozen Dnieper, Ney bringing a few hundred men of his 6,000 through to Orsha."),
        again(KONOVNITSYN, "krasnoi", "With Golitsyn's column, it barred the road west of Krasnoi on the 17th as the Guard held the town.", wasted=WORN),
        again(STROGANOV, "krasnoi", "Golitsyn's grenadiers, in the line facing the Young Guard on the 17th.", wasted=WORN),
        again(PASKEVICH, "krasnoi", "With Miloradovich's corps across the road on the 18th, it met Ney's attempt to break through and threw it back.", wasted=WORN),
        again(KOLUBAKIN, "krasnoi", "Beside Paskevich's division across the road on the 18th, where Ney's column was stopped.", wasted=WORN, formation="12th Division, VII Corps (Raevsky)"),
        again(EUGEN, "krasnoi", "Miloradovich's leading division, which cut the road ahead of Eugène's corps on the 16th and forced it to break through by night.", wasted=WORN),
    ],
}


if __name__ == "__main__":
    art = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
    for b in (VYAZMA, KRASNOI):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in art:
            b["art"] = art[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
