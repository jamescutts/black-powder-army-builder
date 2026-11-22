"""
Writes the southern flank of the 1812 campaign (src/data/battles/{kobrin,gorodechno}.json): Tormasov's Third
Army against Reynier's Saxons and, at Gorodechno, Schwarzenberg's Austrians.

    python3 scripts/forces/russia_1812_south.py && npm run check:forces

Sources (see SOURCES): Nafziger's orders of battle for both (812GBG, 812HBJ). Summaries are our own words.
Staff Ratings are set by ratings.py: 8 unless a commander is one of the book's named ones.
"""

import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from russia_1812 import ru_jager_regiment, ru_regiment

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
NAFZIGER_KOBRIN = {"label": "Order of Battle for Kobrin, 27 July 1812 (Nafziger Collection 812GBG)",
                   "url": "https://www.napoleon-series.org/nafzigger/812GBG.pdf"}
NAFZIGER_GORODECHNO = {"label": "Battle of Gorodetchna, 12 August 1812 (Nafziger Collection 812HBJ)",
                       "url": "https://www.napoleon-series.org/nafzigger/812HBJ.pdf"}
SAX, AT, RU = "saxony", "austria", "russia"
ASSUMED_RU = "Nafziger doesn't give every regiment's battalions; two field battalions each are shown, the usual for 1812."


def sax_line(name, n=2):
    return {"name": f"{name} Infantry", "units": [u("sax-musketeer", f"{['I', 'II'][i]}/{name}") for i in range(n)]}


def sax_light(name):
    return {"name": name, "units": [u("sax-light-infantry", f"{r}/{name}") for r in ("I", "II")]}


def at_regiment(name, hungarian=False, n=2):
    unit = "at-infantry-hungarian" if hungarian else "at-infantry-german"
    return {"name": f"{name} Infantry", "units": [u(unit, f"{['I', 'II'][i]}/{name}") for i in range(n)]}


# ---------------------------------------------------------------- Kobrin, 27 July 1812

KLENGEL = force("kobrin-klengel", SAX, "Klengel's Brigade", "22nd Division (Funck), VII Corps (Reynier)", "Saxon",
                "Left alone at Kobrin to watch the Mukhavets crossings while Reynier's corps was strung out to the west, the brigade found Russian columns closing on every road. It barricaded the town and fought all day from its houses and the old fort, until, with the town burning and its ammunition spent, Klengel surrendered with some 2,300 men.",
                [bde("sax-infantry-brigade", "Klengel's Brigade", "Gen-Maj von Klengel",
                     units=[u("sax-regimental-arty", "König Regimental Battery"), u("sax-regimental-arty", "Niesemeuschel Regimental Battery")],
                     regiments=[sax_line("König"), sax_line("von Niesemeuschel")]),
                 bde("sax-cavalry-brigade", "Prinz Clemens Uhlans", "",
                     [u("sax-uhlan", "Prinz Clemens Uhlans", options=["small-cavalry"])])],
                command=[cmd("sax-div-cmd", "Gen-Maj von Klengel")],
                notes=["After Nafziger: the König and Niesemeuschel regiments, two battalions each, with their two regimental batteries of four 4-pdrs, and three squadrons of the Prinz Clemens Uhlans (Small).",
                       "A Cavalry Brigade of a single regiment is within the list; the uhlans fought and surrendered alongside the infantry."])

TORMASOV_KOBRIN = force("kobrin-tormasov", RU, "Tormasov's Columns", "Third Army of the West", "Russian",
                        "Tormasov, coming north from Volhynia, closed on Kobrin from three sides at once: Madatov's hussars from the north on the Pruzhany road, the Pavlograd Hussars and 13th Jäger from the west, and dragoons and two Jäger regiments from the south. They cut the Saxons off and pressed into the town street by street until it surrendered.",
                        [bde("ru-jager-brigade", "The Jäger", "",
                             regiments=[ru_jager_regiment("10th"), ru_jager_regiment("13th"), ru_jager_regiment("14th")]),
                         bde("ru-light-cavalry-brigade", "Hussars and Uhlans", "Lt-Col Madatov",
                             [u("ru-hussar", "Alexandria Hussars"), u("ru-hussar", "Pavlograd Hussars", options=["large-cavalry"]),
                              u("ru-uhlan", "Tatar Uhlans", options=["small-cavalry"])]),
                         bde("ru-heavy-cavalry-brigade", "The Dragoons", "",
                             [u("ru-dragoon", "Starodub Dragoons"), u("ru-dragoon", "Tver Dragoons", options=["small-cavalry"])])],
                        command=[cmd("ru-div-cmd", "Gen of Cavalry Tormasov")],
                        notes=["After Nafziger, who gives the troops by the road they came on: from the north the Alexandria Hussars (four squadrons, in two waves), the Starodub Dragoons and Tatar Uhlans; from the west the Pavlograd Hussars (eight squadrons, so Large) and the 13th Jäger; from the south the Starodub and Tver Dragoons and the 10th and 14th Jäger. A Cossack sotnia with Madatov is left out.",
                               "Single squadrons make the Tatar Uhlans and the Tver Dragoons (two squadrons) Small. " + ASSUMED_RU,
                               "Nafziger names no guns; Tormasov's batteries shelled the town, so add a Light Battery to the Jäger if you like.",
                               "No Infantry Brigade shows as a historical departure."])

KOBRIN = {"id": "kobrin", "name": "Kobrin", "date": "27 July 1812", "campaign": "russia-1812",
          "summary": "The first Russian victory of the war on the southern flank. Reynier's Saxon VII Corps was spread thin across Volhynia when Tormasov's Third Army came north. At Kobrin his columns closed on Klengel's brigade from three sides; the Saxons held the burning town all day, but with no relief coming Klengel surrendered with his whole brigade.",
          "sources": [NAFZIGER_KOBRIN], "forces": [KLENGEL, TORMASOV_KOBRIN]}


# ---------------------------------------------------------------- Gorodechno, 12 August 1812

TRAUTENBERG = force("gorodechno-trautenberg", AT, "Trautenberg's Division", "Austrian Auxiliary Corps (Schwarzenberg)", "Austrian",
                    "The corps' leading division, with Zechmeister's light troops and hussars out in front. It held the front facing the Russian position behind the marshes at Gorodechno while the Saxons worked round the flank.",
                    [bde("at-advanced-guard-brigade", "Zechmeister's Brigade", "Gen-Maj von Zechmeister",
                         [u("at-jager", "5th Jäger Bn"), u("at-grenz", "I/St Georg Grenz"), u("at-hussar", "Kienmayer Hussars")]),
                     bde("at-line-infantry-brigade", "Plöcher's Brigade", "Gen-Maj von Plöcher",
                         units=[u("at-6pdr-brigade-battery", "6-pdr Brigade Battery")],
                         regiments=[at_regiment("Duka"), at_regiment("Beaulieu")])],
                    command=[cmd("at-inf-div-cmd", "FML von Trautenberg")],
                    notes=["After Nafziger, who marks only Bianchi's Simbschen and Alvinczy regiments as Hungarian, so Duka and Beaulieu are shown as German.",
                           "Each division had a battery of eight 6-pdrs, shown here as its brigade battery; with only four line battalions, where the list wants six for each, it shows as a historical departure."])

BIANCHI = force("gorodechno-bianchi", AT, "Bianchi's Division", "Austrian Auxiliary Corps (Schwarzenberg)", "Austrian",
                "The corps' strongest division, with Liechtenstein's grenadiers. It was fed in on the left as Schwarzenberg and Reynier turned the Russian flank, and pressed Tormasov back off the heights at Podubno.",
                [bde("at-line-infantry-brigade", "Lilienberg's Brigade", "Gen-Maj von Lilienberg",
                     units=[u("at-6pdr-brigade-battery", "6-pdr Brigade Battery")],
                     regiments=[at_regiment("Simbschen", hungarian=True), at_regiment("Alvinczy", hungarian=True)]),
                 bde("at-line-infantry-brigade", "Hessen-Homburg's Brigade", "Gen-Maj Prince of Hessen-Homburg",
                     regiments=[at_regiment("Hiller"), at_regiment("Colloredo-Mansfeld")]),
                 bde("at-line-infantry-brigade", "Liechtenstein's Brigade", "Gen-Maj Prince Alois Liechtenstein",
                     units=[u("at-grenadier", "Kirchenbetter Grenadiers"), u("at-grenadier", "Brzeczinski Grenadiers")],
                     regiments=[at_regiment("Davidovich"), at_regiment("Esterházy")]),
                 bde("at-reserve-artillery", "Corps Reserve", units=[u("at-position-battery", "12-pdr Position Battery")])],
                command=[{"unit": "at-cmd-bianchi"}],
                notes=["Bianchi is the book's named commander.",
                       "After Nafziger, who marks Simbschen and Alvinczy as Hungarian; a brigade of two Hungarian regiments, where the list wants no more Hungarian than German, shows as a historical departure.",
                       "The corps reserve's 12-pdr battery is shown with this division."])

SIEGENTHAL = force("gorodechno-siegenthal", AT, "Siegenthal's Division", "Austrian Auxiliary Corps (Schwarzenberg)", "Austrian",
                   "The corps' third division, with Mohr's light brigade. It followed the advance round the Russian left and joined the push that drove Tormasov off the field in the evening.",
                   [bde("at-line-infantry-brigade", "Mayer's Brigade", "Gen-Maj von Mayer",
                        units=[u("at-6pdr-brigade-battery", "6-pdr Brigade Battery")],
                        regiments=[at_regiment("Sottulinski"), at_regiment("Prince de Ligne")]),
                    bde("at-line-infantry-brigade", "Mayer's Brigade (Czartoryski)", "Gen-Maj von Mayer",
                        regiments=[at_regiment("Czartoryski", n=1)]),
                    bde("at-advanced-guard-brigade", "Mohr's Brigade", "Gen-Maj von Mohr",
                        [u("at-grenz", "I/Warasdiner-Kreuzer Grenz"), u("at-jager", "7th Jäger Bn"),
                         u("at-hussar", "Hessen-Homburg Hussars")])],
                   command=[cmd("at-inf-div-cmd", "FML von Siegenthal")],
                   notes=["Mayer's brigade had three regiments, more than the list's brigade holds, so the single battalion of Czartoryski's is a brigade of its own here.",
                          "After Nafziger. The division's battery of eight 6-pdrs, with five line battalions where the list wants six, shows as a historical departure."])

FRIMONT = force("gorodechno-frimont", AT, "Frimont's Cavalry", "Austrian Auxiliary Corps (Schwarzenberg)", "Austrian",
                "The corps' cavalry division, six regiments of light horse and dragoons, which covered the flank march round the marshes and harried the Russian withdrawal.",
                [bde("at-light-cavalry-brigade", "Frölich's Brigade", "Gen-Maj von Frölich",
                     [u("at-chevauleger", "Hohenzollern Chevaulegers"), u("at-chevauleger", "O'Reilly Chevaulegers")]),
                 bde("at-light-cavalry-brigade", "Frölich's Brigade (Kaiser Hussars)", "Gen-Maj von Frölich",
                     [u("at-hussar", "Kaiser Hussars")]),
                 bde("at-light-cavalry-brigade", "Wrede's Brigade", "Gen-Maj von Wrede",
                     [u("at-hussar", "Blankenstein Hussars"), u("at-dragoon", "Riesch Dragoons")]),
                 bde("at-heavy-cavalry-brigade", "Wrede's Brigade (Levenehr Dragoons)", "Gen-Maj von Wrede",
                     [u("at-dragoon", "Levenehr Dragoons")])],
                command=[cmd("at-inf-div-cmd", "FML Frimont")],
                notes=["After Nafziger. Each of Frölich's and Wrede's brigades had three regiments, more than the list's light cavalry brigade holds, so the Kaiser Hussars and the Levenehr Dragoons are brigades of their own here.",
                       "Four cavalry brigades, where the list allows one of each kind, and no infantry, show as historical departures."])

LECOQ = force("gorodechno-lecoq", SAX, "Le Coq's Division", "21st Division, VII Corps (Reynier)", "Saxon",
              "Reynier's stronger division, with the corps' heavy guns. It led the march through the forest round the Russian left and, deployed across Tormasov's flank and rear, fought off the Russian counter-attacks through the afternoon.",
              [bde("sax-infantry-brigade", "Steindel's Brigade", "Gen-Maj von Steindel",
                   units=[u("sax-grenadier", "Liebenau Grenadiers"), u("sax-regimental-arty", "Prinz Friedrich Regimental Battery"),
                          u("sax-regimental-arty", "Prinz Clemens Regimental Battery"), u("sax-heavy-arty", "12-pdr Foot Battery von Brause")],
                   regiments=[sax_line("Prinz Friedrich August"), sax_line("Prinz Clemens")]),
               bde("sax-infantry-brigade", "Nostitz's Brigade", "Gen-Maj von Nostitz",
                   units=[u("sax-regimental-arty", "Prinz Anton Regimental Battery"), u("sax-foot-arty", "Foot Battery Rouvroy")],
                   regiments=[sax_line("Prinz Anton"), sax_light("1st Light Infantry")])],
              command=[{"unit": "sax-cmd-lecoq"}],
              notes=["Le Coq is the book's named commander.",
                     "After Nafziger. The division's horse battery, von Roth's, has no place in the list's infantry brigades, so it is left out; give it to Gablenz's cavalry with Funck's division if you like. The corps' 12-pdr battery von Brause is shown with Steindel.",
                     "Rouvroy's foot battery with Nostitz's four battalions, where the list wants six, shows as a historical departure."])

FUNCK = force("gorodechno-funck", SAX, "Funck's Division and Gablenz's Cavalry", "22nd Division and 23rd Light Cavalry Brigade, VII Corps (Reynier)", "Saxon",
              "What was left of the 22nd Division after Klengel's brigade was lost at Kobrin: Sahr's grenadiers and light infantry, with the corps' light cavalry under Gablenz, which rode round the Russian flank with the Austrian horse.",
              [bde("sax-grenadier-brigade", "Sahr's Brigade", "Gen-Maj von Sahr",
                   units=[u("sax-grenadier", "von Spiegel Grenadiers"), u("sax-grenadier", "von Anger Grenadiers"),
                          u("sax-foot-arty", "Foot Battery Bonniot")],
                   regiments=[sax_light("2nd Light Infantry")]),
               bde("sax-cavalry-brigade", "Gablenz's Brigade", "Gen-Maj von Gablenz",
                   [u("sax-hussar", "Saxon Hussars", options=["large-cavalry"]), u("sax-chevauleger", "Polenz Chevaulegers"),
                    u("sax-uhlan", "Prinz Clemens Uhlans"), u("sax-horse-arty", "2nd Horse Battery")])],
              command=[cmd("sax-div-cmd", "Gen-Lt von Funck")],
              notes=["After Nafziger. The Saxon Hussars had eight squadrons, so they are Large.",
                     "Klengel's brigade of this division had been taken at Kobrin a fortnight before.",
                     "Grenadiers and light infantry only, with no Saxon Infantry Brigade, and so a Cavalry Brigade with none to go with, show as historical departures."])

KAMENSKY = force("gorodechno-kamensky", RU, "Kamensky's Corps", "18th Division (Shcherbatov), Third Army of the West", "Russian",
                 "Tormasov's left, which found the Saxons coming out of the forest on its flank and rear. Kamensky turned to face them and held through the afternoon, his grenadiers and Jäger fighting off attack after attack until the army could fall back in the night.",
                 [bde("ru-infantry-brigade", "Bernados's Brigade", "Maj-Gen Bernados",
                      units=[u("ru-position-arty", "18th Position Battery")],
                      regiments=[ru_regiment("Tambov"), ru_regiment("Vladimir")]),
                  bde("ru-infantry-brigade", "Khovansky's Brigade", "Maj-Gen Prince Khovansky",
                      units=[u("ru-light-arty", "34th Light Battery")],
                      regiments=[ru_regiment("Dnieper"), ru_regiment("Kostroma")]),
                  bde("ru-jager-brigade", "Meshcherinov's Brigade", "Col Meshcherinov",
                      units=[u("ru-light-arty", "35th Light Battery")],
                      regiments=[ru_jager_regiment("28th"), ru_jager_regiment("32nd")]),
                  bde("ru-combined-grenadier-brigade", "Converged Grenadiers", "",
                      [u("ru-inf-combined-grenadier", "Converged Grenadiers, 9th Division"),
                       u("ru-inf-combined-grenadier", "Converged Grenadiers, 15th Division"),
                       u("ru-inf-combined-grenadier", "Converged Grenadiers, 18th Division")]),
                  bde("ru-light-cavalry-brigade", "Pavlograd Hussars", "",
                      [u("ru-hussar", "Pavlograd Hussars", options=["large-cavalry"]), u("ru-horse-arty", "11th Horse Battery")])],
                 command=[cmd("ru-div-cmd", "Gen of Infantry Count Kamensky")],
                 notes=["After Nafziger. The Pavlograd Hussars had eight squadrons, so they are Large. " + ASSUMED_RU,
                        "The 11th Horse Battery with the corps' one hussar regiment, where the list wants four cavalry regiments for each, shows as a historical departure."])

MARKOV_15 = force("gorodechno-nazimov", RU, "Nazimov's Division", "15th Division, Markov's Corps, Third Army of the West", "Russian",
                  "The 15th Division of Markov's corps, sent across to the threatened left as the Saxons came out on the flank, and part of the line that held there until dark.",
                  [bde("ru-infantry-brigade", "Oldekop's Brigade", "Maj-Gen Oldekop",
                       units=[u("ru-position-arty", "15th Position Battery")],
                       regiments=[ru_regiment("Kurin"), ru_regiment("Kolyvan")]),
                   bde("ru-infantry-brigade", "Stepanov's Brigade", "Maj-Gen Stepanov",
                       units=[u("ru-light-arty", "28th Light Battery")],
                       regiments=[ru_regiment("Kozlov"), ru_regiment("Vitebsk")]),
                   bde("ru-jager-brigade", "Vyazemsky's Brigade", "Maj-Gen Prince Vyazemsky",
                       units=[u("ru-light-arty", "29th Light Battery")],
                       regiments=[ru_jager_regiment("13th"), ru_jager_regiment("14th")])],
                  command=[cmd("ru-div-cmd", "Maj-Gen Nazimov")],
                  notes=["After Nafziger. " + ASSUMED_RU])

MARKOV_9 = force("gorodechno-udom", RU, "Udom's Division", "9th Division, Markov's Corps, Third Army of the West", "Russian",
                 "The 9th Division, which held the front facing the Austrians across the marshes at Gorodechno before being drawn into the fight on the left.",
                 [bde("ru-infantry-brigade", "Reichel's Brigade", "Maj-Gen Reichel",
                      units=[u("ru-position-arty", "9th Position Battery")],
                      regiments=[ru_regiment("Ryazhsk"), ru_regiment("Apsheron")]),
                  bde("ru-infantry-brigade", "Seliverstov's Brigade", "Maj-Gen Seliverstov",
                      units=[u("ru-light-arty", "16th Light Battery")],
                      regiments=[ru_regiment("Yakutsk"), ru_regiment("Nasheburg")]),
                  bde("ru-jager-brigade", "The Jäger", "",
                      units=[u("ru-light-arty", "17th Light Battery")],
                      regiments=[ru_jager_regiment("10th"), ru_jager_regiment("38th")]),
                  bde("ru-light-cavalry-brigade", "Madatov's Hussars", "Col Madatov",
                      [u("ru-hussar", "Alexandria Hussars", options=["large-cavalry"]), u("ru-horse-arty", "12th Horse Battery")])],
                 command=[cmd("ru-div-cmd", "Maj-Gen Udom")],
                 notes=["After Nafziger. The Alexandria Hussars had eight squadrons, so they are Large. " + ASSUMED_RU,
                       "The 12th Horse Battery with the division's one hussar regiment, where the list wants four cavalry regiments for each, shows as a historical departure."])

LAMBERT = force("gorodechno-lambert", RU, "Lambert's Cavalry", "Cavalry Corps, Third Army of the West", "Russian",
                "Tormasov's cavalry: two divisions of dragoons with the Tatar Uhlans, and a host of Cossacks, Bashkirs, Kalmyks and Tatars. It met the Austro-Saxon horse working round the flank and covered the army's withdrawal.",
                [bde("ru-heavy-cavalry-brigade", "Berdyaev's Brigade", "Maj-Gen Berdyaev",
                     [u("ru-dragoon", "Tver Dragoons"), u("ru-dragoon", "Starodub Dragoons")]),
                 bde("ru-heavy-cavalry-brigade", "Khrushchov's Brigade", "Maj-Gen Khrushchov",
                     [u("ru-dragoon", "Zhitomir Dragoons"), u("ru-dragoon", "Arzamas Dragoons")]),
                 bde("ru-light-cavalry-brigade", "Knorring's Brigade", "Maj-Gen Knorring",
                     [u("ru-uhlan", "Tatar Uhlans", options=["large-cavalry"])]),
                 bde("ru-heavy-cavalry-brigade", "Barkov's Brigade", "Maj-Gen Barkov",
                     [u("ru-dragoon", "Taganrog Dragoons"), u("ru-dragoon", "Vladimir Dragoons"), u("ru-dragoon", "Serpukhov Dragoons")]),
                 bde("ru-cossack-brigade", "Don Cossacks", "",
                     [u("ru-mounted-cossack", "Platov IV's Don Cossacks", options=["small-cavalry"]),
                      u("ru-mounted-cossack", "Barabanshchikov II's Don Cossacks", options=["small-cavalry"]),
                      u("ru-mounted-cossack", "Vlasov II's Don Cossacks", options=["small-cavalry"]),
                      u("ru-mounted-cossack", "Diachkin's Cossacks", options=["small-cavalry"])]),
                 bde("ru-cossack-brigade", "Bashkirs, Kalmyks and Tatars", "",
                     [u("ru-irregular-mounted-cossack", "2nd Bashkirs", options=["small-cavalry"]),
                      u("ru-irregular-mounted-cossack", "1st Kalmyks", options=["small-cavalry"]),
                      u("ru-irregular-mounted-cossack", "2nd Kalmyks", options=["small-cavalry"]),
                      u("ru-irregular-mounted-cossack", "Feodosia Tatars", options=["small-cavalry"]),
                      u("ru-irregular-mounted-cossack", "Evpatoria Tatars", options=["small-cavalry"])])],
                command=[cmd("ru-div-cmd", "Maj-Gen Count Lambert")],
                notes=["After Nafziger: the 5th Cavalry Division's dragoon brigades and Knorring's Tatar Uhlans (eight squadrons, so Large), and Chaplits's 8th Division dragoons under Barkov.",
                       "Nafziger gives the nine irregular regiments only thirty squadrons between them, so each is Small; they are two brigades here, more than one of the list's brigades holds.",
                       "More cavalry brigades of each kind than the list allows, and no infantry, show as historical departures."])

GORODECHNO = {"id": "gorodechno", "name": "Gorodechno", "date": "12 August 1812", "campaign": "russia-1812",
              "summary": "Reynier, reinforced by Schwarzenberg's Austrian corps, turned on Tormasov. While the Austrians held the Russians' front behind the marshes at Gorodechno, the Saxons marched round through the forest onto their left flank and rear. Tormasov swung his line round to face them and fought all afternoon, but at nightfall fell back, and the Third Army withdrew to the south.",
              "sources": [NAFZIGER_GORODECHNO],
              "forces": [TRAUTENBERG, BIANCHI, SIEGENTHAL, FRIMONT, LECOQ, FUNCK, KAMENSKY, MARKOV_15, MARKOV_9, LAMBERT]}


if __name__ == "__main__":
    art = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
    for b in (KOBRIN, GORODECHNO):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in art:
            b["art"] = art[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
