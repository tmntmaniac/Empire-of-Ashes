import { Outlet, Link, useLocation } from "react-router-dom";
import { Skull } from "lucide-react";

export default function Layout() {
    const { pathname } = useLocation();
    const isActive = (p) => (pathname === p ? "text-[#2D937D]" : "text-[#E0E0E0] hover:text-[#2D937D]");
    return (
        <div className="min-h-screen flex flex-col" data-testid="app-shell">
            <header className="border-b border-[#222] bg-[#080A09]/95 backdrop-blur sticky top-0 z-40">
                <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
                    <Link to="/" className="flex items-center gap-3" data-testid="nav-home">
                        <div className="w-8 h-8 border border-[#C2A165] flex items-center justify-center">
                            <Skull className="w-4 h-4 text-[#C2A165]" strokeWidth={1.5} />
                        </div>
                        <div className="leading-none">
                            <div className="font-display text-2xl tracking-tight uppercase">Empire of Ashes</div>
                            <div className="font-mono text-[10px] tracking-[0.25em] text-[#888] uppercase">Force Codex // v0.1</div>
                        </div>
                    </Link>
                    <nav className="flex items-center gap-6 text-sm uppercase tracking-wider font-display">
                        <Link to="/" className={isActive("/")} data-testid="nav-link-home">Home</Link>
                        <Link to="/armies" className={isActive("/armies")} data-testid="nav-link-armies">My Armies</Link>
                    </nav>
                </div>
                <div className="h-[2px] stripe-warning opacity-50" />
            </header>
            <main className="flex-1">
                <Outlet />
            </main>
            <footer className="border-t border-[#222] mt-16">
                <div className="max-w-7xl mx-auto px-6 py-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs font-mono text-[#666] uppercase tracking-widest">
                    <span>// Fan-made tactical codex · Empire of Ashes</span>
                    <div className="flex items-center gap-4">
                        <Link to="/legal/impressum" className="hover:text-[#C2A165]">Impressum</Link>
                        <Link to="/legal/datenschutz" className="hover:text-[#C2A165]">Datenschutz</Link>
                    </div>
                    <span>Lists saved locally to your device.</span>
                </div>
                <div className="max-w-7xl mx-auto px-6 pb-6 text-center text-[10px] text-[#555] leading-relaxed">
                    This website is unofficial and in no way endorsed by Games Workshop.<br />
                    Any use of terms from Games Workshop are used without permission. No challenge to their status intended. All rights reserved to their respective owners.
                </div>
            </footer>
        </div>
    );
}
