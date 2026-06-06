import { useState, useRef, useEffect } from "react";
import { Pencil, Check, X, AlertTriangle } from "lucide-react";

const POINT_PRESETS = [1000, 1500, 2000, 3000, 4000];

export default function PointsCapBar({ total, cap, counts, hasHorus, onCapChange }) {
    const [editing, setEditing] = useState(false);
    const [draft, setDraft] = useState(String(cap));
    const inputRef = useRef(null);

    useEffect(() => {
        if (editing && inputRef.current) {
            inputRef.current.focus();
            inputRef.current.select();
        }
    }, [editing]);

    const startEdit = () => {
        setDraft(String(cap));
        setEditing(true);
    };

    const pct = cap > 0 ? Math.min(100, Math.round((total / cap) * 100)) : 0;
    const over = total > cap;
    const approaching = !over && cap > 0 && total / cap >= 0.9;
    const remaining = cap - total;

    // State-driven colors
    let totalColor = "text-[#2D937D]";
    let barColor = "bg-[#2D937D]";
    if (over) {
        totalColor = "text-[#C2392E]";
        barColor = "bg-[#7F1D1D]";
    } else if (approaching) {
        totalColor = "text-[#C2A165]";
        barColor = "bg-[#C2A165]";
    }

    const commit = () => {
        const next = Math.max(100, Math.min(20000, Math.round(Number(draft) || 0)));
        if (next !== cap) onCapChange(next);
        setEditing(false);
    };
    const cancel = () => {
        setDraft(String(cap));
        setEditing(false);
    };
    const pickPreset = (p) => {
        setDraft(String(p));
        if (p !== cap) onCapChange(p);
        setEditing(false);
    };

    return (
        <div className="panel p-4 mb-6" data-testid="points-bar">
            <div className="flex items-center justify-between mb-2 gap-3 flex-wrap">
                <div className="font-mono text-[11px] tracking-[0.3em] text-[#888] uppercase">// Points Allocation</div>

                {editing ? (
                    <div className="flex items-center gap-2" data-testid="cap-editor">
                        <div className="flex gap-1 flex-wrap">
                            {POINT_PRESETS.map((p) => (
                                <button
                                    key={p}
                                    type="button"
                                    onClick={() => pickPreset(p)}
                                    className={`px-2 py-1 font-mono text-[10px] uppercase tracking-widest border ${Number(draft) === p ? "border-[#2D937D] text-[#2D937D]" : "border-[#333] text-[#888] hover:border-[#555]"}`}
                                    data-testid={`cap-preset-${p}`}
                                >
                                    {p}
                                </button>
                            ))}
                        </div>
                        <input
                            ref={inputRef}
                            type="number"
                            min="100"
                            step="50"
                            value={draft}
                            onChange={(e) => setDraft(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === "Enter") commit();
                                if (e.key === "Escape") cancel();
                            }}
                            className="w-24 bg-[#0E1411] border border-[#333] focus:border-[#2D937D] focus:outline-none px-2 py-1 font-mono text-sm text-[#E0E0E0]"
                            data-testid="cap-input"
                        />
                        <button onClick={commit} className="p-1 border border-[#2D937D] text-[#2D937D] hover:bg-[#2D937D]/10" data-testid="cap-save" aria-label="Save cap">
                            <Check className="w-4 h-4" />
                        </button>
                        <button onClick={cancel} className="p-1 border border-[#333] text-[#888] hover:border-[#555]" data-testid="cap-cancel" aria-label="Cancel cap edit">
                            <X className="w-4 h-4" />
                        </button>
                    </div>
                ) : (
                    <div className="flex items-center gap-2">
                        <div className={`font-display text-2xl tracking-tight ${totalColor}`} data-testid="points-total">
                            {total} <span className="text-[#666]">/ {cap}</span> <span className="text-xs text-[#888]">pts</span>
                        </div>
                        <button
                            onClick={startEdit}
                            className="p-1 border border-[#333] text-[#888] hover:border-[#2D937D] hover:text-[#2D937D] transition-colors"
                            data-testid="edit-cap-btn"
                            aria-label="Edit points cap"
                            title="Edit points cap"
                        >
                            <Pencil className="w-3.5 h-3.5" strokeWidth={2} />
                        </button>
                    </div>
                )}
            </div>

            <div className="h-2 bg-[#1A1A1A] overflow-hidden">
                <div className={`h-full transition-all duration-300 ${barColor}`} style={{ width: `${pct}%` }} data-testid="points-bar-fill" />
            </div>

            {/* Status line: over / approaching / remaining */}
            <div className="mt-2 min-h-[18px]">
                {over ? (
                    <div
                        className="inline-flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.25em] text-[#C2392E]"
                        data-testid="cap-warning-over"
                    >
                        <AlertTriangle className="w-3.5 h-3.5" strokeWidth={2} />
                        // Over Cap by {total - cap} pts
                    </div>
                ) : approaching ? (
                    <div className="font-mono text-[10px] uppercase tracking-[0.25em] text-[#C2A165]" data-testid="cap-warning-approaching">
                        // Approaching cap · {remaining} pts remaining
                    </div>
                ) : remaining === 0 && total > 0 ? (
                    <div className="font-mono text-[10px] uppercase tracking-[0.25em] text-[#2D937D]" data-testid="cap-status-exact">
                        // Cap reached exactly
                    </div>
                ) : (
                    <div className="font-mono text-[10px] uppercase tracking-[0.25em] text-[#666]" data-testid="cap-status-remaining">
                        // {remaining} pts remaining
                    </div>
                )}
            </div>

            <div className="flex flex-wrap gap-3 mt-3 font-mono text-[10px] uppercase tracking-widest text-[#888]">
                <span className="tag tag-green" data-testid="count-line">Line {counts.Line || 0}</span>
                <span className="tag" data-testid="count-support">Support {counts.Support || 0}</span>
                {counts["Lords of War"] ? (
                    <span className="tag" data-testid="count-lords-of-war">Lords of War {counts["Lords of War"]}</span>
                ) : null}
                {hasHorus && (
                    <span className="tag" style={{ color: "#C2A165", borderColor: "#C2A165" }} data-testid="count-primarch">
                        Primarch: Horus
                    </span>
                )}
            </div>
        </div>
    );
}
