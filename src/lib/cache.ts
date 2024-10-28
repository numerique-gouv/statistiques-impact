import axios from 'axios';
import { dateHandler } from '../scripts/importStats/utils';

function buildCache() {
    let store: Record<string, string | undefined> = {};

    async function fetch<dataT>(url: string): Promise<dataT> {
        const dateKey = getDateKey();
        const completeKey = `${dateKey}-${url}`;
        if (store[completeKey] !== undefined) {
            return store[completeKey] as dataT;
        }
        const result = await axios.get<dataT>(url);
        store[completeKey] = JSON.stringify(result.data);
        return result.data;
    }

    return { fetch };
}

function getDateKey() {
    const parsedDate = dateHandler.parseDate(new Date());
    return dateHandler.stringifyParsedDate(parsedDate);
}

const cache = buildCache();

export { cache };
