"""
Writes Borodino (src/data/battles/borodino.json), 7 September 1812: every division and cavalry division of both armies
that fought, after Nafziger's orders of battle for the battle (812ICA, 812ICB), with Wikipedia for who fought where.

    python3 scripts/forces/russia_1812_borodino.py && npm run check:forces

Divisions already written for other 1812 battles are reused with Borodino's account; the rest are written here.
Summaries are our own words.
"""

import copy
import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from russia_1812 import ru_regiment
from russia_1812_north import fr_regiment
from russia_1812_autumn import BROUSSIER, CLAPAREDE, DUFOUR, EUGEN, KAPSEVICH, LIKHACHEV, OLSUFIEV, PONIATOWSKI_16, PONIATOWSKI_18, SEBASTIANI, naf
from russia_1812_centre import BAKHMETEV, BRUYERE, CHOGLOKOV, COMPANS, DAVOUT_CAVALRY, DELZONS, DESSAIX, KOLUBAKIN, KONOVNITSYN, PASKEVICH, SAINT_GERMAIN
from russia_1812_retreat import CURIAL, PLATOV, ROGUET
from russia_1812_smolensk import MORAND, NEVEROVSKY
from russia_1812_valutino import GUDIN, LEDRU, MARCHAND, RAZOUT, STROGANOV

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
B = "borodino"
NAF = "After Nafziger's order of battle for Borodino."
CAVALRY_ONLY = "Cavalry without infantry brigades for it to go with shows as a historical departure."


def again(f, slug, summary, **over):
    g = copy.deepcopy(f)
    g["id"] = f"{B}-{slug}"
    g["summary"] = summary
    for k, v in over.items():
        g[k] = v
    if g["side"] in ("Polish", "Italian", "Württemberg", "Saxon", "Westphalian"):
        g["side"] = "French"
    g["notes"] = [n for n in g["notes"] if "six weeks" not in n and "three weeks later" not in n and "After Borodino" not in n
                  and "By now the" not in n and "far below strength" not in n and "four days before" not in n]
    if g["nationId"] == "grand-duchy-of-warsaw":
        for br in g["brigades"]:
            for x in br.get("units", []) + [x for r in br.get("regiments", []) for x in r["units"]]:
                x.pop("options", None)
    return g


# ---------------------------------------------------------------- New French formations

THARREAU = force(f"{B}-tharreau", "westphalia", "Tharreau's Westphalians", "23rd Division, VIII Corps (Junot)", "French",
                 "Junot's corps came up on the right between Poniatowski and Davout, and fought through the Utitsa woods towards the flèches in the afternoon.",
                 [bde("wp-infantry-brigade", "Damas's Brigade", "Gen-Maj Damas", units=[u("wp-light-infantry", "3rd Light Bn")],
                      regiments=[{"name": f"{n} Line", "units": [u("wp-line-infantry", f"{r}/{n} Line") for r in ("I", "II")]} for n in ("2nd", "6th")]),
                  bde("wp-infantry-brigade", "Borstel's Brigade", "Gen-Maj von Borstel", units=[u("wp-light-infantry", "2nd Light Bn"), u("wp-foot-arty", "1st Foot Battery Froede")],
                      regiments=[{"name": "3rd Line", "units": [u("wp-line-infantry", f"{r}/3rd Line") for r in ("I", "II")]},
                                 {"name": "7th Line", "units": [u("wp-line-infantry", f"{r}/7th Line") for r in ("I", "II", "III")]}])],
                 command=[{"unit": "fr-cmd-tharreau"}],
                 notes=["Tharreau, killed at Borodino, is the book's named commander.", NAF])

OCHS = force(f"{B}-ochs", "westphalia", "Ochs's Westphalian Guard", "24th Division, VIII Corps (Junot)", "French",
             "The Westphalian Guard and Jäger, in the woods beside Tharreau's division.",
             [bde("wp-guard-infantry-brigade", "Legras's Brigade", "Gen-Maj Legras",
                  [u("wp-guard-grenadier", "Guard Grenadiers"), u("wp-guard-jager", "Guard Jäger"), u("wp-jager-karabinier", "Jäger-Karabiniers"), u("wp-regimental-arty", "Guard Foot Battery Brünig")]),
              bde("wp-infantry-brigade", "1st Jäger and the Foot Battery", "", units=[u("wp-jager", "1st Jäger Bn"), u("wp-foot-arty", "2nd Foot Battery Lemaître")])],
             command=[{"unit": "wp-cmd-von-ochs"}],
             notes=["Ochs is the book's named commander.", NAF, "The 1st Jäger, which had no brigade of its own, is shown with the second foot battery as a brigade with no line regiment, which shows as a historical departure."])

ITALIAN_GUARD = force(f"{B}-italian-guard", "italy", "The Italian Royal Guard", "IV Corps (Eugène)", "French",
                      "Eugène's Guard, held in reserve behind the attacks on the Great Redoubt.",
                      [bde("it-guard-brigade", "Lecchi's Brigade", "Gén. de Brigade Lecchi",
                           units=[u("it-guard-dragoons", "Guard Dragoons"), u("it-guard-dragoons", "Queen's Dragoons"), u("it-foot-arty", "Guard Foot Battery"), u("it-horse-arty", "Guard Horse Battery")],
                           regiments=[{"name": "Guard Infantry", "units": [u("it-royal-guard-grenadiers", "I/Guard Infantry"), u("it-royal-guard-chasseurs", "II/Guard Infantry")]},
                                      {"name": "Royal Vélites", "units": [u("it-royal-velite-infantry", "I/Royal Vélites"), u("it-royal-velite-infantry", "II/Royal Vélites")]},
                                      {"name": "Guard Conscripts", "units": [u("it-guard-conscripts", "I/Guard Conscripts"), u("it-guard-conscripts", "II/Guard Conscripts")]}])],
                      command=[cmd("it-div-cmd", "Gén. de Brigade Lecchi")],
                      notes=[NAF, "The Guard Infantry's two battalions are shown as one of grenadiers and one of chasseurs."])

THIELMANN = force(f"{B}-thielmann", "saxony", "Thielmann's Saxon Cuirassiers", "7th Cuirassier Division (Lorge), IV Cavalry Corps", "French",
                  "The Saxon Garde du Corps and Zastrow Cuirassiers, with the Polish cuirassiers, rode up the slope into the back of the Great Redoubt in the afternoon as the French infantry stormed its front, the most famous cavalry charge of the day.",
                  [bde("sax-cavalry-reserve", "Thielmann's Brigade", "Gen-Maj von Thielmann",
                       [u("sax-garde-du-corps", "Garde du Corps"), u("sax-cuirassier", "Zastrow Cuirassiers"), u("sax-polish-cuirassier", "14th Polish Cuirassiers"),
                        u("sax-horse-arty", "2nd Saxon Horse Battery von Hiller")])],
                  command=[{"unit": "sax-cmd-thielmann"}],
                  notes=["Thielmann is the book's named commander.", NAF, CAVALRY_ONLY])

LEPEL = force(f"{B}-lepel", "westphalia", "Lepel's Westphalian Cuirassiers", "7th Cuirassier Division (Lorge), IV Cavalry Corps", "French",
              "Lorge's other brigade, which charged beside the Saxons into the Great Redoubt; Lepel was killed.",
              [bde("wp-cavalry-reserve", "Lepel's Brigade", "Gén. de Brigade Lepel",
                   [u("wp-cuirassier", "1st Westphalian Cuirassiers"), u("wp-cuirassier", "2nd Westphalian Cuirassiers"), u("wp-horse-arty", "2nd Westphalian Horse Battery")])],
              command=[cmd("wp-div-cmd", "Gén. de Division Lorge")],
              notes=[NAF, CAVALRY_ONLY])

GROUCHY = force(f"{B}-grouchy", "france", "Grouchy's Cavalry", "III Reserve Cavalry Corps", "French",
                "Supported Eugène's attacks on the Great Redoubt from the north, charging the Russian infantry behind it.",
                [bde("fr-light-cavalry-brigade", "Gauthrin's Brigade", "Gén. de Brigade Gauthrin", [u("fr-hussar-regt", "6th Hussars"), u("fr-chasseur-a-cheval", "8th Chasseurs")]),
                 bde("fr-light-cavalry-brigade", "Girard's Brigade", "Gén. de Brigade Girard", [u("fr-chasseur-a-cheval", "6th Chasseurs"), u("fr-chasseur-a-cheval", "25th Chasseurs")]),
                 bde("fr-light-cavalry-brigade", "Dommanget's Brigade", "Gén. de Brigade Dommanget",
                     [u("fr-bavarian-chevauleger", "1st Bavarian Chevau-légers"), u("fr-bavarian-chevauleger", "2nd Bavarian Chevau-légers"), u("fr-bavarian-chevauleger", "Saxon Prinz Albert Chevau-légers")]),
                 bde("fr-heavy-cavalry-brigade", "La Houssaye's Dragoons", "Gén. de Division La Houssaye",
                     [u("fr-dragoon", "7th Dragoons"), u("fr-dragoon", "23rd Dragoons"), u("fr-dragoon", "28th Dragoons"), u("fr-dragoon", "30th Dragoons")])],
                command=[cmd("fr-div-cmd", "Gén. de Division Grouchy")],
                notes=[NAF, "The Saxon Prinz Albert Chevau-légers are shown as the list's Bavarian Chevau-légers, the nearest type.",
                       "Three light brigades, four dragoon regiments in one brigade, and no infantry show as historical departures."])

MONTBRUN_HEAVY = force(f"{B}-wathier-defrance", "france", "Wathier's and Defrance's Cuirassiers", "II Reserve Cavalry Corps (Montbrun, then Caulaincourt)", "French",
                       "Montbrun was killed by a round shot early on; Caulaincourt, leading the corps in his place, took the 5th Cuirassiers into the Great Redoubt from behind and was killed in it.",
                       [bde("fr-heavy-cavalry-brigade", "Wathier's Division", "Gén. de Division Wathier",
                            [u("fr-cuirassier", "5th Cuirassiers"), u("fr-cuirassier", "8th Cuirassiers"), u("fr-cuirassier", "10th Cuirassiers")]),
                        bde("fr-heavy-cavalry-brigade", "Defrance's Division", "Gén. de Division Defrance",
                            [u("fr-carabinier", "1st Carabiniers"), u("fr-carabinier", "2nd Carabiniers"), u("fr-cuirassier", "1st Cuirassiers")]),
                        bde("fr-artillery-brigade", "Horse Artillery", units=[u("fr-horse-arty", "1/2nd Horse Artillery")])],
                       command=[cmd("fr-div-cmd", "Gén. de Division Montbrun")],
                       notes=[NAF, "Each division's three single-regiment brigades are shown as one brigade.", "Two Heavy Cavalry Brigades, and no infantry, show as historical departures."])

# ---------------------------------------------------------------- New Russian formations


def lg_reg(name, unit="ru-life-guard-infantry"):
    return {"name": name, "units": [u(unit, f"{r}/{name}") for r in ("I", "II", "III")]}


GUARD = force(f"{B}-guard", "russia", "Lavrov's Guard Infantry", "Guard Division, V Corps (Grand Duke Constantine)", "Russian",
              "Held in reserve until the afternoon, when the Izmailovsky and Lithuanian regiments were sent up behind Semenovskoe and stood in square for hours under the French guns and cavalry, losing a third of their men without breaking.",
              [bde("ru-guard-infantry-brigade", "Rosen's Brigade", "Maj-Gen Baron Rosen", units=[u("ru-guard-position-arty", "1st Guard Position Battery")],
                   regiments=[lg_reg("Preobrazhensky"), lg_reg("Semenovsky")]),
               bde("ru-guard-infantry-brigade", "Udom's Brigade", "Maj-Gen Udom", units=[u("ru-guard-light-arty", "1st Guard Light Battery")],
                   regiments=[lg_reg("Izmailovsky"), lg_reg("Lithuanian")]),
               bde("ru-guard-infantry-brigade", "Bistrom's Brigade", "Maj-Gen Bistrom", units=[u("ru-guard-light-arty", "2nd Guard Light Battery")],
                   regiments=[lg_reg("Guard Jäger", "ru-life-guard-jager"), lg_reg("Finland")])],
              command=[cmd("ru-div-cmd", "Lt-Gen Lavrov")],
              notes=[NAF, "Three Guard brigades with no line infantry brigades for them to go with show as historical departures."])

VORONTSOV = force(f"{B}-vorontsov", "russia", "Vorontsov's Converged Grenadiers", "2nd Converged Grenadier Division, VIII Corps (Borozdin)", "Russian",
                  "Held the Semenovskoe flèches against Davout's first attacks at dawn; of its 4,000 men barely 300 were standing at the end of the morning, and Vorontsov himself was wounded leading a bayonet charge.",
                  [bde("ru-combined-grenadier-brigade", "First Brigade", "",
                       [u("ru-inf-combined-grenadier", f"Converged Grenadiers ({r})") for r in ("Pskov", "Moscow", "19th Jäger", "40th Jäger")]
                       + [u("ru-position-arty", "31st Position Battery")]),
                   bde("ru-combined-grenadier-brigade", "Second Brigade", "",
                       [u("ru-inf-combined-grenadier", f"Converged Grenadiers ({r})") for r in ("Astrakhan", "Fanagoria", "6th Jäger", "New Ingermanland", "42nd Jäger", "Odessa", "Vilna")])],
                  command=[{"unit": "ru-cmd-vorontsov"}],
                  notes=["Vorontsov is the book's named commander.", "After Mikaberidze's order of battle: eleven converged grenadier battalions, from the 7th, 24th, 2nd Grenadier, 12th, 26th and 27th Divisions.",
                         "Two Combined Grenadier Brigades, more battalions than one holds, and no infantry brigade show as historical departures."])

MECKLENBURG = force(f"{B}-mecklenburg", "russia", "Prince Karl's 2nd Grenadier Division", "2nd Grenadier Division, VIII Corps (Borozdin)", "Russian",
                    "Sent forward to retake the flèches as they fell; in the counter-attacks there it lost most of its officers, and Prince Karl of Mecklenburg was wounded.",
                    [bde("ru-grenadier-brigade", f"{c}'s Brigade", f"Maj-Gen {c}", units=[bat],
                         regiments=[{"name": f"{r} Grenadiers", "units": [u("ru-grenadier", f"I/{r} Grenadiers"), u("ru-grenadier", f"II/{r} Grenadiers")]} for r in regs])
                     for c, regs, bat in (("Shatilov", ("Kiev", "Moscow"), u("ru-position-arty", "11th Position Battery")),
                                          ("Buxhoeveden", ("Astrakhan", "Fanagoria"), u("ru-light-arty", "20th Light Battery")),
                                          ("Levin", ("Siberia", "Little Russia"), u("ru-light-arty", "21st Light Battery")))],
                    command=[cmd("ru-div-cmd", "Maj-Gen Prince Karl of Mecklenburg")],
                    notes=[NAF, "Three Grenadier Brigades where the list takes one show as a historical departure."])

CUIRASSIERS_1 = force(f"{B}-1st-cuirassiers", "russia", "Depreradovich's 1st Cuirassier Division", "1st Cuirassier Division, V Corps", "Russian",
                      "The Guard and line cuirassiers, sent forward in the afternoon to meet the French cavalry around the Great Redoubt and behind Semenovskoe.",
                      [bde("ru-heavy-cavalry-brigade", "Borozdin II's Brigade", "Maj-Gen Borozdin II",
                           [u("ru-cuirassier", "His Majesty's Cuirassiers"), u("ru-cuirassier", "Her Majesty's Cuirassiers"), u("ru-cuirassier", "Astrakhan Cuirassiers")]),
                       bde("ru-guard-heavy-cavalry-brigade", "Shevich's Brigade", "Maj-Gen Shevich",
                           [u("ru-chevalier-guard", "Chevalier Guard"), u("ru-life-guard-horse", "Life Guard Horse"), u("ru-guard-horse-arty", "1st Guard Horse Battery")])],
                      command=[cmd("ru-div-cmd", "Maj-Gen Depreradovich")],
                      notes=[NAF, "Nafziger names the Guard Dragoons with Shevich; it was the Life Guard Horse that fought with the Chevalier Guard. Guard cavalry without the infantry brigades it needs shows as a historical departure."])

CUIRASSIERS_2 = force(f"{B}-2nd-cuirassiers", "russia", "Duka's 2nd Cuirassier Division", "2nd Cuirassier Division, 2nd Army of the West", "Russian",
                      "Bagration's cuirassiers, which counter-charged the French cavalry around the flèches and Semenovskoe again and again through the morning.",
                      [bde("ru-heavy-cavalry-brigade", "Kretov's Brigade", "Maj-Gen Kretov", [u("ru-cuirassier", "Military Order Cuirassiers"), u("ru-cuirassier", "Ekaterinoslav Cuirassiers")]),
                       bde("ru-heavy-cavalry-brigade", "Duka's Brigade", "Maj-Gen Duka",
                           [u("ru-cuirassier", "Glukhov Cuirassiers"), u("ru-cuirassier", "Novgorod Cuirassiers"), u("ru-cuirassier", "Little Russia Cuirassiers")])],
                      command=[cmd("ru-div-cmd", "Maj-Gen Duka")],
                      notes=[NAF, "Two Heavy Cavalry Brigades, and no infantry, show as historical departures."])

UVAROV = force(f"{B}-uvarov", "russia", "Uvarov's Cavalry", "I Cavalry Corps", "Russian",
               "Sent with Platov's Cossacks on a raid round the French left at midday; it crossed the Kolocha, alarmed Eugène's corps and bought the Russian centre two hours before it was recalled.",
               [bde("ru-guard-light-cavalry-brigade", "Guard Light Cavalry", "Maj-Gen Chalikov",
                    [u("ru-life-guard-uhlan", "Life Guard Uhlans"), u("ru-lg-hussar", "Life Guard Hussars"), u("ru-life-guard-cossack", "Life Guard Cossacks")]),
                bde("ru-light-cavalry-brigade", "Chernyshev's Brigade", "Maj-Gen Chernyshev", [u("ru-dragoon", "Nezhin Dragoons"), u("ru-hussar", "Elisabethgrad Hussars", options=["large-cavalry"]), u("ru-horse-arty", "2nd Horse Battery")])],
               command=[cmd("ru-div-cmd", "Lt-Gen Uvarov")],
               notes=[NAF, "Three Guard regiments where the list's brigade takes two, and Guard cavalry without infantry, show as historical departures."])

KORFF = force(f"{B}-korff", "russia", "Korff's Cavalry", "II Cavalry Corps", "Russian",
              "Moved across from the right in the afternoon to stand behind the Great Redoubt, and met the French cuirassiers that broke through after it fell.",
              [bde("ru-heavy-cavalry-brigade", "Davydov's Brigade", "Col Davydov", [u("ru-dragoon", "Pskov Dragoons"), u("ru-dragoon", "Moscow Dragoons")]),
               bde("ru-light-cavalry-brigade", "Hussars and Uhlans", "", [u("ru-hussar", "Izyum Hussars", options=["large-cavalry"]), u("ru-uhlan", "Polish Uhlans", options=["large-cavalry"]), u("ru-horse-arty", "6th Horse Battery")]),
               bde("ru-heavy-cavalry-brigade", "Kleber's Brigade", "", [u("ru-dragoon", "Orenburg Dragoons"), u("ru-dragoon", "Kurland Dragoons")])],
              command=[cmd("ru-div-cmd", "Maj-Gen Baron Korff")],
              notes=[NAF, "Nafziger also lists Skalon's Siberia and Irkutsk Dragoons and the Sumy and Mariupol Hussars; they're left out. Two heavy brigades and no infantry show as historical departures."])

SIEVERS = force(f"{B}-sievers", "russia", "Sievers's Cavalry", "IV Cavalry Corps", "Russian",
                "Bagration's cavalry on the left, fighting around the flèches and Semenovskoe through the morning; the Kharkov and Chernigov Dragoons fought dismounted among the infantry.",
                [bde("ru-heavy-cavalry-brigade", "Panchulidzev's Brigade", "Maj-Gen Panchulidzev",
                     [u("ru-dragoon", "Kharkov Dragoons", options=["on-foot"]), u("ru-dragoon", "Chernigov Dragoons", options=["on-foot"])]),
                 bde("ru-heavy-cavalry-brigade", "Emmanuel's Brigade", "Maj-Gen Emmanuel", [u("ru-dragoon", "Kiev Dragoons"), u("ru-dragoon", "New Russia Dragoons")]),
                 bde("ru-light-cavalry-brigade", "Hussars and Uhlans", "", [u("ru-hussar", "Akhtyrka Hussars"), u("ru-uhlan", "Lithuanian Uhlans", options=["large-cavalry"]), u("ru-horse-arty", "8th Horse Battery")])],
                command=[cmd("ru-div-cmd", "Maj-Gen Sievers")],
                notes=[NAF, "Two heavy brigades and no infantry show as historical departures."])


# ---------------------------------------------------------------- Mikaberidze's corrections and additions

MIKABERIDZE = {"label": "Alexander Mikaberidze and Eman Vovsi, The Battle of Borodino: Orders of Battle (Napoleon Series)",
               "url": "https://www.napoleon-series.org/military-info/battles/Borodino/Mikaberidze/OrdersofBattle/c_MikaberidzeOOB1.html"}
VOVSI = {"label": "Eman Vovsi, French Numbered Infantry Regiments at Borodino (Napoleon Series)",
         "url": "https://www.napoleon-series.org/military-info/battles/1812/Russia/Borodino/c_french1812.html"}
MIKA = "Brigades and commanders as Mikaberidze and Vovsi give them for Borodino."

DELABORDE = force(f"{B}-delaborde", "french-imperial-guard", "Delaborde's Young Guard", "1st Division, Imperial Guard (Mortier)", "French",
                  "Berthezène's brigade of the Young Guard, held in reserve with the rest of the Guard all day.",
                  [bde("fig-young-guard-brigade", "Berthezène's Brigade", "Gén. de Brigade Berthezène",
                       regiments=[{"name": n, "units": [u(t, f"I/{n}"), u(t, f"II/{n}")]} for n, t in
                                  (("4th Voltigeurs", "fig-yg-voltigeurs"), ("4th Tirailleurs", "fig-yg-tirailleurs"), ("5th Voltigeurs", "fig-yg-voltigeurs"))])],
                  command=[cmd("fig-div-cmd", "Gén. de Division Delaborde")],
                  notes=[MIKA])

GUARD_CAVALRY = force(f"{B}-guard-cavalry", "french-imperial-guard", "Walther's Guard Cavalry", "Guard Cavalry Division (Bessières)", "French",
                      "The Guard's cavalry, kept back with the rest of the Guard; Napoleon would not risk it.",
                      [bde("fig-light-cavalry-brigade", "Lefebvre-Desnouettes's Brigade", "Gén. de Division Lefebvre-Desnouettes",
                           [u("fig-chasseurs-a-cheval", "Chasseurs à Cheval of the Guard"), u("fig-mamluke", "Mamelukes")]),
                       bde("fig-light-cavalry-brigade", "Krasiński's Brigade", "Gén. de Brigade Krasiński",
                           [u("fig-polish-lancers", "1st Polish Chevau-légers Lanciers"), u("fig-gendarmes-elite", "Gendarmes d'Élite")]),
                       bde("fig-light-cavalry-brigade", "Colbert's Brigade", "Gén. de Brigade Colbert", [u("fig-dutch-red-lancers", "2nd (Dutch) Chevau-légers Lanciers")]),
                       bde("fig-heavy-cavalry-brigade", "Walther's Brigade", "Gén. de Division Walther",
                           [u("fig-grenadiers-a-cheval-regt", "Grenadiers à Cheval"), u("fig-empress-dragoons", "Empress Dragoons")])],
                      command=[cmd("fig-div-cmd", "Gén. de Division Walther")],
                      notes=[MIKA, "Durosnel's Gendarmes d'Élite are shown with the Polish lancers.", "Guard cavalry without the infantry brigades it needs shows as a historical departure."])

KREUTZ = force(f"{B}-kreutz", "russia", "Kreutz's Cavalry", "III Reserve Cavalry Corps", "Russian",
               "Stood behind the centre, and in the afternoon charged the French cavalry that broke through beyond the Great Redoubt; Kreutz was wounded.",
               [bde("ru-heavy-cavalry-brigade", "Dyatkov's Brigade", "Maj-Gen Dyatkov", [u("ru-dragoon", "Kurland Dragoons"), u("ru-dragoon", "Orenburg Dragoons")]),
                bde("ru-heavy-cavalry-brigade", "Kreutz's Brigade", "Col Baron Kreutz", [u("ru-dragoon", "Irkutsk Dragoons"), u("ru-dragoon", "Siberia Dragoons")]),
                bde("ru-light-cavalry-brigade", "Dorokhov's Brigade", "Maj-Gen Dorokhov",
                    [u("ru-hussar", "Mariupol Hussars", options=["large-cavalry"]), u("ru-hussar", "Sumy Hussars", options=["large-cavalry"]), u("ru-horse-arty", "7th Horse Battery")])],
               command=[cmd("ru-div-cmd", "Col Baron Kreutz")],
               notes=[MIKA, "Mikaberidze lists the corps under Korff; Kreutz commanded it on the day. Two heavy brigades and no infantry show as historical departures."])


def lineup(f, brigades):
    """Rename a force's brigades, and their commanders, in order: (name, commander) or None to leave one as it is"""
    for b, new in zip(f["brigades"], brigades):
        if new:
            b["name"] = new[0]
            if new[1]:
                b["commander"] = {"name": new[1]}


def regs(*specs):
    return [{"name": n, "units": [u(t, f"{r}/{n}") for r in rs]} for n, t, rs in specs]


def fix(forces):
    by = {f["id"]: f for f in forces}
    k = by[f"{B}-konovnitsyn"]
    lineup(k, [("Tuchkov IV's Brigade", "Maj-Gen Tuchkov IV"), ("Mesheryakov's Brigade", "Col Mesheryakov")])
    k["brigades"][1]["regiments"] = [ru_regiment("Chernigov"), ru_regiment("Selenginsk", n=1)]
    k["notes"].insert(0, MIKA + " Koporye had gone to the 23rd Division; one battalion of Selenginsk took its place.")
    e = by[f"{B}-11th"]
    e["name"], e["command"] = "Bakhmetev I's 11th Division", [cmd("ru-div-cmd", "Maj-Gen Bakhmetev I")]
    lineup(e, [("Laptev's Brigade", "Maj-Gen Laptev"), ("Choglokov's Brigade", "Maj-Gen Choglokov")])
    e["notes"].insert(0, MIKA)
    t = by[f"{B}-23rd"]
    t["name"] = "Bakhmetev III's 23rd Division"
    lineup(t, [("Gurielov's Brigade", "Maj-Gen Prince Gurielov"), ("Aleksopol's Brigade", "Maj-Gen Aleksopol")])
    t["brigades"][1]["regiments"] = [ru_regiment("Koporye", jager="18th")]
    t["notes"] = [MIKA + " Okulov had been killed at Ostrovno.", t["notes"][-1]]
    w = by[f"{B}-12th"]
    w["name"] = "Vasilchikov's 12th Division"
    lineup(w, [("Bogdanovsky's Brigade", "Lt-Col Bogdanovsky"), None, ("Glebov's Brigade", "Col Glebov")])
    w["notes"].insert(0, MIKA + " Vasilchikov had the division by now; Raevsky commanded the corps.")
    p = by[f"{B}-paskevich"]
    lineup(p, [("Savoini's Brigade", "Col Savoini"), ("Kadyshev's Brigade", "Lt-Col Kadyshev")])
    p["notes"].insert(0, MIKA)
    g = by[f"{B}-guard"]
    lineup(g, [None, ("Khrapovitsky's Brigade", "Col Khrapovitsky")])
    g["notes"].insert(0, MIKA)
    c1 = by[f"{B}-1st-cuirassiers"]
    c1["name"], c1["command"] = "Borozdin's 1st Cuirassier Division", [cmd("ru-div-cmd", "Maj-Gen Borozdin II")]
    c1["notes"] = [MIKA, "Guard cavalry without the infantry brigades it needs shows as a historical departure."]
    lineup(by[f"{B}-2nd-cuirassiers"], [None, ("Tolbuzin's Brigade", "Col Tolbuzin")])
    by[f"{B}-2nd-cuirassiers"]["notes"].insert(0, MIKA)
    uv = by[f"{B}-uvarov"]
    uv["brigades"] = [bde("ru-guard-light-cavalry-brigade", "Chalikov's Brigade", "Maj-Gen Chalikov", [u("ru-lg-dragoon", "Life Guard Dragoons"), u("ru-life-guard-uhlan", "Life Guard Uhlans")]),
                      bde("ru-guard-light-cavalry-brigade", "Orlov-Denisov's Brigade", "Maj-Gen Orlov-Denisov", [u("ru-lg-hussar", "Life Guard Hussars"), u("ru-life-guard-cossack", "Life Guard Cossacks")]),
                      bde("ru-light-cavalry-brigade", "Vsevolozhsky's Brigade", "Maj-Gen Vsevolozhsky",
                          [u("ru-hussar", "Elisavetgrad Hussars", options=["large-cavalry"]), u("ru-dragoon", "Nezhin Dragoons"), u("ru-horse-arty", "2nd Horse Battery")])]
    uv["notes"] = [MIKA, "Two Guard light cavalry brigades where the list allows one, and Guard cavalry without infantry, show as historical departures."]
    ko = by[f"{B}-korff"]
    ko["brigades"] = [bde("ru-heavy-cavalry-brigade", "Davydov's Brigade", "Col Davydov", [u("ru-dragoon", "Moscow Dragoons"), u("ru-dragoon", "Pskov Dragoons")]),
                      bde("ru-light-cavalry-brigade", "Panchulidzev II's Brigade", "Maj-Gen Panchulidzev II",
                          [u("ru-hussar", "Izyum Hussars", options=["large-cavalry"]), u("ru-uhlan", "Polish Uhlans", options=["large-cavalry"]), u("ru-horse-arty", "6th Horse Battery")])]
    ko["notes"] = [MIKA, "Cavalry without infantry shows as a historical departure."]
    gd = by[f"{B}-gerard"]
    gd["brigades"][:2] = [bde("fr-infantry-brigade", "Leclerc's Brigade", "Gén. de Brigade Leclerc des Essarts", regiments=[fr_regiment("7th Léger", 5, light=True)]),
                          bde("fr-infantry-brigade", "Baudinot's Brigade", "Gén. de Brigade Baudinot", regiments=[fr_regiment("12th Line", 5)]),
                          bde("fr-infantry-brigade", "Gérard's Brigade", "Gén. de Division Gérard", regiments=[fr_regiment("21st Line", 5)])]
    gd["notes"] = [MIKA + " The 127th Line and the Mecklenburgers guarded the park and did not fight.", gd["notes"][-1]]
    ds = by[f"{B}-dessaix"]
    ds["brigades"] = ds["brigades"][1:]
    ds["notes"].insert(0, MIKA + " Mikaberidze gives the division only the 85th and 108th at Borodino, so Barbanègre's 33rd Léger is left out.")
    cp = by[f"{B}-compans"]
    gu = cp["brigades"][2]
    gu["regiments"], gu["units"] = gu["regiments"][:1], gu["units"][:1]
    cp["brigades"].insert(3, bde("fr-infantry-brigade", "Lonchamp's Brigade", "Gén. de Brigade Lonchamp",
                                 units=[u("fr-regimental-battery", "111th Line Artillery Company")], regiments=[fr_regiment("111th Line", 3)]))
    cp["notes"].insert(0, MIKA + " The 111th had three battalions at Borodino.")
    dz = by[f"{B}-delzons"]
    dz["brigades"][:3] = [bde("fr-infantry-brigade", "Huard's Brigade", "Gén. de Brigade Huard",
                              units=[u("fr-regimental-arty-section", "8th Léger Artillery Company"), u("fr-regimental-arty-section", "84th Line Artillery Company")],
                              regiments=[fr_regiment("8th Léger", 2, light=True), fr_regiment("84th Line", 4), fr_regiment("1st Provisional Croatian", 2)]),
                          bde("fr-infantry-brigade", "Plauzonne's Brigade", "Gén. de Brigade Plauzonne",
                              units=[u("fr-regimental-arty-section", "92nd Line Artillery Company"), u("fr-regimental-arty-section", "106th Line Artillery Company")],
                              regiments=[fr_regiment("92nd Line", 4), fr_regiment("106th Line", 4)])]
    dz["notes"].insert(0, MIKA + " Roussel had been killed after Ostrovno; Huard and Plauzonne both fell at Borodino.")
    mc = by[f"{B}-marchand"]
    mc["brigades"] = [bde("wt-infantry-brigade", "Temporary Regiment", "", regiments=[{"name": "Temporary Württemberg Regiment",
                       "units": [u("wt-line-infantry", f"{r}/Temporary Regiment", options=["small-infantry"]) for r in ("I", "II", "III")]}]),
                      bde("wt-divisional-artillery", "Divisional Artillery", units=[u("wt-light-arty", "1st Foot Battery"), u("wt-light-arty", "2nd Foot Battery"), u("wt-horse-arty", "1st Horse Battery")])]
    mc["notes"] = ["Marchand, who had taken over from the Crown Prince, is the book's named commander.",
                   MIKA + " By Borodino the Württemberg infantry, about 1,500 men, had been merged into one temporary regiment of three battalions, all Small.",
                   "Three battalions in a regiment the list caps at two show as a historical departure."]
    p16 = by[f"{B}-16th"]
    p16["name"], p16["command"] = "Krasiński's 16th Division", [cmd("gdw-div-cmd", "Gén. de Brigade Krasiński")]
    for f in forces:
        if f["id"] in (f"{B}-friant", f"{B}-broussier", f"{B}-18th", f"{B}-olsufiev", f"{B}-kapsevich", f"{B}-old-guard", f"{B}-tharreau", f"{B}-ledru"):
            f["notes"].insert(0, MIKA)


BORODINO = {
    "id": "borodino", "name": "Borodino", "date": "7 September 1812", "campaign": "russia-1812",
    "summary": "Kutuzov's stand seventy miles from Moscow. All day the French threw themselves at the Russian left: at the Semenovskoe flèches, taken and retaken through the morning until Bagration fell, and at the Great Redoubt in the centre, finally carried in the afternoon by infantry from the front and cuirassiers from behind. Napoleon would not commit the Guard; the Russians fell back a mile and held. The bloodiest single day of the wars, with some 70,000 killed and wounded, it left the road to Moscow open but the Russian army unbroken.",
    "sources": [MIKABERIDZE, VOVSI, naf("812ICA", "French Army, Battle of Borodino, 5–7 September 1812"), naf("812ICB", "Russian Army, Battle of Borodino, 5–7 September 1812"),
                {"label": "Battle of Borodino (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Borodino"}],
    "forces": [
        # Davout's I Corps
        again(COMPANS, "compans", "Opened the attack on the flèches at dawn through the Utitsa woods; Compans was wounded in the first assault."),
        again(DESSAIX, "dessaix", "Beside Compans's in the assault on the flèches, where Dessaix too was wounded.", formation="4th Division, I Corps (Davout)"),
        again(DUFOUR, "friant", "Davout's reserve division, which finally took Semenovskoe in the late morning and held it; Friant was wounded there.",
              name="Friant's Division", command=[{"unit": "fr-cmd-friant"}]),
        again(MORAND, "morand", "Lent to Eugène, it stormed the Great Redoubt at mid-morning and was thrown out again by Yermolov's counter-attack, losing Bonamy, taken in the redoubt."),
        again(GUDIN, "gerard", "Gudin's division under Gérard, lent to Eugène, joined the final assault on the Great Redoubt.",
              name="Gérard's Division", command=[cmd("fr-div-cmd", "Gén. de Division Gérard")]),
        # Ney's III Corps
        again(RAZOUT, "razout", "Ney's corps attacked the flèches beside Davout's through the morning."),
        again(LEDRU, "ledru", "Beside Razout's in Ney's attacks on the flèches and Semenovskoe."),
        again(MARCHAND, "marchand", "The Württembergers stormed the flèches with Ney and held them against Russian counter-attacks."),
        # Eugène's IV Corps
        again(DELZONS, "delzons", "Opened the battle by storming the village of Borodino itself at dawn, on the far left."),
        again(BROUSSIER, "broussier", "Led the last great assault on the Great Redoubt from the front in the afternoon."),
        ITALIAN_GUARD,
        # Poniatowski's V Corps
        again(PONIATOWSKI_16, "16th", "Poniatowski's Poles worked round the Russian left along the old Smolensk road, fighting for Utitsa and its mound all day."),
        again(PONIATOWSKI_18, "18th", "Beside the 16th in the fighting for Utitsa."),
        # Junot's VIII Corps
        THARREAU, OCHS,
        # The Guard
        again(ROGUET, "roguet", "Held in reserve; Napoleon refused to commit his Guard, saying he would not destroy it eight hundred leagues from France."),
        again(CURIAL, "old-guard", "Held in reserve with the Young Guard, uncommitted all day."),
        again(CLAPAREDE, "claparede", "The Vistula Legion went forward with Friant's division to help hold Semenovskoe."),
        # The reserve cavalry
        again(BRUYERE, "bruyere", "Nansouty's light cavalry, fighting around Semenovskoe through the afternoon."),
        again(SAINT_GERMAIN, "saint-germain", "Nansouty's cuirassiers charged the Russian squares beyond Semenovskoe."),
        again(DAVOUT_CAVALRY, "valence", "Valence's cuirassiers and the I Corps light cavalry, in the charges around the flèches.", name="Valence's Cuirassiers"),
        again(SEBASTIANI, "pajol", "Montbrun's light cavalry, which charged beyond the Great Redoubt after it fell.", name="Pajol's Light Cavalry", command=[cmd("fr-div-cmd", "Gén. de Division Pajol")]),
        MONTBRUN_HEAVY, GROUCHY, THIELMANN, LEPEL, DELABORDE, GUARD_CAVALRY,
        # The Russian 1st Army
        again(EUGEN, "eugen", "Marched across from the right to the left centre, where it was shot to pieces by the French batteries before Semenovskoe."),
        again(OLSUFIEV, "olsufiev", "Baggovut's other division, sent to the far left to hold Utitsa against Poniatowski."),
        again(CHOGLOKOV, "11th", "Ostermann's corps came across to the centre in the afternoon and stood behind the Great Redoubt under the French guns."),
        again(BAKHMETEV, "23rd", "Beside the 11th behind the Great Redoubt; Bakhmetev lost a leg."),
        again(KAPSEVICH, "kapsevich", "Dokhturov's corps held the line north of the Great Redoubt, and in the afternoon took over the left when Bagration fell."),
        again(LIKHACHEV, "likhachev", "Held the Great Redoubt in the afternoon; Likhachev was wounded and taken in it as it fell."),
        GUARD,
        CUIRASSIERS_1, UVAROV, KORFF, KREUTZ,
        again(PLATOV, "platov", "Rode with Uvarov round the French left at midday, the raid that held up the attack on the centre for two hours."),
        # The Russian 2nd Army
        again(KOLUBAKIN, "12th", "Raevsky's corps held the Great Redoubt, the 'Raevsky Redoubt', against Eugène's attacks until the afternoon.", formation="12th Division, VII Corps (Raevsky)"),
        again(PASKEVICH, "paskevich", "Held the Great Redoubt with Raevsky's corps, its 26th Position Battery in the redoubt itself."),
        again(NEVEROVSKY, "neverovsky", "Fought for the flèches beside Vorontsov's grenadiers and was destroyed there."),
        VORONTSOV, MECKLENBURG,
        again(KONOVNITSYN, "konovnitsyn", "Sent across to the flèches; when Bagration fell Konovnitsyn took command of the left and fell back to Semenovskoe."),
        again(STROGANOV, "stroganov", "Tuchkov's grenadiers held the old Smolensk road at Utitsa against Poniatowski; Tuchkov was killed."),
        CUIRASSIERS_2, SIEVERS,
    ],
}
for f in BORODINO["forces"]:
    f["notes"] = [n for n in f["notes"] if not n.startswith("After Nafziger's order of battle for")] + ([NAF] if NAF not in f["notes"] else [])
fix(BORODINO["forces"])


if __name__ == "__main__":
    art = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
    for b in (BORODINO,):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in art:
            b["art"] = art[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
