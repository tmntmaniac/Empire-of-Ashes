// LocalStorage based persistence for army lists.
const KEY = "eoa.armies.v1";

const read = () => {
    try {
        const raw = localStorage.getItem(KEY);
        if (!raw) return [];
        const arr = JSON.parse(raw);
        return Array.isArray(arr) ? arr : [];
    } catch (e) {
        return [];
    }
};

const write = (arr) => {
    localStorage.setItem(KEY, JSON.stringify(arr));
};

export const listArmies = () => read();

export const getArmy = (id) => read().find((a) => a.id === id) || null;

export const upsertArmy = (army) => {
    const arr = read();
    const idx = arr.findIndex((a) => a.id === army.id);
    const updated = { ...army, updatedAt: new Date().toISOString() };
    if (idx === -1) arr.push(updated);
    else arr[idx] = updated;
    write(arr);
    return updated;
};

export const deleteArmy = (id) => {
    write(read().filter((a) => a.id !== id));
};

export const duplicateArmy = (id) => {
    const a = getArmy(id);
    if (!a) return null;
    const copy = {
        ...a,
        id: crypto.randomUUID(),
        name: `${a.name} (Copy)`,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
    };
    const arr = read();
    arr.push(copy);
    write(arr);
    return copy;
};

export const newArmy = ({ name, factionId, pointsCap }) => ({
    id: crypto.randomUUID(),
    name,
    factionId,
    pointsCap: Number(pointsCap) || 3000,
    formations: [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
});
