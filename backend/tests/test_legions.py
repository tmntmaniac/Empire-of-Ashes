"""Backend tests for the 18 Legiones Astartes expansion (Jan 2026).

Validates that /api/factions returns exactly 18 legions and each detail endpoint
inherits formations/upgrades/units from the Sons of Horus baseline while
applying identity + legionTrait overrides from legions.json.
"""
import os
import pytest
import requests

BASE_URL = os.environ.get(
    'REACT_APP_BACKEND_URL',
    'https://armageddon-squad.preview.emergentagent.com',
).rstrip('/')

EXPECTED_IDS = [
    "dark-angels", "emperors-children", "iron-warriors", "white-scars",
    "space-wolves", "imperial-fists", "night-lords", "blood-angels",
    "iron-hands", "world-eaters", "ultramarines", "death-guard",
    "thousand-sons", "sons-of-horus", "word-bearers", "salamanders",
    "raven-guard", "alpha-legion",
]

# Identity overrides we expect from legions.json
EXPECTED_OVERRIDES = {
    "dark-angels":      {"name": "Dark Angels",       "trait": "Grim Resolve",       "color": "#1F4D2B"},
    "emperors-children":{"name": "Emperor's Children","trait": "Flawless Execution", "color": "#7A2DA0"},
    "iron-warriors":    {"name": "Iron Warriors",     "trait": "Siege Masters",      "color": "#8C8079"},
    "white-scars":      {"name": "White Scars",       "trait": "Lightning Attack",   "color": "#E6E2D3"},
    "space-wolves":     {"name": "Space Wolves",      "trait": "Sons of Russ",       "color": "#324C5E"},
    "imperial-fists":   {"name": "Imperial Fists",    "trait": "Stoic Defenders",    "color": "#D0A93B"},
    "night-lords":      {"name": "Night Lords",       "trait": "Terror Tactics",     "color": "#2C2F4A"},
    "blood-angels":     {"name": "Blood Angels",      "trait": "Red Thirst",         "color": "#A41C1C"},
    "iron-hands":       {"name": "Iron Hands",        "trait": "Flesh is Weak",      "color": "#3C3F44"},
    "world-eaters":     {"name": "World Eaters",      "trait": "Blood Frenzy",       "color": "#C2C2C2"},
    "ultramarines":     {"name": "Ultramarines",      "trait": "Codex Astartes",     "color": "#1F4FA4"},
    "death-guard":      {"name": "Death Guard",       "trait": "Indomitable",        "color": "#7B8C4E"},
    "thousand-sons":    {"name": "Thousand Sons",     "trait": "Sorcerous Lore",     "color": "#C44E10"},
    "sons-of-horus":    {"name": "Sons of Horus",     "trait": "Death Dealers",      "color": "#2D937D"},
    "word-bearers":     {"name": "Word Bearers",      "trait": "Zealots",            "color": "#7A1F1F"},
    "salamanders":      {"name": "Salamanders",       "trait": "Promethean Fire",    "color": "#0E5C3A"},
    "raven-guard":      {"name": "Raven Guard",       "trait": "Shadow Masters",     "color": "#1A1A1A"},
    "alpha-legion":     {"name": "Alpha Legion",      "trait": "Hydra's Many Heads", "color": "#3F6E60"},
}


# --- /api/factions list ---
class TestFactionList:
    @pytest.fixture(scope="class")
    def factions(self):
        r = requests.get(f"{BASE_URL}/api/factions", timeout=15)
        assert r.status_code == 200, r.text
        return r.json()["factions"]

    def test_exactly_18(self, factions):
        assert len(factions) == 18, f"expected 18 factions, got {len(factions)}: {[f['id'] for f in factions]}"

    def test_all_expected_ids_present(self, factions):
        ids = [f["id"] for f in factions]
        for fid in EXPECTED_IDS:
            assert fid in ids, f"missing {fid}"

    def test_required_summary_fields(self, factions):
        for f in factions:
            for key in ("id", "name", "subtitle", "color", "legionTrait"):
                assert key in f, f"{f.get('id')} missing {key}"
            assert f["legionTrait"] and "name" in f["legionTrait"] and "description" in f["legionTrait"]

    def test_identity_overrides_in_list(self, factions):
        by_id = {f["id"]: f for f in factions}
        for fid, exp in EXPECTED_OVERRIDES.items():
            f = by_id[fid]
            assert f["name"] == exp["name"], f"{fid} name mismatch"
            assert f["color"].upper() == exp["color"].upper(), f"{fid} color mismatch ({f['color']})"
            assert f["legionTrait"]["name"] == exp["trait"], f"{fid} trait mismatch ({f['legionTrait']['name']})"


# --- /api/factions/{id} detail ---
class TestFactionDetail:
    @pytest.mark.parametrize("fid", EXPECTED_IDS)
    def test_detail_status_and_shape(self, fid):
        r = requests.get(f"{BASE_URL}/api/factions/{fid}", timeout=15)
        assert r.status_code == 200, f"{fid}: {r.status_code} {r.text[:200]}"
        d = r.json()
        assert d["id"] == fid
        assert "legionTrait" in d and d["legionTrait"]["name"]
        # Inherits roster from baseline
        formations = d.get("formations")
        assert isinstance(formations, list) and len(formations) >= 1, f"{fid} formations empty"
        upgrades = d.get("upgrades")
        assert (isinstance(upgrades, list) and len(upgrades) >= 1) or (isinstance(upgrades, dict) and len(upgrades) >= 1), f"{fid} upgrades empty"
        units = d.get("units")
        assert (isinstance(units, list) and len(units) >= 1) or (isinstance(units, dict) and len(units) >= 1), f"{fid} units empty"

    @pytest.mark.parametrize("fid", EXPECTED_IDS)
    def test_detail_identity_override(self, fid):
        r = requests.get(f"{BASE_URL}/api/factions/{fid}", timeout=15)
        d = r.json()
        exp = EXPECTED_OVERRIDES[fid]
        assert d["name"] == exp["name"]
        assert d["color"].upper() == exp["color"].upper()
        assert d["legionTrait"]["name"] == exp["trait"]

    def test_baseline_roster_size_consistent(self):
        """All legions should share the same formation/unit count as the baseline."""
        baseline = requests.get(f"{BASE_URL}/api/factions/sons-of-horus", timeout=15).json()
        n_form = len(baseline["formations"])
        n_units = len(baseline["units"]) if isinstance(baseline["units"], (list, dict)) else 0
        for fid in EXPECTED_IDS:
            d = requests.get(f"{BASE_URL}/api/factions/{fid}", timeout=15).json()
            assert len(d["formations"]) == n_form, f"{fid} has {len(d['formations'])} formations vs baseline {n_form}"
            cur_units = len(d["units"]) if isinstance(d["units"], (list, dict)) else 0
            assert cur_units == n_units, f"{fid} has {cur_units} units vs baseline {n_units}"

    def test_404_on_unknown_id(self):
        r = requests.get(f"{BASE_URL}/api/factions/not-a-real-legion", timeout=15)
        assert r.status_code == 404


# --- Specific override merge logic ---
class TestDarkAngelsCompositionAppend:
    def test_dreadwing_rule_appended(self):
        r = requests.get(f"{BASE_URL}/api/factions/dark-angels", timeout=15)
        assert r.status_code == 200
        d = r.json()
        rules = d.get("compositionRules") or []
        assert isinstance(rules, list) and rules, "dark-angels should have compositionRules"
        joined = " | ".join(rules)
        for keyword in ("Dreadwing", "Ravenwing", "Deathwing"):
            assert keyword in joined, f"missing {keyword} in compositionRules: {rules}"
        # And the baseline rules should still be present (not replaced).
        baseline_rules = requests.get(f"{BASE_URL}/api/factions/sons-of-horus", timeout=15).json().get("compositionRules") or []
        for br in baseline_rules:
            assert br in rules, f"baseline rule lost on dark-angels: {br}"


class TestSalamandersTrait:
    def test_promethean_fire(self):
        d = requests.get(f"{BASE_URL}/api/factions/salamanders", timeout=15).json()
        assert d["legionTrait"]["name"] == "Promethean Fire"
        assert "flamer" in d["legionTrait"]["description"].lower()
