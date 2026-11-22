"""
Each side's commander at each battle, with a portrait from Wikimedia Commons, shown above that side's forces.
Run on each battle as it's written (see the generators), like ratings.py.

Portraits are public-domain paintings or prints; `thumb` builds Commons' own thumbnail address (at one of its
standard widths, 250px, as others are refused) for a file
from its exact name, so no lookup is needed once the name is known.
"""

import hashlib
import urllib.parse


def thumb(name: str, width: int = 250) -> str:
    """Commons' thumbnail of a file, by its exact name (spaces or underscores)"""
    name = name.replace(" ", "_")
    h = hashlib.md5(name.encode()).hexdigest()
    q = urllib.parse.quote(name)
    suffix = ".png" if name.lower().endswith(".svg") else ""
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/{width}px-{q}{suffix}"


def original(name: str) -> str:
    """A Commons file's original, for one narrower than the standard thumbnail"""
    name = name.replace(" ", "_")
    h = hashlib.md5(name.encode()).hexdigest()
    return f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{urllib.parse.quote(name)}"


def portrait(file, title, artist, date=None, focus="50% 20%", small=False):
    p = {"src": original(file) if small else thumb(file), "title": title, "artist": artist,
         "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(file.replace(" ", "_")), "focus": focus}
    if date:
        p["date"] = date
    return p


PORTRAITS = {
    "wellington": portrait("Sir Arthur Wellesley, 1st Duke of Wellington.jpg", "Arthur Wellesley, Duke of Wellington", "Thomas Lawrence", focus="50% 18%"),
    "napoleon": portrait("Napoleon at Fontainebleau, 31 March 1814 (by Hippolyte Paul Delaroche).jpg", "Napoleon at Fontainebleau", "Paul Delaroche", "1840", "50% 22%"),
    "blucher": portrait("Blücher (nach Gebauer).jpg", "Gebhard Leberecht von Blücher", "after Ernst Gebauer"),
    "ney": portrait("Marechal Ney.jpg", "Marshal Michel Ney", "François Gérard", focus="50% 18%"),
    "grouchy": portrait("Emmanuel de Grouchy 2.jpg", "Marshal Emmanuel de Grouchy", "Jean-Sébastien Rouillard", "1835", "50% 10%"),
    "thielmann": portrait("Johann Adolf Freiherr von Thielmann.jpg", "Johann von Thielmann", "Anton Graff", focus="50% 14%"),
    "soult": portrait("Nicolas Jean de Dieu Soult.jpg", "Marshal Jean-de-Dieu Soult", "after Louis-Henri de Rudder", focus="50% 14%"),
    "junot": portrait("Junot, par Appiani.png", "Jean-Andoche Junot", "Andrea Appiani", focus="50% 22%"),
    "delaborde": portrait("Le général Henri-François Delaborde.jpg", "Henri-François Delaborde", "Jean-Antoine Pinchon", focus="50% 20%"),
    "yorck": portrait("Ludwig Yorck von Wartenburg.jpg", "Ludwig Yorck von Wartenburg", "Ernst Gebauer", "1835", "50% 28%"),
}
PORTRAITS.update({
    "beresford": portrait('Thomas Lawrence (1769-1830) - William Carr (1768–1854), Viscount Beresford, GCB - WM.1480-1948 - Apsley House.jpg', "William Carr Beresford", "Thomas Lawrence", "1818", "50% 16%"),
    "moore": portrait('Thomas Lawrence (1769-1830) - Lieutenant-General Sir John Moore (1761–1809), KB - NAM. 1966-07-22 - National Army Museum.jpg', "Sir John Moore", "Thomas Lawrence", "1805", "50% 18%"),
    "blake": portrait("El general Joaquín Blake y Joyes, por Manuel Ojeda.jpg", "Joaquín Blake", "Manuel Ojeda", focus="50% 18%"),
    "marmont": portrait("Marmont.jpg", "Marshal Auguste de Marmont", "Jean-Baptiste Paulin Guérin", "1837", "50% 16%"),
    "joseph": portrait("Joseph-Bonaparte.jpg", "Joseph Bonaparte, King of Spain", "François Gérard", focus="50% 14%"),
})
# The commanders of divisions and corps, for their forces' cards
PORTRAITS.update({
    "berthezene": portrait("Le L.ant G.al B.on Berthezène (BM 1901,1022.71).jpg", "Pierre Berthezène", "Étienne David", "1840s", "50% 16%"),
    "habert": portrait("Pierre Joseph Habert.JPG", "Pierre-Joseph Habert", "after Ambroise Tardieu", focus="50% 22%"),
    "girard": portrait("Le général Girard (Ecole française du XIXème siècle).jpg", "Jean-Baptiste Girard", "French School", focus="50% 20%"),
    "vichery": portrait("Louis Joseph Vichery.jpg", "Louis Joseph Vichery", "unknown artist", focus="50% 20%"),
    "friant": portrait("Général Louis Friant (2).jpg", "Louis Friant", "Ambroise Tardieu", focus="50% 20%"),
    "delort": portrait("Jacques-Antoine-Adrien Delort.jpg", "Jacques-Antoine-Adrien Delort", "Joseph-Marcellin Combette", focus="50% 20%"),
    "zieten": portrait("Zieten-by-Kruger.jpg", "Hans Ernst Karl von Zieten", "Franz Krüger", focus="50% 18%", small=True),
    "pirch": portrait("Georg Dubislav Ludwig von Pirch.png", "Georg von Pirch", "unknown artist", focus="50% 20%", small=True),
})
# Quatre Bras, Waterloo and Wavre divisional / corps commanders
PORTRAITS.update({
    # French
    "foy": portrait("Maximilien Foy 1.jpg", "Maximilien Sébastien Foy", "unknown artist", focus="50% 20%"),
    "jerome": portrait("Jérôme Bonaparte (Kinson).jpg", "Jérôme Bonaparte, King of Westphalia", "after François Kinson", focus="50% 18%"),
    "bulow": portrait("Friedrich Wilhelm Freiherr von Bulow.jpg", "Friedrich Wilhelm Bülow von Dennewitz", "unknown artist", focus="50% 20%"),
    # British / King's German Legion
    "picton": portrait("Sir Thomas Picton by Sir Martin Archer Shee.jpg", "Sir Thomas Picton", "Martin Archer Shee", focus="50% 20%"),
    "uxbridge": portrait("Thomas Lawrence (1769-1830) - Henry William Paget (1768–1854), 1st Marquess of Anglesey, KG - WM.1474-1948 - Apsley House.jpg", "Henry Paget, Earl of Uxbridge", "Thomas Lawrence", "1818", "50% 16%"),
    "cooke": portrait("Portrait of General Sir George Cooke (1768–1837) (by Jan Willem Pieneman).jpg", "Sir George Cooke", "Jan Willem Pieneman", focus="50% 20%"),
    "lambert": portrait("John-lambert-waterloo.jpg", "Sir John Lambert", "William Salter", focus="50% 20%"),
    # Dutch-Belgian
    "perponcher": portrait("Graaf de Perponcher, H.jpg", "H.G. de Perponcher Sedlnitsky", "P.H.K. van Schendel", focus="50% 20%"),
    "chasse": portrait("General D H Chassé.jpg", "David Hendrik Chassé", "Jan Willem Pieneman", "1832", "50% 20%"),
    # Brunswick
    "brunswick": portrait("Herzog von Braunschweig-Oels.jpg", "Friedrich Wilhelm, Duke of Brunswick-Oels", "Johann Christian Ludwig Tunica", focus="50% 20%"),
})
# More 1815 divisional commanders, found on a second, slower search of Commons
PORTRAITS.update({
    "bachelu": portrait("Général Gilbert Désiré Joseph Bachelu.jpg", "Gilbert Bachelu", "Forestier", "1818", "50% 20%"),
    "pire": portrait("Portrait d'Hippolyte Marie Guillaume de Rosnyvinen (1778-1850) général et comte d'Empire.jpg", "Hippolyte de Piré", "Emmanuel Lauret", "1842", "50% 20%"),
    "marcognet": portrait("Pierre-Louis Binet de Marcognet.jpg", "Pierre-Louis Binet de Marcognet", "unknown artist", focus="50% 20%"),
    "durutte": portrait("General Durutte by François Böhm 1.jpg", "Pierre-François Durutte", "François Böhm", focus="50% 20%"),
    "simmer": portrait("BOYER 2353 - Le Lieutenant général baron Simmer, Ancien député du Puy-de-Dôme.jpg", "François Simmer", "unknown artist", focus="50% 20%"),
    "jeanin": portrait("Jean-Baptiste Jeanin.jpg", "Jean-Baptiste Jeanin", "Jacques-Louis David", "1810", "50% 20%"),
    "wathier": portrait("Pierre Wathier de Saint-Alphonse.jpg", "Pierre Wathier", "unknown artist", focus="50% 20%"),
    "lheritier": portrait("Général Samuel François Lhéritier de Chézelles.jpg", "Samuel-François Lhéritier", "unknown artist", focus="50% 20%"),
    "jacquinot": portrait("Riesener - Le colonel baron C.-C. Jacquinot (1772-1848) en tenue de colonel du 11e chasseurs à cheval.jpg", "Charles-Claude Jacquinot", "Henri-François Riesener", focus="50% 20%"),
    "drouot": portrait("Le général Antoine Drouot (1774-1847).jpg", "Antoine Drouot", "unknown artist", "1816", "50% 20%"),
    "lefebvre_desnouettes": portrait("Général Charles Lefebvre Desnouettes (2).jpg", "Charles Lefebvre-Desnouettes", "unknown artist", focus="50% 20%"),
    "clinton": portrait("Henry Clinton (1771-1829).jpg", "Sir Henry Clinton", "Samuel William Reynolds", "1827", "50% 20%"),
    "vandeleur": portrait("Sir John Ormsby Vandeleur by William Salter.jpg", "Sir John Ormsby Vandeleur", "William Salter", focus="50% 20%"),
    "kruse": portrait("August von Kruse.jpg", "August von Kruse", "unknown artist", focus="50% 20%"),
})
# 1812, the Riga front (George Dawe's Military Gallery portraits)
PORTRAITS.update({
    "steinheil": portrait("Fabian F. von Steinheil.jpg", "Fabian von Steinheil", "George Dawe", focus="50% 18%"),
    "lowis": portrait("FriedrichvonLowisofMenar.jpg", "Friedrich von Löwis of Menar", "George Dawe", focus="50% 18%"),
    "essen": portrait("Essen Ivan N.jpg", "Magnus Gustav von Essen", "George Dawe", focus="50% 18%"),
})
# No public-domain portrait found for: Lefol, Pécheux, Hulot, Strolz, Teste (Wavre/Ligny); Kellermann the younger,
# Alten, Quiot, Donzelot, Roussel d'Hurbal, Duhesme (1815); Grawert, Horn, Alexeyev, Rachmanov (1812 campaign).
# Their force cards show the flag only.
EXTRA = {}

COMMANDERS = {
    "ligny": {"French": ("Napoleon", "napoleon"), "Prussian": ("Field Marshal Blücher", "blucher")},
    "quatre-bras": {"French": ("Marshal Ney", "ney"), "Anglo-allied": ("The Duke of Wellington", "wellington")},
    "waterloo": {"Anglo-allied": ("The Duke of Wellington", "wellington"), "French": ("Napoleon", "napoleon"), "Prussian": ("Field Marshal Blücher", "blucher")},
    "wavre": {"French": ("Marshal Grouchy", "grouchy"), "Prussian": ("Lt-Gen von Thielmann", "thielmann")},
    "eckau": {"Prussian": ("Gen-Lt von Grawert", "grawert"), "Russian": ("Maj-Gen Löwis of Menar", "lowis")},
    "mesoten": {"Prussian": ("Gen-Lt von Yorck", "yorck"), "Russian": ("Lt-Gen Count Steinheil", "steinheil")},
    "dahlenkirchen": {"Prussian": ("Gen-Lt von Yorck", "yorck"), "Russian": ("Lt-Gen von Essen", "essen")},
    "mir": {"Polish": ("Gén. de Division Rożniecki", "rozniecki"), "Russian": ("General Platov", "platov")},
    "romanov": {"Polish": ("Gén. de Division Latour-Maubourg", "latour_maubourg"), "Russian": ("General Platov", "platov")},
    "kobrin": {"Saxon": ("Gen-Maj von Klengel", "klengel"), "Russian": ("General Tormasov", "tormasov")},
    "gorodechno": {"Austrian": ("Prince Schwarzenberg", "schwarzenberg"), "Saxon": ("Général Reynier", "reynier"), "Russian": ("General Tormasov", "tormasov")},
    "rolica": {"Anglo-Portuguese": ("Sir Arthur Wellesley", "wellington"), "French": ("Gén. de Division Delaborde", "delaborde")},
    "vimeiro": {"Anglo-Portuguese": ("Sir Arthur Wellesley", "wellington"), "French": ("Gén. Junot", "junot")},
    "albuera": {"Anglo-Portuguese": ("Marshal Beresford", "beresford"), "Spanish": ("Gen. Joaquín Blake", "blake"), "French": ("Marshal Soult", "soult")},
    "corunna": {"British": ("Lt-Gen Sir John Moore", "moore"), "French": ("Marshal Soult", "soult")},
    "talavera": {"British": ("Sir Arthur Wellesley", "wellington"), "French": ("King Joseph, with Marshal Jourdan", "joseph")},
    "salamanca": {"Anglo-Portuguese": ("The Earl of Wellington", "wellington"), "French": ("Marshal Marmont", "marmont")},
    "vitoria": {"Anglo-Allied": ("The Marquess of Wellington", "wellington"), "Spanish": ("Under Wellington", "wellington"),
                "French": ("King Joseph, with Marshal Jourdan", "joseph")},
}


# A force's own commander, by force id, for a portrait on its card
FORCE_PORTRAITS: dict[str, str] = {
    # Ligny
    "ligny-berthezene": "berthezene", "ligny-habert": "habert", "ligny-girard": "girard", "ligny-vichery": "vichery",
    "ligny-middle-guard": "friant", "ligny-delort": "delort",
    "ligny-prussian-i-corps": "zieten", "ligny-prussian-ii-corps": "pirch", "ligny-prussian-iii-corps": "thielmann",
    # Quatre Bras
    "quatre-bras-foy": "foy", "quatre-bras-jerome": "jerome",
    "quatre-bras-picton": "picton", "quatre-bras-brunswick": "brunswick",
    "quatre-bras-cooke": "cooke", "quatre-bras-perponcher": "perponcher",
    # Waterloo — French
    "waterloo-foy": "foy", "waterloo-jerome": "jerome",
    "waterloo-delort": "delort", "waterloo-middle-guard": "friant",
    # Waterloo — Allied
    "waterloo-picton": "picton", "waterloo-cooke": "cooke",
    "waterloo-lambert": "lambert", "waterloo-heavy-cavalry": "uxbridge",
    "waterloo-perponcher": "perponcher", "waterloo-chasse": "chasse", "waterloo-brunswick": "brunswick",
    "waterloo-prussian-iv-corps": "bulow", "waterloo-prussian-i-corps": "zieten",
    # Wavre — French
    "wavre-habert": "habert", "wavre-berthezene": "berthezene", "wavre-vichery": "vichery",
    # Wavre — Prussian
    "wavre-prussian-iii-corps": "thielmann",
    # 1812
    "eckau-lowis": "lowis", "mesoten-prussian-corps": "yorck", "dahlenkirchen-lowis": "lowis",
    "mir-rozniecki": "rozniecki", "mir-platov": "platov", "romanov-przebendowski": "latour_maubourg", "romanov-platov": "platov",
    "kobrin-tormasov": "tormasov", "gorodechno-bianchi": "bianchi", "gorodechno-lambert": "lambert",
    "gorodechno-kamensky": "kamensky", "gorodechno-nazimov": "nazimov", "gorodechno-udom": "udom",
    "gorodechno-frimont": "frimont", "gorodechno-funck": "funck", "gorodechno-lecoq": "lecoq",
    # Found on the second search
    "quatre-bras-bachelu": "bachelu", "waterloo-bachelu": "bachelu", "quatre-bras-pire": "pire",
    "waterloo-marcognet": "marcognet", "waterloo-durutte": "durutte", "waterloo-simmer": "simmer",
    "waterloo-jeanin": "jeanin", "waterloo-wathier": "wathier", "waterloo-lheritier": "lheritier",
    "waterloo-jacquinot": "jacquinot", "waterloo-old-guard": "drouot", "waterloo-guard-cavalry": "lefebvre_desnouettes",
    "waterloo-clinton": "clinton", "waterloo-vandeleur-vivian": "vandeleur", "waterloo-kruse": "kruse",
}


def apply(battle: dict) -> dict:
    for f in battle["forces"]:
        key = FORCE_PORTRAITS.get(f["id"])
        if key and (PORTRAITS.get(key) or EXTRA.get(key)):
            f["portrait"] = PORTRAITS.get(key) or EXTRA.get(key)
    sides = COMMANDERS.get(battle["id"])
    if not sides:
        return battle
    out = {}
    for side, (name, key) in sides.items():
        entry = {"commander": name}
        p = PORTRAITS.get(key) or EXTRA.get(key)
        if p:
            entry["portrait"] = p
        out[side] = entry
    battle["sides"] = out
    return battle


# 1812: Bagration's retreat and the southern flank
PORTRAITS.update({
    "platov": portrait("Thomas Phillips - Portrait of Matvei Platov - WGA17404.jpg", "Matvei Platov", "Thomas Phillips", "1814", "50% 16%"),
    "rozniecki": portrait("Aleksander Rożniecki 1.PNG", "Aleksander Rożniecki", "unknown artist"),
    "latour_maubourg": portrait("Général Marie Victor Nicolas de Fay de La Tour Maubourg.jpg", "Marie-Victor de Latour-Maubourg", "unknown artist", small=True),
    "vasilchikov": portrait("Vasilchikov 2 Dmitry Vasilyevich.jpg", "Dmitry Vasilchikov", "workshop of George Dawe", focus="50% 18%"),
    "kuteinikov": portrait("Kuteinikov D E.jpg", "Dmitry Kuteinikov", "George Dawe", focus="50% 18%"),
    "tormasov": portrait("Tormasov.jpg", "Alexander Tormasov", "workshop of George Dawe", focus="50% 18%"),
    "lambert": portrait("Lambert Karl Osipovich.jpg", "Karl de Lambert", "workshop of George Dawe", focus="50% 18%"),
})

# Gorodechno's divisional commanders
PORTRAITS.update({
    "kamensky": portrait("Kamensky Sergey Mihailovich.jpg", "Count Sergei Kamensky", "unknown artist", focus="50% 18%"),
    "nazimov": portrait("Nazimov Fyodor Viktorovich.jpg", "Fyodor Nazimov", "workshop of George Dawe", focus="50% 18%"),
    "udom": portrait("Udom 2 Evstafy Evstafyevich.jpg", "Yevstafy Udom", "George Dawe", focus="50% 18%"),
    "frimont": portrait("Johann Frimont.jpg", "Johann Maria Philipp Frimont", "Josef Kriehuber", "1832", "50% 16%"),
    "funck": portrait("Karl Wilhelm Ferdinand von Funck.jpg", "Karl Wilhelm Ferdinand von Funck", "Anton Graff", "1804", "50% 18%"),
    "lecoq": portrait("Karl Christian Erdmann von Le Coq.jpg", "Karl Christian Erdmann von Le Coq", "M. Knäbig", focus="50% 18%"),
})

# The army lists' other named commanders, for the roster's head
PORTRAITS.update({
    "massena": portrait("André Masséna (Hersent).jpg", "Marshal André Masséna", "Louis Hersent"),
    "sebastiani": portrait("Sébastiani, Horace - 4.jpg", "Horace Sébastiani", "Jean-Baptiste Paulin Guérin"),
    "kempt": portrait("Sir James Kempt by William Salter.jpg", "Sir James Kempt", "William Salter"),
    "pack": portrait("Sir Denis Pack.jpg", "Sir Denis Pack", "Saunders", "c. 1800", small=True),
    "orange": portrait("Koning Willem II.jpg", "William, Prince of Orange", "Charles Pierre Verhulst", "1817"),
    "ghigny": portrait("Charles Étienne de Ghigny.jpg", "Charles-Étienne de Ghigny", "unknown artist"),
    "schwarzenberg": portrait("Carl Hummel, Fürst Karl Philipp zu Schwarzenberg (um 1816).jpg", "Karl Philipp, Prince Schwarzenberg", "Carl Hummel", "c. 1816"),
    "bianchi": portrait("Vinzenz Ferrerius von Bianchi.jpg", "Friedrich von Bianchi", "unknown artist", small=True),
    "davout": portrait("Louis nicolas davout.jpg", "Marshal Louis-Nicolas Davout", "after Pierre-Claude Gautherot"),
    "murat": portrait("Murat (Gerard).jpg", "Marshal Joachim Murat", "François Gérard"),
    "compans": portrait("Général Jean Dominique Compans (2).jpg", "Jean Dominique Compans", "Forestier", "1820"),
    "dessaix": portrait("Le général Joseph Marie Dessaix.jpg", "Joseph Marie Dessaix", "unknown artist"),
    "tharreau": portrait("Général Jean Victor Tharreau.jpg", "Jean-Victor Tharreau", "Robert Lefèvre"),
    "marchand": portrait("Général Jean Gabriel Marchand.jpg", "Jean-Gabriel Marchand", "unknown artist"),
    "poniatowski": portrait("Prince Józef Poniatowski.jpg", "Prince Józef Poniatowski", "attributed to Jean-Urbain Guérin"),
    "kutuzov": portrait("Kutuzov2 by Daw.jpg", "Field Marshal Mikhail Kutuzov", "George Dawe", "1829", "50% 14%"),
    "barclay": portrait("Barclay de Tolly (Dawe) (cropped).jpg", "Michael Barclay de Tolly", "George Dawe", "1829", "50% 16%"),
    "bagration": portrait("George Dawe - Portrait of General Pyotr Bagration (1765-1812) - Google Art Project.jpg", "Prince Pyotr Bagration", "George Dawe", focus="50% 18%"),
    "raevsky": portrait("Rajevskij N N.jpg", "Nikolay Raevsky", "George Dawe", focus="50% 18%"),
    "eugen_wurttemberg": portrait("Eugen von Württemberg (1788–1857) by Louis de Saint-Aubin - Hermitage.jpg", "Duke Eugen of Württemberg", "Louis de Saint-Aubin"),
    "denisov": portrait("Denisov 7 Vasily Timofeevich.jpg", "Vasily Denisov", "workshop of George Dawe", focus="50% 18%"),
    "vorontsov": portrait("Dawe, Mikhail Vorontsov.jpg", "Mikhail Vorontsov", "George Dawe", focus="50% 18%"),
    "stroganov": portrait("Stroganov P A.jpg", "Pavel Stroganov", "George Dawe", focus="50% 18%"),
    "kutaisov": portrait("Kutaisov.jpg", "Alexander Kutaisov", "George Dawe", focus="50% 18%"),
    "bogdanovsky": portrait("Bogdanovsky Andrey Vasilyevich.jpg", "Andrei Bogdanovsky", "workshop of George Dawe", focus="50% 18%"),
    "reynier": portrait("Jean-Louis-Ébénézer Reynier.png", "Jean Reynier", "unknown artist"),
    "ochs": portrait("Adam ludwig von ochs.jpg", "Adam Ludwig von Ochs", "unknown artist", "1823"),
    "brunswick_1806": portrait("Annetti - Charles William Ferdinand, Duke of Brunswick.png", "Charles William Ferdinand, Duke of Brunswick", "Annetti", "c. 1790"),
    "hohenlohe": portrait("Friedrich Ludwig zu Hohenlohe-Ingelfingen.jpg", "Friedrich Ludwig, Prince of Hohenlohe-Ingelfingen", "Wilhelm Arndt", "c. 1795"),
    "ruchel": portrait("Ernst von Rüchel.jpg", "Ernst von Rüchel", "unknown artist", "c. 1802"),
    "kalckreuth": portrait("Friedrich Adolf Graf von Kalckreuth.jpg", "Friedrich Adolf von Kalckreuth", "unknown artist", "1809"),
    "tauentzien": portrait("Bogislav von Tauentzien.jpg", "Bogislav von Tauentzien", "unknown artist"),
    "louis_ferdinand": portrait("Louis Ferdinand of Prussia.jpg", "Prince Louis Ferdinand of Prussia", "Jean-Laurent Mosnier", "1799"),
})

# The army lists' named commanders, by unit id, with their portraits: shown in the roster beside the army's flag
# when the army is led by one. Written to src/data/commander-portraits.json by running this file.
NAMED_COMMANDERS = {
    "pb-cmd-wellington": "wellington", "anb-cmd-wellington": "wellington", "pb-cmd-picton": "picton",
    "pf-cmd-junot": "junot", "fac-cmd-napoleon": "napoleon", "dbn-cmd-chasse": "chasse",
    "pr15-cmd-blucher": "blucher", "pr06-cmd-blucher": "blucher", "pr15-cmd-zieten": "zieten",
    "sax-cmd-thielmann": "thielmann", "fr-cmd-friant": "friant",
    "pf-cmd-massena": "massena", "pf-cmd-sebastiani": "sebastiani", "anb-cmd-kempt": "kempt", "anb-cmd-pack": "pack",
    "dbn-cmd-orange": "orange", "dbn-cmd-ghigny": "ghigny", "at-cmd-schwarzenberg": "schwarzenberg", "at-cmd-bianchi": "bianchi",
    "fr-cmd-davout": "davout", "fr-cmd-murat": "murat", "fr-cmd-compans": "compans", "fr-cmd-dessaix": "dessaix",
    "fr-cmd-tharreau": "tharreau", "fr-cmd-marchand": "marchand", "gdw-cmd-poniatowski": "poniatowski",
    "ru-cmd-platov": "platov", "ru-cmd-kutuzov": "kutuzov", "ru-cmd-barclay": "barclay", "ru-cmd-bagration": "bagration", "ru-cmd-raevsky": "raevsky",
    "ru-cmd-eugene-wurttemberg": "eugen_wurttemberg", "ru-cmd-denisov": "denisov", "ru-cmd-vorontsov": "vorontsov",
    "ru-cmd-stroganov": "stroganov", "ru-cmd-kutaisov": "kutaisov", "ru-cmd-bogdanovsky": "bogdanovsky",
    "sax-cmd-reynier": "reynier", "sax-cmd-lecoq": "lecoq", "wp-cmd-von-ochs": "ochs", "pr06-cmd-brunswick": "brunswick_1806",
    "pr06-cmd-hohenlohe": "hohenlohe", "pr06-cmd-ruchel": "ruchel", "pr06-cmd-kalckreuth": "kalckreuth",
    "pr06-cmd-tauentzien": "tauentzien", "pr06-cmd-louisferdinand": "louis_ferdinand",
}


def write_named():
    import json
    from pathlib import Path
    out = {unit: PORTRAITS[key] for unit, key in sorted(NAMED_COMMANDERS.items()) if key in PORTRAITS}
    path = Path(__file__).resolve().parents[2] / "src" / "data" / "commander-portraits.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(f"{len(out)} named commanders with portraits")


if __name__ == "__main__":
    write_named()
