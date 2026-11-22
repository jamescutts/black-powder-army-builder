"""
Writes the first forces of the War of Liberation (src/data/battles/{mockern,lutzen,bautzen,grossbeeren}.json):
the French, their German and Italian allies, and the Russians, from Nafziger's orders of battle. The Prussians
are still to come: each battle lists them as cards saying so (`toCome`), until a list fits them (the 1815
Prussian list is the likeliest).

    python3 scripts/forces/liberation_1813.py && npm run check:forces

There are no 1813 army lists, so every force borrows the nearest: A Clash of Eagles' 1812 lists for the French,
the Imperial Guard, the Confederation of the Rhine, Italy, Saxony and Russia (whose list covers 1812-15). Each
force's notes say so. Summaries are our own words. Staff Ratings are set by ratings.py.
"""

import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
ART = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
NAF = "https://www.napoleon-series.org/nafzigger/"
FR, IT, CR, FIG, SAX, RU = "france", "italy", "confederation-of-the-rhine", "french-imperial-guard", "saxony", "russia"
PRUSSIA_FLAG = "/flags/prussia.png"
ROMAN = ["I", "II", "III", "IV", "V", "VI"]

LIST_FR = ("Built from A Clash of Eagles' French 1812 list, the nearest to 1813: there is no list for the army "
           "Napoleon raised after Russia, largely of conscripts and of battalions drawn from depots all over the Empire.")
CONSCRIPTS = ("Its battalions were mostly young conscripts of the classes of 1813 and 1814. They are rated as ordinary "
              "Line, as they fought: the list's Wavering or Morale 5 would suit those who broke more readily.")
NO_REGT_GUNS = "Regimental guns were lost in Russia and not replaced, so the division has none."
TWO_BATTERIES = "The division's two foot batteries, where the list allows one, show as a historical departure."
LIST_RU = "Built from A Clash of Eagles' Russian list, which covers 1812-15."
ONE_BN = ("By the spring of 1813 Russian infantry regiments were down to a single field battalion each, the rest "
          "having gone back to recruit; each regiment is shown as its one battalion.")


def bns(unit, reg, n, start=0, **kw):
    """A regiment's battalions, "I/134th Line" and on"""
    return [u(unit, f"{ROMAN[start + i]}/{reg}", **kw) for i in range(n)]


def regt(name, units):
    return {"name": name, "units": units}


def line(reg, n, start=0):
    return regt(reg, bns("fr-line-infantry", reg, n, start))


def light(reg, n, start=0):
    return regt(reg, bns("fr-light-infantry", reg, n, start))


def provisional(name, battalions, light_=False):
    """A provisional regiment: two depot battalions of different regiments, "3/40th Line" and so on"""
    unit = "fr-light-infantry" if light_ else "fr-line-infantry"
    return regt(name, [u(unit, b) for b in battalions])


def foot(*names):
    return bde("fr-divisional-artillery", "Divisional Artillery", units=[u("fr-foot-arty", n) for n in names])


def ru_bn(name, attached=None):
    """One Russian battalion, as its regiment, with a battalion attached to it as the list allows (a unit dict)"""
    units = [u("ru-inf-combined-grenadier", f"{name} Infantry")]
    if attached:
        units.append(attached)
    return regt(f"{name} Infantry" + (f" with {attached['name']}" if attached else ""), units)


def to_come(name, formation, summary):
    return {"side": "Prussian", "name": name, "formation": formation, "summary": summary, "flag": PRUSSIA_FLAG}


def battle(id_, name, date, summary, sources, forces, prussians, alliances=(("Russian", "Prussian"),)):
    return {"id": id_, "name": name, "date": date, "campaign": "liberation-1813", "summary": summary,
            "sources": sources, "forces": forces, "toCome": prussians, "alliances": [list(a) for a in alliances]}


def write(b):
    ratings.apply(b)
    commanders.apply(b)
    if b["id"] in ART:
        b["art"] = ART[b["id"]]
    # Keep the file's keys in the order the others have them
    order = ["id", "name", "date", "campaign", "art", "sides", "alliances", "summary", "sources", "forces", "toCome"]
    out = {k: b[k] for k in order if k in b}
    (OUT / f"{b['id']}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(f"{b['name']}: {len(b['forces'])} forces, {len(b['toCome'])} to come")


# ================================================================ Möckern, 5 April 1813

APRIL = {"label": "Grande Armée, 25 April 1813 (Nafziger Collection 813DCB)", "url": NAF + "813DCB.pdf"}
APRIL_NOTE = "After Nafziger's return of 25 April, three weeks after the fight; Nafziger has no order of battle for Möckern itself."

MK_LAGRANGE = force(
    "mockern-lagrange", FR, "Lagrange's Division", "18th Division, V Corps (Lauriston)", "French",
    "Lauriston's leading division, posted round Wahlitz with its outposts forward in Dannigkow and Gommern. Hünerbein's East Prussians stormed Dannigkow in the early afternoon and the village was fought over for hours, the 134th's companies holding it until the French drew back on Gommern at dusk.",
    [bde("fr-infantry-brigade", "Charrière's Brigade", "Gén. de Brigade Charrière",
         regiments=[line("134th Line", 2), line("154th Line", 4)]),
     bde("fr-infantry-brigade", "Suden's Brigade", "Gén. de Brigade Suden",
         regiments=[line("155th Line", 4), regt("3rd Foreign (Irish Legion)", bns("fr-line-infantry", "Irish Legion", 2))]),
     foot("10/1st Foot Artillery", "12/1st Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Lagrange")],
    notes=[LIST_FR, APRIL_NOTE, CONSCRIPTS,
           "The Irish Legion (3rd Foreign Regiment), two battalions, is shown as Line.",
           NO_REGT_GUNS, TWO_BATTERIES])

MK_ZUCCHI = force(
    "mockern-zucchi", IT, "Zucchi's Italian Brigade", "2nd Brigade, 35th Division (Gérard), XI Corps", "French",
    "The Italians held Vehlitz with four battalions and four guns, and two more on the Windmühlenberg behind it. When Borstell's Prussians and Berg's Russians came on in the late afternoon they refused a summons to surrender and were driven off the hill at the bayonet.",
    [bde("it-infantry-brigade", "Zucchi's Brigade", "",
         regiments=[regt("2nd Italian Light", bns("it-light-infantry", "2nd Italian Light", 2, start=2)),
                    regt("5th Italian Line", bns("it-line-infantry", "5th Italian Line", 4))]),
     bde("it-divisional-artillery", "Artillery", units=[u("it-horse-arty", "3rd Italian Horse Battery", options=["half-battery"])])],
    command=[cmd("it-div-cmd", "Gén. de Brigade Zucchi")],
    notes=["Built from A Clash of Eagles' Italian 1812 list, the nearest to 1813.", APRIL_NOTE,
           "The accounts give the brigade four guns at Vehlitz: the division's Italian horse battery, shown as a half battery. With fewer units than the list wants for it, it shows as a historical departure.",
           "Zucchi, a brigadier, commands the force, so he is its commander rather than its brigade's.",
           "The brigade has no divisional commander: Gérard's French brigade (the 6th and 112th Line) wasn't engaged."])

MK_CAVALRY = force(
    "mockern-cavalry", FR, "The Light Cavalry at Zeddenick", "1st Light Cavalry Division, I Cavalry Corps", "French",
    "All the horse Eugène had left after Russia, about 1,200 sabres in the remnants of a dozen regiments, holding Zeddenick on the right. Late in the day Oppen's Prussian horse came up with Cossacks and a half battery and put them to flight, and a counter-charge at Vehlitz was broken by a volley and two squadrons of Prussian dragoons.",
    [bde("fr-light-cavalry-brigade", "Lancers and Hussars", "",
         [u("fr-lancer", "7th Chevau-légers Lanciers", options=["small-cavalry"]),
          u("fr-lancer", "9th Chevau-légers Lanciers", options=["small-cavalry"]),
          u("fr-hussar-regt", "8th Hussars", options=["small-cavalry"])]),
     bde("fr-light-cavalry-brigade", "Combined Chasseurs", "",
         [u("fr-chasseur-a-cheval", "Combined 3rd, 13th, 19th and 22nd Chasseurs")]),
     bde("fr-divisional-artillery", "Horse Artillery", units=[u("fr-horse-arty", "Horse Battery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Bruyère")],
    notes=[LIST_FR, APRIL_NOTE,
           "The German account names the 7th Chevau-légers, 8th Hussars and a 9th lancer regiment (Polish, it says; Nafziger has the 9th Chevau-légers), with parts of four chasseur regiments, about 1,200 horse with one battery. Nafziger puts them in Bruyère's division; the account doesn't name the commander.",
           "Each regiment was a few hundred men at most, so the lancers and hussars are Small and the chasseurs one combined regiment.",
           "Cavalry without infantry shows as a historical departure."])

MK_ROTH = force(
    "mockern-roth", RU, "Roth's Advance Guard", "Advance guard of Berg's Corps (Wittgenstein)", "Russian",
    "The head of Berg's corps, which reached Vehlitz about four in the afternoon and joined Borstell's Prussians in the attack on the village and the Windmühlenberg, its Jäger and militia covering the left; the Grodno Hussars helped break the French cavalry's counter-charge.",
    [bde("ru-infantry-brigade", "Berg's Battalions", "Maj-Gen Roth",
         units=[u("ru-light-arty", "Light Battery #27")],
         regiments=[ru_bn("Tenginsk"), ru_bn("Estonia", u("ru-opolchenie", "Olonetz-Vologda Opolchenie"))]),
     bde("ru-jager-brigade", "26th Jäger", "",
         regiments=[regt("26th Jäger", [u("ru-jager", "26th Jäger")])]),
     bde("ru-light-cavalry-brigade", "Grodno Hussars", "", [u("ru-hussar", "Grodno Hussars")])],
    command=[cmd("ru-div-cmd", "Maj-Gen Roth")],
    notes=[LIST_RU, ONE_BN,
           "The German account names the 26th Jäger, the Olonetz-Vologda militia battalion and two battalions of Berg's corps at Vehlitz, with the Grodno Hussars; the two battalions aren't named, so they are the 14th Division's Tenginsk and Estonia regiments, the 26th Jäger's own division, from Nafziger's order of battle for Lützen. So is the light battery.",
           "The militia battalion is Opolchenie, attached to the Estonia regiment as the list takes it.",
           "A Jäger brigade of one regiment, and a light battery with fewer battalions than the list wants for it, show as historical departures."])

MOCKERN = battle(
    "mockern", "Möckern", "5 April 1813",
    "Eugène, holding the Elbe with the remains of the Grande Armée and the first of the new conscript divisions, came out of Magdeburg towards Berlin and met Wittgenstein's Russians and Yorck's and Bülow's Prussians east of the river. It was three fights more than one battle: at Dannigkow, where Hünerbein's East Prussians stormed the village; at Vehlitz and the Windmühlenberg, where Borstell and Berg drove off the Italians; and at Zeddenick, where Oppen's cavalry routed the French horse. That night Eugène fell back to Magdeburg, and next day behind the Elbe.",
    [APRIL,
     {"label": "Battle of Möckern (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_M%C3%B6ckern"},
     {"label": "Gefecht bei Möckern (German Wikipedia)", "url": "https://de.wikipedia.org/wiki/Gefecht_bei_M%C3%B6ckern"}],
    [MK_LAGRANGE, MK_ZUCCHI, MK_CAVALRY, MK_ROTH],
    [to_come("Yorck's Corps", "Prussian corps, with Wittgenstein",
             "Yorck's advance guard under Hünerbein, three East Prussian battalions with hussars, dragoons, Cossacks and twelve guns, which stormed Dannigkow and held it against Lagrange's counter-attacks; the rest of the corps stood at Leitzkau."),
     to_come("Bülow's Corps", "Borstell's brigade and Oppen's advance guard",
             "Borstell's Pomeranian and East Prussian battalions, with the Queen's Dragoons, which took Vehlitz and the Windmühlenberg with Berg's Russians; and Oppen's cavalry, the 'mad' Major von Platen's dragoons and the Leib Hussars, which routed the French horse at Zeddenick.")])


# ================================================================ Lützen, 2 May 1813

LZ_FR = {"label": "French Forces at Gross Görschen or Lützen, 2 May 1813 (Nafziger Collection 813EAA)", "url": NAF + "813EAA.pdf"}
LZ_AL = {"label": "Russo-Prussian Order of Battle for Gross Görschen or Lützen, 2 May 1813 (Nafziger Collection 813ECD)", "url": NAF + "813ECD.pdf"}
LZ_NOTE = "After Nafziger's order of battle for Lützen, with strengths of 25 April."


def souham(id_, summary, notes=()):
    return force(
        id_, FR, "Souham's Division", "8th Division, III Corps (Ney)", "French", summary,
        [bde("fr-infantry-brigade", "Chasseraux's Brigade", "Gén. de Brigade Chasseraux",
             regiments=[provisional("6th Provisional Légère", ["2/6th Léger", "3/25th Léger"], True),
                        provisional("10th Provisional Légère", ["3/16th Léger", "1/28th Léger"], True),
                        provisional("14th Provisional Line", ["4/34th Line", "3/40th Line"]),
                        provisional("19th Provisional Line", ["6/32nd Line", "3/58th Line"])]),
         bde("fr-infantry-brigade", "Chemineau's Brigade", "Gén. de Brigade Chemineau",
             regiments=[provisional("21st Provisional Line", ["3/59th Line", "4/69th Line"]),
                        provisional("24th Provisional Line", ["3/88th Line", "3/103rd Line"]),
                        regt("22nd Line", [u("fr-line-infantry", f"{b}/22nd Line") for b in ("1", "3", "4", "6")])]),
         foot("9/2nd Foot Artillery", "10/2nd Foot Artillery")],
        command=[cmd("fr-div-cmd", "Gén. de Division Souham")],
        notes=[LIST_FR, *notes, CONSCRIPTS,
               "Most of its regiments were provisional: two depot battalions of different regiments put together, each shown as its two battalions.",
               "Its two provisional light regiments, where the list allows one light regiment in a division, and Chasseraux's four regiments, where the list allows three in a brigade, show as historical departures.",
               NO_REGT_GUNS, TWO_BATTERIES])


LZ_SOUHAM = souham(
    "lutzen-souham",
    "Ney's leading division, camped in the four villages south of Lützen, Gross-Görschen, Klein-Görschen, Rahna and Kaja, when Blücher's Prussians came at it at midday. Its conscripts were driven from village to village and came back again and again; Souham's division lost more than a third of its strength in the day.",
    [LZ_NOTE])

LZ_BRENIER = force(
    "lutzen-brenier", FR, "Brenier's Division", "9th Division, III Corps (Ney)", "French",
    "Sent forward from Kaja to help Souham, it fought for Klein-Görschen and Rahna through the afternoon. Brenier was wounded, and Ney himself came up to lead its battalions back into the villages.",
    [bde("fr-infantry-brigade", "Anthing's Brigade", "Gén. de Brigade Anthing",
         regiments=[provisional("2nd Provisional Légère", ["3/2nd Léger", "3/4th Léger"], True),
                    light("29th Léger", 2), line("136th Line", 4)]),
     bde("fr-infantry-brigade", "Grillot's Brigade", "Gén. de Brigade Grillot",
         regiments=[line("138th Line", 4), line("145th Line", 4)]),
     foot("2/9th Foot Artillery", "11/9th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Brenier")],
    notes=[LIST_FR, LZ_NOTE, CONSCRIPTS,
           "Two light regiments, where the list allows one in a division, show as a historical departure.",
           NO_REGT_GUNS, TWO_BATTERIES])

LZ_GIRARD = force(
    "lutzen-girard", FR, "Girard's Division", "10th Division, III Corps (Ney)", "French",
    "In the second line at the start, it was thrown into Klein-Görschen and Rahna as Souham's battalions gave way. Girard, twice wounded, refused to leave the field and led his men back in on foot.",
    [bde("fr-infantry-brigade", "Goris's Brigade", "Gén. de Brigade Goris",
         regiments=[provisional("4th Provisional Légère", ["4/5th Léger", "4/12th Léger"], True), line("139th Line", 4)]),
     bde("fr-infantry-brigade", "Van Dedem's Brigade", "Gén. de Brigade Van Dedem",
         regiments=[line("140th Line", 4), line("141st Line", 4)]),
     foot("3/7th Foot Artillery", "4/7th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Girard")],
    notes=[LIST_FR, LZ_NOTE, CONSCRIPTS, NO_REGT_GUNS, TWO_BATTERIES])

LZ_RICARD = force(
    "lutzen-ricard", FR, "Ricard's Division", "11th Division, III Corps (Ney)", "French",
    "Ney's reserve, at Starsiedel when the battle began, it came into Kaja in the afternoon and retook the village when the Prussian Guard and Yorck's men had driven the others out.",
    [bde("fr-infantry-brigade", "Tarayre's Brigade", "Gén. de Brigade Tarayre",
         regiments=[light("9th Léger", 2, start=2),
                    provisional("17th Provisional Line", ["4/43rd Line", "3/75th Line"]),
                    provisional("18th Provisional Line", ["3/50th Line", "4/65th Line"])]),
     bde("fr-infantry-brigade", "Dumoulin's Brigade", "Gén. de Brigade Dumoulin",
         regiments=[line("142nd Line", 4), line("144th Line", 4)]),
     foot("18/1st Foot Artillery", "19/7th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Ricard")],
    notes=[LIST_FR, LZ_NOTE, CONSCRIPTS, NO_REGT_GUNS, TWO_BATTERIES])

LZ_MARCHAND = force(
    "lutzen-marchand", CR, "Marchand's Division", "39th Division, III Corps (Ney)", "French",
    "Ney's German division, Baden, Hessian and Frankfurt troops, on the left round Klein-Görschen and Eisdorf, which held its ground against the Prussian and Russian attacks there through the afternoon.",
    [bde("ocs-baden-infantry-brigade", "Stockhorn's Baden Brigade", "Gen-Maj von Stockhorn",
         units=[u("ocs-foot-arty", "1st Baden Foot Battery", options=["half-battery"])],
         regiments=[regt("1st Baden Line", [u("ocs-line-infantry", "II/1st Baden Line")]),
                    regt("3rd Baden Line", bns("ocs-line-infantry", "3rd Baden Line", 2))]),
     bde("ocs-hessian-infantry-brigade", "Prince Emil's Hessian Brigade", "Gen-Maj Prince Emil of Hesse",
         units=[u("ocs-foot-arty", "Hessian Foot Battery (half)", options=["half-battery"])],
         regiments=[regt("Hessian Leib-Garde", bns("ocs-hessian-guard", "Hessian Leib-Garde", 2)),
                    regt("1st Hessian Light", bns("ocs-hessian-guard-fusilier", "1st Hessian Light", 2))]),
     bde("rb-infantry-brigade", "Hessian Line and Frankfurt", "",
         regiments=[regt("2nd Hessian Line", bns("rb-line-infantry", "2nd Hessian Line", 2)),
                    regt("Frankfurt 'Zweyer' Regiment", [u("rb-line-infantry", "II/Frankfurt")])])],
    command=[cmd("cotr-div-cmd", "Gén. de Division Marchand")],
    notes=["Built from A Clash of Eagles' Confederation of the Rhine 1812 list, the nearest to 1813.", LZ_NOTE,
           "The 1st Hessian Light Regiment is shown as the list's Hessian Guard Fusiliers, the only Hessian light troops it has.",
           "The list's Hessian brigade has only Guard regiments, so the 2nd Hessian (Line) Regiment and the Frankfurt battalion are a Rheinbund brigade.",
           "The Baden battery had four guns and the Hessians half a battery of three, each shown as a half battery."])

LZ_DUMOUSTIER = force(
    "lutzen-dumoustier", FIG, "Dumoustier's Young Guard", "1st Young Guard Division, Imperial Guard (Mortier)", "French",
    "Napoleon's last reserve. As the light failed, with Kaja lost again and Ney's divisions spent, he sent sixteen battalions of the Young Guard in four columns under Mortier, behind a battery of seventy guns, through Kaja and Rahna; the allies gave up the villages and drew off in the night.",
    [bde("fig-young-guard-brigade", "Berthezène's Brigade", "Gén. de Brigade Berthezène",
         units=[u("fig-yg-foot-arty", "1st Young Guard Foot Battery")],
         regiments=[regt("Fusilier-Chasseurs", [u("fig-fusilier-chasseurs", "I/Fusilier-Chasseurs")]),
                    regt("Fusilier-Grenadiers", [u("fig-fusilier-grenadiers", "I/Fusilier-Grenadiers")]),
                    regt("7th Tirailleurs", bns("fig-yg-tirailleurs", "7th Tirailleurs", 2))]),
     bde("fig-young-guard-brigade", "Lanusse's Brigade", "Gén. de Brigade Lanusse",
         regiments=[regt("1st Tirailleurs", bns("fig-yg-tirailleurs", "1st Tirailleurs", 2)),
                    regt("2nd Tirailleurs", bns("fig-yg-tirailleurs", "2nd Tirailleurs", 2))]),
     bde("fig-young-guard-brigade", "Tindal's Brigade", "Gén. de Brigade Tindal",
         units=[u("fig-yg-foot-arty", "2nd Young Guard Foot Battery")],
         regiments=[regt("1st Voltigeurs", bns("fig-yg-voltigeurs", "1st Voltigeurs", 2)),
                    regt("2nd Voltigeurs", bns("fig-yg-voltigeurs", "2nd Voltigeurs", 2)),
                    regt("6th Tirailleurs", bns("fig-yg-tirailleurs", "6th Tirailleurs", 2))]),
     bde("fig-artillery-reserve", "Guard Artillery", units=[u("fig-og-heavy-foot-arty", "2nd Old Guard Foot Battery")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Dumoustier")],
    notes=["Built from A Clash of Eagles' Imperial Guard 1812 list, the nearest to 1813.", LZ_NOTE,
           "Nafziger lists the 6th Tirailleurs in both Berthezène's and Tindal's brigades; it is shown once, with Tindal.",
           "The 2nd Old Guard Foot Battery of 12-pdrs, attached to the division, is in the Guard artillery reserve, as the list takes it.",
           "Three Young Guard brigades, where the list allows two without Old Guard, and Tindal's battery in a brigade of four battalions, where the list wants six, show as historical departures."])

LZ_BERG = force(
    "lutzen-berg", RU, "Berg's Corps", "Right wing, second line (Yorck)", "Russian",
    "Wittgenstein's Russian infantry in Yorck's second line, which came up behind the Prussians in the afternoon and fought for Kaja and Rahna beside them; its battalions had fought the whole of 1812 under Wittgenstein on the Dvina.",
    [bde("ru-infantry-brigade", "Mesentsov's Brigade", "Maj-Gen Mesentsov",
         units=[u("ru-position-arty", "Position Battery #5")],
         regiments=[ru_bn("Perm"), ru_bn("Sevsk", u("ru-volunteer-jager", "Grand Duchess Catherine's Battalion"))]),
     bde("ru-infantry-brigade", "Prince of Siberia's Brigade", "Maj-Gen Prince of Siberia",
         regiments=[ru_bn("Kaluga"), ru_bn("Mogilev")]),
     bde("ru-infantry-brigade", "Helfreich's Brigade", "Maj-Gen Helfreich",
         units=[u("ru-light-arty", "Light Battery #27")],
         regiments=[ru_bn("Tenginsk"), ru_bn("Estonia")]),
     bde("ru-light-cavalry-brigade", "Alexeyev's Brigade", "Maj-Gen Alexeyev", [u("ru-dragoon", "Mitau Dragoons")])],
    command=[cmd("ru-div-cmd", "Lt-Gen Berg")],
    notes=[LIST_RU, LZ_NOTE, ONE_BN,
           "The Grand Duchess Catherine's Battalion, raised on her estates in 1812, is shown as Volunteer Jäger attached to the Sevsk regiment.",
           "The position battery, with fewer battalions than the list wants for it, shows as a historical departure."])

LZ_EUGEN = force(
    "lutzen-eugen", RU, "Eugen of Württemberg's Corps", "II Corps, left wing", "Russian",
    "On the allied left, it came up late in the morning and pushed towards Starsiedel against Marmont's corps, then was drawn into the fighting round Kaja; at nightfall it covered the allied withdrawal.",
    [bde("ru-infantry-brigade", "Shilvinsky's Brigade", "Col Shilvinsky",
         units=[u("ru-light-arty", "Light Battery #7")],
         regiments=[ru_bn("Murom"), ru_bn("Revel"), ru_bn("Chernigov")]),
     bde("ru-jager-brigade", "Kapustin's Brigade", "Col Kapustin",
         regiments=[regt("20th Jäger", [u("ru-jager", "20th Jäger")]), regt("21st Jäger", [u("ru-jager", "21st Jäger")])]),
     bde("ru-infantry-brigade", "Treffurt's Brigade", "Col Treffurt",
         units=[u("ru-light-arty", "Light Battery #33")],
         regiments=[ru_bn("Tobolsk"), ru_bn("Volhynia"), ru_bn("Kremenchug")]),
     bde("ru-jager-brigade", "Ivanov's Brigade", "Col Ivanov",
         units=[u("ru-light-arty", "Light Battery #6")],
         regiments=[regt("4th Jäger", [u("ru-jager", "4th Jäger")]), regt("34th Jäger", [u("ru-jager", "34th Jäger")])]),
     bde("ru-cossack-brigade", "Ukrainian Cossacks", "",
         [u("ru-mounted-cossack", "1st Ukrainian Cossacks"), u("ru-mounted-cossack", "3rd Ukrainian Cossacks")])],
    command=[{"unit": "ru-cmd-eugene-wurttemberg"}],
    notes=[LIST_RU, LZ_NOTE, ONE_BN,
           "Prince Eugen of Württemberg is the book's named commander. His corps was Shakhovskoy's 3rd and St Priest's 4th Divisions, shown together.",
           "The Ukrainian Cossack regiments, raised in 1812, are shown as Mounted Cossacks.",
           "Two Jäger brigades, three-regiment infantry brigades and three light batteries, more than the list allows for the corps' ten line battalions, show as historical departures."])

LUTZEN = battle(
    "lutzen", "Lützen", "2 May 1813",
    "Wittgenstein and Blücher, hoping to catch Napoleon's army strung out on the march to Leipzig, fell on Ney's corps in its villages south of Lützen. All afternoon the Prussians and Russians fought Ney's conscripts for Gross-Görschen, Klein-Görschen, Rahna and Kaja, which changed hands again and again; Scharnhorst was mortally wounded. Napoleon brought up his other corps from both flanks, and at dusk the Young Guard retook the villages behind a great battery. The allies withdrew in good order, but Napoleon, with almost no cavalry, could not pursue.",
    [LZ_FR, LZ_AL, {"label": "Battle of Lützen (1813) (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_L%C3%BCtzen_(1813)"}],
    [LZ_SOUHAM, LZ_BRENIER, LZ_GIRARD, LZ_RICARD, LZ_MARCHAND, LZ_DUMOUSTIER, LZ_BERG, LZ_EUGEN],
    [to_come("Blücher's Corps", "Zieten's, Klüx's and Röder's brigades, with Dolffs's cavalry",
             "The Silesian brigades of Zieten and Klüx, which opened the attack on Gross-Görschen and fought for the villages all afternoon; Röder's Brandenburg brigade with the Guard infantry, which stormed Klein-Görschen and Kaja; and Dolffs's Garde du Corps and cuirassiers, which charged the French squares at dusk, Dolffs killed."),
     to_come("Yorck's Corps", "Hünerbein's and Horn's brigades",
             "The old Prussian auxiliary corps of 1812, which came up in the afternoon and fought for Kaja beside Berg's Russians.")])


# ================================================================ Bautzen, 21 May 1813: the northern flank

BZ_FR = {"label": "French Forces at Bautzen 20/21 May 1813 (Nafziger Collection 813ECK)", "url": NAF + "813ECK.pdf"}
BZ_III = {"label": "French III Corps at Bautzen, 20/21 May 1813 (Nafziger Collection 813ECJ)", "url": NAF + "813ECJ.pdf"}
BZ_AL = {"label": "Russo-Prussian Forces at Bautzen 20/21 May 1813 (Nafziger Collection 813ECE)", "url": NAF + "813ECE.pdf"}
BZ_NOTE = "After Nafziger's order of battle for Bautzen, with strengths of mid-May."
BZ_SECTOR = "Bautzen's forces are those of the northern flank on 21 May, where Ney's and Lauriston's corps fought Barclay's Russians and Kleist's Prussians round Gleina and Preititz."

BZ_SOUHAM = souham(
    "bautzen-souham",
    "Leading Ney's march round the allied right on 21 May, it took Preititz at about eleven in the morning, was thrown out again by Kleist's Prussians, and retook it as the rest of III Corps came up; Ney then halted to wait for orders, and the allies' line of retreat stayed open.",
    [BZ_NOTE, BZ_SECTOR])

BZ_DELMAS = force(
    "bautzen-delmas", FR, "Delmas's Division", "9th Division, III Corps (Ney)", "French",
    "Brenier's old division, under Delmas since Brenier's wound at Lützen, which followed Souham to Preititz and helped hold it against Kleist and Barclay through the afternoon.",
    [bde("fr-infantry-brigade", "Anthing's Brigade", "Gén. de Brigade Anthing",
         regiments=[provisional("2nd Provisional Légère", ["3/2nd Léger", "3/4th Léger"], True),
                    regt("29th Léger", [u("fr-light-infantry", "I/29th Léger")]), line("136th Line", 4)]),
     bde("fr-infantry-brigade", "Second Brigade", "",
         regiments=[line("138th Line", 4), line("145th Line", 4)]),
     foot("1/9th Foot Artillery", "11/9th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Delmas")],
    notes=[LIST_FR, BZ_NOTE, BZ_SECTOR, CONSCRIPTS,
           "Two light regiments, where the list allows one in a division, show as a historical departure.",
           NO_REGT_GUNS, TWO_BATTERIES])

BZ_MAISON = force(
    "bautzen-maison", FR, "Maison's Division", "16th Division, V Corps (Lauriston)", "French",
    "Lauriston's leading division on 21 May, which crossed the Spree at Klix and attacked Barclay's Russians on the Gleina heights, turning the allied right while Ney went for Preititz.",
    [bde("fr-infantry-brigade", "Avril's Brigade", "Gén. de Brigade Avril", regiments=[line("151st Line", 4)]),
     bde("fr-infantry-brigade", "Penne's Brigade", "Gén. de Brigade Penne", regiments=[line("153rd Line", 3)]),
     foot("1/1st Foot Artillery", "3/1st Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Maison")],
    notes=[LIST_FR, BZ_NOTE, BZ_SECTOR, CONSCRIPTS, NO_REGT_GUNS, TWO_BATTERIES])

BZ_PUTHOD = force(
    "bautzen-puthod", FR, "Puthod's Division", "17th Division, V Corps (Lauriston)", "French",
    "Lauriston's second division, which followed Maison against Gleina and pushed Barclay's Russians back on Baruth in the afternoon as the allied right gave way.",
    [bde("fr-infantry-brigade", "Vachot's Brigade", "Gén. de Brigade Vachot",
         regiments=[line("146th Line", 4), line("147th Line", 4)]),
     bde("fr-infantry-brigade", "Pastol's Brigade", "Gén. de Brigade Pastol", regiments=[line("148th Line", 4)]),
     foot("1/5th Foot Artillery", "11/5th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Puthod")],
    notes=[LIST_FR, BZ_NOTE, BZ_SECTOR, CONSCRIPTS, NO_REGT_GUNS, TWO_BATTERIES])

BZ_CHAPLITZ = force(
    "bautzen-chaplitz", RU, "Chaplitz's Advance Guard", "Advance guard, 3rd Army of the West (Barclay de Tolly)", "Russian",
    "Barclay's outposts beyond Gleina, which met Lauriston's and Ney's columns as they crossed the Spree on the morning of 21 May and fell back fighting on the main line.",
    [bde("ru-jager-brigade", "Rudzevich's Brigade", "Maj-Gen Rudzevich",
         units=[u("ru-light-arty", "Light Battery #34")],
         regiments=[regt("12th Jäger", bns("ru-jager", "12th Jäger", 2)), regt("22nd Jäger", bns("ru-jager", "22nd Jäger", 2))]),
     bde("ru-light-cavalry-brigade", "Kozlovsky's Brigade", "Col Kozlovsky",
         [u("ru-hussar", "Olviopol Hussars", options=["small-cavalry"]), u("ru-uhlan", "Zhitomir Uhlans", options=["small-cavalry"])]),
     bde("ru-cossack-brigade", "Grekov's Brigade", "Maj-Gen Grekov VIII",
         [u("ru-mounted-cossack", "Grekov #8 Don Cossacks"), u("ru-mounted-cossack", "Kuteinikov Don Cossacks"),
          u("ru-mounted-cossack", "Isaev #2 Don Cossacks")])],
    command=[cmd("ru-div-cmd", "Lt-Gen Chaplitz")],
    notes=[LIST_RU, BZ_NOTE, BZ_SECTOR,
           "The Jäger regiments had two battalions each; the hussars (364 men) and uhlans (142) were each two weak squadrons, so they are Small.",
           "An advance guard without line infantry, and its light battery, show as historical departures."])

BZ_SHCHERBATOV = force(
    "bautzen-shcherbatov", RU, "Shcherbatov's Division", "18th Division, 3rd Army of the West (Barclay de Tolly)", "Russian",
    "The right of Barclay's line on the Gleina heights, which held off Maison's and Puthod's attacks through the morning before Barclay, outflanked, fell back on Preititz and Baruth.",
    [bde("ru-infantry-brigade", "Bernodossov's Brigade", "Maj-Gen Bernodossov",
         units=[u("ru-light-arty", "Light Battery #35")],
         regiments=[ru_bn("Vladimir"), ru_bn("Dnieper")]),
     bde("ru-infantry-brigade", "Heidenreich's Brigade", "Col Heidenreich", regiments=[ru_bn("Kostroma"), ru_bn("Tambov")]),
     bde("ru-jager-brigade", "Karnielov's Brigade", "Maj-Gen Karnielov",
         regiments=[regt("28th Jäger", [u("ru-jager", "28th Jäger")]), regt("32nd Jäger", [u("ru-jager", "32nd Jäger")])]),
     bde("ru-light-cavalry-brigade", "Umanets's Brigade", "Maj-Gen Umanets",
         [u("ru-dragoon", "Kinburn Dragoons", options=["small-cavalry"]), u("ru-mounted-jager", "Seversk Mounted Jäger", options=["small-cavalry"])])],
    command=[cmd("ru-div-cmd", "Maj-Gen Prince Shcherbatov")],
    notes=[LIST_RU, BZ_NOTE, BZ_SECTOR, ONE_BN,
           "Umanets's two cavalry regiments, of about 250 men each, are Small."])

BZ_INSOV = force(
    "bautzen-insov", RU, "Insov's Division", "9th Division, 3rd Army of the West (Barclay de Tolly)", "Russian",
    "The left of Barclay's line, towards Preititz, which with Kleist's Prussians fought to retake the village from Ney in the early afternoon.",
    [bde("ru-infantry-brigade", "Poltaratsky's Brigade", "Maj-Gen Poltaratsky",
         units=[u("ru-light-arty", "Light Battery #28")],
         regiments=[ru_bn("Nasheburg"), ru_bn("Yakutsk")]),
     bde("ru-jager-brigade", "Udom's Brigade", "Maj-Gen Udom I",
         regiments=[regt("10th Jäger", [u("ru-jager", "10th Jäger")]), regt("38th Jäger", [u("ru-jager", "38th Jäger")])]),
     bde("ru-light-cavalry-brigade", "Pahlen's Brigade", "Maj-Gen Pahlen II",
         [u("ru-dragoon", "Tver Dragoons", options=["small-cavalry"]), u("ru-dragoon", "Dorpat Dragoons", options=["small-cavalry"])])],
    command=[cmd("ru-div-cmd", "Maj-Gen Insov")],
    notes=[LIST_RU, BZ_NOTE, BZ_SECTOR, ONE_BN,
           "Pahlen's two dragoon regiments, of about 300 men each, are Small.",
           "The light battery, with fewer battalions than the list wants for it, shows as a historical departure."])

BAUTZEN = battle(
    "bautzen", "Bautzen", "20–21 May 1813",
    "The allies stood behind the Spree at Bautzen in a fortified line along the heights. On the first day Napoleon forced the river and took the town; on the second he pinned the allied centre and left while Ney's and Lauriston's corps marched round the right. Barclay's Russians and Kleist's Prussians held them off long enough round Gleina and Preititz, and when Ney, unsure of his orders, halted instead of driving on to the allies' rear, Wittgenstein and Blücher got their armies away to the east.",
    [BZ_FR, BZ_III, BZ_AL, {"label": "Battle of Bautzen (1813) (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Bautzen_(1813)"}],
    [BZ_SOUHAM, BZ_DELMAS, BZ_MAISON, BZ_PUTHOD, BZ_CHAPLITZ, BZ_SHCHERBATOV, BZ_INSOV],
    [to_come("Kleist's Corps", "Prussian advance guard, with Russian Jäger",
             "Kleist's Prussians, the Colberg Regiment and Silesian hussars, with Russian Jäger and Cossacks, which retook Preititz from Ney before withdrawing."),
     to_come("Blücher's Corps", "Zieten's, Klüx's and Röder's brigades",
             "Blücher's Silesian and Brandenburg brigades on the Kreckwitz heights, nearly cut off when Ney reached Preititz."),
     to_come("Yorck's Corps", "Zielinsky's and Horn's brigades",
             "Sent from the centre to help Blücher hold the heights against Bertrand and Marmont.")])


# ================================================================ Großbeeren, 23 August 1813

GB = {"label": "Order of Battle for Gross-Beeren, 23 August 1813 (Nafziger Collection 813HGE)", "url": NAF + "813HGE.pdf"}
GB_NOTE = "After Nafziger's order of battle for Großbeeren."
LIST_SAX = ("Built from A Clash of Eagles' Saxon 1812 list, the nearest to 1813: the Saxon army that fought in 1813 "
            "was rebuilt from the survivors of Russia on the same lines.")

GB_SAHR = force(
    "grossbeeren-sahr", SAX, "Sahr's Division", "25th (Saxon) Division, VII Corps (Reynier)", "Saxon",
    "Reynier's leading division, which reached Großbeeren in the rain about four in the afternoon, drove out the Prussian battalion holding it, and occupied the village. At six Bülow's whole corps came on behind sixty guns; the Saxons fought in the burning village with the bayonet and the musket butt until they were driven out.",
    [bde("sax-infantry-brigade", "Bose's Brigade", "Oberst von Bose",
         units=[u("sax-grenadier", "Grenadier Battalion 'Sperl'"), u("sax-foot-arty", "3rd Foot Battery 'Kühnel'")],
         regiments=[regt("2nd Light 'von Sahr'", bns("sax-light-infantry", "2nd Light", 2)),
                    regt("König Regiment", [u("sax-musketeer", "II/König")]),
                    regt("Niesemeuschel Regiment", [u("sax-musketeer", "I/Niesemeuschel")])]),
     bde("sax-infantry-brigade", "Ryssel's Brigade", "Oberst von Ryssel",
         units=[u("sax-foot-arty", "4th Foot Battery 'Rouvroy II'")],
         regiments=[regt("Prinz Anton Regiment", bns("sax-musketeer", "Prinz Anton", 2)),
                    regt("von Löw Regiment", bns("sax-musketeer", "von Löw", 2))])],
    command=[cmd("sax-div-cmd", "Gen-Lt von Sahr")],
    notes=[LIST_SAX, GB_NOTE,
           "Each brigade's foot battery, with fewer than the six battalions the list wants for it, shows as a historical departure."])

GB_LECOQ = force(
    "grossbeeren-lecoq", SAX, "Le Coq's Division", "24th (Saxon) Division, VII Corps (Reynier)", "Saxon",
    "Reynier's second division, which came up behind Sahr's and stood on the left of the village. When the Prussian attack broke the first line, six of its battalions went forward to hold the left, and were carried back with the rest in the dark.",
    [bde("sax-infantry-brigade", "Brause's Brigade", "Oberst von Brause",
         units=[u("sax-grenadier", "I/Guard Grenadiers"), u("sax-foot-arty", "1st Foot Battery 'Dietrich'")],
         regiments=[regt("1st Light 'Le Coq'", bns("sax-light-infantry", "1st Light", 2)),
                    regt("Maximilian Regiment", [u("sax-musketeer", "I/Maximilian")]),
                    regt("von Rechten Regiment", [u("sax-musketeer", "II/von Rechten")])]),
     bde("sax-infantry-brigade", "Mellentin's Brigade", "Oberst von Mellentin",
         units=[u("sax-grenadier", "Grenadier Battalion 'Spiegel'"), u("sax-foot-arty", "2nd Foot Battery 'Zandt'")],
         regiments=[regt("Prinz Friedrich August Regiment", bns("sax-musketeer", "Prinz Friedrich August", 2)),
                    regt("von Steindel Regiment", bns("sax-musketeer", "von Steindel", 2))])],
    command=[{"unit": "sax-cmd-lecoq"}],
    notes=[LIST_SAX, GB_NOTE, "Le Coq is the book's named commander.",
           "The battalion of the Guard Grenadiers is shown as Grenadiers.",
           "Each brigade's foot battery, with fewer than the six battalions the list wants for it, shows as a historical departure."])

GB_GABLENZ = force(
    "grossbeeren-gablenz", SAX, "Gablenz's Light Cavalry", "26th Light Cavalry Brigade, VII Corps (Reynier)", "Saxon",
    "Reynier's corps cavalry, which covered the retreat from Großbeeren in the dark after the infantry broke.",
    [bde("sax-cavalry-brigade", "Gablenz's Brigade", "Oberst von Lindenau",
         [u("sax-hussar", "Saxon Hussars", options=["large-cavalry"]), u("sax-uhlan", "Prinz Clemens Uhlans"),
          u("sax-horse-arty", "1st Horse Battery 'Birnbaum'")])],
    command=[cmd("sax-div-cmd", "Gen-Maj von Gablenz")],
    notes=[LIST_SAX, GB_NOTE,
           "The Hussars had eight squadrons, so they are Large; the Uhlans had five.",
           "The brigade was led by Oberst von Lindenau for Gablenz, who commanded the corps cavalry.",
           "Cavalry without infantry shows as a historical departure."])

GB_DURUTTE = force(
    "grossbeeren-durutte", FR, "Durutte's Division", "32nd Division, VII Corps (Reynier)", "French",
    "The French division of Reynier's corps, in reserve behind the Saxons. It was caught up in their rout as the Prussians took the village, and fell back with them on Wittenberg.",
    [bde("fr-infantry-brigade", "Jarry's Brigade", "Gén. de Brigade Jarry",
         regiments=[regt("36th Léger", [u("fr-light-infantry", "I/36th Léger"), u("fr-light-infantry", "IV/36th Léger")]),
                    regt("131st Line", [u("fr-line-infantry", f"{b}/131st Line") for b in ("I", "III", "IV")])]),
     bde("fr-infantry-brigade", "Second Brigade", "",
         regiments=[regt("133rd Line", [u("fr-line-infantry", "III/133rd Line"), u("fr-line-infantry", "IV/133rd Line")]),
                    regt("Würzburg Regiment", [u("fr-rheinbund-infantry", "II/Würzburg"), u("fr-rheinbund-infantry", "III/Würzburg")])])],
    command=[cmd("fr-div-cmd", "Gén. de Division Durutte")],
    notes=[LIST_FR, GB_NOTE, CONSCRIPTS,
           "The Würzburg battalions are Rheinbund infantry, as the list takes German contingents in French divisions; two of them, where the list allows one, show as a historical departure.",
           "Nafziger lists no artillery with the division."])

GROSSBEEREN = battle(
    "grossbeeren", "Großbeeren", "23 August 1813",
    "The armistice over, Napoleon sent Oudinot with three corps to take Berlin. They marched by separate roads through the wooded country south of the city, out of touch with each other, and on the afternoon of the 23rd, in pouring rain, Reynier's Saxon corps took the village of Großbeeren on its own. At six Bülow's Prussian corps, attacking against Bernadotte's wishes, came on behind sixty guns and stormed the village with the bayonet and musket butt; Reynier's corps broke, and Oudinot fell back on Wittenberg.",
    [GB, {"label": "Battle of Großbeeren (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Gro%C3%9Fbeeren"},
     {"label": "Schlacht bei Großbeeren (German Wikipedia)", "url": "https://de.wikipedia.org/wiki/Schlacht_bei_Gro%C3%9Fbeeren"}],
    [GB_SAHR, GB_LECOQ, GB_GABLENZ, GB_DURUTTE],
    [to_come("Bülow's Corps", "III Corps: Hesse-Homburg's, Thümen's, Borstell's and Krafft's brigades, with Oppen's cavalry",
             "Four brigades of line, reserve and Landwehr infantry, each with its cavalry and battery, which stormed Großbeeren at six in the evening behind sixty-four guns, two of their batteries Russian 12-pdrs; the 4th Reserve Regiment fought in the village with musket butts. Borstell's brigade came in on the Saxons' flank from Kleinbeeren, and Oppen's dragoons, hussars and Landwehr cavalry rode down the rearguard in the dark.")],
    alliances=(("Saxon", "French"),))


# What fought with each force but isn't in it, shown at the foot of its brigades in the builder
MISSING = [
    (LZ_MARCHAND, [{"name": "Laboissière's and Jett's cavalry",
                   "reason": "The 10th Hussars, Baden Dragoons, Hessian Chevau-légers and Württemberg light horse Nafziger lists with the division were Ney's corps cavalry, and the Confederation list has no French hussars."}]),
    (GB_LECOQ, [{"name": "1st Jäger Company",
                "reason": "A single company of Saxon Jäger with Brause's brigade, too small for a unit of its own; the Saxon list has no Jäger."}]),
    (GB_GABLENZ, [{"name": "2nd Horse Battery 'Probsthayn'",
                  "reason": "The list allows one horse battery with a cavalry brigade, and the brigade's two regiments are its only ones."}]),
    (GB_DURUTTE, [{"name": "Detachments of the 3/36th Léger and 3/133rd Line",
                  "reason": "Parts of battalions, too small for units of their own."}]),
]
for f, items in MISSING:
    if items:
        f["missing"] = items


if __name__ == "__main__":
    for b in (MOCKERN, LUTZEN, BAUTZEN, GROSSBEEREN):
        write(b)
