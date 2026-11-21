"""
Staff Ratings for historical forces. Orders of battle don't give them, so every commander is rated 8 unless
he's one of the book's named commanders, who come with their own. Where a list can't rate a commander 8 (a
unit only offered at 7, or Russia's "half of all brigade commanders must be Staff Rating 7"), he gets the
nearest it allows, and the force's notes say so.

Run on each battle as it's written (see hundred_days.py and russia_1812.py), after the forces are built, so
the forces' own tables don't need to give ratings at all.
"""

import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "src" / "data" / "supplements"
DEFAULT = 8
_nations: dict[str, dict] = {}


def nation(nation_id: str) -> dict:
    if not _nations:
        for f in DATA.glob("*/nations/*.json"):
            n = json.loads(f.read_text())
            _nations[n["id"]] = n
    return _nations[nation_id]


def _rated(variants: list[dict], cap: int) -> list[dict]:
    """A unit's Staff Rating choices up to `cap`, highest first, plain before Marshal's baton"""
    rated = [v for v in variants if v.get("staffRating") or re.match(r"Staff rating \d+", v["label"])]
    rating = lambda v: v.get("staffRating") or int(re.match(r"Staff rating (\d+)", v["label"]).group(1))
    rated = [v for v in rated if rating(v) <= cap]
    return sorted(rated, key=lambda v: (-rating(v), "baton" in v["label"].lower())), rating


def _set(line: dict, unit: dict, cap: int) -> int | None:
    """Rates a commander line at most `cap`, as near as the unit allows; the rating given, or None for a named one"""
    variants = unit.get("variants") or []
    if not variants:
        return None
    choices, rating = _rated(variants, cap)
    if not choices:
        choices, rating = _rated(variants, 99)
        choices = sorted(choices, key=lambda v: rating(v))
    line["variant"] = choices[0]["label"]
    return rating(choices[0])


# Sentences of a force's own notes about ratings, which the standard note replaces
RATING_TEXT = re.compile(r"Staff Rating|our judgement|is rated|at Staff|rated \d", re.I)


def _drop_rating_text(notes: list[str]) -> list[str]:
    kept = []
    for note in notes:
        sentences = re.split(r"(?<=[.;])\s+", note)
        rest = " ".join(s for s in sentences if not RATING_TEXT.search(s)).strip()
        if rest:
            kept.append(rest)
    return kept


def apply(battle: dict) -> dict:
    for force in battle["forces"]:
        n = nation(force["nationId"])
        units = {u["id"]: u for u in n["units"]}
        types = {b["id"]: b for b in n["brigades"]}
        lower: list[str] = []
        named: list[str] = []

        for line in force.get("command", []):
            unit = units[line["unit"]]
            got = _set(line, unit, DEFAULT)
            if got is None:
                named.append(unit["name"])
            elif got < DEFAULT:
                lower.append(f"{line.get('name') or unit['name']} at {got}, the most the list allows")

        rule = n.get("brigadeCommanderRating")
        brigades = [b for b in force["brigades"] if types[b["type"]].get("commanderUnitId")]
        above = len(brigades) if not rule else int(len(brigades) * rule["maxShareAbove"])
        for i, b in enumerate(brigades):
            unit = units[types[b["type"]]["commanderUnitId"]]
            b.setdefault("commander", {})
            cap = DEFAULT if i < above else rule["maxRating"]
            got = _set(b["commander"], unit, cap)
            if got is not None and got < DEFAULT and i < above:
                lower.append(f"{b['commander'].get('name') or b.get('name')} at {got}, the most the list allows")
        if rule and len(brigades) > above:
            held = len(brigades) - above
            lower.append(
                f"{held} of the {len(brigades)} brigade commanders at {rule['maxRating']}, as the list rates at most "
                f"half of them higher" if len(brigades) > 1 else f"the brigade commander at {rule['maxRating']}, as the list rates at most half of them higher"
            )

        note = "Commanders are at Staff Rating 8, the default for historical forces"
        if named:
            note += f", except the book's named {' and '.join(named)}, with his own rating"
        if lower:
            note += f"; but {'; '.join(lower)}"
        force["notes"] = _drop_rating_text(force.get("notes", [])) + [note + "."]
    return battle
