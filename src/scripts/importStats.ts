import axios from 'axios';
import { dataSource } from '../dataSource';
import { buildIndicatorService, indicatorDtoType } from '../modules/indicator';
import { audioconfAdaptator } from './audioconf.adaptator';
import { padAdaptator } from './pad.adaptator';
import { adaptatorType } from './types';
import { demarchesSimplifieesAdaptator } from './demarchesSimplifiees.adaptator';

const indicatorsToUpdate: Array<{
    productName: string;
    adaptator: adaptatorType<any>;
}> = [
    {
        productName: 'audioconf',
        adaptator: audioconfAdaptator,
    },
    {
        productName: 'pad',
        adaptator: padAdaptator,
    },
    {
        productName: 'demarches-simplifiees',
        adaptator: demarchesSimplifieesAdaptator,
    },
];

async function importStats() {
    await dataSource.initialize();
    const indicatorService = buildIndicatorService(dataSource);

    for (const indicatorToUpdate of indicatorsToUpdate) {
        const result = await indicatorToUpdate.adaptator.fetch();
        const indicatorDtos = indicatorToUpdate.adaptator.map(result);
        await indicatorService.upsertIndicators(
            indicatorDtos.map((indicatorDto) => ({
                ...indicatorDto,
                nom_service_public_numerique: indicatorToUpdate.productName,
            })),
        );
    }
}

importStats();
