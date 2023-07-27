import axios from 'axios';
import { dateHandler } from '../utils';

const audioconfAdaptator = { map, fetch };

type audioconfOutputRowType = { 'Date Begin': string; Count: number };

function map(audioconfOutputRows: Array<audioconfOutputRowType>) {
    const indicatorDtos: Array<any> = [];
    for (const audioconfOutputRow of audioconfOutputRows) {
        try {
            const date_debut = audioconfOutputRow['Date Begin'].slice(0, 10);
            const date = dateHandler.addMonth(date_debut);

            const value = audioconfOutputRow.Count;

            indicatorDtos.push({
                date_debut,
                date,
                indicateur: 'conférences de plus de deux minutes',
                unite_mesure: 'unité',
                frequence_calcul: 'mensuelle',
                est_periode: true,
                valeur: value,
            });
        } catch (error) {
            console.warn(error);
        }
    }

    return indicatorDtos;
}

async function fetch() {
    const url =
        'https://stats.audioconf.numerique.gouv.fr/public/question/f98281a7-5bd6-4f09-8ec6-a278975adfb9.json';
    const result = await axios.get(url);
    return result.data;
}

export { audioconfAdaptator };
