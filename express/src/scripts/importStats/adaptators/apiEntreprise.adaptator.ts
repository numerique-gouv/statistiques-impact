import axios from 'axios';
import { dateHandler } from '../utils';
import { logger } from '../../../lib/logger';
import { PRODUCTS } from '../../../constants';

const apiEntrepriseAdaptator = { fetch };

const productName = PRODUCTS.API_ENTREPRISE.name;

type apiEntrepriseSpecificindicatorOutputType = Array<{ timestamp: string; count: number }>;
type apiEntrepriseIndicatorsOutputType = Array<{ name: string; url: string; type: string }>;

async function fetch() {
    const url = 'https://entreprise.api.gouv.fr/stats.json';
    const indicators = await axios.get<apiEntrepriseIndicatorsOutputType>(url);
    const apiEntrepriseOutput: Record<string, apiEntrepriseSpecificindicatorOutputType> = {};
    for (const indicator of indicators.data) {
        const indicatorName = indicator.name;
        const result = await axios.get<apiEntrepriseSpecificindicatorOutputType>(indicator.url);
        apiEntrepriseOutput[indicatorName] = result.data;
    }

    const indicatorDtos = [];
    const indicatorNames = Object.keys(apiEntrepriseOutput);
    for (const indicatorName of indicatorNames) {
        const indicatorValues = apiEntrepriseOutput[indicatorName];
        for (const indicatorValue of indicatorValues) {
            try {
                const date_debut = dateHandler.formatDate(indicatorValue.timestamp);
                const date = dateHandler.addMonth(date_debut);
                const value = Number(indicatorValue.count);
                if (isNaN(value)) {
                    throw new Error(
                        `The "count" value for ${indicatorValue.timestamp} is ${indicatorValue.count} and could not be parsed as a number.`,
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

export { apiEntrepriseAdaptator };
