import axios from 'axios';
import { dateHandler } from '../utils';
import { logger } from '../../../lib/logger';
import { PRODUCTS } from '../../../constants';

const apiEntrepriseAdaptator = { map, fetch };

const productName = PRODUCTS.API_ENTREPRISE.name;

type apiEntrepriseOutputType = Record<string, Array<{ timestamp: string; count: number }>>;

function map(apiEntrepriseOutput: apiEntrepriseOutputType) {
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
                    frequence_calcul: 'mensuelle',
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

async function fetch(): Promise<apiEntrepriseOutputType> {
    const url = 'https://entreprise.api.gouv.fr/stats.json';
    const indicators = await axios.get(url);
    const apiOutput: apiEntrepriseOutputType = {};
    for (const indicator of indicators.data) {
        const indicatorName = indicator.name;
        const result = await axios.get(indicator.url);
        apiOutput[indicatorName] = result.data;
    }
    return apiOutput;
}

export { apiEntrepriseAdaptator };
