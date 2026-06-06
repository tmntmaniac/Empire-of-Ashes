import { AlertTriangle, ShieldCheck } from "lucide-react";

export default function ArmyValidationPanel({ result, hasFormations }) {
    if (!result) return null;
    const { valid, issues, stats } = result;

    // Don't render anything for a brand-new empty army (cleaner first-run UX)
    if (!hasFormations) return null;

    return (
        <div className="panel p-4 mb-6" data-testid="validation-panel">
            <div className="flex items-center justify-between mb-3 gap-3 flex-wrap">
                <div className="font-mono text-[11px] tracking-[0.3em] text-[#888] uppercase">// Force Composition</div>
                {valid ? (
                    <div className="inline-flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.25em] text-[#2D937D]" data-testid="validation-legal">
                        <ShieldCheck className="w-3.5 h-3.5" strokeWidth={2} />
                        // List Legal
                    </div>
                ) : (
                    <div className="inline-flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.25em] text-[#C2392E]" data-testid="validation-illegal">
                        <AlertTriangle className="w-3.5 h-3.5" strokeWidth={2} />
                        // {issues.length} Violation{issues.length === 1 ? "" : "s"}
                    </div>
                )}
            </div>

            {/* Composition counters */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-3">
                <CounterCell
                    testId="comp-line"
                    label="Line"
                    value={stats.lineCount}
                    sub={stats.lineCount === 0 ? "min 1" : null}
                    danger={hasFormations && stats.lineCount === 0}
                />
                <CounterCell
                    testId="comp-support"
                    label="Support"
                    value={stats.supportCount}
                    sub={`max ${stats.supportLimit}`}
                    danger={stats.supportCount > stats.supportLimit}
                />
                <CounterCell
                    testId="comp-low"
                    label="Lords of War"
                    value={`${stats.lowPoints} pts`}
                    sub={`max ${stats.lowLimit} pts (33%)`}
                    danger={stats.lowPoints > stats.lowLimit && stats.lowLimit > 0}
                />
                <CounterCell
                    testId="comp-primarch"
                    label="Primarch"
                    value={stats.primarchCount}
                    sub="max 1"
                    danger={stats.primarchCount > 1}
                />
            </div>

            {/* Issue list */}
            {issues.length > 0 && (
                <ul className="space-y-1.5" data-testid="validation-issues">
                    {issues.map((iss, i) => (
                        <li
                            key={`${iss.code}-${i}`}
                            className="flex items-start gap-2 text-xs font-sans text-[#E5B4B0] border-l-2 border-[#C2392E] pl-2 py-1 bg-[#C2392E]/5"
                            data-testid={`validation-issue-${iss.code}`}
                        >
                            <AlertTriangle className="w-3.5 h-3.5 mt-0.5 shrink-0 text-[#C2392E]" strokeWidth={2} />
                            <span>{iss.message}</span>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

function CounterCell({ label, value, sub, danger, testId }) {
    return (
        <div
            className={`border px-3 py-2 ${danger ? "border-[#C2392E] bg-[#C2392E]/5" : "border-[#222] bg-[#0A0C0B]"}`}
            data-testid={testId}
        >
            <div className="font-mono text-[9px] tracking-[0.3em] uppercase text-[#888]">{label}</div>
            <div className={`font-display text-xl tracking-tight ${danger ? "text-[#C2392E]" : "text-[#E0E0E0]"}`} data-testid={`${testId}-value`}>
                {value}
            </div>
            {sub && <div className="font-mono text-[9px] uppercase tracking-widest text-[#666] mt-0.5">{sub}</div>}
        </div>
    );
}
