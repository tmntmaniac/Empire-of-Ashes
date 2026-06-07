import { useEffect, useState } from "react";
import { fetchFaction } from "@/lib/api";

export function useFactionAsync(factionId) {
    const [faction, setFaction] = useState(null);

    useEffect(() => {
        let cancelled = false;

        if (!factionId) {
            setFaction(null);
            return;
        }

        fetchFaction(factionId)
            .then((f) => {
                if (!cancelled) setFaction(f);
            })
            .catch(() => {
                if (!cancelled) setFaction(null);
            });

        return () => {
            cancelled = true;
        };
    }, [factionId]);

    return faction;
}
