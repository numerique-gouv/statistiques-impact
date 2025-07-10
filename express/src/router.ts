import Express from 'express';
import { DataSource } from 'typeorm';
import { buildIndicatorController } from './modules/indicator';
import { buildController } from './lib/buildController/buildController';
import { buildLogEntryController } from './modules/logEntry';
import { buildProductController } from './modules/product/product.controller';
import { buildClientController } from './modules/client';
import { buildAuthenticatedController } from './lib/buildController/buildAuthenticatedController';
import { fileUploadHandler } from './lib/fileUploadHandler';
import { buildAdminAuthenticatedController } from './lib/buildController/buildAdminAuthenticatedController';

function buildRouter(dataSource: DataSource) {
    const router = Express.Router();
    const indicatorController = buildIndicatorController(dataSource);
    const productController = buildProductController(dataSource);
    const logEntryController = buildLogEntryController(dataSource);
    const clientController = buildClientController(dataSource);

    router.post('/clients/token', buildAdminAuthenticatedController(clientController.createToken));
    router.patch(
        '/clients/:clientId/client-secret',
        buildAdminAuthenticatedController(clientController.updateClientSecret),
    );
    router.post(
        '/clients/:productName',
        buildAdminAuthenticatedController(clientController.createClient),
    );

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
    router.post(
        '/indicators',
        buildAdminAuthenticatedController(indicatorController.upsertIndicators),
    );
    router.delete(
        '/indicators/:indicatorId',
        buildAdminAuthenticatedController(indicatorController.deleteIndicator),
    );
    return router;
}

export { buildRouter };
