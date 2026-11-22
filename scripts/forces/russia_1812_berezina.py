"""
Writes the Berezina (src/data/battles/berezina.json), 26–29 November 1812: the crossing at Studienka, fought on both banks.

    python3 scripts/forces/russia_1812_berezina.py && npm run check:forces

After Nafziger's orders of battle for the Grande Armée of 1 August (812HAB, for Victor's IX Corps and Dombrowski), the
French II Corps (812ICD), Chichagov's Army of the Danube (812JCK) and Wittgenstein's corps (812JCH), with Wikipedia for
who fought where. By November every formation was far below these strengths. Summaries are our own words.
"""

import copy
import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from russia_1812 import ru_jager_regiment, ru_regiment
from russia_1812_autumn import naf
from russia_1812_north import fr_regiment
from russia_1812_polotsk import BERG2, FOCK, STEINHEIL, cavalry, eighth, legrand, merle

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
B = "berezina"
FR, GDW, RB, RU = "france", "grand-duchy-of-warsaw", "confederation-of-the-rhine", "russia"
WASTED = "By late November every formation was a fraction of the strength in Nafziger's returns; mark battalions Small or leave some out to suit."


def again(f, slug, summary):
    g = copy.deepcopy(f)
    g["id"] = f"{B}-{slug}"
    g["summary"] = summary
    g["notes"] = [WASTED] + g["notes"]
    return g


def pol_reg(name, n):
    return {"name": f"{name} Line", "units": [u("gdw-polish-infantry", f"{['I', 'II', 'III'][i]}/{name} Line") for i in range(n)]}


PARTOUNEAUX = force(f"{B}-partouneaux", FR, "Partouneaux's Division", "12th Division, IX Corps (Victor)", "French",
                    "Victor's rearguard division, left at Borisov to hold off Wittgenstein; marching to rejoin the corps in the dark on 27 November it took the wrong road, ran into Wittgenstein's army and was forced to surrender almost whole.",
                    [bde("fr-infantry-brigade", "Camus's Brigade", "Gén. de Brigade Camus",
                         units=[u("fr-regimental-arty-section", "29th Léger Artillery Company")],
                         regiments=[fr_regiment("10th Léger (4th Bn)", 1, light=True), fr_regiment("29th Léger", 4, light=True)]),
                     bde("fr-infantry-brigade", "Blanmont's Brigade", "Gén. de Brigade Blanmont",
                         units=[u("fr-regimental-arty-section", "125th Line Artillery Company")],
                         regiments=[{"name": "Provisional Regiment", "units": [u("fr-line-infantry", f"IV/{n} Line") for n in ("36th", "51st", "55th")]}, fr_regiment("125th Line", 3)]),
                     bde("fr-infantry-brigade", "Billard's Brigade", "Gén. de Brigade Billard",
                         units=[u("fr-regimental-arty-section", "44th Line Artillery Company"), u("fr-regimental-arty-section", "126th Line Artillery Company")],
                         regiments=[fr_regiment("44th Line", 2), fr_regiment("126th Line", 4)]),
                     bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", "20/5th Foot Artillery")])],
                    command=[cmd("fr-div-cmd", "Gén. de Division Partouneaux")],
                    notes=[WASTED, "After Nafziger's return for 1 August.", "Two Léger regiments in Camus's brigade, where the list allows one, show as a historical departure."])

DAENDELS = force(f"{B}-daendels", RB, "Daendels's Germans", "26th Division, IX Corps (Victor)", "French",
                 "Victor's Baden, Berg and Hessian troops held the heights above Studienka on the left bank through 28 November against Wittgenstein, so that the army could cross the bridges behind them; the Baden brigade, the last across, was nearly destroyed.",
                 [bde("ocs-berg-infantry-brigade", "Damas's Berg Brigade", "Gén. de Brigade Damas", units=[u("ocs-foot-arty", "Berg Foot Battery")],
                      regiments=[{"name": f"{n} Berg Infantry", "units": [u("ocs-line-infantry", f"{r}/{n} Berg") for r in rs]}
                                 for n, rs in (("1st", ("I", "II")), ("2nd", ("I", "II")), ("3rd", ("I",)), ("4th", ("I", "II")))]),
                  bde("ocs-baden-infantry-brigade", "Hochberg's Baden Brigade", "Gen-Maj Hochberg", units=[u("ocs-baden-jager", "Jäger Battalion 'Lingg'"), u("ocs-foot-arty", "Baden Foot Battery")],
                      regiments=[{"name": f"{n} Baden Line", "units": [u("ocs-line-infantry", f"{r}/{n} Baden") for r in ("I", "II")]} for n in ("1st", "3rd")]),
                  bde("ocs-hessian-infantry-brigade", "Prince Emil's Hessian Brigade", "Gén. Prince Emil of Hesse",
                      regiments=[{"name": "Leib Regiment", "units": [u("ocs-hessian-guard", "I/Leib Regiment"), u("ocs-hessian-guard", "II/Leib Regiment")]},
                                 {"name": "Leibgarde Regiment", "units": [u("ocs-hessian-guard", "I/Leibgarde"), u("ocs-hessian-guard", "II/Leibgarde")]},
                                 {"name": "Garde-Füsiliere", "units": [u("ocs-hessian-guard-fusilier", "I/Garde-Füsiliere"), u("ocs-hessian-guard-fusilier", "II/Garde-Füsiliere")]}])],
                 command=[cmd("cotr-div-cmd", "Gén. de Division Daendels")],
                 notes=[WASTED, "After Nafziger's return for 1 August; Prince Emil's Hessian brigade joined the division in November. The 4th Westphalian Line, also with it, is left out."])

GIRARD_28 = force(f"{B}-girard", GDW, "Girard's Poles", "28th Division, IX Corps (Victor)", "French",
                  "Victor's Polish division, beside Daendels's Germans in the rearguard on the left bank at Studienka.",
                  [bde("gdw-infantry-brigade", "Soyez's Brigade", "Gén. de Brigade Soyez", regiments=[pol_reg("4th", 2), pol_reg("7th", 2)]),
                   bde("gdw-infantry-brigade", "9th Line", "", regiments=[pol_reg("9th", 2)]),
                   bde("gdw-divisional-artillery", "1st Polish Foot Battery", units=[u("gdw-foot-arty", "1st Polish Foot Battery")])],
                  command=[cmd("gdw-div-cmd", "Gén. de Division Girard")],
                  notes=[WASTED, "After Nafziger's return for 1 August. Devilliers's Saxon brigade, which joined later, is left out."])

DOMBROWSKI = force(f"{B}-dombrowski", GDW, "Dombrowski's 17th Polish Division", "17th Division, V Corps", "French",
                   "Holding the bridgehead at Borisov, it was driven out by Chichagov's advance on 21 November; on the 28th it fought beside Oudinot's corps in the woods at Stakhov on the right bank, where Dombrowski was wounded.",
                   [bde("gdw-infantry-brigade", "Żółtowski's Brigade", "Gén. de Brigade Żółtowski", regiments=[pol_reg("1st", 3), pol_reg("6th", 3)]),
                    bde("gdw-infantry-brigade", "Krasiński's Brigade", "Gén. de Brigade Krasiński", regiments=[pol_reg("14th", 3), pol_reg("17th", 3)]),
                    bde("gdw-divisional-artillery", "Divisional Artillery", units=[u("gdw-foot-arty", "10th Polish Foot Artillery"), u("gdw-foot-arty", "11th Polish Foot Artillery")])],
                   command=[cmd("gdw-div-cmd", "Gén. de Division Dombrowski")],
                   notes=[WASTED, "After Nafziger's return for 1 August.", "Two foot batteries where the list's divisional artillery is limited by battalions may show as a historical departure."])

CHAPLITS = force(f"{B}-chaplits", RU, "Chaplits's Detachment", "Army of the Danube (Chichagov)", "Russian",
                 "Chichagov's leading troops on the right bank, which attacked Oudinot's bridgehead at Stakhov on 28 November, and were broken in the woods by Doumerc's cuirassiers.",
                 [bde("ru-jager-brigade", "The Jäger", "", regiments=[ru_jager_regiment("28th"), ru_jager_regiment("32nd")]),
                  bde("ru-light-cavalry-brigade", "Cavalry", "", [u("ru-hussar", "Pavlograd Hussars", options=["large-cavalry"]), u("ru-dragoon", "Tver Dragoons", options=["small-cavalry"]), u("ru-horse-arty", "13th Horse Battery")]),
                  bde("ru-cossack-brigade", "Cossacks and Bashkirs", "", [u("ru-mounted-cossack", "Diachkin's Cossacks"), u("ru-irregular-mounted-cossack", "2nd Kalmyks"), u("ru-irregular-mounted-cossack", "Bashkirs")])],
                 command=[cmd("ru-div-cmd", "Maj-Gen Chaplits")],
                 notes=["After Nafziger's order of battle for the Army of the Danube, 15/27 October.", "No Infantry Brigade shows as a historical departure."])

VOINOV = force(f"{B}-voinov", RU, "Voinov's Corps", "Army of the Danube (Chichagov)", "Russian",
               "The main body of Chichagov's infantry, fed into the woods at Stakhov on the 28th against Oudinot's and Ney's men holding the road to Zembin.",
               [bde("ru-infantry-brigade", "Vladimir and Tambov", "", units=[u("ru-position-arty", "18th Position Battery")], regiments=[ru_regiment("Vladimir"), ru_regiment("Tambov")]),
                bde("ru-infantry-brigade", "Dnieper and Kostroma", "", units=[u("ru-light-arty", "34th Light Battery")], regiments=[ru_regiment("Dnieper"), ru_regiment("Kostroma")]),
                bde("ru-infantry-brigade", "Nasheburg and Apsheron", "", units=[u("ru-position-arty", "9th Position Battery")], regiments=[ru_regiment("Nasheburg"), ru_regiment("Apsheron")]),
                bde("ru-infantry-brigade", "Ryazhsk and Yakutsk", "", units=[u("ru-light-arty", "16th Light Battery")], regiments=[ru_regiment("Ryazhsk", jager="10th"), ru_regiment("Yakutsk")]),
                bde("ru-heavy-cavalry-brigade", "Dragoons", "", [u("ru-dragoon", "St Petersburg Dragoons"), u("ru-dragoon", "Lithuania Dragoons"), u("ru-dragoon", "Seversk Dragoons")]),
                bde("ru-light-cavalry-brigade", "White Russia Hussars", "", [u("ru-hussar", "White Russia Hussars", options=["large-cavalry"])])],
               command=[cmd("ru-div-cmd", "Lt-Gen Voinov")],
               notes=["After Nafziger's order of battle for the Army of the Danube, 15/27 October, which also gives two Cossack regiments and the 17th and 35th Light Batteries, left out.",
                      "Four infantry brigades, more than the list allows in a force of this size, show as historical departures."])

SABANEEV = force(f"{B}-sabaneev", RU, "Sabaneev's Reserve", "Army of the Danube (Chichagov)", "Russian",
                 "Chichagov's reserve, which took over the attack in the woods at Stakhov in the afternoon of the 28th, Sabaneev commanding on the right bank.",
                 [bde("ru-infantry-brigade", "Kolyvan and Kurin", "", units=[u("ru-position-arty", "38th Position Battery")], regiments=[ru_regiment("Kolyvan"), ru_regiment("Kurin")]),
                  bde("ru-infantry-brigade", "Vitebsk and Kozlov", "", units=[u("ru-light-arty", "25th Light Battery")], regiments=[ru_regiment("Vitebsk"), ru_regiment("Kozlov")]),
                  bde("ru-jager-brigade", "The Jäger", "", units=[u("ru-light-arty", "50th Light Battery")],
                      regiments=[ru_jager_regiment("7th"), ru_jager_regiment("12th"), ru_jager_regiment("13th")]),
                  bde("ru-combined-grenadier-brigade", "Converged Grenadiers", "", [u("ru-inf-combined-grenadier", f"Converged Grenadiers {i}") for i in range(1, 7)]),
                  bde("ru-heavy-cavalry-brigade", "Dragoons", "", [u("ru-dragoon", "Dorpat Dragoons"), u("ru-dragoon", "Kinburn Dragoons")]),
                  bde("ru-light-cavalry-brigade", "Olviopol Hussars", "", [u("ru-hussar", "Olviopol Hussars", options=["large-cavalry"])])],
                 command=[cmd("ru-div-cmd", "Lt-Gen Sabaneev")],
                 notes=["After Nafziger's order of battle for the Army of the Danube, which gives the three Jäger regiments seven battalions between them; six are shown. Three Cossack regiments and the 39th Position Battery are left out."])

BEREZINA = {
    "id": "berezina", "name": "Berezina", "date": "26–29 November 1812", "campaign": "russia-1812",
    "summary": "With Chichagov holding the far bank at Borisov and Wittgenstein and Kutuzov closing behind, the Grande Armée was trapped against the Berezina. A feint drew Chichagov south while Eblé's pontonniers, standing in the icy river, built two bridges at Studienka. For three days the army crossed, Oudinot and Ney holding off Chichagov in the woods on the right bank and Victor holding the heights on the left against Wittgenstein, until the bridges were burned on the 29th with thousands of stragglers still on the far side.",
    "sources": [naf("812HAB", "French Grande Armée, 1 August 1812"), naf("812ICD", "French II Corps, 15 September 1812"),
                naf("812JCK", "Russian Forces, Battle of the Berezina, Army of the Danube, 15/27 October 1812"),
                naf("812JCH", "Russian I Corps after joined by the Finland Corps, 16/28 October 1812"),
                {"label": "Battle of Berezina (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Berezina"}],
    "forces": [
        again(legrand(B, ""), "legrand", "Oudinot's leading division across the bridges on the 26th, which drove back Chaplits's men and held the woods at Stakhov on the right bank on the 28th; Legrand was wounded."),
        again(eighth(B, "Gén. de Division Maison", ""), "maison", "Beside Legrand's in the woods at Stakhov on the 28th, holding the road to Zembin open."),
        again(merle(B, ""), "merle", "Merle's Swiss charged the Russians again and again in the woods at Stakhov on the 28th, losing most of their men."),
        again(cavalry(B, ""), "doumerc", "On the 28th Doumerc's cuirassiers, a few hundred men, charged through the woods into Chichagov's infantry, breaking several battalions and taking 2,000 prisoners, the last great charge of the campaign."),
        DOMBROWSKI, PARTOUNEAUX, DAENDELS, GIRARD_28,
        CHAPLITS, VOINOV, SABANEEV,
        again(STEINHEIL, "steinheil", "Wittgenstein's leading troops on the left bank, which attacked Victor's rearguard on the heights above Studienka on the 28th."),
        again(BERG2, "berg", "In Wittgenstein's attacks on Victor's rearguard on the left bank, and the shelling of the bridges."),
        again(FOCK, "fock", "Wittgenstein's reserve, which came up behind the attack on Studienka."),
    ],
}
for f in BEREZINA["forces"]:
    if f["side"] in ("Polish", "Bavarian"):
        f["side"] = "French"


if __name__ == "__main__":
    art = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
    for b in (BEREZINA,):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in art:
            b["art"] = art[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
