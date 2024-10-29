import { PRODUCT_ID, PRODUCTS } from '../../../constants';
import { cache } from '../../../lib/cache';
import { logger } from '../../../lib/logger';
import { dateHandler } from '../utils';

type SUITE_PRODUCT_ID = Extract<
    PRODUCT_ID,
    'RESANA' | 'FRANCE_TRANSFERT' | 'IMPRESS' | 'RIZOMO' | 'MEET' | 'PLANKA' | 'REGIE'
>;

type suiteNumeriqueOutputApiType = Array<{
    'Fournisseur Service': string;
    'Distinct values of Sub Fi': number;
}>;

const proConnectMetabaseNameMapping: Record<SUITE_PRODUCT_ID, string> = {
    RESANA: 'DINUM - RESANA',
    FRANCE_TRANSFERT: 'France transfert',
    IMPRESS: 'Impress',
    MEET: 'Meet',
    PLANKA: 'Planka',
    RIZOMO: 'Rizomo',
    REGIE: 'Régie',
};

function buildSuiteAdaptator(productId: SUITE_PRODUCT_ID) {
    const productName = PRODUCTS[productId].name;
    return { fetch };

    async function fetch() {
        const url =
            'http://stats.agentconnect.gouv.fr/public/question/a26a6b26-3d97-4bb1-8b13-983b4ebbc23b.json';
        const data = await cache.fetch<suiteNumeriqueOutputApiType>(url);
        const indicatorName = 'utilisateurs actifs';
        const indicatorDtos: any = [];
        try {
            const row = data.find(
                (row) => row['Fournisseur Service'] === proConnectMetabaseNameMapping[productId],
            );
            if (!row) {
                throw new Error(
                    `Could not find "${proConnectMetabaseNameMapping[productId]}" in the JSON.`,
                );
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
}

const resanaAdaptator = buildSuiteAdaptator('RESANA');
const franceTransfertAdaptator = buildSuiteAdaptator('FRANCE_TRANSFERT');
const impressAdaptator = buildSuiteAdaptator('IMPRESS');
const meetAdaptator = buildSuiteAdaptator('MEET');
const plankaAdaptator = buildSuiteAdaptator('PLANKA');
const rizomoAdaptator = buildSuiteAdaptator('RIZOMO');
const regieAdaptator = buildSuiteAdaptator('REGIE');

export {
    resanaAdaptator,
    franceTransfertAdaptator,
    impressAdaptator,
    meetAdaptator,
    plankaAdaptator,
    rizomoAdaptator,
    regieAdaptator,
};