import { useState } from "react";
import { ChevronDown, ChevronUp, Trash2, Minus, Plus } from "lucide-react";
import UnitStatTable from "@/components/UnitStatTable";
import { formationCost } from "@/lib/points";

export default function FormationEditor({ formation, formationDef, faction, onChange, onRemove, index }) {
    const [open, setOpen] = useState(true);
    if (!formationDef) {
        return (
            <div className="panel p-4 border border-[#7F1D1D]" data-testid={`formation-${index}-missing`}>
                <div className="text-[#C2392E] font-mono uppercase text-xs">Missing formation definition: {formation.formationId}</div>
                <button onClick={onRemove} className="btn-danger mt-2">Remove</button>
            </div>
        );
    }

    const cost = formationCost(formation, formationDef);
    const option = formationDef.unitOptions[formation.optionIndex || 0];

    const setExtra = (delta) => {
        const max = formationDef.extraUnit?.max || 0;
        const next = Math.max(0, Math.min(max, (formation.extraUnits || 0) + delta));
        onChange({ ...formation, extraUnits: next });
    };

    const toggleUpgrade = (upg) => {
        const exists = (formation.upgrades || []).find((u) => u.upgradeId === upg.id);
        if (exists) {
            onChange({ ...formation, upgrades: formation.upgrades.filter((u) => u.upgradeId !== upg.id) });
        } else {
            const newUp = { upgradeId: upg.id, selections: [], flagCost: 0 };
            if (upg.type === "flag") newUp.flagCost = upg.cost || 0;
            if (upg.type === "single" && upg.variants?.length) {
                newUp.selections = [{ variantId: upg.variants[0].id, count: 1, cost: upg.cost || 0 }];
            }
            onChange({ ...formation, upgrades: [...(formation.upgrades || []), newUp] });
        }
    };

    const updateUpgradeSel = (upgId, mapper) => {
        onChange({
            ...formation,
            upgrades: formation.upgrades.map((u) => (u.upgradeId === upgId ? mapper(u) : u)),
        });
    };

    const allowed = (formationDef.allowedUpgrades || []).map((id) => faction.upgrades.find((u) => u.id === id)).filter(Boolean);

    // compute units for stat table
    const baseUnits = (option?.units || []).map((u) => ({ ...u, count: u.count }));
    if (formationDef.extraUnit && formation.extraUnits) {
        const idx = baseUnits.findIndex((x) => x.unit === formationDef.extraUnit.unit);
        if (idx >= 0) baseUnits[idx] = { ...baseUnits[idx], count: baseUnits[idx].count + formation.extraUnits };
    }
    const unitCounts = new Map(baseUnits.map((u) => [u.unit, u.count]));
    // Merge in selected upgrade variants so their stat lines appear in the roster
    (formation.upgrades || []).forEach((selectedUp) => {
        const upDef = faction.upgrades.find((u) => u.id === selectedUp.upgradeId);
        if (!upDef || upDef.type === "flag") return;
        (selectedUp.selections || []).forEach((s) => {
            if (!s.variantId || !s.count) return;
            // Resolve variant id against faction.units (variant.id == unit id by convention)
            if (!faction.units?.[s.variantId]) return;
            unitCounts.set(s.variantId, (unitCounts.get(s.variantId) || 0) + s.count);
        });
    });
    const displayUnits = Array.from(unitCounts.entries()).map(([unitId, count]) => ({ unitId, count }));

    const categoryColor = {
        Line: "tag-green",
        Support: "tag",
        Primarch: "tag",
    }[formationDef.category] || "tag";

    return (
        <div className="panel panel-accent" data-testid={`formation-card-${index}`}>
            <div className="flex items-center justify-between p-4 border-b border-[#222] cursor-pointer" onClick={() => setOpen(!open)}>
                <div className="flex items-center gap-3 flex-1 min-w-0">
                    <span className="font-mono text-[10px] text-[#666] tracking-widest">#{String(index + 1).padStart(2, "0")}</span>
                    <span className={categoryColor}>{formationDef.category}</span>
                    <h3 className="font-display text-2xl uppercase tracking-tight truncate">{formationDef.name}</h3>
                </div>
                <div className="flex items-center gap-4 pl-3">
                    <span className="font-mono text-sm text-[#C2A165]" data-testid={`formation-cost-${index}`}>{cost} pts</span>
                    <button onClick={(e) => { e.stopPropagation(); onRemove(); }} className="text-[#C2392E] hover:text-[#FF5C5C]" data-testid={`remove-formation-${index}`}>
                        <Trash2 className="w-4 h-4" strokeWidth={2} />
                    </button>
                    {open ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                </div>
            </div>

            {open && (
                <div className="p-4 space-y-5">
                    <div className="text-sm text-[#B8B8B8] font-sans">{formationDef.composition}</div>

                    {formationDef.unitOptions.length > 1 && (
                        <div>
                            <label className="field-label block mb-2">Composition Option</label>
                            <select
                                value={formation.optionIndex || 0}
                                onChange={(e) => onChange({ ...formation, optionIndex: Number(e.target.value) })}
                                className="bg-[#0E1411] border border-[#333] focus:border-[#2D937D] focus:outline-none px-3 py-2 font-sans text-[#E0E0E0] w-full sm:w-auto"
                                data-testid={`option-select-${index}`}
                            >
                                {formationDef.unitOptions.map((o, i) => (
                                    <option key={i} value={i}>{o.label}</option>
                                ))}
                            </select>
                        </div>
                    )}

                    {formationDef.extraUnit && (
                        <div className="flex items-center justify-between p-3 border border-[#222] bg-[#0A0C0B]">
                            <div>
                                <div className="font-display text-lg uppercase tracking-tight">{formationDef.extraUnit.label}</div>
                                <div className="font-mono text-xs text-[#888]">+{formationDef.extraUnit.cost} pts each · max {formationDef.extraUnit.max}</div>
                            </div>
                            <div className="flex items-center gap-2">
                                <button onClick={() => setExtra(-1)} className="btn-ghost px-2 py-1" data-testid={`extra-minus-${index}`}><Minus className="w-3 h-3" /></button>
                                <span className="font-mono text-lg w-6 text-center" data-testid={`extra-count-${index}`}>{formation.extraUnits || 0}</span>
                                <button onClick={() => setExtra(1)} className="btn-ghost px-2 py-1" data-testid={`extra-plus-${index}`}><Plus className="w-3 h-3" /></button>
                            </div>
                        </div>
                    )}

                    <div>
                        <div className="field-label mb-2">Roster</div>
                        <UnitStatTable units={displayUnits} faction={faction} />
                    </div>

                    {allowed.length > 0 && (
                        <div>
                            <div className="field-label mb-2">Upgrades</div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                {allowed.map((upg) => {
                                    const current = formation.upgrades?.find((u) => u.upgradeId === upg.id);
                                    const enabled = Boolean(current);
                                    return (
                                        <div key={upg.id} className={`border p-3 ${enabled ? "border-[#2D937D] bg-[#0E1411]" : "border-[#222] bg-[#0A0C0B]"}`} data-testid={`upgrade-${index}-${upg.id}`}>
                                            <label className="flex items-start gap-2 cursor-pointer">
                                                <input
                                                    type="checkbox"
                                                    checked={enabled}
                                                    onChange={() => toggleUpgrade(upg)}
                                                    className="mt-1 accent-[#2D937D]"
                                                    data-testid={`upgrade-toggle-${index}-${upg.id}`}
                                                />
                                                <div className="flex-1">
                                                    <div className="flex items-center justify-between gap-2">
                                                        <div className="font-display text-base uppercase tracking-tight">{upg.name}</div>
                                                        {upg.type === "flag" && upg.cost > 0 && <span className="font-mono text-xs text-[#C2A165]">+{upg.cost}</span>}
                                                        {upg.type === "single" && <span className="font-mono text-xs text-[#C2A165]">+{upg.cost}</span>}
                                                    </div>
                                                    <div className="text-xs text-[#888] font-sans leading-snug">{upg.description}</div>
                                                </div>
                                            </label>

                                            {enabled && upg.type === "single" && upg.variants && (
                                                <select
                                                    value={current.selections[0]?.variantId || ""}
                                                    onChange={(e) => updateUpgradeSel(upg.id, (u) => ({ ...u, selections: [{ variantId: e.target.value, count: 1, cost: upg.cost || 0 }] }))}
                                                    className="mt-2 w-full bg-[#050505] border border-[#333] focus:border-[#2D937D] focus:outline-none px-2 py-1 text-sm font-sans text-[#E0E0E0]"
                                                    data-testid={`upgrade-single-select-${index}-${upg.id}`}
                                                >
                                                    {upg.variants.map((v) => <option key={v.id} value={v.id}>{v.name}</option>)}
                                                </select>
                                            )}

                                            {enabled && upg.type === "multi" && upg.variants && (
                                                <div className="mt-2 space-y-1">
                                                    {upg.variants.map((v) => {
                                                        const sel = current.selections.find((s) => s.variantId === v.id);
                                                        const count = sel?.count || 0;
                                                        const totalCount = current.selections.reduce((s, x) => s + x.count, 0);
                                                        const max = upg.max;
                                                        const setCount = (n) => {
                                                            const others = current.selections.filter((s) => s.variantId !== v.id);
                                                            const nextSelections = n > 0 ? [...others, { variantId: v.id, count: n, cost: v.cost || 0 }] : others;
                                                            updateUpgradeSel(upg.id, (u) => ({ ...u, selections: nextSelections }));
                                                        };
                                                        const canAdd = !max || totalCount < max;
                                                        return (
                                                            <div key={v.id} className="flex items-center justify-between gap-2 text-sm">
                                                                <div className="flex-1">
                                                                    <span className="text-[#E0E0E0]">{v.name}</span>
                                                                    <span className="font-mono text-xs text-[#C2A165] ml-2">+{v.cost} pts</span>
                                                                </div>
                                                                <div className="flex items-center gap-1">
                                                                    <button type="button" onClick={() => setCount(Math.max(0, count - 1))} className="px-2 py-0.5 border border-[#333] hover:border-[#555]" data-testid={`upgrade-variant-minus-${index}-${upg.id}-${v.id}`}>−</button>
                                                                    <span className="font-mono w-5 text-center" data-testid={`upgrade-variant-count-${index}-${upg.id}-${v.id}`}>{count}</span>
                                                                    <button type="button" disabled={!canAdd} onClick={() => setCount(count + 1)} className="px-2 py-0.5 border border-[#333] hover:border-[#555] disabled:opacity-30 disabled:cursor-not-allowed" data-testid={`upgrade-variant-plus-${index}-${upg.id}-${v.id}`}>+</button>
                                                                </div>
                                                            </div>
                                                        );
                                                    })}
                                                    {upg.max && <div className="font-mono text-[10px] text-[#666] tracking-widest mt-1">MAX {upg.max} TOTAL</div>}
                                                </div>
                                            )}
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
