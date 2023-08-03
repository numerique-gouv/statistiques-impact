import { dataSource } from '../../dataSource';
import { buildIndicatorService, indicatorDtoType } from '../../modules/indicator';
import { logger } from '../../lib/logger';
import { PRODUCTS } from '../../constants';
import { audioconfAdaptator } from './adaptators/audioconf.adaptator';
import { padAdaptator } from './adaptators/pad.adaptator';
import { demarchesSimplifieesAdaptator } from './adaptators/demarchesSimplifiees.adaptator';
import { datapassAdaptator } from './adaptators/datapass.adaptator';
import { annuaireDesEntreprisesAdaptator } from './adaptators/annuaireDesEntreprises.adaptator';
import { webinaireAdaptator } from './adaptators/webinaire.adaptator';
import { apiParticulierAdaptator } from './adaptators/apiParticulier.adaptator';
import { apiEntrepriseAdaptator } from './adaptators/apiEntreprise.adaptator';
import { agentConnectAdaptator } from './adaptators/agentConnect.adaptator';
import { tchapAdaptator } from './adaptators/tchap.adaptator';
import { adaptatorType } from './types';
import { dateHandler } from './utils';

const indicatorsToUpdate: Record<string, adaptatorType<any>> = {
    [PRODUCTS.AUDIOCONF.name]: audioconfAdaptator,
    [PRODUCTS.PAD.name]: padAdaptator,
    [PRODUCTS.DEMARCHES_SIMPLIFIEES.name]: demarchesSimplifieesAdaptator,
    [PRODUCTS.DATAPASS.name]: datapassAdaptator,
    [PRODUCTS.ANNUAIRE_DES_ENTREPRISES.name]: annuaireDesEntreprisesAdaptator,
    [PRODUCTS.WEBINAIRE.name]: webinaireAdaptator,
    [PRODUCTS.API_PARTICULIER.name]: apiParticulierAdaptator,
    [PRODUCTS.API_ENTREPRISE.name]: apiEntrepriseAdaptator,
    [PRODUCTS.AGENT_CONNECT.name]: agentConnectAdaptator,
    [PRODUCTS.TCHAP.name]: tchapAdaptator,
};

async function importStats() {
    await dataSource.initialize();
    const indicatorService = buildIndicatorService(dataSource);

    for (const [productName, adaptator] of Object.entries(indicatorsToUpdate)) {
        try {
            const result = await adaptator.fetch();
            const indicatorDtos = adaptator.map(result).filter(filterUncompletedMonth);
            await indicatorService.upsertIndicators(indicatorDtos);
        } catch (error) {
            logger.error({ productName: productName, message: error as string });
        }
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
