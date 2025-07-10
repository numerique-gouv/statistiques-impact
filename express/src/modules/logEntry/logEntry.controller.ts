import { DataSource } from 'typeorm';
import { buildLogEntryService } from './logEntry.service';

export { buildLogEntryController };

function buildLogEntryController(dataSource: DataSource) {
    const indicatorService = buildLogEntryService(dataSource);
    const indicatorController = {
        getLogEntries,
    };

    return indicatorController;

    async function getLogEntries() {
        return indicatorService.getLogEntries();
    }
}
