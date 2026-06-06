import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const fetchFactions = async () => {
    const { data } = await axios.get(`${API}/factions`);
    return data.factions;
};

export const fetchFaction = async (factionId) => {
    const { data } = await axios.get(`${API}/factions/${factionId}`);
    return data;
};
