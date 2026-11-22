"""
Writes the northern flank of the 1812 campaign (src/data/battles/klyastitsy.json): Wittgenstein's I Corps
against Oudinot's II Corps on the road to St Petersburg.

    python3 scripts/forces/russia_1812_north.py && npm run check:forces

Sources (see SOURCES): Nafziger's orders of battle for Jakubovo (812GAA, after Fabry, with Wittgenstein's
corps from 812GBE), dated in the Russian calendar, and the English and Russian Wikipedia articles for how the
fighting went. Summaries are our own words. Staff Ratings are set by ratings.py.
"""

import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from russia_1812 import ru_jager_regiment, ru_regiment

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "battles"
SOURCES = [
    {"label": "French Forces, Battle of Jakobovo, 19 July 1812 [Old Style] (Nafziger Collection 812GAA, after Fabry)",
     "url": "https://www.napoleon-series.org/nafzigger/812GAA.pdf"},
    {"label": "Russian I Corps, 18 July 1812 [Old Style] (Nafziger Collection 812GBE)",
     "url": "https://www.napoleon-series.org/nafzigger/812GBE.pdf"},
    {"label": "Battle of Klyastitsy (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Battle_of_Klyastitsy"},
    {"label": "Сражение под Клястицами (Russian Wikipedia)",
     "url": "https://ru.wikipedia.org/wiki/%D0%A1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5_%D0%BF%D0%BE%D0%B4_%D0%9A%D0%BB%D1%8F%D1%81%D1%82%D0%B8%D1%86%D0%B0%D0%BC%D0%B8"},
]
FR, RU = "france", "russia"
FR_GUNS = "Nafziger (after Fabry) gives each regiment its artillery company, two or four 3-pdrs, shown as Regimental Artillery; he notes it isn't certain they were with their regiments in the field."


def fr_regiment(name, n, light=False):
    unit = "fr-light-infantry" if light else "fr-line-infantry"
    return {"name": name, "units": [u(unit, f"{['I', 'II', 'III', 'IV', 'V'][i]}/{name}") for i in range(n)]}


# ---------------------------------------------------------------- Oudinot's II Corps

LEGRAND = force("klyastitsy-legrand", FR, "Legrand's Division", "6th Division, II Corps (Oudinot)", "French",
                "Oudinot's leading division, which found Kulnev's advance guard at Yakubovo on the afternoon of 30 July and fought it all day, pushing it back to the woods until the Russian horse guns stopped the attack. Next morning it took the weight of Wittgenstein's whole corps and was driven back through Klyastitsy over the Nishcha.",
                [bde("fr-infantry-brigade", "Albert's Brigade", "Gén. de Brigade Albert",
                     units=[u("fr-regimental-arty-section", "26th Léger Artillery Company")],
                     regiments=[fr_regiment("26th Léger", 4, light=True)]),
                 bde("fr-infantry-brigade", "Maison's Brigade", "Gén. de Brigade Maison",
                     units=[u("fr-regimental-arty-section", "19th Line Artillery Company")],
                     regiments=[fr_regiment("19th Line", 4)]),
                 bde("fr-infantry-brigade", "Moreau's Brigade", "Gén. de Brigade Moreau",
                     units=[u("fr-regimental-arty-section", "56th Line Artillery Company")],
                     regiments=[fr_regiment("56th Line", 4)]),
                 bde("fr-divisional-artillery", "Divisional Artillery",
                     units=[u("fr-foot-arty", "11/5th Foot Artillery"), u("fr-horse-arty", "6/3rd Horse Artillery")])],
                command=[cmd("fr-div-cmd", "Gén. de Division Legrand")],
                notes=["After Nafziger: three brigades of one four-battalion regiment each, about 7,000 men.", FR_GUNS,
                       "The horse battery, without the three cavalry regiments the list wants for it, shows as a historical departure."])

VERDIER = force("klyastitsy-verdier", FR, "Verdier's Division", "8th Division, II Corps (Oudinot)", "French",
                "Joined Legrand at Yakubovo late on 30 July and shared the defeat next day. On 1 August, as Oudinot turned at Boyarshchina, it caught Kulnev's pursuing advance guard coming out of the woods and broke it, and then held off Wittgenstein's counter-attack at Golovchitsy.",
                [bde("fr-infantry-brigade", "Vives's Brigade", "Gén. de Brigade Vives",
                     units=[u("fr-regimental-battery", "11th Léger Artillery Company"), u("fr-regimental-battery", "2nd Line Artillery Company")],
                     regiments=[fr_regiment("11th Léger", 4, light=True), fr_regiment("2nd Line", 5)]),
                 bde("fr-infantry-brigade", "Pouget's Brigade", "Gén. de Brigade Pouget",
                     units=[u("fr-regimental-battery", "37th Line Artillery Company"), u("fr-regimental-arty-section", "124th Line Artillery Company")],
                     regiments=[fr_regiment("37th Line", 4), fr_regiment("124th Line", 3)]),
                 bde("fr-divisional-artillery", "Divisional Artillery",
                     units=[u("fr-foot-arty", "15/5th Foot Artillery"), u("fr-horse-arty", "1/3rd Horse Artillery")])],
                command=[cmd("fr-div-cmd", "Gén. de Division Verdier")],
                notes=["After Nafziger: sixteen battalions, about 10,000 men. The 124th was a Dutch regiment, raised from the old Dutch army.", FR_GUNS,
                       "Pouget's brigade mixes a regimental battery (the 37th's four guns) with a section (the 124th's two), and the horse battery has none of the three cavalry regiments the list wants for it; both show as historical departures."])

OUDINOT_CAVALRY = force("klyastitsy-cavalry", FR, "Castex's and Doumerc's Cavalry", "5th Light Cavalry Brigade and 3rd Cuirassier Division, II Corps (Oudinot)", "French",
                        "The corps' light cavalry and the cuirassier division lent to Oudinot, which came up to the Nishcha after the first day and covered the retreat towards Polotsk.",
                        [bde("fr-light-cavalry-brigade", "Castex's Brigade", "Gén. de Brigade Castex",
                             [u("fr-chasseur-a-cheval", "23rd Chasseurs à Cheval"), u("fr-chasseur-a-cheval", "24th Chasseurs à Cheval")]),
                         bde("fr-heavy-cavalry-brigade", "Doumerc's Cuirassiers", "Gén. de Division Doumerc",
                             [u("fr-cuirassier", "4th Cuirassiers"), u("fr-cuirassier", "7th Cuirassiers"), u("fr-cuirassier", "14th Cuirassiers")]),
                         bde("fr-artillery-brigade", "Doumerc's Horse Artillery",
                             units=[u("fr-horse-arty", "1/6th Horse Artillery"), u("fr-horse-arty", "3/6th Horse Artillery")])],
                        command=[cmd("fr-div-cmd", "Gén. de Division Doumerc")],
                        notes=["After Nafziger. Doumerc's three brigades had a regiment each (Berkheim's 4th, L'Héritier's 7th, Doullembourg's 14th Cuirassiers), shown together as one brigade.",
                               "The accounts don't say where the cavalry fought; Wikipedia has it put at Oudinot's disposal for the second day.",
                               "Cavalry without infantry, and the second horse battery, show as historical departures."])

# ---------------------------------------------------------------- Wittgenstein's I Corps

KULNEV = force("klyastitsy-kulnev", RU, "Kulnev's Advance Guard", "Advance Guard, I Corps (Wittgenstein)", "Russian",
               "About 3,700 men with twelve horse guns. It met Legrand at Yakubovo on 30 July and held through the day, Sukhozanet's horse battery losing more than a third of its gunners. After the victory it was sent after Oudinot, and on 1 August, coming out of the woods at Boyarshchina onto open ground before the whole French corps, it was broken, and Kulnev killed by a cannonball.",
               [bde("ru-light-cavalry-brigade", "Kulnev's Cavalry", "Maj-Gen Kulnev",
                    [u("ru-hussar", "Grodno Hussars", options=["large-cavalry"]), u("ru-mounted-cossack", "Platov IV's Don Cossacks", options=["small-cavalry"]),
                     u("ru-horse-arty", "1st Horse Battery (Sukhozanet)")]),
                bde("ru-jager-brigade", "Denisyev's Brigade", "Col Denisyev",
                    regiments=[ru_jager_regiment("25th"), ru_jager_regiment("26th")])],
               command=[cmd("ru-div-cmd", "Maj-Gen Kulnev")],
               notes=["After Nafziger. The Grodno Hussars had eight squadrons, so they are Large; Platov IV's Cossacks, 370 men, are Small.",
                      "No Infantry Brigade, and a horse battery with only two cavalry regiments, show as historical departures."])

BERG = force("klyastitsy-berg", RU, "Berg's First Line", "5th Division, I Corps (Wittgenstein)", "Russian",
             "The corps' main line, sent forward to Yakubovo on the evening of 30 July with the 23rd and 24th Jäger and more guns. Before dawn next day Berg led the whole first line forward; the 23rd Jäger stormed the manor at Yakubovo, the Sevsk and Kaluga regiments drove into the French centre, and Oudinot fell back over the Nishcha.",
             [bde("ru-infantry-brigade", "Prince Sibirsky's Brigade", "Maj-Gen Prince Sibirsky",
                  units=[u("ru-light-arty", "27th Light Battery")],
                  regiments=[ru_regiment("Perm"), ru_regiment("Mogilev")]),
              bde("ru-infantry-brigade", "Kazachkovsky's Brigade", "Col Kazachkovsky",
                  units=[u("ru-light-arty", "9th Light Battery")],
                  regiments=[ru_regiment("Sevsk"), ru_regiment("Kaluga")]),
              bde("ru-jager-brigade", "Frolov's Brigade", "Col Frolov",
                  units=[u("ru-position-arty", "5th Position Battery"), u("ru-position-arty", "14th Position Battery")],
                  regiments=[ru_jager_regiment("23rd"), ru_jager_regiment("24th")])],
             command=[cmd("ru-div-cmd", "Maj-Gen Berg")],
             notes=["After Nafziger, who names Colonel Lukov for the Sevsk and Kaluga brigade; the Russian account has Kazachkovsky leading it in the attack of 31 July.",
                    "Two Position Batteries in one brigade, where it takes one, shows as a historical departure."])

KAKHOVSKY = force("klyastitsy-kakhovsky", RU, "The Second Line", "Grenadiers and Dragoons, I Corps (Wittgenstein)", "Russian",
                  "The corps' grenadiers and dragoons behind the first line. When Oudinot burned the only bridge over the Nishcha, a battalion of the Pavlovsky grenadiers ran across it while it burned, and the pursuit went on.",
                  [bde("ru-combined-grenadier-brigade", "Converged Grenadiers", "",
                       units=[u("ru-inf-combined-grenadier", f"Converged Grenadiers {i}, 5th and 14th Divisions") for i in (1, 2, 3, 4)]
                       + [u("ru-position-arty", "27th Position Battery")]),
                   bde("ru-combined-grenadier-brigade", "Reserve Grenadiers", "",
                       [u("ru-inf-combined-grenadier", f"{r} Grenadiers (Reserve Bn)", options=["small"])
                        for r in ("Leib", "Tauride", "Ekaterinoslav", "Pavlovsky", "Arakcheyev", "St Petersburg")]),
                   bde("ru-heavy-cavalry-brigade", "Balk's Dragoons", "Maj-Gen Balk",
                       [u("ru-dragoon", "Riga Dragoons"), u("ru-dragoon", "Yamburg Dragoons"), u("ru-horse-arty", "3rd Horse Battery")])],
                  command=[cmd("ru-div-cmd", "Lt-Gen Kakhovsky")],
                  notes=["After Nafziger: four converged grenadier battalions of the 5th and 14th Divisions, and the reserve battalions of six grenadier regiments, 1,581 men, so each Small.",
                         "Two Combined Grenadier Brigades where the list allows one, and a horse battery with only two cavalry regiments, show as historical departures."])

SAZONOV = force("klyastitsy-sazonov", RU, "Sazonov's Reserve", "14th Division, I Corps (Wittgenstein)", "Russian",
                "Held back at Katerinovo with Repnin's depot cavalry while the first line fought on 30 and 31 July, it marched to the Drissa that night to support Kulnev, and came up as the corps struck back at Verdier on 1 August.",
                [bde("ru-infantry-brigade", "Harpe's Brigade", "Col Harpe",
                     units=[u("ru-light-arty-half", "Half of the 26th Light Battery")],
                     regiments=[ru_regiment("Tula"), ru_regiment("Navaginsk")]),
                 bde("ru-infantry-brigade", "Helfreich's Brigade", "Maj-Gen Helfreich",
                     units=[u("ru-light-arty-half", "Half of the 26th Light Battery")],
                     regiments=[ru_regiment("Tenginsk"), ru_regiment("Estonia")])],
                command=[cmd("ru-div-cmd", "Maj-Gen Sazonov")],
                notes=["After Nafziger: eight battalions, about 4,500 men, with the 26th Light Battery split between the brigades.",
                       "Repnin's reserve of depot cavalry, a converged Jäger battalion and the 26th Position Battery, about 1,600 men, stayed with it; it isn't included.",
                       "The two halves of one light battery count as two batteries against the list's one per six battalions, which shows as a historical departure."])

KLYASTITSY = {"id": "klyastitsy", "name": "Klyastitsy", "date": "30 July – 1 August 1812", "campaign": "russia-1812",
              "summary": "On the road to St Petersburg, Wittgenstein turned on Oudinot's II Corps instead of waiting for it. Kulnev's advance guard met Legrand at Yakubovo and held all day; before dawn next morning the whole Russian corps attacked, broke the French centre and drove Oudinot back through Klyastitsy, a grenadier battalion running across the burning bridge. Pursuing too far, Kulnev was caught and killed at Boyarshchina on 1 August, but Oudinot fell back on Polotsk, and the threat to the capital was over.",
              "sources": SOURCES,
              "forces": [LEGRAND, VERDIER, OUDINOT_CAVALRY, KULNEV, BERG, KAKHOVSKY, SAZONOV]}


if __name__ == "__main__":
    art = json.loads((Path(__file__).parent / "art.json").read_text())["battles"]
    for b in (KLYASTITSY,):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in art:
            b["art"] = art[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
