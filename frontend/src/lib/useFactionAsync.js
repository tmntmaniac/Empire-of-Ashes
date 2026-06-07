import { useEffect, useState } from "react";
import { fetchFaction } from "@/lib/api";

/**
 * Custom hook to load a faction asynchronously by id.
 * Returns null while loading or if the request fails.
 *
 * Uses empty deps because factionId on a single route lifecycle is
 * effectively page-stable — the route parameter does not mutate without a
 * full remount.
 */
export function useFactionAsync(factionId) {
    const [faction, setFaction] = useState(null);
    useEffect(() => {
        let cancelled = false;
        if (!factionId) return;
        fetchFaction(factionId)
            .then((f) => { if (!cancelled) setFaction(f); })
            .catch(() => { if (!cancelled) setFaction(null); });
    }, []);
    return faction;
}
