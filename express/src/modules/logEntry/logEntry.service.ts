import { LogEntry } from './LogEntry.entity';
import { DataSource } from 'typeorm';

export { buildLogEntryService };

function buildLogEntryService(dataSource: DataSource) {
    const logEntryRepository = dataSource.getRepository(LogEntry);
    const logEntryService = {
        getLogEntries,
        insertLogEntry,
    };

    return logEntryService;

    async function getLogEntries() {
        return logEntryRepository.find();
    }

    async function insertLogEntry(description: string) {
        const logEntry = new LogEntry();

        logEntry.description = description;
        return logEntryRepository.insert(logEntry);
    }
}
