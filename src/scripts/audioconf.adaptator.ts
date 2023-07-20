import axios from 'axios';

const audioconfAdaptator = { map, fetch };

type audioconfOutputRowType = { 'Date Begin': string; Count: number };

function map(audioconfOutputRows: Array<audioconfOutputRowType>) {
    const output: Array<any> = [];
    for (const audioconfOutputRow of audioconfOutputRows) {
        const dateInf = new Date(audioconfOutputRow['Date Begin']);
        const dateSup = new Date(dateInf);
        if (dateInf.getMonth() === 11) {
            dateSup.setMonth(0);
            dateSup.setFullYear(dateInf.getFullYear() + 1);
        } else {
            dateSup.setMonth(dateInf.getMonth() + 1);
        }
        const now = new Date();

        if (dateSup.getTime() > now.getTime()) {
            continue;
        }
        const formattedSupYear = `${dateSup.getFullYear()}`;
        const formattedSupMonth =
            dateSup.getMonth() + 1 < 10
                ? `0${dateSup.getMonth() + 1}`
                : `${dateSup.getMonth() + 1}`;
        const formattedSupDayOfMonth =
            dateSup.getDate() < 10 ? `0${dateSup.getDate()}` : `${dateSup.getDate()}`;
        const date = `${formattedSupYear}-${formattedSupMonth}-${formattedSupDayOfMonth}`;
        const date_debut = audioconfOutputRow['Date Begin'].slice(0, 10);
        const value = audioconfOutputRow.Count;

        output.push({
            date_debut,
            date,
            indicateur: 'Conférences créées',
            unite_mesure: 'unité',
            frequence_calcul: 'mensuelle',
            est_periode: true,
            valeur: value,
        });
    }

    return output;
}

async function fetch() {
    const url =
        'https://stats.audioconf.numerique.gouv.fr/public/question/f98281a7-5bd6-4f09-8ec6-a278975adfb9.json';
    const result = await axios.get(url);
    return result.data;
}

export { audioconfAdaptator };
