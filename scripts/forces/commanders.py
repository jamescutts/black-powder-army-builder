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


def portrait(file, title, artist, date=None, focus="50% 20%"):
    p = {"src": thumb(file), "title": title, "artist": artist,
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
# No public-domain portrait found for Grawert, Steinheil or Löwis of Menar; their sides show the name alone
EXTRA = {}

COMMANDERS = {
    "ligny": {"French": ("Napoleon", "napoleon"), "Prussian": ("Field Marshal Blücher", "blucher")},
    "quatre-bras": {"French": ("Marshal Ney", "ney"), "Anglo-allied": ("The Duke of Wellington", "wellington")},
    "waterloo": {"Anglo-allied": ("The Duke of Wellington", "wellington"), "French": ("Napoleon", "napoleon"), "Prussian": ("Field Marshal Blücher", "blucher")},
    "wavre": {"French": ("Marshal Grouchy", "grouchy"), "Prussian": ("Lt-Gen von Thielmann", "thielmann")},
    "eckau": {"Prussian": ("Gen-Lt von Grawert", "grawert"), "Russian": ("Maj-Gen Löwis of Menar", "lowis")},
    "mesoten": {"Prussian": ("Gen-Lt von Yorck", "yorck"), "Russian": ("Lt-Gen Count Steinheil", "steinheil")},
    "rolica": {"Anglo-Portuguese": ("Sir Arthur Wellesley", "wellington"), "French": ("Gén. de Division Delaborde", "delaborde")},
    "vimeiro": {"Anglo-Portuguese": ("Sir Arthur Wellesley", "wellington"), "French": ("Gén. Junot", "junot")},
    "albuera": {"Anglo-Portuguese": ("Marshal Beresford", "beresford"), "Spanish": ("Gen. Joaquín Blake", "blake"), "French": ("Marshal Soult", "soult")},
    "corunna": {"British": ("Lt-Gen Sir John Moore", "moore"), "French": ("Marshal Soult", "soult")},
    "talavera": {"British": ("Sir Arthur Wellesley", "wellington"), "French": ("King Joseph, with Marshal Jourdan", "joseph")},
    "salamanca": {"Anglo-Portuguese": ("The Earl of Wellington", "wellington"), "French": ("Marshal Marmont", "marmont")},
    "vitoria": {"Anglo-Allied": ("The Marquess of Wellington", "wellington"), "Spanish": ("Under Wellington", "wellington"),
                "French": ("King Joseph, with Marshal Jourdan", "joseph")},
}


def apply(battle: dict) -> dict:
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
