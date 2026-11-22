"""
Writes the battles of October 1812 as Napoleon left Moscow (src/data/battles/{tarutino,maloyaroslavets}.json).

    python3 scripts/forces/russia_1812_autumn.py && npm run check:forces

Sources (see SOURCES): Nafziger's orders of battle for Borodino (812ICA, 812ICB) and the Grande Armée of 1 August (812HAB),
the nearest he gives, with Wikipedia for the course of each battle. Summaries are our own words.
"""

import copy
import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from russia_1812 import ru_jager_regiment, ru_regiment
from russia_1812_centre import DELZONS, KOLUBAKIN, PASKEVICH
from russia_1812_north import fr_regiment

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
FR, GDW, VL, IT, RU = "france", "grand-duchy-of-warsaw", "vistula-legion", "italy", "russia"


def naf(code, title):
    return {"label": f"{title} (Nafziger Collection {code})", "url": f"https://www.napoleon-series.org/nafzigger/{code}.pdf"}


BORODINO_RU = naf("812ICB", "Russian Army, Battle of Borodino, 5–7 September 1812")
BORODINO_FR = naf("812ICA", "French Army, Battle of Borodino, 5–7 September 1812")
SEPT = "After Nafziger's order of battle for Borodino, six weeks earlier; Borodino's losses, never made good, aren't shown, so the regiments were much weaker than this."
AUG = "After Nafziger's order of battle for the Grande Armée on 1 August; the division had lost heavily since."


def again(f, id_, summary, formation=None):
    g = copy.deepcopy(f)
    g["id"], g["summary"] = id_, summary
    if formation:
        g["formation"] = formation
    return g


def ru_div(id_, name, formation, commander, brigades, summary, notes=()):
    return force(id_, RU, name, formation, "Russian", summary, brigades, command=[commander], notes=[SEPT, *notes])


def ru_bde(name, commander, battery, regiments, jager=False):
    t = "ru-jager-brigade" if jager else "ru-infantry-brigade"
    return bde(t, name, commander, units=[battery] if battery else [], regiments=regiments)


def pos(n):
    return u("ru-position-arty", f"{n} Position Battery")


def lt(n):
    return u("ru-light-arty", f"{n} Light Battery")


# ================================================================ Tarutino, 18 October 1812

EUGEN = ru_div("tarutino-eugen", "Eugen's 4th Division", "4th Division, II Corps (Baggovut)", {"unit": "ru-cmd-eugene-wurttemberg"},
               [ru_bde("Pyshnitsky's Brigade", "Maj-Gen Pyshnitsky", pos("4th"), [ru_regiment("Kremenchug"), ru_regiment("Minsk")]),
                ru_bde("Rossi's Brigade", "Col Rossi", lt("7th"), [ru_regiment("Tobolsk"), ru_regiment("Volhynia")]),
                ru_bde("Pillar's Brigade", "Col Pillar", lt("8th"), [ru_jager_regiment("4th"), ru_jager_regiment("34th")], jager=True)],
               "In the centre column, it came out of the woods late, after the Cossacks had struck, and attacked the French camp on the Chernishnya; Baggovut was killed by one of the first shots.",
               ["Prince Eugen of Württemberg is the book's named commander."])

OLSUFIEV = ru_div("tarutino-olsufiev", "Olsufiev's 17th Division", "17th Division, II Corps (Baggovut)", cmd("ru-div-cmd", "Lt-Gen Olsufiev"),
                  [ru_bde("Ivelich's Brigade", "Maj-Gen Ivelich", pos("17th"), [ru_regiment("Ryazan"), ru_regiment("Brest")]),
                   ru_bde("Vadkovsky's Brigade", "Maj-Gen Vadkovsky", lt("32nd"), [ru_regiment("Belozersk"), ru_regiment("Wilmanstrand")]),
                   ru_bde("Potemkin's Brigade", "Col Potemkin", lt("33rd"), [ru_jager_regiment("30th"), ru_jager_regiment("48th")], jager=True)],
                  "Baggovut's other division, beside Eugen's in the attack on the French left as Murat's men fell back from the camp.")

ORLOV = force("tarutino-orlov-denisov", RU, "Orlov-Denisov's Column", "The right-hand column of Bennigsen's attack", "Russian",
              "Ten Cossack regiments and regular cavalry which went round the French left in the night and at dawn burst into Sébastiani's camp, taking guns and baggage; but they stopped to plunder, and the infantry columns came up too late to cut Murat off.",
              [bde("ru-cossack-brigade", "Cossacks", "", [u("ru-mounted-cossack", f"{n} Cossacks") for n in ("Ataman", "Vlasov III's", "Ilovaisky IV's", "Ilovaisky VIII's", "Denisov VII's", "Grekov XVIII's")]),
               bde("ru-light-cavalry-brigade", "Hussars and Uhlans", "", [u("ru-hussar", "Izyum Hussars", options=["large-cavalry"]), u("ru-uhlan", "Polish Uhlans", options=["large-cavalry"]), u("ru-horse-arty", "6th Horse Battery")]),
               bde("ru-heavy-cavalry-brigade", "Davydov's Dragoons", "", [u("ru-dragoon", "Pskov Dragoons"), u("ru-dragoon", "Moscow Dragoons")])],
              command=[cmd("ru-div-cmd", "Lt-Gen Count Orlov-Denisov")],
              notes=["Wikipedia gives Orlov-Denisov ten Cossack regiments with regular cavalry and a Jäger regiment; the regiments here are those of Platov's and Korff's commands in Nafziger's order of battle for Borodino, as the nearest guide, not a certain list.",
                     "More Cossack regiments than the list's brigade holds, and no infantry, show as historical departures."])

PONIATOWSKI_16 = force("tarutino-16th", GDW, "Zajączek's 16th Division", "16th Division, V Corps (Poniatowski)", "Polish",
                       "Poniatowski's Poles held the French right at Tarutino; when the Russian columns came out of the woods they covered Murat's withdrawal down the road to Spas-Kuplya.",
                       [bde("gdw-infantry-brigade", "Krasiński's Brigade", "Gén. de Brigade Krasiński",
                            regiments=[{"name": f"{n} Line", "units": [u("gdw-polish-infantry", f"{r}/{n} Line", options=["small-infantry"]) for r in ("I", "II", "III")]} for n in ("3rd", "15th")]),
                        bde("gdw-infantry-brigade", "Paszkowski's Brigade", "Gén. de Brigade Paszkowski",
                            regiments=[{"name": "16th Line", "units": [u("gdw-polish-infantry", f"{r}/16th Line", options=["small-infantry"]) for r in ("I", "II", "III")]}]),
                        bde("gdw-cavalry-brigade", "Tyszkiewicz's Brigade", "Gén. de Brigade Tyszkiewicz", [u("gdw-uhlan", "12th Uhlans", options=["small-cavalry"])]),
                        bde("gdw-divisional-artillery", "Foot Battery", units=[u("gdw-foot-arty", "3rd Polish Foot Artillery")])],
                       command=[cmd("gdw-div-cmd", "Gén. de Division Zajączek")],
                       notes=[SEPT.replace("Russian", ""), "After Borodino the V Corps was down to a few thousand men, so every battalion and regiment is Small.", "Mikaberidze gives Krasiński as commanding the division and its first brigade at Borodino, Zajączek having been injured."])

PONIATOWSKI_18 = force("tarutino-18th", GDW, "Kniaziewicz's 18th Division", "18th Division, V Corps (Poniatowski)", "Polish",
                       "The other half of the Polish corps, beside the 16th on the right of Murat's line.",
                       [bde("gdw-infantry-brigade", "Bégański's Brigade", "Gén. de Brigade Bégański",
                            regiments=[{"name": f"{n} Line", "units": [u("gdw-polish-infantry", f"{r}/{n} Line", options=["small-infantry"]) for r in ("I", "II", "III")]} for n in ("2nd", "8th")]),
                        bde("gdw-infantry-brigade", "Potocki's Brigade", "Gén. de Brigade Potocki",
                            regiments=[{"name": "12th Line", "units": [u("gdw-polish-infantry", f"{r}/12th Line", options=["small-infantry"]) for r in ("I", "II", "III")]}]),
                        bde("gdw-cavalry-brigade", "Sułkowski's Brigade", "Gen. Prince Sułkowski",
                            [u("gdw-chasseur-a-cheval", "5th Chasseurs à Cheval", options=["small-cavalry"]), u("gdw-hussar", "13th Hussars", options=["small-cavalry"])]),
                        bde("gdw-divisional-artillery", "Foot Battery", units=[u("gdw-foot-arty", "4th Polish Foot Artillery")])],
                       command=[cmd("gdw-div-cmd", "Gén. de Division Kniaziewicz")],
                       notes=["After Nafziger's order of battle for Borodino.", "After Borodino the V Corps was down to a few thousand men, so every battalion and regiment is Small."])

SEBASTIANI = force("tarutino-sebastiani", FR, "Sébastiani's Cavalry", "II Reserve Cavalry Corps", "French",
                   "Camped carelessly on Murat's left, it was surprised at dawn by Orlov-Denisov's Cossacks, lost its guns and baggage and was driven back, rallying only when Murat led his cavalry against the Russian regulars.",
                   [bde("fr-light-cavalry-brigade", "Desirad's Brigade", "Gén. de Brigade Desirad", [u("fr-chasseur-a-cheval", "11th Chasseurs", options=["small-cavalry"]), u("fr-chasseur-a-cheval", "12th Chasseurs", options=["small-cavalry"])]),
                    bde("fr-light-cavalry-brigade", "Burthe's Brigade", "Gén. de Brigade Burthe", [u("fr-hussar-regt", "5th Hussars", options=["small-cavalry"]), u("fr-hussar-regt", "9th Hussars", options=["small-cavalry"])]),
                    bde("fr-light-cavalry-brigade", "Subervie's Brigade", "Gén. de Brigade Subervie",
                        [u("fr-wurttemberg-horse-jager", "3rd Württemberg Jäger zu Pferd", options=["small-cavalry"]), u("fr-lancer", "Prussian Combined Uhlans", options=["small-cavalry"]),
                         u("fr-hussar-regt", "10th Polish Hussars", options=["small-cavalry"])])],
                   command=[{"unit": "fr-cmd-murat"}],
                   notes=["Murat, the book's named commander, led the advance guard and rallied this cavalry himself.",
                          "After Nafziger's order of battle for Borodino, where these brigades were Pajol's division; by October the reserve cavalry was a few hundred horse a regiment, so all are Small. Sébastiani commanded the corps at Tarutino.",
                          "Three Light Cavalry Brigades and no infantry show as historical departures."])

CLAPAREDE = force("tarutino-claparede", VL, "Claparède's Vistula Legion", "Vistula Legion, Imperial Guard", "Polish",
                  "The Legion's Poles came up from the reserve to steady the line as Murat pulled back.",
                  [bde("vl-infantry-brigade", "Chłopicki's Brigade", "Gén. de Brigade Chłopicki",
                       regiments=[{"name": f"{n} Vistula", "units": [u("vl-infantry", f"{r}/{n} Vistula") for r in ("I", "II")]} for n in ("1st", "2nd")]),
                   bde("vl-infantry-brigade", "Second Brigade", "", regiments=[{"name": "3rd Vistula", "units": [u("vl-infantry", f"{r}/3rd Vistula") for r in ("I", "II")]}])],
                  command=[cmd("vl-div-cmd", "Gén. de Division Claparède")],
                  notes=["After Nafziger's order of battle for Borodino, which gives each Vistula regiment two battalions.",
                         "Wikipedia names the Legion with Murat's advance guard; its place in the fight isn't recorded."])

DUFOUR = force("tarutino-dufour", FR, "Dufour's Division", "2nd Division, I Corps (Davout)", "French",
               "Friant's old division under Dufour, lent to Murat's advance guard; it held the woods on the French left as the Russian infantry came on.",
               [bde("fr-infantry-brigade", "Dufour's Brigade", "Gén. de Brigade Dufour", regiments=[fr_regiment("15th Léger", 5, light=True)]),
                bde("fr-infantry-brigade", "Van Dedem's Brigade", "Gén. de Brigade van Dedem", regiments=[fr_regiment("33rd Line", 5)]),
                bde("fr-infantry-brigade", "Grosne's Brigade", "Gén. de Brigade Grosne",
                    regiments=[fr_regiment("48th Line", 5), {"name": "Joseph Napoléon Regiment", "units": [u("fr-spanish-infantry", f"{r}/Joseph Napoléon") for r in ("II", "III")]}]),
                bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "2/7th Foot Artillery"), u("fr-horse-arty", "5/3rd Horse Artillery")])],
               command=[cmd("fr-div-cmd", "Gén. de Brigade Dufour")],
               notes=["After Nafziger's order of battle for Borodino, where Friant was wounded; Dufour led the division afterwards.",
                      "The horse battery, without three cavalry regiments in the force, shows as a historical departure."])

TARUTINO = {
    "id": "tarutino", "name": "Tarutino", "date": "18 October 1812", "campaign": "russia-1812",
    "summary": "While Napoleon waited in Moscow for a peace that never came, Murat's advance guard sat facing Kutuzov's camp at Tarutino. Bennigsen struck it at dawn: Orlov-Denisov's Cossacks burst into Sébastiani's camp, but the infantry columns lost their way in the woods and came up late, and Murat got his men away with the loss of 2,500 men and three dozen guns. Next day Napoleon left Moscow.",
    "sources": [BORODINO_RU, BORODINO_FR, {"label": "Battle of Tarutino (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Tarutino"}],
    "forces": [SEBASTIANI, PONIATOWSKI_16, PONIATOWSKI_18, CLAPAREDE, DUFOUR, ORLOV, EUGEN, OLSUFIEV],
}
for f in TARUTINO["forces"]:
    if f["side"] == "Polish":
        f["side"] = "French"


# ================================================================ Maloyaroslavets, 24 October 1812

BROUSSIER = force("maloyaroslavets-broussier", FR, "Broussier's Division", "14th Division, IV Corps (Eugène)", "French",
                  "Fed into the burning town behind Delzons's men and fought for it street by street through the day, as it changed hands again and again.",
                  [bde("fr-infantry-brigade", "Sivray's Brigade", "Gén. de Brigade Bertrand de Sivray",
                       units=[u("fr-regimental-arty-section", "18th Léger Artillery Company"), u("fr-regimental-arty-section", "53rd Line Artillery Company")],
                       regiments=[fr_regiment("18th Léger", 2, light=True), fr_regiment("53rd Line", 4),
                                  {"name": "Joseph Napoléon Regiment", "units": [u("fr-spanish-infantry", "I/Joseph Napoléon"), u("fr-spanish-infantry", "IV/Joseph Napoléon")]}]),
                   bde("fr-infantry-brigade", "Alméras's Brigade", "Gén. de Brigade Alméras",
                       units=[u("fr-regimental-arty-section", "9th Line Artillery Company"), u("fr-regimental-arty-section", "35th Line Artillery Company")],
                       regiments=[fr_regiment("9th Line", 4), fr_regiment("35th Line", 4)]),
                   bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "7/2nd Foot Artillery"), u("fr-horse-arty", "3/4th Horse Artillery")])],
                  command=[cmd("fr-div-cmd", "Gén. de Division Broussier")],
                  notes=["Brigades as Mikaberidze and Vovsi give them for Borodino; battalions after Nafziger's return for 1 August, the division having lost heavily since.", "Each French regiment had two 3-pdrs, shown as Regimental Artillery.", "The horse battery, without three cavalry regiments in the force, shows as a historical departure."])


def it_reg(name, n, light=False):
    return {"name": name, "units": [u("it-light-infantry" if light else "it-line-infantry", f"{['I', 'II', 'III', 'IV'][i]}/{name}") for i in range(n)]}


PINO = force("maloyaroslavets-pino", IT, "Pino's Italian Division", "15th Division, IV Corps (Eugène)", "Italian",
             "Eugène's Italians, sent into the town in the afternoon when the French hold on it was failing; they retook it and held it to the end, at heavy cost.",
             [bde("it-infantry-brigade", "Fontana's Brigade", "Gén. de Brigade Fontana", units=[u("it-regimental-arty-section", "2nd Line Artillery Company")],
                  regiments=[it_reg("1st Light (4th Bn)", 1, light=True), it_reg("2nd Line", 4)]),
              bde("it-infantry-brigade", "Guillaume's Brigade", "Gén. de Brigade Guillaume",
                  units=[u("it-regimental-arty-section", "3rd Light Artillery Company"), u("it-regimental-arty-section", "Dalmatian Artillery Company")],
                  regiments=[it_reg("3rd Light", 4, light=True), it_reg("Dalmatian Regiment", 3)]),
              bde("it-infantry-brigade", "Dembowski's Brigade", "Gén. de Brigade Dembowski", units=[u("it-regimental-arty-section", "3rd Line Artillery Company")],
                  regiments=[it_reg("3rd Line", 4)]),
              bde("it-divisional-artillery", "Divisional Artillery", units=[u("it-foot-arty", "14/1st Foot Artillery"), u("it-horse-arty", "2/1st Horse Artillery")])],
             command=[cmd("it-div-cmd", "Gén. de Division Pino")],
             notes=[AUG, "The Dalmatian Regiment is shown as Line.", "Each regiment had two 3-pdrs, shown as Regimental Artillery."])

KAPSEVICH = ru_div("maloyaroslavets-kapsevich", "Kapsevich's 7th Division", "7th Division, VI Corps (Dokhturov)", cmd("ru-div-cmd", "Lt-Gen Kapsevich"),
                   [ru_bde("Lyapunov's Brigade", "Col Lyapunov", pos("7th"), [ru_regiment("Moscow"), ru_regiment("Pskov")]),
                    ru_bde("Aigustov's Brigade", "Col Aigustov", lt("12th"), [ru_regiment("Libau"), ru_regiment("Sofia")]),
                    ru_bde("Kashirinov's Brigade", "Lt-Col Kashirinov", lt("13th"), [ru_jager_regiment("11th"), ru_jager_regiment("36th")], jager=True)],
                   "Dokhturov's corps marched all night to bar the new road south and reached Maloyaroslavets at dawn, just after Delzons's men had crossed the Luzha; it threw them back into the town and fought for it until Raevsky's corps came up.")

LIKHACHEV = ru_div("maloyaroslavets-likhachev", "Likhachev's 24th Division", "24th Division, VI Corps (Dokhturov)", cmd("ru-div-cmd", "Maj-Gen Likhachev"),
                   [ru_bde("Tsibulsky's Brigade", "Col Tsibulsky", pos("24th"), [ru_regiment("Ufa"), ru_regiment("Shirvan")]),
                    ru_bde("Denisyev's Brigade", "Col Denisyev", lt("45th"), [ru_regiment("Tomsk"), ru_regiment("Butyrsk")]),
                    ru_bde("Vuich's Brigade", "Col Vuich", lt("46th"), [ru_jager_regiment("19th"), ru_jager_regiment("40th")], jager=True)],
                   "Dokhturov's second division, fed into the streets as the town changed hands again and again through the day.")

MALOYAROSLAVETS = {
    "id": "maloyaroslavets", "name": "Maloyaroslavets", "date": "24 October 1812", "campaign": "russia-1812",
    "summary": "Leaving Moscow, Napoleon tried to march south-west by the untouched Kaluga road. At Maloyaroslavets Eugène's leading division crossed the Luzha just as Dokhturov's corps arrived; all day the burning town changed hands, eight times by some counts, as both sides fed in division after division. The French held it at nightfall, but Kutuzov's army stood across the road beyond, and Napoleon turned back onto the ruined Smolensk road by which he had come.",
    "sources": [BORODINO_RU, naf("812HAB", "French Grande Armée, 1 August 1812"),
                {"label": "Battle of Maloyaroslavets (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Maloyaroslavets"}],
    "forces": [
        again(DELZONS, "maloyaroslavets-delzons", "Eugène's leading division, which crossed the Luzha in the dark and seized the town, then lost it to Dokhturov's men at dawn; Delzons was killed leading the counter-attack, and his brother beside him."),
        BROUSSIER, PINO, KAPSEVICH, LIKHACHEV,
        again(KOLUBAKIN, "maloyaroslavets-12th", "Raevsky's corps came up in the afternoon and went into the town to relieve Dokhturov's exhausted men.", "12th Division, VII Corps (Raevsky)"),
        again(PASKEVICH, "maloyaroslavets-paskevich", "Paskevich's division went in with Raevsky's attack in the afternoon and fought in the streets until the town was given up at nightfall."),
    ],
}
for f in MALOYAROSLAVETS["forces"]:
    if f["side"] == "Italian":
        f["side"] = "French"
for f in MALOYAROSLAVETS["forces"][-2:]:
    f["notes"] = [n for n in f["notes"] if "Smolensk regiment" not in n and "42nd Jäger" not in n]


if __name__ == "__main__":
    art = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
    for b in (TARUTINO, MALOYAROSLAVETS):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in art:
            b["art"] = art[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
