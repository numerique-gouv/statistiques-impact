import Express from 'express';
import { buildIndicatorController } from './modules/indicator';
import { buildController } from './lib/buildController';

const router = Express.Router();
const indicatorController = buildIndicatorController();

router.get('/', (req, res) => {
    res.send('Hello world!');
});

router.get('/indicators', buildController(indicatorController.getIndicators));

export { router };
