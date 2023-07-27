import axios from 'axios';
import { logger } from '../../../lib/logger';
import { PRODUCTS } from '../constants';
import { dateHandler } from '../utils';

const padAdaptator = { map, fetch };

type padApiOutputType = {
    dateInf: string;
    dateSup: string;
    activeUsers: number;
};

function map(padApiOutput: padApiOutputType) {
    let indicatorDtos = [];
    const indicatorName = 'utilisateurs actifs';

    try {
        const date_debut = dateHandler.formatDate(padApiOutput.dateInf);
        const date = dateHandler.formatDate(padApiOutput.dateSup);
        const value = Number(padApiOutput.activeUsers);
        if (!isNaN(value)) {
            throw new Error(`activeUsers "${padApiOutput.activeUsers}" is NaN`);
        }

        indicatorDtos.push({
            date,
            date_debut,
            valeur: value,
            indicateur: indicatorName,
            unite_mesure: 'unité',
            frequence_calcul: 'mensuelle',
            est_periode: true,
        });
    } catch (error) {
        logger.error({
            productName: PRODUCTS.PAD,
            indicator: indicatorName,
            message: error as string,
        });
    }

    return indicatorDtos;
}

async function fetch() {
    const url = `https://pad.numerique.gouv.fr/stats/users/lastMonth`;
    const result = await axios.get(url);
    return result.data;
}

export { padAdaptator };
