"""
Build a static JSON snapshot of every faction (summary + full) and write it
into the frontend source tree so production builds (e.g. Vercel) can render
the full force-builder *without* a running FastAPI backend.

Run from repo root:
    python backend/scripts/build_frontend_snapshot.py

Output:
    frontend/src/data/factions-snapshot.json
"""
import json
import os
import sys
from pathlib import Path

# Make `backend/` importable regardless of CWD.
HERE = Path(__file__).resolve()
BACKEND_DIR = HERE.parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from server import build_factions  # noqa: E402

OUTPUT = BACKEND_DIR.parent / "frontend" / "src" / "data" / "factions-snapshot.json"


def main() -> None:
    factions = build_factions()

    summary = {
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

    full = {f["id"]: f for f in factions}

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as fh:
        json.dump({"summary": summary, "full": full}, fh, ensure_ascii=False, separators=(",", ":"))

    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"[snapshot] wrote {len(factions)} factions ({size_kb:.1f} KB) -> {OUTPUT}")


if __name__ == "__main__":
    main()
