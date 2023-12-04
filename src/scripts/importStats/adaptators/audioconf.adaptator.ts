import axios from 'axios';
import { dateHandler } from '../utils';
import { logger } from '../../../lib/logger';
import { PRODUCTS } from '../../../constants';

const audioconfAdaptator = { fetch };

const productName = PRODUCTS.AUDIOCONF.name;

type audioconfApiOutputType = Array<{ 'Date Begin': string; 'Nombre de lignes': number }>;

async function fetch() {
    const url =
        'https://stats.audioconf.numerique.gouv.fr/public/question/f98281a7-5bd6-4f09-8ec6-a278975adfb9.json';
    const result = await axios.get<audioconfApiOutputType>(url);
    const audioconfOutputRows = result.data;

    const indicatorDtos = [];
    const indicatorName = 'conférences de plus de deux minutes';
    for (const audioconfOutputRow of audioconfOutputRows) {
        try {
            const date_debut = dateHandler.formatDate(audioconfOutputRow['Date Begin']);
            const date = dateHandler.addMonth(date_debut);

            const value = Number(audioconfOutputRow['Nombre de lignes']);
            if (isNaN(value)) {
                throw new Error(
                    `The "Nombre de lignes" value for ${date_debut} is ${audioconfOutputRow['Nombre de lignes']} and could not be parsed as a number.`,
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

export { audioconfAdaptator };
