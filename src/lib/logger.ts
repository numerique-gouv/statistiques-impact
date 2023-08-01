import { dataSource } from '../dataSource';
import { buildLogEntryService } from '../modules/logEntry';

const logger = buildLogger();

function buildLogger() {
    const logEntryService = buildLogEntryService(dataSource);
    return { error };

    async function error({
        productName,
        indicator,
        message,
    }: {
        productName: string;
        indicator?: string;
        message: string;
    }) {
        const description = `${productName} - ${indicator || ''} - ${message}`;
        console.warn(description);
        await logEntryService.insertLogEntry(description);
    }
}

export { logger };
