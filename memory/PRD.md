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
- 2026-02 — Added `legions.json` with all 18 Legiones Astartes. Refactored `server.py` to merge baseline rules with per-legion identity/trait overrides.
- 2026-02 — Populated the remaining 8 skeleton legions with full lore, legion trait, allies, extra formations (incl. Primarch detachment), per-formation `unitOptions` and Primarch + named-unit stat blocks.
- 2026-02 — Added **Solar Auxilia** (17 formations, 40 units) and **Imperialis Militia** (20 formations, 39 units) as standalone factions in `factions.json`. Refactored `validation.js` and `Builder.jsx` to be data-driven via `limitsFor(faction)`. Hardened `FormationEditor.jsx` against missing `faction.upgrades` / `selections`.
- 2026-02 — Patched flag upgrades that ADD units (`addedUnits: [{unit,count}]`) so Ogryn Brute Squad, Rapier Battery, Fire Support, Snipers, Ogryn Charonite all surface in the roster stat table. Converted `sa-support` to a multi upgrade with `bundleCost: 75`.
- 2026-02 — Added **Knight Households** (7 formations, 15 units, 6 upgrades) and **Legio Titanicus** (9 formations, 12 units, 10 upgrades incl. 6 weapon-slot upgrades) as standalone factions. Introduced `conversion: true` flag on upgrades (Titan weapon-slot picks) so they pay variant cost without injecting fake units into the roster. 22 active factions total. 7/7 new-army backend tests + e2e smoke confirmed (KH Quesetorius Lance @ 425 pts, LT Warlord @ 850 pts, Warhound Pack @ 550 pts with 4 weapon slots).

## Backlog
- P1 — **Mechanicum Taghmata** (next and final auxiliary army on the roadmap).
- P2 — URL-based army sharing (stateless base64 share string).
- P2 — Cache `build_factions()` with mtime check (currently re-reads + deep-copies per request).
- P2 — Refresh stale tests in `test_legions.py` / `test_soh_isolation.py` (27 stale assertions still expect 18 factions and the old Alpha Legion trait name).
- P3 — Export army list to PDF.
- P3 — Rotate hero LORE on Landing (currently hardcoded Sons of Horus quote).
- P3 — Per-faction conversion engine: surface Acheron/Atropos in the roster when Enhanced Forges is taken (currently the upgrade pays its cost but the original Knight unit remains visible).
- P3 — `/api/health` readiness endpoint.

## Test credentials
n/a — localStorage only, no auth.
