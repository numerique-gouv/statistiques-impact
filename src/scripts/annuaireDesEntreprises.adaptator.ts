import axios from 'axios';
import { dateHandler } from './utils';

const annuaireDesEntreprisesAdaptator = { fetch, map };

type annuaireDesEntreprisesApiResultType = {
    copyPasteAction: Array<{ label: string; value: number }>;
    redirectedSiren: Array<{ label: string; value: number }>;
};

async function fetch() {
    const url = `https://annuaire-entreprises.data.gouv.fr/api/stats`;
    const result = await axios.get(url);

    return result.data;
}

function map(annuaireDesEntreprisesApiOutput: annuaireDesEntreprisesApiResultType) {
    let indicatorDtos = [];
    const indicatorNames = {
        copyPasteAction: 'Nombre de copier/coller depuis une fiche entreprise',
        redirectedSiren: 'Nombre de SIREN utilisés en accès direct',
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
                    unite_mesure: 'unité',
                    frequence_calcul: 'mensuelle',
                    est_periode: true,
                };
                indicatorDtos.push(indicatorDto);
            } catch (error) {
                console.warn(error);
            }
        }
    }

    return indicatorDtos;
}

export { annuaireDesEntreprisesAdaptator };
