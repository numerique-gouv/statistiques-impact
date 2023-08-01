import Express from 'express';
import { buildIndicatorController } from './modules/indicator';
import { buildController } from './lib/buildController';
import { DataSource } from 'typeorm';
import { buildLogEntryController } from './modules/logEntry';

const DATE_REGEX = /^\d{4}-\d{2}-\d{2}$/;

function buildRouter(dataSource: DataSource) {
    const router = Express.Router();
    const indicatorController = buildIndicatorController(dataSource);
    const logEntryController = buildLogEntryController(dataSource);

    router.get('/log-entries', buildController(logEntryController.getLogEntries));

    router.get('/indicators', buildController(indicatorController.getIndicators));
    router.get(
        '/indicators/:name',
        buildController(indicatorController.getIndicatorsByProductName),
    );
    router.delete('/indicators/:indicatorId', buildController(indicatorController.deleteIndicator));

    return router;
}

export { buildRouter };
