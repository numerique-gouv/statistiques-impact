import Express from 'express';
import Joi from 'joi';
import { buildIndicatorController } from './modules/indicator';
import { buildController } from './lib/buildController';
import { buildProductController } from './modules/product';
import { DataSource } from 'typeorm';

function buildRouter(dataSource: DataSource) {
    const router = Express.Router();
    const indicatorController = buildIndicatorController(dataSource);
    const productController = buildProductController(dataSource);

    router.get('/indicators', buildController(indicatorController.getIndicators));
    router.delete('/indicators/:indicatorId', buildController(indicatorController.deleteIndicator));

    router.post(
        '/indicators',
        buildController(indicatorController.upsertIndicator, {
            schema: Joi.object({
                nom_service_public_numerique: Joi.string().required(),
                indicateur: Joi.string().required(),
                valeur: Joi.number().required(),
                unite_mesure: Joi.string().required(),
                frequence_calcul: Joi.string().required(),
                date: Joi.string()
                    .required()
                    .regex(/^\d{4}-\d{2}-\d{2}$/),
                est_periode: Joi.boolean().required(),
            }),
        }),
    );

    router.get('/products', buildController(productController.getProducts));
    router.post(
        '/products',
        buildController(productController.createProduct, {
            schema: Joi.object({
                name: Joi.string().required(),
            }),
        }),
    );
    return router;
}

export { buildRouter };
