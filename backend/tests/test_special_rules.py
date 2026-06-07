"""Regression: specialRules array on the 7 non-Astartes factions."""
import os
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL_FOR_TESTS", "http://localhost:8001")
TIMEOUT = 15

EXPECTED_COUNTS = {
    "solar-auxilia": 2,
    "imperialis-militia": 2,
    "knight-household": 2,
    "legio-titanicus": 1,
    "mechanicum-taghmata": 2,
    "legio-custodes": 1,
    "daemons-ruinstorm": 3,
}

EXPECTED_FIRST_NAMES = {
    "solar-auxilia": "Legate Commanders",
    "imperialis-militia": "Discipline Masters / Rogue Psykers",
    "knight-household": "Ion Gauntlet",
    "legio-titanicus": "Void Shields",
    "mechanicum-taghmata": "Automaton",
    "legio-custodes": "The Emperor's Chosen",
    "daemons-ruinstorm": "Instability",
}


def _get(path):
    r = requests.get(f"{BASE_URL}{path}", timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def test_special_rules_present_with_correct_shape():
    for fid, count in EXPECTED_COUNTS.items():
        f = _get(f"/api/factions/{fid}")
        sr = f.get("specialRules")
        assert isinstance(sr, list), f"{fid} missing specialRules array"
        assert len(sr) == count, f"{fid} expected {count} rules, got {len(sr)}"
        for rule in sr:
            assert isinstance(rule.get("name"), str) and rule["name"]
            assert isinstance(rule.get("description"), str) and len(rule["description"]) > 30


def test_special_rules_first_entry_names():
    for fid, expected_name in EXPECTED_FIRST_NAMES.items():
        f = _get(f"/api/factions/{fid}")
        assert f["specialRules"][0]["name"] == expected_name, (
            f"{fid}: first rule expected '{expected_name}', got '{f['specialRules'][0]['name']}'"
        )


def test_astartes_factions_have_no_special_rules():
    """Special Rules box must not surface for Astartes — the legion trait covers them."""
    for fid in ("sons-of-horus", "dark-angels", "ultramarines"):
        f = _get(f"/api/factions/{fid}")
        sr = f.get("specialRules")
        assert sr is None or sr == [], f"{fid} unexpectedly has specialRules={sr}"
