import { dataSource } from '../dataSource';
import { buildIndicatorService, indicatorDtoType } from '../modules/indicator';
import { audioconfAdaptator } from './audioconf.adaptator';
import { padAdaptator } from './pad.adaptator';
import { adaptatorType } from './types';
import { demarchesSimplifieesAdaptator } from './demarchesSimplifiees.adaptator';
import { datapassAdaptator } from './datapass.adaptator';
import { dateHandler } from './utils';
import { annuaireDesEntreprisesAdaptator } from './annuaireDesEntreprises.adaptator';

const indicatorsToUpdate: Array<{
    productName: string;
    adaptator: adaptatorType<any>;
}> = [
    // {
    //     productName: 'audioconf',
    //     adaptator: audioconfAdaptator,
    // },
    // {
    //     productName: 'pad',
    //     adaptator: padAdaptator,
    // },
    // {
    //     productName: 'demarches-simplifiees',
    //     adaptator: demarchesSimplifieesAdaptator,
    // },
    // { productName: 'datapass', adaptator: datapassAdaptator },
    { productName: 'annuaire-des-entreprises', adaptator: annuaireDesEntreprisesAdaptator },
];

async function importStats() {
    await dataSource.initialize();
    const indicatorService = buildIndicatorService(dataSource);

    for (const indicatorToUpdate of indicatorsToUpdate) {
        const result = await indicatorToUpdate.adaptator.fetch();
        const indicatorDtos = indicatorToUpdate.adaptator
            .map(result)
            .map((indicatorDto) => ({
                ...indicatorDto,
                nom_service_public_numerique: indicatorToUpdate.productName,
            }))
            .filter(filter);
        await indicatorService.upsertIndicators(indicatorDtos);
    }
}

function filter(indicatorDto: indicatorDtoType): boolean {
    const parsedDate = dateHandler.parseDate(indicatorDto.date);
    const dateSup = new Date();
    dateSup.setFullYear(parsedDate.year);
    dateSup.setMonth(parsedDate.month - 1);
    dateSup.setDate(parsedDate.dayOfMonth);

    const now = new Date();
    return now.getTime() > dateSup.getTime();
}

importStats();
