import { DataSource } from 'typeorm';
import { buildIndicatorService, indicatorDtoType } from './indicator.service';

export { buildIndicatorController };

function buildIndicatorController(dataSource: DataSource) {
    const indicatorService = buildIndicatorService(dataSource);
    const indicatorController = {
        getIndicators,
        upsertIndicator,
        deleteIndicator,
    };

    return indicatorController;

    async function getIndicators() {
        return indicatorService.getIndicators();
    }

    async function deleteIndicator(params: { urlParams: { indicatorId: string } }) {
        return indicatorService.deleteIndicator(params.urlParams.indicatorId);
    }

    async function upsertIndicator(params: { body: indicatorDtoType }) {
        return indicatorService.upsertIndicator(params.body);
    }
}
