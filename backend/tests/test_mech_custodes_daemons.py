"""Regression tests for Mechanicum Taghmata, Legio Custodes, and Daemons of the Ruinstorm."""
import os
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL_FOR_TESTS", "http://localhost:8001")
TIMEOUT = 15


def _get(path):
    r = requests.get(f"{BASE_URL}{path}", timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def _check_unit_refs(faction):
    units = faction["units"]
    upgrade_ids = {u["id"] for u in faction["upgrades"]}
    for form in faction["formations"]:
        for opt in form.get("unitOptions", []):
            for u in opt["units"]:
                assert u["unit"] in units, f"{form['id']} -> missing unit {u['unit']}"
        extra = form.get("extraUnit")
        if extra:
            assert extra["unit"] in units, f"{form['id']} extraUnit missing {extra['unit']}"
        for up_id in form.get("allowedUpgrades", []):
            assert up_id in upgrade_ids, f"{form['id']} -> missing upgrade {up_id}"
    # Upgrade addedUnits must resolve
    for up in faction["upgrades"]:
        for au in up.get("addedUnits", []) or []:
            assert au["unit"] in units, f"upgrade {up['id']} addedUnits -> missing {au['unit']}"


def test_factions_list_includes_all_three():
    factions = _get("/api/factions")["factions"]
    ids = {f["id"] for f in factions}
    for fid in ("mechanicum-taghmata", "legio-custodes", "daemons-ruinstorm"):
        assert fid in ids, f"{fid} missing from /api/factions"


def test_mechanicum_payload():
    f = _get("/api/factions/mechanicum-taghmata")
    assert f["id"] == "mechanicum-taghmata"
    assert f["name"] == "Mechanicum Taghmata"
    # Mechanicum uses Astartes defaults (no compositionLimits override).
    assert "compositionLimits" not in f or f.get("compositionLimits") is None
    cats = {fm["category"] for fm in f["formations"]}
    assert {"Line", "Support", "Lords of War"}.issubset(cats)
    assert len(f["formations"]) >= 20
    assert len(f["units"]) >= 25
    # 1-per-force caps for Ordinatus Majora + Ark Mechanicus
    caps = {fm["id"]: fm.get("maxPerArmy") for fm in f["formations"] if fm.get("maxPerArmy")}
    assert caps.get("ordinatus-majoris") == 1
    assert caps.get("ark-mechanicus") == 1
    _check_unit_refs(f)


def test_custodes_payload():
    f = _get("/api/factions/legio-custodes")
    assert f["id"] == "legio-custodes"
    # Custodes-specific composition: 50% LoW cap (vs default 33%)
    assert f["compositionLimits"]["lowPct"] == 0.5
    assert f["compositionLimits"]["maxSupportPerLine"] == 3
    cats = {fm["category"] for fm in f["formations"]}
    assert {"Line", "Support", "Lords of War"}.issubset(cats)
    assert len(f["formations"]) >= 14
    assert len(f["units"]) >= 20
    _check_unit_refs(f)


def test_daemons_payload():
    f = _get("/api/factions/daemons-ruinstorm")
    assert f["id"] == "daemons-ruinstorm"
    # Daemons: only 1 Support per Line (R2 tighter), upgrades effectively unlimited.
    assert f["compositionLimits"]["maxSupportPerLine"] == 1
    cats = {fm["category"] for fm in f["formations"]}
    assert {"Line", "Support", "Lords of War"}.issubset(cats)
    # Four chaos gods × line detachments
    line_ids = {fm["id"] for fm in f["formations"] if fm["category"] == "Line"}
    assert {"change-coven", "depraved-host", "murder-tide", "putrid-legion"}.issubset(line_ids)
    assert len(f["formations"]) >= 22
    assert len(f["units"]) >= 30
    _check_unit_refs(f)


def test_total_active_factions_is_25():
    factions = _get("/api/factions")["factions"]
    # 18 Astartes + Solar Auxilia + Imperialis Militia + Knight Households +
    # Legio Titanicus + Mechanicum + Custodes + Daemons = 25
    assert len(factions) == 25, f"expected 25, got {len(factions)}: {[f['id'] for f in factions]}"
