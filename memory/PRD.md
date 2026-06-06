# Empire of Ashes — Force Builder (PRD)

## Original Problem Statement
Build a force builder web application (similar to legionbuilder.app) for the "Empire of Ashes" (Epic Armageddon fan system) using unit stats and rules from an uploaded PDF.

## Product Requirements (MVP)
- LocalStorage-only persistence — **no user accounts, no database** for saving lists.
- Start strictly with the **Sons of Horus** faction (XVI Legion · The Luperci · Death Dealers legion trait).
- Visual aesthetic: **Grimdark / Warhammer 30K** (see `/app/design_guidelines.json`).
- Standard force builder features: adding formations & units, points calculation, detachments, save/duplicate/delete, print view.

## User Personas
- Tabletop hobbyist / Epic Armageddon fan player building army lists for Empire of Ashes games.

## Core Architecture
- **Frontend**: React + React Router + Tailwind (Grimdark theme) + Shadcn UI. State persisted in browser `localStorage` under key `eoa.armies.v1` via `/app/frontend/src/lib/storage.js`.
- **Backend**: FastAPI serving parsed PDF rules data as static JSON. Single endpoint: `GET /api/factions`. Mongo client present but unused (MVP).
- **No auth, no DB writes.**

## Key Files
- `/app/backend/server.py` — FastAPI app
- `/app/backend/data/factions.json` — Sons of Horus units/formations/upgrades (dict-keyed by id)
- `/app/backend/tests/test_factions.py` — backend pytest suite
- `/app/frontend/src/App.js` + `/app/frontend/src/pages/{Landing,ArmyManager,Builder,PrintView}.jsx`
- `/app/frontend/src/components/{Layout,FormationEditor,UnitStatTable}.jsx`
- `/app/frontend/src/lib/{storage,api,points}.js`
- `/app/design_guidelines.json`

## Sons of Horus Formation IDs (kebab-case)
`tactical-detachment`, `assault-detachment`, `breacher-detachment`, `terminator-detachment`, `reaver-detachment`, `luperci-pack`, `justaerian-detachment`, `horus` (primarch — unique, max 1).

## Completed (CHANGELOG)
- **Feb 2026** — MVP Force Builder complete & verified.
  - Landing, ArmyManager, Builder, PrintView, FormationEditor, UnitStatTable React UI.
  - Tailwind Grimdark styling.
  - FastAPI `/api/factions` serving Sons of Horus JSON.
  - LocalStorage save/load/duplicate/delete with toast notifications.
  - Formation cards with stat table (Unit / Type / Speed / Armour / CC / FF / Weapons).
  - Upgrade toggle + variant +/- (e.g., Rhino +10 each); Primarch Horus uniqueness enforced.
  - Print view with print-total and back nav.
  - Full data-testid coverage on all interactive elements.
  - **Testing**: Backend 6/6 pytest pass, Frontend 16/16 e2e flows pass (iteration_1 and iteration_2 confirm). No console errors.

## Roadmap

### P1 — Next
- Implement legal list validation (max detachments per army, required core formations, faction-specific composition rules from PDF).
- Replace `window.confirm()` (in `ArmyManager.handleDelete` & `Builder.removeFormation`) with Shadcn `AlertDialog` for visual consistency and cleaner e2e test wiring.
- Point-cap warning UI when total > cap (color + message).

### P2 — Future / Backlog
- Add more factions from the PDF (Imperial Fists, Death Guard, etc.).
- URL-based army sharing (encode army into shareable link, no backend persistence).
- Export army list to PDF.
- Optional Mongo persistence (cloud sync) — opt-in.
- Mobile-optimized builder layout.

## Test Credentials
N/A — no auth.
