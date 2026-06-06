"""Backend assertions for the Sons of Horus expansion (Jan 2026)."""
import os
import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://armageddon-squad.preview.emergentagent.com').rstrip('/')

EXPECTED_LOW_IDS = [
    "plutona-assault-drill",
    "heavy-tank-battery",
    "superheavy-squadron",
    "superheavy-tank-destroyer",
    "gunship-flight",
    "interceptor-flight",
    "stormbird-lander",
]

EXPECTED_NEW_SUPPORT_IDS = [
    "destroyer-squad", "inductii-squad", "recon-squad", "scout-detachment",
    "veteran-squad", "outrider-squad", "jetbike-squad", "land-speeder-squadron",
    "javelin-squadron", "castraferrum-talon", "contemptor-talon", "leviathan-talon",
    "air-defence-battery", "artillery-battery-arquitor", "artillery-battery-basilisk",
    "artillery-battery-medusa", "artillery-battery-whirlwind", "kratos-heavy-squadron",
    "land-raider-squadron", "predator-squadron", "sabre-squadron", "sicaran-squadron",
    "vindicator-squadron", "storm-eagle-flight", "thunderhawk-gunship",
    "thunderhawk-transporter-flight", "legion-spacecraft-strike-cruiser",
    "legion-spacecraft-battleship", "assault-squad-support", "breacher-squad-support",
    "rapier-battery",
]


@pytest.fixture(scope="module")
def faction():
    r = requests.get(f"{BASE_URL}/api/factions/sons-of-horus", timeout=15)
    assert r.status_code == 200, r.text
    return r.json()


class TestCounts:
    def test_formation_count_46(self, faction):
        assert len(faction["formations"]) == 46, f"got {len(faction['formations'])} formations"

    def test_unit_count_71(self, faction):
        units = faction["units"]
        if isinstance(units, dict):
            assert len(units) == 71, f"got {len(units)} units"
        else:
            assert len(units) == 71

    def test_category_breakdown(self, faction):
        from collections import Counter
        cats = Counter(f.get("category") for f in faction["formations"])
        # Expected: 5 Line, 33 Support, 7 Lords of War, 1 Primarch
        assert cats.get("Line") == 5, f"Line={cats.get('Line')} all={dict(cats)}"
        assert cats.get("Support") == 33, f"Support={cats.get('Support')} all={dict(cats)}"
        assert cats.get("Lords of War") == 7, f"LoW={cats.get('Lords of War')} all={dict(cats)}"
        assert cats.get("Primarch") == 1, f"Primarch={cats.get('Primarch')} all={dict(cats)}"


class TestReaverReclass:
    def test_reaver_is_line(self, faction):
        f = next((x for x in faction["formations"] if x["id"] == "reaver-detachment"), None)
        assert f is not None, "reaver-detachment formation missing"
        assert f["category"] == "Line", f"reaver-detachment category={f['category']}"


class TestLordsOfWar:
    @pytest.mark.parametrize("low_id", EXPECTED_LOW_IDS)
    def test_low_present(self, faction, low_id):
        f = next((x for x in faction["formations"] if x["id"] == low_id), None)
        assert f is not None, f"missing LoW formation {low_id}"
        assert f["category"] == "Lords of War", f"{low_id} category={f['category']}"


class TestNewSupport:
    @pytest.mark.parametrize("sid", EXPECTED_NEW_SUPPORT_IDS)
    def test_support_present(self, faction, sid):
        f = next((x for x in faction["formations"] if x["id"] == sid), None)
        assert f is not None, f"missing Support formation {sid}"


class TestUnitRefs:
    def test_no_broken_unit_refs(self, faction):
        units = faction["units"]
        unit_keys = set(units.keys()) if isinstance(units, dict) else {u["id"] for u in units}
        missing = []
        for f in faction["formations"]:
            for opt in f.get("unitOptions", []) or []:
                for u in opt.get("units", []) or []:
                    uid = u.get("unit")
                    if uid and uid not in unit_keys:
                        missing.append((f["id"], "units", uid))
                eu = opt.get("extraUnit")
                if eu and isinstance(eu, dict):
                    uid = eu.get("unit")
                    if uid and uid not in unit_keys:
                        missing.append((f["id"], "extraUnit", uid))
        assert not missing, f"Broken unit refs: {missing}"


class TestKeyLoWUnitsExist:
    def test_plutona_and_stormbird_units(self, faction):
        units = faction["units"]
        unit_keys = set(units.keys()) if isinstance(units, dict) else {u["id"] for u in units}
        # The LoW formations should reference some real units
        for low_id in EXPECTED_LOW_IDS:
            f = next(x for x in faction["formations"] if x["id"] == low_id)
            refs = []
            for opt in f.get("unitOptions", []) or []:
                for u in opt.get("units", []) or []:
                    refs.append(u.get("unit"))
            assert refs, f"LoW {low_id} has no unit refs"
            for r in refs:
                assert r in unit_keys, f"LoW {low_id} -> missing unit {r}"
