import { buildIndicatorService } from './indicator.service';

export { buildIndicatorController };

function buildIndicatorController() {
    const indicatorService = buildIndicatorService();
    const indicatorController = {
        getIndicators,
    };

    return indicatorController;

    async function getIndicators() {
        return indicatorService.getIndicators();
    }
}
