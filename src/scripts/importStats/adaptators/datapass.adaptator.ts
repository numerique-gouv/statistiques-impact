import axios from 'axios';
import { dateHandler } from '../utils';
import { logger } from '../../../lib/logger';
import { PRODUCTS } from '../../../constants';

const datapassAdaptator = { fetch };

type datapassApiResultType = {
    monthly_enrollment_count: Array<{ month: string; validated: number }>;
};

const productName = PRODUCTS.DATAPASS.name;

async function fetch() {
    const url = `https://back.datapass.api.gouv.fr/api/stats`;
    const result = await axios.get<datapassApiResultType>(url);

    const datapassApiOutput = result.data;

    let indicatorDtos = [];
    const indicatorName = 'habilitations validées';
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
                nom_service_public_numerique: productName,
                unite_mesure: 'unité',
                frequence_monitoring: 'mensuelle',
                est_automatise: true,
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
