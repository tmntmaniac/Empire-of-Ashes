import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { toast } from "sonner";
import { getArmy } from "@/lib/storage";
import { useFactionAsync } from "@/lib/useFactionAsync";
import { armyTotal, formationCost } from "@/lib/points";
import { encodeArmy, decodeArmy } from "@/lib/share";
import { Printer, ArrowLeft, Download, ExternalLink } from "lucide-react";

// Detect whether we're loaded inside a cross-origin iframe (e.g. the Emergent
// preview frame). In that context the browser silently blocks window.print(),
// file-download triggers, and other top-level chrome APIs.
function detectIframe() {
    try {
        return window.top !== window.self;
    } catch {
        // Cross-origin parent → accessing window.top throws → definitely in an iframe.
        return true;
    }
}

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
    const [army] = useState(() => {
        // Prefer URL-embedded payload (used when opening the roster in a new
        // top-level tab from the Emergent preview iframe — its localStorage is
        // partitioned away from the new tab).
        try {
            const params = new URLSearchParams(window.location.search);
            const encoded = params.get("a");
            if (encoded) {
                const decoded = decodeArmy(encoded);
                if (decoded && (!id || decoded.id === id)) return decoded;
            }
        } catch {
            // ignore — fall back to localStorage
        }
        return getArmy(id);
    });
    const faction = useFactionAsync(army?.factionId);
    const [savingPdf, setSavingPdf] = useState(false);
    const printableRef = useRef(null);
    const inIframe = useMemo(detectIframe, []);

    // Pick up the action the user requested in the OTHER (iframe) tab. We do
    // NOT auto-trigger it because browsers strip transient user activation
    // across the tab boundary — instead we render a prominent prompt that the
    // user clicks once. That single click carries a real user gesture, so
    // window.print() / file downloads succeed reliably.
    const [pendingAction, setPendingAction] = useState(() => {
        try {
            const a = new URLSearchParams(window.location.search).get("action");
            return a === "print" || a === "pdf" ? a : null;
        } catch {
            return null;
        }
    });

    // Once the army has been hydrated from the URL, strip the long `?a=`
    // payload AND the `?action=` marker so the address bar stays clean and a
    // refresh does not re-trigger the action prompt.
    useEffect(() => {
        if (!army) return;
        try {
            const params = new URLSearchParams(window.location.search);
            let mutated = false;
            if (params.has("a")) { params.delete("a"); mutated = true; }
            if (params.has("action")) { params.delete("action"); mutated = true; }
            if (!mutated) return;
            const qs = params.toString();
            const newUrl = window.location.pathname + (qs ? `?${qs}` : "") + window.location.hash;
            window.history.replaceState(null, "", newUrl);
        } catch {
            // ignore — non-fatal cosmetic concern
        }
    }, [army]);

    const safeFilename = useMemo(() => {
        const cleaned = (army?.name || "field-roster")
            .trim()
            .replace(/[^a-z0-9-_ ]/gi, "")
            .replace(/\s+/g, "-")
            .toLowerCase();
        return cleaned || "field-roster";
    }, [army?.name]);

    const openInNewTab = (action) => {
        // localStorage is partitioned per top-level site in modern browsers,
        // so the new tab won't see armies saved while inside the preview
        // iframe. Serialize the army payload into the URL itself so the new
        // tab can hydrate without depending on shared storage. An optional
        // `action` triggers the same export (print/pdf) automatically in the
        // new tab so the user only has to click once.
        const encoded = army ? encodeArmy(army) : "";
        const qs = new URLSearchParams();
        qs.set("fullscreen", "1");
        if (encoded) qs.set("a", encoded);
        if (action) qs.set("action", action);
        const url = `${window.location.pathname}?${qs.toString()}`;
        const win = window.open(url, "_blank", "noopener");
        if (!win) {
            toast.error("Pop-up blocked", {
                description: "Allow pop-ups for this site, or copy the URL into a new tab manually.",
            });
        }
    };

    const handlePrint = () => {
        if (inIframe) {
            toast.message("Opening roster in a new tab…", {
                description: "Print is blocked inside the Emergent preview frame. The print dialog will appear automatically in the new tab.",
            });
            openInNewTab("print");
            return;
        }
        // Detect a silently-blocked print() (sandboxed pop-up, mobile browser
        // without print support, embedded webview, etc.) by listening for the
        // `beforeprint` event. If it doesn't fire within 1.2s, the browser
        // never actually opened the dialog and we tell the user how to recover.
        let beforeFired = false;
        const onBefore = () => { beforeFired = true; };
        window.addEventListener("beforeprint", onBefore, { once: true });

        toast.message("Opening print dialog…", {
            description: "Choose 'Save as PDF' as the destination if you'd rather save a file.",
        });
        // Synchronous call keeps the user-gesture token alive across browsers.
        window.print();

        window.setTimeout(() => {
            window.removeEventListener("beforeprint", onBefore);
            if (beforeFired) return;
            toast.error("Browser blocked the print dialog", {
                description:
                    "This tab still has sandbox restrictions. Copy this page's URL, paste it into a brand-new browser tab (not via Emergent's pop-up), then press Ctrl/Cmd+P.",
                duration: 12000,
            });
        }, 1200);
    };

    const handleSavePdf = async () => {
        if (inIframe) {
            toast.message("Opening roster in a new tab…", {
                description: "PDF downloads are blocked inside the Emergent preview frame. The download will start automatically in the new tab.",
            });
            openInNewTab("pdf");
            return;
        }
        if (!printableRef.current || savingPdf) return;
        setSavingPdf(true);
        const t = toast.loading("Generating PDF…");
        // Pre-open a blank window synchronously while we still own the user
        // gesture. We'll either close it (download path succeeded) or fill it
        // with the rendered PDF blob (download path was suppressed by the
        // browser sandbox). This guarantees the user gets the PDF one way or
        // the other instead of seeing a fake "downloaded" toast with no file.
        const fallbackWin = window.open("", "_blank");
        if (fallbackWin) {
            try {
                fallbackWin.document.write(
                    "<title>Generating PDF…</title><style>body{background:#080A09;color:#C2A165;font-family:monospace;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;letter-spacing:.3em;text-transform:uppercase;font-size:12px}</style><body>// Generating PDF…</body>"
                );
            } catch {
                // ignore — sandbox may forbid document.write
            }
        }
        try {
            // Dynamic import keeps the ~150KB pdf bundle out of the landing critical path.
            const html2pdf = (await import("html2pdf.js")).default;
            // We need the rendered jsPDF instance so we can both attempt the
            // direct .save() (preferred — gives a clean Downloads-folder file)
            // AND fall back to a blob URL if that download silently fails.
            const worker = html2pdf()
                .set({
                    margin: 10,
                    filename: `${safeFilename}-roster.pdf`,
                    image: { type: "jpeg", quality: 0.95 },
                    html2canvas: {
                        scale: 3,
                        backgroundColor: "#ffffff",
                        useCORS: true,
                        // html2canvas rasterizes the live DOM and does NOT
                        // apply @media print styles — so the on-screen grey
                        // palette would bleed into the PDF and become
                        // illegible on paper. Walk EVERY element in the
                        // cloned document (html2pdf wraps the source element
                        // in extra containers before this hook runs, so we
                        // can't reliably scope by data-testid) and force pure
                        // black text on a pure white page. Inline styles win
                        // the cascade against Tailwind utility classes.
                        onclone: (clonedDoc) => {
                            const win = clonedDoc.defaultView || window;
                            clonedDoc.documentElement.style.background = "#ffffff";
                            if (clonedDoc.body) clonedDoc.body.style.background = "#ffffff";
                            const all = clonedDoc.querySelectorAll("body *");
                            all.forEach((el) => {
                                if (el.classList && el.classList.contains("no-print")) {
                                    el.style.display = "none";
                                    return;
                                }
                                el.style.color = "#000000";
                                el.style.textShadow = "none";
                                el.style.boxShadow = "none";
                                el.style.opacity = "1";
                                el.style.filter = "none";
                                try {
                                    const cs = win.getComputedStyle(el);
                                    const bg = cs.backgroundColor;
                                    if (bg && bg !== "rgba(0, 0, 0, 0)" && bg !== "transparent") {
                                        el.style.backgroundColor = "#ffffff";
                                    }
                                    const bw =
                                        parseFloat(cs.borderTopWidth || "0") +
                                        parseFloat(cs.borderBottomWidth || "0") +
                                        parseFloat(cs.borderLeftWidth || "0") +
                                        parseFloat(cs.borderRightWidth || "0");
                                    if (bw > 0) el.style.borderColor = "#000000";
                                    // Bump thin font weights to medium so the
                                    // anti-aliased strokes don't look washed
                                    // out at small sizes on paper.
                                    const fw = parseInt(cs.fontWeight || "400", 10);
                                    if (fw && fw < 500) el.style.fontWeight = "500";
                                } catch {
                                    // ignore — best-effort styling
                                }
                            });
                        },
                    },
                    jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
                    pagebreak: { mode: ["css", "legacy"], avoid: ["[data-testid^='print-formation-']", ".print-keep"] },
                })
                .from(printableRef.current);

            // Render once, then drive two outputs from the same jsPDF instance.
            const pdf = await worker.toPdf().get("pdf");
            const blobUrl = pdf.output("bloburl");

            // Try the standard direct-download path first.
            pdf.save(`${safeFilename}-roster.pdf`);

            // If the browser actually started the download, close the fallback
            // window. Otherwise (sandboxed), navigate it to the blob URL so the
            // user gets the rendered PDF rendered inline (Ctrl/Cmd+S to save).
            // We can't reliably detect download-success, so always offer the
            // fallback link in the toast — the user can click it if no file
            // appears in Downloads.
            if (fallbackWin && !fallbackWin.closed) {
                try {
                    fallbackWin.location.href = blobUrl;
                } catch {
                    // ignore
                }
            }
            toast.success("PDF ready", {
                id: t,
                description:
                    "If no file appeared in your Downloads folder, use the PDF tab that just opened — press Ctrl/Cmd+S to save it locally.",
                duration: 10000,
            });
        } catch (err) {
            console.error("PDF export failed", err);
            if (fallbackWin && !fallbackWin.closed) {
                try { fallbackWin.close(); } catch { /* ignore */ }
            }
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

    const runPendingAction = () => {
        const action = pendingAction;
        setPendingAction(null);
        if (action === "print") {
            // Use handlePrint so the silent-block detection runs here too.
            handlePrint();
        } else if (action === "pdf") {
            handleSavePdf();
        }
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
                {!inIframe && pendingAction && (
                    <div
                        className="no-print fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-sm px-6"
                        data-testid="action-prompt-overlay"
                    >
                        <div className="max-w-md w-full border-2 border-[#C2A165] bg-[#080A09] p-8 text-center">
                            <div className="font-mono text-[10px] tracking-[0.4em] text-[#C2A165] uppercase mb-3">
                                // {pendingAction === "print" ? "Ready to print" : "Ready to download"}
                            </div>
                            <h2 className="font-display text-3xl uppercase tracking-tight mb-3">
                                {pendingAction === "print" ? "Press to open print dialog" : "Press to save PDF"}
                            </h2>
                            <p className="text-sm text-[#888] mb-6">
                                Your browser requires a click in this tab before it will
                                {pendingAction === "print" ? " show the print dialog." : " download the file."}
                            </p>
                            <button
                                type="button"
                                onClick={runPendingAction}
                                autoFocus
                                className="btn-primary inline-flex items-center gap-2 text-base px-6 py-3"
                                data-testid="action-prompt-confirm"
                            >
                                {pendingAction === "print"
                                    ? (<><Printer className="w-5 h-5" /> Start Print</>)
                                    : (<><Download className="w-5 h-5" /> Download PDF</>)}
                            </button>
                            <div className="mt-4">
                                <button
                                    type="button"
                                    onClick={() => setPendingAction(null)}
                                    className="font-mono text-[10px] tracking-[0.3em] uppercase text-[#666] hover:text-[#999]"
                                    data-testid="action-prompt-cancel"
                                >
                                    Cancel — just show the roster
                                </button>
                            </div>
                        </div>
                    </div>
                )}
                {inIframe && (
                    <div className="no-print mb-6 p-4 border border-[#7F1D1D] bg-[#7F1D1D]/10" data-testid="iframe-banner">
                        <div className="flex items-start gap-3 flex-wrap">
                            <div className="flex-1 min-w-[280px]">
                                <div className="font-mono text-[10px] tracking-[0.3em] text-[#7F1D1D] uppercase mb-1">// Preview frame detected</div>
                                <p className="text-sm text-[#E0E0E0]">
                                    Print and PDF download are blocked inside the Emergent preview window for security reasons.
                                    Use one of the options below — the second one always works even when Emergent's pop-ups inherit the same restrictions.
                                </p>
                            </div>
                            <div className="flex flex-col gap-2">
                                <button
                                    type="button"
                                    onClick={() => openInNewTab()}
                                    className="btn-primary inline-flex items-center gap-2"
                                    data-testid="open-fullscreen-btn"
                                >
                                    <ExternalLink className="w-4 h-4" /> Open in New Tab
                                </button>
                                <button
                                    type="button"
                                    onClick={() => {
                                        const encoded = army ? encodeArmy(army) : "";
                                        const u = `${window.location.origin}${window.location.pathname}?fullscreen=1${encoded ? `&a=${encoded}` : ""}`;
                                        if (navigator.clipboard?.writeText) {
                                            navigator.clipboard.writeText(u).then(
                                                () => toast.success("Roster URL copied", {
                                                    description: "Open a fresh browser tab (Ctrl/Cmd+T), paste (Ctrl/Cmd+V) and press Enter. Print + PDF will work from there.",
                                                    duration: 10000,
                                                }),
                                                () => toast.error("Couldn't copy URL — select the address-bar URL and copy it manually."),
                                            );
                                        } else {
                                            window.prompt("Copy this URL, then paste it into a fresh browser tab:", u);
                                        }
                                    }}
                                    className="btn-secondary inline-flex items-center gap-2 text-sm"
                                    data-testid="copy-roster-url-btn"
                                >
                                    📋 Copy URL (paste in a fresh tab)
                                </button>
                            </div>
                        </div>
                    </div>
                )}
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
