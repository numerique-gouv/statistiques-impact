import { Indicator } from './Indicator.entity';
import { buildIndicatorService, indicatorDto } from './indicator.service';

export { buildIndicatorController };

function buildIndicatorController() {
    const indicatorService = buildIndicatorService();
    const indicatorController = {
        getIndicators,
        createIndicator,
        deleteIndicator,
    };

    return indicatorController;

    async function getIndicators() {
        return indicatorService.getIndicators();
    }

    async function deleteIndicator(params: { urlParams: { indicatorId: string } }) {
        return indicatorService.deleteIndicator(params.urlParams.indicatorId);
    }

    async function createIndicator(params: { body: indicatorDto }) {
        return indicatorService.createIndicator(params.body);
    }
}
