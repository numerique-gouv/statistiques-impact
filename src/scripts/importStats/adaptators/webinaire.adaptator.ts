import axios from 'axios';
import { dateHandler } from '../utils';
import { logger } from '../../../lib/logger';
import { PRODUCTS } from '../../../constants';

const webinaireAdaptator = { fetch };

const productName = PRODUCTS.WEBINAIRE.name;

type webinaireApiOutputType = Array<{ 'Created At': string; 'Nombre de lignes': number }>;

async function fetch() {
    const url =
        'http://webinaire-metabase.osc-secnum-fr1.scalingo.io/public/question/ddae3b19-ed8b-41db-84b1-24ec5841cce5.json';
    const result = await axios.get<webinaireApiOutputType>(url);

    const webinaireOutputRows = result.data;

    const indicatorDtos = [];
    const indicatorName = 'conférences';
    for (const webinaireOutputRow of webinaireOutputRows) {
        try {
            const date_debut = dateHandler.formatDate(webinaireOutputRow['Created At']);
            const date = dateHandler.addMonth(date_debut);
            const value = Number(webinaireOutputRow['Nombre de lignes']);
            if (isNaN(value)) {
                throw new Error(
                    `The "Nombre de lignes" value for ${date_debut} is ${webinaireOutputRow['Nombre de lignes']} and could not be parsed as a number.`,
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

    return indicatorDtos;
}

export { webinaireAdaptator };
