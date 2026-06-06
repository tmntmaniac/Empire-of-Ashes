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
**Line (5)**: `tactical-detachment`, `assault-detachment`, `breacher-detachment`, `terminator-detachment`, `reaver-detachment`.
**Support (33)**: `luperci-pack`, `justaerian-detachment`, `destroyer-squad`, `inductii-squad`, `recon-squad`, `scout-detachment`, `veteran-squad`, `outrider-squad`, `jetbike-squad`, `land-speeder-squadron`, `javelin-squadron`, `castraferrum-talon`, `contemptor-talon`, `leviathan-talon`, `air-defence-battery`, `artillery-battery-arquitor`, `artillery-battery-basilisk`, `artillery-battery-medusa`, `artillery-battery-whirlwind`, `kratos-heavy-squadron`, `land-raider-squadron`, `predator-squadron`, `sabre-squadron`, `sicaran-squadron`, `vindicator-squadron`, `storm-eagle-flight`, `thunderhawk-gunship`, `thunderhawk-transporter-flight`, `legion-spacecraft-strike-cruiser`, `legion-spacecraft-battleship`, `assault-squad-support`, `breacher-squad-support`, `rapier-battery`.
**Lords of War (7)**: `plutona-assault-drill`, `heavy-tank-battery`, `superheavy-squadron`, `superheavy-tank-destroyer`, `gunship-flight`, `interceptor-flight`, `stormbird-lander`.
**Primarch (1)**: `horus` (unique, max 1).

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
- **Feb 2026** — Upgrade-variant Roster integration.
  - `factions.json` expanded to 43 units, 8 formations, 12 upgrades; all variant ids resolve to unit defs.
  - `FormationEditor.jsx` merges selected upgrade variants into `displayUnits` passed to `UnitStatTable` so Rhino/Damocles/Predator/Sicaran/Dreadnought variants/Consuls/Armoury assets all render their stats in the roster.
  - **Backend hot-reload fix**: `server.py` now reads `factions.json` fresh per request (removed import-time cache that silently served stale data until manual `supervisorctl restart`).
  - **Testing**: iteration_3 — 18/18 critical regression assertions pass post-fix. Backend pytest 6/6 pass. No console errors.
- **Feb 2026** — In-app Confirm dialogs for destructive actions (delete army & remove formation).
  - New reusable component `/app/frontend/src/components/ConfirmDialog.jsx` — grimdark `corner-frame` panel, red eyebrow + AlertTriangle for destructive variant, configurable testIds.
  - `Builder.jsx` `removeFormation` → opens `remove-formation-dialog` (KEEP / DISBAND); shows the formation's display name in the body.
  - `ArmyManager.jsx` `handleDelete` → opens `delete-army-dialog` (KEEP / DISBAND); shows the army name; removes browser `window.confirm()` (was being blocked/ugly in some iframes).
  - testIds: `remove-formation-dialog{,-cancel,-confirm}`, `delete-army-dialog{,-cancel,-confirm}`.
  - **Testing**: Self-tested via Playwright — seed army → click trash → dialog appears → cancel preserves → confirm deletes; same flow verified in ArmyManager. Toast confirmations fire on success.
- **Feb 2026** — Sons of Horus codex full expansion (Support + Lords of War).
  - `factions.json` grown from 8 → **46 formations** (5 Line, 33 Support, 7 Lords of War, 1 Primarch) and 43 → **71 units**.
  - Reclassified `reaver-detachment` from "Support" → "Line" per source PDF.
  - **New Line**: (reaver moved in).
  - **New Support (31)**: destroyer-squad, inductii-squad, recon-squad, scout-detachment, veteran-squad, outrider-squad, jetbike-squad, land-speeder-squadron, javelin-squadron, castraferrum-talon, contemptor-talon, leviathan-talon, air-defence-battery (Skyreaper), artillery-batteries (Arquitor / Basilisk / Medusa / Whirlwind), kratos-heavy-squadron, land-raider-squadron, predator-squadron, sabre-squadron, sicaran-squadron, vindicator-squadron, storm-eagle-flight, thunderhawk-gunship, thunderhawk-transporter-flight, legion-spacecraft-{strike-cruiser,battleship}, assault-squad-support, breacher-squad-support, rapier-battery.
  - **New Lords of War (7)**: plutona-assault-drill, heavy-tank-battery (Falchion), superheavy-squadron (Fellblade), superheavy-tank-destroyer (Glaive), gunship-flight (Fire Raptor), interceptor-flight (Xiphon), stormbird-lander.
  - `Builder.jsx` AddFormationDialog now renders 4 ordered category sections: `Line | Support | Lords of War | Primarch`.
  - **Testing**: iteration_4 — Backend pytest **50/50** pass (6 base + 44 new expansion assertions in `test_expansion.py`); frontend E2E 100% (category order, LoW formations add, Reaver shows under LINE, extra-unit +60 increments, multi-formation localStorage persistence). No console errors.

## Testid Reference (for future testing agents)
- Builder Save button: `data-testid="builder-save-btn"` (NOT `save-army-btn`).
- Builder Print button: `data-testid="builder-print-btn"`.
- PrintView print trigger: `data-testid="print-trigger"`.
- AddFormationDialog category headers render as `// LINE`, `// SUPPORT`, `// LORDS OF WAR`, `// PRIMARCH` (use `innerText`).
- Extra-unit increment buttons: `extra-plus-{formation-index}` (e.g., `extra-plus-1`).

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
