// URL-safe base64 encoding of an army payload, used to pass roster state
// across a browser-tab boundary when the source tab is inside an iframe whose
// localStorage is partitioned away from the new top-level tab.
const toUrlSafe = (b64) => b64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const fromUrlSafe = (s) => {
    const pad = s.length % 4 === 0 ? "" : "=".repeat(4 - (s.length % 4));
    return s.replace(/-/g, "+").replace(/_/g, "/") + pad;
};

export const encodeArmy = (army) => {
    try {
        const json = JSON.stringify(army);
        const bytes = new TextEncoder().encode(json);
        let bin = "";
        bytes.forEach((b) => { bin += String.fromCharCode(b); });
        return toUrlSafe(btoa(bin));
    } catch {
        return "";
    }
};

export const decodeArmy = (encoded) => {
    if (!encoded) return null;
    try {
        const bin = atob(fromUrlSafe(encoded));
        const bytes = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
        const json = new TextDecoder().decode(bytes);
        const parsed = JSON.parse(json);
        return parsed && typeof parsed === "object" && parsed.id ? parsed : null;
    } catch {
        return null;
    }
};
