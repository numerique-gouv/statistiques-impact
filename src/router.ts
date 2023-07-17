import Express from 'express';
import { buildIndicatorController } from './modules/indicator';
import { buildController } from './lib/buildController';
import Joi from 'joi';

const router = Express.Router();
const indicatorController = buildIndicatorController();

router.get('/', (req, res) => {
    res.send('Hello world!');
});

router.get('/indicators', buildController(indicatorController.getIndicators));

router.post(
    '/indicators',
    buildController(indicatorController.createIndicator, {
        schema: Joi.object({
            nom_service_public_numerique: Joi.string().required(),
            indicateur: Joi.string().required(),
            valeur: Joi.number().required(),
            unite_mesure: Joi.string().required(),
            frequence_calcul: Joi.string().required(),
            date: Joi.number().required(),
            est_periode: Joi.boolean().required(),
        }),
    }),
);

export { router };
