"""Backend smoke tests for Empire of Ashes API."""
import os
import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://armageddon-squad.preview.emergentagent.com').rstrip('/')


@pytest.fixture(scope="module")
def api_client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# --- Root health ---
class TestRoot:
    def test_root(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/")
        assert r.status_code == 200, r.text
        data = r.json()
        assert "message" in data
        assert "factions" in data
        assert "sons-of-horus" in data["factions"]


# --- Faction list ---
class TestFactionList:
    def test_list_factions_status(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/factions")
        assert r.status_code == 200, r.text

    def test_list_factions_contains_sons_of_horus(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/factions")
        data = r.json()
        assert "factions" in data
        ids = [f["id"] for f in data["factions"]]
        assert "sons-of-horus" in ids
        soh = next(f for f in data["factions"] if f["id"] == "sons-of-horus")
        assert soh["name"] == "Sons of Horus"
        assert soh.get("available") is True


# --- Faction detail ---
class TestFactionDetail:
    def test_get_sons_of_horus(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/factions/sons-of-horus")
        assert r.status_code == 200, r.text
        data = r.json()
        # Required keys
        for key in ["id", "name", "formations", "upgrades", "units", "legionTrait"]:
            assert key in data, f"missing key {key}"
        assert data["id"] == "sons-of-horus"
        assert isinstance(data["formations"], list) and len(data["formations"]) >= 1
        # upgrades and units may be list or dict depending on schema
        upgrades = data["upgrades"]
        assert (isinstance(upgrades, list) and len(upgrades) >= 1) or (isinstance(upgrades, dict) and len(upgrades) >= 1)
        units = data["units"]
        assert (isinstance(units, list) and len(units) >= 1) or (isinstance(units, dict) and len(units) >= 1)
        assert data["legionTrait"].get("name") == "Death Dealers"

    def test_get_faction_not_found(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/factions/does-not-exist")
        assert r.status_code == 404

    def test_formation_ids_include_expected(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/factions/sons-of-horus")
        data = r.json()
        f_ids = [f["id"] for f in data["formations"]]
        # Expected formation IDs from prompt
        for expected in ["tactical-detachment", "horus"]:
            assert expected in f_ids, f"missing formation {expected} in {f_ids}"
