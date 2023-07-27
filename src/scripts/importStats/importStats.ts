import { dataSource } from '../../dataSource';
import { buildIndicatorService, indicatorDtoType } from '../../modules/indicator';
import { audioconfAdaptator } from './adaptators/audioconf.adaptator';
import { padAdaptator } from './adaptators/pad.adaptator';
import { demarchesSimplifieesAdaptator } from './adaptators/demarchesSimplifiees.adaptator';
import { datapassAdaptator } from './adaptators/datapass.adaptator';
import { annuaireDesEntreprisesAdaptator } from './adaptators/annuaireDesEntreprises.adaptator';
import { adaptatorType } from './types';
import { dateHandler } from './utils';
import { PRODUCTS } from './constants';
import { webinaireAdaptator } from './adaptators/webinaire.adaptator';
import { apiParticulierAdaptator } from './adaptators/apiParticulier.adaptator';

const indicatorsToUpdate: Array<{
    productName: string;
    adaptator: adaptatorType<any>;
}> = [
    {
        productName: PRODUCTS.AUDIOCONF,
        adaptator: audioconfAdaptator,
    },
    {
        productName: PRODUCTS.PAD,
        adaptator: padAdaptator,
    },
    {
        productName: PRODUCTS.DEMARCHES_SIMPLIFIEES,
        adaptator: demarchesSimplifieesAdaptator,
    },
    { productName: PRODUCTS.DATAPASS, adaptator: datapassAdaptator },
    { productName: PRODUCTS.ANNUAIRE_DES_ENTREPRISES, adaptator: annuaireDesEntreprisesAdaptator },
    { productName: PRODUCTS.WEBINAIRE, adaptator: webinaireAdaptator },
    { productName: PRODUCTS.API_PARTICULIER, adaptator: apiParticulierAdaptator },
];

async function importStats() {
    await dataSource.initialize();
    const indicatorService = buildIndicatorService(dataSource);

    for (const indicatorToUpdate of indicatorsToUpdate) {
        const result = await indicatorToUpdate.adaptator.fetch();
        const indicatorDtos = indicatorToUpdate.adaptator
            .map(result)
            .filter(filterUncompletedMonth);
        await indicatorService.upsertIndicators(indicatorDtos);
    }
}

function filterUncompletedMonth(indicatorDto: indicatorDtoType): boolean {
    const parsedDate = dateHandler.parseDate(indicatorDto.date);
    const dateSup = new Date();
    dateSup.setFullYear(parsedDate.year);
    dateSup.setMonth(parsedDate.month - 1);
    dateSup.setDate(parsedDate.dayOfMonth);

    const now = new Date();
    return now.getTime() > dateSup.getTime();
}

importStats();
