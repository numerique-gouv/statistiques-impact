import { config } from '../config';

const api = { fetchProducts, fetchTables };

type productRecordType = { id: number; fields: { Produit: string; slug: string; Equipe: number } };

async function fetchProducts() {
    const API_BASE_URL = `${config.GRIST_URL}/api/docs/${config.GRIST_DOCUMENT_ID}/tables/Produits/records`;
    const result = await fetch(API_BASE_URL, {
        headers: { Authorization: `Bearer ${config.GRIST_API_KEY}` },
    });
    const parsed: { records: Array<productRecordType> } = await result.json();
    return parsed.records;
}

async function fetchTables() {
    const API_BASE_URL = `${config.GRIST_URL}/api/docs/${config.GRIST_DOCUMENT_ID}/tables`;
    const result = await fetch(API_BASE_URL, {
        headers: { Authorization: `Bearer ${config.GRIST_API_KEY}` },
    });
    const parsed = await result.json();
    return parsed;
}

export { api };
