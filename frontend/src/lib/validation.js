// Pure list-validation logic for Empire of Ashes.
// Rules (per source PDF, pages 4–6):
//   R1 — At least 1 Line detachment required for any non-empty army.
//   R2 — Up to 3 Support detachments allowed per Line detachment.
//   R3 — Lords of War may consume at most 33% of the army's points cap.
//   R4 — Each Line detachment may take up to 4 upgrades.
//   R5 — Only 1 Primarch may be taken.
import { formationCost } from "@/lib/points";

export const LOW_PCT_LIMIT = 0.33;
export const MAX_SUPPORT_PER_LINE = 3;
export const MAX_UPGRADES_PER_LINE = 4;
export const MAX_PRIMARCHS = 1;

export function validateArmy(army, faction) {
    const issues = [];
    if (!army || !faction) return { valid: true, issues, stats: null };

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
    const lowLimit = Math.floor(cap * LOW_PCT_LIMIT);
    const supportLimit = lineCount * MAX_SUPPORT_PER_LINE;

    // R1 — at least one Line detachment (only meaningful if any formation is present)
    if (formations.length > 0 && lineCount === 0) {
        issues.push({
            code: "no-line",
            severity: "error",
            message: "Army must include at least one Line detachment.",
        });
    }

    // R2 — Support ≤ Line × 3
    if (supportCount > supportLimit) {
        issues.push({
            code: "support-over-limit",
            severity: "error",
            message:
                lineCount === 0
                    ? `${supportCount} Support detachments taken — Support requires a Line detachment.`
                    : `Too many Support detachments — ${supportCount} taken, max ${supportLimit} allowed (3 per Line).`,
        });
    }

    // R3 — Lords of War ≤ 33% of points cap
    if (lowPoints > lowLimit && cap > 0) {
        issues.push({
            code: "low-over-limit",
            severity: "error",
            message: `Lords of War exceed 33% of cap — ${lowPoints} pts taken, max ${lowLimit} pts allowed.`,
        });
    }

    // R4 — Each Line detachment may take up to 4 upgrades
    byCategory.Line.forEach((e) => {
        const upgradesTaken = (e.formation.upgrades || []).length;
        if (upgradesTaken > MAX_UPGRADES_PER_LINE) {
            issues.push({
                code: "upgrades-over-limit",
                severity: "error",
                formationIdx: e.idx,
                message: `${e.def.name} has ${upgradesTaken} upgrades — max ${MAX_UPGRADES_PER_LINE} per Line detachment.`,
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
        },
    };
}
