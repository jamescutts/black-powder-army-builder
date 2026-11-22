"""
Writes the forces of the War of Liberation (src/data/battles/{mockern,lutzen,bautzen,grossbeeren,katzbach,hagelberg,plagwitz,dennewitz,wartenburg,hanau}.json):
the French, their German and Italian allies, and the Russians, from Nafziger's orders of battle. The Prussians
are built from the 1815 Prussian list, one force a corps.

    python3 scripts/forces/liberation_1813.py && npm run check:forces

There are no 1813 army lists, so every force borrows the nearest: A Clash of Eagles' 1812 lists for the French,
the Imperial Guard, the Confederation of the Rhine, Italy, Saxony and Russia (whose list covers 1812-15). Each
force's notes say so. Summaries are our own words. Staff Ratings are set by ratings.py.
"""

import copy
import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
ART = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
NAF = "https://www.napoleon-series.org/nafzigger/"
FR, IT, CR, FIG, SAX, RU = "france", "italy", "confederation-of-the-rhine", "french-imperial-guard", "saxony", "russia"
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


def battle(id_, name, date, summary, sources, forces, prussians, alliances=(("Russian", "Prussian"),)):
    b = {"id": id_, "name": name, "date": date, "campaign": "liberation-1813", "summary": summary,
         "sources": sources, "forces": forces, "toCome": prussians, "alliances": [list(a) for a in alliances]}
    # A battle with nothing still to come, or no allies fighting apart, leaves those out
    return {k: v for k, v in b.items() if v or k not in ("toCome", "alliances")}


def write(b):
    ratings.apply(b)
    commanders.apply(b)
    if b["id"] in ART:
        b["art"] = ART[b["id"]]
    # Keep the file's keys in the order the others have them
    order = ["id", "name", "date", "campaign", "art", "sides", "alliances", "summary", "sources", "forces", "toCome"]
    out = {k: b[k] for k in order if k in b}
    (OUT / f"{b['id']}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(f"{b['name']}: {len(b['forces'])} forces, {len(b.get('toCome', []))} to come")


# ================================================================ The Prussians, from the 1815 list

PR15 = "prussians-1815"
M, F_, LW = "pr15-musketeer", "pr15-fusilier", "pr15-landwehr"
KIND = {"M": M, "F": F_, "L": LW}
PR_LIST = ("Built from Albion Triumphant's Prussian 1815 list, the nearest to 1813: its Prussian Infantry Brigade is the "
           "1813 brigade, the size of another army's division, with line, reserve and Landwehr battalions.")
PR_WHOLE = "A Prussian brigade was the size of another army's division, so the whole corps is here. Take the brigades you want; each is a force in itself."
PR_GROUPED = ("Battalions of different regiments that served together are grouped as a regiment, as the list takes them. "
              "Reserve battalions are the list's Musketeers; grenadier battalions are Musketeers with its Veteran upgrade.")
PR_GUARD_VETERAN = ("The Guard takes the list's Veteran upgrades: the Guard Infantry and the Normal Battalion, the Garde du Corps and "
                    "Guard Light Cavalry, and the Guard foot and horse batteries. The Guard Jäger, as Schützen, have none to take. Both of Werder's "
                    "regiments Veteran, where the list allows half a brigade's, shows as a historical departure.")
PR_SUB = "Brigades of three regiments or more have a Subordinate Commander, named where the order of battle names the brigade's infantry commander."
PR_SPRING = ("In the spring of 1813 the brigades had no Landwehr yet: each was two line regiments, with grenadier, reserve and "
             "Jäger battalions besides, so most have more line regiments, or more battalions in a regiment, than the list's brigade "
             "takes, which shows as historical departures.")
CUIRASSIERS = ("The list has no cuirassiers or Guard cavalry: the Garde du Corps and the East Prussian, Silesian and Brandenburg "
               "Cuirassiers are its Dragoons, its only heavy cavalry, and the Guard Light Cavalry its Hussars. Jürgass's three cuirassier "
               "regiments, where the list's brigade takes two Dragoons, show as a historical departure.")
GUARD = ("The list has no Guard: the Guard Infantry Regiment and the Normal Battalion are Musketeers and Fusiliers, and the Guard "
         "Jäger and Wedell's Guard Volunteer Jäger are the list's attached Schützen, its only Jäger battalion a brigade takes; with the Silesian Schützen, "
         "three where the list allows one in the army, they show as historical departures.")
PR_CAVALRY = ("More cavalry brigades than the list allows for the infantry, and brigades of two-squadron regiments, show as historical departures; "
              "regiments of two or three squadrons are shown at full size.")
PR_ARTY = ("Batteries beyond the one each brigade takes are in the corps artillery, as the list's reserve takes them; more than it allows, "
           "or a reserve horse battery with fewer brigades than the list wants for it, show as historical departures.")


def bn(kind, name):
    """A Prussian battalion; a grenadier or Guard battalion with the list's Veteran upgrade"""
    elite = "Grenadier" in name or "Guard" in name or name.startswith("Normal")
    return u(KIND[kind], name, **({"options": ["veteran-infantry"]} if elite else {}))


def pi(name, commander, regiments, units=(), sub=None):
    """A Prussian infantry brigade: regiments as (name, [(kind, battalion)]), with a Subordinate Commander when it has three or more"""
    extra = [u("pr15-sub-cmd", sub)] if len(regiments) >= 3 else []
    return bde("pr15-infantry-brigade", name, commander, units=extra + list(units),
               regiments=[regt(r, [bn(k, b) for k, b in bns_]) for r, bns_ in regiments])


def pc(name, commander, units, landwehr=False):
    return bde("pr15-landwehr-cavalry-brigade" if landwehr else "pr15-cavalry-brigade", name, commander, units=list(units))


def pres(*units):
    return bde("pr15-army-reserve-artillery", "Corps Artillery", units=list(units))


HALF = {"options": ["half-battery"]}
RUSSIAN_BATTERIES = "Russian batteries lent to the brigades, which a force from the Prussian list can't take."

# --- Möckern: Yorck's corps and Bülow's, after Nafziger's returns for April (813DBJ, 813DCA)

MK_PR_YORCK = {"label": "Prussian Corps, Generallieutenant Yorck, April–May 1813 (Nafziger Collection 813DBJ)", "url": NAF + "813DBJ.pdf"}
MK_PR_ARMY = {"label": "Prussian Army, 1 April 1813 (Nafziger Collection 813DCA)", "url": NAF + "813DCA.pdf"}
MK_PR_NOTE = "After Nafziger's returns for April; he has no order of battle for Möckern itself."

MK_YORCK = force(
    "mockern-yorck", PR15, "Yorck's Corps", "Prussian corps, with Wittgenstein", "Prussian",
    "The old Prussian auxiliary corps of 1812. Its advance guard under Hünerbein, three East Prussian battalions with hussars, dragoons, Cossacks and twelve guns, stormed Dannigkow and held it against Lagrange's counter-attacks; the rest of the corps stood at Leitzkau.",
    [pi("1st Brigade (Hünerbein)", "Gen-Maj von Hünerbein",
        [("1st East Prussian Infantry", [("M", "I/1st East Prussian Infantry"), ("M", "II/1st East Prussian Infantry"), ("F", "F/1st East Prussian Infantry")]),
         ("Colberg Infantry", [("M", "I/Colberg Infantry"), ("M", "II/Colberg Infantry"), ("F", "F/Colberg Infantry")]),
         ("Leib Infantry", [("F", "F/Leib Infantry")])],
        [u("pr15-foot-arty", "6-pdr Foot Battery #1")]),
     pi("2nd Brigade (Horn)", "Col von Horn",
        [("5th Combined Infantry", [("M", "I/1st West Prussian Infantry"), ("M", "II/2nd West Prussian Infantry"), ("F", "F/2nd West Prussian Infantry")]),
         ("6th Combined Infantry", [("M", "II/1st Silesian Infantry"), ("M", "II/2nd Silesian Infantry"), ("F", "F/2nd Silesian Infantry")])],
        [u("pr15-foot-arty", "6-pdr Foot Battery #2")]),
     pc("Corps Cavalry", "", [u("pr15-dragoon", "Lithuanian Dragoons"), u("pr15-dragoon", "2nd Combined Dragoons"),
                              u("pr15-hussar", "2nd Leib Hussars"), u("pr15-horse-arty", "6-pdr Horse Battery #2")]),
     pres(u("pr15-heavy-arty", "½ 12-pdr Battery #3", **HALF), u("pr15-foot-arty", "½ 3-pdr Battery #1", **HALF),
          u("pr15-horse-arty", "6-pdr Horse Battery #3"))],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Yorck")],
    notes=[PR_LIST, MK_PR_NOTE, PR_WHOLE, PR_SPRING, PR_GROUPED, PR_SUB,
           "The Leib Regiment's fusilier battalion, a regiment of its own in Hünerbein's brigade, shows as a historical departure.",
           "The brigades' cavalry is together as the corps cavalry: the Lithuanian Dragoons and the 2nd Leib Hussars' two halves from Hünerbein, the combined dragoons from Horn. The 2nd Combined Dragoons were two squadrons each of the 1st West Prussian and Brandenburg Dragoons.",
           "The half 3-pdr battery is the list's Foot Artillery, as a half battery.", PR_ARTY])

MK_BULOW = force(
    "mockern-bulow", PR15, "Bülow's Corps", "Borstell's brigade and Oppen's cavalry", "Prussian",
    "Borstell's Pomeranian and East Prussian battalions, with the Queen's Dragoons, which took Vehlitz and the Windmühlenberg with Berg's Russians; and Oppen's cavalry, the 'mad' Major von Platen's dragoons and the Leib Hussars, which routed the French horse at Zeddenick.",
    [pi("Pomeranian Brigade (Borstell)", "Gen-Maj von Borstell",
        [("1st Pomeranian Infantry", [("M", "I/1st Pomeranian Infantry"), ("M", "II/1st Pomeranian Infantry")]),
         ("Pomeranian Grenadiers and East Prussian Fusiliers", [("M", "Pomeranian Grenadier Battalion"), ("F", "F/4th East Prussian Infantry")])],
        [u("pr15-foot-arty", "6-pdr Foot Battery #10")]),
     pc("Oppen's Cavalry", "Gen-Maj von Oppen",
        [u("pr15-dragoon", "Queen's Dragoons"), u("pr15-dragoon", "2nd West Prussian Dragoons"), u("pr15-hussar", "1st Leib Hussars"),
         u("pr15-horse-arty", "6-pdr Horse Battery #6")]),
     pres(u("pr15-horse-arty", "Horse Battery #11"))],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Bülow")],
    notes=[PR_LIST, MK_PR_NOTE,
           "Only Borstell's brigade and Oppen's cavalry fought at Möckern; Hesse-Homburg's and Clausewitz's brigades of Bülow's corps are left out. The Queen's Dragoons, Borstell's own, ride with Oppen's regiments here.",
           PR_GROUPED,
           "Borstell's horse battery is in the corps artillery, as the list takes it.",
           "In April 1813 the brigade had no Landwehr yet, which the list's brigade wants; that, Oppen's cavalry brigade with only one infantry brigade to allow it, and a reserve horse battery with too few brigades, show as historical departures."])

# --- Lützen and Bautzen: Blücher's corps and Yorck's, after Nafziger (813ECD, 813ECE, from Plotho)

LZ_PR_NOTE = "After Nafziger's order of battle for Lützen, from Plotho."
BZ_PR_NOTE = "After Nafziger's order of battle for Bautzen, from Plotho."
DOLFFS = [
    pc("Reserve Cavalry (Werder)", "Lt-Col von Werder",
       [u("pr15-dragoon", "Garde du Corps", options=["veteran-cavalry"]), u("pr15-hussar", "Guard Light Cavalry", options=["veteran-cavalry"]),
        u("pr15-horse-arty", "Guard Horse Battery #4", options=["veteran-artillery"])]),
    pc("Reserve Cavalry (Jürgass)", "Col von Jürgass",
       [u("pr15-dragoon", "East Prussian Cuirassiers"), u("pr15-dragoon", "Silesian Cuirassiers"),
        u("pr15-dragoon", "Brandenburg Cuirassiers"), u("pr15-horse-arty", "Horse Battery #10")]),
]
ZIETEN_CAV = pc("Upper Silesian Cavalry (Laroche)", "Maj Laroche von Starkenfeld",
                [u("pr15-hussar", "1st Silesian Hussars (2 squadrons)"), u("pr15-hussar", "2nd Silesian Hussars (2 squadrons)"),
                 u("pr15-uhlan", "Silesian Uhlans (2 squadrons)"), u("pr15-horse-arty", "Horse Battery #9")])
KLUX_CAV = pc("Lower Silesian Cavalry (Mutius)", "Col von Mutius",
              [u("pr15-dragoon", "Neumark Dragoons"), u("pr15-dragoon", "1st West Prussian Dragoons (2 squadrons)"),
               u("pr15-horse-arty", "Horse Battery #7")])

LZ_BLUCHER = force(
    "lutzen-blucher", PR15, "Blücher's Corps", "Zieten's, Klüx's and Röder's brigades, with Dolffs's cavalry", "Prussian",
    "The Silesian brigades of Zieten and Klüx, which opened the attack on Gross-Görschen and fought for the villages all afternoon; Röder's Brandenburg brigade with the Guard infantry, which stormed Klein-Görschen and Kaja; and Dolffs's Garde du Corps and cuirassiers, which charged the French squares at dusk, Dolffs killed.",
    [pi("Upper Silesian Brigade (Zieten)", "Gen-Maj von Zieten",
        [("1st Silesian Infantry", [("M", "I/1st Silesian Infantry"), ("M", "III/1st Silesian Infantry"), ("F", "F/1st Silesian Infantry")]),
         ("2nd Silesian Infantry", [("M", "I/2nd Silesian Infantry"), ("M", "III/2nd Silesian Infantry")]),
         ("Silesian Grenadiers", [("M", "Silesian Grenadier Battalion")])],
        [u("pr15-schutzen", "Silesian Schützen Battalion"), u("pr15-foot-arty", "6-pdr Foot Battery #11")], sub="Col von Pirch"),
     ZIETEN_CAV,
     pi("Lower Silesian Brigade (Klüx)", "Col von Klüx",
        [("1st West Prussian Infantry", [("M", "II/1st West Prussian Infantry"), ("M", "III/1st West Prussian Infantry"), ("F", "F/1st West Prussian Infantry")]),
         ("2nd West Prussian Infantry", [("M", "II/2nd West Prussian Infantry"), ("M", "III/2nd West Prussian Infantry")]),
         ("West Prussian Grenadiers", [("M", "West Prussian Grenadier Battalion")])],
        [u("pr15-foot-arty", "6-pdr Foot Battery #7")], sub="Maj von Jagow"),
     KLUX_CAV,
     pi("Brandenburg Brigade (Röder)", "Gen-Maj von Röder",
        [("Guard Infantry", [("M", "I/Guard Infantry"), ("M", "II/Guard Infantry"), ("F", "F/Guard Infantry")]),
         ("Leib Infantry and Normal Battalion", [("M", "III/Leib Infantry"), ("M", "Normal Infantry Battalion")]),
         ("Grenadier Battalions", [("M", "Leib Grenadier Battalion"), ("M", "1st East Prussian Grenadier Battalion")])],
        [u("pr15-schutzen", "Guard Jäger Battalion"), u("pr15-schutzen", "Guard Volunteer Jäger Battalion (Wedell)"),
         u("pr15-foot-arty", "Guard 6-pdr Foot Battery #4", options=["veteran-artillery"])], sub="Lt-Col von Tippelskirch"),
     pc("Brandenburg Cavalry (Katzler)", "Lt-Col von Katzler",
        [u("pr15-uhlan", "West Prussian Uhlans"), u("pr15-hussar", "Brandenburg Hussars (2 squadrons)"), u("pr15-horse-arty", "Horse Battery #8")]),
     *DOLFFS,
     pres(u("pr15-heavy-arty", "½ 12-pdr Foot Battery #3", **HALF), u("pr15-foot-arty", "6-pdr Foot Battery #13"),
          u("pr15-foot-arty", "6-pdr Foot Battery #9"))],
    command=[{"unit": "pr15-cmd-blucher"}],
    notes=[PR_LIST, LZ_PR_NOTE, "Blücher is the book's named commander.", PR_WHOLE, PR_SPRING, PR_GROUPED, PR_SUB, GUARD, PR_GUARD_VETERAN, CUIRASSIERS,
           "The Silesian Schützen are the list's attached Schützen battalion.", PR_CAVALRY, PR_ARTY])
LZ_BLUCHER["missing"] = [{"name": "Russian Position Batteries #1, #14 and #33", "reason": RUSSIAN_BATTERIES}]

LZ_YORCK = force(
    "lutzen-yorck", PR15, "Yorck's Corps", "Hünerbein's and Horn's brigades, with Steinmetz's reserve", "Prussian",
    "The old Prussian auxiliary corps of 1812, the left of Yorck's second line beside Berg's Russians, which came up in the afternoon and fought for Kaja.",
    [pi("Hünerbein's Brigade", "Gen-Maj von Hünerbein",
        [("1st Combined Infantry", [("M", "II/1st East Prussian Infantry"), ("M", "I/2nd East Prussian Infantry"), ("F", "F/1st East Prussian Infantry")]),
         ("Leib Infantry", [("F", "F/Leib Infantry")])],
        [u("pr15-foot-arty", "6-pdr Foot Battery #1")]),
     pi("Horn's Brigade", "Col von Horn",
        [("5th Combined Infantry", [("M", "I/1st West Prussian Infantry"), ("M", "II/2nd West Prussian Infantry"), ("F", "F/2nd West Prussian Infantry")]),
         ("6th Combined Infantry", [("M", "II/1st Silesian Infantry"), ("M", "II/2nd Silesian Infantry"), ("F", "F/2nd Silesian Infantry")])],
        [u("pr15-foot-arty", "6-pdr Foot Battery #2")]),
     pi("Reserve (Steinmetz)", "Lt-Col von Steinmetz",
        [("Colberg Infantry", [("M", "I/Colberg Infantry"), ("M", "II/Colberg Infantry"), ("F", "F/Colberg Infantry")])],
        [u("pr15-hussar-attached", "2nd Leib Hussars")]),
     pc("Corps Cavalry", "", [u("pr15-dragoon", "Lithuanian Dragoons"), u("pr15-dragoon", "2nd Combined Dragoons"),
                              u("pr15-horse-arty", "6-pdr Horse Battery #2")]),
     pres(u("pr15-heavy-arty", "½ 12-pdr Battery #3", **HALF), u("pr15-foot-arty", "½ 6-pdr Foot Battery #3", **HALF))],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Yorck")],
    notes=[PR_LIST, LZ_PR_NOTE, PR_WHOLE, PR_SPRING, PR_GROUPED,
           "The Leib Regiment's fusilier battalion, a regiment of its own in Hünerbein's brigade, and Steinmetz's reserve of the one Colberg Regiment, where the list's brigade wants two, show as historical departures.",
           "The Lithuanian Dragoons from Hünerbein and the 2nd Combined Dragoons (two squadrons each of the 1st West Prussian and Brandenburg Dragoons) from Horn are together as the corps cavalry, with Steinmetz's horse battery; the 2nd Leib Hussars are Steinmetz's attached hussars.",
           "The East Prussian Jäger were detached to Kleist.", PR_ARTY])
LZ_YORCK["missing"] = [{"name": "3-pdr Foot Battery #1", "reason": "A battery of light 3-pdrs with Steinmetz's reserve; the corps artillery's one foot battery is the half of #3."}]

BZ_KLEIST = force(
    "bautzen-kleist", PR15, "Kleist's Corps", "Prussian advance guard, with Russian Jäger", "Prussian",
    "Kleist's Prussians, the Colberg Regiment and Silesian hussars, with Russian Jäger and Cossacks, which retook Preititz from Ney before withdrawing.",
    [pi("Steinmetz's Brigade", "Lt-Col von Steinmetz",
        [("Colberg Infantry", [("M", "I/Colberg Infantry"), ("M", "II/Colberg Infantry"), ("F", "F/Colberg Infantry")])],
        [u("pr15-hussar-attached", "3rd Combined Hussars (Thümen)")]),
     pres(u("pr15-horse-arty", "Horse Battery #3"))],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Kleist")],
    notes=[PR_LIST, BZ_PR_NOTE,
           "Only Kleist's Prussians are here: the Colberg Regiment, the 3rd Combined Hussars (two squadrons each of the 1st and 2nd Silesian Hussars) as its attached hussars, and Horse Battery #3 in the corps artillery. One regiment, where the list's brigade wants two, no Landwehr, which the spring brigades didn't yet have, and a reserve horse battery with too few brigades show as historical departures."])
BZ_KLEIST["missing"] = [{"name": "Rüdiger's, Vlastov's, Roth's and Rodionov's Russians",
                         "reason": "The Grodno Hussars, the 23rd to 26th Jäger, Horse Battery #23 and three Don Cossack regiments were Russian, which a force from the Prussian list can't take."}]

BZ_BLUCHER = force(
    "bautzen-blucher", PR15, "Blücher's Corps", "Zieten's, Klüx's and Röder's brigades, with Dolffs's cavalry", "Prussian",
    "Blücher's Silesian and Brandenburg brigades on the Kreckwitz heights, nearly cut off when Ney reached Preititz.",
    [pi("Upper Silesian Brigade (Zieten)", "Gen-Maj von Zieten",
        [("1st Silesian Infantry", [("M", "I/1st Silesian Infantry"), ("M", "III/1st Silesian Infantry"), ("F", "F/1st Silesian Infantry")]),
         ("2nd Silesian Infantry", [("M", "I/2nd Silesian Infantry"), ("M", "III/2nd Silesian Infantry")]),
         ("Silesian Grenadiers and Leib Reserve", [("M", "Silesian Grenadier Battalion"), ("M", "3rd Reserve Battalion, Leib Infantry"), ("M", "5th Reserve Battalion, Leib Infantry")])],
        [u("pr15-schutzen", "Silesian Schützen Battalion"), u("pr15-foot-arty", "6-pdr Foot Battery #8")], sub="Col von Pirch"),
     ZIETEN_CAV,
     pi("Lower Silesian Brigade (Klüx)", "Col von Klüx",
        [("1st West Prussian Infantry", [("M", "II/1st West Prussian Infantry"), ("M", "III/1st West Prussian Infantry"), ("F", "F/1st West Prussian Infantry")]),
         ("West Prussian and Leib Reserve", [("M", "II/2nd West Prussian Infantry"), ("M", "III/3rd West Prussian Infantry"), ("M", "2nd Reserve Battalion, Leib Infantry")]),
         ("West Prussian Grenadiers", [("M", "West Prussian Grenadier Battalion")])],
        [u("pr15-foot-arty", "6-pdr Foot Battery #9")], sub="Maj von Jagow"),
     KLUX_CAV,
     pi("Brandenburg Brigade (Röder)", "Gen-Maj von Röder",
        [("Guard Infantry", [("M", "I/Guard Infantry"), ("M", "II/Guard Infantry"), ("F", "F/Guard Infantry")]),
         ("Leib Infantry and Normal Battalion", [("M", "III/Leib Infantry"), ("M", "1st Reserve Battalion, Leib Infantry"), ("M", "Normal Infantry Battalion")]),
         ("Grenadier Battalions", [("M", "Leib Grenadier Battalion"), ("M", "1st East Prussian Grenadier Battalion")])],
        [u("pr15-schutzen", "Guard Jäger Battalion"), u("pr15-schutzen", "Guard Volunteer Jäger Battalion (Wedell)"),
         u("pr15-foot-arty", "Guard Foot Battery #4", options=["veteran-artillery"])], sub="Lt-Col von Tippelskirch"),
     pc("Brandenburg Cavalry (Katzler)", "Lt-Col von Katzler",
        [u("pr15-uhlan", "West Prussian Uhlans"), u("pr15-hussar", "Brandenburg Hussars (2 squadrons)"),
         u("pr15-hussar", "2nd Leib Hussars"), u("pr15-horse-arty", "Horse Battery #8")]),
     *DOLFFS,
     pres(u("pr15-foot-arty", "6-pdr Foot Battery #13"))],
    command=[{"unit": "pr15-cmd-blucher"}],
    notes=[PR_LIST, BZ_PR_NOTE, "Blücher is the book's named commander.", PR_WHOLE, PR_SPRING, PR_GROUPED, PR_SUB, GUARD, PR_GUARD_VETERAN, CUIRASSIERS,
           "Nafziger lists the 3rd Reserve Battalion of the Leib Regiment with both Zieten and Klüx; it is shown once, with Zieten. His '3/3rd West Prussian' is shown as he gives it.",
           "Hobe's 2nd Leib Hussars and Brandenburg Hussars ride with Katzler's uhlans as one brigade; the two squadrons of Brandenburg Uhlans, not in the battle, are left out.",
           "The Silesian Schützen are the list's attached Schützen battalion.", PR_CAVALRY, PR_ARTY])
BZ_BLUCHER["missing"] = [{"name": "Russian Position Batteries #14 and #33", "reason": RUSSIAN_BATTERIES}]

BZ_YORCK = force(
    "bautzen-yorck", PR15, "Yorck's Corps", "Zielinsky's and Horn's brigades", "Prussian",
    "Sent from the centre to help Blücher hold the heights against Bertrand and Marmont.",
    [pi("Zielinsky's Brigade", "Col von Zielinsky",
        [("1st East Prussian Infantry", [("M", "I/1st East Prussian Infantry"), ("M", "II/1st East Prussian Infantry"), ("F", "Combined Fusiliers, 1st East Prussian and Leib")]),
         ("Leib Infantry", [("M", "I/Leib Infantry"), ("M", "II/Leib Infantry"), ("F", "F/2nd East Prussian Infantry")])],
        [u("pr15-foot-arty", "6-pdr Foot Battery #1")]),
     pi("Horn's Brigade", "Col von Horn",
        [("5th Combined Infantry", [("M", "I/1st West Prussian Infantry"), ("M", "II/2nd West Prussian Infantry"), ("F", "Combined Fusiliers, 5th and 6th Combined")]),
         ("6th Combined Infantry", [("M", "II/1st Silesian Infantry"), ("M", "II/2nd Silesian Infantry")])],
        [u("pr15-foot-arty", "6-pdr Foot Battery #3")]),
     pc("Corps Cavalry (Wuthenow)", "Lt-Col von Wuthenow",
        [u("pr15-dragoon", "Lithuanian Dragoons"), u("pr15-dragoon", "1st West Prussian Dragoons (2 squadrons)"),
         u("pr15-dragoon", "Brandenburg Dragoons (2 squadrons)"), u("pr15-horse-arty", "6-pdr Horse Battery #2")]),
     pres(u("pr15-foot-arty", "6-pdr Foot Battery #2"), u("pr15-horse-arty", "6-pdr Horse Battery #1"))],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Yorck")],
    notes=[PR_LIST, BZ_PR_NOTE, PR_WHOLE, PR_GROUPED,
           "Corswandt's right wing: Wuthenow's dragoons, with the Lithuanian and Brandenburg Dragoons attached to Horn, are together as the corps cavalry; three dragoon regiments, where the list allows two, show as a historical departure.",
           "Zielinsky's second battery and Horn's horse battery are in the corps artillery.", PR_SPRING, PR_ARTY])
BZ_YORCK["missing"] = [{"name": "3-pdr Foot Battery #1", "reason": "A battery of light 3-pdrs with Horn's brigade, which takes one battery; the corps artillery's foot battery is #2."}]

# --- Großbeeren: Bülow's III Corps, after Nafziger (813HGE)

GB_BULOW = force(
    "grossbeeren-bulow", PR15, "Bülow's Corps", "III Corps: Hesse-Homburg's, Thümen's, Borstell's and Krafft's brigades, with Oppen's cavalry", "Prussian",
    "Four brigades of line, reserve and Landwehr infantry, each with its cavalry and battery, which stormed Großbeeren at six in the evening behind sixty-four guns, two of their batteries Russian 12-pdrs; the 4th Reserve Regiment fought in the village with musket butts. Borstell's brigade came in on the Saxons' flank from Kleinbeeren, and Oppen's dragoons, hussars and Landwehr cavalry rode down the rearguard in the dark.",
    [pi("3rd Brigade (Hesse-Homburg)", "Gen-Maj Prince Ludwig of Hesse-Homburg",
        [("3rd East Prussian Infantry", [("M", "2nd East Prussian Grenadier Battalion"), ("M", "I/3rd East Prussian Infantry"), ("M", "II/3rd East Prussian Infantry"), ("F", "F/3rd East Prussian Infantry")]),
         ("4th Reserve Infantry", [("M", "I/4th Reserve Infantry"), ("M", "II/4th Reserve Infantry"), ("M", "III/4th Reserve Infantry")]),
         ("3rd East Prussian Landwehr", [("L", "8th Bn, 3rd East Prussian Landwehr"), ("L", "11th Bn, 3rd East Prussian Landwehr"),
                                         ("L", "12th Bn, 3rd East Prussian Landwehr"), ("L", "20th Bn, 3rd East Prussian Landwehr")])],
        [u("pr15-hussar-attached", "1st Leib Hussars"), u("pr15-foot-arty", "6-pdr Foot Battery #5")]),
     pi("4th Brigade (Thümen)", "Gen-Maj von Thümen",
        [("4th East Prussian Infantry", [("M", "I/4th East Prussian Infantry"), ("M", "II/4th East Prussian Infantry"), ("F", "F/4th East Prussian Infantry")]),
         ("5th Reserve Infantry", [("M", "I/5th Reserve Infantry"), ("M", "II/5th Reserve Infantry"), ("M", "III/5th Reserve Infantry"), ("M", "IV/5th Reserve Infantry")]),
         ("Elbe Infantry", [("M", "I/Elbe Infantry"), ("M", "II/Elbe Infantry")])],
        [u("pr15-jager-coy", "2nd Company, East Prussian Jäger"), u("pr15-jager-coy", "4th Company, East Prussian Jäger"),
         u("pr15-hussar-attached", "Pomeranian National Cavalry"), u("pr15-foot-arty", "6-pdr Foot Battery #6")]),
     pi("5th Brigade (Borstell)", "Gen-Maj von Borstell",
        [("1st Pomeranian Infantry", [("M", "Pomeranian Grenadier Battalion"), ("M", "I/1st Pomeranian Infantry"), ("M", "II/1st Pomeranian Infantry"), ("F", "F/1st Pomeranian Infantry")]),
         ("2nd Reserve Infantry", [("M", "I/2nd Reserve Infantry"), ("M", "II/2nd Reserve Infantry"), ("M", "III/2nd Reserve Infantry")]),
         ("2nd Kurmark Landwehr", [("L", "II/2nd Kurmark Landwehr"), ("L", "IV/2nd Kurmark Landwehr")])],
        [u("pr15-foot-arty", "6-pdr Foot Battery #10")]),
     pc("5th Brigade Cavalry", "", [u("pr15-hussar", "Pomeranian Hussars"), u("pr15-uhlan", "West Prussian Uhlans")]),
     pi("6th Brigade (Krafft)", "Gen-Maj von Krafft",
        [("Colberg Infantry", [("M", "I/Colberg Infantry"), ("M", "II/Colberg Infantry"), ("F", "F/Colberg Infantry")]),
         ("9th Reserve Infantry", [("M", "I/9th Reserve Infantry"), ("M", "II/9th Reserve Infantry"), ("M", "III/9th Reserve Infantry")]),
         ("1st Neumark Landwehr", [("L", "I/1st Neumark Landwehr"), ("L", "II/1st Neumark Landwehr"), ("L", "III/1st Neumark Landwehr"), ("L", "IV/1st Neumark Landwehr")])],
        [u("pr15-mounted-landwehr-attached", "1st Pomeranian Landwehr Cavalry"), u("pr15-foot-arty", "6-pdr Foot Battery #16")]),
     pc("Reserve Cavalry (Oppen)", "Gen-Maj von Oppen",
        [u("pr15-dragoon", "Queen's Dragoons"), u("pr15-dragoon", "Brandenburg Dragoons"), u("pr15-dragoon", "2nd West Prussian Dragoons"),
         u("pr15-hussar", "2nd Silesian Hussars (2 squadrons)"), u("pr15-horse-arty", "Horse Battery #5")]),
     pc("Reserve Cavalry (Oppen, Landwehr)", "Gen-Maj von Oppen",
        [u("pr15-mounted-landwehr", "2nd Kurmark Landwehr Cavalry"), u("pr15-mounted-landwehr", "4th Kurmark Landwehr Cavalry"),
         u("pr15-horse-arty", "Horse Battery #6")], landwehr=True),
     pres(u("pr15-heavy-arty", "12-pdr Foot Battery #4"), u("pr15-heavy-arty", "12-pdr Foot Battery #5"), u("pr15-foot-arty", "6-pdr Foot Battery #19"))],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Bülow")],
    notes=[PR_LIST, "After Nafziger's order of battle for Großbeeren.", PR_WHOLE, PR_GROUPED, PR_SUB,
           "Each brigade's grenadier battalion is with its first line regiment. Thümen's brigade had no Landwehr, which the list's brigade wants. Reserve regiments of three or four battalions, Landwehr regiments of four, and line regiments of three or more musketeer battalions show as historical departures.",
           "The Pomeranian National Cavalry, a volunteer regiment, is Thümen's attached hussars; two attached hussar regiments in the corps, where the list allows one, show as a historical departure.",
           "Borstell's Pomeranian Hussars and West Prussian Uhlans are a cavalry brigade of their own. Three dragoon regiments in Oppen's brigade, line and Landwehr cavalry brigades together, and more cavalry brigades than the infantry allows show as historical departures.",
           "Two 12-pdr batteries, where the corps artillery takes one, show as a historical departure."])
GB_BULOW["missing"] = [{"name": "Russian 12-pdr Batteries #7 and #21", "reason": "Two Russian position batteries in Bülow's artillery reserve, which a force from the Prussian list can't take."}]


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
    [APRIL, MK_PR_YORCK, MK_PR_ARMY,
     {"label": "Battle of Möckern (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_M%C3%B6ckern"},
     {"label": "Gefecht bei Möckern (German Wikipedia)", "url": "https://de.wikipedia.org/wiki/Gefecht_bei_M%C3%B6ckern"}],
    [MK_LAGRANGE, MK_ZUCCHI, MK_CAVALRY, MK_ROTH, MK_YORCK, MK_BULOW],
    [])


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
    [LZ_SOUHAM, LZ_BRENIER, LZ_GIRARD, LZ_RICARD, LZ_MARCHAND, LZ_DUMOUSTIER, LZ_BERG, LZ_EUGEN, LZ_BLUCHER, LZ_YORCK],
    [])


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
    [BZ_SOUHAM, BZ_DELMAS, BZ_MAISON, BZ_PUTHOD, BZ_CHAPLITZ, BZ_SHCHERBATOV, BZ_INSOV, BZ_KLEIST, BZ_BLUCHER, BZ_YORCK],
    [])


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
    [GB_SAHR, GB_LECOQ, GB_GABLENZ, GB_DURUTTE, GB_BULOW],
    [],
    alliances=(("Saxon", "French"),))


# ================================================================ Wartenburg, 3 October 1813

WB_FR = {"label": "French Forces, Battle of Wartenberg, 3 October 1813 (Nafziger Collection 813JJB, after Mirus)", "url": NAF + "813JJB.pdf"}
WB_PR = {"label": "Prussian Forces, Battle of Wartenberg, 3 October 1813 (Nafziger Collection 813JJA, after Mirus)", "url": NAF + "813JJA.pdf"}
WB_IV = {"label": "French IV Corps, 20 September 1813 (Nafziger Collection 813IZL)", "url": NAF + "813IZL.pdf"}
WB_NOTE = "After Nafziger's order of battle for Wartenburg, from Mirus's history of the fight; its batteries are from his return of the IV Corps a fortnight before."
WT, WP = "wurttemberg", "westphalia"
WEAK = ("Bertrand's corps was worn down by Dennewitz: a fortnight before, its battalions averaged about four hundred men, "
        "and some Italian regiments were down to a few hundred. They are shown at full size; the list's Small upgrade would suit many of them.")

WB_MORAND = force(
    "wartenburg-morand", FR, "Morand's Division", "12th Division, IV Corps (Bertrand)", "French",
    "Bertrand's French division, posted in Wartenburg village and along the dike in front of it, which made a ready-made breastwork. It threw back Steinmetz's brigade, attacking straight across the open marshland, again and again, and only gave the village up when Horn's brigade came in on its flank.",
    [bde("fr-infantry-brigade", "Ligier-Belair's Brigade", "Gén. de Brigade Ligier-Belair", regiments=[light("8th Léger", 4)]),
     bde("fr-infantry-brigade", "Toussaint's Brigade", "Gén. de Brigade Toussaint",
         units=[u("fr-regimental-arty-section", "Artillery Company, 13th Line")], regiments=[line("13th Line", 4)]),
     bde("fr-infantry-brigade", "Hulot's Brigade", "Gén. de Brigade Hulot",
         units=[u("fr-regimental-arty-section", "Artillery Company, 23rd Line")],
         regiments=[regt("23rd Line", [u("fr-line-infantry", f"{b}/23rd Line") for b in ("1", "2", "4")])]),
     foot("1/2nd Foot Artillery", "3/2nd Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Morand")],
    notes=[LIST_FR, WB_NOTE, WEAK,
           "The 13th and 23rd Line still had their regimental artillery companies, each shown as a section of regimental guns.",
           TWO_BATTERIES])

WB_FONTANELLI = force(
    "wartenburg-fontanelli", IT, "Fontanelli's Division", "15th Division, IV Corps (Bertrand)", "French",
    "The Italians stood behind Morand round Wartenburg, and were coming up to support him when Horn's brigade, having waded through the backwaters and over the dikes, fell on them and turned the French line.",
    [bde("it-infantry-brigade", "Martel's Brigade", "Gén. de Brigade Martel",
         regiments=[regt("1st Italian Line", [u("it-line-infantry", "1st Italian Line")]),
                    regt("4th Italian Line", [u("it-line-infantry", "4th Italian Line")])]),
     bde("it-infantry-brigade", "Saint-Andrea's Brigade", "Gén. de Brigade Saint-Andrea",
         regiments=[regt("1st Italian Light", [u("it-light-infantry", "1st Italian Light")]),
                    regt("6th Italian Line", [u("it-line-infantry", "6th Italian Line")])]),
     bde("it-infantry-brigade", "Moroni's Brigade", "Gén. de Brigade Moroni",
         regiments=[regt("Milan Guard", [u("it-line-infantry", "Milan Guard Battalion")]),
                    regt("7th Italian Line", [u("it-line-infantry", "7th Italian Line")])]),
     bde("it-divisional-artillery", "Divisional Artillery",
         units=[u("it-foot-arty", "1/1st Italian Foot Battery"), u("it-foot-arty", "13/1st Italian Foot Battery")])],
    command=[cmd("it-div-cmd", "Gén. de Division Fontanelli")],
    notes=["Built from A Clash of Eagles' Italian list, the nearest to 1813.", WB_NOTE,
           "Each regiment was down to a single battalion, of a few hundred men; each is shown as one battalion.",
           "The Milan Guard Battalion, a city guard and not the Royal Guard, is shown as Line.",
           "The division's two foot batteries, where the list allows one, and only for an army of eight battalions or more, show as historical departures."])

WB_FRANQUEMONT = force(
    "wartenburg-franquemont", WT, "Franquemont's Division", "38th (Württemberg) Division, IV Corps (Bertrand)", "French",
    "All that was left of the Württemberg contingent, four combined battalions, holding Bleddin on Bertrand's right. Prince Karl of Mecklenburg's brigade came up the Elbe against it in the late morning, and by two in the afternoon had driven it out of the village.",
    [bde("wt-light-infantry-brigade", "Stockmayer's Brigade", "Gen-Maj von Stockmayer",
         units=[u("wt-light-infantry", "Combined Light Battalion")],
         regiments=[regt("1st Combined Line", [u("wt-line-infantry", "1st Combined Line Battalion")])]),
     bde("wt-infantry-brigade", "Döring's Brigade", "Gen-Maj von Döring",
         regiments=[regt("2nd Combined Line", [u("wt-line-infantry", "2nd Combined Line Battalion")]),
                    regt("3rd Combined Line", [u("wt-line-infantry", "3rd Combined Line Battalion")])]),
     bde("wt-divisional-artillery", "Divisional Artillery", units=[u("wt-light-arty", "1st Württemberg Foot Battery")])],
    command=[cmd("wt-div-cmd", "Gen-Lt Graf Franquemont")],
    notes=["Built from A Clash of Eagles' Württemberg 1812 list, the nearest to 1813.", WB_NOTE,
           "After Dennewitz each pair of regiments was put together as one combined battalion: the light battalion from the 9th and 10th Light, and the line battalions from the 1st, 4th and 6th Line. Together they had under two thousand men.",
           "The foot battery, four 6-pdrs and two howitzers, is the list's Light Artillery; with four battalions, where the list wants seven for it, it shows as a historical departure."])

WB_BEAUMONT = force(
    "wartenburg-beaumont", WP, "Beaumont's Cavalry", "29th Light Cavalry Brigade, IV Corps (Bertrand)", "French",
    "The corps' cavalry, two regiments of German light horse, on the right near Bleddin. It was swept aside by Mecklenburg's hussars as the Württembergers gave way.",
    [bde("wp-cavalry-brigade", "Wolff's Brigade", "Gen-Maj Wolff",
         units=[u("wp-guard-chevau-leger", "Westphalian Guard Chevau-légers"), u("wp-hussar", "Hessian Chevau-légers")])],
    command=[cmd("wp-div-cmd", "Gén. de Division Beaumont")],
    notes=["Built from A Clash of Eagles' Westphalian 1812 list, for its Guard Chevau-légers.", WB_NOTE,
           "The Hessian Chevau-légers are shown as Westphalian Hussars, the list's other light cavalry.",
           "A cavalry brigade on its own has no infantry brigade, which the list needs for it, so this shows as a historical departure. Play it alongside Franquemont's or Fontanelli's division."])


def pr_regt(name, units):
    return regt(name, [u(unit, n, **({"options": ["veteran-infantry"]} if "Grenadier" in n else {})) for unit, n in units])


WB_YORCK = force(
    "wartenburg-yorck", PR15, "Yorck's Corps", "I Corps, Army of Silesia", "Prussian",
    "Blücher's leading corps, which crossed the Elbe on two pontoon bridges in the river's bend and attacked Bertrand in his marshes at dawn. Steinmetz's brigade was shot down before the dike at Wartenburg; Prince Karl of Mecklenburg's went upstream and took Bleddin from the Württembergers; and Horn's, wading through the backwaters with the Leib Regiment at its head, came in on the French flank and decided the day. The corps lost some two thousand men, and Yorck took his title from the village.",
    [bde("pr15-infantry-brigade", "Advance Guard Infantry (Hiller)", "Maj Hiller von Gärtringen",
         units=[u("pr15-jager-coy", "East Prussian Jäger (2 companies)"), u("pr15-jager-coy", "Guard Jäger Company"),
                u("pr15-mounted-landwehr-attached", "5th Silesian Landwehr Cavalry")],
         regiments=[pr_regt("Grenadier Battalions", [(M, "Leib-Grenadier Battalion"), (M, "West Prussian Grenadier Battalion")]),
                    pr_regt("Line and Reserve Battalions", [(M, "I/Brandenburg Infantry"), (M, "II/12th Reserve Infantry"), (F_, "F/2nd East Prussian Infantry")]),
                    pr_regt("Silesian Landwehr", [(LW, "III/13th Silesian Landwehr"), (LW, "II/14th Silesian Landwehr"), (LW, "IV/15th Silesian Landwehr")])]),
     bde("pr15-cavalry-brigade", "Advance Guard Cavalry (Katzler)", "Col von Katzler",
         units=[u("pr15-hussar", "Brandenburg Hussars"), u("pr15-uhlan", "Brandenburg Uhlans"),
                u("pr15-hussar", "East Prussian National Cavalry"), u("pr15-horse-arty", "Horse Battery #2")]),
     bde("pr15-infantry-brigade", "1st Brigade (Steinmetz)", "Col von Steinmetz",
         units=[u("pr15-foot-arty", "6-pdr Foot Battery #2")],
         regiments=[pr_regt("East Prussian Grenadiers and 2nd East Prussian", [(M, "1st East Prussian Grenadier Battalion"), (M, "I/2nd East Prussian Infantry")]),
                    pr_regt("5th and 6th Silesian Landwehr", [(LW, "I/6th Silesian Landwehr"), (LW, "I/5th Silesian Landwehr"), (LW, "III/5th Silesian Landwehr")]),
                    pr_regt("13th Silesian Landwehr", [(LW, "I/13th Silesian Landwehr"), (LW, "II/13th Silesian Landwehr"), (LW, "IV/13th Silesian Landwehr")])]),
     bde("pr15-infantry-brigade", "2nd Brigade (Mecklenburg)", "Gen-Maj Prince Karl of Mecklenburg",
         units=[u("pr15-hussar-attached", "2nd Leib Hussars"), u("pr15-hussar-attached", "Mecklenburg-Strelitz Hussars"),
                u("pr15-foot-arty", "6-pdr Foot Battery #1")],
         regiments=[pr_regt("1st East Prussian Infantry", [(M, "I/1st East Prussian Infantry"), (M, "II/1st East Prussian Infantry"), (F_, "F/1st East Prussian Infantry")]),
                    pr_regt("Silesian Grenadiers and 2nd East Prussian", [(M, "Silesian Grenadier Battalion"), (M, "II/2nd East Prussian Infantry")]),
                    pr_regt("5th Silesian Landwehr", [(LW, "IV/5th Silesian Landwehr")])]),
     bde("pr15-infantry-brigade", "7th Brigade (Horn)", "Gen-Maj von Horn",
         units=[u("pr15-foot-arty", "½ 6-pdr Foot Battery #3", options=["half-battery"])],
         regiments=[pr_regt("Leib Infantry", [(M, "I/Leib Infantry"), (M, "II/Leib Infantry"), (F_, "F/Leib Infantry")]),
                    pr_regt("Thuringian Battalion", [(M, "Thuringian Battalion")]),
                    pr_regt("15th Silesian Landwehr", [(LW, "I/15th Silesian Landwehr"), (LW, "II/15th Silesian Landwehr")]),
                    pr_regt("4th Silesian Landwehr", [(LW, "III/4th Silesian Landwehr"), (LW, "Combined II & IV/Silesian Landwehr")])]),
     bde("pr15-infantry-brigade", "8th Brigade (Hünerbein)", "Gen-Maj von Hünerbein",
         units=[u("pr15-foot-arty", "6-pdr Foot Battery #15")],
         regiments=[pr_regt("Brandenburg Infantry", [(M, "II/Brandenburg Infantry"), (F_, "F/Brandenburg Infantry")]),
                    pr_regt("12th Reserve Infantry", [(M, "I/12th Reserve Infantry"), (F_, "F/12th Reserve Infantry")]),
                    pr_regt("14th Silesian Landwehr", [(LW, "IV/14th Silesian Landwehr")])]),
     bde("pr15-cavalry-brigade", "Reserve Cavalry (Jürgass)", "Col von Wahlen-Jürgass",
         units=[u("pr15-dragoon", "Lithuanian Dragoons"), u("pr15-dragoon", "West Prussian Dragoons"), u("pr15-horse-arty", "Horse Battery #1")]),
     bde("pr15-landwehr-cavalry-brigade", "Reserve Cavalry (Jürgass, Landwehr)", "Col von Wahlen-Jürgass",
         units=[u("pr15-mounted-landwehr", "10th Silesian Landwehr Cavalry"), u("pr15-mounted-landwehr", "1st Neumark Landwehr Cavalry"),
                u("pr15-horse-arty", "Horse Battery #3")]),
     bde("pr15-army-reserve-artillery", "Corps Artillery",
         units=[u("pr15-foot-arty", "½ 6-pdr Foot Battery #3 (with Mecklenburg)", options=["half-battery"])])],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Yorck")],
    notes=["Built from Albion Triumphant's Prussian 1815 list, the nearest to 1813: its Prussian Infantry Brigade is the 1813 brigade, the size of another army's division, with line, reserve and Landwehr battalions.",
           WB_NOTE.replace(", from Mirus's history of the fight; its batteries are from his return of the IV Corps a fortnight before", ", from Mirus's history of the fight"),
           "A Prussian brigade was the size of another army's division, so the whole corps is here. Take the brigades you want; each is a force in itself.",
           PR_GROUPED,
           "Nafziger's corps return of the same day has Hünerbein's Landwehr and half his battery detached to Halle; his Wartenburg order of battle, followed here, has the IV/14th Landwehr and the whole of Battery #15 with the brigade.",
           "The East Prussian National Cavalry, a volunteer regiment, is shown as Hussars. The 5th Silesian Landwehr Cavalry is the advance guard infantry's attached Landwehr cavalry.",
           "Mecklenburg's two hussar regiments are shown as attached small hussars; two of them, where the list allows one in the army, show as a historical departure. Battery #3 was split between Mecklenburg and Horn, so each has half of it, Mecklenburg's from the corps artillery.",
           "One-battalion Landwehr regiments in Mecklenburg's and Hünerbein's brigades, Horn's four regiments, and Jürgass's line and Landwehr cavalry brigades together show as historical departures."])

for b in WB_YORCK["brigades"]:
    if b["type"] == "pr15-infantry-brigade" and len(b.get("regiments", [])) >= 3:
        b["units"] = [u("pr15-sub-cmd")] + b["units"]
WB_YORCK["notes"].insert(4, PR_SUB)

WB_FRANQUEMONT["missing"] = [{"name": "Jett's 24th Light Cavalry Brigade",
                              "reason": "A squadron each of the 1st and 3rd Württemberg Chevau-légers, about a hundred men in all, too few for a unit."}]
WB_YORCK["missing"] = [{"name": "III/2nd Leib Hussars", "reason": "One squadron with Katzler's advance guard, too small for a unit of its own; the rest of the regiment is with Mecklenburg."},
                       {"name": "II/5th Silesian Landwehr", "reason": "Detached to Halle, and not at Wartenburg."}]

WARTENBURG = battle(
    "wartenburg", "Wartenburg", "3 October 1813",
    "Blücher, marching north to join Bernadotte before Leipzig, threw two pontoon bridges over the Elbe where the river bends round Wartenburg. Bertrand's corps held the far bank, Morand's French in the village behind a long dike, with marsh and backwaters in front. Yorck's corps crossed at dawn. Steinmetz's brigade attacked the dike head-on and was shot down; Mecklenburg's went upstream and drove the Württembergers out of Bleddin; and Horn's, wading through the mud, came in on the flank. Bertrand fell back on Kemberg, and the Army of Silesia was over the Elbe.",
    [WB_FR, WB_PR, WB_IV, {"label": "Battle of Wartenburg (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Wartenburg"}],
    [WB_MORAND, WB_FONTANELLI, WB_FRANQUEMONT, WB_BEAUMONT, WB_YORCK], [], alliances=())


# ================================================================ Hanau, 30–31 October 1813

HN_BAV = {"label": "Bavarian Army Corps, Battle of Hanau, 29–31 October 1813 (Nafziger Collection 813JAC)", "url": NAF + "813JAC.pdf"}
HN_AL = {"label": "Allied Forces, Battle of Hanau, 29–31 October 1813 (Nafziger Collection 813JAG)", "url": NAF + "813JAG.pdf"}
HN_GUARD = {"label": "French Imperial Guard, 1 November 1813 (Nafziger Collection 813KXD)", "url": NAF + "813KXD.pdf"}
HN_GUARD_CAV = {"label": "French Guard Cavalry, 15 October 1813 (Nafziger Collection 813JZD)", "url": NAF + "813JZD.pdf"}
HN_OOB = {"label": "Battle of Hanau order of battle (Wikipedia, after Mir)", "url": "https://en.wikipedia.org/wiki/Hanau_order_of_battle"}
HN_FR_NOTE = "After Wikipedia's order of battle for Hanau, from Mir's history of the battle; the page names regiments and battalions but no batteries."
HN_AL_NOTE = "After Nafziger's order of battle for Hanau, from the Bavarian war archives' history."
AU, BAV = "austria", "bavaria"
HN_WEAK = ("Only these divisions of Victor's and Macdonald's corps were engaged, and after Leipzig their battalions were far "
           "below strength; they are shown at full size, and the list's Small upgrade would suit many of them.")
CAV_ONLY = ("A cavalry force on its own has no infantry brigade, which the list needs to allow its cavalry, so this shows as a "
            "historical departure. Play it alongside infantry, or agree it with your opponent.")


def fr_regt(name, n, light_=False):
    return light(name, n) if light_ else line(name, n)


HN_CHARPENTIER = force(
    "hanau-charpentier", FR, "Charpentier's Division", "36th Division, XI Corps (Macdonald)", "French",
    "Macdonald's leading division, which went into the Lamboy forest in skirmish order on the morning of the 30th and pushed Wrede's light troops back through the trees, opening the way for the Guard's guns.",
    [bde("fr-infantry-brigade", "Simmer's Brigade", "Gén. de Brigade Simmer", regiments=[fr_regt("6th Line", 2), fr_regt("112th Line", 4)]),
     bde("fr-infantry-brigade", "Meunier's Brigade", "Gén. de Brigade Meunier", regiments=[fr_regt("14th Léger", 3, True), fr_regt("3rd Line", 2)])],
    command=[cmd("fr-div-cmd", "Gén. de Division Charpentier")],
    notes=[LIST_FR, HN_FR_NOTE, HN_WEAK])

HN_DUBRETON = force(
    "hanau-dubreton", FR, "Dubreton's Division", "4th Division, II Corps (Victor)", "French",
    "Victor's division, which fought through the forest beside Charpentier's and cleared it in front of the allied centre by midday.",
    [bde("fr-infantry-brigade", "Dubreton's Brigade", "", regiments=[fr_regt("24th Line", 4), fr_regt("10th Line", 4)]),
     bde("fr-infantry-brigade", "Brun's Brigade", "Gén. de Brigade Brun", regiments=[fr_regt("37th Line", 3), fr_regt("56th Line", 4)])],
    command=[cmd("fr-div-cmd", "Gén. de Division Dubreton")],
    notes=[LIST_FR, HN_FR_NOTE, HN_WEAK, "The order of battle names no commander for the division's first brigade."])

HN_GUARD_INF = force(
    "hanau-old-guard", FIG, "The Old Guard, with Drouot's Guns", "1st and 2nd Old Guard Divisions (Friant, Curial), Imperial Guard", "French",
    "The Guard's infantry, which held the edge of the forest while Drouot brought its artillery out on a track towards Wrede's left. Fifty guns, massed under the Guard's protection, silenced the allied batteries and opened the way for the Guard cavalry; on the 31st the Guard marched on through Hanau.",
    [bde("fig-old-guard-brigade", "Christiani's Brigade", "Gén. de Brigade Christiani",
         units=[u("fig-og-foot-arty", "Old Guard Foot Battery")],
         regiments=[regt("1st Chasseurs à Pied", bns("fig-old-guard-chasseurs", "1st Chasseurs à Pied", 2)),
                    regt("2nd Chasseurs à Pied", bns("fig-middle-guard-chasseurs", "2nd Chasseurs à Pied", 2))]),
     bde("fig-old-guard-brigade", "Michel's Brigade", "Gén. de Brigade Michel",
         units=[u("fig-og-foot-arty", "Old Guard Foot Battery")],
         regiments=[regt("1st Grenadiers à Pied", bns("fig-old-guard-grenadiers", "1st Grenadiers à Pied", 2)),
                    regt("2nd Grenadiers à Pied", bns("fig-middle-guard-grenadiers", "2nd Grenadiers à Pied", 2))]),
     bde("fig-young-guard-brigade", "Curial's Fusiliers", "Gén. de Division Curial",
         regiments=[regt("Fusilier-Chasseurs", bns("fig-fusilier-chasseurs", "Fusilier-Chasseurs", 2)),
                    regt("Fusilier-Grenadiers", bns("fig-fusilier-grenadiers", "Fusilier-Grenadiers", 2))]),
     bde("fig-italian-brigade", "Curial's Vélites", "", units=[u("fig-velites-turin", "Vélites of Turin"), u("fig-velites-florence", "Vélites of Florence")]),
     bde("fig-artillery-reserve", "Guard Artillery (Drouot)",
         units=[u("fig-og-heavy-foot-arty", "Old Guard 12-pdr Foot Battery"), u("fig-og-horse-arty", "Old Guard Horse Battery"),
                u("fig-og-horse-arty", "Old Guard Horse Battery")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Friant")],
    notes=["Built from A Clash of Eagles' Imperial Guard 1812 list, the nearest to 1813.", HN_FR_NOTE,
           "The 1st Chasseurs and Grenadiers à Pied are the list's Old Guard, and the 2nd, raised in 1811, its Middle Guard.",
           "The Fusilier regiments of Curial's division, without the Young Guard regiment the list's brigade wants beside them, show as a historical departure; the Vélites of Turin and Florence are the list's Italian brigade.",
           "The order of battle gives the Guard artillery as forty foot and twelve horse guns, about five foot and two horse batteries. Two Old Guard foot batteries, one with each Old Guard brigade, the 12-pdr battery and the two horse batteries are here; the batteries themselves aren't named.",
           "Drouot commanded the Guard infantry and artillery at Hanau; Friant leads the force, as its senior division commander."])
HN_GUARD_INF["missing"] = [{"name": "Two more Guard foot batteries", "reason": "The rest of Drouot's forty foot guns, more than the list's Old Guard brigades and reserve take."}]

HN_GUARD_CAV_F = force(
    "hanau-guard-cavalry", FIG, "Nansouty's Guard Cavalry", "Guard Cavalry Corps, Imperial Guard", "French",
    "Brought out beside Drouot's guns on Wrede's left, it fell on the Bavarian and Austrian cavalry there, the Grenadiers à Cheval and Dragoons riding them down, and drove them back on the Kinzig.",
    [bde("fig-heavy-cavalry-brigade", "Walther's Heavy Cavalry", "Gén. de Division Walther",
         units=[u("fig-grenadiers-a-cheval-regt", "Grenadiers à Cheval"), u("fig-empress-dragoons", "Empress Dragoons"),
                u("fig-og-horse-arty", "Old Guard Horse Battery")]),
     bde("fig-light-cavalry-brigade", "Lion's Brigade", "Gén. de Brigade Lion",
         units=[u("fig-chasseurs-a-cheval", "Chasseurs à Cheval"), u("fig-og-horse-arty", "Old Guard Horse Battery")]),
     bde("fig-light-cavalry-brigade", "Krasinski's Brigade", "Gén. de Brigade Krasinski", units=[u("fig-polish-lancers", "1st (Polish) Chevau-légers Lanciers")]),
     bde("fig-light-cavalry-brigade", "Colbert's Brigade", "Gén. de Brigade Colbert",
         units=[u("fig-dutch-red-lancers", "2nd (Dutch) Chevau-légers Lanciers"), u("fig-og-horse-arty", "Old Guard Horse Battery")])],
    command=[cmd("fig-div-cmd", "Gén. de Division Nansouty")],
    notes=["Built from A Clash of Eagles' Imperial Guard 1812 list, the nearest to 1813.", HN_FR_NOTE,
           "Each Guard regiment is shown as one unit, its Old and Young Guard squadrons together: Walther's Old Guard squadrons and Lefebvre-Desnouettes's Young Guard ones.",
           "The Guard Cavalry's four horse batteries are from Nafziger's return of 15 October.",
           CAV_ONLY])
HN_GUARD_CAV_F["missing"] = [
    {"name": "1st to 4th Gardes d'Honneur", "reason": "The list has only the Italian Gardes d'Honneur, and only with its Italian vélites."},
    {"name": "Berg Lancers", "reason": "A line regiment of the Grand Duchy of Berg riding with the Guard, which the Guard list can't take."},
    {"name": "Young Guard Dragoons (Pinteville)", "reason": "Two squadrons apart from the Empress Dragoons, too few for a unit of their own."}]

HN_SEBASTIANI = force(
    "hanau-sebastiani", FR, "Sébastiani's Cavalry", "II Cavalry Corps", "French",
    "About three thousand horsemen in twenty-two regiments, which came out with the Guard cavalry on Wrede's left and joined in the charges that drove the allied horse back.",
    [bde("fr-light-cavalry-brigade", "Gérard's Brigade", "Gén. de Brigade Gérard",
         units=[u("fr-lancer", "2nd Chevau-légers"), u("fr-chasseur-a-cheval", "11th Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "12th Chasseurs à Cheval")]),
     bde("fr-light-cavalry-brigade", "Dommanget's Brigade", "Gén. de Brigade Dommanget",
         units=[u("fr-lancer", "4th Chevau-légers"), u("fr-hussar-regt", "5th Hussars"), u("fr-hussar-regt", "9th Hussars")]),
     bde("fr-light-cavalry-brigade", "Maurin's Brigade", "Gén. de Brigade Maurin",
         units=[u("fr-lancer", "6th Chevau-légers"), u("fr-chasseur-a-cheval", "4th Chasseurs à Cheval"),
                u("fr-chasseur-a-cheval", "7th Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "20th Chasseurs à Cheval")]),
     bde("fr-light-cavalry-brigade", "Wathier's Brigade", "Gén. de Brigade Wathier",
         units=[u("fr-chasseur-a-cheval", "23rd Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "24th Chasseurs à Cheval"), u("fr-hussar-regt", "11th Hussars")]),
     bde("fr-heavy-cavalry-brigade", "Daugeranville's Brigade", "Gén. de Brigade Daugeranville",
         units=[u("fr-carabinier", "1st Carabiniers"), u("fr-carabinier", "2nd Carabiniers"), u("fr-cuirassier", "1st Cuirassiers")]),
     bde("fr-heavy-cavalry-brigade", "Thiry's Brigade", "Gén. de Brigade Thiry",
         units=[u("fr-cuirassier", "5th Cuirassiers"), u("fr-cuirassier", "8th Cuirassiers"), u("fr-cuirassier", "10th Cuirassiers")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Sébastiani")],
    notes=[LIST_FR, HN_FR_NOTE,
           "The corps' twenty-two regiments had two to four squadrons each, about 140 men on average; they are shown at full size, and the list's Small upgrade would suit them.",
           "The chevau-légers lanciers are the list's Lancers.", CAV_ONLY])

# --- Wrede's army

KREIS = ("The Kreis battalions were national field battalions, raised in 1813 from the districts' militia and often made up of parts of "
         "two; they are shown as Line.")
WURST = "The Wurst batteries, light 6-pdrs with the gunners riding on the limbers, are the list's Light Artillery."
LIST_BAV = "Built from A Clash of Eagles' Bavarian 1812 list, the nearest to 1813; Bavaria had changed sides a fortnight before."
LIST_AU = "Built from A Clash of Eagles' Austrian 1812 list, the nearest to 1813."


def bav(name, n=0, bns_=()):
    return regt(name, [u("bav-line-infantry", b) for b in bns_] if bns_ else bns("bav-line-infantry", name, n))


HN_BECKERS = force(
    "hanau-beckers", BAV, "Beckers's Division", "2nd Division, Bavarian Army Corps (Wrede)", "Bavarian",
    "Part of Wrede's centre, posted along the Frankfurt road where it left the Lamboy forest. Its light troops were driven back out of the trees by Charpentier's and Dubreton's skirmishers, and when the French guns came into action its line was pounded and fell back on the Kinzig.",
    [bde("bav-infantry-brigade", "Pappenheim's Brigade", "Gen-Maj Graf Pappenheim",
         units=[u("bav-light-infantry", "Combined Jäger Battalion (5th and 6th)")],
         regiments=[bav("4th Line", 2), bav("Kreis Battalions", bns_=["Combined Salzach Kreis Battalion", "1st Regen Kreis Battalion"])]),
     bde("bav-infantry-brigade", "Zoller's Brigade", "Gen-Maj Freiherr von Zoller",
         units=[u("bav-light-infantry", "1st Jäger Battalion")],
         regiments=[bav("6th Line", 2), bav("Kreis Battalions", bns_=["1st Iller Kreis Battalion", "Combined Rezat Kreis Battalion"])]),
     bde("bav-cavalry-brigade", "Elbracht's Brigade", "Gen-Maj Elbracht",
         units=[u("bav-chevau-leger", "3rd Chevau-légers"), u("bav-chevau-leger", "6th Chevau-légers"), u("bav-light-arty", "2nd Wurst Battery")]),
     bde("bav-divisional-artillery", "Divisional Artillery",
         units=[u("bav-foot-arty", "7th 6-pdr Foot Battery (Danner)"), u("bav-position-battery", "11th 12-pdr Foot Battery (Dietrich)")])],
    command=[cmd("bav-div-cmd", "Gen-Lt Beckers von Westerstetten")],
    notes=[LIST_BAV, HN_AL_NOTE, KREIS, WURST,
           "The corps' artillery reserve, two 12-pdr batteries under Ulmer, is shown one with each division, as the list's Heavy Foot Battery.",
           "The Wurst battery rides with Elbracht's chevau-légers, as the list takes a light battery in a cavalry brigade; the 3rd Chevau-légers had three squadrons."])

HN_LAMOTTE = force(
    "hanau-lamotte", BAV, "Lamotte's Division", "3rd Division, Bavarian Army Corps (Wrede)", "Bavarian",
    "Wrede's right, by the Kinzig and the Lamboy bridge. When the centre gave way it was left with the river at its back and a single bridge to cross; many men were drowned trying to get over, and the division fell back into Hanau.",
    [bde("bav-infantry-brigade", "Stockh's Brigade", "Gen-Maj Jason von der Stockh",
         regiments=[bav("11th Line", 2), bav("7th Line", bns_=["I/7th Line"]),
                    bav("Kreis Battalions", bns_=["1st Iller Kreis Battalion", "1st Unter-Donau Kreis Battalion"])]),
     bde("bav-infantry-brigade", "Deroy's Brigade", "Gen-Maj von Deroy",
         regiments=[bav("5th Line", bns_=["I/5th Line"]), bav("8th Line", bns_=["I/8th Line"]), bav("9th Line", bns_=["I/9th Line"]),
                    bav("Kreis Battalions", bns_=["2nd Iller Kreis Battalion", "1st Isar Kreis Battalion"])]),
     bde("bav-cavalry-brigade", "Diez's Brigade", "Col Diez",
         units=[u("bav-chevau-leger", "4th Chevau-légers"), u("bav-chevau-leger", "5th Chevau-légers"), u("bav-light-arty", "3rd Wurst Battery (Halder)")]),
     bde("bav-divisional-artillery", "Divisional Artillery",
         units=[u("bav-foot-arty", "9th 6-pdr Foot Battery (Achner)"), u("bav-position-battery", "8th 12-pdr Foot Battery (Anzinger)")])],
    command=[cmd("bav-div-cmd", "Gen-Lt Freiherr von Lamotte")],
    notes=[LIST_BAV, HN_AL_NOTE, KREIS, WURST,
           "Both brigades were made up of single battalions of different regiments, so Stockh's has three regiments and Deroy's four, where the list's brigade takes two; these show as historical departures.",
           "The corps' artillery reserve, two 12-pdr batteries under Ulmer, is shown one with each division, as the list's Heavy Foot Battery.",
           "The Wurst battery rides with Diez's chevau-légers, as the list takes a light battery in a cavalry brigade; both regiments had three squadrons."])

HN_VIEREGG = force(
    "hanau-vieregg", BAV, "Vieregg's Cavalry", "1st Cavalry Brigade, Bavarian Army Corps (Wrede)", "Bavarian",
    "The Bavarian cavalry reserve, on Wrede's left with the Austrian horse, which met the charge of the Guard cavalry and Sébastiani's squadrons when Drouot's guns had done their work, and was driven back.",
    [bde("bav-cavalry-brigade", "Vieregg's Brigade", "Gen-Maj Freiherr von Vieregg",
         units=[u("bav-chevau-leger", "1st Chevau-légers"), u("bav-chevau-leger", "2nd Chevau-légers"), u("bav-chevau-leger", "7th Chevau-légers")])],
    command=[cmd("bav-div-cmd", "Gen-Maj Freiherr von Vieregg")],
    notes=[LIST_BAV, HN_AL_NOTE, "Three regiments, where the list's brigade takes two, show as a historical departure.", CAV_ONLY])

HN_FRESNEL = force(
    "hanau-fresnel", AU, "Fresnel's Light Division", "Light Division, Austrian I Corps", "Austrian",
    "The Austrian light troops, Jäger, hussars and uhlans, out in front of the allied line and in the forest, the first to meet the French columns on the morning of the 30th.",
    [bde("at-light-cavalry-brigade", "Hardegg's Brigade", "Gen-Maj Graf Hardegg", units=[u("at-hussar", "Archduke Joseph Hussars")]),
     bde("at-advanced-guard-brigade", "Volkmann's Brigade", "Gen-Maj von Volkmann",
         units=[u("at-jager", "3rd Jäger Battalion"), u("at-uhlan", "Schwarzenberg Uhlans"), u("at-cavalry-arty", "Cavalry Battery")])],
    command=[cmd("at-inf-div-cmd", "FML Graf Fresnel")],
    notes=[LIST_AU, HN_AL_NOTE,
           "The division's Szekler Grenz regiment was detached to Bach's division, and is shown there.",
           "With no line infantry brigade, which the list wants first, the division shows a historical departure. Play it alongside Bach's division."])

HN_BACH = force(
    "hanau-bach", AU, "Bach's Division", "Line Division, Austrian I Corps", "Austrian",
    "The Austrian line infantry, with the Szekler Grenzers lent from the light division, in the allied centre beside the Bavarians; it held its ground until the French guns and cavalry broke the left, then fell back over the Kinzig.",
    [bde("at-line-infantry-brigade", "Bach's Brigade", "Gen-Maj von Bach",
         units=[u("at-grenz", "I/Szekler Grenz"), u("at-grenz", "II/Szekler Grenz"), u("at-6pdr-brigade-battery", "6-pdr Brigade Battery"),
                u("at-6pdr-brigade-battery", "6-pdr Brigade Battery")],
         regiments=[regt("Archduke Rudolph Infantry (IR 14)", bns("at-infantry-german", "Archduke Rudolph", 4)),
                    regt("Jordis Infantry (IR 59)", bns("at-infantry-german", "Jordis", 4))]),
     bde("at-reserve-artillery", "Reserve Artillery (Sertnik)", units=[u("at-position-battery", "12-pdr Position Battery")])],
    command=[cmd("at-inf-div-cmd", "Gen-Maj von Bach")],
    notes=[LIST_AU, HN_AL_NOTE,
           "Each regiment fought with four battalions, where the list takes two Large ones; the Grenz battalions and two brigade batteries together are more additional troops than the brigade takes. These show as historical departures.",
           "One of the corps' three 12-pdr batteries is here as the list's Position Battery; with eight line battalions, where the list wants nine for it, and one brigade where the list wants one per 500 points, these show as historical departures."])
HN_BACH["missing"] = [{"name": "Two more 12-pdr Position Batteries and a 6-pdr Foot Battery", "reason": "The rest of Sertnik's corps artillery, more than the list takes for the division's battalions."}]

HN_TRAUTENBERG = force(
    "hanau-trautenberg", AU, "Trautenberg's Grenadiers", "1st Reserve Division, Austrian I Corps", "Austrian",
    "Seven battalions of Austrian grenadiers, Wrede's reserve, which covered the retreat over the Kinzig when the centre gave way.",
    [bde("at-grenadier-brigade", "Klenau's Brigade", "Gen-Maj Graf Klenau",
         units=[*[u("at-grenadier", f"Grenadier Battalion {i}") for i in range(1, 5)], u("at-6pdr-brigade-battery", "6-pdr Brigade Battery")]),
     bde("at-grenadier-brigade", "Diemar's Brigade", "Gen-Maj von Diemar",
         units=[u("at-grenadier", f"Grenadier Battalion {i}") for i in range(5, 8)])],
    command=[cmd("at-inf-div-cmd", "FML von Trautenberg")],
    notes=[LIST_AU, HN_AL_NOTE, "The order of battle doesn't name the grenadier battalions, so they are numbered here.",
           "Two grenadier brigades with no line infantry brigade, which the list wants first, and Klenau's 6-pdr battery with no line battalions to allow it, show as historical departures. Play it alongside Bach's division."])
HN_TRAUTENBERG["missing"] = [{"name": "Diemar's 3-pdr Brigade Battery", "reason": "The list's grenadier brigade takes only a 6-pdr battery."}]

HN_SPLENY = force(
    "hanau-spleny", AU, "Spleny's Cavalry", "Cavalry Reserve Division, Austrian I Corps", "Austrian",
    "The Austrian heavy and hussar cavalry, on the allied left beside Vieregg's Bavarians, which was overthrown by the Guard cavalry's charge.",
    [bde("at-light-cavalry-brigade", "Minutillo's Brigade", "Gen-Maj Minutillo", units=[u("at-hussar", "Szekler Hussars")]),
     bde("at-heavy-cavalry-brigade", "Flachenfeld's Brigade", "Col von Flachenfeld",
         units=[u("at-dragoon", "Knesevich Dragoons"), u("at-cuirassier", "Liechtenstein Cuirassiers"), u("at-cavalry-arty", "Cavalry Battery")])],
    command=[cmd("at-inf-div-cmd", "FML von Spleny")],
    notes=[LIST_AU, HN_AL_NOTE,
           "The Frimont Hussars, Minutillo's other regiment, were detached and are left out.",
           "A light brigade of one regiment, and dragoons and cuirassiers in one heavy brigade, which the list's brigade doesn't mix, show as historical departures.",
           CAV_ONLY])

HN_MENSDORFF = force(
    "hanau-mensdorff", RU, "Mensdorff's Cossacks", "Streifkorps, with Wrede", "Russian",
    "Two Don Cossack regiments of Mensdorff's raiding column, which had come to join Wrede and harried the French columns on the road from Gelnhausen.",
    [bde("ru-cossack-brigade", "Mensdorff's Streifkorps", "Lt-Col Count Mensdorff-Pouilly",
         units=[u("ru-mounted-cossack", "Gorin #1 Don Cossacks"), u("ru-mounted-cossack", "Ilovaisky #10 Don Cossacks")])],
    command=[cmd("ru-div-cmd", "Lt-Col Count Mensdorff-Pouilly")],
    notes=[LIST_RU, HN_AL_NOTE, "Mensdorff was an Austrian officer leading a column of Russian Cossacks.",
           "Chernyshev's and Orlov-Denisov's raiding columns, which Nafziger lists with Wrede's army, were not in the battle.",
           "A Cossack brigade on its own has no infantry brigade, which the list wants, so this shows as a historical departure."])

HANAU = battle(
    "hanau", "Hanau", "30–31 October 1813",
    "Wrede, whose Bavarians had changed sides a fortnight before, marched with Austrians and Bavarians to stand across Napoleon's road home at Hanau, with the Kinzig at his back and the Lamboy forest in front. On the 30th Charpentier's and Dubreton's divisions cleared the forest in skirmish order; Drouot then brought fifty of the Guard's guns out on Wrede's left and silenced his batteries, and Nansouty's Guard cavalry and Sébastiani's squadrons rode down the allied horse. Wrede's line fell back over the Kinzig, many men drowning at the Lamboy bridge, and on the 31st the Grande Armée's remnant marched on through Hanau to the Rhine.",
    [HN_BAV, HN_AL, HN_GUARD, HN_GUARD_CAV, HN_OOB, {"label": "Battle of Hanau (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Hanau"}],
    [HN_CHARPENTIER, HN_DUBRETON, HN_GUARD_INF, HN_GUARD_CAV_F, HN_SEBASTIANI,
     HN_BECKERS, HN_LAMOTTE, HN_VIEREGG, HN_FRESNEL, HN_BACH, HN_TRAUTENBERG, HN_SPLENY, HN_MENSDORFF],
    [], alliances=(("Bavarian", "Austrian", "Russian"),))


# ================================================================ Hagelberg, 27 August 1813

HG_PR = {"label": "Prussian Order of Battle for Hagelberg, 27 August 1813 (Nafziger Collection 813HHC)", "url": NAF + "813HHC.pdf"}
HG_FR = {"label": "French Forces, Battle of Hagelberg, 27 August 1813 (Nafziger Collection 813HID)", "url": NAF + "813HID.pdf"}
HG_NOTE = "After Nafziger's order of battle for Hagelberg."

HG_GIRARD = force(
    "hagelberg-girard", FR, "Girard's Division", "Magdeburg Division (Lanusse), under Girard", "French",
    "Girard's column out of Magdeburg, marching to join Oudinot's drive on Berlin: third battalions of French regiments, Westphalians, Saxon ducal troops and Croats. Caught round Hagelberg by Hirschfeld's Landwehr, it was broken in the village and among its walls and gardens, much of the fighting done with musket butts; Girard was wounded, and barely a third of his men got back to Magdeburg.",
    [bde("fr-infantry-brigade", "Sennegon's Brigade", "Gén. de Brigade Sennegon",
         regiments=[provisional("Light Battalions", ["3/24th Léger", "3/26th Léger"], True),
                    provisional("Line Battalions", ["3/18th Line", "3/19th Line", "2/1st Croatian"]),
                    regt("9th Westphalian Line", [u("fr-rheinbund-infantry", "1/9th Westphalian Line")])]),
     bde("fr-infantry-brigade", "Baville's Brigade", "Gén. de Brigade Baville",
         regiments=[regt("134th Line", [u("fr-line-infantry", "3/134th Line"), u("fr-line-infantry", "6/134th Line")]),
                    provisional("Line Battalions", ["3/56th Line", "3/72nd Line"]),
                    regt("Saxon Ducal House (4th Rheinbund)", [u("fr-rheinbund-infantry", "1/Saxon Ducal House"), u("fr-rheinbund-infantry", "2/Saxon Ducal House")])]),
     bde("fr-light-cavalry-brigade", "Attached Cavalry", "", units=[u("fr-hussar-regt", "13th Hussars")]),
     foot("1/9th Foot Artillery", "16/9th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Girard")],
    notes=[LIST_FR, HG_NOTE,
           "Lanusse commanded the Magdeburg Division under Girard, who led the whole column; Girard leads the force.",
           "The third and sixth battalions of regiments serving elsewhere, sent out from their depots, are grouped as the brigades' regiments, as the list takes them. The Croatian battalion is shown as Line.",
           "The 9th Westphalian and the Saxon ducal battalions are the list's Rheinbund infantry; two Rheinbund battalions in Baville's regiment, where the list takes one, show as a historical departure.",
           "The 13th Hussars had three squadrons, about 500 men.", TWO_BATTERIES])
HG_GIRARD["missing"] = [{"name": "Two escadrons de marche", "reason": "A squadron each of heavy and light cavalry drafts on their way to the army, too few for units of their own."}]

HG_HIRSCHFELD = force(
    "hagelberg-hirschfeld", PR15, "Hirschfeld's Corps", "Detached corps, Army of the North", "Prussian",
    "Hirschfeld's column of Kurmark Landwehr, raw troops of a few weeks' service with only a stiffening of the 1st Reserve Regiment, which caught Girard round Hagelberg. Its battalions stormed the village, and when their wet muskets would not fire they fought it out at the walls with butts and bayonets; Chernyshev's Cossacks came up to complete the rout.",
    [pi("Advance Guard (Langen)", "Maj von Langen",
        [("1st Reserve Infantry", [("M", "I/1st Reserve Infantry"), ("M", "II/1st Reserve Infantry"), ("M", "III/1st Reserve Infantry")])]),
     pi("Right Wing (Puttlitz)", "Gen-Maj von Puttlitz",
        [("1st Reserve Infantry", [("M", "IV/1st Reserve Infantry")]),
         ("6th Kurmark Landwehr", [("L", "I/6th Kurmark Landwehr"), ("L", "II/6th Kurmark Landwehr"), ("L", "III/6th Kurmark Landwehr"), ("L", "IV/6th Kurmark Landwehr")]),
         ("7th Kurmark Landwehr", [("L", "II/7th Kurmark Landwehr")])]),
     pi("Left Wing (Boguslawski)", "Col von Boguslawski",
        [("3rd Kurmark Landwehr", [("L", "II/3rd Kurmark Landwehr")]),
         ("4th Kurmark Landwehr", [("L", "II/4th Kurmark Landwehr"), ("L", "III/4th Kurmark Landwehr")])]),
     pi("Reserve (Marwitz)", "Lt-Col von der Marwitz",
        [("3rd Kurmark Landwehr", [("L", "I/3rd Kurmark Landwehr"), ("L", "III/3rd Kurmark Landwehr"), ("L", "IV/3rd Kurmark Landwehr")])]),
     pi("Detachment (Reuss)", "Lt-Col von Reuss",
        [("Elbe Infantry", [("M", "I/Elbe Infantry")]),
         ("4th and 7th Kurmark Landwehr", [("L", "I/4th Kurmark Landwehr"), ("L", "I/7th Kurmark Landwehr")])],
        [u("pr15-mounted-landwehr-attached", "3rd Kurmark Landwehr Cavalry (1 squadron)"), u("pr15-foot-arty", "6-pdr Foot Battery #6")]),
     pc("Cavalry (Bismarck)", "Col von Bismarck",
        [u("pr15-mounted-landwehr", "3rd Kurmark Landwehr Cavalry"), u("pr15-mounted-landwehr", "5th Kurmark Landwehr Cavalry"),
         u("pr15-mounted-landwehr", "6th Kurmark Landwehr Cavalry")], landwehr=True)],
    command=[cmd("pr15-corps-cmd", "Gen-Maj von Hirschfeld")],
    notes=[PR_LIST, HG_NOTE, PR_GROUPED, PR_SUB,
           "The Kurmark Landwehr had been raised that summer and were the list's Landwehr to the life, Unreliable rule and all.",
           "Hirschfeld's brigades were wings and detachments of a few battalions each, not the list's brigades: Langen's three 1st Reserve battalions with no Landwehr, Marwitz's one Landwehr regiment and Boguslawski's two with no line regiment, Landwehr regiments of one or four battalions, and Reuss's battery with three battalions to support it all show as historical departures.",
           "The 3rd Kurmark Landwehr Cavalry's fourth squadron rode with Reuss's detachment, as its attached Landwehr cavalry."])
HG_HIRSCHFELD["missing"] = [
    {"name": "Russian Light Battery #26 (Chamborand)", "reason": "A Russian battery of ten guns with Bismarck's cavalry, which a force from the Prussian list can't take."},
    {"name": "Chernyshev's Cossacks", "reason": "Five Cossack regiments that came up to join the pursuit; Russian, so not in a force from the Prussian list."}]

HAGELBERG = battle(
    "hagelberg", "Hagelberg", "27 August 1813",
    "While Oudinot fell back from Großbeeren, Girard marched out of Magdeburg with a column of depot battalions and German allies to join him. Hirschfeld, with a corps of Kurmark Landwehr only weeks old and a few regular battalions, caught him near Belzig and attacked round the village of Hagelberg in the rain. The Landwehr's muskets would not fire, and the fight at the village walls was settled with butts and bayonets; Girard's column broke, his cavalry fled, Chernyshev's Cossacks joined the pursuit, and little more than a third of it reached Magdeburg.",
    [HG_PR, HG_FR, {"label": "Battle of Hagelberg (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Hagelberg"}],
    [HG_GIRARD, HG_HIRSCHFELD], [], alliances=())


# ================================================================ Dennewitz, 6 September 1813

DN_FR = {"label": "French Forces, Battle of Dennewitz, 6 September 1813 (Nafziger Collection 813IAG)", "url": NAF + "813IAG.pdf"}
DN_AL = {"label": "Allied Forces, Battle of Dennewitz, 6 September 1813 (Nafziger Collection 813IAF)", "url": NAF + "813IAF.pdf"}
DN_NOTE = "After Nafziger's order of battle for Dennewitz."
DN_SAX_NOTE = ("After Nafziger's order of battle for Großbeeren, a fortnight before: his Dennewitz return gives the Saxons as one "
               "division, an organisation he notes was only set up on 17 September, so the two divisions of August are kept here.")
GDW = "grand-duchy-of-warsaw"
DN_WEAK = "Its battalions were well under strength after Großbeeren; they are shown at full size, and the list's Small upgrade would suit many of them."


def again(f, id_, summary, notes):
    """A force from another battle, as it fought here"""
    g = copy.deepcopy(f)
    g["id"], g["summary"] = id_, summary
    g["notes"] = notes + [n for n in g["notes"][1:] if n not in (GB_NOTE,)]
    g.pop("missing", None)
    return g


def bn_list(unit, reg, labels):
    return regt(reg, [u(unit, f"{b}/{reg}") for b in labels])


DN_MORAND = force(
    "dennewitz-morand", FR, "Morand's Division", "12th Division, IV Corps (Bertrand)", "French",
    "Bertrand's leading division, which came on Tauentzien's corps across the Agerbach at Dennewitz in the morning and fought the Prussian Landwehr there until Bülow's brigades came up on its flank.",
    [bde("fr-infantry-brigade", "Ligier-Belair's Brigade", "Gén. de Brigade Ligier-Belair", regiments=[bn_list("fr-light-infantry", "8th Léger", ["2", "4"])]),
     bde("fr-infantry-brigade", "Toussaint's Brigade", "Gén. de Brigade Toussaint",
         units=[u("fr-regimental-arty-section", "Artillery Company, 13th Line")], regiments=[bn_list("fr-line-infantry", "13th Line", ["1", "2", "3", "4", "6"])]),
     bde("fr-infantry-brigade", "Hulot's Brigade", "Gén. de Brigade Hulot",
         units=[u("fr-regimental-arty-section", "Artillery Company, 23rd Line")], regiments=[bn_list("fr-line-infantry", "23rd Line", ["1", "2", "4", "6"])]),
     foot("1/2nd Foot Artillery", "3/2nd Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Morand")],
    notes=[LIST_FR, DN_NOTE,
           "The 13th and 23rd Line's regimental artillery companies are from Nafziger's IV Corps return of 20 September, each shown as a section of regimental guns.",
           TWO_BATTERIES])

DN_FONTANELLI = force(
    "dennewitz-fontanelli", IT, "Fontanelli's Division", "15th Division, IV Corps (Bertrand)", "French",
    "Bertrand's Italians, who came up beside Morand against Tauentzien's line and were drawn into the fighting round Dennewitz and Rohrbeck as Bülow's corps arrived.",
    [bde("it-infantry-brigade", "Martel's Brigade", "Gén. de Brigade Martel",
         regiments=[bn_list("it-line-infantry", "1st Italian Line", ["3", "4"]), bn_list("it-line-infantry", "4th Italian Line", ["2", "3", "4"])]),
     bde("it-infantry-brigade", "Saint-Andrea's Brigade", "Gén. de Brigade Saint-Andrea",
         regiments=[bn_list("it-light-infantry", "1st Italian Light", ["2", "3", "4"]), bn_list("it-line-infantry", "6th Italian Line", ["3", "4"])]),
     bde("it-infantry-brigade", "Moroni's Brigade", "Gén. de Brigade Moroni",
         regiments=[regt("Milan Guard", [u("it-line-infantry", "1st Milan Guard Battalion")]), bn_list("it-line-infantry", "7th Italian Line", ["2", "3", "4"])]),
     bde("it-divisional-artillery", "Divisional Artillery",
         units=[u("it-foot-arty", "1/1st Italian Foot Battery"), u("it-foot-arty", "13/1st Italian Foot Battery")])],
    command=[cmd("it-div-cmd", "Gén. de Division Fontanelli")],
    notes=["Built from A Clash of Eagles' Italian list, the nearest to 1813.", DN_NOTE,
           "The Milan Guard Battalion, a city guard and not the Royal Guard, is shown as Line.",
           "The division's two foot batteries, where the list allows one, show as a historical departure."])

DN_FRANQUEMONT = force(
    "dennewitz-franquemont", WT, "Franquemont's Division", "38th (Württemberg) Division, IV Corps (Bertrand)", "French",
    "The Württemberg contingent, with Jett's chevau-légers, on Bertrand's left. It fought for Göhlsdorf and Rohrbeck against Bülow's brigades through the afternoon and lost heavily in the rout; after the battle it was down to four combined battalions.",
    [bde("wt-light-infantry-brigade", "Stockmayer's Brigade", "Gen-Maj von Stockmayer",
         units=[u("wt-light-infantry", "I/9th Light"), u("wt-light-infantry", "I/10th Light")],
         regiments=[regt("7th Line", bns("wt-line-infantry", "7th Line", 2))]),
     bde("wt-infantry-brigade", "Spitzenberg's Brigade", "Gen-Maj von Spitzenberg",
         regiments=[regt("1st Line", bns("wt-line-infantry", "1st Line", 2)), regt("2nd Line", [u("wt-line-infantry", "I/2nd Line")])]),
     bde("wt-infantry-brigade", "Döring's Brigade", "Gen-Maj von Döring",
         regiments=[regt("4th Line", bns("wt-line-infantry", "4th Line", 2)), regt("6th Line", bns("wt-line-infantry", "6th Line", 2))]),
     bde("wt-cavalry-brigade", "Jett's Brigade", "Gen-Maj von Jett",
         units=[u("wt-chevauleger", "1st Chevau-légers 'Prince Adam'"), u("wt-chevauleger", "3rd Chevau-légers 'Duke Louis'"),
                u("wt-horse-arty", "1st Horse Battery")]),
     bde("wt-divisional-artillery", "Divisional Artillery", units=[u("wt-light-arty", "1st Württemberg Foot Battery")])],
    command=[cmd("wt-div-cmd", "Gen-Lt Graf Franquemont")],
    notes=["Built from A Clash of Eagles' Württemberg 1812 list, the nearest to 1813.", DN_NOTE,
           "The foot battery, four 6-pdrs and two howitzers, is the list's Light Artillery.",
           "Jett's two regiments had about 300 men between them a fortnight later."])

DN_DOMBROWSKI = force(
    "dennewitz-dombrowski", GDW, "Dombrowski's Division", "27th (Polish) Division, IV Corps (Bertrand)", "French",
    "The Polish division of Bertrand's corps, two infantry regiments and Krukowiecki's light horse, which covered the corps' flank and fell back with it.",
    [bde("gdw-infantry-brigade", "Zoltowski's Brigade", "Gén. de Brigade Zoltowski",
         regiments=[regt("2nd Polish Infantry", bns("gdw-polish-infantry", "2nd Polish", 2)), regt("4th Polish Infantry", bns("gdw-polish-infantry", "4th Polish", 2))]),
     bde("gdw-cavalry-brigade", "Krukowiecki's Brigade", "Gén. de Brigade Krukowiecki",
         units=[u("gdw-uhlan", "2nd Uhlans"), u("gdw-chasseur-a-cheval", "4th Chasseurs à Cheval")])],
    command=[cmd("gdw-div-cmd", "Gén. de Division Dombrowski")],
    notes=["Built from A Clash of Eagles' Grand Duchy of Warsaw list, the nearest to 1813.", DN_NOTE,
           "Nafziger has the 2nd Polish attached to Durutte's division; it is shown here with its own division, as the French list can't take it.",
           "One infantry brigade for its cavalry brigade, where the list wants two, shows as a historical departure."])

DN_SAHR = again(GB_SAHR, "dennewitz-sahr",
                "Reynier's leading Saxon division, which took Göhlsdorf in the afternoon and held it against Bülow's attacks until Borstell's brigade came up on its flank about four; when Oudinot's corps was moved away behind it, the Saxons were left alone, and broke.",
                [LIST_SAX, DN_SAX_NOTE])
DN_LECOQ = again(GB_LECOQ, "dennewitz-lecoq",
                 "Reynier's second Saxon division, fed into the fight for Göhlsdorf beside Sahr's and carried away in the rout when the line broke behind it.",
                 [LIST_SAX, DN_SAX_NOTE])
DN_GABLENZ = again(GB_GABLENZ, "dennewitz-gablenz",
                   "Reynier's Saxon horse, the Hussars and the Prinz Clemens Uhlans, which tried to cover the corps' retreat after Göhlsdorf.",
                   [LIST_SAX, DN_SAX_NOTE])

DN_DURUTTE = force(
    "dennewitz-durutte", FR, "Durutte's Division", "32nd Division, VII Corps (Reynier)", "French",
    "The French division of Reynier's corps, in support of the Saxons at Göhlsdorf, caught up again in their rout.",
    [bde("fr-infantry-brigade", "Devaux's Brigade", "Gén. de Brigade Devaux",
         regiments=[bn_list("fr-light-infantry", "35th Léger", ["1", "4"]), bn_list("fr-line-infantry", "132nd Line", ["1", "3", "4"])]),
     bde("fr-infantry-brigade", "Jarry's Brigade", "Gén. de Brigade Jarry",
         regiments=[bn_list("fr-light-infantry", "36th Léger", ["1", "4"]), bn_list("fr-line-infantry", "131st Line", ["1", "3", "4"])]),
     bde("fr-infantry-brigade", "Menu's Brigade", "Gén. de Brigade Menu",
         regiments=[bn_list("fr-line-infantry", "133rd Line", ["3", "4"]),
                    regt("Würzburg Regiment", [u("fr-rheinbund-infantry", "2/Würzburg"), u("fr-rheinbund-infantry", "3/Würzburg")])]),
     foot("12/1st Foot Artillery", "13/8th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Durutte")],
    notes=[LIST_FR, DN_NOTE, CONSCRIPTS, DN_WEAK,
           "Two light regiments, where the list allows one in a division, and two Würzburg battalions as Rheinbund infantry, where it allows one, show as historical departures.",
           TWO_BATTERIES])

DN_PACTHOD = force(
    "dennewitz-pacthod", FR, "Pacthod's Division", "13th Division, XII Corps (Oudinot)", "French",
    "Oudinot's leading division, which came up late in the afternoon to support Reynier at Göhlsdorf, before Ney ordered the corps away to his left.",
    [bde("fr-infantry-brigade", "Bardet's Brigade", "Gén. de Brigade Bardet",
         regiments=[bn_list("fr-light-infantry", "1st Léger", ["4"]), bn_list("fr-line-infantry", "7th Line", ["3", "4"]), bn_list("fr-line-infantry", "42nd Line", ["4"])]),
     bde("fr-infantry-brigade", "Cacault's Brigade", "Gén. de Brigade Cacault",
         regiments=[bn_list("fr-line-infantry", "67th Line", ["3", "4"]), bn_list("fr-line-infantry", "101st Line", ["2", "3", "4"])]),
     foot("4/4th Foot Artillery", "20/4th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Pacthod")],
    notes=[LIST_FR, DN_NOTE, CONSCRIPTS, DN_WEAK, TWO_BATTERIES])

DN_GUILLEMINOT = force(
    "dennewitz-guilleminot", FR, "Guilleminot's Division", "14th Division, XII Corps (Oudinot)", "French",
    "Oudinot's second French division, moved across the rear of the battle on Ney's order just as Borstell struck Göhlsdorf, and so out of the fight when it was decided.",
    [bde("fr-infantry-brigade", "Gruyer's Brigade", "Gén. de Brigade Gruyer",
         regiments=[bn_list("fr-light-infantry", "18th Léger", ["2", "6"]), bn_list("fr-line-infantry", "156th Line", ["1", "2", "3"])]),
     bde("fr-infantry-brigade", "Brun de Villeret's Brigade", "Gén. de Brigade Brun de Villeret",
         regiments=[regt("Illyrian Regiment", [u("fr-line-infantry", "2/Illyrian Regiment")]),
                    bn_list("fr-line-infantry", "52nd Line", ["3", "4"]), bn_list("fr-line-infantry", "137th Line", ["1", "2", "3"])]),
     foot("2/4th Foot Artillery", "1/8th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Guilleminot")],
    notes=[LIST_FR, DN_NOTE, CONSCRIPTS, DN_WEAK, "The Illyrian battalion is shown as Line.", TWO_BATTERIES])

DN_RAGLOVICH = force(
    "dennewitz-raglovich", BAV, "Raglovich's Division", "29th (Bavarian) Division, XII Corps (Oudinot)", "French",
    "Oudinot's Bavarian division, single battalions of many regiments and two Jäger battalions, which marched off with the rest of the corps at Ney's order and covered the retreat.",
    [bde("bav-infantry-brigade", "Beckers's Brigade", "Gen-Maj von Beckers",
         units=[u("bav-light-infantry", "1st Jäger Battalion")],
         regiments=[bav("3rd and 4th Line", bns_=["II/3rd Line", "I/4th Line"]), bav("8th and 13th Line", bns_=["II/8th Line", "Reserve Battalion, 13th Line"])]),
     bde("bav-infantry-brigade", "Second Brigade", "",
         units=[u("bav-light-infantry", "2nd Jäger Battalion")],
         regiments=[bav("5th and 7th Line", bns_=["II/5th Line", "II/7th Line"]), bav("9th and 10th Line", bns_=["II/9th Line", "II/10th Line"])]),
     bde("bav-divisional-artillery", "Divisional Artillery", units=[u("bav-light-arty", "1st Foot Battery"), u("bav-foot-arty", "2nd Foot Battery")])],
    command=[cmd("bav-div-cmd", "Gen-Lt von Raglovich")],
    notes=[LIST_BAV.replace("; Bavaria had changed sides a fortnight before", ", still on the French side"), DN_NOTE,
           "Its line battalions were each from a different regiment; they are grouped in pairs as the brigades' regiments, as the list takes them.",
           "Nafziger doesn't say what the two foot batteries were; one is shown as the list's Light Artillery, the other as Foot Artillery."])

DN_BEAUMONT = force(
    "dennewitz-beaumont", WP, "Beaumont's Cavalry", "29th Light Cavalry Brigade, XII Corps (Oudinot)", "French",
    "Oudinot's corps cavalry, three regiments of German light horse.",
    [bde("wp-cavalry-brigade", "Wolff's Brigade", "Gen-Maj Wolff",
         units=[u("wp-guard-chevau-leger", "Westphalian Chevau-légers-lanciers"), u("wp-hussar", "Hessian Chevau-légers"), u("wp-hussar", "Bavarian Chevau-légers")])],
    command=[cmd("wp-div-cmd", "Gén. de Division Beaumont")],
    notes=["Built from A Clash of Eagles' Westphalian 1812 list, for its Guard Chevau-légers.", DN_NOTE,
           "The Hessian and Bavarian Chevau-légers are shown as Westphalian Hussars, the list's other light cavalry.",
           "Three regiments, where the list's brigade takes two, and a cavalry brigade with no infantry brigade to allow it, show as historical departures."])

DN_ARRIGHI = force(
    "dennewitz-arrighi", FR, "Arrighi's Cavalry", "III Cavalry Corps", "French",
    "The army's cavalry reserve, squadrons from many regiments, which covered the retreat after the French line broke.",
    [bde("fr-light-cavalry-brigade", "Jacquinot's Brigade", "Gén. de Brigade Jacquinot",
         units=[u("fr-chasseur-a-cheval", "5th Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "10th Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "13th Chasseurs à Cheval")]),
     bde("fr-light-cavalry-brigade", "Merlin's Brigade", "Gén. de Brigade Merlin",
         units=[u("fr-chasseur-a-cheval", "15th Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "21st Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "22nd Chasseurs à Cheval")]),
     bde("fr-light-cavalry-brigade", "Mouriez's Brigade", "Gén. de Brigade Mouriez",
         units=[u("fr-chasseur-a-cheval", "29th Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "31st Chasseurs à Cheval"), u("fr-hussar-regt", "1st Hussars")]),
     bde("fr-light-cavalry-brigade", "Ameil's Brigade", "Gén. de Brigade Ameil",
         units=[u("fr-hussar-regt", "2nd Hussars"), u("fr-hussar-regt", "4th Hussars"), u("fr-hussar-regt", "12th Hussars")]),
     bde("fr-heavy-cavalry-brigade", "Axamitowski's Brigade", "Gén. de Brigade Axamitowski",
         units=[u("fr-dragoon", "4th and 5th Dragoons"), u("fr-dragoon", "12th and 14th Dragoons"), u("fr-dragoon", "24th Dragoons")]),
     bde("fr-heavy-cavalry-brigade", "Quinette's Brigade", "Gén. de Brigade Quinette",
         units=[u("fr-dragoon", "16th and 17th Dragoons"), u("fr-dragoon", "21st and 26th Dragoons"), u("fr-dragoon", "27th Dragoons and 13th Cuirassiers")]),
     bde("fr-divisional-artillery", "Horse Artillery", units=[u("fr-horse-arty", "1/5th Horse Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Arrighi")],
    notes=[LIST_FR, DN_NOTE,
           "Most regiments sent one or two squadrons, so each listed regiment is shown as a unit; the dragoon brigades' many single squadrons are paired, two regiments to a unit, and the 13th Cuirassiers' one squadron rides with the 27th Dragoons.",
           "Ameil's three hussar regiments, where the list's brigade takes two, show as a historical departure. The corps' other horse batteries, more than the list takes, are on the Not in this force card.",
           CAV_ONLY])
DN_ARRIGHI["missing"] = [{"name": "5/5th, 2/1st and 4/6th Horse Artillery", "reason": "The corps' other three horse batteries, more than the list takes."}]

# --- The allies

DN_TAUENTZIEN = force(
    "dennewitz-tauentzien", PR15, "Tauentzien's Corps", "IV Corps, Army of the North", "Prussian",
    "Almost all Landwehr, standing across the road to Jüterbog, it took Bertrand's attack in the morning and held on at Dennewitz for hours against odds until Bülow's corps came in on the French flank.",
    [pi("Dobschütz's Brigade", "Gen-Maj von Dobschütz",
        [("3rd Reserve Infantry", [("M", "I/3rd Reserve Infantry"), ("M", "II/3rd Reserve Infantry"), ("M", "III/3rd Reserve Infantry")]),
         ("1st Kurmark Landwehr", [("L", "I/1st Kurmark Landwehr"), ("L", "II/1st Kurmark Landwehr")]),
         ("1st Silesian Landwehr", [("L", "I/1st Silesian Landwehr"), ("L", "II/1st Silesian Landwehr"), ("L", "III/1st Silesian Landwehr")])],
        [u("pr15-foot-arty", "6-pdr Foot Battery #27")]),
     pi("Lindenau's Brigade", "Col Graf Lindenau",
        [("2nd Neumark Landwehr", [("L", f"{r}/2nd Neumark Landwehr") for r in ("I", "II", "III", "IV")]),
         ("5th Kurmark Landwehr", [("L", f"{r}/5th Kurmark Landwehr") for r in ("I", "II", "III", "IV")])],
        [u("pr15-foot-arty", "Heavy 6-pdr Foot Battery #17")]),
     pc("Landwehr Cavalry", "", [u("pr15-mounted-landwehr", "Berlin Landwehr Cavalry (2 squadrons)"), u("pr15-mounted-landwehr", "2nd Kurmark Landwehr Cavalry (2 squadrons)"),
                                 u("pr15-mounted-landwehr", "2nd Neumark Landwehr Cavalry (2 squadrons)"), u("pr15-mounted-landwehr", "3rd East Prussian Landwehr Cavalry"),
                                 u("pr15-mounted-landwehr", "3rd Pomeranian Landwehr Cavalry"), u("pr15-mounted-landwehr", "7th Kurmark Landwehr Cavalry (Katte)"),
                                 u("pr15-horse-arty", "½ Horse Battery #6", **HALF)], landwehr=True),
     pres(u("pr15-foot-arty", "½ 6-pdr Foot Battery #30", **HALF), u("pr15-horse-arty", "½ Horse Battery #11", **HALF))],
    command=[cmd("pr15-corps-cmd", "Gen-Lt Graf Tauentzien")],
    notes=[PR_LIST, DN_NOTE, PR_GROUPED, PR_SUB,
           "Nafziger gives the corps' infantry as Lindenau's one division; it is split into the two brigades of his Großbeeren return, Dobschütz's and Lindenau's.",
           "A reserve regiment of three musketeer battalions, Landwehr regiments of four battalions, Lindenau's brigade with no line regiment, and six Landwehr cavalry regiments in one brigade, where it takes five, show as historical departures.",
           "The half horse battery #6 rides with the Landwehr cavalry.", PR_ARTY])
DN_TAUENTZIEN["missing"] = [{"name": "Ilovaisky #3 Don Cossacks", "reason": "A Russian Cossack regiment with the corps, which a force from the Prussian list can't take."}]

DN_BULOW = force(
    "dennewitz-bulow", PR15, "Bülow's Corps", "III Corps, Army of the North", "Prussian",
    "Marching to Tauentzien's help, Thümen's and Hesse-Homburg's brigades came in on Bertrand's flank at midday and Krafft's soon after; Borstell, ordered elsewhere, came on his own initiative about four and struck the Saxons at Göhlsdorf. With Oudinot's corps marched away behind them, the French line broke.",
    [pi("4th Brigade (Thümen)", "Gen-Maj von Thümen",
        [("4th East Prussian Infantry", [("M", "I/4th East Prussian Infantry"), ("M", "II/4th East Prussian Infantry"), ("M", "III/4th East Prussian Infantry"), ("F", "F/4th East Prussian Infantry")]),
         ("5th Reserve Infantry", [("M", f"{r}/5th Reserve Infantry") for r in ("I", "II", "III", "IV")]),
         ("Elbe Infantry", [("M", "I/Elbe Infantry"), ("M", "II/Elbe Infantry")])],
        [u("pr15-jager-coy", "2nd Company, East Prussian Jäger"), u("pr15-jager-coy", "3rd Company, East Prussian Jäger"),
         u("pr15-foot-arty", "6-pdr Foot Battery #6")], sub="Col von Stutterheim"),
     pi("3rd Brigade (Hesse-Homburg)", "Gen-Maj Prince Ludwig of Hesse-Homburg",
        [("3rd East Prussian Infantry", [("M", "2nd East Prussian Grenadier Battalion"), ("M", "I/3rd East Prussian Infantry"), ("M", "II/3rd East Prussian Infantry"), ("F", "F/3rd East Prussian Infantry")]),
         ("4th Reserve Infantry", [("M", "I/4th Reserve Infantry"), ("M", "II/4th Reserve Infantry"), ("M", "III/4th Reserve Infantry")]),
         ("3rd East Prussian Landwehr", [("L", f"{r}/3rd East Prussian Landwehr") for r in ("I", "II", "III", "IV")])],
        [u("pr15-hussar-attached", "1st Leib Hussars"), u("pr15-foot-arty", "6-pdr Foot Battery #5")], sub="Lt-Col von Sjöholm"),
     pi("6th Brigade (Krafft)", "Col von Krafft",
        [("Colberg Infantry", [("M", "I/Colberg Infantry"), ("M", "II/Colberg Infantry"), ("F", "F/Colberg Infantry")]),
         ("9th Reserve Infantry", [("M", "I/9th Reserve Infantry"), ("M", "II/9th Reserve Infantry"), ("M", "III/9th Reserve Infantry")]),
         ("1st Neumark Landwehr", [("L", f"{r}/1st Neumark Landwehr") for r in ("I", "II", "III", "IV")])],
        [u("pr15-mounted-landwehr-attached", "1st Pomeranian Landwehr Cavalry"), u("pr15-foot-arty", "6-pdr Foot Battery #16")], sub="Lt-Col von Zastrow"),
     pi("5th Brigade (Borstell)", "Gen-Maj von Borstell",
        [("1st Pomeranian Infantry", [("M", "Pomeranian Grenadier Battalion"), ("M", "I/1st Pomeranian Infantry"), ("M", "II/1st Pomeranian Infantry"), ("M", "III/1st Pomeranian Infantry")]),
         ("2nd Reserve Infantry", [("M", "I/2nd Reserve Infantry"), ("M", "II/2nd Reserve Infantry"), ("F", "F/2nd Reserve Infantry")]),
         ("2nd Kurmark Landwehr", [("L", f"{r}/2nd Kurmark Landwehr") for r in ("I", "II", "III", "IV")])],
        [u("pr15-hussar-attached", "Pomeranian Hussars"), u("pr15-foot-arty", "6-pdr Foot Battery #10")], sub="Lt-Col von Schoon"),
     pc("Brigade Dragoons", "", [u("pr15-dragoon", "Brandenburg Dragoons (3 squadrons)"), u("pr15-dragoon", "West Prussian Dragoons (2 squadrons)")]),
     pc("Reserve Cavalry (Oppen)", "Gen-Maj von Oppen",
        [u("pr15-dragoon", "Queen's Dragoons"), u("pr15-dragoon", "2nd West Prussian Dragoons"), u("pr15-hussar", "Pomeranian National Cavalry"),
         u("pr15-horse-arty", "Horse Battery #5")]),
     pc("Reserve Cavalry (Oppen, Landwehr)", "Gen-Maj von Oppen",
        [u("pr15-mounted-landwehr", "2nd Kurmark Landwehr Cavalry (3 squadrons)"), u("pr15-mounted-landwehr", "4th Kurmark Landwehr Cavalry (3 squadrons)"),
         u("pr15-mounted-landwehr", "2nd Pomeranian Landwehr Cavalry (3 squadrons)"), u("pr15-horse-arty", "½ Horse Battery #6", **HALF)], landwehr=True),
     pres(u("pr15-heavy-arty", "12-pdr Foot Battery #4"), u("pr15-heavy-arty", "12-pdr Foot Battery #5 (2 howitzers)", **HALF),
          u("pr15-foot-arty", "6-pdr Foot Battery #19"))],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Bülow")],
    notes=[PR_LIST, DN_NOTE, PR_GROUPED, PR_SUB,
           "Nafziger lists the 1st Leib Hussars with both Thümen and Hesse-Homburg; they are shown once, with Hesse-Homburg, as at Großbeeren. The Brandenburg Dragoons, attached to Thümen, and the West Prussian Dragoons, to Krafft, are a dragoon brigade of their own.",
           "Each brigade's grenadier battalion is with its first line regiment. Line and reserve regiments of three or more musketeer battalions, Thümen's brigade with no Landwehr and three line regiments, Landwehr regiments of four, two attached hussar regiments where the list allows one, line and Landwehr cavalry brigades together, and two 12-pdr batteries where the corps artillery takes one show as historical departures.",
           "Thümen's 12-pdr battery and Krafft's two 12-pdr howitzers are in the corps artillery."])
DN_BULOW["missing"] = [
    {"name": "Russian 12-pdr Batteries #7 and #21", "reason": "Russian batteries with Thümen and Krafft, which a force from the Prussian list can't take."},
    {"name": "Mörner Hussars and a Swedish horse battery", "reason": "Swedes who came up with Borstell about four; there is no Swedish list."}]

DN_PAHLEN = force(
    "dennewitz-pahlen", RU, "Pahlen's Advance Guard", "Lead elements, Winzingerode's Russian corps", "Russian",
    "The head of Winzingerode's Russian corps, which reached the field about six as the French gave way, and joined the pursuit.",
    [bde("ru-light-cavalry-brigade", "Pahlen's Brigade", "Maj-Gen Baron Pahlen",
         units=[u("ru-hussar", "Izyum Hussars"), u("ru-hussar", "Converged Hussars")]),
     bde("ru-jager-brigade", "44th Jäger", "", regiments=[regt("44th Jäger", bns("ru-jager", "44th Jäger", 2))])],
    command=[cmd("ru-div-cmd", "Maj-Gen Baron Pahlen")],
    notes=[LIST_RU, DN_NOTE, "A Jäger brigade of one regiment, and cavalry with no infantry brigade to allow it, show as historical departures."])

DENNEWITZ = battle(
    "dennewitz", "Dennewitz", "6 September 1813",
    "Ney, sent in Oudinot's place to take Berlin, marched across the front of the Army of the North towards Jüterbog. Bertrand's corps ran into Tauentzien's Landwehr at Dennewitz, which held through the morning until Bülow's corps came in on the French flank at midday. Reynier's Saxons took Göhlsdorf and held it, but as Borstell arrived on their flank about four, Ney ordered Oudinot's corps across the rear of the battle to his other wing; the Saxons were left alone and broke, the French line went with them, and Ney's army streamed back on Torgau, losing some 20,000 men. The Saxons and Bavarians took their defeat as a sign to change sides.",
    [DN_FR, DN_AL, GB, WB_IV, {"label": "Battle of Dennewitz (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Dennewitz"}],
    [DN_MORAND, DN_FONTANELLI, DN_FRANQUEMONT, DN_DOMBROWSKI, DN_SAHR, DN_LECOQ, DN_GABLENZ, DN_DURUTTE,
     DN_PACTHOD, DN_GUILLEMINOT, DN_RAGLOVICH, DN_BEAUMONT, DN_ARRIGHI, DN_TAUENTZIEN, DN_BULOW, DN_PAHLEN],
    [], alliances=(("Saxon", "French"), ("Prussian", "Russian")))


# ================================================================ Plagwitz, 29 August 1813

PW_FR = {"label": "Grande Armée, 15 August 1813 (Nafziger Collection 813HFC)", "url": NAF + "813HFC.pdf"}
PW_RU = {"label": "Army of Silesia, Battle of the Katzbach, 26 August 1813 (Nafziger Collection 813HHB)", "url": NAF + "813HHB.pdf"}
PW_COS = {"label": "Plagwitz (Clash of Steel)", "url": "https://www.clash-of-steel.co.uk/battles/1294"}
PW_HOW = {"label": "Combat of Plagwitz, 29 August 1813 (History of War)", "url": "https://www.historyofwar.org/articles/combat_plagwitz.html"}
PW_RU_NOTE = ("After Nafziger's order of battle for the Katzbach three days before; Nafziger has none for Plagwitz, and Clash of Steel "
              "names the Russian VI Corps and I Cavalry Corps as the troops that caught Puthod.")


def ru_regt(name, n, unit="ru-inf-combined-grenadier"):
    return regt(name, bns(unit, name, n) if n > 1 else [u(unit, name)])


PW_PUTHOD = force(
    "plagwitz-puthod", FR, "Puthod's Division", "17th Division, V Corps (Lauriston)", "French",
    "Sent off to Macdonald's right before the Katzbach, it was cut off by the defeat there and marched west to the Bober, only to find the bridges down and the river in flood. Langeron's Russians caught it at Plagwitz, east of Löwenberg, with the river at its back; it formed on the heights, was broken by the Russian cavalry, and surrendered, Puthod and his eagles with it, many men drowning as they tried to swim the Bober.",
    [bde("fr-infantry-brigade", "Vachot's Brigade", "Gén. de Brigade Vachot",
         regiments=[regt("3rd Foreign (Irish Legion)", bns("fr-line-infantry", "Irish Legion", 2)), line("134th Line", 2), line("146th Line", 3)]),
     bde("fr-infantry-brigade", "Boisserolles's Brigade", "Gén. de Brigade Boisserolles", regiments=[line("147th Line", 3), line("148th Line", 3)]),
     foot("1/5th Foot Artillery", "11/5th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Puthod")],
    notes=[LIST_FR, "After Nafziger's return of the Grande Armée for 15 August, a fortnight before; Nafziger has no order of battle for Plagwitz.",
           CONSCRIPTS, "The Irish Legion (3rd Foreign Regiment), two weak battalions of about 230 men each, is shown as Line.",
           NO_REGT_GUNS, TWO_BATTERIES])

PW_SHCHERBATOV = force(
    "plagwitz-shcherbatov", RU, "Shcherbatov's Corps", "VI Corps, Langeron's corps, Army of Silesia", "Russian",
    "Langeron's infantry, which followed Puthod's column to the Bober and closed on it at Plagwitz as the cavalry pinned it against the river.",
    [bde("ru-infantry-brigade", "Kirschnitzky's Brigade", "Col Kirschnitzky", units=[u("ru-position-arty", "Position Battery #15")],
         regiments=[ru_regt("Pskov Infantry", 2), ru_regt("Moscow Infantry", 2)]),
     bde("ru-infantry-brigade", "Augustov's Brigade", "Col Augustov", units=[u("ru-light-arty", "Light Battery #17")],
         regiments=[ru_regt("Sofia Infantry", 1), ru_regt("Libau Infantry", 2)]),
     bde("ru-jager-brigade", "Dietrich's Brigade", "Col Dietrich",
         regiments=[ru_regt("11th Jäger", 2, "ru-jager"), ru_regt("36th Jäger", 1, "ru-jager")]),
     bde("ru-infantry-brigade", "Blagoveshchensky's Brigade", "Lt-Col Blagoveshchensky", units=[u("ru-light-arty", "Light Battery #28")],
         regiments=[ru_regt("Vladimir Infantry", 1), ru_regt("Dnieper Infantry", 1)]),
     bde("ru-infantry-brigade", "Tambov and Kostroma", "", regiments=[ru_regt("Tambov Infantry", 1), ru_regt("Kostroma Infantry", 1)]),
     bde("ru-jager-brigade", "Meshcherinov's Brigade", "Maj-Gen Meshcherinov",
         regiments=[ru_regt("32nd Jäger", 1, "ru-jager"), ru_regt("28th Jäger", 1, "ru-jager")])],
    command=[cmd("ru-div-cmd", "Lt-Gen Prince Shcherbatov")],
    notes=[LIST_RU, PW_RU_NOTE,
           "Talyzin's 7th Division (the first three brigades) and Bernodossov's 18th (the last three), about 8,300 men in all at the Katzbach; regiments are shown with the battalions Nafziger gives them.",
           "Nafziger also lists the 36th Jäger in Udom's 9th Division; it is shown here only.",
           "Four infantry brigades and two Jäger brigades, where the list allows three and one, show as historical departures."])

PW_KORFF = force(
    "plagwitz-korff", RU, "Korff's Cavalry", "I Cavalry Corps, Langeron's corps, Army of Silesia", "Russian",
    "Langeron's cavalry, which reached Puthod's column on the Plagwitz heights, rode it down against the flooded Bober and took the surrender of most of what was left.",
    [bde("ru-heavy-cavalry-brigade", "Berdyaev's Brigade", "Maj-Gen Berdyaev",
         units=[u("ru-dragoon", "Tver Dragoons"), u("ru-dragoon", "Kinburn Dragoons")]),
     bde("ru-light-cavalry-brigade", "Panchulidzev's Brigade", "Maj-Gen Panchulidzev",
         units=[u("ru-mounted-jager", "Chernigov Mounted Jäger"), u("ru-mounted-jager", "Seversk Mounted Jäger"), u("ru-mounted-jager", "Arzamas Mounted Jäger")]),
     bde("ru-light-cavalry-brigade", "Pahlen's Brigade", "Maj-Gen Count Pahlen",
         units=[u("ru-mounted-jager", "Dorpat Mounted Jäger"), u("ru-mounted-jager", "Lithuania Mounted Jäger"), u("ru-horse-arty", "Horse Battery #6")]),
     bde("ru-cossack-brigade", "Witte's Ukrainian Cossacks", "Maj-Gen Count de Witte",
         units=[u("ru-mounted-cossack", "1st Ukrainian Cossacks"), u("ru-mounted-cossack", "2nd Ukrainian Cossacks"), u("ru-mounted-cossack", "3rd Ukrainian Cossacks")])],
    command=[cmd("ru-div-cmd", "Lt-Gen Baron Korff")],
    notes=[LIST_RU, PW_RU_NOTE,
           "About 4,000 men at the Katzbach, its regiments of two or three squadrons each. The Chasseurs à Cheval are the list's Mounted Jäger, and the Ukrainian Cossack regiments, raised in 1812, its Mounted Cossacks.",
           "Three mounted jäger regiments in Panchulidzev's brigade, where the list takes two, two light cavalry brigades where it allows one, and cavalry with no infantry brigade to allow it, show as historical departures."])

PLAGWITZ = battle(
    "plagwitz", "Plagwitz", "29 August 1813",
    "Puthod's division, detached to Macdonald's right before the Katzbach, was cut off by his defeat there. Marching west in the rain, it found the Bober in flood and its bridges gone at Hirschberg and again at Löwenberg. Langeron's Russians caught it at Plagwitz, east of the river; it stood on the heights with the Bober at its back until the Russian cavalry broke it. Puthod surrendered with his eagles and some 3,000 men; the rest were cut down or drowned trying to swim the river, and of a division of 7,500 almost nothing got away.",
    [PW_FR, PW_RU, PW_COS, PW_HOW],
    [PW_PUTHOD, PW_SHCHERBATOV, PW_KORFF], [], alliances=())


# ================================================================ The Katzbach, 26 August 1813

KB_FR = {"label": "French Forces, Battle of the Katzbach, 26 August 1813 (Nafziger Collection 813HIC)", "url": NAF + "813HIC.pdf"}
KB_AL = {"label": "Army of Silesia, Battle of the Katzbach, 26 August 1813 (Nafziger Collection 813HHB)", "url": NAF + "813HHB.pdf"}
KB_NOTE = "After Nafziger's order of battle for the Katzbach."
KB_WET = ("It rained all day: muskets would hardly fire, and much of the fighting on the plateau was done with bayonet, "
          "butt and sabre.")


def fr_bns(unit, reg, labels):
    return regt(reg, [u(unit, f"{b}/{reg}") for b in labels])


L_, I_ = "fr-light-infantry", "fr-line-infantry"

KB_BRAYER = force(
    "katzbach-brayer", FR, "Brayer's Division", "8th Division, III Corps (Souham)", "French",
    "Souham's leading division, which came up the defile from Kroitsch onto the plateau late in the afternoon as the first French troops there were giving way, and was fed into the fight in the rain against Yorck's and Sacken's lines.",
    [bde("fr-infantry-brigade", "1st Brigade", "",
         regiments=[provisional("6th Provisional Légère", ["2/6th Léger", "3/25th Léger"], True),
                    provisional("10th Provisional Légère", ["3/16th Léger", "1/28th Léger"], True),
                    provisional("14th Provisional Line", ["4/34th Line", "3/40th Line"]),
                    provisional("19th Provisional Line", ["6/32nd Line", "2/58th Line"])]),
     bde("fr-infantry-brigade", "Charrière's Brigade", "Gén. de Brigade Charrière",
         regiments=[fr_bns(I_, "22nd Line", ["1", "3", "4"]),
                    provisional("21st Provisional Line", ["3/59th Line", "4/69th Line"]),
                    provisional("24th Provisional Line", ["3/88th Line", "3/103rd Line"])]),
     foot("10/2nd Foot Artillery", "5/9th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Brigade Brayer")],
    notes=[LIST_FR, KB_NOTE, CONSCRIPTS,
           "Souham's old division, which he led at Lützen and Bautzen; Brayer commanded it under him here. Most of its regiments were provisional, two depot battalions of different regiments each.",
           "Its two provisional light regiments, where the list allows one in a division, and the first brigade's four regiments, where it allows three, show as historical departures.",
           NO_REGT_GUNS, TWO_BATTERIES])

KB_DELMAS = force(
    "katzbach-delmas", FR, "Delmas's Division", "9th Division, III Corps (Souham)", "French",
    "Souham's second division, which followed Brayer's up from the Katzbach and was caught in the crush on the plateau when the allied cavalry broke the French left.",
    [bde("fr-infantry-brigade", "1st Brigade", "",
         regiments=[provisional("2nd Provisional Légère", ["3/2nd Léger", "3/4th Léger"], True), fr_bns(L_, "29th Léger", ["1", "2"]),
                    fr_bns(I_, "136th Line", ["1", "2", "3"])]),
     bde("fr-infantry-brigade", "Vergez's Brigade", "Gén. de Brigade Vergez",
         regiments=[fr_bns(I_, "138th Line", ["1", "2", "3"]), fr_bns(I_, "145th Line", ["1", "2", "3"])]),
     foot("2/9th Foot Artillery", "11/9th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Delmas")],
    notes=[LIST_FR, KB_NOTE, CONSCRIPTS, "Two light regiments, where the list allows one in a division, show as a historical departure.", NO_REGT_GUNS, TWO_BATTERIES])

KB_ALBERT = force(
    "katzbach-albert", FR, "Albert's Division", "10th Division, III Corps (Souham)", "French",
    "Girard's old division, under Albert since Girard was wounded at Lützen, part of Souham's corps marching up from Liegnitz to the plateau.",
    [bde("fr-infantry-brigade", "Van Dedem's Brigade", "Gén. de Brigade Van Dedem",
         regiments=[provisional("4th Provisional Légère", ["4/5th Léger", "4/12th Léger"], True), fr_bns(I_, "139th Line", ["1", "2", "3"])]),
     bde("fr-infantry-brigade", "Suden's Brigade", "Gén. de Brigade Suden",
         regiments=[fr_bns(I_, "140th Line", ["1", "2", "3"]), fr_bns(I_, "141st Line", ["1", "2", "3"])]),
     foot("3/7th Foot Artillery", "4/7th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Albert")],
    notes=[LIST_FR, KB_NOTE, CONSCRIPTS, NO_REGT_GUNS, TWO_BATTERIES])

KB_RICARD = force(
    "katzbach-ricard", FR, "Ricard's Division", "11th Division, III Corps (Souham)", "French",
    "Souham's last division, still marching up when the French on the plateau broke, and swept back with them over the flooded streams.",
    [bde("fr-infantry-brigade", "1st Brigade", "",
         regiments=[fr_bns(L_, "9th Léger", ["3", "4"]), provisional("17th Provisional Line", ["4/43rd Line", "3/75th Line"]),
                    regt("50th and 65th Line", [u(I_, "3/50th Line"), u(I_, "4/50th Line"), u(I_, "4/65th Line")])]),
     bde("fr-infantry-brigade", "Dumoulin's Brigade", "Gén. de Brigade Dumoulin",
         regiments=[fr_bns(I_, "142nd Line", ["1", "2", "3"]), fr_bns(I_, "144th Line", ["1", "2", "3"])]),
     foot("19/7th Foot Artillery", "5/9th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Ricard")],
    notes=[LIST_FR, KB_NOTE, CONSCRIPTS,
           "Nafziger gives the 5/9th Foot Artillery to both Brayer and Ricard; it is shown with each, as he gives it.",
           NO_REGT_GUNS, TWO_BATTERIES])

KB_MARCHAND = force(
    "katzbach-marchand", CR, "Marchand's Division", "39th Division, III Corps (Souham)", "French",
    "Souham's German division, Baden and Hessian troops, which came up behind the French divisions and covered the retreat to the Katzbach.",
    [bde("ocs-baden-infantry-brigade", "Stockhorn's Baden Brigade", "Gen-Maj von Stockhorn",
         units=[u("ocs-foot-arty", "1st Baden Foot Battery")],
         regiments=[regt("1st Baden Line", bns("ocs-line-infantry", "1st Baden Line", 2)), regt("3rd Baden Line", bns("ocs-line-infantry", "3rd Baden Line", 2))]),
     bde("ocs-hessian-infantry-brigade", "Prince Emil's Hessian Brigade", "Gen-Maj Prince Emil of Hesse",
         units=[u("ocs-foot-arty", "1st Hessian Foot Battery")],
         regiments=[regt("Hessian Leib-Garde", bns("ocs-hessian-guard", "Hessian Leib-Garde", 2)),
                    regt("Hessian Garde-Füsiliere", bns("ocs-hessian-guard-fusilier", "Hessian Garde-Füsiliere", 2))]),
     bde("rb-infantry-brigade", "2nd Hessian Leib Regiment", "", regiments=[regt("2nd Hessian (Leib) Regiment", bns("rb-line-infantry", "2nd Hessian Leib", 2))])],
    command=[cmd("cotr-div-cmd", "Gén. de Division Marchand")],
    notes=["Built from A Clash of Eagles' Confederation of the Rhine 1812 list, the nearest to 1813.", KB_NOTE,
           "The list's Hessian brigade takes only Guard regiments, so the 2nd Hessian (Leib) Regiment is a Rheinbund brigade, as at Lützen."])

KB_BEURMANN = force(
    "katzbach-beurmann", FR, "Beurmann's Light Cavalry", "23rd Light Cavalry Brigade, III Corps (Souham)", "French",
    "Souham's corps cavalry, the 10th Hussars and the Baden Dragoons, which rode up onto the plateau with the infantry.",
    [bde("fr-light-cavalry-brigade", "Beurmann's Brigade", "Gén. de Brigade Beurmann", units=[u("fr-hussar-regt", "10th Hussars", options=["large-cavalry"])]),
     bde("fr-heavy-cavalry-brigade", "Baden Dragoons", "", units=[u("fr-dragoon", "Baden Dragoons")])],
    command=[cmd("fr-div-cmd", "Gén. de Brigade Beurmann")],
    notes=[LIST_FR, KB_NOTE, "The 10th Hussars had six squadrons, so they are Large, though the list allows Large on only half a brigade's regiments; the Baden Dragoons, five squadrons, are the list's Dragoons in a heavy brigade of their own.", CAV_ONLY])

KB_MAISON = force(
    "katzbach-maison", FR, "Maison's Division", "16th Division, V Corps (Lauriston)", "French",
    "Lauriston's leading division on the French right, south of the Katzbach, which pushed Langeron's advance guard back towards Hennersdorf before the defeat on the plateau called it back.",
    [bde("fr-infantry-brigade", "Penne's Brigade", "Gén. de Brigade Penne", regiments=[fr_bns(I_, "152nd Line", ["1", "2", "3"])]),
     bde("fr-infantry-brigade", "2nd Brigade", "", regiments=[fr_bns(I_, "153rd Line", ["1", "2", "3"]), fr_bns(I_, "154th Line", ["1", "2", "3"])]),
     foot("1/1st Foot Artillery", "3/1st Foot Artillery"),
     bde("fr-artillery-brigade", "Attached Horse Artillery", units=[u("fr-horse-arty", "7/6th Horse Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Maison")],
    notes=[LIST_FR, KB_NOTE, CONSCRIPTS, "The 151st Line was in Glogau and is left out.", TWO_BATTERIES,
           "The horse battery attached to the division, with no cavalry to allow it, shows as a historical departure."])

KB_ROCHAMBEAU = force(
    "katzbach-rochambeau", FR, "Rochambeau's Division", "19th Division, V Corps (Lauriston)", "French",
    "Lauriston's second division, which fought Langeron's Russians round Hennersdorf on the French right.",
    [bde("fr-infantry-brigade", "Harlet's Brigade", "Gén. de Brigade Harlet", regiments=[fr_bns(I_, "135th Line", ["1", "2", "3"]), fr_bns(I_, "149th Line", ["1", "2", "3"])]),
     bde("fr-infantry-brigade", "Lafitte's Brigade", "Gén. de Brigade Lafitte", regiments=[fr_bns(I_, "150th Line", ["1", "2", "3"]), fr_bns(I_, "155th Line", ["1", "2", "3"])]),
     foot("12/5th Foot Artillery", "17/5th Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Rochambeau")],
    notes=[LIST_FR, KB_NOTE, CONSCRIPTS, TWO_BATTERIES])

KB_DERMONCOURT = force(
    "katzbach-dermoncourt", FR, "Dermoncourt's Light Cavalry", "6th Light Cavalry Brigade, V Corps (Lauriston)", "French",
    "Lauriston's corps cavalry, three regiments of chasseurs, on the French right.",
    [bde("fr-light-cavalry-brigade", "Dermoncourt's Brigade", "Gén. de Brigade Dermoncourt",
         units=[u("fr-chasseur-a-cheval", "2nd Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "3rd Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "6th Chasseurs à Cheval")])],
    command=[cmd("fr-div-cmd", "Gén. de Brigade Dermoncourt")],
    notes=[LIST_FR, KB_NOTE, "The 2nd and 3rd Chasseurs had two squadrons each, the 6th three.", CAV_ONLY])

KB_HENIN = force(
    "katzbach-henin", FR, "D'Henin's Division", "35th Division, XI Corps (Gérard)", "French",
    "Gérard's leading division, French and Zucchi's Italians, which crossed the Katzbach at Niederkrayn and fought on the plateau's southern edge before the rout carried it back.",
    [bde("fr-infantry-brigade", "Senecal's Brigade", "Gén. de Brigade Senecal",
         regiments=[fr_bns(I_, "6th Line", ["3", "4", "7"]), fr_bns(I_, "112th Line", ["1", "2", "3", "4"])]),
     bde("fr-infantry-brigade", "Zucchi's Italian Brigade", "Gén. de Brigade Zucchi",
         regiments=[fr_bns(L_, "2nd Italian Léger", ["3", "4"]), fr_bns(I_, "5th Italian Line", ["1", "2", "3", "4"])]),
     foot("6/1st Foot Artillery"),
     bde("fr-artillery-brigade", "Attached Horse Artillery", units=[u("fr-horse-arty", "3rd Italian Horse Battery")])],
    command=[cmd("fr-div-cmd", "Gén. de Brigade d'Henin")],
    notes=[LIST_FR, KB_NOTE, CONSCRIPTS,
           "Zucchi's Italians are shown as French Line and Light, so the division stays one force; the Italian list would rate them the same.",
           "The Italian horse battery, with no cavalry to allow it, shows as a historical departure."])

KB_CHARPENTIER = force(
    "katzbach-charpentier", FR, "Charpentier's Division", "36th Division, XI Corps (Gérard)", "French",
    "The first French division up onto the plateau, it pushed towards Eichholtz in the rain and was there when Blücher attacked; the Prussian and Russian charges drove it back over the edge into the flooded Wütende Neisse.",
    [bde("fr-infantry-brigade", "Simmer's Brigade", "Gén. de Brigade Simmer",
         regiments=[fr_bns(L_, "22nd Léger", ["1", "2", "3", "4"]), fr_bns(I_, "10th Line", ["4", "6"])]),
     bde("fr-infantry-brigade", "Meunier's Brigade", "Gén. de Brigade Meunier",
         regiments=[fr_bns(L_, "3rd Léger", ["3", "4"]), fr_bns(L_, "14th Léger", ["3", "4", "7"])]),
     foot("5/1st Foot Artillery", "19/2nd Foot Artillery")],
    command=[cmd("fr-div-cmd", "Gén. de Division Charpentier")],
    notes=[LIST_FR, KB_NOTE, CONSCRIPTS, "Three light regiments, where the list allows one in a division, show as a historical departure.", TWO_BATTERIES])

KB_XI_CAV = force(
    "katzbach-xi-cavalry", FR, "Gérard's Corps Cavalry", "Corps Cavalry Brigade, XI Corps", "French",
    "XI Corps' cavalry, Italian and Neapolitan chasseurs, with Gérard's divisions on the plateau's southern edge.",
    [bde("fr-light-cavalry-brigade", "Corps Cavalry Brigade", "",
         units=[u("fr-chasseur-a-cheval", "4th Italian Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "2nd Neapolitan Chasseurs à Cheval")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Gérard")],
    notes=[LIST_FR, KB_NOTE, "The Italian and Neapolitan chasseurs are the list's Chasseurs à Cheval.", CAV_ONLY])
KB_XI_CAV["missing"] = [{"name": "1/Würzburg Chevau-légers", "reason": "One squadron, too few for a unit of its own."}]

KB_SEBASTIANI = force(
    "katzbach-sebastiani", FR, "Sébastiani's Cavalry", "II Cavalry Corps", "French",
    "Some 10,000 horsemen, who crowded up the narrow defiles onto the plateau with Charpentier's infantry and were caught there, half-formed, by the charges of Sacken's and Yorck's cavalry; driven back down into the swollen streams, they lost men and guns by the hundred.",
    [bde("fr-light-cavalry-brigade", "Gérard's Brigade", "Gén. de Brigade Gérard",
         units=[u("fr-hussar-regt", "9th Hussars"), u("fr-lancer", "4th Chevau-légers"), u("fr-hussar-regt", "5th Hussars")]),
     bde("fr-light-cavalry-brigade", "Domanget's Brigade", "Gén. de Brigade Domanget",
         units=[u("fr-lancer", "2nd Chevau-légers"), u("fr-chasseur-a-cheval", "11th Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "12th Chasseurs à Cheval")]),
     bde("fr-light-cavalry-brigade", "Maurin's Brigade", "Gén. de Brigade Maurin",
         units=[u("fr-lancer", "6th Chevau-légers"), u("fr-chasseur-a-cheval", "4th Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "7th Chasseurs à Cheval")]),
     bde("fr-light-cavalry-brigade", "Wathier's Brigade", "Gén. de Brigade Wathier",
         units=[u("fr-chasseur-a-cheval", "20th Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "23rd Chasseurs à Cheval"),
                u("fr-chasseur-a-cheval", "24th Chasseurs à Cheval"), u("fr-hussar-regt", "11th Hussars")]),
     bde("fr-heavy-cavalry-brigade", "Daugeranville's Brigade", "Gén. de Brigade Daugeranville",
         units=[u("fr-carabinier", "1st Carabiniers"), u("fr-carabinier", "2nd Carabiniers"), u("fr-cuirassier", "1st Cuirassiers")]),
     bde("fr-heavy-cavalry-brigade", "Thiry's Brigade", "Gén. de Brigade Thiry",
         units=[u("fr-cuirassier", "5th Cuirassiers"), u("fr-cuirassier", "8th Cuirassiers"), u("fr-cuirassier", "10th Cuirassiers")]),
     bde("fr-divisional-artillery", "Horse Artillery", units=[u("fr-horse-arty", "7/1st Horse Artillery")])],
    command=[cmd("fr-div-cmd", "Gén. de Division Sébastiani")],
    notes=[LIST_FR, KB_NOTE, "The chevau-légers lanciers are the list's Lancers.", CAV_ONLY,
           "The corps' other two horse batteries, more than the list takes, are on the Not in this force card."])
KB_SEBASTIANI["missing"] = [{"name": "7/4th and 8/6th Horse Artillery", "reason": "The corps' other two horse batteries, more than the list takes."}]

# --- Blücher's army

KB_YORCK = force(
    "katzbach-yorck", PR15, "Yorck's Corps", "I Corps, Army of Silesia", "Prussian",
    "Blücher's centre. When the French came up onto the plateau Yorck's brigades went forward against them in the rain, the Landwehr with butt and bayonet as their muskets failed; Jürgass's cavalry charged with Sacken's, and the whole French mass was driven back over the edge into the flooded Katzbach and Wütende Neisse.",
    [pi("1st Brigade (Steinmetz)", "Col von Steinmetz",
        [("Grenadier Battalions", [("M", "East Prussian Grenadier Battalion"), ("M", "Leib Grenadier Battalion"),
                                   ("M", "Silesian Grenadier Battalion"), ("M", "West Prussian Grenadier Battalion")]),
         ("5th Silesian Landwehr", [("L", f"{r}/5th Silesian Landwehr") for r in ("I", "II", "III", "IV")]),
         ("13th Silesian Landwehr", [("L", f"{r}/13th Silesian Landwehr") for r in ("I", "II", "III", "IV")])],
        [u("pr15-jager-coy", "3rd Company, East Prussian Jäger"), u("pr15-jager-coy", "4th Company, East Prussian Jäger"),
         u("pr15-hussar-attached", "2nd Silesian Hussars"), u("pr15-foot-arty", "6-pdr Foot Battery #2")], sub="Col von Hiller"),
     pi("2nd Brigade (Mecklenburg)", "Gen-Maj Prince Karl of Mecklenburg",
        [("1st East Prussian Infantry", [("M", "I/1st East Prussian Infantry"), ("M", "II/1st East Prussian Infantry"), ("F", "F/1st East Prussian Infantry")]),
         ("2nd East Prussian Infantry", [("M", "I/2nd East Prussian Infantry"), ("M", "II/2nd East Prussian Infantry"), ("F", "F/2nd East Prussian Infantry")]),
         ("6th Silesian Landwehr", [("L", f"{r}/6th Silesian Landwehr") for r in ("I", "II", "III", "IV")])],
        [u("pr15-hussar-attached", "Mecklenburg-Strelitz Hussars"), u("pr15-foot-arty", "6-pdr Foot Battery #1")], sub="Lt-Col von Lobenthal"),
     pi("7th Brigade (Horn)", "Gen-Maj von Horn",
        [("Leib Infantry", [("M", "I/Leib Infantry"), ("M", "II/Leib Infantry"), ("F", "F/Leib Infantry")]),
         ("Thuringian Battalion", [("M", "Thuringian Battalion")]),
         ("4th Silesian Landwehr", [("L", f"{r}/4th Silesian Landwehr") for r in ("I", "II", "III", "IV")]),
         ("15th Silesian Landwehr", [("L", f"{r}/15th Silesian Landwehr") for r in ("I", "II", "III", "IV")])],
        [u("pr15-jager-coy", "3rd Company, Guard Jäger"), u("pr15-jager-coy", "4th Company, Guard Jäger"),
         u("pr15-hussar-attached", "Brandenburg Hussars (3 squadrons)"), u("pr15-mounted-landwehr-attached", "3rd Silesian Landwehr Cavalry (2 squadrons)"),
         u("pr15-foot-arty", "6-pdr Foot Battery #3")], sub="Lt-Col von Zepelin"),
     pi("8th Brigade (Hünerbein)", "Gen-Maj von Hünerbein",
        [("Brandenburg Infantry", [("M", "I/Brandenburg Infantry"), ("M", "II/Brandenburg Infantry"), ("F", "F/Brandenburg Infantry")]),
         ("12th Reserve Infantry", [("M", "I/12th Reserve Infantry"), ("M", "II/12th Reserve Infantry"), ("F", "F/12th Reserve Infantry")]),
         ("14th Silesian Landwehr", [("L", f"{r}/14th Silesian Landwehr") for r in ("I", "II", "III", "IV")])],
        [u("pr15-hussar-attached", "Brandenburg Hussars (2 squadrons)"), u("pr15-mounted-landwehr-attached", "3rd Silesian Landwehr Cavalry (2 squadrons)"),
         u("pr15-foot-arty", "6-pdr Foot Battery #15")], sub="Lt-Col von Bork"),
     pc("Reserve Cavalry (Henckel)", "Col Graf Henckel von Donnersmarck",
        [u("pr15-dragoon", "1st West Prussian Dragoons"), u("pr15-dragoon", "Lithuanian Dragoons"), u("pr15-horse-arty", "Horse Battery #1")]),
     pc("Reserve Cavalry (Katzler)", "Col von Katzler",
        [u("pr15-uhlan", "Brandenburg Uhlans"), u("pr15-hussar", "East Prussian National Cavalry"), u("pr15-horse-arty", "Horse Battery #2")]),
     pc("Reserve Cavalry (Bieberstein)", "Maj von Bieberstein",
        [u("pr15-mounted-landwehr", "1st Neumark Landwehr Cavalry"), u("pr15-mounted-landwehr", "5th Silesian Landwehr Cavalry"),
         u("pr15-mounted-landwehr", "10th Silesian Landwehr Cavalry")], landwehr=True),
     pres(u("pr15-heavy-arty", "12-pdr Foot Battery #1"), u("pr15-foot-arty", "6-pdr Foot Battery #12"), u("pr15-horse-arty", "Horse Battery #3"))],
    command=[cmd("pr15-corps-cmd", "Gen-Lt von Yorck")],
    notes=[PR_LIST, KB_NOTE, KB_WET, PR_WHOLE, PR_GROUPED, PR_SUB,
           "The grenadier battalions of Hiller's detachment are one regiment of four; the Landwehr regiments had four battalions each; Horn's brigade had four regiments and Steinmetz's no line regiment but the grenadiers. These, three or more attached hussar regiments where the list allows one, and line and Landwehr cavalry brigades together, show as historical departures.",
           "The Brandenburg Hussars and 3rd Silesian Landwehr Cavalry were split between Horn and Hünerbein, each half shown as attached cavalry. The East Prussian National Cavalry, a volunteer regiment, is shown as Hussars.",
           PR_ARTY])
KB_YORCK["missing"] = [{"name": "12-pdr Foot Battery #2, 6-pdr Foot Battery #24, 3-pdr Foot Battery #1 and Horse Battery #12",
                        "reason": "The rest of the corps' reserve artillery, more than the list's reserve takes."}]

KB_SACKEN = force(
    "katzbach-sacken", RU, "Sacken's Corps", "Right wing, Army of Silesia", "Russian",
    "Blücher's right, on the plateau north of Eichholtz. Its batteries on the Taubenberg tore into the French columns as they came up, and its infantry went forward with Yorck's when the French broke.",
    [bde("ru-infantry-brigade", "Agatin's Brigade", "Maj-Gen Agatin", units=[u("ru-position-arty", "Position Battery #13")],
         regiments=[ru_regt("Yaroslavl Infantry", 2), regt("Okhotsk and Kamchatka Infantry", [u("ru-inf-combined-grenadier", "Okhotsk Infantry"), u("ru-inf-combined-grenadier", "Kamchatka Infantry")])]),
     bde("ru-infantry-brigade", "Sass's Brigade", "Col Sass", units=[u("ru-light-arty", "Light Battery #24")],
         regiments=[ru_regt("Crimea Infantry", 1), ru_regt("Belozersk Infantry", 2)]),
     bde("ru-jager-brigade", "Akhlestyshev's Brigade", "Col Akhlestyshev",
         regiments=[ru_regt("8th Jäger", 2, "ru-jager"), ru_regt("39th Jäger", 2, "ru-jager")]),
     bde("ru-infantry-brigade", "Lewandowsky's Brigade", "Col Lewandowsky", units=[u("ru-position-arty", "Position Battery #28")],
         regiments=[ru_regt("Odessa Infantry", 1), ru_regt("Vilna Infantry", 1)]),
     bde("ru-infantry-brigade", "Alexeyev's Brigade", "Col Alexeyev", units=[u("ru-light-arty", "Light Battery #35")],
         regiments=[ru_regt("Tarnopol Infantry", 1), ru_regt("Simbirsk Infantry", 1)]),
     bde("ru-jager-brigade", "Kollogribov's Brigade", "Col Kollogribov",
         regiments=[ru_regt("49th Jäger", 2, "ru-jager"), ru_regt("50th Jäger", 1, "ru-jager")])],
    command=[cmd("ru-div-cmd", "Gen-Lt Baron Sacken")],
    notes=[LIST_RU, KB_NOTE,
           "Lieven's 10th Division (the first three brigades) and Neverovsky's 27th (the last three), with Repninsky's two battalions of the 16th Division, the Okhotsk and Kamchatka regiments, shown together as one regiment in Agatin's brigade.",
           "Four infantry brigades and two Jäger brigades, where the list allows three and one, show as historical departures."])

KB_VASILCHIKOV = force(
    "katzbach-vasilchikov", RU, "Vasilchikov's Cavalry", "Cavalry, Sacken's corps", "Russian",
    "Sacken's hussars and dragoons, which swung round the French left on the plateau and, with Jürgass's Prussians, rode down Sébastiani's horsemen and broke the French infantry behind them.",
    [bde("ru-heavy-cavalry-brigade", "Panchulidzev's Brigade", "Maj-Gen Panchulidzev", units=[u("ru-dragoon", "Courland Dragoons"), u("ru-dragoon", "Smolensk Dragoons")]),
     bde("ru-light-cavalry-brigade", "Vasilchikov's Brigade", "Col Vasilchikov",
         units=[u("ru-hussar", "Akhtyrka Hussars"), u("ru-hussar", "Mariupol Hussars"), u("ru-horse-arty", "Horse Battery #18")]),
     bde("ru-light-cavalry-brigade", "Kozlovsky's Brigade", "Maj-Gen Kozlovsky", units=[u("ru-hussar", "Alexandria Hussars"), u("ru-hussar", "White Russia Hussars")])],
    command=[cmd("ru-div-cmd", "Gen-Lt Vasilchikov")],
    notes=[LIST_RU, KB_NOTE,
           "Nafziger names Chaplitz as the corps' cavalry commander; Vasilchikov led it in the battle, and leads the force here.",
           "Two light cavalry brigades, where the list allows one, and cavalry with no infantry brigade to allow it, show as historical departures."])

KB_KARPOV = force(
    "katzbach-karpov", RU, "Karpov's Cossacks", "Cossacks, Sacken's corps", "Russian",
    "Sacken's Cossacks, Don regiments with Ukrainian, Kalmyk and Bashkir horse, which harried the French flank and joined the pursuit to the Bober.",
    [bde("ru-cossack-brigade", "Karpov's Brigade", "Maj-Gen Karpov",
         units=[u("ru-mounted-cossack", "Karpov #2 Don Cossacks"), u("ru-mounted-cossack", "Lukovkin Don Cossacks"),
                u("ru-mounted-cossack", "Chernozubov #3 Don Cossacks"), u("ru-mounted-cossack", "Kuteinikov #4 Don Cossacks"),
                u("ru-mounted-cossack", "Semenchenkov Don Cossacks")]),
     bde("ru-cossack-brigade", "Irregulars", "",
         units=[u("ru-mounted-cossack", "Grekov #2 Don Cossacks"), u("ru-mounted-cossack", "4th Ukrainian Cossacks"),
                u("ru-irregular-mounted-cossack", "2nd Kalmyk Regiment"), u("ru-irregular-mounted-cossack", "2nd Bashkir Regiment")])],
    command=[cmd("ru-div-cmd", "Maj-Gen Karpov")],
    notes=[LIST_RU, KB_NOTE, "The Kalmyks and Bashkirs are the list's Irregular Cossacks.",
           "Two Cossack brigades, where the list allows one, and Cossacks with no infantry brigade to allow them show as historical departures."])

KB_OLSUFIEV = force(
    "katzbach-olsufiev", RU, "Olsufiev's Corps", "IX Corps, Langeron's corps, Army of Silesia", "Russian",
    "Part of Langeron's wing south of the Katzbach, which fell back before Lauriston towards Hennersdorf and the Jauer road, then came on again as the French drew off.",
    [bde("ru-infantry-brigade", "Poltaratsky's and Ogryumov's Brigade", "Col Poltaratsky",
         regiments=[ru_regt("Nasheburg Infantry", 1), ru_regt("Yakutsk Infantry", 1), ru_regt("Ryazhsk Infantry", 2)]),
     bde("ru-jager-brigade", "Grimbladt's Brigade", "Maj Grimbladt", regiments=[ru_regt("10th Jäger", 1, "ru-jager"), ru_regt("38th Jäger", 1, "ru-jager")]),
     bde("ru-infantry-brigade", "Tern's Brigade", "Col Tern", units=[u("ru-position-arty", "Position Battery #18")],
         regiments=[ru_regt("Vitebsk Infantry", 1), ru_regt("Kozlov Infantry", 1)]),
     bde("ru-infantry-brigade", "Anensur's Brigade", "Lt-Col Anensur", units=[u("ru-light-arty", "Light Battery #29")],
         regiments=[ru_regt("Kura Infantry", 2), ru_regt("Kolyvan Infantry", 1)]),
     bde("ru-jager-brigade", "Tikhanovsky's Brigade", "Col Tikhanovsky", units=[u("ru-light-arty", "Light Battery #34")],
         regiments=[ru_regt("12th Jäger", 2, "ru-jager"), ru_regt("22nd Jäger", 1, "ru-jager")])],
    command=[cmd("ru-div-cmd", "Gen-Lt Olsufiev")],
    notes=[LIST_RU, KB_NOTE,
           "Udom's 9th Division (the first two brigades) and Rudzevich's 15th (the last three). Udom's two infantry brigades, the Nasheburg regiment alone and the Yakutsk and Ryazhsk together, are shown as one.",
           "Nafziger lists the 36th Jäger in both Udom's and Talyzin's divisions; it is shown with Talyzin's, in Shcherbatov's corps, so Udom's Jäger brigade here has the 10th and the 38th, from his Bautzen return.",
           "Three infantry regiments in one brigade, where the list takes two, and two Jäger brigades, where it allows one, show as historical departures."])

KB_KAPTSEVICH = force(
    "katzbach-kaptsevich", RU, "Kaptsevich's Corps", "X Corps, Langeron's corps, Army of Silesia", "Russian",
    "Langeron's reserve, which came up to stop Lauriston's advance at Hennersdorf in the afternoon and joined the pursuit as the French fell back.",
    [bde("ru-infantry-brigade", "Shindshin's Brigade", "Lt-Col Shindshin",
         regiments=[ru_regt("Arkhangelsk Infantry", 2), ru_regt("Old Ingermanland Infantry", 2)]),
     bde("ru-jager-brigade", "Rerin's Brigade", "Col Rerin",
         regiments=[ru_regt("7th Jäger", 2, "ru-jager"), ru_regt("37th Jäger", 1, "ru-jager")]),
     bde("ru-infantry-brigade", "Shapskoy's Brigade", "Maj-Gen Shapskoy",
         regiments=[ru_regt("Vyatka Infantry", 2), ru_regt("Staroskol Infantry", 2)]),
     bde("ru-jager-brigade", "Durnov's Brigade", "Col Durnov",
         regiments=[ru_regt("29th Jäger", 2, "ru-jager"), ru_regt("45th Jäger", 2, "ru-jager")])],
    command=[cmd("ru-div-cmd", "Gen-Lt Kaptsevich")],
    notes=[LIST_RU, KB_NOTE,
           "Urusov's 8th Division (the first two brigades) and Turchaninov's 22nd (the last two). Rerin's Schlusselburg regiment, a single battalion with two Jäger regiments, and Shapskoy's Olonets battalion are left out, as the list's brigades take them; see Not in this force.",
           "Two Jäger brigades, where the list allows one, show as a historical departure.",
           "Nafziger gives the corps no artillery of its own; Langeron's reserve artillery is left out."])
KB_KAPTSEVICH["missing"] = [{"name": "Schlusselburg and Olonets Infantry", "reason": "Single battalions that don't fit the list's Jäger brigade or its two-regiment infantry brigade."}]

KB_SHCHERBATOV = again(PW_SHCHERBATOV, "katzbach-shcherbatov",
                       "Langeron's leading corps, which held Hennersdorf and the ground before Jauer against Lauriston's divisions through the afternoon.",
                       [LIST_RU, KB_NOTE])
KB_KORFF = again(PW_KORFF, "katzbach-korff",
                 "Langeron's cavalry, which covered his wing as it fell back before Lauriston and then pushed the French back in the evening.",
                 [LIST_RU, KB_NOTE])

KATZBACH = battle(
    "katzbach", "The Katzbach", "26 August 1813",
    "With Napoleon gone to Dresden, Macdonald advanced against Blücher's army in Silesia, crossing the Katzbach and the Wütende Neisse in a downpour. Charpentier's division and Sébastiani's cavalry climbed the narrow defiles onto the plateau beyond and found Sacken's and Yorck's corps waiting for them. Muskets would hardly fire; the Prussian and Russian infantry came on with butt and bayonet, and their cavalry rode down the French horse and drove the whole mass back over the edge into the swollen streams. South of the river Lauriston pushed Langeron back, but fell back himself when the centre broke, and in the pursuit of the next days, Puthod's division among it, Macdonald lost some 30,000 men.",
    [KB_FR, KB_AL, {"label": "Battle of the Katzbach (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Katzbach"}],
    [KB_BRAYER, KB_DELMAS, KB_ALBERT, KB_RICARD, KB_MARCHAND, KB_BEURMANN, KB_MAISON, KB_ROCHAMBEAU, KB_DERMONCOURT,
     KB_HENIN, KB_CHARPENTIER, KB_XI_CAV, KB_SEBASTIANI,
     KB_YORCK, KB_SACKEN, KB_VASILCHIKOV, KB_KARPOV, KB_SHCHERBATOV, KB_OLSUFIEV, KB_KAPTSEVICH, KB_KORFF],
    [], alliances=(("Prussian", "Russian"),))


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
    for b in (MOCKERN, LUTZEN, BAUTZEN, GROSSBEEREN, KATZBACH, HAGELBERG, PLAGWITZ, DENNEWITZ, WARTENBURG, HANAU):
        write(b)
