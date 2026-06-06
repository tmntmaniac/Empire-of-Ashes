"""Regression: maxPer caps for Knight Households + Legio Titanicus formations.

These caps were added to back the validation.js R6 rule (1 per N points).
"""
import os
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL_FOR_TESTS", "http://localhost:8001")
TIMEOUT = 15

EXPECTED = {
    "knight-household": {
        "cerastus-lance": 2000,
        "grand-quesetorius-lance": 2000,
    },
    "legio-titanicus": {
        "warhound-scout": 2000,
        "direwolf-heavy-scout": 2000,
        "warbringer-titan": 2000,
        "emperor-titan": 7500,
    },
}


def _get(path):
    r = requests.get(f"{BASE_URL}{path}", timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def test_max_per_points_caps_exist():
    for fid, caps in EXPECTED.items():
        fac = _get(f"/api/factions/{fid}")
        form_map = {f["id"]: f for f in fac["formations"]}
        for form_id, points in caps.items():
            assert form_id in form_map, f"{fid}: missing formation {form_id}"
            mp = form_map[form_id].get("maxPer")
            assert mp == {"points": points}, (
                f"{fid}/{form_id}: expected maxPer={{points:{points}}}, got {mp}"
            )


def test_formations_without_cap_have_no_maxper():
    """Sanity: Astartes Tactical Detachment should not get a stray maxPer."""
    fac = _get("/api/factions/sons-of-horus")
    for f in fac["formations"]:
        assert "maxPer" not in f, f"sons-of-horus/{f['id']} unexpectedly has maxPer={f.get('maxPer')}"
