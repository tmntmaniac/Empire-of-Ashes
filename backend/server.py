from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import json
import logging
from pathlib import Path


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection (kept for future use)
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Load static faction data
DATA_PATH = ROOT_DIR / 'data' / 'factions.json'
with open(DATA_PATH, 'r', encoding='utf-8') as fh:
    FACTION_DATA = json.load(fh)

app = FastAPI(title="Empire of Ashes Force Builder API")
api_router = APIRouter(prefix="/api")


@api_router.get("/")
async def root():
    return {"message": "Empire of Ashes API online", "factions": [f["id"] for f in FACTION_DATA["factions"]]}


@api_router.get("/factions")
async def list_factions():
    """Return summary of all factions."""
    return {
        "factions": [
            {
                "id": f["id"],
                "name": f["name"],
                "subtitle": f.get("subtitle", ""),
                "color": f.get("color", "#2D937D"),
                "available": True,
            }
            for f in FACTION_DATA["factions"]
        ]
    }


@api_router.get("/factions/{faction_id}")
async def get_faction(faction_id: str):
    """Return full faction data including formations, upgrades and units."""
    for f in FACTION_DATA["factions"]:
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
