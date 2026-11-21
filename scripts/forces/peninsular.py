"""
Writes the Peninsular War's historical forces (src/data/battles/{rolica,vimeiro,albuera}.json) from the
Albion Triumphant lists: the Peninsular British (with the Portuguese), the Peninsular French and the
Spanish.

    python3 scripts/forces/peninsular.py && npm run check:forces

Sources (see each battle's SOURCES): Wikipedia's battle articles and its Vimeiro and Albuera orders of
battle (the latter citing Oman and Lipscombe), Ron McGuigan's order of battle of the British army in
Portugal and Stuart Hadaway's account of Roliça on the Napoleon Series. Summaries are our own words;
ratings.py sets Staff Ratings as each battle is written.
"""

import json
from pathlib import Path

import ratings
from hundred_days import bde, cmd, force, u

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
ART = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
ROMAN = ["I", "II", "III", "IV"]

# ---------------------------------------------------------------- The Peninsular British (and Portuguese)

PB = "peninsular-british"


def line(name, **kw):
    return u("pb-line", name, **kw)


def light(name):
    return u("pb-line", name, options=["light-infantry"])


def highland(name):
    return u("pb-line", name, options=["highlanders"])


def pb_bde(name, commander, units):
    return bde("pb-infantry-brigade", name, commander, units)


def pb_battery(name, unit="pb-royal-arty"):
    return bde("pb-divisional-artillery", name, units=[u(unit, name)])


def portuguese(name, commander, units):
    return bde("pb-portuguese-infantry-brigade", name, commander, units)


def pt_line(name, large=False):
    return u("pb-portuguese-line", name, **({"options": ["large"]} if large else {}))


# ---------------------------------------------------------------- The Peninsular French

PF = "peninsular-french"


def pf_regiment(num, n, kind="Ligne", first=0):
    """A French regiment's battalions; a Léger regiment takes the list's Light upgrade, which is the regiment's"""
    label = f"{num} {kind}"
    reg = {"name": label, "units": [u("pf-line", f"{ROMAN[first + i]}/{label}") for i in range(n)]}
    if kind == "Léger":
        reg["options"] = ["light"]
    return reg


def pf_bde(name, commander, regiments):
    return bde("pf-infantry-brigade", name, commander, regiments=regiments)


def pf_battery(name, unit="pf-foot-arty"):
    return bde("pf-army-artillery", name, units=[u(unit, name)])


def pf_cav(name, commander, regiments):
    kinds = {"Dragons": "pf-dragoon", "Hussards": "pf-line-light-cav", "Chasseurs": "pf-line-light-cav", "Lanciers": "pf-vistula-lancer"}
    return bde("pf-cavalry-brigade", name, commander, [u(kinds[k], f"{n} {k}") for n, k in regiments])


# The batteries an order of battle gives a force can be more than the list's "one per six battalions"
ARTILLERY = "The force had more guns than the list allows for its battalions (one battery per six), which shows as a historical departure."

# ---------------------------------------------------------------- The Spanish

SP = "spanish"


def sp_regiment(name, n=1):
    return {"name": name, "units": [u("sp-line", f"{ROMAN[i]}/{name}" if n > 1 else name) for i in range(n)]}


SPANISH_BATTALIONS = (
    "The order of battle names each Spanish unit but gives no battalion counts, so each is taken as one battalion."
)

# ---------------------------------------------------------------- Roliça

ROLICA_SOURCES = [
    {"label": "Battle of Roliça (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Roli%C3%A7a"},
    {"label": "Stuart Hadaway, Roliça: a most important affair (Napoleon Series)",
     "url": "https://www.napoleon-series.org/military-info/battles/1808/c_rolica1.html"},
    {"label": "Ron McGuigan, The British Army in Portugal and Spain: its order of battle (Napoleon Series)",
     "url": "https://www.napoleon-series.org/military-info/battles/1808/Peninsula/BritishArmy/c_britarmy2.html"},
]

ROLICA = {
    "id": "rolica", "name": "Roliça", "date": "17 August 1808", "campaign": "peninsular-war",
    "summary": "Wellesley's first battle in the Peninsula. Delaborde held a string of hill positions with a small division to delay the British march on Lisbon; Wellesley turned him out of the first, then out of the steep gullies of the second, with Ferguson's column working round the French right, and Delaborde fell back in good order.",
    "sources": ROLICA_SOURCES,
    "forces": [
        force("rolica-centre", PB, "Wellesley's Centre", "The main column", "Anglo-Portuguese",
              "The bulk of Wellesley's army, which pinned Delaborde in front. The 29th, pushing too far up a gully, was caught and its colonel killed, but the attack carried the heights.",
              [pb_bde("Hill's Brigade", "Maj-Gen Rowland Hill",
                      [line("1/5th Foot"), line("1/9th Foot"), line("1/38th Foot"), u("pb-light-dragoon-small", "20th Light Dragoons (detachment)")]),
               pb_bde("Nightingall's Brigade", "Brig-Gen Miles Nightingall", [line("29th Foot"), line("1/82nd Foot")]),
               pb_bde("Craufurd's Brigade", "Brig-Gen Catlin Craufurd", [line("1/45th Foot"), line("1/50th Foot"), highland("1/91st Highlanders")]),
               pb_bde("Fane's Brigade", "Brig-Gen Henry Fane", [u("pb-rifle-coys", "5/60th Rifles"), u("pb-rifle-coy", "2/95th Rifles (four companies)")]),
               bde("pb-portuguese-cavalry-brigade", "Portuguese Cavalry", "",
                   [u("pb-portuguese-cavalry", "6th (Bragança) Cavalry"), u("pb-portuguese-cavalry", "12th (Miranda) Cavalry")]),
               pb_battery("Light 6-pdr Battery"), pb_battery("Light 6-pdr Battery")],
              command=[{"unit": "pb-cmd-wellington"}],
              notes=["Fane's light brigade was riflemen only, the 5/60th and four companies of the 2/95th, with no Line battalions for the list's Infantry Brigade; that shows as a historical departure.",
                     "The 6th Caçadores were held in reserve and are left out. The centre had twelve guns, shown as two batteries.", ARTILLERY]),
        force("rolica-ferguson", PB, "Ferguson's Column", "The left flank march", "Anglo-Portuguese",
              "Sent wide round the French right to cut them off, Ferguson's column came in late; its threat helped force Delaborde back from his second position.",
              [pb_bde("Ferguson's Brigade", "Maj-Gen Ronald Ferguson",
                      [line("36th Foot"), line("1/40th Foot"), highland("1/71st Highlanders"), u("pb-rifle-coys", "Rifle companies")]),
               pb_bde("Bowes's Brigade", "Brig-Gen Barnard Bowes", [line("1/6th Foot"), line("1/32nd Foot")]),
               pb_battery("Light 6-pdr Battery")],
              command=[cmd("pb-div-cmd", "Maj-Gen Ronald Ferguson")],
              notes=["The column had three companies of riflemen and six guns.", ARTILLERY]),
        force("rolica-trant", PB, "Trant's Portuguese", "The right flank march", "Anglo-Portuguese",
              "Trant's Portuguese marched round the French left to threaten their line of retreat.",
              [portuguese("Trant's Brigade", "Lt-Col Nicholas Trant",
                          [pt_line("12th (Chaves) Line"), pt_line("21st (Valença) Line"), pt_line("24th (Bragança) Line")]),
               bde("pb-portuguese-cavalry-brigade", "Cavalry", "", [u("pb-portuguese-cavalry", "11th (Almeida) Cavalry", options=["small"])])],
              command=[cmd("pb-div-cmd", "Lt-Col Nicholas Trant")],
              notes=["Three Portuguese line regiments where the list's brigade takes two, and no British brigades for the Portuguese one to go with; these show as historical departures.",
                     "The 11th Cavalry had about fifty men, so it's Small."]),
        force("rolica-delaborde", PF, "Delaborde's Division", "Detached from Junot's Army of Portugal", "French",
              "Five battalions, a few squadrons and five guns, outnumbered three or four to one, which held two positions in turn and got away with the loss of three guns.",
              [pf_bde("Brenier's Brigade", "Gén. de Brigade Brenier", [pf_regiment("70e", 2), pf_regiment("2e", 1, "Léger")]),
               pf_bde("Thomières's Brigade", "Gén. de Brigade Thomières", [pf_regiment("4e", 1, "Léger"), pf_regiment("4e", 1, "Suisse")]),
               pf_cav("Cavalry", "", [("26e", "Chasseurs")]),
               pf_battery("Foot Battery (five guns)")],
              command=[cmd("pf-div-cmd", "Gén. de Division Delaborde")],
              notes=["The sources give the battalions but not their brigades at Roliça; they're grouped as Brenier and Thomières had them at Vimeiro.",
                     "The 26th Chasseurs were a single regiment where the list's Cavalry Brigade takes two, which shows as a historical departure.", ARTILLERY]),
    ],
}

# ---------------------------------------------------------------- Vimeiro

VIMEIRO_SOURCES = [
    {"label": "Battle of Vimeiro order of battle (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Vimeiro_order_of_battle"},
    {"label": "Battle of Vimeiro (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Vimeiro"},
    {"label": "Ron McGuigan, The British Army in Portugal and Spain: its order of battle (Napoleon Series)",
     "url": "https://www.napoleon-series.org/military-info/battles/1808/Peninsula/BritishArmy/c_britarmy2.html"},
]

VIMEIRO = {
    "id": "vimeiro", "name": "Vimeiro", "date": "21 August 1808", "campaign": "peninsular-war",
    "summary": "Junot came out of Lisbon to attack Wellesley's army around the village of Vimeiro. His columns were shot to pieces by the British line on Vimeiro hill and on the eastern ridge, and by midday the French were in retreat. Wellesley was stopped from pursuing by his newly arrived superiors, and the Convention of Cintra followed.",
    "sources": VIMEIRO_SOURCES,
    "forces": [
        force("vimeiro-hill", PB, "Vimeiro Hill", "Fane's and Anstruther's Brigades", "Anglo-Portuguese",
              "Held the hill before the village against Delaborde's columns and Kellermann's grenadiers; the 20th Light Dragoons charged the broken French and were cut up in turn.",
              [pb_bde("Fane's Brigade", "Brig-Gen Henry Fane",
                      [line("1/50th Foot"), u("pb-rifle-coys", "5/60th Rifles"), u("pb-rifle-coy", "2/95th Rifles (four companies)")]),
               pb_bde("Anstruther's Brigade", "Brig-Gen Robert Anstruther",
                      [line("2/9th Foot"), light("2/43rd Light Infantry"), light("2/52nd Light Infantry"), line("2/97th Foot"),
                       u("pb-light-dragoon-small", "20th Light Dragoons")]),
               pb_battery("Foot Battery")],
              command=[{"unit": "pb-cmd-wellington"}],
              notes=["Fane's brigade had one Line battalion where the list's brigade takes two, and Anstruther's two Light battalions where it allows one in four; these show as historical departures.",
                     "The 20th Light Dragoons (240 men) are the list's attached Small Light Dragoon regiment.", ARTILLERY]),
        force("vimeiro-eastern-ridge", PB, "The Eastern Ridge", "Ferguson's, Nightingall's, Bowes's and Acland's Brigades", "Anglo-Portuguese",
              "Moved across to the ridge north-east of the village as Junot's flank march appeared, it broke Solignac's and then Brenier's columns at Ventosa and took their guns.",
              [pb_bde("Ferguson's Brigade", "Maj-Gen Ronald Ferguson", [line("36th Foot"), line("1/40th Foot"), highland("1/71st Highlanders")]),
               pb_bde("Nightingall's Brigade", "Brig-Gen Miles Nightingall", [line("29th Foot"), line("1/82nd Foot")]),
               pb_bde("Bowes's Brigade", "Brig-Gen Barnard Bowes", [line("1/6th Foot"), line("1/32nd Foot")]),
               pb_bde("Acland's Brigade", "Brig-Gen Wroth Acland",
                      [line("2nd Foot"), line("20th Foot (7½ companies)", options=["small"]), u("pb-rifle-coy", "1/95th Rifles (two companies)")]),
               pb_battery("Foot Battery")],
              command=[cmd("pb-div-cmd", "Maj-Gen Ronald Ferguson")],
              notes=["The 20th Foot had 401 men in seven and a half companies, so it's Small."]),
        force("vimeiro-reserve", PB, "Hill, Craufurd and Trant", "The western ridge and reserve", "Anglo-Portuguese",
              "Wellesley's reserve on the western ridge behind the village, with Trant's Portuguese, little engaged as the fighting went to the hill and the eastern ridge.",
              [pb_bde("Hill's Brigade", "Maj-Gen Rowland Hill", [line("1/5th Foot"), line("1/9th Foot"), line("1/38th Foot")]),
               pb_bde("Craufurd's Brigade", "Brig-Gen Catlin Craufurd", [line("1/45th Foot"), highland("91st Highlanders")]),
               portuguese("Trant's Brigade", "Lt-Col Nicholas Trant",
                          [pt_line("12th Line"), pt_line("21st Line"), pt_line("24th Line", large=False), u("pb-cacadores", "Porto Caçadores", options=["cacadores-green"])]),
               bde("pb-portuguese-cavalry-brigade", "Portuguese Cavalry", "",
                   [u("pb-portuguese-cavalry", "6th Cavalry", options=["small"]), u("pb-portuguese-cavalry", "11th Cavalry", options=["small"]),
                    u("pb-portuguese-cavalry", "12th Cavalry", options=["small"])]),
               pb_battery("Portuguese Battery (4th Artillery)", "pb-portuguese-arty")],
              command=[cmd("pb-div-cmd", "Maj-Gen Brent Spencer")],
              notes=["Spencer, Wellesley's second in command, leads it. Trant had three Portuguese line regiments where the list's brigade takes two, which shows as a historical departure.",
                     "The Portuguese cavalry regiments had about a hundred men each, so they're Small; the Lisbon police cavalry (41) are left out. The Porto Caçadores are the list's untried early Caçadores."]),
        force("vimeiro-delaborde", PF, "Delaborde's Division", "Army of Portugal (Junot)", "French",
              "Attacked Vimeiro hill head on in column; Thomières's and then Brenier's brigades were broken by the British line, Brenier later attacking again at Ventosa, where he was wounded and taken.",
              [pf_bde("Brenier's Brigade", "Gén. de Brigade Brenier",
                      [pf_regiment("70e", 2), pf_regiment("2e", 1, "Léger", first=2), pf_regiment("4e", 1, "Léger", first=2)]),
               pf_bde("Thomières's Brigade", "Gén. de Brigade Thomières",
                      [pf_regiment("86e", 2), {"name": "4e Suisse", "units": [u("pf-line", "4e Suisse (two companies)", options=["small"])]}]),
               pf_battery("Foot Battery")],
              command=[cmd("pf-div-cmd", "Gén. de Division Delaborde")],
              notes=["The two companies of the 4th Swiss are Small."]),
        force("vimeiro-loison", PF, "Loison's Division", "Army of Portugal (Junot)", "French",
              "Half of it went straight at Vimeiro hill with Delaborde; Solignac's brigade marched round to the eastern ridge, where it was broken by Ferguson.",
              [pf_bde("Solignac's Brigade", "Gén. de Brigade Solignac",
                      [pf_regiment("12e", 1, "Léger", first=2), pf_regiment("15e", 1, "Léger", first=2), pf_regiment("58e", 1, first=2)]),
               pf_bde("Charlot's Brigade", "Gén. de Brigade Charlot", [pf_regiment("32e", 1, first=2), pf_regiment("82e", 1, first=2)]),
               pf_battery("Foot Battery")],
              command=[cmd("pf-div-cmd", "Gén. de Division Loison")],
              notes=["Each regiment's third battalion served, most of them over 1,000 strong; one battalion per brigade could be Large.", ARTILLERY]),
        force("vimeiro-reserve-fr", PF, "Junot's Reserve", "Kellermann's grenadiers and Margaron's cavalry", "French",
              "Junot's last throw: Kellermann's converged grenadiers went up Vimeiro hill and were thrown back like the rest, while Margaron's dragoons covered the retreat.",
              [bde("pf-reserve-infantry-brigade", "Kellermann's Grenadiers", "Gén. de Division Kellermann",
                   [u("pf-combined-grenadier", "I/1st Reserve Grenadiers"), u("pf-combined-grenadier", "II/1st Reserve Grenadiers"),
                    u("pf-combined-grenadier", "I/2nd Reserve Grenadiers"), u("pf-combined-grenadier", "II/2nd Reserve Grenadiers")]),
               pf_cav("Margaron's Cavalry", "Gén. de Brigade Margaron",
                      [("3rd Provisional", "Dragons"), ("4th Provisional", "Dragons"), ("5th Provisional", "Dragons"), ("1st Provisional", "Chasseurs")]),
               pf_battery("Foot Battery")],
              command=[{"unit": "pf-cmd-junot"}],
              notes=["Junot is the book's named commander.",
                     "Without the army's infantry divisions there are no Infantry Brigades, which the list needs and which its cavalry is allowed by; these show as historical departures. The squadron of volunteer cavalry is left out.", ARTILLERY]),
    ],
}

# ---------------------------------------------------------------- Albuera

ALBUERA_SOURCES = [
    {"label": "Battle of Albuera order of battle (Wikipedia, after Oman and Lipscombe)",
     "url": "https://en.wikipedia.org/wiki/Battle_of_Albuera_order_of_battle"},
    {"label": "Battle of Albuera (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Albuera"},
    {"label": "Battle of Albuera (History of War)", "url": "https://www.historyofwar.org/articles/battles_albuera.html"},
]

ALLIED_ART = "Batteries are given to divisions as the order of battle lists them under Dickson's artillery; it doesn't say which served with which."

ALBUERA = {
    "id": "albuera", "name": "Albuera", "date": "16 May 1811", "campaign": "peninsular-war",
    "summary": "Soult marched to relieve Badajoz and fell on Beresford's British, Portuguese and Spanish army behind the Albuera stream. His main blow came round the allied right; Zayas's Spaniards held it, Colborne's brigade was ridden down by lancers in a hailstorm, and the British 2nd and 4th Divisions fought it out with Girard's and Gazan's columns in one of the bloodiest battles of the war until the French gave way.",
    "sources": ALBUERA_SOURCES,
    "forces": [
        force("albuera-stewart", PB, "Stewart's 2nd Division", "Beresford's army", "Anglo-Portuguese",
              "Thrown in to support the Spanish on the hill. Colborne's brigade, caught in line by the Vistula lancers and hussars in a squall, lost three of its four battalions; Hoghton's and Abercrombie's then stood and traded volleys with the French columns at close range.",
              [pb_bde("Colborne's Brigade", "Lt-Col John Colborne",
                      [line("1/3rd (Buffs)"), line("2/31st Foot"), line("2/48th Foot"), line("2/66th Foot")]),
               pb_bde("Hoghton's Brigade", "Maj-Gen Daniel Hoghton",
                      [line("29th Foot"), line("1/48th Foot"), line("1/57th Foot (Die-hards)"), u("pb-rifle-coys", "5/60th Rifles (three companies)")]),
               pb_bde("Abercrombie's Brigade", "Lt-Col Alexander Abercrombie", [line("2/28th Foot"), line("2/34th Foot"), line("2/39th Foot")]),
               pb_battery("Hawker's Battery RA")],
              command=[cmd("pb-div-cmd", "Maj-Gen William Stewart")],
              notes=["The division's three companies of the 5/60th are the list's Small Rifle Companies, with Hoghton's brigade.", ALLIED_ART]),
        force("albuera-cole", PB, "Cole's 4th Division", "Beresford's army", "Anglo-Portuguese",
              "Advanced on its own initiative late in the battle; Myers's Fusiliers climbed the slope into the flank of the French columns and broke them, while Harvey's Portuguese held off the French cavalry.",
              [pb_bde("Myers's Fusilier Brigade", "Lt-Col Sir William Myers", [line("1/7th Fusiliers"), line("2/7th Fusiliers"), line("1/23rd Royal Welch Fusiliers")]),
               portuguese("Harvey's Brigade", "Brig-Gen William Harvey",
                          [pt_line("11th Line", large=True), pt_line("23rd Line", large=True), u("pb-loyal-lusitanian", "Loyal Lusitanian Legion")]),
               pb_battery("Sympher's Battery KGL")],
              command=[cmd("pb-div-cmd", "Maj-Gen Lowry Cole")],
              notes=["Each Portuguese line regiment of two battalions is one of the list's regiments, Large at over 1,100 men; the list allows one Large regiment in a brigade, and the British brigades its Portuguese one goes with, so these show as historical departures.",
                     "Kemmis's brigade was only three light companies at Albuera and is left out.", ALLIED_ART]),
        force("albuera-hamilton", PB, "Hamilton's Portuguese Division", "Beresford's army", "Anglo-Portuguese",
              "Held the allied left around the village and the bridge, moving across late in the day to support the right.",
              [portuguese("Campbell's Brigade", "Brig-Gen Archibald Campbell", [pt_line("4th Line", large=True), pt_line("10th Line", large=True)]),
               portuguese("Fonseca's Brigade", "Brig-Gen Luiz Fonseca", [pt_line("2nd Line", large=True), pt_line("14th Line", large=True)]),
               pb_battery("Braun's Portuguese Battery", "pb-portuguese-arty"), pb_battery("Arriaga's Portuguese Battery", "pb-portuguese-arty")],
              command=[cmd("pb-div-cmd", "Maj-Gen John Hamilton")],
              notes=["Each Portuguese line regiment of two battalions is one of the list's regiments, Large at over 1,100 men, where the list allows one Large in a brigade. With no British brigades for its Portuguese brigades to go with, and more guns than its battalions allow, these show as historical departures.", ALLIED_ART]),
        force("albuera-alten", PB, "Alten's and Collins's Brigades", "Albuera village", "Anglo-Portuguese",
              "Alten's King's German Legion light battalions held the village of Albuera and its bridge against Godinot's attack all day, with Collins's Portuguese in support.",
              [bde("pb-kgl-light-brigade", "Alten's KGL Brigade", "Maj-Gen Charles Alten",
                   [u("pb-kgl-light", "1st Light Bn KGL"), u("pb-kgl-light", "2nd Light Bn KGL")]),
               portuguese("Collins's Brigade", "Col Richard Collins", [pt_line("5th Line"), u("pb-cacadores", "5th Caçadores")]),
               pb_battery("Cleeves' Battery KGL")],
              command=[cmd("pb-div-cmd", "Maj-Gen Charles Alten")],
              notes=["No British Infantry Brigade for the list's Portuguese brigade to go with, which shows as a historical departure.", ARTILLERY, ALLIED_ART]),
        force("albuera-lumley", PB, "Lumley's Cavalry", "Beresford's army", "Anglo-Portuguese",
              "Outnumbered more than two to one by Latour-Maubourg's horsemen, it held the open ground on the allied right and kept the French cavalry from rolling up the line.",
              [bde("pb-heavy-cavalry-brigade", "De Grey's Brigade", "Col George de Grey",
                   [u("pb-dragoon-guards", "3rd Dragoons"), u("pb-dragoon-guards", "4th Dragoons"), u("pb-light-dragoon-hussar", "13th Light Dragoons")]),
               bde("pb-portuguese-cavalry-brigade", "Otway's Portuguese Brigade", "Col Loftus Otway",
                   [u("pb-portuguese-cavalry", "1st Dragoons"), u("pb-portuguese-cavalry", "7th Dragoons"),
                    u("pb-portuguese-cavalry", "5th and 8th Dragoons (a squadron each)", options=["small"])]),
               bde("pb-horse-artillery", "Lefebvre's Troop RHA", units=[u("pb-royal-horse-arty", "Lefebvre's Troop RHA")])],
              command=[cmd("pb-div-cmd", "Maj-Gen William Lumley")],
              notes=["The 13th Light Dragoons, unbrigaded, are the list's Light Dragoon regiment with the heavy brigade.",
                     "Cavalry on its own has none of the infantry brigades its brigades are allowed by, which shows as a historical departure."]),
        force("albuera-zayas", SP, "Zayas's Division", "4th Army (Blake)", "Spanish",
              "Swung round to face Soult's flank attack on the hill, it stood in line under the French columns' fire for the critical first hour, its Guards and Irish regiments holding until the British came up.",
              [bde("sp-guard-infantry-brigade", "Cruz-Murgeon's Brigade", "Brig-Gen Cruz-Murgeon",
                   [u("sp-guard-infantry", "2nd Spanish Guards"), u("sp-guard-infantry", "4th Spanish Guards"), u("sp-guard-infantry", "1st Walloon Guards"),
                    u("sp-line", "2nd Irlanda"), u("sp-line", "3rd Irlanda")]),
               bde("sp-infantry-brigade", "Polo's Brigade", "Brig-Gen Polo",
                   regiments=[sp_regiment("Imperiales de Toledo"), sp_regiment("Legión de Extranjeros"), sp_regiment("Ciudad Rodrigo"), sp_regiment("Patria")]),
               bde("sp-artillery-support", "Battery", units=[u("sp-artillery", "Foot Battery")])],
              command=[cmd("sp-div-cmd", "Gen José Zayas")],
              notes=["The 1st Walloon Guards (with Polo) and the Patria regiment (with Cruz-Murgeon) are swapped between the brigades, so the Guards serve together; even so there are three Guard battalions where the list's brigade takes two, and four regiments in Polo's where it takes three, which show as historical departures.",
                     SPANISH_BATTALIONS]),
        force("albuera-lardizabal", SP, "Lardizábal's Division", "Vanguard Division, 4th Army (Blake)", "Spanish",
              "Blake's vanguard, which formed alongside Zayas on the threatened right and shared in the long firefight on the hill.",
              [bde("sp-infantry-brigade", "Casinos's Brigade", "Brig-Gen Casinos",
                   [u("sp-militia", "Provincial Militia of Canarias")], regiments=[sp_regiment("Murcia", 2)]),
               bde("sp-infantry-brigade", "Second Brigade", "",
                   [u("sp-light", "Cazadores Reunidos")], regiments=[sp_regiment("León"), sp_regiment("Campo Mayor")]),
               bde("sp-artillery-support", "Battery", units=[u("sp-artillery", "Foot Battery")])],
              command=[cmd("sp-div-cmd", "Gen José de Lardizábal")],
              notes=[SPANISH_BATTALIONS]),
        force("albuera-ballesteros", SP, "Ballesteros's Division", "3rd Division, 4th Army (Blake)", "Spanish",
              "Asturian and Catalan battalions that came up on the right in support of Zayas as the French attack developed.",
              [bde("sp-infantry-brigade", "First Brigade", "",
                   [u("sp-light", "Catalan Light Companies"), u("sp-light", "2nd Cazadores de Barbastro")], regiments=[sp_regiment("Pravia")]),
               bde("sp-infantry-brigade", "Carvajal's Brigade", "Brig-Gen Carvajal",
                   regiments=[sp_regiment("Lena"), sp_regiment("Castropol"), sp_regiment("Cangas de Tineo"), sp_regiment("Infiesto")])],
              command=[cmd("sp-div-cmd", "Gen Francisco Ballesteros")],
              notes=["Carvajal's four Asturian regiments are one more than the list's brigade takes, which shows as a historical departure.", SPANISH_BATTALIONS]),
        force("albuera-girard", PF, "Girard's Division", "1st Division, V Corps", "French",
              "Led Soult's flanking attack onto the hill in a vast column of battalions; held by the Spanish line, it was shot to pieces in the long exchange of fire with Stewart's brigades.",
              [pf_bde("Veilande's Brigade", "Gén. de Brigade Veilande", [pf_regiment("34e", 2), pf_regiment("88e", 2)]),
               pf_bde("Pepin's Brigade", "Gén. de Brigade Pepin", [pf_regiment("40e", 2), pf_regiment("64e", 3)]),
               pf_battery("Foot Battery")],
              command=[cmd("pf-div-cmd", "Gén. de Division Girard")]),
        force("albuera-gazan", PF, "Gazan's Division", "2nd Division, V Corps", "French",
              "Followed Girard's division onto the hill in support, packed in behind it and unable to deploy, and suffered as badly when the attack broke.",
              [pf_bde("Maransin's Brigade", "Gén. de Brigade Maransin", [pf_regiment("21e", 2, "Léger"), pf_regiment("100e", 2)]),
               pf_bde("Brayer's Brigade", "Gén. de Brigade Brayer", [pf_regiment("28e", 3, "Léger"), pf_regiment("103e", 3)]),
               pf_battery("Foot Battery")],
              command=[cmd("pf-div-cmd", "Gén. de Division Gazan")],
        ),
        force("albuera-werle", PF, "Werlé, Godinot and the Grenadiers", "Soult's reserve and the attack on the village", "French",
              "Godinot made the feint on Albuera village; Werlé's big brigade, Soult's last reserve, went in against Cole's Fusiliers and was driven off the hill with them.",
              [pf_bde("Werlé's Brigade", "Gén. de Brigade Werlé", [pf_regiment("12e", 3, "Léger"), pf_regiment("55e", 3), pf_regiment("58e", 3)]),
               pf_bde("Godinot's Brigade", "Gén. de Brigade Godinot", [pf_regiment("16e", 3, "Léger"), pf_regiment("51e", 3)]),
               bde("pf-reserve-infantry-brigade", "Combined Grenadiers", "",
                   [u("pf-combined-grenadier", "Combined Grenadiers (45e, 63e)"), u("pf-combined-grenadier", "Combined Grenadiers (95e, 4th Vistula)")]),
               pf_battery("Foot Battery")],
              command=[cmd("pf-div-cmd", "Marshal Soult")],
              notes=["The grenadier companies of four regiments, about 1,000 men, are shown as two Combined Grenadier battalions.",
                     "Soult commanded the army; he leads this force as its Divisional Commander, the book having no named Soult."]),
        force("albuera-latour-maubourg", PF, "Latour-Maubourg's Cavalry", "Armée du Midi", "French",
              "Over 4,000 horsemen on the open plain. The Vistula Lancers and 2nd Hussars rode down Colborne's brigade in the hailstorm and took its colours.",
              [pf_cav("Briche's Brigade", "Gén. de Brigade Briche", [("2e", "Hussards"), ("10e", "Hussards"), ("21e", "Chasseurs")]),
               pf_cav("Bron's Brigade", "Gén. de Brigade Bron", [("4e", "Dragons"), ("20e", "Dragons"), ("26e", "Dragons")]),
               pf_cav("Bouvier des Éclaz's Brigade", "Gén. de Brigade Bouvier des Éclaz", [("14e", "Dragons"), ("17e", "Dragons"), ("27e", "Dragons")]),
               pf_cav("Lancers and Chasseurs", "", [("1st Vistula", "Lanciers"), ("27e", "Chasseurs"), ("4e Spanish", "Chasseurs")]),
               pf_battery("Horse Battery", "pf-horse-arty"), pf_battery("Horse Battery", "pf-horse-arty")],
              command=[cmd("pf-div-cmd", "Gén. de Division Latour-Maubourg")],
              notes=["Four brigades where the list takes three, and no infantry brigades for the cavalry to go with, show as historical departures. The unbrigaded Vistula Lancers, 27th Chasseurs and 4th Spanish Chasseurs are grouped as a fourth brigade."]),
    ],
}

# Periods: 1808 is the lists' Early period, 1811 their Middle
for f in ROLICA["forces"] + VIMEIRO["forces"]:
    f["period"] = "early"
for f in ALBUERA["forces"]:
    f["period"] = "middle"


if __name__ == "__main__":
    for b in (ROLICA, VIMEIRO, ALBUERA):
        ratings.apply(b)
        if b["id"] in ART:
            b["art"] = ART[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
