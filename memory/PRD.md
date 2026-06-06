# Empire of Ashes — Force Builder

## Original problem statement
Build a force-builder web app (legionbuilder.app-style) for the fan "Empire of Ashes" Epic Armageddon system. LocalStorage-only MVP (no accounts, no DB for saved lists), grimdark / Warhammer 30K visual aesthetic, must support all 18 Legiones Astartes; Mechanicum, Solar Auxilia and Knight Households come after.

## Personas
- Heresy-era hobbyist composing army lists offline at home, club night, or tournament.
- No account; lists live in the player's browser only.

## Core requirements
- All 18 Legiones Astartes selectable with unique trait card.
- Standard force-builder: add formations, add upgrades, live point total, save/load multiple armies.
- LocalStorage persistence (key `eoa.armies.v1`).
- Grimdark UI: dark panels, mono accents, asymmetric layout, no AI-slop gradients.

## Architecture
- Frontend: React + React Router + Tailwind + Shadcn UI. State via `localStorage` (`/app/frontend/src/lib/storage.js`).
- Backend: FastAPI serving static JSON rules. **No DB used by MVP** (Mongo client kept for future).
- Data:
  - `/app/backend/data/factions.json` — baseline rules (Sons of Horus master template with all formations, upgrades, units, transports).
  - `/app/backend/data/legions.json` — 18 legion overrides (identity, lore, legionTrait, optional `compositionRulesAppend` / `compositionRules` / `allies` / `extraUnits` / `unitOverrides`).
  - `/app/backend/server.py::build_factions()` merges baseline + overrides at request time. `baseFactionId` in `legions.json` selects the template.

## API
- `GET /api/factions` — list of all 18 faction cards (id, name, subtitle, color, legionTrait).
- `GET /api/factions/{id}` — full faction document (formations[], upgrades[], units[], compositionRules[], allies, lore).
- `GET /api/factions/unknown` — 404.

## Changelog
- 2026-02 — Added `legions.json` with all 18 Legiones Astartes (Dark Angels, Emperor's Children, Iron Warriors, White Scars, Space Wolves, Imperial Fists, Night Lords, Blood Angels, Iron Hands, World Eaters, Ultramarines, Death Guard, Thousand Sons, Sons of Horus, Word Bearers, Salamanders, Raven Guard, Alpha Legion). Refactored `server.py` to merge baseline rules with per-legion identity/trait overrides. Removed stale "More Legions / Classified" placeholder on Landing (now teases auxiliary forces). 94/94 backend tests + 15/15 frontend scenarios pass.

## Backlog
- P1 — Auxiliary armies: Mechanicum Taghmata, Solar Auxilia, Knight Households.
- P1 — Deep-link `Build →` cards on Landing to pre-select the legion in the New Army dialog (`/armies?new=<id>`).
- P2 — URL-based army sharing (base64-encoded stateless share string).
- P2 — Per-legion accent color applied to the "Active" badge on Landing.
- P2 — Cache `build_factions()` with mtime check (currently re-reads + deep-copies per request; fine for MVP scale).
- P3 — Export army list to PDF.
- P3 — Rotate hero LORE on Landing (currently hardcoded Sons of Horus quote).
- P3 — `/api/health` readiness endpoint.

## Test credentials
n/a — localStorage only, no auth.
