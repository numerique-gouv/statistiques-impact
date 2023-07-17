import { Indicator } from './Indicator.entity';
import { buildIndicatorService, indicatorDto } from './indicator.service';

export { buildIndicatorController };

function buildIndicatorController() {
    const indicatorService = buildIndicatorService();
    const indicatorController = {
        getIndicators,
        createIndicator,
    };

    return indicatorController;

    async function getIndicators() {
        return indicatorService.getIndicators();
    }

    async function createIndicator(params: { body: indicatorDto }) {
        return indicatorService.createIndicator(params.body);
    }
}
