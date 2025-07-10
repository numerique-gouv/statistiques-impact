import { cache } from '../../../lib/cache';
import { dateHandler } from '../utils';
import { logger } from '../../../lib/logger';
import { PRODUCTS } from '../../../constants';
import { log } from "console";

const regieAdaptator = { fetch };

const productName = PRODUCTS.REGIE.name;

interface Dictionary<T> {
    [key: string]: T;
}


type regieApiOutputType = Dictionary<{
    total_users: number;
    mau: number;
    teams: number;
    domains: number;
    mailboxes: number;
}>;

async function fetch() {
    const url = 'https://regie.numerique.gouv.fr/api/v1.0/stats/';
    const data = await cache.fetch<regieApiOutputType>(url);
    const indicatorName = 'utilisateurs actifs';
    const indicatorDtos: any = [];
    log(data["mau"])

    const now = new Date();
    const date = dateHandler.formatDate(now.toISOString());
    const date_debut = dateHandler.substractMonth(date);


    try {
        indicatorDtos.push({
            date_debut,
            date,
            indicateur: indicatorName,
            unite_mesure: 'unité',
            nom_service_public_numerique: productName,
            frequence_monitoring: 'mensuelle',
            est_automatise: true,
            est_periode: true,
            valeur: Number(data),
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

export { regieAdaptator };
