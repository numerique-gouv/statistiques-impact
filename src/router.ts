import Express from 'express';
import { DataSource } from 'typeorm';
import { buildIndicatorController } from './modules/indicator';
import { buildController } from './lib/buildController/buildController';
import { buildLogEntryController } from './modules/logEntry';
import { buildProductController } from './modules/product/product.controller';
import { buildClientController } from './modules/client';
import { buildAuthenticatedController } from './lib/buildController/buildAuthenticatedController';
import { fileUploadHandler } from './lib/fileUploadHandler';

function buildRouter(dataSource: DataSource) {
    const router = Express.Router();
    const indicatorController = buildIndicatorController(dataSource);
    const productController = buildProductController(dataSource);
    const logEntryController = buildLogEntryController(dataSource);
    const clientController = buildClientController(dataSource);

    router.post('/clients/token', buildController(clientController.createToken));
    router.post('/clients/:productName', buildController(clientController.createClient));

    router.get('/log-entries', buildController(logEntryController.getLogEntries));

    router.get('/indicators', buildController(indicatorController.getIndicators));
    router.get('/products', buildController(productController.getProducts));
    router.get(
        '/indicators/:name',
        buildController(indicatorController.getIndicatorsByProductName),
    );
    router.post(
        '/products/:productName/indicators',
        fileUploadHandler.uploadSingleFileMiddleware,
        buildAuthenticatedController(indicatorController.insertRawIndicators),
    );
    router.post('/indicators', buildController(indicatorController.upsertIndicators));
    router.delete('/indicators/:indicatorId', buildController(indicatorController.deleteIndicator));
    return router;
}

export { buildRouter };
