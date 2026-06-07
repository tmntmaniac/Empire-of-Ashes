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
- 2026-02 — Added **Knight Households** (7 formations, 15 units, 6 upgrades) and **Legio Titanicus** (9 formations, 12 units, 10 upgrades incl. 6 weapon-slot upgrades) as standalone factions. Introduced `conversion: true` flag on upgrades (Titan weapon-slot picks) so they pay variant cost without injecting fake units into the roster. 22 active factions total. 7/7 new-army backend tests + e2e UI confirmed via testing_agent_v3_fork iter11 (10/10 frontend scenarios, KH Quesetorius Lance @ 325 pts, KH Dominus Lance @ 425 pts, LT Warlord @ 725 pts, Warhound Hunting Pack @ 500 pts with 6 conversion weapon slots, free-variant + premium-variant (+25) costs, conversion guarantees no phantom roster row).
- 2026-02 — Added **R6 per-formation count caps** to `validation.js`. New data field `formation.maxPer: {points: N}` reads "1 instance per N points of pointsCap". Six formations now carry the cap: Knight Households (Cerastus Lance, Grand Quesetorius Lance: 1 per 2000), Legio Titanicus (Warhound Scout, Direwolf Heavy Scout, Warbringer Titan: 1 per 2000; Emperor Titan: 1 per 7500). Issue code `formation-over-cap` with message `<name>: <count> taken — max <allowed> allowed (1 per <N> pts).` Verified via iter12 (9/9 pytest + 8/8 Playwright, all rules R1-R6 green).
- 2026-02 — Added **Mechanicum Taghmata** (20 formations, 28 units, 8 upgrades — Adsecularis/Thallax/Ursarax/Vorax/Castellax Line; Myrmidon/Arletax/Domitar/Karacnos/Krios/Tarantula/Thanatar/Minotaur/Vulturax/Ordinatus-Minorus Support; Avenger/Lightning/Falchion/Ordinatus-Majoris/Ark-Mechanicus LoW), **Legio Custodes** (14 formations, 22 units, 8 upgrades — 50% LoW cap, lowPct:0.5), and **Daemons of the Ruinstorm** (22 formations, 33 units, 18 upgrades — four chaos god Line detachments, only 1 Support per Line, upgrades effectively unlimited via maxUpgradesPerLine:99). 25 active factions total. Added new validation rule **R7 (`formation-over-army-cap`)** — `formation.maxPerArmy: N` is now enforced (Ordinatus Majoris/Ark Mechanicus/Command Retinue all 1-per-force). Removed the "Mechanicum coming soon" teaser from Landing. Verified via iter13 (14/14 pytest + 12/12 Playwright scenarios, zero bugs).

## Backlog
- P2 — URL-based army sharing (stateless base64 share string).
- P2 — Cache `build_factions()` with mtime check (currently re-reads + deep-copies per request).
- P2 — Refresh stale tests in `test_legions.py` / `test_soh_isolation.py` (27 stale assertions still expect 18 factions and the old Alpha Legion trait name).
- P2 — Add `data-testid="formation-option-${def.id}"` to AddFormation dialog cards for easier future test selection (carried over from iter13 review).
- P3 — Export army list to PDF.
- P3 — Rotate hero LORE on Landing (currently hardcoded Sons of Horus quote).
- P3 — Per-faction conversion engine: surface Acheron/Atropos in the roster when Enhanced Forges is taken (currently the upgrade pays its cost but the original Knight unit remains visible).
- P3 — `/api/health` readiness endpoint.
- P3 — Psi-Titan loyalty restriction (loyalist-only — needs an army-level loyalty flag first).
- P3 — Daemonic "single chaos-god affiliation" enforcement (e.g. Bloodthirster cannot ally with Tzeentch-only force).

## Test credentials
n/a — localStorage only, no auth.
