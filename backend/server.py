from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import copy
import json
import logging
import os
from pathlib import Path


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection (kept for future use; MVP relies on localStorage)
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Static data sources — read fresh per request so on-disk edits hot-reload
# without a manual `supervisorctl restart backend`.
DATA_PATH = ROOT_DIR / 'data' / 'factions.json'
LEGIONS_PATH = ROOT_DIR / 'data' / 'legions.json'


def _read_json(path: Path):
    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)


def load_baseline_factions():
    """Factions defined fully in factions.json (master template, e.g. Sons of Horus)."""
    return _read_json(DATA_PATH)['factions']


def load_legion_overrides():
    """Compact per-legion overrides that inherit from a baseline faction."""
    return _read_json(LEGIONS_PATH)


def build_factions():
    """
    Merge baseline factions (full rules) with legion overrides (identity + trait
    overrides) to produce one canonical list of playable Legiones Astartes.

    The merge is shallow on top-level keys, BUT a legion override always wins
    on identity (id/name/subtitle/color/lore) and legionTrait, while inheriting
    formations / unitOptions / allowedUpgrades / allies / compositionRules
    from the baseline so we don't duplicate kilobytes of static rules.
    """
    baseline_list = load_baseline_factions()
    baseline_by_id = {f['id']: f for f in baseline_list}

    legions_doc = load_legion_overrides()
    base_id = legions_doc.get('baseFactionId')
    if base_id not in baseline_by_id:
        # If misconfigured, fall back to the first baseline entry.
        base_id = baseline_list[0]['id']
    base_template = baseline_by_id[base_id]

    merged = []
    for override in legions_doc.get('legions', []):
        # Deep-copy baseline so each legion is an independent object.
        faction = copy.deepcopy(base_template)

        # Identity always comes from the override.
        for key in ('id', 'name', 'subtitle', 'color', 'lore', 'legionTrait'):
            if key in override:
                faction[key] = override[key]

        # Optional structural overrides.
        if 'compositionRules' in override:
            faction['compositionRules'] = override['compositionRules']
        if 'compositionRulesAppend' in override:
            faction['compositionRules'] = list(faction.get('compositionRules', [])) + list(override['compositionRulesAppend'])
        if 'allies' in override:
            faction['allies'] = override['allies']

        # Optional per-legion unit roster tweaks.
        if 'extraUnits' in override and isinstance(faction.get('units'), list):
            faction['units'] = faction['units'] + override['extraUnits']
        if 'unitOverrides' in override and isinstance(faction.get('units'), list):
            patches = {u['id']: u for u in override['unitOverrides'] if 'id' in u}
            faction['units'] = [
                {**u, **patches[u['id']]} if u.get('id') in patches else u
                for u in faction['units']
            ]

        merged.append(faction)

    # Include any baseline factions that aren't overridden by legions.json
    # (e.g. future Mechanicum / Solar Auxilia entries added directly there).
    overridden_ids = {f['id'] for f in merged}
    for f in baseline_list:
        if f['id'] not in overridden_ids:
            merged.append(f)

    return merged


app = FastAPI(title="Empire of Ashes Force Builder API")
api_router = APIRouter(prefix="/api")


@api_router.get("/")
async def root():
    factions = build_factions()
    return {
        "message": "Empire of Ashes API online",
        "factions": [f["id"] for f in factions],
    }


@api_router.get("/factions")
async def list_factions():
    """Return summary cards for every playable faction."""
    factions = build_factions()
    return {
        "factions": [
            {
                "id": f["id"],
                "name": f["name"],
                "subtitle": f.get("subtitle", ""),
                "color": f.get("color", "#2D937D"),
                "legionTrait": f.get("legionTrait"),
                "available": True,
            }
            for f in factions
        ]
    }


@api_router.get("/factions/{faction_id}")
async def get_faction(faction_id: str):
    """Return full faction data (formations, upgrades, units) for one faction."""
    for f in build_factions():
        if f["id"] == faction_id:
            return f
    raise HTTPException(status_code=404, detail=f"Faction '{faction_id}' not found")


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
