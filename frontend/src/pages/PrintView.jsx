import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { toast } from "sonner";
import { getArmy } from "@/lib/storage";
import { fetchFaction } from "@/lib/api";
import { armyTotal, formationCost } from "@/lib/points";
import { Printer, ArrowLeft, Download } from "lucide-react";

// Resolve every unit (with summed counts) that appears in a fielded formation,
// merging:  base option units  →  optional extraUnits  →  addedUnits from
// selected flag upgrades  →  multi-variant upgrades whose variant id is also a
// real unit id (e.g. Infantry Support Tank → Leman Russ Demolisher).
function resolveFormationUnits(formation, def, faction) {
    const counts = new Map();
    const add = (unitId, count) => {
        if (!unitId || !faction.units[unitId]) return;
        counts.set(unitId, (counts.get(unitId) || 0) + count);
    };

    const option = def.unitOptions?.[formation.optionIndex || 0];
    (option?.units || []).forEach((u) => add(u.unit, u.count));

    if (def.extraUnit && formation.extraUnits > 0) {
        add(def.extraUnit.unit, formation.extraUnits);
    }

    const upgradeMap = Object.fromEntries(faction.upgrades.map((u) => [u.id, u]));
    (formation.upgrades || []).forEach((u) => {
        const upg = upgradeMap[u.upgradeId];
        if (!upg) return;
        (upg.addedUnits || []).forEach((au) => add(au.unit, au.count));
        if (upg.type === "multi" && !upg.conversion) {
            (u.selections || []).forEach((sel) => {
                if (faction.units[sel.variantId]) add(sel.variantId, sel.count || 0);
            });
        }
    });

    return Array.from(counts.entries()).map(([unitId, count]) => ({
        unitId,
        count,
        unit: faction.units[unitId],
    }));
}

function UnitStatBlock({ count, unit }) {
    return (
        <div className="border border-[#333] p-3 mb-2 print-keep" data-testid={`print-unit-${unit.name.replace(/\s+/g, "-").toLowerCase()}`}>
            <div className="flex items-baseline justify-between gap-3 flex-wrap mb-1">
                <h4 className="font-display text-base uppercase tracking-tight">
                    <span className="text-[#C2A165]">{count}×</span> {unit.name}
                </h4>
                <div className="font-mono text-[10px] text-[#888] uppercase tracking-widest flex gap-3">
                    <span>Type <span className="text-[#E0E0E0]">{unit.type || "—"}</span></span>
                    <span>Speed <span className="text-[#E0E0E0]">{unit.speed || "—"}</span></span>
                    <span>Armour <span className="text-[#E0E0E0]">{unit.armour || "—"}</span></span>
                    <span>CC <span className="text-[#E0E0E0]">{unit.cc || "—"}</span></span>
                    <span>FF <span className="text-[#E0E0E0]">{unit.ff || "—"}</span></span>
                </div>
            </div>
            {Array.isArray(unit.weapons) && unit.weapons.length > 0 && (
                <table className="w-full text-xs border-collapse mt-1">
                    <thead>
                        <tr className="text-left text-[#888] font-mono uppercase tracking-widest">
                            <th className="font-normal py-0.5 w-1/3">Weapon</th>
                            <th className="font-normal py-0.5 w-1/4">Range</th>
                            <th className="font-normal py-0.5">Firepower</th>
                        </tr>
                    </thead>
                    <tbody>
                        {unit.weapons.map((w, i) => (
                            <tr key={i} className="border-t border-[#222]">
                                <td className="py-0.5 pr-2 text-[#E0E0E0]">{w.name}</td>
                                <td className="py-0.5 pr-2 text-[#B8B8B8]">{w.range}</td>
                                <td className="py-0.5 text-[#B8B8B8]">{w.firepower}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
            {Array.isArray(unit.notes) && unit.notes.length > 0 && (
                <div className="mt-1 text-[11px] text-[#888] italic">{unit.notes.join(" ")}</div>
            )}
        </div>
    );
}

export default function PrintView() {
    const { id } = useParams();
    const army = useMemo(() => getArmy(id), [id]);
    const [faction, setFaction] = useState(null);
    const [savingPdf, setSavingPdf] = useState(false);
    const printableRef = useRef(null);

    useEffect(() => {
        if (army) fetchFaction(army.factionId).then(setFaction);
    }, [army]);

    const safeFilename = (name) =>
        (name || "field-roster").trim().replace(/[^a-z0-9-_ ]/gi, "").replace(/\s+/g, "-").toLowerCase() || "field-roster";

    const handlePrint = () => {
        toast.message("Opening print dialog…", { description: "Choose 'Save as PDF' as the destination if you'd rather save a file." });
        // Defer to next tick so the toast paints before the modal print dialog steals focus.
        setTimeout(() => window.print(), 60);
    };

    const handleSavePdf = async () => {
        if (!printableRef.current || savingPdf) return;
        setSavingPdf(true);
        const t = toast.loading("Generating PDF…");
        try {
            // Dynamic import keeps the ~150KB pdf bundle out of the landing critical path.
            const html2pdf = (await import("html2pdf.js")).default;
            await html2pdf()
                .set({
                    margin: 10,
                    filename: `${safeFilename(army?.name)}-roster.pdf`,
                    image: { type: "jpeg", quality: 0.95 },
                    html2canvas: { scale: 2, backgroundColor: "#ffffff", useCORS: true },
                    jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
                    pagebreak: { mode: ["css", "legacy"], avoid: ["[data-testid^='print-formation-']", ".print-keep"] },
                })
                .from(printableRef.current)
                .save();
            toast.success("PDF downloaded", { id: t });
        } catch (err) {
            // Surface the failure without crashing the page; user can retry or fall back to Print.
            console.error("PDF export failed", err);
            toast.error("Could not generate PDF", {
                id: t,
                description: "Try the Print button and choose 'Save as PDF' in the print dialog.",
            });
        } finally {
            setSavingPdf(false);
        }
    };

    if (!army) {
        return (
            <div className="max-w-3xl mx-auto p-8 text-center">
                <h1 className="font-display text-3xl uppercase">Army not found</h1>
                <Link to="/armies" className="btn-primary mt-4 inline-block">Back</Link>
            </div>
        );
    }
    if (!faction) return <div className="p-8 font-mono text-[#666] uppercase">Loading...</div>;

    const formDefMap = Object.fromEntries(faction.formations.map((f) => [f.id, f]));
    const upgradeMap = Object.fromEntries(faction.upgrades.map((u) => [u.id, u]));
    const total = armyTotal(army, faction);

    const variantName = (upgId, varId) => {
        const u = upgradeMap[upgId];
        const v = u?.variants?.find((x) => x.id === varId);
        return v?.name || varId;
    };

    return (
        <div className="min-h-screen bg-[#050505] text-[#E0E0E0]">
            <div className="no-print sticky top-0 bg-[#080A09] border-b border-[#222] z-10">
                <div className="max-w-5xl mx-auto px-6 py-3 flex items-center justify-between gap-3 flex-wrap">
                    <Link to={`/builder/${army.id}`} className="font-mono text-[10px] tracking-[0.3em] uppercase text-[#888] hover:text-[#2D937D] inline-flex items-center gap-1" data-testid="print-back">
                        <ArrowLeft className="w-3 h-3" /> Back to Builder
                    </Link>
                    <div className="flex items-center gap-2 flex-wrap">
                        <span className="hidden sm:inline font-mono text-[10px] tracking-[0.3em] uppercase text-[#555]">// Output</span>
                        <button
                            type="button"
                            onClick={handlePrint}
                            className="btn-primary inline-flex items-center gap-2"
                            data-testid="print-trigger"
                            title="Open your browser's print dialog"
                        >
                            <Printer className="w-4 h-4" /> Print
                        </button>
                        <button
                            type="button"
                            onClick={handleSavePdf}
                            disabled={savingPdf}
                            className="btn-secondary inline-flex items-center gap-2 disabled:opacity-50"
                            data-testid="save-pdf-trigger"
                            title="Download a .pdf copy to your device"
                        >
                            <Download className="w-4 h-4" /> {savingPdf ? "Generating…" : "Save as PDF"}
                        </button>
                    </div>
                </div>
            </div>

            <div ref={printableRef} className="max-w-5xl mx-auto px-6 py-10 print-section" data-testid="print-view">
                <div className="border-b-2 border-[#C2A165] pb-4 mb-6">
                    <div className="font-mono text-[10px] tracking-[0.4em] text-[#C2A165] uppercase mb-2">// Field Roster Manifest</div>
                    <h1 className="font-display text-5xl uppercase tracking-tight" data-testid="print-army-name">{army.name}</h1>
                    <div className="flex items-baseline justify-between mt-2 flex-wrap gap-2">
                        <div className="font-mono text-sm text-[#888] uppercase tracking-widest">{faction.name} · {faction.subtitle}</div>
                        <div className="font-display text-2xl text-[#2D937D]" data-testid="print-total">{total} / {army.pointsCap} pts</div>
                    </div>
                </div>

                <div className="mb-6 p-3 border border-[#C2A165]">
                    <div className="font-mono text-[10px] tracking-[0.3em] text-[#C2A165] uppercase mb-1">Legion Trait — {faction.legionTrait.name}</div>
                    <div className="text-sm">{faction.legionTrait.description}</div>
                </div>

                {Array.isArray(faction.specialRules) && faction.specialRules.length > 0 && (
                    <div className="mb-6 p-3 border border-[#7F1D1D]" data-testid="print-special-rules">
                        <div className="font-mono text-[10px] tracking-[0.3em] text-[#7F1D1D] uppercase mb-2">// Special Rules</div>
                        <div className="space-y-2">
                            {faction.specialRules.map((rule, idx) => (
                                <div key={idx}>
                                    <div className="font-display text-sm uppercase tracking-tight text-[#E5E5E5]">{rule.name}</div>
                                    <div className="text-xs text-[#B8B8B8] leading-relaxed whitespace-pre-line">{rule.description}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {(army.formations || []).map((f, i) => {
                    const def = formDefMap[f.formationId];
                    if (!def) return null;
                    const cost = formationCost(f, def);
                    const resolvedUnits = resolveFormationUnits(f, def, faction);
                    return (
                        <div key={f.id} className="mb-8 print-section" data-testid={`print-formation-${i}`}>
                            <div className="flex items-baseline justify-between border-b border-[#444] pb-1 mb-3">
                                <h2 className="font-display text-2xl uppercase tracking-tight">{def.name} <span className="text-sm text-[#888]">({def.category})</span></h2>
                                <span className="font-mono text-sm text-[#C2A165]">{cost} pts</span>
                            </div>

                            {(f.upgrades || []).length > 0 && (
                                <div className="mb-3">
                                    <div className="font-mono text-[10px] tracking-[0.3em] text-[#888] uppercase mb-1">Upgrades</div>
                                    <ul className="text-xs pl-4 list-disc text-[#B8B8B8] space-y-0.5">
                                        {f.upgrades.map((u) => {
                                            const upg = upgradeMap[u.upgradeId];
                                            if (!upg) return null;
                                            return (
                                                <li key={u.upgradeId}>
                                                    <span className="text-[#E0E0E0] font-semibold">{upg.name}</span>
                                                    {u.selections && u.selections.length > 0 && (
                                                        <span> — {u.selections.map((s) => `${s.count}× ${variantName(u.upgradeId, s.variantId)}`).join(", ")}</span>
                                                    )}
                                                    {upg.description && <span className="text-[#777]"> · {upg.description}</span>}
                                                </li>
                                            );
                                        })}
                                    </ul>
                                </div>
                            )}

                            {resolvedUnits.length > 0 && (
                                <div data-testid={`print-formation-${i}-stats`}>
                                    <div className="font-mono text-[10px] tracking-[0.3em] text-[#888] uppercase mb-1">Unit Stats</div>
                                    {resolvedUnits.map(({ unitId, count, unit }) => (
                                        <UnitStatBlock key={unitId} count={count} unit={unit} />
                                    ))}
                                </div>
                            )}
                        </div>
                    );
                })}

                {(army.formations || []).length === 0 && (
                    <div className="text-center text-[#666] font-mono uppercase tracking-widest py-12">// Roster Empty</div>
                )}
            </div>
        </div>
    );
}
