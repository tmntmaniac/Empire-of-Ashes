import { useEffect, useMemo, useState } from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import { getArmy, upsertArmy } from "@/lib/storage";
import { fetchFaction } from "@/lib/api";
import { armyTotal, formationCost } from "@/lib/points";
import FormationEditor from "@/components/FormationEditor";
import ConfirmDialog from "@/components/ConfirmDialog";
import PointsCapBar from "@/components/PointsCapBar";
import ArmyValidationPanel from "@/components/ArmyValidationPanel";
import { validateArmy, limitsFor } from "@/lib/validation";
import { ArrowLeft, Plus, Printer, Save } from "lucide-react";
import { toast } from "sonner";

export default function Builder() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [army, setArmy] = useState(() => getArmy(id));
    const [faction, setFaction] = useState(null);
    const [error, setError] = useState(army ? null : "Army not found.");
    const [addOpen, setAddOpen] = useState(false);
    const [removeIdx, setRemoveIdx] = useState(null);
if (!army) return null;

    useEffect(() => {
        if (!army) return;
        fetchFaction(army.factionId).then(setFaction).catch(() => setError("Failed to load faction codex."));
    }, [army]);

    // Auto save on every change
    useEffect(() => {
        if (army && faction) {
            upsertArmy(army);
        }
    }, [army, faction]);

    const formDefMap = useMemo(() => Object.fromEntries((faction?.formations || []).map((f) => [f.id, f])), [faction]);

    if (error) {
        return (
            <div className="max-w-3xl mx-auto px-6 py-20 text-center">
                <div className="font-mono text-[11px] tracking-[0.4em] text-[#C2392E] uppercase mb-2">// Transmission Lost</div>
                <h1 className="font-display text-4xl uppercase mb-4">{error}</h1>
                <Link to="/armies" className="btn-primary inline-flex items-center gap-2"><ArrowLeft className="w-4 h-4" /> Back to Armies</Link>
            </div>
        );
    }
    if (!army || !faction) {
        return <div className="max-w-7xl mx-auto px-6 py-20 text-center font-mono text-[#666] uppercase tracking-widest" data-testid="builder-loading">Decrypting codex...</div>;
    }

    const total = army ? armyTotal(army, faction) : 0;
    const cap = army?.pointsCap || 0;

    // Counts for composition rules
    const counts = (army?.formations || []).reduce((acc, f) => {
        const def = formDefMap[f.formationId];
        if (!def) return acc;
        acc[def.category] = (acc[def.category] || 0) + 1;
        return acc;
    }, {});
    const hasHorus = (army?.formations || []).some((f) => f.formationId === "horus");

    const validation = validateArmy(army, faction);

    const addFormation = (formDef) => {
        const newForm = {
            id: crypto.randomUUID(),
            formationId: formDef.id,
            optionIndex: 0,
            extraUnits: 0,
            upgrades: [],
        };
        setArmy({ ...army, formations: [...(army?.formations || []), newForm] });
        setAddOpen(false);
        toast.success(`${formDef.name} added.`);
    };

    const updateFormation = (idx, updated) => {
        const next = [...army?.formations];
        next[idx] = updated;
        setArmy({ ...army, formations: next });
    };
    const removeFormation = (idx) => {
        setRemoveIdx(idx);
    };
    const confirmRemoveFormation = () => {
        if (removeIdx == null) return;
        const def = formDefMap[army?.formations[removeIdx]?.formationId];
        setArmy({ ...army, formations: army?.formations.filter((_, i) => i !== removeIdx) });
        setRemoveIdx(null);
        toast.success(`${def?.name || "Formation"} disbanded.`);
    };

    return (
        <div className="max-w-7xl mx-auto px-6 py-8" data-testid="builder-page">
            {/* Header */}
            <div className="flex flex-wrap items-start justify-between gap-4 mb-6 pb-4 border-b border-[#222]">
                <div>
                    <Link to="/armies" className="font-mono text-[10px] tracking-[0.3em] text-[#888] hover:text-[#2D937D] uppercase inline-flex items-center gap-1 mb-2" data-testid="back-to-armies">
                        <ArrowLeft className="w-3 h-3" /> Roster
                    </Link>
                    <h1 className="font-display text-4xl sm:text-5xl uppercase tracking-tight" data-testid="builder-army-name">{army.name}</h1>
                    <div className="font-mono text-[11px] tracking-[0.3em] text-[#C2A165] uppercase mt-1">{faction.name} · {faction.subtitle}</div>
                </div>
                <div className="flex flex-wrap items-center gap-2">
                    <Link to={`/print/${army.id}`} className="btn-ghost inline-flex items-center gap-2" data-testid="builder-print-btn">
                        <Printer className="w-4 h-4" /> Print
                    </Link>
                    <button onClick={() => { upsertArmy(army); toast.success("Saved."); }} className="btn-primary inline-flex items-center gap-2" data-testid="builder-save-btn">
                        <Save className="w-4 h-4" /> Save
                    </button>
                </div>
            </div>

            {/* Points bar */}
            <PointsCapBar
                total={total}
                cap={cap}
                counts={counts}
                hasHorus={hasHorus}
                onCapChange={(next) => setArmy({ ...army, pointsCap: next })}
            />

            {/* Force composition validation */}
            <ArmyValidationPanel result={validation} hasFormations={(army?.formations || []).length > 0} />

            {/* Legion Trait */}
            <div className="panel panel-gold p-4 mb-6" data-testid="legion-trait">
                <div className="font-mono text-[10px] tracking-[0.3em] text-[#C2A165] uppercase mb-1">// Legion Trait</div>
                <div className="flex items-baseline gap-3 flex-wrap">
                    <h3 className="font-display text-2xl uppercase tracking-tight text-[#C2A165]">{faction.legionTrait.name}</h3>
                    <p className="text-sm text-[#B8B8B8] font-sans flex-1 min-w-[200px]">{faction.legionTrait.description}</p>
                </div>
            </div>

            {/* Special Rules (faction-specific army rules from the source rulebook) */}
            {Array.isArray(faction?.specialRules) && faction?.specialRules.length > 0 && (
                <div className="panel p-4 mb-6 border border-[#7F1D1D]" data-testid="special-rules">
                    <div className="font-mono text-[10px] tracking-[0.3em] text-[#7F1D1D] uppercase mb-3">// Special Rules</div>
                    <div className="space-y-3">
                        {faction?.specialRules.map((rule, idx) => (
                            <div key={idx} data-testid={`special-rule-${idx}`}>
                                <h4 className="font-display text-lg uppercase tracking-tight text-[#E5E5E5] mb-1">{rule.name}</h4>
                                <p className="text-sm text-[#B8B8B8] font-sans leading-relaxed whitespace-pre-line">{rule.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Formations */}
            <div className="space-y-4 mb-6" data-testid="formations-list">
                {(army?.formations || []).length === 0 && (
                    <div className="panel corner-frame p-10 text-center" data-testid="empty-formations">
                        <div className="font-mono text-[11px] tracking-[0.4em] text-[#C2A165] uppercase mb-2">// Awaiting Orders</div>
                        <h3 className="font-display text-2xl uppercase mb-3">No Formations Deployed</h3>
                        <p className="text-[#888] mb-4 text-sm">Add your first detachment to begin building this force.</p>
                    </div>
                )}
                {(army?.formations || []).map((f, i) => {
                    const def = formDefMap[f.formationId];
                    const isLine = def?.category === "Line";
                    const upgradeMax = isLine ? limitsFor(faction).maxUpgradesPerLine : null;
                    return (
                        <FormationEditor
                            key={f.id}
                            index={i}
                            formation={f}
                            formationDef={def}
                            faction={faction}
                            upgradeMax={upgradeMax}
                            onChange={(updated) => updateFormation(i, updated)}
                            onRemove={() => removeFormation(i)}
                        />
                    );
                })}
            </div>

            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="add-formation-btn">
                <Plus className="w-4 h-4" /> Add Formation
            </button>

            {/* Composition Rules side panel */}
            <details className="mt-10 panel p-4" data-testid="composition-rules">
                <summary className="cursor-pointer font-display text-xl uppercase tracking-tight">Composition Rules</summary>
                <ul className="mt-3 text-sm text-[#B8B8B8] list-disc pl-5 space-y-1 font-sans">
                    {(faction.compositionRules || []).map((r, i) => <li key={i}>{r}</li>)}
                </ul>
            </details>

            {addOpen && (
                <AddFormationDialog
                    faction={faction}
                    hasHorus={hasHorus}
                    onClose={() => setAddOpen(false)}
                    onAdd={addFormation}
                />
            )}

            <ConfirmDialog
                open={removeIdx != null}
                eyebrow="// Disband Formation"
                title="Remove Formation?"
                message={
                    removeIdx != null
                        ? `${formDefMap[army?.formations[removeIdx]?.formationId]?.name || "This formation"} will be removed from the roster. Upgrades and unit selections will be lost.`
                        : ""
                }
                confirmLabel="Disband"
                cancelLabel="Keep"
                destructive
                onConfirm={confirmRemoveFormation}
                onCancel={() => setRemoveIdx(null)}
                testId="remove-formation-dialog"
            />
        </div>
    );
}

function AddFormationDialog({ faction, hasHorus, onClose, onAdd }) {
    const groups = (faction?.formations || []).reduce((acc, f) => {
        (acc[f.category] = acc[f.category] || []).push(f);
        return acc;
    }, {});

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4" data-testid="add-formation-dialog">
            <div className="panel corner-frame w-full max-w-4xl max-h-[85vh] overflow-y-auto bg-[#0A0C0B] p-6">
                <div className="flex items-center justify-between mb-4 border-b border-[#222] pb-3">
                    <div>
                        <div className="font-mono text-[11px] tracking-[0.4em] text-[#C2A165] uppercase mb-1">// Detachment Selection</div>
                        <h2 className="font-display text-3xl uppercase tracking-tight">Add Formation</h2>
                    </div>
                    <button onClick={onClose} className="btn-ghost" data-testid="close-add-formation">Close</button>
                </div>
                {["Line", "Support", "Lords of War", "Primarch"].map((cat) =>
                    groups[cat] ? (
                        <div key={cat} className="mb-6">
                            <div className="font-mono text-[10px] tracking-[0.3em] text-[#888] uppercase mb-2">// {cat}</div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                {groups[cat].map((f) => {
                                    const disabled = f.id === "horus" && hasHorus;
                                    return (
                                        <button
                                            key={f.id}
                                            disabled={disabled}
                                            onClick={() => onAdd(f)}
                                            className="text-left p-3 border border-[#222] hover:border-[#2D937D] bg-[#0A0C0B] disabled:opacity-30 disabled:cursor-not-allowed transition-colors group"
                                            data-testid={`add-formation-${f.id}`}
                                        >
                                            <div className="flex items-center justify-between mb-1">
                                                <h4 className="font-display text-xl uppercase tracking-tight group-hover:text-[#2D937D]">{f.name}</h4>
                                                <span className="font-mono text-sm text-[#C2A165]">{f.baseCost} pts</span>
                                            </div>
                                            <div className="text-xs text-[#888] font-sans">{f.composition}</div>
                                            {disabled && <div className="text-[10px] text-[#C2392E] uppercase tracking-widest mt-1 font-mono">Already taken</div>}
                                        </button>
                                    );
                                })}
                            </div>
                        </div>
                    ) : null
                )}
            </div>
        </div>
    );
}
