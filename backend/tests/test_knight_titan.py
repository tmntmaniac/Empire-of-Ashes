"""Regression tests for Knight Households and Legio Titanicus factions."""
import os
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL_FOR_TESTS", "http://localhost:8001")
TIMEOUT = 15

EXPECTED_LIMITS = {"maxSupportPerLine": 2, "maxUpgradesPerLine": 3, "lowPct": 0.33}


def _get(path):
    r = requests.get(f"{BASE_URL}{path}", timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def _check_integrity(faction):
    units = faction["units"]
    upgrade_ids = {u["id"] for u in faction["upgrades"]}
    for form in faction["formations"]:
        for opt in form.get("unitOptions", []):
            for u in opt["units"]:
                assert u["unit"] in units, f"{form['id']} -> missing {u['unit']}"
        extra = form.get("extraUnit")
        if extra:
            assert extra["unit"] in units, f"{form['id']} extraUnit -> {extra['unit']}"
        for upg in form.get("allowedUpgrades", []):
            assert upg in upgrade_ids, f"{form['id']} -> unknown upgrade {upg}"
    for up in faction["upgrades"]:
        for au in up.get("addedUnits", []):
            assert au["unit"] in units, f"{up['id']} addedUnits -> {au['unit']}"


def test_factions_list_includes_knight_and_titan():
    data = _get("/api/factions")
    ids = {f["id"] for f in data["factions"]}
    assert "knight-household" in ids
    assert "legio-titanicus" in ids
    # 18 Legions + 4 standalones = 22
    assert len(data["factions"]) >= 22


def test_knight_household_payload():
    f = _get("/api/factions/knight-household")
    assert f["name"] == "Knight Households"
    assert f["compositionLimits"] == EXPECTED_LIMITS
    assert len(f["formations"]) >= 7
    assert "porphyrion" in f["units"]
    assert "castellan" in f["units"]
    assert "lancer" in f["units"]
    cats = {form["category"] for form in f["formations"]}
    assert {"Line", "Support", "Lords of War"} <= cats
    _check_integrity(f)


def test_legio_titanicus_payload():
    f = _get("/api/factions/legio-titanicus")
    assert f["name"] == "Legio Titanicus"
    assert f["compositionLimits"] == EXPECTED_LIMITS
    assert len(f["formations"]) >= 9
    # Critical titans must be present
    for u in ("warhound-scout-titan", "reaver-battle-titan",
              "warlord-battle-titan", "warbringer-nemesis-titan",
              "direwolf-heavy-scout-titan", "warmaster-heavy-battle-titan",
              "warlord-sinister", "emperor-titan"):
        assert u in f["units"], f"missing titan unit {u}"
    # Weapon-slot upgrades exist and are marked conversion
    weapon_ups = [u for u in f["upgrades"] if u["id"].startswith("titan-weapons-")]
    assert len(weapon_ups) >= 6
    for w in weapon_ups:
        assert w.get("conversion") is True
        assert w["type"] == "multi"
        assert isinstance(w["max"], int)
    cats = {form["category"] for form in f["formations"]}
    assert {"Line", "Support", "Lords of War"} <= cats
    _check_integrity(f)
