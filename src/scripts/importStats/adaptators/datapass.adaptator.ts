import axios from 'axios';
import { dateHandler } from '../utils';
import { PRODUCTS } from '../constants';
import { logger } from '../../../lib/logger';

const datapassAdaptator = { fetch, map };

type datapassApiResultType = {
    monthly_enrollment_count: Array<{ month: string; validated: number }>;
};

async function fetch() {
    const url = `https://back.datapass.api.gouv.fr/api/stats`;
    const result = await axios.get(url);

    return result.data;
}

function map(datapassApiOutput: datapassApiResultType) {
    let indicatorDtos = [];
    const indicatorName = 'habilitations validées';
    const productName = PRODUCTS.DATAPASS;
    for (const monthlyValue of datapassApiOutput.monthly_enrollment_count) {
        try {
            const { month, validated } = monthlyValue;
            const date_debut = dateHandler.formatDate(month);
            const date = dateHandler.addMonth(date_debut);
            const indicatorDto = {
                date,
                date_debut,
                valeur: validated,
                indicateur: indicatorName,
                unite_mesure: 'unité',
                frequence_calcul: 'mensuelle',
                est_periode: true,
            };
            indicatorDtos.push(indicatorDto);
        } catch (error) {
            logger.error({ productName, indicator: indicatorName, message: error as string });
        }
    }
    return indicatorDtos;
}

export { datapassAdaptator };
