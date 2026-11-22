"""
Writes the rearguard fights of the Russian armies' retreat to Smolensk (src/data/battles/{saltanovka,ostrovno}.json):
Raevsky against Davout at Saltanovka, and Ostermann-Tolstoy, Konovnitsyn and Pahlen against Murat and Eugène at
Ostrovno.

    python3 scripts/forces/russia_1812_centre.py && npm run check:forces

Sources (see SOURCES): Nafziger's orders of battle for the Russian armies at the start of the campaign (812XBA)
and the Grande Armée on 1 August (812HAB), with the English and Russian Wikipedia articles for who fought when.
Summaries are our own words. Staff Ratings are set by ratings.py.
"""

import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from russia_1812 import ru_jager_regiment, ru_regiment
from russia_1812_north import fr_regiment

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
NAFZIGER_RU = {"label": "Russian Armies at the beginning of the 1812 Campaign (Nafziger Collection 812XBA)",
               "url": "https://www.napoleon-series.org/nafzigger/812XBA.pdf"}
NAFZIGER_FR = {"label": "French Grande Armée, 1 August 1812 (Nafziger Collection 812HAB)",
               "url": "https://www.napoleon-series.org/nafzigger/812HAB.pdf"}
FR, RU = "france", "russia"
RU_ORDER = "After Nafziger's order of battle for the start of the campaign; losses since then aren't shown."
FR_ORDER = "After Nafziger's order of battle for 1 August, a week or so after the fight."


# ---------------------------------------------------------------- Saltanovka, 23 July 1812

DESSAIX = force("saltanovka-dessaix", FR, "Dessaix's Division", "4th Division, I Corps (Davout)", "French",
                "Davout's division in the line behind the Saltanovka stream, its guns covering the dam on the Mogilev road. When Raevsky's Smolensk column came at the dam, the 85th struck it in the flank, and on the left the 108th, hidden in the standing wheat, ambushed Paskevich's men as they came out of the woods at Fatova.",
                [bde("fr-infantry-brigade", "Barbanègre's Brigade", "Gén. de Brigade Barbanègre",
                     units=[u("fr-regimental-battery", "33rd Léger Artillery Company")],
                     regiments=[fr_regiment("33rd Léger", 4, light=True)]),
                 bde("fr-infantry-brigade", "Friederichs's Brigade", "Gén. de Brigade Friederichs",
                     units=[u("fr-regimental-battery", "85th Line Artillery Company")],
                     regiments=[fr_regiment("85th Line", 5)]),
                 bde("fr-infantry-brigade", "Leguay's Brigade", "Gén. de Brigade Leguay",
                     units=[u("fr-regimental-battery", "108th Line Artillery Company")],
                     regiments=[fr_regiment("108th Line", 5)]),
                 bde("fr-divisional-artillery", "Divisional Artillery",
                     units=[u("fr-foot-arty", "9/7th Foot Artillery"), u("fr-horse-arty", "2/5th Horse Artillery")])],
                command=[{"unit": "fr-cmd-dessaix"}],
                notes=["Dessaix is the book's named commander.", FR_ORDER,
                       "Each regiment had its own company of four 3-pdrs, shown as a Regimental Battery.",
                       "The horse battery, without three cavalry regiments in the force, shows as a historical departure."])

COMPANS = force("saltanovka-compans", FR, "Compans's Division", "5th Division, I Corps (Davout)", "French",
                "Davout's second division, in reserve behind Dessaix's. Its 61st was sent up to Fatova when Paskevich's attack turned the French left, and helped throw the Russians back into the woods.",
                [bde("fr-infantry-brigade", "Duppelin's Brigade", "Gén. de Brigade Duppelin",
                     units=[u("fr-regimental-battery", "25th Line Artillery Company")],
                     regiments=[fr_regiment("25th Line", 5)]),
                 bde("fr-infantry-brigade", "Teste's Brigade", "Gén. de Brigade Teste",
                     units=[u("fr-regimental-battery", "57th Line Artillery Company")],
                     regiments=[fr_regiment("57th Line", 5)]),
                 bde("fr-infantry-brigade", "Guyardet's Brigade", "Gén. de Brigade Guyardet",
                     units=[u("fr-regimental-battery", "61st Line Artillery Company"), u("fr-regimental-battery", "111th Line Artillery Company")],
                     regiments=[fr_regiment("61st Line", 5), fr_regiment("111th Line", 5)]),
                 bde("fr-divisional-artillery", "Divisional Artillery",
                     units=[u("fr-foot-arty", "2/6th Foot Artillery"), u("fr-horse-arty", "16/7th Horse Artillery")])],
                command=[{"unit": "fr-cmd-compans"}],
                notes=["Compans is the book's named commander.", FR_ORDER,
                       "Only the 61st is recorded in the fighting; the rest of the division stood in reserve.",
                       "The horse battery, without three cavalry regiments in the force, shows as a historical departure."])

DAVOUT_CAVALRY = force("saltanovka-cavalry", FR, "Valence's and Bordessoulle's Cavalry", "5th Cuirassier Division and I Corps cavalry", "French",
                       "The cuirassiers and light horse with Davout at Mogilev, which held the open ground behind the infantry and stood ready for a Russian break-through that never came.",
                       [bde("fr-light-cavalry-brigade", "Bordessoulle's Brigade", "Gén. de Brigade Bordessoulle",
                            [u("fr-chasseur-a-cheval", "1st Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "3rd Chasseurs à Cheval")]),
                        bde("fr-heavy-cavalry-brigade", "Valence's Cuirassiers", "Gén. de Division Valence",
                            [u("fr-cuirassier", "6th Cuirassiers"), u("fr-cuirassier", "11th Cuirassiers"), u("fr-cuirassier", "12th Cuirassiers"),
                             u("fr-lancer-small", "Company, 5th Chevau-légers")]),
                        bde("fr-artillery-brigade", "Valence's Horse Artillery",
                            units=[u("fr-horse-arty", "4/5th Horse Artillery"), u("fr-horse-arty", "6/5th Horse Artillery")])],
                       command=[cmd("fr-div-cmd", "Gén. de Division Valence")],
                       notes=[FR_ORDER,
                              "The accounts name Bordessoulle and Valence with Davout but not their regiments; these are their commands in Nafziger's order of battle. Valence's three brigades of one regiment each are shown together.",
                              "Cavalry without infantry, and the second horse battery, show as historical departures."])

KOLUBAKIN = force("saltanovka-kolubakin", RU, "Kolubakin's Division", "12th Division, VII Corps (Raevsky)", "Russian",
                  "Its Jäger opened the attack at seven in the morning and drove the French outposts back to the dam, but could get no further under the guns on the heights. In the afternoon Raevsky himself took the Smolensk regiment forward along the road; hit in the chest by canister, he stayed in its ranks and turned it on the French battalion that had struck its flank.",
                  [bde("ru-infantry-brigade", "Ryleev's Brigade", "Maj-Gen Ryleev",
                       units=[u("ru-position-arty", "12th Position Battery")],
                       regiments=[ru_regiment("Smolensk"), ru_regiment("Narva")]),
                   bde("ru-infantry-brigade", "Panzerbieter's Brigade", "Maj-Gen Panzerbieter",
                       units=[u("ru-light-arty", "22nd Light Battery")],
                       regiments=[ru_regiment("New Ingermanland"), ru_regiment("Alexopol")]),
                   bde("ru-jager-brigade", "Palitsyn's Brigade", "Col Palitsyn",
                       units=[u("ru-light-arty", "23rd Light Battery")],
                       regiments=[ru_jager_regiment("6th"), ru_jager_regiment("41st")])],
                  command=[{"unit": "ru-cmd-raevsky"}],
                  notes=["Raevsky, the book's named commander, led this division's attack himself; Kolubakin commanded it.", RU_ORDER,
                         "The story that Raevsky led the Smolensk regiment with his two sons beside him was a patriotic fiction he denied himself, though his elder son was with the army."])

PASKEVICH = force("saltanovka-paskevich", RU, "Paskevich's Division", "26th Division, VII Corps (Raevsky)", "Russian",
                  "Sent through the forest to turn the French left, it came out at Fatova and took the village, then was thrown back by the 108th rising out of the wheat and the 85th behind it. The village changed hands several times before Paskevich, with twelve guns, made one last attack and drew off.",
                  [bde("ru-infantry-brigade", "Liebhard's Brigade", "Col Liebhard",
                       units=[u("ru-position-arty", "26th Position Battery")],
                       regiments=[ru_regiment("Ladoga"), ru_regiment("Poltava")]),
                   bde("ru-infantry-brigade", "Orel and Nizhny Novgorod", "",
                       units=[u("ru-light-arty", "47th Light Battery")],
                       regiments=[ru_regiment("Orel"), ru_regiment("Nizhny Novgorod")]),
                   bde("ru-jager-brigade", "Gogel's Brigade", "Col Gogel",
                       units=[u("ru-light-arty", "48th Light Battery")],
                       regiments=[ru_jager_regiment("5th"), ru_jager_regiment("42nd")])],
                  command=[cmd("ru-div-cmd", "Maj-Gen Paskevich")],
                  notes=[RU_ORDER, "The 42nd Jäger fought in skirmish order beside the Smolensk regiment's column on the main road."])

SALTANOVKA = {"id": "saltanovka", "name": "Saltanovka", "date": "23 July 1812", "campaign": "russia-1812",
              "summary": "Bagration, trying to break through to join Barclay, sent Raevsky's VII Corps against Davout at Mogilev. Davout held the line of the Saltanovka stream, its dam and bridge covered by his guns. Raevsky's frontal attack was shot to pieces, though he led the Smolensk regiment forward himself, and Paskevich's flank march through the woods was thrown back from Fatova; that night the Russians drew off, and Bagration took another road east.",
              "sources": [NAFZIGER_RU, NAFZIGER_FR,
                          {"label": "Battle of Saltanovka (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Saltanovka"},
                          {"label": "Бой под Салтановкой (Russian Wikipedia)",
                           "url": "https://ru.wikipedia.org/wiki/%D0%91%D0%BE%D0%B9_%D0%BF%D0%BE%D0%B4_%D0%A1%D0%B0%D0%BB%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%BE%D0%B9"}],
              "forces": [DESSAIX, COMPANS, DAVOUT_CAVALRY, KOLUBAKIN, PASKEVICH]}


# ---------------------------------------------------------------- Ostrovno, 25–27 July 1812

BRUYERE = force("ostrovno-bruyere", FR, "Bruyère's Light Cavalry", "1st Light Cavalry Division, I Reserve Cavalry Corps (Nansouty)", "French",
                "Murat's leading division, which ran into Ostermann's rearguard on the Vitebsk road on 25 July. Piré's brigade charged and took eight guns, and the hussars and lancers came on again and again against the Russian squares on the narrow road between the woods.",
                [bde("fr-light-cavalry-brigade", "Jacquinot's Brigade", "Gén. de Brigade Jacquinot",
                     [u("fr-hussar-regt", "7th Hussars"), u("fr-lancer", "9th Chevau-légers Lanciers")]),
                 bde("fr-light-cavalry-brigade", "Piré's Brigade", "Gén. de Brigade Piré",
                     [u("fr-chasseur-a-cheval", "16th Chasseurs à Cheval"), u("fr-hussar-regt", "8th Hussars")]),
                 bde("fr-light-cavalry-brigade", "Niewiewski's Brigade", "Gén. de Brigade Niewiewski",
                     [u("fr-polish-uhlan", "6th Polish Uhlans"), u("fr-polish-uhlan", "8th Polish Uhlans"),
                      u("fr-hussar-regt", "2nd Combined Prussian Hussars")]),
                 bde("fr-artillery-brigade", "Horse Artillery", units=[u("fr-horse-arty", "7/6th Horse Artillery")])],
                command=[cmd("fr-div-cmd", "Gén. de Division Bruyère")],
                notes=[FR_ORDER, "The 2nd Combined Prussian Hussars, from Yorck's contingent, rode with Niewiewski's Poles.",
                       "Three Light Cavalry Brigades and no infantry show as historical departures."])

SAINT_GERMAIN = force("ostrovno-saint-germain", FR, "Saint-Germain's Cuirassiers", "1st Cuirassier Division, I Reserve Cavalry Corps (Nansouty)", "French",
                      "Nansouty's heavy division, on the French right on 25 July, where it threw back a charge by Russian dragoons; the 2nd Cuirassiers lost 187 horses in the day.",
                      [bde("fr-heavy-cavalry-brigade", "Saint-Germain's Cuirassiers", "Gén. de Division Saint-Germain",
                           [u("fr-cuirassier", "2nd Cuirassiers"), u("fr-cuirassier", "3rd Cuirassiers"), u("fr-cuirassier", "9th Cuirassiers"),
                            u("fr-lancer-small", "Company, 1st Chevau-légers")]),
                       bde("fr-artillery-brigade", "Horse Artillery",
                           units=[u("fr-horse-arty", "1/5th Horse Artillery"), u("fr-horse-arty", "3/5th Horse Artillery")])],
                      command=[cmd("fr-div-cmd", "Gén. de Division Saint-Germain")],
                      notes=[FR_ORDER, "Its three brigades of one regiment each (Bessières's, Bruno's, Queunot's) are shown together.",
                             "Cavalry without infantry, and the second horse battery, show as historical departures."])

DELZONS = force("ostrovno-delzons", FR, "Delzons's Division", "13th Division, IV Corps (Eugène)", "French",
                "The first infantry up. Two battalions of its 8th Léger came forward with Murat on 25 July, and as the division arrived it worked through the forest to turn the Russian left, forcing Ostermann back towards Vitebsk; next day it led the attacks on Konovnitsyn. Roussel, one of its brigadiers, was shot dead that night by a French sentry.",
                [bde("fr-infantry-brigade", "Huard's Brigade", "Gén. de Brigade Huard",
                     units=[u("fr-regimental-arty-section", "8th Léger Artillery Company"), u("fr-regimental-arty-section", "84th Line Artillery Company")],
                     regiments=[fr_regiment("8th Léger", 2, light=True), fr_regiment("84th Line", 4)]),
                 bde("fr-infantry-brigade", "Roussel's Brigade", "Gén. de Brigade Roussel",
                     units=[u("fr-regimental-arty-section", "92nd Line Artillery Company")],
                     regiments=[fr_regiment("1st Provisional Croatian", 2), fr_regiment("92nd Line", 4)]),
                 bde("fr-infantry-brigade", "106th Line", "",
                     units=[u("fr-regimental-arty-section", "106th Line Artillery Company")],
                     regiments=[fr_regiment("106th Line", 4)]),
                 bde("fr-divisional-artillery", "Divisional Artillery",
                     units=[u("fr-foot-arty", "9/2nd Foot Artillery"), u("fr-horse-arty", "2/4th Horse Artillery")])],
                command=[cmd("fr-div-cmd", "Gén. de Division Delzons")],
                notes=[FR_ORDER, "The 1st Provisional Croatian Regiment, raised in the Illyrian Provinces, is shown as Line infantry.",
                       "Each regiment but the Croatians had two 3-pdrs, shown as Regimental Artillery.",
                       "The horse battery, without three cavalry regiments in the force, shows as a historical departure."])

CHOGLOKOV = force("ostrovno-choglokov", RU, "Choglokov's Division", "11th Division, IV Corps (Ostermann-Tolstoy)", "Russian",
                  "Half of Ostermann's corps, which stood across the Vitebsk road on 25 July in battalion squares under Murat's guns and charges. Asked what to do, Ostermann is said to have answered: stand and die.",
                  [bde("ru-infantry-brigade", "Filisov's Brigade", "Maj-Gen Filisov",
                       units=[u("ru-position-arty", "2nd Position Battery")],
                       regiments=[ru_regiment("Polotsk"), ru_regiment("Elets")]),
                   bde("ru-infantry-brigade", "Kexholm and Pernov", "",
                       units=[u("ru-light-arty", "3rd Light Battery")],
                       regiments=[ru_regiment("Kexholm"), ru_regiment("Pernov")]),
                   bde("ru-jager-brigade", "Bistrom's Brigade", "Col Bistrom",
                       units=[u("ru-light-arty", "4th Light Battery")],
                       regiments=[ru_jager_regiment("1st"), ru_jager_regiment("33rd")])],
                  command=[cmd("ru-div-cmd", "Maj-Gen Choglokov")],
                  notes=[RU_ORDER])

BAKHMETEV = force("ostrovno-bakhmetev", RU, "Bakhmetev's Division", "23rd Division, IV Corps (Ostermann-Tolstoy)", "Russian",
                  "The other half of Ostermann's corps on 25 July, holding the woods on the left until Delzons's infantry came round them; Okulov, one of its brigadiers, was killed in the three days' fighting.",
                  [bde("ru-infantry-brigade", "Okulov's Brigade", "Maj-Gen Okulov",
                       units=[u("ru-position-arty", "23rd Position Battery")],
                       regiments=[ru_regiment("Rylsk"), ru_regiment("Ekaterinburg")]),
                   bde("ru-infantry-brigade", "Selenginsk and 18th Jäger", "",
                       units=[u("ru-light-arty", "43rd Light Battery"), u("ru-light-arty", "44th Light Battery")],
                       regiments=[ru_regiment("Selenginsk", jager="18th")])],
                  command=[cmd("ru-div-cmd", "Maj-Gen Bakhmetev")],
                  notes=[RU_ORDER, "The division had only five regiments; the 18th Jäger is attached to the Selenginsk regiment, as the list takes it.",
                         "Two light batteries in one brigade, and a position battery with only eight battalions, where the list wants nine, show as historical departures."])

OSTERMANN_CAVALRY = force("ostrovno-cavalry", RU, "Ostermann's Cavalry", "With IV Corps (Ostermann-Tolstoy)", "Russian",
                          "The cavalry with the rearguard, which ran into the French advance guard at the start of the day: the Life Guard Hussars and the Nezhin Dragoons, then a second hussar regiment, with a horse battery that lost six guns in the woods to the 8th Hussars.",
                          [bde("ru-guard-light-cavalry-brigade", "Life Guard Hussars", "",
                               [u("ru-lg-hussar", "Life Guard Hussars")]),
                           bde("ru-light-cavalry-brigade", "Hussars and Dragoons", "",
                               [u("ru-hussar", "Izyum Hussars", options=["large-cavalry"]), u("ru-dragoon", "Nezhin Dragoons"), u("ru-horse-arty", "Horse Battery")])],
                          command=[cmd("ru-div-cmd", "Lt-Gen Count Ostermann-Tolstoy")],
                          notes=["The Russian accounts name the Life Guard Hussars and the Nezhin Dragoons, with a second hussar regiment, a dragoon brigade and a horse battery. The Izyum Hussars (eight squadrons, so Large) were attached to the 23rd Division in Nafziger's order of battle; which hussars came up isn't recorded.",
                                 "Guard cavalry without the infantry brigades it needs, no infantry, and a horse battery with only two cavalry regiments, show as historical departures."])

KONOVNITSYN = force("ostrovno-konovnitsyn", RU, "Konovnitsyn's Division", "3rd Division, III Corps (Tuchkov)", "Russian",
                    "Relieved Ostermann's battered corps on 26 July and held the forest road all day against Murat and Delzons until Napoleon himself came up in the afternoon; by three o'clock the line had broken, and the retreat nearly became a rout.",
                    [bde("ru-infantry-brigade", "Tuchkov III's Brigade", "Maj-Gen Tuchkov III",
                         units=[u("ru-position-arty", "3rd Position Battery")],
                         regiments=[ru_regiment("Murom"), ru_regiment("Revel")]),
                     bde("ru-infantry-brigade", "Voeikov's Brigade", "Col Voeikov",
                         units=[u("ru-light-arty", "5th Light Battery")],
                         regiments=[ru_regiment("Chernigov"), ru_regiment("Koporye")]),
                     bde("ru-jager-brigade", "Prince Shakhovskoy's Brigade", "Maj-Gen Prince Shakhovskoy",
                         units=[u("ru-light-arty", "6th Light Battery")],
                         regiments=[ru_jager_regiment("20th"), ru_jager_regiment("21st"),
                                    {"name": "Converged Grenadiers", "units": [u("ru-grenadier", "1st Converged Grenadier Bn"), u("ru-grenadier", "2nd Converged Grenadier Bn")]}])],
                    command=[cmd("ru-div-cmd", "Lt-Gen Konovnitsyn")],
                    notes=[RU_ORDER, "The division's two converged grenadier battalions are the Jäger brigade's Grenadier regiment, as the list builds it.",
                           "Uvarov's cuirassiers stood behind it in reserve but couldn't be used in the woods."])

PAHLEN = force("ostrovno-pahlen", RU, "Pahlen's Cavalry", "3rd Cavalry Division", "Russian",
               "The last rearguard, with some infantry and forty guns, which held at Dobreyka eight kilometres from Vitebsk on 27 July from dawn until mid-afternoon, and then fell back behind the Luchesa while Barclay's army marched for Smolensk.",
               [bde("ru-heavy-cavalry-brigade", "Skalon's Brigade", "Maj-Gen Skalon",
                    [u("ru-dragoon", "Orenburg Dragoons"), u("ru-dragoon", "Siberia Dragoons")]),
                bde("ru-light-cavalry-brigade", "Klebeck's Brigade", "",
                    [u("ru-dragoon", "Irkutsk Dragoons", options=["large-cavalry"]), u("ru-hussar", "Mariupol Hussars", options=["large-cavalry"]),
                     u("ru-horse-arty", "9th Horse Battery")])],
               command=[cmd("ru-div-cmd", "Lt-Gen Count Pahlen")],
               notes=[RU_ORDER, "The Irkutsk Dragoons and Mariupol Hussars had eight squadrons each, so they are Large.",
                      "Pahlen's rearguard also had three to four thousand infantry, which the accounts don't name; add a brigade from the IV Corps if you like.",
                      "No Infantry Brigade shows as a historical departure."])

OSTROVNO = {"id": "ostrovno", "name": "Ostrovno", "date": "25–27 July 1812", "campaign": "russia-1812",
            "summary": "Three days of rearguard fighting on the road to Vitebsk, where Barclay meant to stand. On the 25th Ostermann-Tolstoy's corps held Murat's cavalry in squares on the forest road until Delzons's infantry turned its flank; on the 26th Konovnitsyn's division held on until Napoleon came up and broke it; on the 27th Pahlen held at Dobreyka. Then Barclay, learning Bagration could not join him, slipped away towards Smolensk.",
            "sources": [NAFZIGER_RU, NAFZIGER_FR,
                        {"label": "Battle of Ostrovno (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Ostrovno"},
                        {"label": "Бой под Островно (Russian Wikipedia)",
                         "url": "https://ru.wikipedia.org/wiki/%D0%91%D0%BE%D0%B9_%D0%BF%D0%BE%D0%B4_%D0%9E%D1%81%D1%82%D1%80%D0%BE%D0%B2%D0%BD%D0%BE"}],
            "forces": [BRUYERE, SAINT_GERMAIN, DELZONS, CHOGLOKOV, BAKHMETEV, OSTERMANN_CAVALRY, KONOVNITSYN, PAHLEN]}


if __name__ == "__main__":
    art = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
    for b in (SALTANOVKA, OSTROVNO):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in art:
            b["art"] = art[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
