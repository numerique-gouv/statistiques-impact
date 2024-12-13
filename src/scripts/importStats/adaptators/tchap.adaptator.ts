import axios from 'axios';
import { dateHandler } from '../utils';
import { logger } from '../../../lib/logger';
import { PRODUCTS } from '../../../constants';

const tchapAdaptator = { fetch };

const productName = PRODUCTS.TCHAP.name;

type tchapApiOutputType = Array<{
    Month: string;
    'Valeurs distinctes de User ID': string;
}>;

async function fetch() {
    const url =
        'https://stats.tchap.incubateur.net/public/question/ae34205d-9010-4a00-b1bf-5d6a7c5901fb.json';
    const result = await axios.get<tchapApiOutputType>(url);
    const tchapOutputRows = result.data;

    const indicatorName = 'utilisateurs actifs';
    const indicatorDtos: any = [];
    for (const tchapOutputRow of tchapOutputRows) {
        try {
            const date_debut = parseWrittenDate(tchapOutputRow.Month);
            const date = dateHandler.addMonth(date_debut);
            const value = Number(tchapOutputRow['Nombre de lignes'].replace(/ /g, ''));
            if (isNaN(value)) {
                throw new Error(
                    `tchapOutputRow['Nombre de lignes'] ${tchapOutputRow['Nombre de lignes']} is NaN`,
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

function parseWrittenDate(writtenDate: string) {
    const YEAR_REGEX = /^[0-9]{4}$/;
    const [writtenMonth, year] = writtenDate.split(', ');
    if (!writtenMonth || !year || !year.match(YEAR_REGEX) || !monthMapping[writtenMonth]) {
        throw new Error(`Could not parse written date ${writtenDate}`);
    }
    const month = monthMapping[writtenMonth];
    return `${year}-${month}-01`;
}

const monthMapping: Record<string, string> = {
    'avr.': '04',
    mai: '05',
    juin: '06',
    'juil.': '07',
    août: '08',
    'sept.': '09',
    'oct.': '10',
    'nov.': '11',
    'déc.': '12',
    'janv.': '01',
    'févr.': '02',
    mars: '03',
};

export { tchapAdaptator };
