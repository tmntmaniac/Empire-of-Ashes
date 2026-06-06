"""
Regression tests for Solar Auxilia and Imperialis Militia factions.

These armies use the standalone-faction pattern in factions.json
(no merge with the Legiones Astartes baseline). The backend includes
them automatically via the `baseline factions not overridden by legions`
loop in server.build_factions().
"""
import os
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL_FOR_TESTS", "http://localhost:8001")
TIMEOUT = 15

EXPECTED_LIMITS = {
    "maxSupportPerLine": 2,
    "maxUpgradesPerLine": 3,
    "lowPct": 0.33,
}


def _get(path):
    r = requests.get(f"{BASE_URL}{path}", timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def test_factions_list_includes_new_armies():
    data = _get("/api/factions")
    ids = {f["id"] for f in data["factions"]}
    assert "solar-auxilia" in ids, ids
    assert "imperialis-militia" in ids, ids


def _assert_referential_integrity(faction):
    """Every unit referenced by a formation must exist in faction['units']."""
    units = faction["units"]
    for form in faction["formations"]:
        for opt in form.get("unitOptions", []):
            for u in opt["units"]:
                assert u["unit"] in units, (
                    f"{faction['id']}: formation {form['id']} references "
                    f"missing unit '{u['unit']}'"
                )
        extra = form.get("extraUnit")
        if extra:
            assert extra["unit"] in units, (
                f"{faction['id']}: formation {form['id']} extraUnit references "
                f"missing unit '{extra['unit']}'"
            )

    upgrade_ids = {u["id"] for u in faction["upgrades"]}
    for form in faction["formations"]:
        for upg in form.get("allowedUpgrades", []):
            assert upg in upgrade_ids, (
                f"{faction['id']}: formation {form['id']} allows unknown "
                f"upgrade '{upg}'"
            )


def _assert_has_category(faction, category):
    cats = {f["category"] for f in faction["formations"]}
    assert category in cats, (
        f"{faction['id']} missing category {category} (have: {cats})"
    )


def test_solar_auxilia_full_payload():
    f = _get("/api/factions/solar-auxilia")
    assert f["name"] == "Solar Auxilia"
    assert f["compositionLimits"] == EXPECTED_LIMITS
    assert len(f["formations"]) >= 17
    assert len(f["units"]) >= 30
    assert len(f["upgrades"]) >= 5
    for cat in ("Line", "Support", "Lords of War"):
        _assert_has_category(f, cat)
    # Sanity: Lord Marshall character and a Leman Russ chassis exist.
    assert "lord-marshall" in f["units"]
    assert "sa-leman-russ-battle" in f["units"]
    _assert_referential_integrity(f)


def test_imperialis_militia_full_payload():
    f = _get("/api/factions/imperialis-militia")
    assert f["name"] == "Imperialis Militia"
    assert f["compositionLimits"] == EXPECTED_LIMITS
    assert len(f["formations"]) >= 19
    assert len(f["units"]) >= 30
    assert len(f["upgrades"]) >= 5
    for cat in ("Line", "Support", "Lords of War"):
        _assert_has_category(f, cat)
    # Sanity: provenance-driven characters and core line units exist.
    assert "discipline-master" in f["units"]
    assert "conscript-squad" in f["units"]
    assert "force-command" in f["units"]
    _assert_referential_integrity(f)


def test_astartes_legions_still_have_default_limits():
    """Adding the new armies must not break the existing Legion data."""
    f = _get("/api/factions/sons-of-horus")
    # Legions don't carry compositionLimits — frontend falls back to defaults.
    assert "compositionLimits" not in f or f.get("compositionLimits") is None
    # They must still report the canonical Astartes composition rules.
    rules = " ".join(f.get("compositionRules", []))
    assert "Max 3 Support" in rules
    assert "Max 4 Upgrades" in rules
