"""
Writes the Hundred Days battles' historical forces (src/data/battles/{ligny,quatre-bras,waterloo,wavre}.json)
from the compact tables below, so each army's brigades are built the same way throughout.

    python3 scripts/forces/hundred_days.py && npm run check:forces

Orders of battle are from Wikipedia's "Waterloo campaign order of battle". Summaries are our own words.
Staff Ratings aren't in any order of battle, so ratings.py sets them as each battle is written: every
commander at 8 unless he's one of the book's named commanders.
"""

import json
from pathlib import Path

import commanders
import ratings

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
ROMAN = ["I", "II", "III", "IV"]
SOURCES = [
    {"label": "Waterloo campaign order of battle (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Waterloo_campaign_order_of_battle"},
    {"label": "Prussian Army of the Lower Rhine, June 1815 (Nafziger Collection 815FAG, after Plotho)", "url": "https://www.napoleon-series.org/nafzigger/815FAG.pdf"},
]
RATINGS = "Staff Ratings are our judgement: the division's commander at 8, brigade commanders at 7."


def u(unit, name=None, **kw):
    d = {"unit": unit}
    if name:
        d["name"] = name
    d.update(kw)
    return d


def cmd(unit, name=None):
    """An army or division commander; his Staff Rating is set by ratings.py"""
    d = {"unit": unit}
    if name:
        d["name"] = name
    return d


def bde(type_, name, commander=None, units=(), regiments=()):
    """A brigade; its commander's Staff Rating is set by ratings.py"""
    b = {"type": type_, "name": name}
    if commander:
        b["commander"] = {"name": commander}
    if units:
        b["units"] = list(units)
    if regiments:
        b["regiments"] = list(regiments)
    return b


def force(id_, nation, name, formation, side, summary, brigades, command=(), notes=()):
    f = {"id": id_, "nationId": nation, "name": name}
    if formation:
        f["formation"] = formation
    f["side"] = side
    f["summary"] = summary
    if notes:
        f["notes"] = list(notes)
    if command:
        f["command"] = list(command)
    f["brigades"] = brigades
    return f


# ---------------------------------------------------------------- French (The Army of the North 1815)

FR = "french-army-corps"


def fr_bns(reg, n, light=False):
    """A French regiment's battalions: "I/54e de Ligne", or Léger with the Light infantry upgrade"""
    label = f"{reg} Léger" if light else f"{reg} de Ligne"
    return [u("fac-line", f"{ROMAN[i]}/{label}", **({"options": ["light-infantry"]} if light else {})) for i in range(n)]


def fr_inf(name, commander, regs):
    units = []
    for reg in regs:
        units += fr_bns(*reg)
    return bde("fac-infantry-brigade", name, commander, units)


def fr_battery(name):
    return bde("fac-divisional-artillery", "Divisional Artillery", units=[u("fac-foot-arty", name)])


def fr_div(id_, name, formation, commander, brigades, battery, summary, notes=()):
    return force(
        id_, FR, name, formation, "French", summary,
        [fr_inf(*b) for b in brigades] + [fr_battery(battery)],
        command=[cmd("fac-div-cmd", commander)],
        notes=list(notes) + [RATINGS],
    )


def fr_cav(type_, name, commander, regiments):
    unit = {"Cuirassiers": "fac-cuirassier", "Carabiniers": "fac-carabinier", "Dragons": "fac-dragoon",
            "Hussards": "fac-hussar", "Chasseurs": "fac-chasseur-a-cheval", "Lanciers": "fac-chevau-legers-lancers"}
    return bde(type_, name, commander, [u(unit[kind], f"{num} {kind}") for num, kind in regiments])


def fr_horse(name):
    return bde("fac-divisional-artillery", "Horse Artillery", units=[u("fac-horse-arty-attached", name)])


CAV_ALONE = (
    "A cavalry division on its own has no Infantry Brigade, which the list needs; its cavalry brigades are allowed "
    "by infantry brigades, and reserve cavalry can be at most half an army. So these show as historical "
    "departures. Play it alongside an infantry division, or agree it with your opponent."
)

# Divisions, as tables: (id suffix, name, formation, commander, brigades, battery)
QUIOT = ("quiot", "Quiot's Division", "1st Division, I Corps (d'Erlon)", "Gén. de Brigade Quiot",
         [("Charlet's Brigade", "Col. Charlet", [("54e", 2), ("55e", 2)]),
          ("Bourgeois' Brigade", "Gén. de Brigade Bourgeois", [("28e", 2), ("105e", 2)])],
         "20/6e à Pied (Hamelin)")
DURUTTE = ("durutte", "Durutte's Division", "4th Division, I Corps (d'Erlon)", "Gén. de Division Durutte",
           [("Pégot's Brigade", "Gén. de Brigade Pégot", [("8e", 2), ("29e", 2)]),
            ("Brue's Brigade", "Gén. de Brigade Brue", [("85e", 2), ("95e", 2)])],
           "9/6e à Pied (Bourgeois)")
BACHELU = ("bachelu", "Bachelu's Division", "5th Division, II Corps (Reille)", "Gén. de Division Bachelu",
           [("Husson's Brigade", "Gén. de Brigade Husson", [("2e", 2, True), ("61e", 2)]),
            ("Campi's Brigade", "Gén. de Brigade Campi", [("72e", 2), ("108e", 3)])],
           "18/6e à Pied (Deshaulles)")
JEROME = ("jerome", "Prince Jérôme's Division", "6th Division, II Corps (Reille)", "Prince Jérôme Bonaparte",
          [("Bauduin's Brigade", "Gén. de Brigade Bauduin", [("1er", 3, True), ("3e", 4)]),
           ("Soye's Brigade", "Gén. de Brigade Soye", [("1er", 3), ("2e", 3)])],
          "2/2e à Pied (Meunier)")
GIRARD = ("girard", "Girard's Division", "7th Division, II Corps (Reille)", "Gén. de Division Girard",
          [("Villiers' Brigade", "Gén. de Brigade de Villiers", [("11e", 2, True), ("82e", 1)]),
           ("Piat's Brigade", "Gén. de Brigade Piat", [("12e", 3, True), ("4e", 2)])],
          "3/2e à Pied (Barbaux)")
FOY = ("foy", "Foy's Division", "9th Division, II Corps (Reille)", "Gén. de Division Foy",
       [("Gauthier's Brigade", "Gén. de Brigade Gauthier", [("92e", 2), ("93e", 2)]),
        ("Jamin's Brigade", "Gén. de Brigade Jamin", [("4e", 3, True), ("100e", 3)])],
       "1/6e à Pied (Tacon)")
LEFOL = ("lefol", "Lefol's Division", "8th Division, III Corps (Vandamme)", "Gén. de Division Lefol",
         [("Billiard's Brigade", "Gén. de Brigade Billiard", [("15e", 3, True), ("23e", 3)]),
          ("Corsin's Brigade", "Gén. de Brigade Corsin", [("37e", 3), ("64e", 2)])],
         "7/6e à Pied (Chauveau)")
HABERT = ("habert", "Habert's Division", "10th Division, III Corps (Vandamme)", "Gén. de Division Habert",
          [("Gengoult's Brigade", "Gén. de Brigade Gengoult", [("34e", 3), ("88e", 3)]),
           ("Dupeyroux's Brigade", "Gén. de Brigade Dupeyroux", [("22e", 3), ("70e", 2)])],
          "18/2e à Pied (Guerin)")
BERTHEZENE = ("berthezene", "Berthezène's Division", "11th Division, III Corps (Vandamme)", "Gén. de Division Berthezène",
              [("Dufour's Brigade", "Gén. de Brigade Dufour", [("12e", 2), ("56e", 2)]),
               ("Lagarde's Brigade", "Gén. de Brigade Lagarde", [("33e", 2), ("86e", 2)])],
              "17/2e à Pied (Guerin)")
PECHEUX = ("pecheux", "Pécheux's Division", "12th Division, IV Corps (Gérard)", "Gén. de Division Pécheux",
           [("Rome's Brigade", "Gén. de Brigade Rome", [("30e", 3), ("96e", 3)]),
            ("Schoeffer's Brigade", "Gén. de Brigade Schoeffer", [("6e", 2, True), ("63e", 3)])],
           "2/5e à Pied (Fenouillat)")
VICHERY = ("vichery", "Vichery's Division", "13th Division, IV Corps (Gérard)", "Gén. de Division Vichery",
           [("Le Capitaine's Brigade", "Gén. de Brigade le Capitaine", [("59e", 2), ("76e", 2)]),
            ("Desprez's Brigade", "Gén. de Brigade Desprez", [("48e", 2), ("69e", 2)])],
           "1/5e à Pied (Saint-Cyr)")
HULOT = ("hulot", "Hulot's Division", "14th Division, IV Corps (Gérard)", "Gén. de Brigade Hulot",
         [("Hulot's Brigade", "Col. Baume", [("9e", 2, True), ("111e", 3)]),
          ("Toussaint's Brigade", "Gén. de Brigade Toussaint", [("44e", 2), ("50e", 2)])],
         "Divisional Foot Battery")
SIMMER = ("simmer", "Simmer's Division", "19th Division, VI Corps (Lobau)", "Gén. de Division Simmer",
          [("Bellair's Brigade", "Gén. de Brigade Julienne de Bellair", [("5e", 2), ("11e", 3)]),
           ("Thévenet's Brigade", "Gén. de Brigade Thévenet", [("27e", 2), ("84e", 2)])],
          "1/8e à Pied (Parisot)")
JEANIN = ("jeanin", "Jeanin's Division", "20th Division, VI Corps (Lobau)", "Gén. de Division Jeanin",
          [("Bony's Brigade", "Gén. de Brigade Bony", [("5e", 2, True), ("10e", 2)]),
           ("Tromelin's Brigade", "Gén. de Brigade de Tromelin", [("107e", 2)])],
          "2/8e à Pied (Paquet)")
TESTE = ("teste", "Teste's Division", "21st Division, VI Corps (detached to Grouchy)", "Gén. de Division Teste",
         [("Lafitte's Brigade", "Gén. de Brigade Lafitte", [("8e", 2, True)]),
          ("Penne's Brigade", "Gén. de Brigade Penne", [("65e", 1), ("75e", 2)])],
         "3/8e à Pied (Duverrey)")

LIGHT_NOTE = {
    "girard": "Girard's division had five Light battalions (11e and 12e Léger) of eight, where the list allows one in four, so the extra Light battalions show as historical departures.",
    "foy": "The 4e Léger brought three battalions, one more Light battalion than the list's one in four allows, which shows as a historical departure.",
    "lefol": "The 15e Léger brought three battalions, one more Light battalion than the list's one in four allows, which shows as a historical departure.",
    "jeanin": "Tromelin's brigade had only the 107e's two battalions, fewer than the list's three for a brigade, and the 5e Léger's two battalions are one more Light battalion than one in four allows; both show as historical departures.",
    "teste": "Teste's brigades were small: Lafitte had only the 8e Léger's two battalions, fewer than the list's three, and those are more Light battalions than one in four allows; both show as historical departures.",
}
EXTRA_NOTE = {
    "habert": "The 2e Régiment Étranger (Swiss) also served in Dupeyroux's brigade; the order of battle gives no battalion count, so it's left out.",
    "hulot": "Bourmont commanded the division until he deserted to the allies on 15 June; Hulot led it from then. The order of battle gives the division no battery of its own; one foot battery is shown.",
    "jerome": "Prince Jérôme commanded, though Guilleminot, his chief of staff, did much of the work.",
}


def fr(table, battle, summary):
    id_, name, formation, commander, brigades, battery = table
    notes = [n for n in (LIGHT_NOTE.get(id_), EXTRA_NOTE.get(id_)) if n]
    return fr_div(f"{battle}-{id_}", name, formation, commander, brigades, battery, summary, notes)


def wathier(battle, summary):
    return force(f"{battle}-wathier", FR, "Wathier's Cuirassiers", "13th Cavalry Division, IV Cavalry Corps (Milhaud)", "French", summary,
                 [fr_cav("fac-heavy-cavalry-brigade", "Dubois' Brigade", "Gén. de Brigade Dubois", [("1er", "Cuirassiers"), ("4e", "Cuirassiers")]),
                  fr_cav("fac-heavy-cavalry-brigade", "Travers' Brigade", "Gén. de Brigade Travers", [("7e", "Cuirassiers"), ("12e", "Cuirassiers")]),
                  fr_horse("5/1er à Cheval (Duchet)")],
                 command=[cmd("fac-div-cmd", "Gén. de Division Wathier")], notes=[CAV_ALONE, RATINGS])


def delort(battle, summary):
    return force(f"{battle}-delort", FR, "Delort's Cuirassiers", "14th Cavalry Division, IV Cavalry Corps (Milhaud)", "French", summary,
                 [fr_cav("fac-heavy-cavalry-brigade", "Farine's Brigade", "Gén. de Brigade Farine", [("5e", "Cuirassiers"), ("10e", "Cuirassiers")]),
                  fr_cav("fac-heavy-cavalry-brigade", "Vial's Brigade", "Gén. de Brigade Vial", [("6e", "Cuirassiers"), ("9e", "Cuirassiers")]),
                  fr_horse("4/3e à Cheval (Legay)")],
                 command=[cmd("fac-div-cmd", "Gén. de Division Delort")], notes=[CAV_ALONE, RATINGS])


def lheritier(battle, summary):
    return force(f"{battle}-lheritier", FR, "L'Héritier's Division", "11th Cavalry Division, III Cavalry Corps (Kellermann)", "French", summary,
                 [fr_cav("fac-cavalry-brigade", "Picquet's Brigade", "Gén. de Brigade Picquet", [("2e", "Dragons"), ("7e", "Dragons")]),
                  fr_cav("fac-heavy-cavalry-brigade", "Guiton's Brigade", "Gén. de Brigade Guiton", [("8e", "Cuirassiers"), ("11e", "Cuirassiers")]),
                  fr_horse("3/2e à Cheval (de Marcillac)")],
                 command=[cmd("fac-div-cmd", "Gén. de Division L'Héritier")], notes=[CAV_ALONE, RATINGS])


def roussel(battle, summary):
    return force(f"{battle}-roussel", FR, "Roussel d'Hurbal's Division", "12th Cavalry Division, III Cavalry Corps (Kellermann)", "French", summary,
                 [fr_cav("fac-heavy-cavalry-brigade", "Blanchard's Brigade", "Gén. de Brigade Blanchard", [("1er", "Carabiniers"), ("2e", "Carabiniers")]),
                  fr_cav("fac-heavy-cavalry-brigade", "Donop's Brigade", "Gén. de Brigade Donop", [("2e", "Cuirassiers"), ("3e", "Cuirassiers")]),
                  fr_horse("2/2e à Cheval (Lebau)")],
                 command=[cmd("fac-div-cmd", "Gén. de Division Roussel d'Hurbal")], notes=[CAV_ALONE, RATINGS])


def jacquinot(battle, summary):
    return force(f"{battle}-jacquinot", FR, "Jacquinot's Light Cavalry", "1st Cavalry Division, I Corps (d'Erlon)", "French", summary,
                 [fr_cav("fac-cavalry-brigade", "Bruno's Brigade", "Gén. de Brigade Bruno", [("7e", "Hussards"), ("3e", "Chasseurs")]),
                  fr_cav("fac-cavalry-brigade", "Gobrecht's Brigade", "Gén. de Brigade Gobrecht", [("3e", "Lanciers"), ("4e", "Lanciers")]),
                  fr_horse("2/1er à Cheval (Bourgeois)")],
                 command=[cmd("fac-div-cmd", "Gén. de Division Jacquinot")], notes=[CAV_ALONE, RATINGS])


def pire(battle, summary):
    return force(f"{battle}-pire", FR, "Piré's Light Cavalry", "2nd Cavalry Division, II Corps (Reille)", "French", summary,
                 [fr_cav("fac-cavalry-brigade", "Huber's Brigade", "Gén. de Brigade Huber", [("1er", "Chasseurs"), ("6e", "Chasseurs")]),
                  fr_cav("fac-cavalry-brigade", "Wathiez's Brigade", "Gén. de Brigade Wathiez", [("5e", "Lanciers"), ("6e", "Lanciers")]),
                  fr_horse("2/4e à Cheval (Gronnier)")],
                 command=[cmd("fac-div-cmd", "Gén. de Division Piré")], notes=[CAV_ALONE, RATINGS])


def guiton(battle, summary):
    return force(f"{battle}-guiton", FR, "Kellermann's Cuirassiers", "Guiton's Brigade, 11th Cavalry Division", "French", summary,
                 [fr_cav("fac-heavy-cavalry-brigade", "Guiton's Brigade", "Gén. de Brigade Guiton", [("8e", "Cuirassiers"), ("11e", "Cuirassiers")]),
                  fr_horse("3/2e à Cheval (de Marcillac)")],
                 command=[cmd("fac-div-cmd", "Gén. de Division Kellermann")],
                 notes=["Only Guiton's brigade of Kellermann's corps reached the field, and Kellermann led its charge himself.", CAV_ALONE])


def strolz(battle, summary):
    return force(f"{battle}-strolz", FR, "Strolz's Dragoons", "9th Cavalry Division, II Cavalry Corps (Exelmans)", "French", summary,
                 [fr_cav("fac-cavalry-brigade", "Burthe's Brigade", "Gén. de Brigade Burthe", [("5e", "Dragons"), ("13e", "Dragons")]),
                  fr_cav("fac-cavalry-brigade", "Vincent's Brigade", "Gén. de Brigade Vincent", [("15e", "Dragons"), ("20e", "Dragons")]),
                  fr_horse("4/1er à Cheval (Godet)")],
                 command=[cmd("fac-div-cmd", "Gén. de Division Strolz")], notes=[CAV_ALONE, RATINGS])


# ---------------------------------------------------------------- Imperial Guard (1815)

FG = "french-imperial-guard-1815"
GUARD_RATINGS = "Staff Ratings are our judgement: the Guard's division commanders at 8, brigade commanders at 7."


def guard_bns(unit, reg, n):
    return [u(unit, f"{ROMAN[i]}/{reg}") for i in range(n)]


def old_guard(battle, summary, notes=()):
    return force(f"{battle}-old-guard", FG, "The Old Guard", "1st and 2nd Grenadiers and Chasseurs à Pied", "French", summary,
                 [bde("fig15-old-guard-brigade", "Grenadiers à Pied", "Gén. Petit",
                      guard_bns("fig15-old-guard-grenadiers", "1er Grenadiers", 2) + guard_bns("fig15-old-guard-grenadiers", "2e Grenadiers", 2)),
                  bde("fig15-old-guard-brigade", "Chasseurs à Pied", "Gén. Cambronne",
                      guard_bns("fig15-old-guard-chasseurs", "1er Chasseurs", 2) + guard_bns("fig15-old-guard-chasseurs", "2e Chasseurs", 2)),
                  bde("fig15-guards-artillery", "Guard Foot Artillery", units=[u("fig15-foot-marine-arty", "Old Guard Foot Battery")])],
                 command=[cmd("fig15-div-cmd", "Gén. de Division Morand")], notes=list(notes) + [GUARD_RATINGS])


def middle_guard(battle, summary, notes=()):
    return force(f"{battle}-middle-guard", FG, "The Middle Guard", "3rd and 4th Grenadiers and Chasseurs à Pied", "French", summary,
                 [bde("fig15-middle-guard-brigade", "Grenadiers à Pied", "Gén. Poret de Morvan",
                      guard_bns("fig15-middle-guard-grenadiers", "3e Grenadiers", 2) + guard_bns("fig15-middle-guard-grenadiers", "4e Grenadiers", 1)),
                  bde("fig15-middle-guard-brigade", "Chasseurs à Pied", "Gén. Michel",
                      guard_bns("fig15-middle-guard-chasseurs", "3e Chasseurs", 2) + guard_bns("fig15-middle-guard-chasseurs", "4e Chasseurs", 2)),
                  bde("fig15-guards-artillery", "Guard Foot Artillery", units=[u("fig15-foot-marine-arty", "Guard Foot Battery")])],
                 command=[cmd("fig15-div-cmd", "Gén. de Division Friant")], notes=list(notes) + [GUARD_RATINGS])


def young_guard(battle, summary):
    return force(f"{battle}-young-guard", FG, "The Young Guard", "Duhesme's Division", "French", summary,
                 [bde("fig15-young-guard-brigade", "Chartrand's Brigade", "Gén. Chartrand",
                      guard_bns("fig15-yg-tirailleurs", "1er Tirailleurs", 2) + guard_bns("fig15-yg-voltigeurs", "1er Voltigeurs", 2)),
                  bde("fig15-young-guard-brigade", "Guye's Brigade", "Gén. Guye",
                      guard_bns("fig15-yg-tirailleurs", "3e Tirailleurs", 2) + guard_bns("fig15-yg-voltigeurs", "3e Voltigeurs", 2)),
                  bde("fig15-guards-artillery", "Guard Artillery", units=[u("fig15-foot-marine-arty", "Guard Foot Battery")])],
                 command=[cmd("fig15-div-cmd", "Gén. de Division Duhesme")], notes=[GUARD_RATINGS])


def guard_cavalry(battle, summary):
    return force(f"{battle}-guard-cavalry", FG, "The Guard Cavalry", "Guyot's heavy and Lefebvre-Desnouettes' light divisions", "French", summary,
                 [bde("fig15-heavy-cavalry-brigade", "Guyot's Heavy Cavalry", "Gén. Guyot",
                      [u("fig15-grenadier-guards-a-cheval", "Grenadiers à Cheval"), u("fig15-empress-dragoons", "Dragons de l'Impératrice"),
                       u("fig15-gendarmes-tiny", "Gendarmes d'Élite")]),
                  bde("fig15-light-cavalry-brigade", "Lefebvre-Desnouettes' Light Cavalry", "Gén. Lallemand",
                      [u("fig15-chasseurs-a-cheval", "Chasseurs à Cheval", options=["large"]), u("fig15-guard-lancer", "1er Lanciers (Polish)"),
                       u("fig15-guard-lancer", "2e Lanciers (Red Lancers)")]),
                  bde("fig15-guards-artillery", "Guard Horse Artillery", units=[u("fig15-horse-arty", "Guard Horse Battery")])],
                 command=[cmd("fig15-div-cmd", "Gén. de Division Lefebvre-Desnouettes")],
                 notes=["The Guard cavalry rode without the three Guard infantry brigades the list asks for first, and the light division had two Lancer regiments where the list allows one; these show as historical departures.",
                        "The Chasseurs à Cheval, over 1,200 strong, are Large.", GUARD_RATINGS])


# ---------------------------------------------------------------- Anglo-allied: British, KGL and Hanoverians

AN = "anglo-netherlands-british"
LINE = "anb-line"


def br(name, **kw):
    return u(LINE, name, **kw)


def picton(battle, summary, hanoverians, notes=()):
    han_name, han_cmd, han_bns = hanoverians
    return force(f"{battle}-picton", AN, "Picton's Division", "5th Division, Reserve", "Anglo-allied", summary,
                 [bde("anb-british-infantry-brigade", "Kempt's Brigade (8th British)", "Maj-Gen Sir James Kempt",
                      [br("1/28th (North Gloucestershire)"), br("1/32nd (Cornwall)"), br("1/79th (Cameron Highlanders)", options=["highlanders"]),
                       br("1/95th Rifles", options=["rifles"])]),
                  bde("anb-british-infantry-brigade", "Pack's Brigade (9th British)", "Maj-Gen Sir Denis Pack",
                      [br("3/1st (Royal Scots)"), br("1/42nd (Royal Highland)", options=["highlanders"]), br("2/44th (East Essex)"),
                       br("1/92nd (Gordon Highlanders)", options=["highlanders"])]),
                  bde("anb-hanoverian-brigade", han_name, han_cmd, [u("anb-hanover-landwehr", f"Landwehr Bn {b}") for b in han_bns]),
                  bde("anb-divisional-artillery", "Rogers' Battery RA", units=[u("anb-royal-arty", "Rogers' Battery RA")]),
                  bde("anb-divisional-artillery", "Braun's Hanoverian Battery", units=[u("anb-hanover-foot-arty", "Braun's Foot Battery")])],
                 command=[cmd("anb-div-cmd", "Lt-Gen Sir Thomas Picton")],
                 notes=["Pack's brigade had two Highland battalions, the 42nd and 92nd, where the list allows one Highland battalion in four, so it shows as a historical departure.",
                        "The 1/95th is the list's Rifle Battalion, taken as the Rifles upgrade on a Line battalion.",
                        *notes,
                        "Staff Ratings are our judgement: Picton, Kempt and Pack at 8, the Hanoverian brigade's commander at 7. The named Kempt and Pack from the book can be added under Army command instead."])


def alten(battle, summary, notes=()):
    return force(f"{battle}-alten", AN, "Alten's Division", "3rd Division, I Corps (Prince of Orange)", "Anglo-allied", summary,
                 [bde("anb-british-infantry-brigade", "Halkett's Brigade (5th British)", "Maj-Gen Sir Colin Halkett",
                      [br("2/30th (Cambridgeshire)"), br("33rd (1st Yorkshire West Riding)"), br("2/69th (South Lincolnshire)"), br("2/73rd")]),
                  bde("anb-kgl-infantry-brigade", "Ompteda's Brigade (2nd KGL)", "Col Christian von Ompteda",
                      [u("anb-kgl-line", "1st Light Bn KGL", options=["kgl-light-infantry"]),
                       u("anb-kgl-line", "2nd Light Bn KGL (Baring)", options=["kgl-light-infantry"]),
                       u("anb-kgl-line", "5th Line Bn KGL"), u("anb-kgl-line", "8th Line Bn KGL")]),
                  bde("anb-hanoverian-brigade", "Kielmansegge's Brigade (1st Hanoverian)", "Maj-Gen Friedrich von Kielmansegge",
                      [u("anb-hanover-line", "Field Bn Bremen"), u("anb-hanover-line", "Field Bn Verden"),
                       u("anb-hanover-line", "Field Bn Duke of York (Osnabrück)"), u("anb-hanover-light", "Light Bn Lüneburg"),
                       u("anb-hanover-light", "Light Bn Grubenhagen"), u("anb-hanover-jager", "Feldjäger (two companies)")]),
                  bde("anb-divisional-artillery", "Lloyd's Battery RA", units=[u("anb-royal-arty", "Lloyd's Battery RA")]),
                  bde("anb-divisional-artillery", "Cleeves' Battery KGL", units=[u("anb-royal-arty", "Cleeves' Foot Battery KGL")])],
                 command=[{"unit": "anb-cmd-alten"}],
                 notes=["Ompteda's brigade had two KGL Light battalions, where the list allows one in four, so it shows as a historical departure.",
                        *notes,
                        "Alten is the book's named commander. Brigade Staff Ratings are our judgement, all at 7.",
                        "Kielmansegge's Feldjäger (two companies) are the list's Jäger Companies."])


def cooke(battle, summary, notes=()):
    return force(f"{battle}-cooke", AN, "Cooke's Guards Division", "1st Division, I Corps (Prince of Orange)", "Anglo-allied", summary,
                 [bde("anb-guards-brigade", "Maitland's Brigade (1st Guards)", "Maj-Gen Peregrine Maitland",
                      [u("anb-foot-guard", "2/1st Foot Guards"), u("anb-foot-guard", "3/1st Foot Guards")]),
                  bde("anb-guards-brigade", "Byng's Brigade (2nd Guards)", "Maj-Gen Sir John Byng",
                      [u("anb-foot-guard", "2/Coldstream Guards"), u("anb-foot-guard", "2/3rd Foot Guards")]),
                  bde("anb-divisional-artillery", "Sandham's Battery RA", units=[u("anb-royal-arty", "Sandham's Battery RA")]),
                  bde("anb-horse-artillery", "Kuhlmann's Battery KGL", units=[u("anb-royal-horse-arty", "Kuhlmann's Horse Battery KGL")])],
                 command=[cmd("anb-div-cmd", "Maj-Gen George Cooke")],
                 notes=["The division was two Guards brigades, with none of the British and Hanoverian brigades the list needs. The list allows one Guards Brigade, taken once two British or KGL brigades are, so these show as historical departures.",
                        "Support brigades like these can be at most half an army, and the list allows horse artillery by the cavalry taken, so Kuhlmann's KGL horse battery shows as a departure too.",
                        *notes, "Staff Ratings are our judgement, all at 7."])


def clinton(battle, summary):
    return force(f"{battle}-clinton", AN, "Clinton's Division", "2nd Division, II Corps (Hill)", "Anglo-allied", summary,
                 [bde("anb-british-infantry-brigade", "Adam's Brigade (3rd British)", "Maj-Gen Frederick Adam",
                      [br("1/52nd (Oxfordshire)", options=["large"]), br("1/71st (Highland Light Infantry)", options=["highlanders"]),
                       br("2/95th Rifles", options=["rifles"]), u("anb-rifle-coy", "3/95th Rifles (two companies)")]),
                  bde("anb-kgl-infantry-brigade", "Du Plat's Brigade (1st KGL)", "Col Georg du Plat",
                      [u("anb-kgl-line", f"{n} Line Bn KGL") for n in ("1st", "2nd", "3rd", "4th")]),
                  bde("anb-hanoverian-brigade", "Halkett's Brigade (3rd Hanoverian)", "Col Hugh Halkett",
                      [u("anb-hanover-landwehr", f"Landwehr Bn {b}") for b in ("Bremervörde", "Osnabrück", "Quakenbrück", "Salzgitter")]),
                  bde("anb-divisional-artillery", "Bolton's Battery RA", units=[u("anb-royal-arty", "Bolton's Battery RA")]),
                  bde("anb-horse-artillery", "Sympher's Battery KGL", units=[u("anb-royal-horse-arty", "Sympher's Horse Battery KGL")])],
                 command=[cmd("anb-div-cmd", "Lt-Gen Sir Henry Clinton")],
                 notes=["The 1/52nd, over a thousand strong, is Large, and the 1/71st Highlanders; the 2/95th is the list's Rifle Battalion and the two companies of the 3/95th its Rifle Company.",
                        "Adam's brigade had only three battalions, too few for the list's one-in-four Highland and Large upgrades, and Sympher's KGL horse battery is more horse artillery than a division with no cavalry is allowed; these show as historical departures.",
                        "Staff Ratings are our judgement: Clinton and Adam at 8, the others at 7."])


def lambert(battle, summary):
    return force(f"{battle}-lambert", AN, "Lambert's and Best's Brigades", "6th Division, Reserve", "Anglo-allied", summary,
                 [bde("anb-british-infantry-brigade", "Lambert's Brigade (10th British)", "",
                      [br("1/4th (King's Own)"), br("1/27th (Inniskilling)"), br("2/40th (2nd Somersetshire)")]),
                  bde("anb-hanoverian-brigade", "Best's Brigade (4th Hanoverian)", "Col Charles Best",
                      [u("anb-hanover-landwehr", f"Landwehr Bn {b}") for b in ("Lüneburg", "Münden", "Osterode", "Verden")]),
                  bde("anb-divisional-artillery", "Sinclair's Battery RA", units=[u("anb-royal-arty", "Sinclair's Battery RA")])],
                 command=[cmd("anb-div-cmd", "Maj-Gen Sir John Lambert")],
                 notes=["Cole, the 6th Division's commander, wasn't there; Lambert led his brigade, with Best's Hanoverians, which the order of battle lists alongside it. The 2/81st was left in Brussels.",
                        "Sinclair's battery is the one the order of battle lists after the division. " + RATINGS])


def uxbridge_heavies(battle, summary):
    return force(f"{battle}-heavy-cavalry", AN, "The Household and Union Brigades", "1st and 2nd Cavalry Brigades (Uxbridge)", "Anglo-allied", summary,
                 [bde("anb-heavy-cavalry-brigade", "Ponsonby's Union Brigade", "Maj-Gen Sir William Ponsonby",
                      [u("anb-dragoons-dragoon-guards", "1st (Royal) Dragoons"), u("anb-dragoons-dragoon-guards", "2nd Dragoons (Scots Greys)"),
                       u("anb-dragoons-dragoon-guards", "6th (Inniskilling) Dragoons")]),
                  bde("anb-household-brigade", "Somerset's Household Brigade", "Maj-Gen Lord Edward Somerset",
                      [u("anb-household-cav", "1st Life Guards"), u("anb-household-cav", "2nd Life Guards"),
                       u("anb-household-cav", "Royal Horse Guards (Blues)"), u("anb-dragoons-dragoon-guards", "1st King's Dragoon Guards")])],
                 command=[cmd("anb-div-cmd", "Lt-Gen the Earl of Uxbridge")],
                 notes=["Two heavy brigades on their own: the list needs British and Hanoverian infantry brigades, and its heavy cavalry comes with them, and the Household Brigade had three Household regiments where it allows two, and support brigades can be at most half an army, so these show as historical departures.",
                        "Uxbridge led the charge in person, as the army's cavalry commander."])


def light_cavalry(battle, summary):
    lc = "anb-light-dragoon-hussar"
    return force(f"{battle}-vandeleur-vivian", AN, "Vandeleur's and Vivian's Light Cavalry", "4th and 6th Cavalry Brigades (Uxbridge)", "Anglo-allied", summary,
                 [bde("anb-light-cavalry-brigade", "Vandeleur's Brigade (4th)", "Maj-Gen Sir John Vandeleur",
                      [u(lc, "11th Light Dragoons"), u(lc, "12th Light Dragoons"), u(lc, "16th Light Dragoons")]),
                  bde("anb-light-cavalry-brigade", "Vivian's Brigade (6th)", "Maj-Gen Sir Hussey Vivian",
                      [u(lc, "10th Hussars"), u(lc, "18th Hussars"), u(lc, "1st Hussars KGL")]),
                  bde("anb-horse-artillery", "Gardiner's Troop RHA", units=[u("anb-royal-horse-arty", "E Troop RHA (Gardiner)")])],
                 command=[cmd("anb-div-cmd", "Lt-Gen the Earl of Uxbridge")],
                 notes=["Two light brigades on their own: the list needs British and Hanoverian infantry brigades, its light cavalry comes with them, and support brigades can be at most half an army, so these show as historical departures.",
                        "Gardiner's troop is one of the horse artillery troops attached to the cavalry. Staff Ratings are our judgement: Uxbridge 9, Vivian 8, Vandeleur 7."])


# ---------------------------------------------------------------- Netherlands, Nassau and Brunswick

DBN = "dutch-belgian-nassau"
BW = "brunswick"


def perponcher(battle, summary, notes=()):
    return force(f"{battle}-perponcher", DBN, "Perponcher's Division", "2nd Netherlands Division, I Corps (Prince of Orange)", "Anglo-allied", summary,
                 [bde("dbn-dutch-belgian-infantry-brigade", "Bijlandt's Brigade", "Gen-Maj van Bijlandt",
                      [u("dbn-jager", "27th Jäger Bn"), u("dbn-line", "7th Line Bn"), u("dbn-militia", "5th Militia Bn"),
                       u("dbn-militia", "7th Militia Bn"), u("dbn-militia", "8th Militia Bn")]),
                  bde("dbn-nassau-infantry-brigade", "Saxe-Weimar's Brigade", "Col Prince Bernhard of Saxe-Weimar",
                      [u("dbn-line", "I/2nd Nassau"), u("dbn-line", "II/2nd Nassau"), u("dbn-line", "III/2nd Nassau"),
                       u("dbn-line", "I/Orange-Nassau"), u("dbn-line", "II/Orange-Nassau"),
                       u("dbn-nassau-jager-coy", "Volunteer Jäger Company")]),
                  bde("dbn-divisional-artillery", "Divisional Artillery",
                      units=[u("dbn-belgian-foot-battery", "Stevenart's Foot Battery"), u("dbn-dutch-horse-battery", "Bijleveld's Horse Battery")])],
                 command=[cmd("dbn-div-cmd", "Lt-Gen de Perponcher")],
                 notes=[*notes,
                        "The order of battle gives Goedecke as the 2nd Brigade's commander; Saxe-Weimar led it after Goedecke was hurt before the campaign opened.",
                        "Staff Ratings are our judgement: Perponcher and Saxe-Weimar at 8, Bijlandt at 7."])


def chasse(battle, summary):
    return force(f"{battle}-chasse", DBN, "Chassé's Division", "3rd Netherlands Division, I Corps (Prince of Orange)", "Anglo-allied", summary,
                 [bde("dbn-dutch-belgian-infantry-brigade", "Detmers' Brigade", "Col Detmers",
                      [u("dbn-jager", "35th Jäger Bn"), u("dbn-line", "2nd Line Bn"), u("dbn-militia", "4th Militia Bn"),
                       u("dbn-militia", "6th Militia Bn"), u("dbn-militia", "17th Militia Bn"), u("dbn-militia", "19th Militia Bn")]),
                  bde("dbn-dutch-belgian-infantry-brigade", "d'Aubremé's Brigade", "Gen-Maj d'Aubremé",
                      [u("dbn-jager", "36th Jäger Bn"), u("dbn-line", "3rd Line Bn"), u("dbn-line", "12th Line Bn"),
                       u("dbn-line", "13th Line Bn"), u("dbn-militia", "3rd Militia Bn"), u("dbn-militia", "10th Militia Bn")]),
                  bde("dbn-divisional-artillery", "Divisional Artillery",
                      units=[u("dbn-belgian-foot-battery", "Lux's Foot Battery"), u("dbn-dutch-horse-battery", "Krahmer's Horse Battery")])],
                 command=[{"unit": "dbn-cmd-chasse"}],
                 notes=["Both brigades had six battalions where the list allows five, and Detmers had four Militia battalions where it allows three, so these show as historical departures.",
                        "Chassé is the book's named commander. Brigade Staff Ratings are our judgement, at 7."])


def kruse(battle, summary):
    return force(f"{battle}-kruse", DBN, "Kruse's Nassauers", "1st Nassau Regiment", "Anglo-allied", summary,
                 [bde("dbn-nassau-infantry-brigade", "1st Nassau Regiment", "Col von Steuben",
                      [u("dbn-line", "I/1st Nassau", options=["large"]), u("dbn-line", "II/1st Nassau", options=["large"]),
                       u("dbn-line", "III/1st Nassau", options=["large"])])],
                 command=[cmd("dbn-div-cmd", "Gen-Maj von Kruse")],
                 notes=["The Nassau contingent was one big regiment of three battalions, each nearly a thousand strong, so all three are Large.",
                        "On its own it has no Dutch/Belgian Infantry Brigade, which the list needs, so that shows as a historical departure.",
                        "Staff Ratings are our judgement, at 7."])


def brunswick(battle, summary, commander, notes=()):
    return force(f"{battle}-brunswick", BW, "The Brunswick Corps", "Reserve", "Anglo-allied", summary,
                 [bde("bw-advanced-guard", "Advance Guard (Rauschenplatt)", units=[u("bw-vanguard-battalion", "Avantgarde Bn")]),
                  bde("bw-infantry-brigade", "Light Brigade (Butlar)", "Lt-Col von Butlar",
                      [u("bw-light", "1st Light Bn"), u("bw-light", "2nd Light Bn"), u("bw-light", "3rd Light Bn"),
                       u("bw-leib-light", "Leib (Guard) Bn")]),
                  bde("bw-infantry-brigade", "Line Brigade (Specht)", "Lt-Col von Specht",
                      [u("bw-line", "1st Line Bn"), u("bw-line", "2nd Line Bn"), u("bw-line", "3rd Line Bn")]),
                  bde("bw-cavalry-brigade", "Cavalry (Cramm)", "Maj von Cramm",
                      [u("bw-hussar", "2nd Hussars"), u("bw-uhlan-squadron", "Uhlan Squadron")]),
                  bde("bw-divisional-artillery", "Artillery (Mahn)",
                      units=[u("bw-foot-battery", "Moll's Foot Battery"), u("bw-horse-battery", "Heinemann's Horse Battery")])],
                 command=[cmd("bw-div-cmd", commander)],
                 notes=[*notes, "The order of battle's Guard Battalion is the list's Leib Light Battalion. Staff Ratings are our judgement: the corps' commander at 8, the others at 7."])


# ---------------------------------------------------------------- Prussians 1815

PR = "prussians-1815"
PR_RATINGS = "Staff Ratings are our judgement: the brigade commander at 8, the list's lowest."


def pr_ir(name):
    num = name.split(" ")[0]
    return {"name": f"{name} Infantry", "units": [u("pr15-musketeer", f"I/{num} Infantry"), u("pr15-musketeer", f"II/{num} Infantry"),
                                                   u("pr15-fusilier", f"F/{num} Infantry")]}


def pr_lw(name):
    short = name.split(" (")[0]
    return {"name": f"{name} Landwehr", "units": [u("pr15-landwehr", f"{ROMAN[i]}/{short} Landwehr") for i in range(3)]}


PR_BRIGADES = {
    1: ("Steinmetz", "I Corps (Zieten)", ["12th (2nd Brandenburg)", "24th (4th Brandenburg)"], ["1st Westphalian"]),
    2: ("Pirch II", "I Corps (Zieten)", ["6th (1st West Prussian)", "28th (1st Berg)", "16th (3rd Westphalian)"], ["2nd Westphalian"]),
    3: ("Jagow", "I Corps (Zieten)", ["7th (2nd West Prussian)", "29th (2nd Berg)"], ["3rd Westphalian"]),
    4: ("Henckel von Donnersmarck", "I Corps (Zieten)", ["13th (1st Reserve)", "19th (7th Reserve)"], ["4th Westphalian"]),
    5: ("Tippelskirch", "II Corps (Pirch I)", ["2nd (1st Pomeranian)", "25th (Lützow)"], ["5th Westphalian"]),
    6: ("Krafft", "II Corps (Pirch I)", ["9th (Kolberg)", "26th (Elbe)"], ["1st Elbe"]),
    7: ("Brause", "II Corps (Pirch I)", ["14th (2nd Reserve)", "22nd (10th Reserve)"], ["2nd Elbe"]),
    8: ("Bose", "II Corps (Pirch I)", ["21st (9th Reserve)", "23rd (11th Reserve)"], ["3rd Elbe"]),
    9: ("Borcke", "III Corps (Thielemann)", ["8th (Leib)", "30th (1st Russo-German Legion)"], ["1st Kurmark"]),
    10: ("Kemphen", "III Corps (Thielemann)", ["27th"], ["2nd Kurmark"]),
    11: ("Luck", "III Corps (Thielemann)", [], ["3rd Kurmark", "4th Kurmark"]),
    12: ("Stülpnagel", "III Corps (Thielemann)", ["31st (2nd Russo-German Legion)"], ["5th Kurmark", "6th Kurmark"]),
    13: ("Hake", "IV Corps (Bülow)", ["10th (1st Silesian)"], ["2nd Neumark", "3rd Neumark"]),
    14: ("Ryssel", "IV Corps (Bülow)", ["11th (2nd Silesian)"], ["1st Pomeranian", "2nd Pomeranian"]),
    15: ("Losthin", "IV Corps (Bülow)", ["18th (6th Reserve)"], ["3rd Silesian", "4th Silesian"]),
    16: ("Hiller", "IV Corps (Bülow)", ["15th (3rd Reserve)"], ["1st Silesian", "2nd Silesian"]),
}
PR_COMMANDERS = {2: "Gen-Maj von Pirch II", 4: "Gen-Maj Graf Henckel von Donnersmarck", 10: "Col von Kemphen", 11: "Col von Luck"}
PR_NOTES = {
    2: "The order of battle gives Pirch II's brigade four regiments, the 16th Infantry among them, where the list's brigade has at most two Line regiments and three in all, so these show as historical departures.",
    11: "Luck's brigade was all Landwehr, two Kurmark regiments, where the list's brigade needs a Line regiment, which shows as a historical departure.",
}


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


PR_CORPS = {
    "I": ("Zieten's I Corps", [1, 2, 3, 4], {"unit": "pr15-cmd-zieten"}),
    "II": ("Pirch's II Corps", [5, 6, 7, 8], cmd("pr15-corps-cmd", "Gen-Maj von Pirch I")),
    "III": ("Thielemann's III Corps", [9, 10, 11, 12], cmd("pr15-corps-cmd", "Lt-Gen von Thielemann")),
    "IV": ("Bülow's IV Corps", [13, 14, 15, 16], cmd("pr15-corps-cmd", "Gen von Bülow")),
}
CORPS_RATINGS = {
    "I": "Zieten is the book's named commander. Brigade Staff Ratings are our judgement, at 8, the list's lowest.",
    "II": "Pirch I commands as the optional Corps Commander (Albion Triumphant p. 78), at Staff Rating 7; his brigade commanders at 8, the list's lowest. Our judgement.",
    "III": "Thielemann commands as the optional Corps Commander (Albion Triumphant p. 78), at Staff Rating 8; his brigade commanders at 8, the list's lowest. Our judgement.",
    "IV": "Bülow commands as the optional Corps Commander (Albion Triumphant p. 78), at Staff Rating 8; his brigade commanders at 8, the list's lowest. Our judgement.",
}


def pr_brigade(n):
    commander, _corps, irs, lws = PR_BRIGADES[n]
    return bde("pr15-infantry-brigade", f"{ordinal(n)} Brigade ({commander})", PR_COMMANDERS.get(n, f"Gen-Maj von {commander}"),
               units=[u("pr15-foot-arty", f"{ordinal(n)} Brigade Foot Battery")],
               regiments=[pr_ir(r) for r in irs] + [pr_lw(r) for r in lws])


# Each corps' cavalry, after Nafziger (815FAG, from Plotho): (brigade commander, [(unit, regiment)]), with
# Landwehr cavalry kept as brigades of their own, since the list's brigades take one or the other
D, UH, HU, LWC = "pr15-dragoon", "pr15-uhlan", "pr15-hussar", "pr15-mounted-landwehr"
PR_CAVALRY = {
    "I": ("Röder", [
        ("Treskow", [(D, "5th (Brandenburg) Dragoons"), (D, "2nd (1st West Prussian) Dragoons"), (UH, "3rd (Brandenburg) Uhlans")], True),
        ("Lützow", [(HU, "4th (1st Silesian) Hussars"), (UH, "6th (2nd West Prussian) Uhlans")], True),
        ("Lützow", [(LWC, "1st Kurmark Landwehr Cavalry"), (LWC, "2nd Kurmark Landwehr Cavalry"), (LWC, "Westphalian Landwehr Cavalry")], False),
    ], True),
    "II": ("Wahlen-Jürgass", [
        ("Thümen", [(D, "1st (Queen's) Dragoons"), (D, "6th (Neumark) Dragoons"), (UH, "2nd (Silesian) Uhlans")], True),
        ("Sohr", [(HU, "3rd (Brandenburg) Hussars"), (HU, "5th (Pomeranian) Hussars"), (HU, "11th (Berg) Hussars")], True),
        ("Schulenburg", [(LWC, "4th Kurmark Landwehr Cavalry"), (LWC, "5th Kurmark Landwehr Cavalry"), (LWC, "Elbe Landwehr Cavalry")], True),
    ], False),
    "III": ("Hobe", [
        ("Lottum", [(D, "7th (Westphalian) Dragoons"), (UH, "5th Uhlans"), (UH, "7th (Rhineland) Uhlans"), (UH, "8th (Rhineland) Uhlans")], True),
        ("Marwitz", [(HU, "9th (Rhineland) Hussars"), (HU, "12th Hussars")], True),
        ("Marwitz", [(LWC, "3rd Kurmark Landwehr Cavalry"), (LWC, "6th Kurmark Landwehr Cavalry")], False),
    ], True),
    "IV": ("Prince Wilhelm of Prussia", [
        ("Schwerin", [(D, "8th Dragoons"), (UH, "1st (West Prussian) Uhlans"), (HU, "6th (2nd Silesian) Hussars")], True),
        ("Watzdorf", [(HU, "8th (1st Westphalian) Hussars"), (HU, "10th (1st Magdeburg) Hussars")], True),
        ("Sydow", [(LWC, "1st Neumark Landwehr Cavalry"), (LWC, "2nd Neumark Landwehr Cavalry"),
                   (LWC, "1st Pomeranian Landwehr Cavalry"), (LWC, "2nd Pomeranian Landwehr Cavalry")], True),
        ("Sydow", [(LWC, "1st Silesian Landwehr Cavalry"), (LWC, "2nd Silesian Landwehr Cavalry"), (LWC, "3rd Silesian Landwehr Cavalry")], False),
    ], False),
}
CAVALRY_NOTES = {
    "I": "Lützow's brigade mixed line and Landwehr cavalry, which the list's brigades don't, so its two Landwehr regiments and the Westphalian are a brigade of their own here.",
    "III": "Lottum's brigade had three Uhlan regiments where the list allows two, and Marwitz's mixed line and Landwehr cavalry, so its two Kurmark regiments are a brigade of their own here.",
    "IV": "Sydow's brigade had seven Landwehr cavalry regiments, more than one of the list's brigades holds, so it is split in two here.",
}


def pr_cavalry(corps):
    """A corps' cavalry: its line and Landwehr brigades, each with a horse battery where it had one to spare"""
    _cmd, brigades, _reserve_horse = PR_CAVALRY[corps]
    out, seen = [], set()
    for commander, regiments, horse in brigades:
        landwehr = all(unit == LWC for unit, _ in regiments)
        part = " (Landwehr)" if commander in seen else ""
        seen.add(commander)
        out.append(bde("pr15-landwehr-cavalry-brigade" if landwehr else "pr15-cavalry-brigade",
                       f"{commander}'s Cavalry Brigade{part}", f"Gen-Maj von {commander}" if commander != "Sydow" else "Lt-Col von Sydow",
                       units=[u(unit, name) for unit, name in regiments] + ([u("pr15-horse-arty", "Horse Battery")] if horse else [])))
    return out


def pr_reserve(corps):
    """A corps' reserve artillery, as much of it as the list's reserve takes: one heavy, one foot and one horse battery"""
    reserve_horse = PR_CAVALRY[corps][2]
    return bde("pr15-army-reserve-artillery", f"{corps} Corps Reserve Artillery",
               units=[u("pr15-heavy-arty", "12-pdr Battery"), u("pr15-foot-arty", "6-pdr Battery")]
               + ([u("pr15-horse-arty", "Horse Battery")] if reserve_horse else []))


def prussian_corps(corps, battle, summary, notes=()):
    """A Prussian corps as one force: its four brigades were each the size of another army's division"""
    name, brigades, commander = PR_CORPS[corps]
    return force(f"{battle}-prussian-{corps.lower()}-corps", PR, name, f"{corps} Corps, Army of the Lower Rhine", "Prussian", summary,
                 [pr_brigade(n) for n in brigades] + pr_cavalry(corps) + [pr_reserve(corps)], command=[commander],
                 notes=[n_ for n_ in (PR_NOTES.get(n) for n in brigades) if n_] + list(notes) + [
                     "A Prussian brigade was the size of another army's division, so the whole corps is here. Take the brigades you want; each is a force in itself.",
                     "Each regiment's three battalions are the list's two Musketeer and one Fusilier battalions, or three Landwehr. The order of battle doesn't number the brigades' foot batteries.",
                     f"The corps cavalry, under {PR_CAVALRY[corps][0]}, follows Nafziger's order of battle (after Plotho). The list takes line or Landwehr cavalry brigades but not both, so a corps with both shows it as a historical departure.",
                     *([CAVALRY_NOTES[corps]] if corps in CAVALRY_NOTES else []),
                     "Nafziger gives each corps three 12-pdr batteries, a howitzer battery and more 6-pdr foot and horse batteries than its brigades had; the list's reserve takes one heavy, one foot and one horse battery, so only those are here. Which horse batteries rode with the cavalry brigades is our reading.",
                     CORPS_RATINGS[corps]])


# ---------------------------------------------------------------- Battles

def battle(id_, name, date, summary, forces):
    return {"id": id_, "name": name, "date": date, "campaign": "hundred-days", "summary": summary, "sources": SOURCES, "forces": forces}


ART = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]


def write(b):
    """Writes a battle, with its Staff Ratings set and its painting (art.json) where it has one"""
    ratings.apply(b)
    commanders.apply(b)
    if b["id"] in ART:
        b["art"] = ART[b["id"]]
    (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")


LIGNY = battle(
    "ligny", "Ligny", "16 June 1815",
    "Napoleon fell on Blücher's Prussians strung out along the Ligny brook. All afternoon the villages of Saint-Amand and Ligny changed hands; in the evening the Imperial Guard broke the Prussian centre. Blücher, ridden over in a cavalry charge, survived, and his army fell back north towards Wavre in good order.",
    [
        fr(LEFOL, "ligny", "Opened Vandamme's attack on Saint-Amand, fighting through the village and its walled orchards against Steinmetz's Prussians in some of the hardest fighting of the day."),
        fr(BERTHEZENE, "ligny", "Vandamme's reserve division, fed into the fighting around Saint-Amand as the Prussians counter-attacked through the afternoon."),
        fr(HABERT, "ligny", "Fought on Vandamme's left around Saint-Amand-la-Haye and Wagnelée, where Blücher tried to turn the French flank."),
        fr(GIRARD, "ligny", "Lent from Reille's corps, it took Saint-Amand-la-Haye and held it against repeated Prussian attacks. Girard was mortally wounded leading it."),
        fr(PECHEUX, "ligny", "Gérard's leading division against Ligny itself, where the fight for the village and its churchyard went on for hours at close quarters."),
        fr(VICHERY, "ligny", "Fed into Ligny village behind Pécheux, and part of the final push when the Guard broke through in the evening."),
        fr(HULOT, "ligny", "Led by Hulot after Bourmont deserted the day before, it held Gérard's right towards Tongrinne against Thielemann's corps."),
        middle_guard("ligny", "The Guard's grenadiers and chasseurs, sent in at dusk through Ligny village, broke the Prussian centre and decided the battle."),
        delort("ligny", "Milhaud's cuirassiers followed the Guard through the Prussian centre at dusk and caught Blücher's last counter-charge, in which the old marshal was unhorsed."),
        prussian_corps("I", "ligny", "Held the line of the Ligny brook from Saint-Amand to Ligny itself, and bore the worst of the day: Steinmetz's brigade fought for Saint-Amand all afternoon, Jagow's and Henckel's held Ligny village house by house until the Guard broke through at dusk."),
        prussian_corps("II", "ligny", "Blücher's reserve behind the line, fed in brigade by brigade: into Saint-Amand-la-Haye and Wagnelée to try to turn the French left, and into Ligny as the centre was worn down."),
        prussian_corps("III", "ligny", "Held the Prussian left around Sombreffe, Tongrinne and Boignée. Kept apart from the main fight by Grouchy's cavalry and Hulot's division, it came through the day the least hurt of Blücher's corps."),
    ],
)

QUATRE_BRAS = battle(
    "quatre-bras", "Quatre Bras", "16 June 1815",
    "While Napoleon fought the Prussians at Ligny, Ney attacked the crossroads of Quatre Bras, held at first only by Perponcher's Netherlanders. Through the afternoon Wellington's divisions arrived one after another to hold the farms, the Bossu wood and the road. By nightfall the allies held the field, but they could not march to help Blücher.",
    [
        fr(BACHELU, "quatre-bras", "Ney's right-hand division, attacking across the fields east of the Charleroi road into Picton's newly arrived battalions."),
        fr(FOY, "quatre-bras", "Pressed up the main road towards the crossroads, taking Gemioncourt farm and fighting for the ground beside it into the evening."),
        fr(JEROME, "quatre-bras", "Fought its way into the Bossu wood on the French left, until Cooke's Guards cleared it again at dusk."),
        pire("quatre-bras", "Its lancers and chasseurs rode down allied battalions caught out of square, and in one charge came close to taking the crossroads."),
        guiton("quatre-bras", "Kellermann led this one brigade straight up the road to the crossroads, riding over the 69th and taking its colour, before guns and musketry drove it back."),
        perponcher("quatre-bras", "Held the crossroads alone through the morning and early afternoon against Ney's whole corps, buying the time for Wellington's army to come up.",
                   ["At Quatre Bras the division fought complete; it suffered heavily, which matters if it's used for Waterloo."]),
        picton("quatre-bras", "Arrived in the afternoon to hold the Namur road east of the crossroads. Its squares stood against charge after charge of lancers and cuirassiers; Pack's Highlanders suffered terribly.",
               ("Best's Brigade (4th Hanoverian)", "Col Charles Best", ["Lüneburg", "Münden", "Osterode", "Verden"])),
        brunswick("quatre-bras", "Came up in the afternoon to fill the gap beside the Bossu wood. The Duke of Brunswick was killed rallying his men against Piré's cavalry.",
                  "Duke of Brunswick", ["At Quatre Bras the Duke of Brunswick led the corps, and was killed there."]),
        alten("quatre-bras", "Came up late in the afternoon. Halkett's brigade was caught by Kellermann's cuirassiers before it could form square, and the 69th lost a colour.",
              ["At Quatre Bras Ompteda's brigade arrived last and was little engaged; Alten's other brigades did the fighting."]),
        cooke("quatre-bras", "Arrived after a long march in the evening and cleared Prince Jérôme's men out of the Bossu wood."),
    ],
)


def waterloo():
    existing = json.loads((OUT / "waterloo.json").read_text())
    kept = {f["id"]: f for f in existing["forces"]}
    allied = [
        kept["waterloo-picton"],
        kept["waterloo-alten"],
        cooke("waterloo", "Held the allied right. Its light companies, with others, defended the château of Hougoumont all day, while Maitland's brigade lay behind the ridge until it rose to meet the Guard's last attack in the evening."),
        clinton("waterloo", "Stood in reserve behind Hougoumont through the afternoon. In the evening Adam's brigade swung forward against the flank of the Imperial Guard's attack, and the 52nd's volleys helped break it."),
        lambert("waterloo", "Came up from Brussels to the allied left centre, and was sent forward to plug the line around La Haye Sainte in the late afternoon, suffering heavily."),
        perponcher("waterloo", "Formed on the allied left centre. Bijlandt's brigade, worn down at Quatre Bras, stood in the path of d'Erlon's attack; Saxe-Weimar's Nassauers held the farms of Papelotte and La Haye on the far left all day.",
                   ["Bijlandt's brigade had lost heavily at Quatre Bras; Small upgrades are a fair way to show it."]),
        chasse("waterloo", "In reserve on the far right until the evening, when Chassé brought it into the centre, where it helped turn back the last attack of the Imperial Guard."),
        kruse("waterloo", "Stood in the allied centre beside the Brussels road, behind La Haye Sainte, and fought to hold the line there as the farm fell."),
        brunswick("waterloo", "Stood in the centre-right through the great cavalry charges, then went forward to close the line beside Alten's division in the evening.",
                  "Col Olfermann", ["The Duke of Brunswick had been killed at Quatre Bras, so Olfermann commanded at Waterloo."]),
        uxbridge_heavies("waterloo", "Charged d'Erlon's broken columns in the early afternoon, scattering them and taking two eagles, then rode on into the French guns and were cut up by lancers and cuirassiers."),
        light_cavalry("waterloo", "Guarded the allied left flank until the Prussians arrived, then moved to the centre in the evening and charged in the final general advance."),
    ]
    french = [
        kept["waterloo-donzelot"], kept["waterloo-marcognet"],
        fr(QUIOT, "waterloo", "The left-hand division of d'Erlon's great attack, part of it against La Haye Sainte and the rest up the slope towards Kempt's brigade, before the Union Brigade drove it back."),
        fr(DURUTTE, "waterloo", "On d'Erlon's right, attacking towards Papelotte. It kept its order when the rest of the corps was broken, and fought on against the farms into the evening."),
        fr(JEROME, "waterloo", "Opened the battle against Hougoumont and spent the whole day trying to take it, drawing in far more men than the allied garrison."),
        fr(FOY, "waterloo", "Fed into the fighting around Hougoumont, then joined Bachelu's late infantry attack between the château and La Haye Sainte."),
        fr(BACHELU, "waterloo", "Stood in reserve behind Hougoumont until the evening, when it and Foy's division made a last infantry attack after the great cavalry charges had failed."),
        fr(SIMMER, "waterloo", "Sent east with Lobau's corps to hold off the Prussians, it fought for Plancenoit through the late afternoon and evening."),
        fr(JEANIN, "waterloo", "Lobau's second division, small after detachments, holding the ground in front of Plancenoit against Bülow's corps."),
        wathier("waterloo", "Led Ney's great cavalry charges against the allied squares between Hougoumont and La Haye Sainte through the middle of the afternoon."),
        delort("waterloo", "Joined Milhaud's charges on the allied centre, riding round the squares again and again under the allied guns."),
        lheritier("waterloo", "Kellermann's corps, sent in to join Milhaud's charges on the allied squares late in the afternoon."),
        roussel("waterloo", "The carabiniers and cuirassiers of Kellermann's second division, committed to the cavalry charges on the allied centre."),
        jacquinot("waterloo", "Guarded d'Erlon's right flank, and its lancers fell on the Union Brigade when it charged too far."),
        old_guard("waterloo", "The Emperor's last reserve. Battalions went to retake Plancenoit from the Prussians; at the end, the 1st and 2nd Grenadiers and Chasseurs formed the squares that covered the retreat."),
        middle_guard("waterloo", "Made the last French attack of the day up the slope west of La Haye Sainte, and was broken by Maitland's Guards and Adam's brigade."),
        young_guard("waterloo", "Sent to hold Plancenoit against Bülow's Prussians, it fought in the village through the evening until driven out."),
        guard_cavalry("waterloo", "Followed Milhaud and Kellermann into the great charges on the allied squares in the late afternoon."),
    ]
    prussians = [
        prussian_corps("IV", "waterloo", "The first Prussian corps onto the field, untouched at Ligny. Losthin's and Hiller's brigades came out of the Bois de Paris onto the French right in the late afternoon, and with Hake's and Ryssel's behind them fought Lobau's corps and the Young Guard for Plancenoit until it fell in the evening."),
        prussian_corps("I", "waterloo", "Marched across from Wavre to join Wellington's left. Steinmetz's brigade led it onto the field near Papelotte in the evening, and pushed into the French right as their line broke.",
                       ["At Waterloo only Steinmetz's brigade, at the head of the column, was fully engaged; the rest of the corps was still coming up."]),
    ]
    b = battle("waterloo", "Waterloo", "18 June 1815", existing["summary"], allied + french + prussians)
    return b


WATERLOO_SUMMARY = (
    "Wellington's Anglo-allied army held the ridge of Mont-Saint-Jean through a long afternoon of French attacks: "
    "on Hougoumont, d'Erlon's great columns, Ney's cavalry and finally the Imperial Guard. From late afternoon Blücher's "
    "Prussians came up on Napoleon's right at Plancenoit, and in the evening the French army broke."
)

WAVRE = battle(
    "wavre", "Wavre", "18–19 June 1815",
    "Sent after the Prussians with a third of the army, Grouchy caught Thielemann's corps holding the crossings of the Dyle at Wavre while the rest of Blücher's army marched to Waterloo. The French fought for the bridges into the night and won the field the next morning, too late and too far away to matter.",
    [
        fr(LEFOL, "wavre", "Vandamme's leading division, sent straight at the bridges into Wavre town and thrown back again and again."),
        fr(HABERT, "wavre", "Attacked the bridges in Wavre itself; Habert was badly wounded leading his men across."),
        fr(BERTHEZENE, "wavre", "Part of Vandamme's attacks on Wavre town and its crossings through the afternoon."),
        fr(PECHEUX, "wavre", "Gérard's corps came up to attack the mill at Bierges, upstream of Wavre, where Gérard himself was wounded."),
        fr(VICHERY, "wavre", "With Gérard's corps, crossed the Dyle upstream at Limale in the evening to turn the Prussian flank."),
        fr(HULOT, "wavre", "Attacked the Bierges mill crossing with Gérard's corps before moving on to Limale."),
        fr(TESTE, "wavre", "Lobau's third division, detached to Grouchy, it fought for Wavre and covered his withdrawal on 20 June."),
        strolz("wavre", "Exelmans' dragoons, who had followed the Prussians from Ligny, screening the French advance on the Dyle."),
        prussian_corps("III", "wavre", "Left behind as Blücher's rearguard while the rest of the army marched to Waterloo. Kemphen's brigade held Wavre's bridges against Vandamme, Luck's Landwehr the Dyle beside it, and Stülpnagel's the upstream crossings at Bierges and Limale, where Grouchy turned the flank on the 19th.",
                       ["Borcke's brigade had begun the march to Waterloo and only part of it came back to fight."]),
    ],
)


if __name__ == "__main__":
    for b in (LIGNY, QUATRE_BRAS, WAVRE):
        write(b)
    w = waterloo()
    w["summary"] = WATERLOO_SUMMARY
    write(w)
    for b in (LIGNY, QUATRE_BRAS, w, WAVRE):
        print(f"{b['name']}: {len(b['forces'])} forces")
