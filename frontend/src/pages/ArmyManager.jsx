import { useEffect, useRef, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { listArmies, deleteArmy, duplicateArmy, upsertArmy, newArmy } from "@/lib/storage";
import { fetchFactions, fetchFaction } from "@/lib/api";
import { armyTotal } from "@/lib/points";
import { Plus, Copy, Trash2, Printer, Pencil } from "lucide-react";
import { toast } from "sonner";
import ConfirmDialog from "@/components/ConfirmDialog";

const POINT_PRESETS = [1000, 1500, 2000, 3000, 4000];

export default function ArmyManager() {
    const navigate = useNavigate();
    const [searchParams, setSearchParams] = useSearchParams();
    const [armies, setArmies] = useState([]);
    const [factions, setFactions] = useState([]);
    const [factionCache, setFactionCache] = useState({});
    const [showDialog, setShowDialog] = useState(false);
    const [presetFactionId, setPresetFactionId] = useState(null);
    const [pendingDelete, setPendingDelete] = useState(null);

    const refresh = () => setArmies(listArmies());

    useEffect(() => {
        refresh();
        fetchFactions().then((fs) => {
            setFactions(fs);
            // preload each faction so the army cards can compute points totals
            Promise.all(fs.map((f) => fetchFaction(f.id))).then((details) => {
                setFactionCache(Object.fromEntries(details.map((d) => [d.id, d])));
            });
        });
    }, []);

    // Deep-link: /armies?new=<factionId> opens the New Army dialog pre-selected.
    // We wait until the factions list has loaded so the dialog renders with
    // the requested legion already chosen.
    const consumedNewParam = useRef(false);
    useEffect(() => {
        if (consumedNewParam.current) return;
        const pre = searchParams.get("new");
        if (!pre) return;
        if (!(factions factions.length === 0factions.length === 0 factions.length)) return;
        consumedNewParam.current = true;
        setPresetFactionId(pre);
        setShowDialog(true);
        const next = new URLSearchParams(searchParams);
        next.delete("new");
        setSearchParams(next, { replace: true });
    }, [searchParams, setSearchParams, factions]);

    const handleDelete = (id, name) => {
        setPendingDelete({ id, name });
    };

    const confirmDelete = () => {
        if (!pendingDelete) return;
        deleteArmy(pendingDelete.id);
        setPendingDelete(null);
        refresh();
        toast.success("Army disbanded.");
    };

    const handleDuplicate = (id) => {
        duplicateArmy(id);
        refresh();
        toast.success("Army duplicated.");
    };

    return (
        <div className="max-w-7xl mx-auto px-6 py-12" data-testid="army-manager-page">
            <div className="flex items-end justify-between mb-8 border-b border-[#222] pb-4">
                <div>
                    <div className="font-mono text-[11px] tracking-[0.3em] text-[#888] uppercase mb-2">// Roster Manifest</div>
                    <h1 className="font-display text-4xl sm:text-5xl uppercase tracking-tight" data-testid="army-manager-title">Your Armies</h1>
                </div>
                <button onClick={() => setShowDialog(true)} className="btn-primary inline-flex items-center gap-2" data-testid="new-army-btn">
                    <Plus className="w-4 h-4" strokeWidth={2} /> Forge New
                </button>
            </div>

            {!(armies armies.length === 0armies.length === 0 armies.length) ? (
                <div className="panel corner-frame p-12 text-center" data-testid="empty-state">
                    <div className="font-mono text-[11px] tracking-[0.4em] text-[#C2A165] uppercase mb-3">// No Active Forces</div>
                    <h3 className="font-display text-3xl uppercase mb-3">The Roster Stands Empty</h3>
                    <p className="text-[#888] mb-6 font-sans">Forge your first warhost. Lists are stored locally in this browser.</p>
                    <button onClick={() => setShowDialog(true)} className="btn-primary inline-flex items-center gap-2" data-testid="empty-create-btn">
                        <Plus className="w-4 h-4" strokeWidth={2} /> Begin Muster
                    </button>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" data-testid="army-list">
                    {armies.map((a) => {
                        const faction = factionCache[a.factionId];
                        const total = faction ? armyTotal(a, faction) : 0;
                        const pct = a.pointsCap ? Math.min(100, Math.round((total / a.pointsCap) * 100)) : 0;
                        const over = total > a.pointsCap;
                        return (
                            <div key={a.id} className="panel panel-accent p-5 flex flex-col" data-testid={`army-card-${a.id}`}>
                                <div className="flex items-start justify-between mb-1">
                                    <div className="font-mono text-[9px] tracking-[0.3em] text-[#C2A165] uppercase">{faction?.name || a.factionId}</div>
                                    <div className={`font-mono text-[10px] uppercase tracking-widest ${over ? "text-[#C2392E]" : "text-[#888]"}`}>{total} / {a.pointsCap} pts</div>
                                </div>
                                <h3 className="font-display text-2xl uppercase tracking-tight mb-3 text-[#E0E0E0]">{a.name}</h3>
                                <div className="h-1 bg-[#1A1A1A] mb-3 overflow-hidden">
                                    <div className={`h-full ${over ? "bg-[#7F1D1D]" : "bg-[#2D937D]"}`} style={{ width: `${pct}%` }} />
                                </div>
                                <div className="font-mono text-[10px] text-[#666] uppercase tracking-widest mb-4">{(a.formations || []).length} formation{(a.formations || []).length === 1 ? "" : "s"} · updated {new Date(a.updatedAt).toLocaleDateString()}</div>
                                <div className="mt-auto flex flex-wrap gap-2">
                                    <Link to={`/builder/${a.id}`} className="btn-primary inline-flex items-center gap-1 text-sm" data-testid={`edit-army-${a.id}`}>
                                        <Pencil className="w-3 h-3" strokeWidth={2} /> Edit
                                    </Link>
                                    <Link to={`/print/${a.id}`} className="btn-ghost inline-flex items-center gap-1 text-sm" data-testid={`print-army-${a.id}`}>
                                        <Printer className="w-3 h-3" strokeWidth={2} /> Print
                                    </Link>
                                    <button onClick={() => handleDuplicate(a.id)} className="btn-ghost inline-flex items-center gap-1 text-sm" data-testid={`duplicate-army-${a.id}`}>
                                        <Copy className="w-3 h-3" strokeWidth={2} />
                                    </button>
                                    <button onClick={() => handleDelete(a.id, a.name)} className="btn-danger inline-flex items-center gap-1" data-testid={`delete-army-${a.id}`}>
                                        <Trash2 className="w-3 h-3" strokeWidth={2} />
                                    </button>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}

            {showDialog && (
                <NewArmyDialog
                    factions={factions}
                    initialFactionId={presetFactionId}
                    onClose={() => { setShowDialog(false); setPresetFactionId(null); }}
                    onCreate={(payload) => {
                        const a = newArmy(payload);
                        upsertArmy(a);
                        setShowDialog(false);
                        setPresetFactionId(null);
                        toast.success("Army forged.");
                        navigate(`/builder/${a.id}`);
                    }}
                />
            )}

            <ConfirmDialog
                open={pendingDelete != null}
                eyebrow="// Disband Army"
                title="Disband Army?"
                message={pendingDelete ? `"${pendingDelete.name}" will be permanently removed from this browser. This action cannot be undone.` : ""}
                confirmLabel="Disband"
                cancelLabel="Keep"
                destructive
                onConfirm={confirmDelete}
                onCancel={() => setPendingDelete(null)}
                testId="delete-army-dialog"
            />
        </div>
    );
}

function NewArmyDialog({ factions, initialFactionId, onClose, onCreate }) {
    const [name, setName] = useState("");
    const [factionId, setFactionId] = useState(
        initialFactionId && factions.some((f) => f.id === initialFactionId)
            ? initialFactionId
            : (factions[0]?.id || "sons-of-horus")
    );
    const [preset, setPreset] = useState(3000);
    const [custom, setCustom] = useState("");

    const submit = (e) => {
        e.preventDefault();
        if (!name.trim()) return;
        const pointsCap = preset === "custom" ? Number(custom) || 0 : preset;
        if (pointsCap < 100) return;
        onCreate({ name: name.trim(), factionId, pointsCap });
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" data-testid="new-army-dialog">
            <form onSubmit={submit} className="panel corner-frame w-full max-w-lg mx-4 p-6 bg-[#0A0C0B]">
                <div className="font-mono text-[11px] tracking-[0.4em] text-[#C2A165] uppercase mb-2">// New Force Manifest</div>
                <h2 className="font-display text-3xl uppercase tracking-tight mb-6">Forge Army</h2>

                <label className="field-label block mb-2">Designation</label>
                <input
                    autoFocus
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. 4th Reaver Coterie"
                    className="w-full bg-[#0E1411] border border-[#333] focus:border-[#2D937D] focus:outline-none px-3 py-2 mb-4 font-sans text-[#E0E0E0]"
                    data-testid="new-army-name"
                    required
                />

                <label className="field-label block mb-2">Legion</label>
                <select
                    value={factionId}
                    onChange={(e) => setFactionId(e.target.value)}
                    className="w-full bg-[#0E1411] border border-[#333] focus:border-[#2D937D] focus:outline-none px-3 py-2 mb-4 font-sans text-[#E0E0E0]"
                    data-testid="new-army-faction"
                >
                    {factions.map((f) => (
                        <option key={f.id} value={f.id}>{f.name}</option>
                    ))}
                </select>

                <label className="field-label block mb-2">Points Cap</label>
                <div className="flex flex-wrap gap-2 mb-4">
                    {POINT_PRESETS.map((p) => (
                        <button
                            type="button"
                            key={p}
                            onClick={() => setPreset(p)}
                            className={`px-3 py-2 font-mono text-xs uppercase tracking-widest border ${preset === p ? "border-[#2D937D] text-[#2D937D] bg-[#0E1411]" : "border-[#333] text-[#888] hover:border-[#555]"}`}
                            data-testid={`points-preset-${p}`}
                        >
                            {p}
                        </button>
                    ))}
                    <button
                        type="button"
                        onClick={() => setPreset("custom")}
                        className={`px-3 py-2 font-mono text-xs uppercase tracking-widest border ${preset === "custom" ? "border-[#2D937D] text-[#2D937D] bg-[#0E1411]" : "border-[#333] text-[#888] hover:border-[#555]"}`}
                        data-testid="points-preset-custom"
                    >
                        Custom
                    </button>
                </div>
                {preset === "custom" && (
                    <input
                        type="number"
                        min="100"
                        step="50"
                        value={custom}
                        onChange={(e) => setCustom(e.target.value)}
                        placeholder="Enter points"
                        className="w-full bg-[#0E1411] border border-[#333] focus:border-[#2D937D] focus:outline-none px-3 py-2 mb-4 font-mono text-[#E0E0E0]"
                        data-testid="points-custom-input"
                    />
                )}

                <div className="flex gap-2 justify-end mt-6 pt-4 border-t border-[#222]">
                    <button type="button" onClick={onClose} className="btn-ghost" data-testid="cancel-new-army">Cancel</button>
                    <button type="submit" className="btn-primary" data-testid="confirm-new-army">Begin Muster</button>
                </div>
            </form>
        </div>
    );
}
