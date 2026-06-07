import axios from "axios";
import snapshot from "@/data/factions-snapshot.json";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

// Static snapshot bundled at build time. Used as a fallback when the FastAPI
// backend is unreachable (e.g. Vercel production deploys the frontend only).
const SNAPSHOT_SUMMARY = Array.isArray(snapshot?.summary?.factions) ? snapshot.summary.factions : [];
const SNAPSHOT_FULL = snapshot?.full && typeof snapshot.full === "object" ? snapshot.full : {};

const apiEnabled = typeof BACKEND_URL === "string" && BACKEND_URL.length > 0;

if (typeof window !== "undefined" && !apiEnabled) {
    console.warn("[eoa] REACT_APP_BACKEND_URL is empty — using bundled faction snapshot.");
}

export const fetchFactions = async () => {
    return SNAPSHOT_SUMMARY;
};

export const fetchFaction = async (factionId) => {
    return SNAPSHOT_FULL[factionId] || null;
};
