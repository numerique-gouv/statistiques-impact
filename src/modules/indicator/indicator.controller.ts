import { DataSource } from 'typeorm';
import { buildIndicatorService, indicatorDtoType } from './indicator.service';

export { buildIndicatorController };

function buildIndicatorController(dataSource: DataSource) {
    const indicatorService = buildIndicatorService(dataSource);
    const indicatorController = {
        getIndicators,
        getIndicatorsByProductName,
        deleteIndicator,
        upsertIndicators,
        insertRawIndicators,
    };

    return indicatorController;

    async function getIndicators() {
        return indicatorService.getIndicators();
    }

    async function getIndicatorsByProductName(params: { urlParams: { name: string } }) {
        return indicatorService.getIndicatorsByProductName(params.urlParams.name);
    }

    async function upsertIndicators(params: {
        body: { productName: string; indicatorDtos: indicatorDtoType[] };
    }) {
        return indicatorService.upsertIndicators(
            params.body.productName,
            params.body.indicatorDtos,
        );
    }

    async function deleteIndicator(params: { urlParams: { indicatorId: string } }) {
        return indicatorService.deleteIndicator(params.urlParams.indicatorId);
    }

    async function insertRawIndicators(
        params: { urlParams: { productName: string } },
        clientId: string,
    ) {
        console.log(clientId);
        return {};
    }
}
