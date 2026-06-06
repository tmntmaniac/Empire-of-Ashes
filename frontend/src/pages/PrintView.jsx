import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getArmy } from "@/lib/storage";
import { fetchFaction } from "@/lib/api";
import { armyTotal, formationCost } from "@/lib/points";
import { Printer, ArrowLeft } from "lucide-react";

export default function PrintView() {
    const { id } = useParams();
    const [army, setArmy] = useState(null);
    const [faction, setFaction] = useState(null);

    useEffect(() => {
        const a = getArmy(id);
        setArmy(a);
        if (a) fetchFaction(a.factionId).then(setFaction);
    }, [id]);

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
                <div className="max-w-5xl mx-auto px-6 py-3 flex items-center justify-between">
                    <Link to={`/builder/${army.id}`} className="font-mono text-[10px] tracking-[0.3em] uppercase text-[#888] hover:text-[#2D937D] inline-flex items-center gap-1" data-testid="print-back">
                        <ArrowLeft className="w-3 h-3" /> Back to Builder
                    </Link>
                    <button onClick={() => window.print()} className="btn-primary inline-flex items-center gap-2" data-testid="print-trigger">
                        <Printer className="w-4 h-4" /> Print Document
                    </button>
                </div>
            </div>

            <div className="max-w-5xl mx-auto px-6 py-10 print-section" data-testid="print-view">
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

                {(army.formations || []).map((f, i) => {
                    const def = formDefMap[f.formationId];
                    if (!def) return null;
                    const cost = formationCost(f, def);
                    const option = def.unitOptions[f.optionIndex || 0];
                    const units = (option?.units || []).map((u) => ({ ...u }));
                    if (def.extraUnit && f.extraUnits) {
                        const idx = units.findIndex((x) => x.unit === def.extraUnit.unit);
                        if (idx >= 0) units[idx] = { ...units[idx], count: units[idx].count + f.extraUnits };
                    }
                    return (
                        <div key={f.id} className="mb-6 print-section" data-testid={`print-formation-${i}`}>
                            <div className="flex items-baseline justify-between border-b border-[#444] pb-1 mb-2">
                                <h2 className="font-display text-2xl uppercase tracking-tight">{def.name} <span className="text-sm text-[#888]">({def.category})</span></h2>
                                <span className="font-mono text-sm text-[#C2A165]">{cost} pts</span>
                            </div>
                            <div className="font-mono text-xs text-[#888] mb-2">
                                {units.map((u, j) => {
                                    const unit = faction.units[u.unit];
                                    return <span key={j}>{u.count}× {unit?.name || u.unit}{j < units.length - 1 ? " · " : ""}</span>;
                                })}
                            </div>
                            {(f.upgrades || []).length > 0 && (
                                <ul className="text-sm pl-4 list-disc text-[#B8B8B8]">
                                    {f.upgrades.map((u) => {
                                        const upg = upgradeMap[u.upgradeId];
                                        if (!upg) return null;
                                        return (
                                            <li key={u.upgradeId}>
                                                <span className="text-[#E0E0E0] font-semibold">{upg.name}</span>
                                                {u.selections.length > 0 && (
                                                    <span> — {u.selections.map((s) => `${s.count}× ${variantName(u.upgradeId, s.variantId)}`).join(", ")}</span>
                                                )}
                                            </li>
                                        );
                                    })}
                                </ul>
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
