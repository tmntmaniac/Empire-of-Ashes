import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchFactions } from "@/lib/api";
import { ArrowRight, Lock } from "lucide-react";

const LORE = "History records that it is the Sons of Horus Legion who lit the spark of rebellion and stood upon the ashes of the old Imperium. Ambition, ruthlessness, unbowed determination — Horus Lupercal's chosen carve their destiny across the stars.";

export default function Landing() {
    const [factions, setFactions] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchFactions()
            .then(setFactions)
            .catch(() => setFactions([]))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div data-testid="landing-page">
            {/* Hero */}
            <section className="relative overflow-hidden border-b border-[#222]">
                <div
                    className="absolute inset-0 opacity-[0.18]"
                    style={{
                        backgroundImage: "url('https://images.pexels.com/photos/7185968/pexels-photo-7185968.jpeg')",
                        backgroundSize: "cover",
                        backgroundPosition: "center",
                        filter: "grayscale(0.5) contrast(1.1)",
                    }}
                />
                <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#050505]/40 to-[#050505]" />
                <div className="relative max-w-7xl mx-auto px-6 py-24 sm:py-32">
                    <div className="max-w-3xl">
                        <div className="font-mono text-[11px] tracking-[0.4em] text-[#C2A165] uppercase mb-6" data-testid="hero-eyebrow">
                            // Encrypted Field Codex · Access Granted
                        </div>
                        <h1 className="font-display text-5xl sm:text-7xl uppercase leading-[0.92] tracking-tight mb-6" data-testid="hero-title">
                            Forge the<br />
                            <span className="text-[#2D937D]">Warmaster's</span> Legion
                        </h1>
                        <p className="text-base sm:text-lg text-[#B8B8B8] max-w-2xl leading-relaxed mb-10 font-sans" data-testid="hero-lore">
                            {LORE}
                        </p>
                        <div className="flex flex-wrap gap-3">
                            <Link to="/armies" className="btn-primary inline-flex items-center gap-2" data-testid="cta-build-army">
                                Forge a New Force <ArrowRight className="w-4 h-4" strokeWidth={2} />
                            </Link>
                            <Link to="/armies" className="btn-ghost" data-testid="cta-my-armies">
                                View Saved Lists
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* Faction picker */}
            <section className="max-w-7xl mx-auto px-6 py-16">
                <div className="flex items-end justify-between mb-8 border-b border-[#222] pb-4">
                    <div>
                        <div className="font-mono text-[11px] tracking-[0.3em] text-[#888] uppercase mb-2">// Legions Available</div>
                        <h2 className="font-display text-3xl sm:text-4xl uppercase tracking-tight">Choose Your Allegiance</h2>
                    </div>
                    <div className="font-mono text-xs text-[#666] uppercase tracking-widest hidden sm:block">{factions.length} legion{factions.length === 1 ? "" : "s"} online</div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {loading && (
                        <div className="panel p-8 col-span-full text-center text-[#666] font-mono uppercase tracking-widest text-sm" data-testid="factions-loading">
                            Loading dossiers...
                        </div>
                    )}
                    {!loading && factions.map((f) => (
                        <Link
                            key={f.id}
                            to={`/armies?new=${f.id}`}
                            className="panel panel-accent p-6 group relative overflow-hidden hover:border-[#2D937D] transition-colors"
                            data-testid={`faction-card-${f.id}`}
                        >
                            <div className="absolute top-0 right-0 px-2 py-1 font-mono text-[9px] tracking-widest uppercase text-[#050505] bg-[#2D937D]">Active</div>
                            <div className="font-mono text-[10px] tracking-[0.3em] text-[#C2A165] uppercase mb-2">{f.subtitle}</div>
                            <h3 className="font-display text-3xl uppercase tracking-tight mb-3 group-hover:text-[#2D937D] transition-colors">{f.name}</h3>
                            <div className="flex items-center justify-between mt-6 pt-4 border-t border-[#222]">
                                <span className="font-mono text-xs text-[#888] uppercase tracking-widest">Build →</span>
                                <ArrowRight className="w-4 h-4 text-[#2D937D] group-hover:translate-x-1 transition-transform" strokeWidth={2} />
                            </div>
                        </Link>
                    ))}
                    {/* Future armies teaser — all 18 Legiones Astartes are now live */}
                    <div className="panel p-6 opacity-50 cursor-not-allowed" data-testid="faction-card-coming-soon">
                        <div className="font-mono text-[10px] tracking-[0.3em] text-[#666] uppercase mb-2 flex items-center gap-2">
                            <Lock className="w-3 h-3" strokeWidth={2} /> Incoming
                        </div>
                        <h3 className="font-display text-3xl uppercase tracking-tight mb-3 text-[#555]">Auxiliary Forces</h3>
                        <p className="text-xs text-[#666] font-sans leading-relaxed">Mechanicum Taghmata, Solar Auxilia and Knight Households await transmission.</p>
                    </div>
                </div>
            </section>

            {/* Feature strip */}
            <section className="border-t border-[#222] bg-[#0A0C0B]">
                <div className="max-w-7xl mx-auto px-6 py-12 grid grid-cols-1 sm:grid-cols-3 gap-8">
                    {[
                        { k: "01", t: "Codex Stats", d: "All units rendered as monospace stat blocks pulled directly from the field manual." },
                        { k: "02", t: "Live Points", d: "Costs update in real time as you compose formations, upgrades and extra detachments." },
                        { k: "03", t: "Local Only", d: "No login. No cloud. Your lists never leave the device." },
                    ].map((it) => (
                        <div key={it.k} className="border-l-2 border-[#2D937D] pl-4" data-testid={`feature-${it.k}`}>
                            <div className="font-mono text-[10px] tracking-[0.4em] text-[#C2A165] uppercase mb-1">// {it.k}</div>
                            <h4 className="font-display text-xl uppercase tracking-tight mb-1">{it.t}</h4>
                            <p className="text-sm text-[#888] font-sans">{it.d}</p>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
}
