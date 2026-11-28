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
    "hirschfeld": portrait("Karl Friedrich von Hirschfeld (Krethlow).jpg", "Karl Friedrich von Hirschfeld", "Johann Ferdinand Krethlow", focus="50% 22%", small=True),
    "macdonald": portrait("MacDonald par Antoine Jean Gros.jpg", "Marshal Jacques Macdonald", "Antoine-Jean Gros", focus="50% 18%"),
    "sacken": portrait("Fabian Wilhelm von Osten-Sacken.jpg", "Fabian von der Osten-Sacken", "George Dawe", "1820", "50% 18%"),
    "langeron": portrait("Langeron A F.jpg", "Count Alexandre de Langeron", "George Dawe", "before 1825", "50% 18%"),
    "kleist": portrait("Hermann Scherenberg-Friedrich Graf Kleist von Nollendorf.jpg", "Friedrich Kleist von Nollendorf", "Hermann Scherenberg", "1863", "50% 20%"),
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
    "klyastitsy": {"French": ("Marshal Oudinot", "oudinot"), "Russian": ("Lt-Gen Count Wittgenstein", "wittgenstein")},
    "saltanovka": {"French": ("Marshal Davout", "davout"), "Russian": ("Lt-Gen Raevsky", "raevsky")},
    "ostrovno": {"French": ("Marshal Murat", "murat"), "Russian": ("Lt-Gen Count Ostermann-Tolstoy", "ostermann")},
    "medina-de-rioseco": {"French": ("Marshal Bessières", "bessieres"), "Spanish": ("Gen Blake, with Gen Cuesta", "blake")},
    "bailen": {"French": ("Gén. Dupont", "dupont"), "Spanish": ("Gen Castaños", "castanos")},
    "bussaco": {"French": ("Marshal Masséna", "massena"), "Anglo-Portuguese": ("Viscount Wellington", "wellington")},
    "fuentes-de-onoro": {"Anglo-Portuguese": ("Viscount Wellington", "wellington"), "French": ("Marshal Masséna", "massena")},
    "sorauren": {"French": ("Marshal Soult", "soult"), "Anglo-Portuguese": ("The Marquess of Wellington", "wellington")},
    "orthez": {"French": ("Marshal Soult", "soult"), "Anglo-Portuguese": ("The Marquess of Wellington", "wellington")},
    "polotsk": {"French": ("Marshal Oudinot", "oudinot"), "Bavarian": ("Gén. Gouvion Saint-Cyr", "saint_cyr"), "Russian": ("Lt-Gen Count Wittgenstein", "wittgenstein")},
    "polotsk-2": {"French": ("Marshal Gouvion Saint-Cyr", "saint_cyr"), "Bavarian": ("Gen-Lt von Wrede", "wrede"), "Russian": ("Lt-Gen Count Wittgenstein", "wittgenstein")},
    "valutino": {"French": ("Marshal Ney", "ney"), "Russian": ("General Barclay de Tolly", "barclay")},
    "tarutino": {"French": ("Marshal Murat", "murat"), "Russian": ("General Bennigsen", "bennigsen")},
    "maloyaroslavets": {"French": ("Prince Eugène", "eugene"), "Russian": ("General Dokhturov", "dokhturov")},
    "vyazma": {"French": ("Marshal Davout, with Eugène and Ney", "davout"), "Russian": ("General Miloradovich", "miloradovich")},
    "krasnoi": {"French": ("Napoleon", "napoleon"), "Russian": ("Field Marshal Kutuzov", "kutuzov")},
    "smolensk": {"French": ("Napoleon", "napoleon"), "Russian": ("General Barclay de Tolly", "barclay")},
    "borodino": {"French": ("Napoleon", "napoleon"), "Russian": ("General Kutuzov", "kutuzov")},
    "berezina": {"French": ("Napoleon", "napoleon"), "Russian": ("General Wittgenstein, with Admiral Chichagov", "wittgenstein")},
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


# 1813: the War of Liberation
COMMANDERS.update({
    "mockern": {"French": ("Eugène de Beauharnais", "eugene"), "Russian": ("Lt-Gen Berg", "berg"), "Prussian": ("Gen-Lt von Yorck", "yorck")},
    "lutzen": {"French": ("Napoleon", "napoleon"), "Russian": ("General Wittgenstein", "wittgenstein"), "Prussian": ("General Blücher", "blucher")},
    "bautzen": {"French": ("Marshal Ney", "ney"), "Russian": ("General Barclay de Tolly", "barclay"), "Prussian": ("General Blücher", "blucher")},
    "grossbeeren": {"Saxon": ("Général Reynier", "reynier"), "French": ("Marshal Oudinot", "oudinot"), "Prussian": ("Gen-Lt von Bülow", "bulow")},
    "wartenburg": {"French": ("Général Bertrand", "bertrand"), "Prussian": ("Gen-Lt von Yorck", "yorck")},
    "dennewitz": {"French": ("Marshal Ney", "ney"), "Saxon": ("Général Reynier", "reynier"), "Prussian": ("Gen-Lt von Bülow", "bulow"), "Russian": ("Maj-Gen Baron Pahlen", "pahlen")},
    "katzbach": {"French": ("Marshal Macdonald", "macdonald"), "Prussian": ("General Blücher", "blucher"), "Russian": ("Gen-Lt Baron Sacken, with Langeron", "sacken")},
    "reichenbach": {"French": ("Napoleon", "napoleon"), "Russian": ("General Miloradovich", "miloradovich")},
    "mockern-leipzig": {"French": ("Marshal Marmont", "marmont"), "Prussian": ("Gen-Lt von Yorck", "yorck")},
    "luckau": {"French": ("Marshal Oudinot", "oudinot"), "Prussian": ("Gen-Lt von Bülow", "bulow")},
    "rippach": {"French": ("Napoleon, with Marshal Ney", "napoleon"), "Russian": ("Gen-Lt Winzingerode", "winzingerode")},
    "haynau": {"French": ("Gén. de Division Maison", "maison"), "Prussian": ("General Blücher", "blucher")},
    "plagwitz": {"French": ("Gén. de Division Puthod", "puthod"), "Russian": ("General Langeron", "langeron")},
    "hagelberg": {"French": ("Gén. de Division Girard", "girard"), "Prussian": ("Gen-Maj von Hirschfeld", "hirschfeld")},
    "brienne": {"French": ("Napoleon", "napoleon"), "Russian": ("Field Marshal Blücher", "blucher")},
    "champaubert": {"French": ("Napoleon", "napoleon"), "Russian": ("Gen-Lt Olsufiev", "olsufiev")},
    "montmirail": {"French": ("Napoleon", "napoleon"), "Russian": ("Gen-Lt Baron Sacken", "sacken"), "Prussian": ("Gen-Lt von Yorck", "yorck")},
    "chateau-thierry": {"French": ("Napoleon", "napoleon"), "Prussian": ("Gen-Lt von Yorck", "yorck"), "Russian": ("Gen-Lt Baron Sacken", "sacken")},
    "vauchamps": {"French": ("Napoleon", "napoleon"), "Prussian": ("Field Marshal Blücher", "blucher"), "Russian": ("Gen-Lt Kaptsevich", "kaptsevich")},
    "mormant": {"French": ("Napoleon", "napoleon"), "Russian": ("Gen-Lt Count Pahlen", "pahlen"), "Austrian": ("FML Hardegg", None), "Bavarian": ("Gen-Lt Lamotte", None)},
    "montereau": {"French": ("Napoleon", "napoleon"), "Württemberg": ("The Crown Prince of Württemberg", None), "Austrian": ("Under the Crown Prince", None)},
    "bar-sur-aube": {"French": ("Marshal Oudinot", "oudinot"), "Russian": ("General Wittgenstein", "wittgenstein"), "Bavarian": ("General Wrede", "wrede"), "Austrian": ("Under Wrede", "wrede")},
    "laubressel": {"French": ("Marshal Macdonald", "macdonald"), "Russian": ("General Wittgenstein", "wittgenstein"), "Bavarian": ("General Wrede", "wrede"), "Württemberg": ("The Crown Prince of Württemberg", None), "Austrian": ("FZM Gyulai", None)},
    "craonne": {"French": ("Napoleon", "napoleon"), "Russian": ("Gen-Lt Count Vorontsov", "vorontsov")},
    "laon": {"French": ("Napoleon", "napoleon"), "Prussian": ("Field Marshal Blücher", "blucher"), "Russian": ("Under Blücher", "blucher")},
    "reims": {"French": ("Napoleon", "napoleon"), "Russian": ("Gen-Lt Count Saint-Priest", "st_priest"), "Prussian": ("Gen-Maj von Jagow", None)},
    "limonest": {"French": ("Marshal Augereau", None), "Austrian": ("Prince Philipp of Hesse-Homburg", None)},
    "arcis-sur-aube": {"French": ("Napoleon", "napoleon"), "Bavarian": ("General Wrede", "wrede"), "Austrian": ("Field Marshal Schwarzenberg", "schwarzenberg"), "Württemberg": ("Under Schwarzenberg", "schwarzenberg"), "Russian": ("Under Schwarzenberg", "schwarzenberg"), "Prussian": ("Under Schwarzenberg", "schwarzenberg")},
    "fere-champenoise": {"French": ("Marshal Marmont", "marmont"), "Russian": ("Tsar Alexander, with Schwarzenberg", "schwarzenberg"), "Austrian": ("Under Schwarzenberg", "schwarzenberg"), "Württemberg": ("The Crown Prince of Württemberg", None)},
    "saint-dizier": {"French": ("Napoleon", "napoleon"), "Russian": ("Gen-Lt Winzingerode", "winzingerode")},
    "paris": {"French": ("King Joseph, with Marshals Marmont and Mortier", "joseph"), "Russian": ("General Barclay de Tolly", "barclay"), "Prussian": ("Field Marshal Blücher", "blucher"), "Württemberg": ("The Crown Prince of Württemberg", None), "Austrian": ("Under the Crown Prince", None)},
    "la-rothiere": {"French": ("Napoleon", "napoleon"), "Russian": ("Field Marshal Blücher", "blucher"), "Austrian": ("Under Blücher", "blucher"),
                    "Württemberg": ("Under Blücher", "blucher"), "Bavarian": ("Under Blücher", "blucher"),
                    "Prussian": ("Under Blücher", "blucher")},
    "hanau": {"French": ("Napoleon", "napoleon"), "Bavarian": ("General Wrede", "wrede"), "Austrian": ("Under Wrede", "wrede"), "Russian": ("Under Wrede", "wrede")},
})

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
    "klyastitsy-legrand": "legrand", "klyastitsy-verdier": "verdier", "klyastitsy-cavalry": "doumerc",
    "klyastitsy-kulnev": "kulnev", "klyastitsy-berg": "berg", "klyastitsy-sazonov": "sazonov",
    "saltanovka-dessaix": "dessaix", "saltanovka-compans": "compans", "saltanovka-cavalry": "bordessoulle",
    "saltanovka-kolubakin": "raevsky", "saltanovka-paskevich": "paskevich",
    "ostrovno-bruyere": "bruyere", "ostrovno-delzons": "delzons", "ostrovno-bakhmetev": "bakhmetev",
    "ostrovno-cavalry": "ostermann", "ostrovno-konovnitsyn": "konovnitsyn", "ostrovno-pahlen": "pahlen",
    # The Peninsula: commanders whose portraits we already have
    "rolica-centre": "wellington", "rolica-delaborde": "delaborde",
    "vimeiro-hill": "wellington", "vimeiro-delaborde": "delaborde", "vimeiro-reserve-fr": "junot",
    "albuera-girard": "girard", "albuera-werle": "soult", "albuera-latour-maubourg": "latour_maubourg",
    "corunna-delaborde": "delaborde",
    "talavera-hill": "wellington", "talavera-sebastiani": "sebastiani", "talavera-dragoons": "latour_maubourg",
    "salamanca-pakenham": "wellington", "salamanca-clinton": "clinton", "salamanca-portuguese": "pack", "salamanca-foy": "foy",
    "vitoria-light": "wellington", "vitoria-picton": "picton",
    # The Peninsula's divisional commanders
    "rolica-ferguson": "ferguson",
    "vimeiro-eastern-ridge": "ferguson",
    "vimeiro-reserve": "spencer",
    "vimeiro-loison": "loison",
    "albuera-cole": "cole",
    "albuera-lumley": "lumley",
    "albuera-zayas": "zayas",
    "albuera-ballesteros": "ballesteros",
    "albuera-gazan": "gazan",
    "corunna-baird": "baird",
    "corunna-hope": "hope",
    "corunna-paget": "paget_edward",
    "corunna-fraser": "fraser",
    "corunna-merle": "merle",
    "corunna-mermet": "mermet",
    "corunna-cavalry": "lahoussaye",
    "talavera-sherbrooke": "sherbrooke",
    "talavera-ruffin": "ruffin",
    "talavera-villatte": "villatte",
    "salamanca-cole": "cole",
    "salamanca-heavy": "cotton",
    "salamanca-light-cav": "cotton",
    "salamanca-clausel": "clausel",
    "salamanca-bonet": "bonet",
    "salamanca-ferey": "ferey",
    "vitoria-morillo": "morillo",
    "vitoria-cole": "cole",
    "vitoria-dalhousie": "dalhousie",
    "vitoria-portuguese": "graham",
    "vitoria-heavy": "cotton",
    "vitoria-villatte": "villatte",
    "vitoria-conroux": "conroux",
    "vitoria-darmagnac": "darmagnac",
    "medina-merle": "merle",
    "medina-blake": "blake",
    "bussaco-merle": "merle",
    "bussaco-marchand": "marchand",
    "bussaco-mermet": "mermet",
    "bussaco-loison": "loison",
    "bussaco-spencer": "spencer",
    "bussaco-cole": "cole",
    "bussaco-portuguese": "pack",
    "fuentes-spencer": "spencer",
    "fuentes-picton": "picton",
    "fuentes-cavalry": "cotton",
    "fuentes-ferey": "ferey",
    "fuentes-marchand": "marchand",
    "fuentes-mermet": "mermet",
    "fuentes-conroux": "conroux",
    "sorauren-conroux": "conroux",
    "sorauren-foy": "foy",
    "sorauren-lamartiniere": "lamartiniere",
    "sorauren-cole": "cole",
    "sorauren-pack": "pack",
    "sorauren-picton": "picton",
    "orthez-foy": "foy",
    "orthez-darmagnac": "darmagnac",
    "orthez-cole": "cole",
    "orthez-picton": "picton",
    "orthez-clinton": "clinton",
    "orthez-hussars": "cotton",
    "polotsk-legrand": "legrand",
    "polotsk-eighth": "verdier",
    "polotsk-merle": "merle",
    "polotsk-cavalry": "doumerc",
    "polotsk-deroy": "deroy",
    "polotsk-wrede": "wrede",
    "polotsk-helfreich": "helfreich",
    "polotsk-berg": "berg",
    "polotsk-sazonov": "sazonov",
    "polotsk-2-legrand": "legrand",
    "polotsk-2-eighth": "maison",
    "polotsk-2-merle": "merle",
    "polotsk-2-cavalry": "doumerc",
    "polotsk-2-bavarians": "wrede",
    "polotsk-2-yashvil": "yashvil",
    "polotsk-2-steinheil": "steinheil",
    "polotsk-2-berg": "berg",
    "valutino-marchand": "marchand",
    "valutino-konovnitsyn": "konovnitsyn",
    "valutino-stroganov": "stroganov",
    "valutino-bakhmetev": "bakhmetev",
    "tarutino-sebastiani": "murat",
    "tarutino-16th": "zajaczek",
    "tarutino-18th": "kniaziewicz",
    "tarutino-claparede": "claparede",
    "tarutino-orlov-denisov": "orlov_denisov",
    "tarutino-eugen": "eugen_wurttemberg",
    "maloyaroslavets-delzons": "delzons",
    "maloyaroslavets-broussier": "broussier",
    "maloyaroslavets-pino": "pino",
    "maloyaroslavets-12th": "raevsky",
    "maloyaroslavets-paskevich": "paskevich",
    "vyazma-compans": "compans",
    "vyazma-dessaix": "dessaix",
    "vyazma-broussier": "broussier",
    "vyazma-pino": "pino",
    "vyazma-16th": "zajaczek",
    "vyazma-eugen": "eugen_wurttemberg",
    "vyazma-paskevich": "paskevich",
    "vyazma-platov": "platov",
    "krasnoi-roguet": "roguet",
    "krasnoi-compans": "compans",
    "krasnoi-konovnitsyn": "konovnitsyn",
    "krasnoi-stroganov": "stroganov",
    "krasnoi-paskevich": "paskevich",
    "krasnoi-kolubakin": "raevsky",
    "krasnoi-eugen": "eugen_wurttemberg",
    "smolensk-marchand": "marchand",
    "smolensk-friant": "friant",
    "smolensk-16th": "zajaczek",
    "smolensk-18th": "kniaziewicz",
    "smolensk-kolubakin": "raevsky",
    "smolensk-paskevich": "paskevich",
    "smolensk-konovnitsyn": "konovnitsyn",
    "smolensk-eugen": "eugen_wurttemberg",
    "borodino-compans": "compans",
    "borodino-dessaix": "dessaix",
    "borodino-friant": "friant",
    "borodino-morand": "morand",
    "borodino-gerard": "gerard",
    "borodino-marchand": "marchand",
    "borodino-delzons": "delzons",
    "borodino-broussier": "broussier",
    "borodino-16th": "zajaczek",
    "borodino-18th": "kniaziewicz",
    "borodino-tharreau": "tharreau",
    "borodino-ochs": "ochs",
    "borodino-roguet": "roguet",
    "borodino-claparede": "claparede",
    "borodino-bruyere": "bruyere",
    "borodino-valence": "bordessoulle",
    "borodino-pajol": "pajol",
    "borodino-wathier-defrance": "montbrun",
    "borodino-grouchy": "grouchy",
    "borodino-thielmann": "thielmann",
    "borodino-eugen": "eugen_wurttemberg",
    "borodino-23rd": "bakhmetev",
    "borodino-delaborde": "delaborde", "borodino-guard-cavalry": "lefebvre_desnouettes",
    "borodino-uvarov": "uvarov",
    "borodino-korff": "korff",
    "borodino-platov": "platov",
    "borodino-12th": "raevsky",
    "borodino-paskevich": "paskevich",
    "borodino-neverovsky": "neverovsky",
    "borodino-vorontsov": "vorontsov",
    "borodino-konovnitsyn": "konovnitsyn",
    "borodino-stroganov": "stroganov",
    "borodino-2nd-cuirassiers": "duka",
    "borodino-sievers": "sievers",
    "berezina-legrand": "legrand",
    "berezina-maison": "maison",
    "berezina-merle": "merle",
    "berezina-doumerc": "doumerc",
    "berezina-steinheil": "steinheil",
    "berezina-berg": "berg",
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

# Klyastitsy
PORTRAITS.update({
    "wittgenstein": portrait("Pjotr-christianowitsch-wittgenstein.jpg", "Count Peter Wittgenstein", "George Dawe", focus="50% 18%"),
    "kulnev": portrait("Kulnev.jpg", "Yakov Kulnev", "George Dawe", focus="50% 18%"),
    "berg": portrait("Berg 1 Grigory Maximobich.jpg", "Grigory Berg", "George Dawe", focus="50% 18%"),
    "sazonov": portrait("Sazonov 1 Ivan Terentyevich.jpg", "Ivan Sazonov", "workshop of George Dawe", focus="50% 18%"),
    "oudinot": portrait("Nicolas Charles Oudinot by Robert Lefèvre.jpg", "Marshal Nicolas Oudinot", "Robert Lefèvre", "1811", "50% 16%"),
    "legrand": portrait("Général Claude Juste Alexandre Legrand.jpg", "Claude Legrand", "Antoine-Jean Gros"),
    "verdier": portrait("Jean Antoine Verdier.jpg", "Jean-Antoine Verdier", "André Dutertre"),
    "doumerc": portrait("General Doumerc.jpg", "Jean-Pierre Doumerc", "unknown artist"),
})

# Saltanovka and Ostrovno
PORTRAITS.update({
    "ostermann": portrait("Ostermann-tolstoi.jpg", "Count Alexander Ostermann-Tolstoy", "George Dawe", "1825", "50% 18%"),
    "konovnitsyn": portrait("George Dawe - Portrait of Pyotr P. Konovnitsyn.jpg", "Pyotr Konovnitsyn", "George Dawe", focus="50% 18%"),
    "pahlen": portrait("Peter Graf von der Pahlen.jpg", "Count Peter von der Pahlen", "George Dawe", focus="50% 18%"),
    "paskevich": portrait("Ivan Paskevich.jpg", "Ivan Paskevich", "George Dawe", "1823", "50% 18%"),
    "bakhmetev": portrait("Bahmetyev 3 Alexey Nikolaevich.jpg", "Alexey Bakhmetev", "George Dawe", focus="50% 18%"),
    "delzons": portrait("General Delzons Maitrier - cropped.png", "Alexis Joseph Delzons", "Maitrier", "1830"),
    "bruyere": portrait("Général Jean Pierre Bruguière dit Bruyères.jpg", "Jean-Pierre Bruyère", "unknown artist", small=True),
    "bordessoulle": portrait("Brémond - General Bordessoule.jpg", "Étienne de Bordessoulle", "Jean-François Brémond", "1838"),
})

# The Peninsula's divisional commanders
PORTRAITS.update({
    "ferguson": portrait("Anthony Cardon - Sir Ronald Craufurd Ferguson, M P - B1977.14.9921 - Yale Center for British Art.jpg", "Sir Ronald Craufurd Ferguson", "Anthony Cardon", "1810", "50% 18%"),
    "spencer": portrait("WP Brent Spencer.jpg", "Sir Brent Spencer", "unknown artist", None, "50% 18%"),
    "loison": portrait("Général Louis Henri Loison.jpg", "Louis Henri Loison", "unknown artist", None, "50% 18%"),
    "cole": portrait("Sir Galbraith Lowry Cole by William Dyce.jpg", "Sir Lowry Cole", "William Dyce", None, "50% 18%"),
    "lumley": portrait("Sir William Lumley (1769-1850).jpg", "Sir William Lumley", "Thomas Lawrence", None, "50% 18%"),
    "zayas": portrait("El general José Pascual de Zayas y Chacón, por Vicente López.jpg", "José Pascual de Zayas", "Vicente López", "c. 1818", "50% 18%"),
    "ballesteros": portrait("Ballesteros, PA02569.jpg", "Francisco Ballesteros", "unknown artist", None, "50% 18%"),
    "gazan": portrait("Honoré Théodore Maxime Gazan de la Peyrière.png", "Honoré Gazan", "Aubry", "1804", "50% 18%"),
    "baird": portrait("Sir David Baird, 3rd Bt by Southwell Brothers.jpg", "Sir David Baird", "Southwell Brothers", None, "50% 18%"),
    "hope": portrait("Henry Raeburn (1756-1823) - General Sir John Hope, 4th Earl of Hopetoun, GCB - CUPMS-1998.98 - County Buildings (West Section) St Catherine's Street, Cupar.jpg", "Sir John Hope", "Henry Raeburn", None, "50% 18%"),
    "paget_edward": portrait("Martin Archer Shee (1769-1850) - Sir Edward Paget (1775–1849), General - 1138 - Government Art Collection.jpg", "Sir Edward Paget", "Martin Archer Shee", None, "50% 18%"),
    "fraser": portrait("Alexander Mackenzie Fraser.jpg", "Alexander Mackenzie Fraser", "after Henry Raeburn", None, "50% 18%"),
    "merle": portrait("Pierre Hugues Victoire Merle (1766-1830).jpg", "Pierre Hugues Victoire Merle", "unknown artist", None, "50% 18%"),
    "mermet": portrait("Julien Auguste Joseph Mermet.jpg", "Julien Mermet", "unknown artist", None, "50% 18%"),
    "lahoussaye": portrait("Armand Lebrun de La Houssaye (1768-1846) Col.jpg", "Armand Lebrun de La Houssaye", "unknown artist", None, "50% 18%"),
    "sherbrooke": portrait("John Coape Sherbrooke.jpg", "Sir John Sherbrooke", "Robert Field", None, "50% 18%"),
    "ruffin": portrait("François Amable Ruffin.jpg", "François Amable Ruffin", "unknown artist", None, "50% 18%"),
    "villatte": portrait("Général Eugène Casimir Villatte.png", "Eugène-Casimir Villatte", "unknown artist", None, "50% 18%", small=True),
    "cotton": portrait("Portrait of General Stapleton Cotton, Viscount & Baron Combermere, G.C.B. (4671422).jpg", "Sir Stapleton Cotton", "Joseph John Jenkins", "1833", "50% 18%"),
    "clausel": portrait("Clausel, PA03433.jpg", "Bertrand Clausel", "Antoine Maurin", "1851", "50% 18%"),
    "bonet": portrait("Jean Pierre François Bonet (1768-1857).jpg", "Jean-Pierre-François Bonet", "unknown artist", None, "50% 18%"),
    "ferey": portrait("Claude François Ferey, baron de Rosengath (1771-1812).jpg", "Claude François Ferey", "F. G. Weitsch", "1808", "50% 18%"),
    "graham": portrait("Thomas Graham (1748–1843), Baron Lynedoch by Thomas Lawrence 1.jpg", "Sir Thomas Graham", "Thomas Lawrence", "1817", "50% 18%"),
    "morillo": portrait("Pablo-morillo.jpg", "Pablo Morillo", "Horace Vernet", None, "50% 18%"),
    "dalhousie": portrait("George Ramsay, 9th Earl of Dalhousie, from the National Gallery of Canada (cropped).jpg", "The Earl of Dalhousie", "unknown artist", None, "50% 18%"),
    "conroux": portrait("Nicolas François Conroux.jpg", "Nicolas François Conroux", "Jean-Baptiste Wicar", None, "50% 18%"),
    "darmagnac": portrait("Général Jean Barthélémy Claude Toussaint Darmagnac.png", "Jean Barthélemy Darmagnac", "unknown artist", None, "50% 18%", small=True),
})

# Polotsk
PORTRAITS.update({
    "saint_cyr": portrait("Laurent de Gouvion-Saint-Cyr.jpg", "Laurent Gouvion Saint-Cyr", "Horace Vernet", "1821", "50% 16%"),
    "deroy": portrait("Le général Bernhard Erasmus von Deroy (F. Hanfstaengl, 1829).jpg", "Bernhard Erasmus von Deroy", "Franz Hanfstaengl", "1829"),
    "wrede": portrait("Karl Philipp Wrede.jpg", "Karl Philipp von Wrede", "Franz Hanfstaengl", "1828"),
    "maison": portrait("Maison, Nicolas-Joseph.jpg", "Nicolas Joseph Maison", "Alois Senefelder", small=True),
    "corbineau": portrait("Lieutenant-général Corbineau.jpg", "Jean-Baptiste Corbineau", "unknown artist", "c. 1830"),
    "yashvil": portrait("Yashvil LM.jpg", "Prince Lev Yashvil", "George Dawe", focus="50% 18%"),
    "helfreich": portrait("Gelfrejh Bogdan Borisovich.jpg", "Bogdan von Helfreich", "George Dawe", focus="50% 18%"),
})

# Tarutino and Maloyaroslavets
PORTRAITS.update({
    "bennigsen": portrait("PPN663944481 Bildnis von Levin August Gottlieb Bennigsen (1822).jpg", "Count Levin von Bennigsen", "George Dawe", "1822", "50% 18%"),
    "dokhturov": portrait("Dmitry Sergeyevich Dokhturov.jpg", "Dmitry Dokhturov", "George Dawe", "1819", "50% 18%"),
    "eugene": portrait("Portrait of Prince Eugene de Beauharnais, Viceroy of Italy and Duke of Leuchtenberg.jpg", "Eugène de Beauharnais, Viceroy of Italy", "Andrea Appiani", "1810"),
    "orlov_denisov": portrait("Orlov-Denisov.jpg", "Count Vasily Orlov-Denisov", "workshop of George Dawe", focus="50% 18%"),
    "claparede": portrait("Villain -Michel Marie Claparède (1770-1842) - French General - Peer of France.jpg", "Michel Claparède", "François le Villain", "1835"),
    "broussier": portrait("Général Broussier jean-baptiste.jpg", "Jean-Baptiste Broussier", "Bovinet"),
    "pino": portrait("Domenico Pino.jpg", "Domenico Pino", "unknown artist"),
    "kniaziewicz": portrait("Karol Otto Kniaziewicz 1.PNG", "Karol Kniaziewicz", "unknown artist"),
    "zajaczek": portrait("Le général Zayonchek.png", "Józef Zajączek", "André Dutertre"),
})

# Vyazma and Krasnoi
PORTRAITS.update({
    "miloradovich": portrait("Mikhail Andreevitch Miloradovitch by George Dawe - Suvorov museum.jpg", "Count Mikhail Miloradovich", "George Dawe", focus="50% 18%"),
    "roguet": portrait("François Roguet.jpg", "François Roguet", "unknown artist"),
})

# Borodino
PORTRAITS.update({
    "morand": portrait("Portrait équestre du général Morand.jpg", "Charles-Antoine Morand", "unknown artist"),
    "gerard": portrait("David Etienne Maurice Gerard.jpg", "Étienne Maurice Gérard", "Jacques-Louis David", "1816", "50% 14%"),
    "neverovsky": portrait("Dmitry Petrovich Neverovsky.jpg", "Dmitry Neverovsky", "workshop of George Dawe", focus="50% 18%"),
    "uvarov": portrait("Uvarov Fedor.jpg", "Fyodor Uvarov", "workshop of George Dawe", focus="50% 18%"),
    "depreradovich": portrait("Depreradovich Nikolay Ivanovich.jpg", "Nikolay Depreradovich", "George Dawe", focus="50% 18%"),
    "korff": portrait("Korf Fyodor Karlovich.jpg", "Baron Fyodor Korff", "workshop of George Dawe", focus="50% 18%"),
    "sievers": portrait("Sievers 1 Karl Karlovich.jpg", "Count Karl Sievers", "workshop of George Dawe", focus="50% 18%"),
    "montbrun": portrait("Velyn - Louis-Pierre de Montbrun, comte de l'Empire, né le 30 mars 1771 à Florensac.jpg", "Louis-Pierre Montbrun", "Philippus Velijn"),
    "pajol": portrait("Le Général Pajol (1772-1844).jpg", "Claude-Pierre Pajol", "Charles Formentin"),
    "duka": portrait("Duka Ilya Michailovich.jpg", "Ilya Duka", "George Dawe", focus="50% 18%"),
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


# Each campaign's chief commanders, shown with their portraits on its card in the Historical forces list.
# Written to src/data/battles/campaign-commanders.json by running this file.
PORTRAITS.update({
    "bernadotte": portrait("Charles XIV John as Crown Prince of Sweden - François Gérard.jpg", "Jean-Baptiste Bernadotte, Crown Prince of Sweden", "after François Gérard", focus="50% 18%"),
})
CAMPAIGN_COMMANDERS = {
    "peninsular-war": [("Wellington", "wellington"), ("Moore", "moore"), ("Soult", "soult"), ("Masséna", "massena")],
    "russia-1812": [("Napoleon", "napoleon"), ("Kutuzov", "kutuzov"), ("Barclay de Tolly", "barclay"), ("Bagration", "bagration")],
    "liberation-1813": [("Napoleon", "napoleon"), ("Blücher", "blucher"), ("Schwarzenberg", "schwarzenberg"), ("Bernadotte", "bernadotte")],
    "france-1814": [("Napoleon", "napoleon"), ("Blücher", "blucher"), ("Schwarzenberg", "schwarzenberg"), ("Marmont", "marmont")],
    "hundred-days": [("Napoleon", "napoleon"), ("Wellington", "wellington"), ("Blücher", "blucher"), ("Ney", "ney")],
}


def write_campaigns():
    import json
    from pathlib import Path
    out = {c: [{"name": name, **({"portrait": PORTRAITS[key]} if key in PORTRAITS else {})} for name, key in people]
           for c, people in CAMPAIGN_COMMANDERS.items()}
    path = Path(__file__).resolve().parents[2] / "src" / "data" / "battles" / "campaign-commanders.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(f"{len(out)} campaigns' commanders")


def write_named():
    import json
    from pathlib import Path
    out = {unit: PORTRAITS[key] for unit, key in sorted(NAMED_COMMANDERS.items()) if key in PORTRAITS}
    path = Path(__file__).resolve().parents[2] / "src" / "data" / "commander-portraits.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(f"{len(out)} named commanders with portraits")


# 1813 forces' commanders
FORCE_PORTRAITS.update({
    "mockern-cavalry": "bruyere", "mockern-roth": "berg",
    "lutzen-girard": "girard", "lutzen-marchand": "marchand", "lutzen-berg": "berg", "lutzen-eugen": "eugen_wurttemberg",
    "grossbeeren-lecoq": "lecoq", "grossbeeren-durutte": "durutte",
    "wartenburg-morand": "morand", "wartenburg-yorck": "yorck",
    "dennewitz-morand": "morand", "dennewitz-durutte": "durutte", "dennewitz-lecoq": "lecoq", "dennewitz-bulow": "bulow",
    "katzbach-yorck": "yorck", "katzbach-maison": "maison", "katzbach-sebastiani": "sebastiani", "katzbach-sacken": "sacken",
    "katzbach-xi-cavalry": "gerard",
    "reichenbach-durutte": "durutte", "reichenbach-eugen": "eugen_wurttemberg", "reichenbach-latour-maubourg": "latour_maubourg",
    "mockern-leipzig-compans": "compans", "mockern-leipzig-yorck": "yorck", "mockern-leipzig-delmas": "delmas",
    "luckau-bulow": "bulow",
    "hanau-old-guard": "friant", "hagelberg-girard": "girard", "hagelberg-hirschfeld": "hirschfeld",
    "mockern-yorck": "yorck", "lutzen-yorck": "yorck", "bautzen-yorck": "yorck", "bautzen-kleist": "kleist",
    "mockern-bulow": "bulow", "grossbeeren-bulow": "bulow", "lutzen-blucher": "blucher", "bautzen-blucher": "blucher",
})


# 1813's commanders, filled in across the campaign: public-domain portraits only (the CC BY-SA ones of Pacthod,
# Souham, Dumoustier and Barrois are left out, as a portrait here carries no licence to credit)
PORTRAITS.update({
    "puthod": portrait("Jacques Pierre Louis Marie Joseph Puthod.jpg", "Jacques-Pierre-Louis Puthod", "unknown artist"),
    "bertrand": portrait("General Henri Gatien, count Bertrand by Paul Delaroche.png", "Henri-Gatien Bertrand", "Paul Delaroche", "c. 1840", "50% 18%"),
    "delmas": portrait("Delmas.jpg", "Antoine Guillaume Delmas", "19th-century engraving"),
    "franquemont": portrait("Comte Frederic v. Franquemont.jpg", "Friedrich von Franquemont", "unknown artist"),
    "charpentier": portrait("Comte général Henri François Marie Charpentier (1769-1831).jpg", "Henri François Marie Charpentier", "unknown artist"),
    "raglovich": portrait("Barbara Krafft - Generalleutnant Clemens Freiherr von Raglovich (ca.1813).jpg", "Clemens von Raglovich", "Barbara Krafft", "c. 1813"),
    "fontanelli": portrait("PORTRAIT OF ACHILLE FONTANELLI.PNG", "Achille Fontanelli", "Andrea Appiani"),
    "dombrowski": portrait("Jan Henryk Dąbrowski 1.PNG", "Jan Henryk Dąbrowski", "unknown artist", focus="50% 18%"),
    "ricard": portrait("Etienne Pierre Sylvestre Ricard.jpg", "Étienne Pierre Sylvestre Ricard", "from Panckoucke's portraits of French generals", "1818"),
    "chaplitz": portrait("Chaplits Yefim Ignatyevich.jpg", "Yefim Chaplits", "workshop of George Dawe", focus="50% 18%"),
    "insov": portrait("Inzov Ivan Nikitich.jpg", "Ivan Inzov", "workshop of George Dawe", focus="50% 18%"),
    "emmanuel": portrait("EmmanuelGA.jpg", "Georgi Emmanuel", "George Dawe", focus="50% 18%"),
    "st_priest": portrait("Saint-Priest E F.jpg", "Guillaume Emmanuel de Saint-Priest", "George Dawe", focus="50% 18%"),
    "guilleminot": portrait("Le général Guilleminot (1774-1840) vers 1823.jpg", "Armand Charles Guilleminot", "Louise Adélaïde Desnos", "1843"),
    "arrighi": portrait("Jean-Thomas Arrighi de Casanova.jpg", "Jean-Toussaint Arrighi de Casanova", "unknown artist"),
    "dubreton": portrait("J. L. Dubreton Lieut. Général, Pair de France (BM 1929,0608.24).jpg", "Jean-Louis Dubreton", "unknown artist", focus="50% 25%"),
    "nansouty": portrait("Etienne-Marie-Antoine Champion de Nansouty.jpg", "Étienne de Nansouty", "L. Lanta, engraved by Paul Petit"),
    "mensdorff": portrait("Emanuel Graf Mensdorff-Pouilly.jpg", "Emmanuel von Mensdorff-Pouilly", "Ferdinand Georg Waldmüller", "1839"),
    "rochambeau": portrait("Donatien de Rochambeau.jpg", "Donatien de Rochambeau", "unknown artist"),
    "ilarion_vasilchikov": portrait("I.I. Vasilchikov.JPG", "Illarion Vasilchikov", "photograph by Ivan Gudovsky", "1850s"),
    "brenier": portrait("Antoine François Brenier de Montmorand.jpg", "Antoine-François Brenier", "unknown artist"),
    "normann": portrait("Karl von Normann-Ehrenfels.jpg", "Karl von Normann-Ehrenfels", "unknown artist"),
    "beaumont": portrait("Louis Chrétien Carrière de Beaumont.jpg", "Louis Chrétien Carrière de Beaumont", "unknown artist"),
    "lorencz": portrait("Guillaume Latrille de Lorencez.jpg", "Guillaume Latrille de Lorencez", "unknown artist"),
    "brayer": portrait("Général Brayer Michel Sylvestre.jpg", "Michel Sylvestre Brayer", "unknown artist"),
    "dermoncourt": portrait("Dermoncourt.jpg", "Paul Ferdinand Dermoncourt", "unknown artist"),
    "gablenz": portrait("Heinrich Adolf Freiherr von Gablenz.jpg", "Heinrich Adolph von Gablenz", "Ferdinand von Rayski", "1841"),
    "spleny": portrait("Gabriel-splenyi-Mihalay.jpg", "Gabriel Splényi", "Maximilian Mändl", "1897"),
    "zeschau": portrait("Heinrich Wilhelm von Zeschau als Vrijmetselaar.jpg", "Heinrich Wilhelm von Zeschau", "unknown artist", "1866", small=True),
    "shcherbatov": portrait("Scherbatov 1 Alexey Grigoryevich.jpg", "Alexei Shcherbatov", "George Dawe", focus="50% 18%"),
    "olsufiev": portrait("Olsufjev 1 Zahar Dmitrievich.jpg", "Zakhar Olsufiev", "workshop of George Dawe", focus="50% 18%"),
    "bessieres": portrait("Reisener - Portrait du maréchal Jean-Baptiste Bessières, duc d'Istries (1768-1813).jpg", "Marshal Jean-Baptiste Bessières", "Henri-François Riesener", focus="50% 15%"),
    "winzingerode": portrait("Vinzingerode.jpg", "Ferdinand von Wintzingerode", "workshop of George Dawe", focus="50% 18%"),
    "kaptsevich": portrait("Kaptzevich Petr.jpg", "Pyotr Kaptsevich", "George Dawe", "1821", "50% 18%"),
})

FORCE_PORTRAITS.update({
    # Already in the gallery
    "bautzen-guard-cavalry": "lefebvre_desnouettes", "reichenbach-guard-cavalry": "lefebvre_desnouettes",
    "katzbach-korff": "korff", "plagwitz-korff": "korff", "bautzen-maison": "maison", "bautzen-morand": "morand",
    "bautzen-compans": "compans", "bautzen-bonet": "bonet", "bautzen-gerard": "gerard", "bautzen-old-guard": "roguet",
    "bautzen-eugen": "eugen_wurttemberg", "bautzen-berg": "berg", "dennewitz-tauentzien": "tauentzien",
    "hanau-sebastiani": "sebastiani", "katzbach-marchand": "marchand", "reichenbach-reinforcements": "miloradovich",
    # Found for 1813
    "bautzen-puthod": "puthod", "plagwitz-puthod": "puthod",
    "bautzen-beaumont": "beaumont", "dennewitz-beaumont": "beaumont", "luckau-cavalry": "beaumont", "wartenburg-beaumont": "beaumont",
    "bautzen-delmas": "delmas", "katzbach-delmas": "delmas",
    "bautzen-franquemont": "franquemont", "dennewitz-franquemont": "franquemont", "wartenburg-franquemont": "franquemont",
    "bautzen-charpentier": "charpentier", "hanau-charpentier": "charpentier", "katzbach-charpentier": "charpentier",
    "bautzen-raglovich": "raglovich", "dennewitz-raglovich": "raglovich",
    "dennewitz-fontanelli": "fontanelli", "wartenburg-fontanelli": "fontanelli",
    "dennewitz-dombrowski": "dombrowski", "mockern-leipzig-dombrowski": "dombrowski",
    "dennewitz-gablenz": "gablenz", "grossbeeren-gablenz": "gablenz",
    "katzbach-ricard": "ricard", "lutzen-ricard": "ricard",
    "bautzen-chaplitz": "chaplitz", "bautzen-shcherbatov": "shcherbatov", "plagwitz-shcherbatov": "shcherbatov", "katzbach-shcherbatov": "shcherbatov",
    "bautzen-insov": "insov", "bautzen-lorencz": "lorencz", "bautzen-emmanuel": "emmanuel", "bautzen-st-priest": "st_priest",
    "dennewitz-guilleminot": "guilleminot", "dennewitz-arrighi": "arrighi", "hanau-dubreton": "dubreton", "hanau-guard-cavalry": "nansouty",
    "hanau-spleny": "spleny", "hanau-mensdorff": "mensdorff", "katzbach-brayer": "brayer", "mockern-leipzig-brayer": "brayer",
    "katzbach-rochambeau": "rochambeau", "katzbach-dermoncourt": "dermoncourt", "katzbach-vasilchikov": "ilarion_vasilchikov",
    "katzbach-olsufiev": "olsufiev", "katzbach-kaptsevich": "kaptsevich", "lutzen-brenier": "brenier",
    "mockern-leipzig-normann": "normann", "rippach-guard-cavalry": "bessieres", "rippach-winzingerode": "winzingerode", "reichenbach-saxons": "zeschau",
    # 1814
    "brienne-guard-cavalry": "lefebvre_desnouettes",
    "la-rothiere-guard-cavalry": "nansouty", "la-rothiere-ricard": "ricard",
    "champaubert-ricard": "ricard", "montmirail-ricard": "ricard", "montmirail-friant": "friant",
    "montmirail-lefebvre-desnouettes": "lefebvre_desnouettes", "chateau-thierry-friant": "friant",
    "chateau-thierry-lefebvre-desnouettes": "lefebvre_desnouettes", "vauchamps-ricard": "ricard", "vauchamps-friant": "friant",
    "vauchamps-lefebvre-desnouettes": "lefebvre_desnouettes", "craonne-friant": "friant", "craonne-charpentier": "charpentier",
    "craonne-pac": "nansouty", "vauchamps-kleist": "kleist", "vauchamps-kaptsevich": "kaptsevich",
    "laon-friant": "friant", "laon-charpentier": "charpentier", "laon-ricard": "ricard", "laon-arrighi": "arrighi",
    "paris-ricard": "ricard", "paris-arrighi": "arrighi", "paris-charpentier": "charpentier",
    "laubressel-brayer": "brayer", "laubressel-leval": "leval",
    "la-rothiere-gyulai": "gyulai", "la-rothiere-olsufiev": "olsufiev", "la-rothiere-vasilchikov": "ilarion_vasilchikov",
    "la-rothiere-wurttemberg": "wurttemberg_crown_prince", "la-rothiere-paskevich": "paskevich",
    "craonne-vasilchikov": "ilarion_vasilchikov", "craonne-stroganov": "stroganov",
    "laon-yorck": "yorck", "laon-kleist": "kleist", "laon-bulow": "bulow",
    "reims-emmanuel": "emmanuel",
    "laubressel-eugen": "eugen_wurttemberg", "bar-sur-aube-eugen": "eugen_wurttemberg", "arcis-sur-aube-eugen": "eugen_wurttemberg",
    "paris-eugen": "eugen_wurttemberg", "brienne-pahlen": "pahlen", "mormant-pahlen": "pahlen", "laubressel-pahlen": "pahlen",
    "bar-sur-aube-pahlen": "pahlen", "arcis-sur-aube-pahlen": "pahlen", "fere-champenoise-pahlen": "pahlen", "paris-pahlen": "pahlen",
    "laon-pac": "nansouty", "reims-ricard": "ricard", "reims-arrighi": "arrighi", "reims-friant": "friant",
    "champaubert-olsufiev": "olsufiev", "montmirail-yorck": "yorck", "chateau-thierry-yorck": "yorck",
    "montmirail-vasilchikov": "ilarion_vasilchikov", "chateau-thierry-vasilchikov": "ilarion_vasilchikov",
})


if __name__ == "__main__":
    write_named()
    write_campaigns()
