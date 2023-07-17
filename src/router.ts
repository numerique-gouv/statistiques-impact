import Express from 'express';
import { buildIndicatorService } from './modules/indicator';

const router = Express.Router();

router.get('/', (req, res) => {
    res.send('Hello world!');
});

router.get('/indicators', async (req, res) => {
    const indicatorService = buildIndicatorService();
    const indicators = await indicatorService.getIndicators();
    res.send(indicators);
});

export { router };
