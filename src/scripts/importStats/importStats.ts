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
import { dateHandler, parsedDateType } from './utils';
import { documentationAdaptator } from './adaptators/documentation.adaptator';
import { hubeeAdaptator } from './adaptators/hubee.adaptator';
import {
    resanaAdaptator,
    franceTransfertAdaptator,
    impressAdaptator,
    meetAdaptator,
    plankaAdaptator,
    rizomoAdaptator,
    regieAdaptator,
} from './adaptators/suite.adaptator';

const indicatorsToUpdate: Record<string, adaptatorType> = {
    [PRODUCTS.HUBEE.name]: hubeeAdaptator,
    [PRODUCTS.AUDIOCONF.name]: audioconfAdaptator,
    [PRODUCTS.PAD.name]: padAdaptator,
    [PRODUCTS.DEMARCHES_SIMPLIFIEES.name]: demarchesSimplifieesAdaptator,
    [PRODUCTS.DATAPASS.name]: datapassAdaptator,
    [PRODUCTS.ANNUAIRE_DES_ENTREPRISES.name]: annuaireDesEntreprisesAdaptator,
    [PRODUCTS.WEBINAIRE.name]: webinaireAdaptator,
    [PRODUCTS.AGENT_CONNECT.name]: agentConnectAdaptator,
    [PRODUCTS.TCHAP.name]: tchapAdaptator,
    [PRODUCTS.DOCUMENTATION.name]: documentationAdaptator,
    [PRODUCTS.API_PARTICULIER.name]: apiParticulierAdaptator,
    [PRODUCTS.API_ENTREPRISE.name]: apiEntrepriseAdaptator,
    [PRODUCTS.RESANA.name]: resanaAdaptator,
    [PRODUCTS.IMPRESS.name]: impressAdaptator,
    [PRODUCTS.FRANCE_TRANSFERT.name]: franceTransfertAdaptator,
    [PRODUCTS.MEET.name]: meetAdaptator,
    [PRODUCTS.PLANKA.name]: plankaAdaptator,
    [PRODUCTS.REGIE.name]: regieAdaptator,
    [PRODUCTS.RIZOMO.name]: rizomoAdaptator,
};

async function importStats() {
    console.log('IMPORT STATS');
    console.log('===');
    console.log(`Initializing database...`);
    await dataSource.initialize();
    console.log(`Database initialized...`);

    const indicatorService = buildIndicatorService(dataSource);

    for (const [productName, adaptator] of Object.entries(indicatorsToUpdate)) {
        console.log(`Fetching indicators for "${productName}"...`);
        try {
            const result = await adaptator.fetch();
            const now = new Date();
            const parsedNowDate = {
                year: now.getFullYear(),
                month: now.getMonth() + 1,
                dayOfMonth: now.getDate(),
            };
            const indicatorDtos = result.filter((indicatorDto) =>
                filterUncompletedMonth(indicatorDto, parsedNowDate),
            );
            console.log(`${indicatorDtos.length} found! Inserting in database...`);
            await indicatorService.upsertIndicators(productName, indicatorDtos);
            console.log(`Indicators inserted!`);
        } catch (error) {
            logger.error({ productName: productName, message: error as string });
        }
    }
}

function filterUncompletedMonth(
    indicatorDto: indicatorDtoType,
    parsedNowDate: parsedDateType,
): boolean {
    const parsedIndicatorDate = dateHandler.parseStringDate(indicatorDto.date);
    const result = dateHandler.compareDates(parsedIndicatorDate, parsedNowDate) !== -1;
    return result;
}

importStats();
