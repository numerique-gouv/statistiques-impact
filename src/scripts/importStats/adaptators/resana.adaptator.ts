import { dateHandler } from '../utils';
import { logger } from '../../../lib/logger';
import { PRODUCTS } from '../../../constants';
import { cache } from '../../../lib/cache';

const resanaAdaptator = { fetch };

const productName = PRODUCTS.RESANA.name;

type suiteNumeriqueOutputApiType = Array<{
    'Fournisseur Service': string;
    'Distinct values of Sub Fi': number;
}>;

async function fetch() {
    const url =
        'http://stats.agentconnect.gouv.fr/public/question/a26a6b26-3d97-4bb1-8b13-983b4ebbc23b.json';
    const data = await cache.fetch<suiteNumeriqueOutputApiType>(url);

    const indicatorName = 'utilisateurs actifs';
    const indicatorDtos: any = [];
    try {
        const row = data.find((row) => row['Fournisseur Service'] === 'DINUM - RESANA');
        if (!row) {
            throw new Error(`Could not find "DINUM - RESANA" in the JSON.`);
        }
        const value = row['Distinct values of Sub Fi'];

        const now = new Date();
        const date = dateHandler.formatDate(now.toISOString());
        const date_debut = dateHandler.substractMonth(date);
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

    return indicatorDtos;
}

export { resanaAdaptator };
