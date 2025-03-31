import { PRODUCT_ID, PRODUCTS } from '../../../constants';
import { cache } from '../../../lib/cache';
import { logger } from '../../../lib/logger';
import { dateHandler } from '../utils';

type SUITE_PRODUCT_ID = Extract<
    PRODUCT_ID,
    'RESANA' | 'FRANCE_TRANSFERT' | 'DOCS' | 'RIZOMO' | 'VISIO' | 'PLANKA' | 'PAD'
>;

type suiteNumeriqueOutputApiType = Array<{
    'Fournisseur Service': string;
    'Valeurs distinctes de Sub FI': number;
}>;

const proConnectMetabaseNameMapping: Record<SUITE_PRODUCT_ID, string> = {
    RESANA: 'DINUM - RESANA',
    FRANCE_TRANSFERT: 'France transfert',
    DOCS: 'Docs',
    VISIO: 'Visio',
    PLANKA: 'Planka',
    RIZOMO: 'Rizomo',
    PAD: 'Pad',
};

function buildSuiteAdaptator(productId: SUITE_PRODUCT_ID) {
    const productName = PRODUCTS[productId].name;
    return { fetch };

    async function fetch() {
        const url =
            'https://stats.moncomptepro.beta.gouv.fr/public/question/0e3cee98-df38-4d57-8c37-d38c5a2d3231.json';
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
            const value = row['Valeurs distinctes de Sub FI'];

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
const docsAdaptator = buildSuiteAdaptator('DOCS');
const visioAdaptator = buildSuiteAdaptator('VISIO');
const plankaAdaptator = buildSuiteAdaptator('PLANKA');
const rizomoAdaptator = buildSuiteAdaptator('RIZOMO');
const padAdaptator = buildSuiteAdaptator('PAD');

export {
    resanaAdaptator,
    franceTransfertAdaptator,
    docsAdaptator,
    visioAdaptator,
    plankaAdaptator,
    rizomoAdaptator,
    padAdaptator,
};
