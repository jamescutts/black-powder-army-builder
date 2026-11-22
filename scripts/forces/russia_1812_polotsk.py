"""
Writes the two battles of Polotsk (src/data/battles/{polotsk,polotsk-2}.json): Oudinot's and then Saint-Cyr's II and
VI Corps against Wittgenstein's I Corps on the Dvina.

    python3 scripts/forces/russia_1812_polotsk.py && npm run check:forces

Sources (see SOURCES): Nafziger's returns of the French II Corps (812ICD), the Bavarian VI Corps (812HCE, 812IXA) and
Wittgenstein's corps (812HBL, 812JCH), after Fabry and the French archives, with Wikipedia for the course of each battle.
Summaries are our own words. Staff Ratings are set by ratings.py.
"""

import copy
import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from russia_1812 import ru_jager_regiment, ru_regiment
from russia_1812_north import fr_regiment

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
FR, BAV, RU = "france", "bavaria", "russia"


def naf(code, title):
    return {"label": f"{title} (Nafziger Collection {code})", "url": f"https://www.napoleon-series.org/nafzigger/{code}.pdf"}


FR_RETURN = "After Nafziger's return of the II Corps for 15 September 1812."
FR_GUNS = "Each regiment had its own two or four 3-pdrs, shown as Regimental Artillery."
BAV_WEAK = ("Typhus and the march had wrecked the Bavarian corps: Nafziger's returns give whole regiments three to five hundred men, "
            "so every battalion is Small.")


def guns(regs):
    """Regimental artillery: a section for two guns, a battery for four"""
    return [u("fr-regimental-battery" if four else "fr-regimental-arty-section", f"{name} Artillery Company") for name, four in regs]


# ---------------------------------------------------------------- Oudinot's (later Saint-Cyr's) II Corps

def legrand(battle, summary):
    return force(f"{battle}-legrand", FR, "Legrand's Division", "6th Division, II Corps", "French", summary,
                 [bde("fr-infantry-brigade", "Albert's Brigade", "Gén. de Brigade Albert", units=guns([("26th Léger", False)]),
                      regiments=[fr_regiment("26th Léger", 4, light=True)]),
                  bde("fr-infantry-brigade", "Moreau's Brigade", "Gén. de Brigade Moreau", units=guns([("19th Line", False), ("56th Line", False)]),
                      regiments=[fr_regiment("19th Line", 4), fr_regiment("56th Line", 4)]),
                  bde("fr-infantry-brigade", "Pamplona's Brigade", "Gén. de Brigade Pamplona", units=guns([("128th Line", False)]),
                      regiments=[fr_regiment("128th Line", 2)]),
                  bde("fr-divisional-artillery", "Divisional Artillery",
                      units=[u("fr-foot-arty", "11/5th Foot Artillery"), u("fr-horse-arty", "6/3rd Horse Artillery")])],
                 command=[cmd("fr-div-cmd", "Gén. de Division Legrand")],
                 notes=[FR_RETURN, FR_GUNS, "The horse battery, without the three cavalry regiments the list wants for it, shows as a historical departure."])


def eighth(battle, commander, summary):
    return force(f"{battle}-eighth", FR, f"{commander.split()[-1]}'s Division", "8th Division, II Corps", "French", summary,
                 [bde("fr-infantry-brigade", "Vives's Brigade", "Gén. de Brigade Vives", units=guns([("11th Léger", True), ("2nd Line", True)]),
                      regiments=[fr_regiment("11th Léger", 4, light=True), fr_regiment("2nd Line", 5)]),
                  bde("fr-infantry-brigade", "Pouget's Brigade", "Gén. de Brigade Pouget", units=guns([("37th Line", True), ("124th Line", False)]),
                      regiments=[fr_regiment("37th Line", 4), fr_regiment("124th Line", 3)]),
                  bde("fr-divisional-artillery", "Divisional Artillery",
                      units=[u("fr-foot-arty", "15/5th Foot Artillery"), u("fr-horse-arty", "1/3rd Horse Artillery")])],
                 command=[cmd("fr-div-cmd", commander)],
                 notes=[FR_RETURN, FR_GUNS, "Pouget's brigade mixes a regimental battery with a section, and the horse battery has none of the three cavalry regiments the list wants for it; both show as historical departures."])


def merle(battle, summary):
    return force(f"{battle}-merle", FR, "Merle's Division", "9th Division, II Corps", "French", summary,
                 [bde("fr-infantry-brigade", "Condras's Brigade", "Gén. de Brigade Condras", units=guns([("1st Swiss", False), ("2nd Swiss", False)]),
                      regiments=[fr_regiment("1st Swiss", 2), fr_regiment("2nd Swiss", 3)]),
                  bde("fr-infantry-brigade", "Amey's Brigade", "Gén. de Brigade Amey", units=guns([("4th Swiss", False), ("3rd Croatian", False)]),
                      regiments=[fr_regiment("4th Swiss", 3), fr_regiment("3rd Provisional Croatian", 2)]),
                  bde("fr-infantry-brigade", "Coutard's Brigade", "Gén. de Brigade Coutard", units=guns([("3rd Swiss", False), ("123rd Line", False)]),
                      regiments=[fr_regiment("3rd Swiss", 3), fr_regiment("123rd Line", 3)]),
                  bde("fr-divisional-artillery", "Divisional Artillery",
                      units=[u("fr-foot-arty", "4/7th Foot Artillery"), u("fr-horse-arty", "5/2nd Horse Artillery")])],
                 command=[cmd("fr-div-cmd", "Gén. de Division Merle")],
                 notes=[FR_RETURN, FR_GUNS, "The Swiss regiments and the Croatians are shown as Line.",
                        "The horse battery, without the three cavalry regiments the list wants for it, shows as a historical departure."])


def cavalry(battle, summary):
    return force(f"{battle}-cavalry", FR, "Corbineau's and Doumerc's Cavalry", "II Corps cavalry and 3rd Cuirassier Division", "French", summary,
                 [bde("fr-light-cavalry-brigade", "Castex's Brigade", "Gén. de Brigade Castex",
                      [u("fr-chasseur-a-cheval", "23rd Chasseurs à Cheval", options=["small-cavalry"]), u("fr-chasseur-a-cheval", "24th Chasseurs à Cheval", options=["small-cavalry"])]),
                  bde("fr-light-cavalry-brigade", "Corbineau's Brigade", "Gén. de Brigade Corbineau",
                      [u("fr-chasseur-a-cheval", "7th Chasseurs à Cheval", options=["small-cavalry"]), u("fr-chasseur-a-cheval", "20th Chasseurs à Cheval", options=["small-cavalry"]),
                       u("fr-lancer", "8th Chevau-légers Lanciers", options=["small-cavalry"])]),
                  bde("fr-heavy-cavalry-brigade", "Doumerc's Cuirassiers", "Gén. de Division Doumerc",
                      [u("fr-cuirassier", "4th Cuirassiers"), u("fr-cuirassier", "7th Cuirassiers", options=["small-cavalry"]), u("fr-cuirassier", "14th Cuirassiers")]),
                  bde("fr-artillery-brigade", "Doumerc's Horse Artillery",
                      units=[u("fr-horse-arty", "1/6th Horse Artillery"), u("fr-horse-arty", "3/6th Horse Artillery")])],
                 command=[cmd("fr-div-cmd", "Gén. de Division Doumerc")],
                 notes=[FR_RETURN + " The light regiments were down to two to four hundred men each, so they are Small, as is the 7th Cuirassiers.",
                        "Doumerc's three brigades of one regiment each are shown together.",
                        "Cavalry without infantry, two light brigades and the second horse battery show as historical departures."])


# ---------------------------------------------------------------- Saint-Cyr's Bavarian VI Corps

def bav_reg(name, n=2):
    return {"name": f"{name} Line Infantry", "units": [u("bav-line-infantry", f"{['I', 'II'][i]}/{name}") for i in range(n)], "options": []}


def bav_bde(name, commander, light, regiments):
    b = bde("bav-infantry-brigade", name, commander, units=[u("bav-light-infantry", light, options=["small-infantry"])], regiments=regiments)
    for r in b["regiments"]:
        for x in r["units"]:
            x["options"] = ["small-infantry"]
    return b


def deroy(battle, summary, commander="Gen-Lt von Deroy"):
    return force(f"{battle}-deroy", BAV, "Deroy's Division", "19th Division, VI Corps (Saint-Cyr)", "Bavarian", summary,
                 [bav_bde("Siebein's Brigade", "Gen-Maj von Siebein", "1st Light Bn", [bav_reg("1st"), bav_reg("9th")]),
                  bav_bde("Raglovich's Brigade", "Gen-Maj von Raglovich", "3rd Light Bn", [bav_reg("4th"), bav_reg("10th")]),
                  bav_bde("Rechberg's Brigade", "Gen-Maj Count Rechberg", "6th Light Bn", [bav_reg("8th")]),
                  bde("bav-divisional-artillery", "Divisional Artillery",
                      units=[u("bav-light-arty", "1st Light Battery Widemann"), u("bav-light-arty", "3rd Light Battery Halder"),
                             u("bav-foot-arty", "11th Battery Brack"), u("bav-position-battery", "6th Battery Rois (12-pdrs)")])],
                 command=[cmd("bav-div-cmd", commander)],
                 notes=["After Nafziger's returns of 29 August and 15 September 1812.", BAV_WEAK, "The howitzer battery is left out."])


def wrede(battle, summary):
    return force(f"{battle}-wrede", BAV, "Wrede's Division", "20th Division, VI Corps (Saint-Cyr)", "Bavarian", summary,
                 [bav_bde("Vincenti's Brigade", "Gen-Maj von Vincenti", "2nd Light Bn", [bav_reg("2nd"), bav_reg("6th")]),
                  bav_bde("Beckers's Brigade", "Gen-Maj Count Beckers", "4th Light Bn", [bav_reg("3rd"), bav_reg("7th")]),
                  bav_bde("Third Brigade", "", "5th Light Bn", [bav_reg("5th"), bav_reg("11th")]),
                  bde("bav-divisional-artillery", "Divisional Artillery",
                      units=[u("bav-light-arty", "2nd Light Battery Gotthard"), u("bav-light-arty", "4th Light Battery Gravenreuth"),
                             u("bav-foot-arty", "5th Battery Hoffstetten"), u("bav-foot-arty", "8th Battery Ulmer"),
                             u("bav-position-battery", "4th Battery Berchem (12-pdrs)")])],
                 command=[cmd("bav-div-cmd", "Gen-Lt von Wrede")],
                 notes=["After Nafziger's returns of 29 August and 15 September 1812.", BAV_WEAK,
                        "Two foot batteries where the list's divisional artillery takes one show as a historical departure.",
                        "The corps' four chevau-léger regiments were with the main army, not at Polotsk."])


# ================================================================ First Polotsk, 17–18 August 1812

HELFREICH = force("polotsk-helfreich", RU, "Helfreich's Advance Guard", "Advance Guard, I Corps (Wittgenstein)", "Russian",
                  "Kulnev's old advance guard, under Helfreich since his death, which led the attack on the French positions before Polotsk on the 17th.",
                  [bde("ru-light-cavalry-brigade", "Grodno Hussars", "", [u("ru-hussar", "Grodno Hussars (four squadrons)"), u("ru-mounted-cossack", "Cossacks", options=["small-cavalry"])]),
                   bde("ru-jager-brigade", "The Jäger", "", units=[u("ru-light-arty", "26th Light Battery")],
                       regiments=[ru_jager_regiment("25th"), ru_jager_regiment("26th")])],
                  command=[cmd("ru-div-cmd", "Maj-Gen Helfreich")],
                  notes=["After Nafziger's return of Wittgenstein's corps for 14 August.", "No Infantry Brigade shows as a historical departure."])

BERG = force("polotsk-berg", RU, "Berg's First Line", "5th Division, I Corps (Wittgenstein)", "Russian",
             "The corps' first line, which pressed the French back towards Polotsk on the 17th and on the 18th was caught by Saint-Cyr's surprise counter-attack in the afternoon, losing guns before the cavalry and reserves restored the line.",
             [bde("ru-infantry-brigade", "Kazachkovsky's Brigade", "Col Kazachkovsky", units=[u("ru-position-arty", "5th Position Battery")],
                  regiments=[ru_regiment("Sevsk"), ru_regiment("Kaluga", jager="23rd")]),
              bde("ru-infantry-brigade", "Prince Sibirsky's Brigade", "Maj-Gen Prince Sibirsky", units=[u("ru-position-arty", "28th Position Battery"), u("ru-light-arty", "9th Light Battery")],
                  regiments=[ru_regiment("Perm"), ru_regiment("Mogilev"), ru_regiment("Converged Infantry")]),
              bde("ru-heavy-cavalry-brigade", "Berg's Cavalry", "", [u("ru-cuirassier", "Converged Cuirassiers (depot squadrons)"), u("ru-dragoon", "Yamburg Dragoons (two squadrons)", options=["small-cavalry"])]),
              bde("ru-guard-light-cavalry-brigade", "Guard Depot Squadrons", "", [u("ru-lg-hussar", "Converged Guard Squadrons", options=["small-cavalry"])])],
             command=[cmd("ru-div-cmd", "Maj-Gen Berg")],
             notes=["After Nafziger's return for 14 August. The 23rd Jäger is attached to the Kaluga regiment, as the list takes Jäger.",
                    "Three regiments in Sibirsky's brigade and two batteries in it, the converged Guard depot squadrons, and dragoons and cuirassiers mixed in one brigade, show as historical departures."])

SAZONOV = force("polotsk-sazonov", RU, "Sazonov's Second Line", "14th Division, I Corps (Wittgenstein)", "Russian",
                "The 14th Division in the second line, fed in to hold the centre when Saint-Cyr's attack broke through on the 18th.",
                [bde("ru-infantry-brigade", "Tenginsk and Estonia", "", units=[u("ru-light-arty", "27th Light Battery")],
                     regiments=[ru_regiment("Tenginsk"), ru_regiment("Estonia")]),
                 bde("ru-infantry-brigade", "Tula and Navaginsk", "",
                     regiments=[ru_regiment("Tula"), ru_regiment("Navaginsk", jager="Converged (11th and 36th Reserve)")]),
                 bde("ru-heavy-cavalry-brigade", "Riga Dragoons", "", [u("ru-dragoon", "Riga Dragoons")])],
                command=[cmd("ru-div-cmd", "Maj-Gen Sazonov")],
                notes=["After Nafziger's return for 14 August. The converged Jäger of the 11th's and 36th's reserve battalions are attached to the Navaginsk regiment."])

KAKHOVSKY = force("polotsk-kakhovsky", RU, "Kakhovsky's Reserve", "Reserve, I Corps (Wittgenstein)", "Russian",
                  "The corps' grenadiers and horse guns, which held the line while Wittgenstein drew off after the second day.",
                  [bde("ru-combined-grenadier-brigade", "Converged Grenadiers", "",
                       units=[u("ru-inf-combined-grenadier", "Converged Grenadiers, 14th Division"), u("ru-inf-combined-grenadier", "Converged Grenadiers, 14th Division"),
                              u("ru-position-arty", "14th Position Battery")]),
                   bde("ru-grenadier-brigade", "Reserve Grenadiers", "",
                       regiments=[{"name": f"{r} Grenadiers (Reserve Bn)", "units": [u("ru-grenadier", f"{r} Grenadiers (Reserve Bn)", options=["small"])]}
                                  for r in ("Leib", "Tauride", "Ekaterinoslav", "Pavlovsky", "Arakcheyev", "St Petersburg")]),
                   bde("ru-heavy-cavalry-brigade", "Yamburg Dragoons", "", [u("ru-dragoon", "Yamburg Dragoons (two squadrons)", options=["small-cavalry"]),
                                                                            u("ru-horse-arty", "1st Horse Battery"), u("ru-horse-arty", "3rd Horse Battery")])],
                  command=[cmd("ru-div-cmd", "Lt-Gen Kakhovsky")],
                  notes=["After Nafziger's return for 14 August, which also gives two converged infantry regiments; they're left out.",
                         "Six reserve grenadier battalions in a brigade that takes two regiments, and two horse batteries with one dragoon regiment, show as historical departures."])

POLOTSK = {
    "id": "polotsk", "name": "First Polotsk", "date": "17–18 August 1812", "campaign": "russia-1812",
    "summary": "Wittgenstein followed Oudinot back to Polotsk on the Dvina and attacked. On the 17th the Russians pressed the French and Bavarians back to the town, and Oudinot was wounded. Saint-Cyr, taking over, struck back without warning in the afternoon of the 18th, his Bavarians and French columns breaking the Russian line and taking guns, though Deroy was mortally wounded; Wittgenstein fell back, and Saint-Cyr won his marshal's baton.",
    "sources": [naf("812ICD", "French II Corps, 15 September 1812"), naf("812HCE", "French VI Corps, 29 August 1812"),
                naf("812HBL", "Russian I Corps, 14 August 1812"),
                {"label": "First Battle of Polotsk (Wikipedia)", "url": "https://en.wikipedia.org/wiki/First_Battle_of_Polotsk"}],
    "forces": [
        legrand("polotsk", "Held the line before Polotsk on the 17th, and on the 18th led the French part of Saint-Cyr's counter-attack."),
        eighth("polotsk", "Gén. de Division Verdier", "Fought in the centre on the 17th, where Verdier was wounded; Maison took over the division."),
        merle("polotsk", "Merle's Swiss and Croatians held the left of the line by the Dvina on both days."),
        cavalry("polotsk", "Out on the flanks; on the 18th Doumerc's cuirassiers rode down the Russian cavalry that had taken a Bavarian battery."),
        deroy("polotsk", "Saint-Cyr's right wing, which opened the surprise attack on the 18th and drove deep into the Russian line; Deroy fell mortally wounded at its head."),
        wrede("polotsk", "Beside Deroy's, it went in on the 18th and took the Russian batteries in the centre."),
        HELFREICH, BERG, SAZONOV, KAKHOVSKY,
    ],
}


# ================================================================ Second Polotsk, 18–20 October 1812

YASHVIL = force("polotsk-2-yashvil", RU, "Yashvil's Advance Guard", "Advance Guard, I Corps (Wittgenstein)", "Russian",
                "The strongest of Wittgenstein's columns, which attacked the French entrenchments in front of Polotsk on the 18th and fought its way into the town in the night of the 19th.",
                [bde("ru-light-cavalry-brigade", "Hussars and Cossacks", "", [u("ru-hussar", "Grodno Hussars", options=["large-cavalry"]), u("ru-hussar", "Converged Hussars"),
                                                                                u("ru-mounted-cossack", "Rodionov II's Don Cossacks"), u("ru-horse-arty", "1st Horse Battery")]),
                 bde("ru-jager-brigade", "The Jäger", "", units=[u("ru-light-arty", "26th Light Battery")],
                     regiments=[ru_jager_regiment("2nd"), ru_jager_regiment("3rd"), ru_jager_regiment("24th"), ru_jager_regiment("25th")]),
                 bde("ru-infantry-brigade", "Mogilev, Podolsk and Navaginsk", "", units=[u("ru-position-arty", "14th Position Battery", options=[])],
                     regiments=[ru_regiment("Mogilev"), ru_regiment("Podolsk"), ru_regiment("Navaginsk")])],
                command=[cmd("ru-div-cmd", "Lt-Gen Prince Yashvil")],
                notes=["After Nafziger's return for 16/28 October, which gives the 2nd, 3rd, 24th and 25th Jäger seven battalions between them, and also a converged dragoon regiment and Platov's Cossacks, left out.",
                       "Four Jäger regiments and three line regiments in a brigade, where the list takes three and two, show as historical departures."])

STEINHEIL = force("polotsk-2-steinheil", RU, "Steinheil's Finland Corps", "Right Wing, with Wittgenstein's I Corps", "Russian",
                  "Steinheil's troops from Riga, the veterans of Mesoten, which came down the left bank of the Dvina, crossed to attack the French rear from the south and so cut off their retreat.",
                  [bde("ru-infantry-brigade", "First Line", "", units=[u("ru-position-arty", "6th Position Battery")],
                       regiments=[ru_regiment("Tenginsk", jager="26th"), ru_regiment("Tula")]),
                   bde("ru-infantry-brigade", "Estonia and Navaginsk", "", regiments=[ru_regiment("Estonia"), ru_regiment("Navaginsk")]),
                   bde("ru-infantry-brigade", "Adadurov's Second Line", "Maj-Gen Adadurov", units=[u("ru-light-arty", "11th Light Battery")],
                       regiments=[ru_regiment("Petrovsk"), ru_regiment("Lithuania")]),
                   bde("ru-heavy-cavalry-brigade", "Dragoons", "", [u("ru-dragoon", "Mitau Dragoons"), u("ru-dragoon", "Riga Dragoons")])],
                  command=[cmd("ru-div-cmd", "Lt-Gen Count Steinheil")],
                  notes=["After Nafziger's return for 16/28 October, which puts Wittgenstein's 14th Division regiments with Steinheil's on the right wing; the Navaginsk regiment appears in both his and the advance guard's column."])

BERG2 = force("polotsk-2-berg", RU, "Berg's Left Wing", "Left Wing, I Corps (Wittgenstein)", "Russian",
              "Attacked the French lines on the left on the 18th, where the converged Guard cavalry and the Jäger stormed the redoubts.",
              [bde("ru-infantry-brigade", "Bibikov's First Line", "Maj-Gen Bibikov", units=[u("ru-position-arty", "5th Position Battery"), u("ru-light-arty", "7th Light Battery")],
                   regiments=[ru_regiment("Perm", jager="Converged"), ru_regiment("Sevsk")]),
               bde("ru-infantry-brigade", "Second Line", "", regiments=[ru_regiment("Kaluga", n=2), ru_regiment("Azov", n=2)]),
               bde("ru-heavy-cavalry-brigade", "Dragoons", "", [u("ru-dragoon", "Yamburg Dragoons")]),
               bde("ru-guard-light-cavalry-brigade", "Converged Guard Cavalry", "", [u("ru-lg-hussar", "Converged Guard Cavalry")])],
              command=[cmd("ru-div-cmd", "Lt-Gen Berg")],
              notes=["After Nafziger's return for 16/28 October, which gives the Kaluga and Azov regiments five battalions between them; four are shown.",
                     "Guard cavalry without the infantry brigades it needs, and two batteries in a brigade, show as historical departures."])

FOCK = force("polotsk-2-fock", RU, "Fock's Reserve", "Reserve, I Corps (Wittgenstein)", "Russian",
             "The grenadiers and marines of the reserve, brought up to support the attack on the town.",
             [bde("ru-infantry-brigade", "Rachmanov's Right Reserve", "Maj-Gen Rachmanov", units=[u("ru-position-arty", "21st Position Battery")],
                  regiments=[ru_regiment("Nizov"), ru_regiment("1st Marine")]),
              bde("ru-combined-grenadier-brigade", "Converged Grenadiers", "",
                  [u("ru-inf-combined-grenadier", f"Converged Grenadiers {i}, 5th and 14th Divisions") for i in (1, 2, 3, 4)]),
              bde("ru-grenadier-brigade", "Reserve Grenadiers", "", regiments=[
                  {"name": f"{n} Reserve Grenadier Regiment", "units": [u("ru-grenadier", f"I/{n} Reserve Grenadiers"), u("ru-grenadier", f"II/{n} Reserve Grenadiers")]}
                  for n in ("1st", "2nd", "3rd")]),
              bde("ru-heavy-cavalry-brigade", "Converged Cuirassiers", "", [u("ru-cuirassier", "Converged Cuirassiers"), u("ru-horse-arty", "3rd Horse Battery")])],
             command=[cmd("ru-div-cmd", "Maj-Gen Fock")],
             notes=["After Nafziger's return for 16/28 October.", "Three reserve grenadier regiments where the list's brigade takes two, and the horse battery with one cavalry regiment, show as historical departures."])

BAVARIANS = force("polotsk-2-bavarians", BAV, "The Bavarian Corps", "VI Corps (Wrede)", "Bavarian",
                  "All that was left of Saint-Cyr's Bavarians by October, about two thousand men, who held the entrenchments in front of the town and covered the crossing of the Dvina when Polotsk was given up.",
                  [bav_bde("Deroy's Division", "Gen-Maj von Raglovich", "3rd Light Bn", [bav_reg("1st"), bav_reg("4th")]),
                   bav_bde("Wrede's Division", "Gen-Maj von Vincenti", "2nd Light Bn", [bav_reg("2nd"), bav_reg("6th")]),
                   bde("bav-divisional-artillery", "Corps Artillery", units=[u("bav-light-arty", "Light Battery"), u("bav-position-battery", "12-pdr Battery")])],
                  command=[cmd("bav-div-cmd", "Gen-Lt von Wrede")],
                  notes=[BAV_WEAK, "The two divisions, merged in practice, are shown as a brigade each of their strongest regiments; the rest were down to a few hundred men."])

POLOTSK2 = {
    "id": "polotsk-2", "name": "Second Polotsk", "date": "18–20 October 1812", "campaign": "russia-1812",
    "summary": "Reinforced by Steinheil's Finland Corps, Wittgenstein came back against Saint-Cyr's worn-down French and Bavarians at Polotsk. His columns stormed the entrenchments before the town on the 18th, and as Steinheil crossed the Dvina to come in from the south Saint-Cyr, wounded, gave the town up in the night of the 19th after fierce street fighting, retreating with the threat to the Grande Armée's line of retreat now real.",
    "sources": [naf("812ICD", "French II Corps, 15 September 1812"), naf("812IXA", "Bavarian VI Corps, 15 September 1812"),
                naf("812JCH", "Russian I Corps after joined by the Finland Corps, 16/28 October 1812"),
                {"label": "Second Battle of Polotsk (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Second_Battle_of_Polotsk"}],
    "forces": [
        legrand("polotsk-2", "Held the entrenched camp in front of Polotsk against Yashvil's attacks on the 18th."),
        eighth("polotsk-2", "Gén. de Division Maison", "Held the town's defences and fought for its streets in the night of the 19th."),
        merle("polotsk-2", "Merle's Swiss held the line by the Dvina and fought a desperate rearguard as the town was given up."),
        cavalry("polotsk-2", "Covered the flanks of the entrenched camp, and the retreat over the Dvina."),
        BAVARIANS, YASHVIL, STEINHEIL, BERG2, FOCK,
    ],
}


if __name__ == "__main__":
    art = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
    for b in (POLOTSK, POLOTSK2):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in art:
            b["art"] = art[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
