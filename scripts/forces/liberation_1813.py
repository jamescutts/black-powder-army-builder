"""
Writes the forces of the War of Liberation (src/data/battles/{mockern,lutzen,bautzen,grossbeeren,wartenburg}.json):
the French, their German and Italian allies, and the Russians, from Nafziger's orders of battle. The Prussians
are built from the 1815 Prussian list, one force a corps.

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
    """A Prussian battalion; a grenadier battalion with the list's Veteran upgrade"""
    return u(KIND[kind], name, **({"options": ["veteran-infantry"]} if "Grenadier" in name else {}))


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
       [u("pr15-dragoon", "Garde du Corps"), u("pr15-hussar", "Guard Light Cavalry"), u("pr15-horse-arty", "Guard Horse Battery #4")]),
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
         u("pr15-foot-arty", "Guard 6-pdr Foot Battery #4")], sub="Lt-Col von Tippelskirch"),
     pc("Brandenburg Cavalry (Katzler)", "Lt-Col von Katzler",
        [u("pr15-uhlan", "West Prussian Uhlans"), u("pr15-hussar", "Brandenburg Hussars (2 squadrons)"), u("pr15-horse-arty", "Horse Battery #8")]),
     *DOLFFS,
     pres(u("pr15-heavy-arty", "½ 12-pdr Foot Battery #3", **HALF), u("pr15-foot-arty", "6-pdr Foot Battery #13"),
          u("pr15-foot-arty", "6-pdr Foot Battery #9"))],
    command=[{"unit": "pr15-cmd-blucher"}],
    notes=[PR_LIST, LZ_PR_NOTE, "Blücher is the book's named commander.", PR_WHOLE, PR_SPRING, PR_GROUPED, PR_SUB, GUARD, CUIRASSIERS,
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
         u("pr15-foot-arty", "Guard Foot Battery #4")], sub="Lt-Col von Tippelskirch"),
     pc("Brandenburg Cavalry (Katzler)", "Lt-Col von Katzler",
        [u("pr15-uhlan", "West Prussian Uhlans"), u("pr15-hussar", "Brandenburg Hussars (2 squadrons)"),
         u("pr15-hussar", "2nd Leib Hussars"), u("pr15-horse-arty", "Horse Battery #8")]),
     *DOLFFS,
     pres(u("pr15-foot-arty", "6-pdr Foot Battery #13"))],
    command=[{"unit": "pr15-cmd-blucher"}],
    notes=[PR_LIST, BZ_PR_NOTE, "Blücher is the book's named commander.", PR_WHOLE, PR_SPRING, PR_GROUPED, PR_SUB, GUARD, CUIRASSIERS,
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
    for b in (MOCKERN, LUTZEN, BAUTZEN, GROSSBEEREN, WARTENBURG):
        write(b)
