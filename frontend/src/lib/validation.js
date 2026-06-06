// Pure list-validation logic for Empire of Ashes.
// Rules (per source PDF, pages 4–6 + 31–36):
//   R1 — At least 1 Line detachment required for any non-empty army.
//   R2 — Up to N Support detachments allowed per Line detachment.
//        (Astartes: 3 per Line. Solar Auxilia / Imperialis Militia: 2 per Line.)
//   R3 — Lords of War may consume at most 33% of the army's points cap.
//   R4 — Each Line detachment may take up to M upgrades.
//        (Astartes: 4. Solar Auxilia / Imperialis Militia: 3.)
//   R5 — Only 1 Primarch may be taken.
//   R6 — Per-formation count caps. A formation may carry `maxPer: {points: N}`
//        which means "1 instance allowed per N points of the army's pointsCap"
//        (e.g. Cerastus Lance: 1 per 2,000 pts → 1 at 2000pts, 2 at 4000pts).
//
// Limits are read from `faction.compositionLimits` when present, with
// Astartes defaults as a fallback so existing legion data keeps working.
import { formationCost } from "@/lib/points";

// Astartes defaults (used when a faction omits compositionLimits).
export const DEFAULT_LIMITS = {
    maxSupportPerLine: 3,
    maxUpgradesPerLine: 4,
    lowPct: 0.33,
};
export const MAX_PRIMARCHS = 1;

// Back-compat exports — kept for any importer outside this module.
export const LOW_PCT_LIMIT = DEFAULT_LIMITS.lowPct;
export const MAX_SUPPORT_PER_LINE = DEFAULT_LIMITS.maxSupportPerLine;
export const MAX_UPGRADES_PER_LINE = DEFAULT_LIMITS.maxUpgradesPerLine;

export function limitsFor(faction) {
    return { ...DEFAULT_LIMITS, ...(faction?.compositionLimits || {}) };
}

export function validateArmy(army, faction) {
    const issues = [];
    if (!army || !faction) return { valid: true, issues, stats: null };

    const limits = limitsFor(faction);
    const formDefMap = Object.fromEntries((faction.formations || []).map((f) => [f.id, f]));
    const formations = army.formations || [];
    const cap = army.pointsCap || 0;

    // Group formations by category and capture each formation's def+cost.
    const byCategory = { Line: [], Support: [], "Lords of War": [], Primarch: [] };
    formations.forEach((f, idx) => {
        const def = formDefMap[f.formationId];
        if (!def) return;
        const entry = { idx, formation: f, def, cost: formationCost(f, def) };
        if (byCategory[def.category]) byCategory[def.category].push(entry);
    });

    const lineCount = byCategory.Line.length;
    const supportCount = byCategory.Support.length;
    const lowCount = byCategory["Lords of War"].length;
    const primarchCount = byCategory.Primarch.length;

    const lowPoints = byCategory["Lords of War"].reduce((s, e) => s + e.cost, 0);
    const lowLimit = Math.floor(cap * limits.lowPct);
    const supportLimit = lineCount * limits.maxSupportPerLine;

    // R1 — at least one Line detachment (only meaningful if any formation is present)
    if (formations.length > 0 && lineCount === 0) {
        issues.push({
            code: "no-line",
            severity: "error",
            message: "Army must include at least one Line detachment.",
        });
    }

    // R2 — Support ≤ Line × N
    if (supportCount > supportLimit) {
        issues.push({
            code: "support-over-limit",
            severity: "error",
            message:
                lineCount === 0
                    ? `${supportCount} Support detachments taken — Support requires a Line detachment.`
                    : `Too many Support detachments — ${supportCount} taken, max ${supportLimit} allowed (${limits.maxSupportPerLine} per Line).`,
        });
    }

    // R3 — Lords of War ≤ lowPct of points cap
    if (lowPoints > lowLimit && cap > 0) {
        const pct = Math.round(limits.lowPct * 100);
        issues.push({
            code: "low-over-limit",
            severity: "error",
            message: `Lords of War exceed ${pct}% of cap — ${lowPoints} pts taken, max ${lowLimit} pts allowed.`,
        });
    }

    // R4 — Each Line detachment may take up to M upgrades
    byCategory.Line.forEach((e) => {
        const upgradesTaken = (e.formation.upgrades || []).length;
        if (upgradesTaken > limits.maxUpgradesPerLine) {
            issues.push({
                code: "upgrades-over-limit",
                severity: "error",
                formationIdx: e.idx,
                message: `${e.def.name} has ${upgradesTaken} upgrades — max ${limits.maxUpgradesPerLine} per Line detachment.`,
            });
        }
    });

    // R5 — Max 1 Primarch (already enforced by UI; validate defensively)
    if (primarchCount > MAX_PRIMARCHS) {
        issues.push({
            code: "primarch-over-limit",
            severity: "error",
            message: `Only ${MAX_PRIMARCHS} Primarch allowed — ${primarchCount} taken.`,
        });
    }

    // R6 — Per-formation count caps (formation.maxPer: { points: N })
    //   "1 per N points" → allowed = floor(cap / N)
    if (cap > 0) {
        const formationCounts = new Map();
        formations.forEach((f) => {
            formationCounts.set(f.formationId, (formationCounts.get(f.formationId) || 0) + 1);
        });
        formationCounts.forEach((count, formationId) => {
            const def = formDefMap[formationId];
            const perPoints = def?.maxPer?.points;
            if (!perPoints) return;
            const allowed = Math.floor(cap / perPoints);
            if (count > allowed) {
                issues.push({
                    code: "formation-over-cap",
                    severity: "error",
                    message: `${def.name}: ${count} taken — max ${allowed} allowed (1 per ${perPoints} pts).`,
                });
            }
        });
    }

    return {
        valid: issues.length === 0,
        issues,
        stats: {
            lineCount,
            supportCount,
            supportLimit,
            lowCount,
            lowPoints,
            lowLimit,
            primarchCount,
            limits,
        },
    };
}
