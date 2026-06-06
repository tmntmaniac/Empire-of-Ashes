"""Inject `maxPer: {points: N}` caps onto Knight Households and Legio Titanicus
formations per the source rules:
  - Knight Households: cerastus-lance, grand-quesetorius-lance — 1 per 2,000 pts
  - Legio Titanicus: warhound-scout, direwolf-heavy-scout, warbringer-titan — 1 per 2,000 pts
  - Legio Titanicus: emperor-titan — 1 per 7,500 pts
Safe, idempotent: re-running just overwrites the same fields.
"""
import json
from pathlib import Path

PATH = Path("/app/backend/data/factions.json")
data = json.loads(PATH.read_text())

CAPS = {
    "knight-household": {
        "cerastus-lance": {"points": 2000},
        "grand-quesetorius-lance": {"points": 2000},
    },
    "legio-titanicus": {
        "warhound-scout": {"points": 2000},
        "direwolf-heavy-scout": {"points": 2000},
        "warbringer-titan": {"points": 2000},
        "emperor-titan": {"points": 7500},
    },
}

changed = 0
for fac in data["factions"]:
    caps = CAPS.get(fac["id"])
    if not caps:
        continue
    for fm in fac["formations"]:
        if fm["id"] in caps:
            fm["maxPer"] = caps[fm["id"]]
            changed += 1
            print(f"  set maxPer={caps[fm['id']]} on {fac['id']}/{fm['id']}")

PATH.write_text(json.dumps(data, indent=2))
print(f"Done. {changed} formations updated.")
