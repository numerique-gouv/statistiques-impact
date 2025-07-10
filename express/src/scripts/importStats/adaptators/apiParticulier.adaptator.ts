import axios from 'axios';
import { dateHandler } from '../utils';
import { logger } from '../../../lib/logger';
import { PRODUCTS } from '../../../constants';

const apiParticulierAdaptator = { fetch };

const productName = PRODUCTS.API_PARTICULIER.name;

type apiParticulierSpecificindicatorOutputType = Array<{ timestamp: string; 'Nb appels': number }>;
type apiParticulierIndicatorsOutputType = Array<{ name: string; url: string; type: string }>;

async function fetch() {
    const url = 'https://particulier.api.gouv.fr/stats.json';
    const indicators = await axios.get<apiParticulierIndicatorsOutputType>(url);
    const apiOutput: Record<string, apiParticulierSpecificindicatorOutputType> = {};
    for (const indicator of indicators.data) {
        const indicatorName = indicator.name;
        const result = await axios.get<apiParticulierSpecificindicatorOutputType>(indicator.url);
        apiOutput[indicatorName] = result.data;
    }

    const indicatorDtos = [];
    const indicatorNames = Object.keys(apiOutput);
    for (const indicatorName of indicatorNames) {
        const indicatorValues = apiOutput[indicatorName];
        for (const indicatorValue of indicatorValues) {
            try {
                const date_debut = dateHandler.formatDate(indicatorValue.timestamp);
                const date = dateHandler.addMonth(date_debut);
                const value = Number(indicatorValue['Nb appels']);
                if (isNaN(value)) {
                    throw new Error(
                        `The "Nb appels" value for ${indicatorValue.timestamp} is ${indicatorValue['Nb appels']} and could not be parsed as a number.`,
                    );
                }
                indicatorDtos.push({
                    date_debut,
                    date,
                    indicateur: indicatorName,
                    unite_mesure: 'unité',
                    nom_service_public_numerique: productName,
                    frequence_monitoring: 'mensuelle',
                    est_automatise: true,
                    est_periode: true,
                    valeur: value,
                });
            } catch (error) {
                logger.error({
                    productName,
                    indicator: indicatorName,
                    message: error as string,
                });
            }
        }
    }

    return indicatorDtos;
}

export { apiParticulierAdaptator };
