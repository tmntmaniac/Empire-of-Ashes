"""Backend tests for Sons of Horus override isolation (Jan 2026).

After the legions.json refactor:
  - factions.json holds the generic baseline (id 'legiones-astartes', hidden).
  - legions.json owns per-legion overrides.
  - Sons of Horus carries its own extra units (Reaver/Luperci/Justaerian, Primarch
    Horus) and the Despoiler weapon option, which MUST NOT bleed into other legions.

These tests guard against regression of that contamination bug.
"""
import os
import pytest
import requests

BASE_URL = os.environ.get(
    'REACT_APP_BACKEND_URL',
    'https://armageddon-squad.preview.emergentagent.com',
).rstrip('/')

SOH_ONLY_FORMATIONS = {"reaver-detachment", "luperci-pack", "justaerian-detachment", "horus"}
SOH_ONLY_UNITS = {"despoiler", "reaver", "luperci", "justaerian", "horus"}
NON_SOH_LEGIONS = [
    "dark-angels", "emperors-children", "iron-warriors", "white-scars",
    "space-wolves", "imperial-fists", "night-lords", "blood-angels",
    "iron-hands", "world-eaters", "ultramarines", "death-guard",
    "thousand-sons", "word-bearers", "salamanders", "raven-guard", "alpha-legion",
]


# --- Baseline must be hidden from the public list ---
class TestBaselineHidden:
    def test_list_is_exactly_18_and_no_baseline(self):
        r = requests.get(f"{BASE_URL}/api/factions", timeout=15)
        assert r.status_code == 200, r.text
        data = r.json()["factions"]
        ids = [f["id"] for f in data]
        assert len(ids) == 18, f"expected 18, got {len(ids)}: {ids}"
        assert "legiones-astartes" not in ids, "hidden baseline must not appear in /api/factions"

    def test_baseline_detail_returns_404_or_hidden(self):
        # Baseline can still be fetched directly (it exists), but it must not
        # be the public list entry. Spec says baseline is hidden from list.
        # We don't require 404 on the detail endpoint; just enforce list hiding.
        r = requests.get(f"{BASE_URL}/api/factions", timeout=15).json()
        ids = {f["id"] for f in r["factions"]}
        assert "legiones-astartes" not in ids


# --- Sons of Horus owns its overrides ---
class TestSonsOfHorusOverrides:
    @pytest.fixture(scope="class")
    def soh(self):
        r = requests.get(f"{BASE_URL}/api/factions/sons-of-horus", timeout=15)
        assert r.status_code == 200, r.text
        return r.json()

    def test_soh_has_all_extra_formations(self, soh):
        f_ids = {f["id"] for f in soh["formations"]}
        for fid in SOH_ONLY_FORMATIONS:
            assert fid in f_ids, f"sons-of-horus missing formation {fid}; got {sorted(f_ids)}"

    def test_soh_has_all_extra_units(self, soh):
        assert isinstance(soh["units"], dict), "units expected as a dict for override merging"
        unit_ids = set(soh["units"].keys())
        for uid in SOH_ONLY_UNITS:
            assert uid in unit_ids, f"sons-of-horus missing unit {uid}"

    def test_soh_tactical_detachment_has_despoiler_option(self, soh):
        td = next((f for f in soh["formations"] if f["id"] == "tactical-detachment"), None)
        assert td is not None, "sons-of-horus missing tactical-detachment formation"
        opts = td.get("unitOptions") or []
        text_blob = " | ".join(
            (opt.get("name") or opt.get("label") or "") + " " + (opt.get("description") or "")
            for opt in opts if isinstance(opt, dict)
        )
        assert "Despoiler" in text_blob, f"Despoiler option missing from SoH tactical-detachment: {opts}"

    def test_soh_composition_rules_include_overrides(self, soh):
        rules = soh.get("compositionRules") or []
        joined = " | ".join(rules)
        assert "Primarch Horus" in joined and "Supreme Commander" in joined, \
            f"Primarch Horus rule missing: {rules}"
        # Reaver / Luperci / Justaerian 1-per-2000 rule
        assert "Reaver" in joined and "Luperci" in joined and "Justaerian" in joined, \
            f"Reaver/Luperci/Justaerian rule missing: {rules}"
        assert "2,000" in joined or "2000" in joined, f"1-per-2000 rule missing: {rules}"

    def test_soh_trait_is_death_dealers(self, soh):
        assert soh["legionTrait"]["name"] == "Death Dealers"


# --- No bleed into other legions ---
class TestNoBleedIntoOtherLegions:
    @pytest.mark.parametrize("fid", NON_SOH_LEGIONS)
    def test_no_soh_formations(self, fid):
        d = requests.get(f"{BASE_URL}/api/factions/{fid}", timeout=15).json()
        f_ids = {f["id"] for f in d["formations"]}
        leaked = SOH_ONLY_FORMATIONS & f_ids
        assert not leaked, f"{fid} leaked SoH formations: {leaked}"

    @pytest.mark.parametrize("fid", NON_SOH_LEGIONS)
    def test_no_soh_units(self, fid):
        d = requests.get(f"{BASE_URL}/api/factions/{fid}", timeout=15).json()
        units = d.get("units") or {}
        unit_ids = set(units.keys()) if isinstance(units, dict) else {u.get("id") for u in units}
        leaked = SOH_ONLY_UNITS & unit_ids
        assert not leaked, f"{fid} leaked SoH units: {leaked}"

    @pytest.mark.parametrize("fid", NON_SOH_LEGIONS)
    def test_no_despoiler_option_on_tactical_detachment(self, fid):
        d = requests.get(f"{BASE_URL}/api/factions/{fid}", timeout=15).json()
        td = next((f for f in d["formations"] if f["id"] == "tactical-detachment"), None)
        assert td is not None, f"{fid} missing tactical-detachment"
        opts = td.get("unitOptions") or []
        for opt in opts:
            if not isinstance(opt, dict):
                continue
            blob = (opt.get("name") or opt.get("label") or "") + " " + (opt.get("description") or "")
            assert "Despoiler" not in blob, f"{fid} tactical-detachment leaked Despoiler option: {opt}"

    @pytest.mark.parametrize("fid", NON_SOH_LEGIONS)
    def test_has_own_legion_trait(self, fid):
        d = requests.get(f"{BASE_URL}/api/factions/{fid}", timeout=15).json()
        trait = d.get("legionTrait") or {}
        assert trait.get("name"), f"{fid} missing legionTrait.name"
        # baseline placeholder name was 'Legiones Astartes' — must NOT leak.
        assert trait["name"] != "Legiones Astartes", f"{fid} still has baseline placeholder trait"
        assert trait["name"] != "Death Dealers", f"{fid} inherited Death Dealers trait from SoH baseline"
