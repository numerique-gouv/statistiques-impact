import axios from 'axios';
import { dataSource } from '../dataSource';
import { buildIndicatorService, indicatorDtoType } from '../modules/indicator';
import { audioconfAdaptator } from './audioconf.adaptator';
import { padAdaptator } from './pad.adaptator';

const indicatorsToUpdate: Array<{
    productName: string;
    adaptator: (input: any) => Array<Omit<indicatorDtoType, 'nom_service_public_numerique'>>;
    url: string;
}> = [
    {
        productName: 'audioconf',
        adaptator: audioconfAdaptator.format,
        url: 'https://stats.audioconf.numerique.gouv.fr/public/question/f98281a7-5bd6-4f09-8ec6-a278975adfb9.json',
    },
    {
        productName: 'pad',
        adaptator: padAdaptator.format,
        url: `https://pad.numerique.gouv.fr/stats/users/lastMonth`,
    },
];

async function importStats() {
    await dataSource.initialize();
    const indicatorService = buildIndicatorService(dataSource);

    for (const indicatorToUpdate of indicatorsToUpdate) {
        const result = await axios.get(indicatorToUpdate.url);
        const indicatorDtos = indicatorToUpdate.adaptator(result.data);
        await indicatorService.upsertIndicators(
            indicatorDtos.map((indicatorDto) => ({
                ...indicatorDto,
                nom_service_public_numerique: indicatorToUpdate.productName,
            })),
        );
    }
}

importStats();
