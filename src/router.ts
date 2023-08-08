import Express from 'express';
import { DataSource } from 'typeorm';
import { buildIndicatorController } from './modules/indicator';
import { buildController } from './lib/buildController';
import { buildLogEntryController } from './modules/logEntry';
import { buildProductController } from './modules/product/product.controller';

function buildRouter(dataSource: DataSource) {
    const router = Express.Router();
    const indicatorController = buildIndicatorController(dataSource);
    const productController = buildProductController(dataSource);
    const logEntryController = buildLogEntryController(dataSource);

    router.get('/log-entries', buildController(logEntryController.getLogEntries));

    router.get('/indicators', buildController(indicatorController.getIndicators));
    router.get('/products', buildController(productController.getProducts));
    router.get(
        '/indicators/:name',
        buildController(indicatorController.getIndicatorsByProductName),
    );
    router.delete('/indicators/:indicatorId', buildController(indicatorController.deleteIndicator));

    return router;
}

export { buildRouter };
