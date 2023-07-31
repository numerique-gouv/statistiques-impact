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
import { apiEntrepriseAdaptator } from './adaptators/apiEntreprise.adaptator';
import { agentConnectAdaptator } from './adaptators/agentConnect.adaptator';
import { tchapAdaptator } from './adaptators/tchap.adaptator';

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
    { productName: PRODUCTS.API_ENTREPRISE, adaptator: apiEntrepriseAdaptator },
    { productName: PRODUCTS.AGENT_CONNECT, adaptator: agentConnectAdaptator },
    { productName: PRODUCTS.TCHAP, adaptator: tchapAdaptator },
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
    const parsedIndicatorDate = dateHandler.parseDate(indicatorDto.date);
    const now = new Date();
    const parsedNowDate = {
        year: now.getFullYear(),
        month: now.getMonth() + 1,
        dayOfMonth: now.getDate(),
    };

    return dateHandler.compareDates(parsedIndicatorDate, parsedNowDate) !== -1;
}

importStats();
