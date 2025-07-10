import axios from 'axios';
import { dateHandler } from '../utils';
import { logger } from '../../../lib/logger';
import { PRODUCTS } from '../../../constants';

const annuaireDesEntreprisesAdaptator = { fetch };

type annuaireDesEntreprisesApiResultType = {
    copyPasteAction: Array<{ label: string; value: number }>;
    redirectedSiren: Array<{ label: string; value: number }>;
};

const productName = PRODUCTS.ANNUAIRE_DES_ENTREPRISES.name;

async function fetch() {
    const url = `https://annuaire-entreprises.data.gouv.fr/api/data-fetching/stats`;
    const result = await axios.get<annuaireDesEntreprisesApiResultType>(url);

    const annuaireDesEntreprisesApiOutput = result.data;

    let indicatorDtos = [];
    const indicatorNames = {
        copyPasteAction: 'copier/coller depuis une fiche entreprise',
        redirectedSiren: 'SIREN utilisés en accès direct',
    };
    for (const indicatorName of Object.keys(indicatorNames) as Array<
        'copyPasteAction' | 'redirectedSiren'
    >) {
        for (const { label, value } of annuaireDesEntreprisesApiOutput[indicatorName]) {
            try {
                const { date, date_debut } = dateHandler.parseReadableDate(label);
                const indicatorDto = {
                    date,
                    date_debut,
                    valeur: value,
                    indicateur: indicatorNames[indicatorName],
                    nom_service_public_numerique: productName,
                    unite_mesure: 'unité',
                    frequence_monitoring: 'mensuelle',
                    est_automatise: true,
                    est_periode: true,
                };
                indicatorDtos.push(indicatorDto);
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

export { annuaireDesEntreprisesAdaptator };
