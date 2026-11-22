"""
Writes three more of the Peninsular War's battles (src/data/battles/{medina-de-rioseco,bailen,bussaco}.json).

    python3 scripts/forces/peninsular_early.py && npm run check:forces

Sources (see each battle's sources): Nafziger's orders of battle (808GSAT, 808GSAG, 808GSAH, 810ISAC, 810ISAD),
after Oman, Clerc and the Spanish army's Estados of 1822, with Wikipedia for the course of each battle. Summaries
are our own words; ratings.py sets Staff Ratings as each battle is written.
"""

import json
from pathlib import Path

import commanders
import ratings
from hundred_days import bde, cmd, force, u
from peninsular import ART, OUT, PB, PF, SP, ARTILLERY, highland, line, pb_battery, pb_bde, pf_battery, pf_bde, pf_cav, pf_regiment
from peninsular_more import AP, R, fr_div, kgl, pt_bde, rifles, wiki


def naf(code, title):
    return {"label": f"{title} (Nafziger Collection {code})", "url": f"https://www.napoleon-series.org/nafzigger/{code}.pdf"}


def sp(unit, name, **kw):
    return u(unit, name, **kw)


def sp_reg(name, n=1):
    return {"name": name, "units": [u("sp-line", f"{['I', 'II', 'III'][i]}/{name}" if n > 1 else name) for i in range(n)]}


def sp_bde(name, commander, regiments=(), units=()):
    return bde("sp-infantry-brigade", name, commander, units=list(units), regiments=list(regiments))


def sp_cav(name, commander, units):
    return bde("sp-cavalry-brigade", name, commander, units)


def sp_guns(name, unit="sp-artillery"):
    return bde("sp-artillery-support", name, units=[u(unit, name)])


SP_BRIGADES = "Nafziger lists each division's units without brigades; the brigades here are ours, grouping its regiments as the list builds them."
SP_CAV = "The Spanish cavalry regiments were mere squadrons, a hundred or so men, so they are Small; a cavalry brigade of them, short of the heavy regiments it needs, shows as a historical departure."
CAVALRY_ONLY = "Cavalry on its own has no infantry brigades for its brigades to go with, which shows as a historical departure."


# ================================================================ Medina de Rioseco, 14 July 1808

LASALLE = force("medina-lasalle", PF, "Lasalle's Division", "Bessières's Corps of the Western Pyrenees", "French",
                "Bessières's cavalry with Sabatier's brigade of provisional infantry. Lasalle's chasseurs rode down the Spanish left as Merle's infantry climbed the Monclin heights, and swept the field when the Spanish line broke.",
                [pf_cav("Lasalle's Brigade", "Gén. de Brigade Lasalle", [("10e", "Chasseurs"), ("22e", "Chasseurs")]),
                 pf_bde("Sabatier's Brigade", "Gén. de Brigade Sabatier", [pf_regiment("17th Provisional", 2), pf_regiment("18th Provisional", 2)]),
                 pf_battery("Foot Battery")],
                command=[cmd("pf-div-cmd", "Gén. de Division Lasalle")],
                notes=["After Nafziger. The provisional regiments were raw conscript battalions, soon merged into the 120th Line; mark them Unreliable if you like."])

MERLE = force("medina-merle", PF, "Merle's Division", "Bessières's Corps of the Western Pyrenees", "French",
              "Turned the Spanish left on the Monclin heights and then, with the Guard's fusiliers, drove into the gap between Blake's and Cuesta's armies, breaking Blake's line.",
              [pf_bde("Darmagnac's Brigade", "Gén. de Brigade Darmagnac",
                      [pf_regiment("47th", 1), {"name": "86th Ligne (two companies) and 3rd Swiss", "units": [u("pf-line", "Two companies, 86th Ligne", options=["small"]), u("pf-line", "II/3rd Swiss")]}]),
               pf_bde("Ducos's Brigade", "Gén. de Brigade Ducos", [pf_regiment("13th Provisional", 1), pf_regiment("14th Provisional", 4)]),
               pf_battery("Foot Battery")],
              command=[cmd("pf-div-cmd", "Gén. de Division Merle")],
              notes=["After Nafziger. The 13th and 14th Provisional, conscripts, were soon merged into the 119th Line."])

MOUTON = force("medina-mouton", PF, "Mouton's Division", "Bessières's Corps of the Western Pyrenees", "French",
               "Bessières's other division, which struck Cuesta's army as it came forward too late to save Blake's, and drove it from the field and through the town of Medina.",
               [pf_bde("Reynaud's Brigade", "Gén. de Brigade Reynaud", [pf_regiment("4e", 3, "Léger"), pf_regiment("15e", 3)]),
                pf_bde("Rey's Brigade", "Gén. de Brigade Rey", [pf_regiment("2e", 1, "Léger"), pf_regiment("12e", 1, "Léger")]),
                pf_cav("Provisional Cuirassiers", "", [("Provisional Squadron of", "Dragons")]),
                pf_battery("Foot Battery")],
               command=[cmd("pf-div-cmd", "Gén. de Division Mouton")],
               notes=["After Nafziger, who doesn't give Rey's battalions; one each is shown.",
                      "The provisional squadron of cuirassiers and carabiniers is shown as the list's Dragoons, as a cavalry brigade of one, below the two regiments it needs; both that and Rey's two Light regiments show as historical departures."])

GUARD_BURGOS = force("medina-guard", PF, "The Guard Detachment", "From the garrison of Burgos", "French",
                     "Two battalions of the Imperial Guard's fusiliers with small detachments of Guard cavalry, brought from Burgos. They followed Merle into the gap in the Spanish centre.",
                     [bde("pf-young-guard-brigade", "Guard Fusiliers", "",
                          [u("pf-young-guard", "Fusiliers-Chasseurs"), u("pf-young-guard", "Fusiliers-Grenadiers")]),
                      bde("pf-guard-cavalry-brigade", "Guard Cavalry Detachments", "",
                          [u("pf-guard-light", "Chasseurs à Cheval of the Guard", options=["small"]), u("pf-guard-lancer", "Polish Light Horse of the Guard", options=["small"]),
                           u("pf-empress-dragoon", "Dragoons of the Guard", options=["small"])]),
                      pf_battery("Foot Battery")],
                     command=[cmd("pf-div-cmd", "Gén. de Brigade Dorsenne")],
                     notes=["After Nafziger: about 1,900 fusiliers and 290 Guard cavalry in three detachments, so each Small, with ten guns. The Fusiliers are shown as the list's Young Guard.",
                            "Guard brigades without the infantry and cavalry brigades they need show as historical departures."])

BLAKE = force("medina-blake", SP, "Blake's Army of Galicia", "Vanguard, 1st and 4th Divisions", "Spanish",
              "Blake's regulars and militia held the low ridge in front of Medina. Merle's attack turned their left on the Monclin heights; Blake's counter-attack was beaten off, and when the French drove between his army and Cuesta's the Galicians broke, losing their guns.",
              [sp_bde("Maceda's Vanguard", "Brig Conde de Maceda",
                      regiments=[sp_reg("Zaragoza")],
                      units=[sp("sp-grenadier", "Converged Grenadiers"), sp("sp-light", "Voluntarios de Gerona", options=["small"]),
                             sp("sp-light", "Voluntarios de Cataluña", options=["small"])]),
               sp_bde("Cagigal's 1st Division", "Mariscal de Campo Cagigal",
                      regiments=[sp_reg("Rey", 2), sp_reg("Hibernia", 2), sp_reg("Mallorca")],
                      units=[sp("sp-grenadier", "Militia Grenadiers of Galicia"), sp("sp-militia", "Salamanca Militia"), sp("sp-militia", "Mondoñedo Militia"),
                             sp("sp-militia", "Tuy Militia"), sp("sp-militia", "Buenos Aires Provincial Battalion"), sp("sp-light", "Voluntarios de Barbastro", options=["small"])]),
               sp_bde("Portago's 4th Division", "Mariscal de Campo Marqués de Portago",
                      regiments=[sp_reg("Príncipe", 2), sp_reg("Toledo", 2), sp_reg("Aragón", 2)],
                      units=[sp("sp-grenadier", "Converged Grenadiers"), sp("sp-light", "Navarra Light Battalion")]),
               sp_cav("Vanguard Cavalry", "", [sp("sp-heavy", "Montesa Cavalry", options=["small"]), sp("sp-heavy", "Reina Dragoons", options=["small"])]),
               sp_guns("4th Artillery, Vanguard"), sp_guns("4th Artillery, 1st Division"), sp_guns("4th Artillery, 4th Division")],
              command=[cmd("sp-div-cmd", "Lt-Gen Joaquín Blake")],
              notes=["After Nafziger. Each division is shown as one brigade; the half-battalions of volunteers are Small light battalions.",
                     "The 1st Division's Militia Grenadiers were two battalions; one is shown. More Militia and Line regiments in a brigade than the list allows show as historical departures.",
                     SP_CAV, "Three batteries of five or six guns for twenty-odd battalions show as a historical departure."])

CUESTA = force("medina-cuesta", SP, "Cuesta's Army of Castile", "1st and 2nd Divisions", "Spanish",
               "Cuesta's half-trained levies, posted apart from Blake's army, came forward too late to save it and were broken in their turn by Mouton's division, the Leon volunteers and the guardsmen of the Garde du Corps fighting hardest.",
               [sp_bde("1st Division", "", regiments=[sp_reg("Córdoba")],
                       units=[sp("sp-militia", "I/Voluntarios de León"), sp("sp-militia", "II/Voluntarios de León")]),
                sp_bde("2nd Division", "", units=[sp("sp-militia", "III/Voluntarios de León"), sp("sp-militia", "Tercios de Castilla")]),
                sp_cav("Cuesta's Cavalry", "", [sp("sp-heavy", "Garde du Corps", options=["guard-heavy", "small"]), sp("sp-heavy", "Royal Carabiniers", options=["small"]),
                                                 sp("sp-heavy", "Reina Dragoons", options=["small"])])],
               command=[cmd("sp-div-cmd", "Capt-Gen Gregorio de la Cuesta")],
               notes=["After Nafziger: about 10,000 infantry and 560 cavalry, with no guns. The volunteers and tercios, newly raised, are shown as Militia.",
                      "A brigade of only Militia, without the Line regiment it needs, shows as a historical departure.", SP_CAV])

MEDINA = {
    "id": "medina-de-rioseco", "name": "Medina de Rioseco", "date": "14 July 1808", "campaign": "peninsular-war",
    "summary": "Blake's Army of Galicia and Cuesta's Army of Castile, drawn up apart on the open plain north of Valladolid, were beaten in turn by Bessières's smaller corps. Merle turned Blake's left and drove between the two armies; Mouton then broke Cuesta's, and the road to Madrid lay open for King Joseph.",
    "sources": [naf("808GSAT", "Battle of Medina de Rio Seco, 14 July 1808"), wiki("Battle_of_Medina_de_Rioseco", "Battle of Medina de Rioseco")],
    "forces": [LASALLE, MERLE, MOUTON, GUARD_BURGOS, BLAKE, CUESTA],
}


# ================================================================ Bailén, 19 July 1808

LEGIONS = "The Legions of Reserve were raw conscripts; mark them Unreliable if you like."

BARBOU = force("bailen-barbou", PF, "Barbou's Division", "1st Division, Dupont's Corps", "French",
               "Dupont's leading division, which marched into the Spanish army across the road at Bailén at dawn and attacked again and again through the heat of the day, until its men were spent and their water gone.",
               [pf_bde("Chabert's Brigade", "Gén. de Brigade Chabert", [pf_regiment("4th Legion of Reserve", 3, "Ligne"), pf_regiment("4th Swiss", 1)]),
                pf_bde("Pannetier's Brigade", "Gén. de Brigade Pannetier", [pf_regiment("3rd Legion of Reserve", 2, "Ligne"), pf_regiment("Garde de Paris", 2)]),
                pf_battery("Foot Battery")],
               command=[cmd("pf-div-cmd", "Gén. de Division Barbou")],
               notes=["After Nafziger.", LEGIONS, "The corps' 36 guns were mostly lost on the road; one battery is shown with each division."])

FRERE = force("bailen-frere", PF, "Frère's Division", "3rd Division, Dupont's Corps", "French",
              "Schramm's brigade of Swiss in Spanish service, with a battalion of the Guard's seamen. In the last attack many of the Swiss went over to their countrymen in Reding's division.",
              [pf_bde("Schramm's Brigade", "Gén. de Brigade Schramm", [pf_regiment("Reding Swiss", 2), pf_regiment("Preux Swiss", 2), pf_regiment("Marines of the Guard", 1)]),
               pf_battery("Foot Battery")],
              command=[cmd("pf-div-cmd", "Gén. de Division Frère")],
              notes=["After Nafziger: the Reding and Preux Swiss regiments, four battalions about 2,000 men, shown two each, and the Guard Marines' battalion."])

FRESIA = force("bailen-fresia", PF, "Fresia's Cavalry", "4th Division, Dupont's Corps", "French",
               "Dupont's provisional regiments of dragoons, chasseurs and cuirassiers, which charged the Spanish line repeatedly and once broke into it, taking guns they could not hold.",
               [pf_cav("Privé's Brigade", "Gén. de Brigade Privé", [("1st Provisional", "Dragons"), ("2nd Provisional", "Dragons")]),
                pf_cav("Dupré's Brigade", "Gén. de Brigade Dupré", [("1st Provisional", "Chasseurs"), ("2nd Provisional", "Chasseurs")]),
                pf_cav("Boussart's Brigade", "Gén. de Brigade Boussart", [("6th Provisional", "Dragons"), ("2nd Provisional Cuirassiers,", "Dragons")]),
                pf_battery("Horse Battery", "pf-horse-arty")],
               command=[cmd("pf-div-cmd", "Gén. de Division Fresia")],
               notes=["After Nafziger. The 2nd Provisional Cuirassiers, from Gobert's division, fought here and are shown as the list's Dragoons with Boussart.", CAVALRY_ONLY])

VEDEL = force("bailen-vedel", PF, "Vedel's Division", "2nd Division, Dupont's Corps", "French",
              "Left behind at La Carolina, it came up on the Spanish rear only in the afternoon, after Dupont had asked for terms, and was included in the capitulation.",
              [pf_bde("Poinsot's Brigade", "Gén. de Brigade Poinsot", [pf_regiment("5th Legion of Reserve", 3), pf_regiment("3rd Swiss", 1)]),
               pf_bde("Cassagne's Brigade", "Gén. de Brigade Cassagne", [pf_regiment("1st Legion of Reserve", 3)]),
               pf_battery("Foot Battery")],
              command=[cmd("pf-div-cmd", "Gén. de Division Vedel")],
              notes=["After Nafziger, who gives the 1st Legion one battalion of 2,147 men; three are shown.", LEGIONS])

REDING = force("bailen-reding", SP, "Reding's Division", "1st Division, Army of Andalusia (Castaños)", "Spanish",
               "Blocked the road at Bailén and held it all day against Dupont's attacks, its Walloon and Swiss guards and line regiments standing in the heat while the gunners fought the French batteries down.",
               [bde("sp-guard-infantry-brigade", "Walloon Guards", "", [u("sp-guard-infantry", "III/Walloon Guards")]),
                sp_bde("First Brigade", "", regiments=[sp_reg("Reina"), sp_reg("Corona"), sp_reg("Jaén")],
                       units=[sp("sp-militia", "Provincial de Jaén"), sp("sp-light", "Voluntarios de Barbastro", options=["small"])]),
                sp_bde("Second Brigade", "", regiments=[sp_reg("Irlanda", 2), sp_reg("Reding (Swiss)"), sp_reg("1st Voluntarios de Granada")],
                       units=[sp("sp-militia", "Tercio de Tejas"), sp("sp-light", "Cazadores de Antequera", options=["small"])]),
                sp_cav("Reding's Cavalry", "", [sp("sp-heavy", "Montesa Cavalry", options=["small"]), sp("sp-heavy", "Farnesio Cavalry", options=["small"]),
                                                 sp("sp-heavy", "Reina Dragoons", options=["small"]), sp("sp-heavy", "Numancia Dragoons", options=["small"]),
                                                 sp("sp-heavy", "Olivenza Dragoons", options=["small"]), sp("sp-lancer", "Utrera Lancers", options=["small"])]),
                sp_guns("Horse Battery", "sp-horse-artillery"), sp_guns("Foot Battery")],
               command=[cmd("sp-div-cmd", "Lt-Gen Teodoro Reding")],
               notes=[SP_BRIGADES, SP_CAV, "More cavalry regiments than one brigade holds also shows as a historical departure."])

COUPIGNY = force("bailen-coupigny", SP, "Coupigny's Division", "2nd Division, Army of Andalusia (Castaños)", "Spanish",
                 "Beside Reding's, on the left of the line at Bailén, it held off the French attacks and then turned to face Vedel's division as it came up behind.",
                 [sp_bde("First Brigade", "", regiments=[sp_reg("Ceuta"), sp_reg("Órdenes Militares", 2)],
                         units=[sp("sp-militia", "Provincial de Granada"), sp("sp-militia", "Provincial de Trujillo"), sp("sp-light", "Voluntarios de Cataluña")]),
                  sp_bde("Second Brigade", "", regiments=[sp_reg("2nd Voluntarios de Granada"), sp_reg("3rd Voluntarios de Granada")],
                         units=[sp("sp-militia", "Provincial de Bujalance"), sp("sp-militia", "Provincial de Cuenca"), sp("sp-militia", "Provincial de Ciudad Real")]),
                  sp_cav("Coupigny's Cavalry", "", [sp("sp-heavy", "Borbón Cavalry"), sp("sp-heavy", "España Cavalry", options=["small"])]),
                  sp_guns("Horse Battery", "sp-horse-artillery")],
                 command=[cmd("sp-div-cmd", "Mariscal de Campo Marqués de Coupigny")],
                 notes=[SP_BRIGADES, "More Militia battalions in a brigade than the list's two show as historical departures."])

LA_PENA = force("bailen-la-pena", SP, "La Peña's and Jones's Divisions", "Reserve and 3rd Divisions, Army of Andalusia (Castaños)", "Spanish",
                "Castaños's other two divisions, which followed Dupont from Andújar and closed on his rear as the battle ended, sealing the French in between them and Reding.",
                [sp_bde("La Peña's Reserve", "Lt-Gen Manuel de La Peña", regiments=[sp_reg("Burgos", 2), sp_reg("Africa"), sp_reg("Murcia")],
                        units=[sp("sp-grenadier", "Provincial Grenadiers"), sp("sp-militia", "Provincial de Sigüenza"), sp("sp-light", "Zaragoza Battalion")]),
                 sp_bde("Jones's Division", "Mariscal de Campo Félix Jones", regiments=[sp_reg("Córdoba"), sp_reg("Campomayor"), sp_reg("Valencia")],
                        units=[sp("sp-militia", "Provincial de Burgos"), sp("sp-militia", "Provincial de Plasencia")]),
                 sp_cav("Reserve Cavalry", "", [sp("sp-heavy", "Pavía Dragoons"), sp("sp-heavy", "Príncipe Cavalry", options=["small"]),
                                                sp("sp-heavy", "Calatrava Cavalry", options=["small"]), sp("sp-lancer", "Jerez Lancers", options=["small"])]),
                 sp_guns("Reserve Artillery")],
                command=[cmd("sp-div-cmd", "Lt-Gen Manuel de La Peña")],
                notes=[SP_BRIGADES, "Jones's division's smaller provincial battalions (Alcázar de San Juan, Guadix, Sevilla, Lorca) and the Santiago and Sagunto cavalry are left out.",
                       "A cavalry brigade with one full heavy regiment, short of the two it needs, shows as a historical departure."])

BAILEN = {
    "id": "bailen", "name": "Bailén", "date": "19 July 1808", "campaign": "peninsular-war",
    "summary": "Dupont's corps, strung out and laden with the loot of Córdoba, found Reding's division across its road home at Bailén. All day in the Andalusian heat the French threw themselves at the Spanish line and were beaten back, their Swiss going over to the enemy; with Castaños's other divisions closing behind and Vedel too late to help, Dupont surrendered his whole corps, the first great defeat of a French army in the field.",
    "sources": [naf("808GSAG", "French Forces at Baylen, 19 July 1808"), naf("808GSAH", "Spanish Forces at Baylen, 19 July 1808"),
                wiki("Battle_of_Bail%C3%A9n", "Battle of Bailén")],
    "forces": [BARBOU, FRERE, FRESIA, VEDEL, REDING, COUPIGNY, LA_PENA],
}


# ================================================================ Bussaco, 27 September 1810

PT2 = "Each Portuguese line regiment had two battalions, shown as one Large or standard battalion as the list builds them."
FR_BN = "After Nafziger, with each regiment's battalions as he gives them."

BUSSACO_FR = [
    fr_div("bussaco-merle", "Merle's Division", "1st Division, II Corps (Reynier)", "Gén. de Division Merle",
           [("Sarrut's Brigade", "Gén. de Brigade Sarrut", [R("2e", 4, "Léger"), R("36e", 4)]), ("Graindorge's Brigade", "Gén. de Brigade Graindorge", [R("4e", 4, "Léger")])],
           "Climbed the steep ridge north of São Antonio de Cantaro through the morning mist and reached the crest, only to be met by Picton's men and the 88th and 45th, and thrown back down in disorder.", [FR_BN]),
    fr_div("bussaco-heudelet", "Heudelet's Division", "2nd Division, II Corps (Reynier)", "Gén. de Division Heudelet",
           [("Foy's Brigade", "Gén. de Brigade Foy", [R("17e", 3, "Léger"), R("70e", 4)]), ("Arnauld's Brigade", "Gén. de Brigade Arnauld", [R("31e", 4, "Léger"), R("47e", 4)])],
           "Its column, led by Foy's brigade, also reached the top of the ridge, and was driven off it by Leith's division coming along the crest from the south.", [FR_BN]),
    fr_div("bussaco-marchand", "Marchand's Division", "1st Division, VI Corps (Ney)", "Gén. de Division Marchand",
           [("Maucune's Brigade", "Gén. de Brigade Maucune", [R("6e", 2, "Léger"), R("69e", 3)]), ("Marcognet's Brigade", "Gén. de Brigade Marcognet", [R("39e", 3), R("76e", 3)])],
           "Ney's second attack, up the road towards the convent; it was stopped by Pack's Portuguese and the guns above.", [FR_BN]),
    fr_div("bussaco-mermet", "Mermet's Division", "2nd Division, VI Corps (Ney)", "Gén. de Division Mermet",
           [("Bardet's Brigade", "Gén. de Brigade Bardet", [R("25e", 2, "Léger"), R("27e", 3)]), ("Labassée's Brigade", "Gén. de Brigade Labassée", [R("50e", 3), R("59e", 3)])],
           "Ney's reserve, held below the ridge while Loison and Marchand attacked.", [FR_BN]),
    fr_div("bussaco-loison", "Loison's Division", "3rd Division, VI Corps (Ney)", "Gén. de Division Loison",
           [("Simon's Brigade", "Gén. de Brigade Simon", [pf_regiment("Légion du Midi", 1), pf_regiment("Hanoverian Legion", 2), pf_regiment("26e", 3, first=0)]),
            ("Ferey's Brigade", "Gén. de Brigade Ferey", [pf_regiment("32e", 1, "Léger"), pf_regiment("66e", 3), pf_regiment("82e", 2)])],
           "Ney's first attack, straight up the road to the convent at Sula. Simon's brigade reached the crest under the Light Division's fire and was met by the 43rd and 52nd rising from behind it at fifty yards; Simon was wounded and taken.",
           [FR_BN, "The Légion du Midi and the Hanoverian Legion are shown as Line."]),
]

BUSSACO_AL = [
    force("bussaco-spencer", PB, "Spencer's 1st Division", "Wellington's army", AP,
          "Held the centre of the ridge around the convent, in reserve behind the Light Division and Pack's Portuguese.",
          [bde("pb-guards-brigade", "Campbell's Guards Brigade", "Maj-Gen Henry Campbell", [u("pb-foot-guard", "1/Coldstream Guards"), u("pb-foot-guard", "1/3rd Guards"), rifles()]),
           pb_bde("Blantyre's Brigade", "Col Lord Blantyre", [line("2/24th Foot"), highland("2/42nd Highlanders"), line("1/61st Foot"), rifles()]),
           bde("pb-kgl-brigade", "Löwe's KGL Brigade", "Maj-Gen von Löwe", [u("pb-line", "1st Line Bn KGL"), u("pb-line", "2nd Line Bn KGL"), u("pb-line", "5th Line Bn KGL"), u("pb-line", "7th Line Bn KGL")]),
           pb_bde("Pakenham's Brigade", "Col Edward Pakenham", [line("1/7th Fusiliers"), highland("1/79th Highlanders")]),
           pb_battery("6-pdr Battery")],
          command=[cmd("pb-div-cmd", "Lt-Gen Sir Brent Spencer")],
          notes=["After Nafziger, who gives Sherbrooke; Spencer commanded the division at Bussaco.",
                 "A KGL brigade of four battalions, where the list's has three at most, and Highland battalions in small brigades, show as historical departures."]),
    force("bussaco-hill", PB, "Hill's 2nd Division", "Wellington's army", AP,
          "On the far right of the ridge, out of the fighting, until Hill sent battalions north along the crest to help Leith.",
          [pb_bde("Stewart's Brigade", "Maj-Gen William Stewart", [line("1/3rd Foot (Buffs)"), line("2/31st Foot"), line("2/48th Foot"), line("2/66th Foot"), rifles()]),
           pb_bde("Inglis's Brigade", "Col William Inglis", [line("29th Foot"), line("1/48th Foot"), line("1/57th Foot"), rifles()]),
           pb_bde("Wilson's Brigade", "Col Wilson", [line("2/28th Foot"), line("2/34th Foot"), line("2/39th Foot"), rifles()]),
           pb_battery("Portuguese 6-pdr Battery", "pb-portuguese-arty"), pb_battery("9-pdr Battery")],
          command=[cmd("pb-div-cmd", "Lt-Gen Rowland Hill")],
          notes=["After Nafziger. " + ARTILLERY]),
    force("bussaco-hamilton", PB, "Hamilton's Portuguese Division", "Wellington's army", AP,
          "Portuguese regulars on the right of the line beside Hill, ready to support Leith.",
          [pt_bde("Campbell's Brigade", "Col Archibald Campbell", ["4th Line", "10th Line"]),
           pt_bde("Fonseca's Brigade", "Brig-Gen Fonseca", ["2nd Line", "14th Line"])],
          command=[cmd("pb-div-cmd", "Maj-Gen John Hamilton")],
          notes=[PT2, "Without British brigades for the Portuguese ones to go with, the list's ratio shows as a historical departure."]),
    force("bussaco-picton", PB, "Picton's 3rd Division", "Wellington's army", AP,
          "Held the pass of São Antonio de Cantaro, where Reynier's columns came up out of the mist; the 88th and 45th charged Merle's men on the crest and threw them down the slope.",
          [pb_bde("Mackinnon's Brigade", "Col Henry Mackinnon", [line("1/45th Foot"), line("1/74th Foot"), line("1/88th Connaught Rangers")]),
           pb_bde("Lightburne's Brigade", "Maj-Gen Lightburne", [line("2/5th Foot"), line("2/83rd Foot"), rifles("5/60th Rifles (three companies)")]),
           pt_bde("Champalimaud's Brigade", "Col Champalimaud", ["9th Line", "21st Line"]),
           pb_battery("6-pdr Battery"), pb_battery("6-pdr Battery")],
          command=[{"unit": "pb-cmd-picton"}],
          notes=["Picton is the book's named commander.", PT2, ARTILLERY]),
    force("bussaco-cole", PB, "Cole's 4th Division", "Wellington's army", AP,
          "On the far left of the ridge above Ney's attacks, which never reached it.",
          [pb_bde("Campbell's Brigade", "Col Alexander Campbell", [line("2/7th Fusiliers"), line("1/11th Foot"), line("2/53rd Foot"), rifles()]),
           pb_bde("Kemmis's Brigade", "Col Kemmis", [line("3/27th Foot"), line("1/40th Foot"), line("97th Foot"), rifles()]),
           pt_bde("Collins's Brigade", "Col Richard Collins", ["11th Line", "23rd Line"])],
          command=[cmd("pb-div-cmd", "Maj-Gen Lowry Cole")],
          notes=["After Nafziger.", PT2]),
    force("bussaco-leith", PB, "Leith's 5th Division", "Wellington's army", AP,
          "Moved north along the crest as Heudelet's column reached it, and Barnes's brigade, the 9th and 38th leading, charged and drove it off the ridge.",
          [pb_bde("Barnes's Brigade", "Col James Barnes", [line("3/1st Foot (Royal Scots)"), line("1/9th Foot"), line("2/38th Foot")]),
           pt_bde("Spry's Brigade", "Col Spry", ["3rd Line", "15th Line", "Thomar Militia"]),
           portuguese_eben := bde("pb-portuguese-infantry-brigade", "Eben's Brigade", "Baron Eben", [u("pb-portuguese-line", "8th Line"), u("pb-loyal-lusitanian", "Loyal Lusitanian Legion")]),
           pb_battery("Portuguese 6-pdr Battery", "pb-portuguese-arty")],
          command=[cmd("pb-div-cmd", "Maj-Gen James Leith")],
          notes=[PT2, "The Thomar militia battalion is shown as Portuguese Line, a third in Spry's brigade where the list takes two, which shows as a historical departure."]),
    force("bussaco-light", PB, "Craufurd's Light Division", "Wellington's army", AP,
          "Lay hidden behind the crest above Sula while Loison's division climbed towards it under the rifles' fire; at fifty yards Craufurd called the 43rd and 52nd forward, and their volley and charge swept the French back down the hill.",
          [bde("pb-light-brigade", "Beckwith's Brigade", "Lt-Col Sidney Beckwith",
               [u("pb-light-inf", "1/43rd Light Infantry"), u("pb-cacadores", "3rd Caçadores"), u("pb-rifle-coys", "1/95th Rifles (four companies)")]),
           bde("pb-light-brigade", "Barclay's Brigade", "Lt-Col Robert Barclay",
               [u("pb-light-inf", "1/52nd Light Infantry"), u("pb-cacadores", "1st Caçadores"), u("pb-rifle-coys", "1/95th Rifles (four companies)")]),
           bde("pb-horse-artillery", "Ross's Troop RHA", units=[u("pb-royal-horse-arty", "Ross's Troop RHA")])],
          command=[{"unit": "pb-cmd-craufurd"}],
          notes=["Craufurd is the book's named commander.", "Two Light Brigades where the list takes one, and a horse troop with an infantry division, show as historical departures."]),
    force("bussaco-portuguese", PB, "Pack's, Campbell's and Coleman's Portuguese", "Independent brigades", AP,
          "Pack's brigade held the crest beside the Light Division and helped throw back Marchand's attack up the road.",
          [pt_bde("Pack's Brigade", "Brig-Gen Denis Pack", ["1st Line", "16th Line"], "4th Caçadores"),
           pt_bde("Campbell's Brigade", "Brig-Gen Alexander Campbell", ["6th Line", "18th Line"], "6th Caçadores"),
           pt_bde("Coleman's Brigade", "Brig-Gen Coleman", ["7th Line", "19th Line"], "2nd Caçadores")],
          command=[cmd("pb-div-cmd", "Brig-Gen Denis Pack")],
          notes=[PT2, "Without British brigades for the Portuguese ones to go with, the list's ratio shows as a historical departure."]),
]

BUSSACO = {
    "id": "bussaco", "name": "Bussaco", "date": "27 September 1810", "campaign": "peninsular-war",
    "summary": "Masséna, invading Portugal, found Wellington's Anglo-Portuguese army drawn up along the ten-mile ridge of Bussaco and attacked it head-on. Reynier's columns climbed out of the mist to the crest and were thrown back by Picton's and Leith's men; Ney's, coming up the road to the convent, met the Light Division's volley at fifty yards. The French lost four and a half thousand men and turned the position instead, and Wellington fell back on the Lines of Torres Vedras.",
    "sources": [naf("810ISAC", "British Order of Battle at Busaco, 27 September 1810"), naf("810ISAD", "French Order of Battle at Busaco, 27 September 1810"),
                wiki("Battle_of_Bu%C3%A7aco", "Battle of Buçaco")],
    "forces": BUSSACO_FR + BUSSACO_AL,
}

# Periods: 1808 is the lists' Early period, 1810 their Middle
for f in MEDINA["forces"] + BAILEN["forces"]:
    f["period"] = "early"
for f in BUSSACO["forces"]:
    f["period"] = "middle"


if __name__ == "__main__":
    for b in (MEDINA, BAILEN, BUSSACO):
        ratings.apply(b)
        commanders.apply(b)
        if b["id"] in ART:
            b["art"] = ART[b["id"]]
        (OUT / f"{b['id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        print(f"{b['name']}: {len(b['forces'])} forces")
