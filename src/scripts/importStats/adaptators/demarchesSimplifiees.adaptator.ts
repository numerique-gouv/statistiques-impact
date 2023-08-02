import axios from 'axios';
import { dateHandler, parseCsv } from '../utils';
import { logger } from '../../../lib/logger';
import { PRODUCTS } from '../../../constants';

const demarchesSimplifieesAdaptator = { map, fetch };

type indicatorSummaryType = {
    data: Array<{
        id: string;
        title: string;
        url: string;
    }>;
};

const indicatorName = 'procédures créées';
const productName = PRODUCTS.DEMARCHES_SIMPLIFIEES.name;

function map(indicators: Array<{ date: string; csv: string }>) {
    const indicatorDtos = [];
    for (const indicator of indicators) {
        try {
            const { values } = parseCsv(indicator.csv, { columnsCount: 2, rowsCount: 1 });

            const value = Number(values[0][1]);
            if (isNaN(value)) {
                throw new Error(
                    `value "${values[0][1]}" is not a number ; it cannot be interpreted`,
                );
            }

            const indicatorDto = {
                date: indicator.date,
                date_debut: dateHandler.substractMonth(indicator.date),
                valeur: value,
                indicateur: indicatorName,
                nom_service_public_numerique: productName,
                unite_mesure: 'unité',
                frequence_calcul: 'mensuelle',
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
    return indicatorDtos;
}

async function fetch() {
    const indicatorSummaryUrl = `https://www.data.gouv.fr/api/2/datasets/62d677bde7e4ca2c759142ce/resources/?page=1&type=main`;
    const indicatorSummaryApiResult = await axios.get<indicatorSummaryType>(indicatorSummaryUrl);

    const CREATED_PROCESSES_COUNT_REGEX =
        /^nb-procedures-creees-par-mois-[a-z]+(\d{4})(\d{2})(\d{2})-.+\.csv/;

    const fetchedData = [];

    for (const indicatorSummary of indicatorSummaryApiResult.data.data) {
        try {
            const regexMatch = indicatorSummary.title.match(CREATED_PROCESSES_COUNT_REGEX);
            if (!regexMatch || regexMatch.length !== 4) {
                continue;
            }
            const year = regexMatch[1];
            const month = regexMatch[2];
            const dayOfMonth = regexMatch[3];
            const date = `${year}-${month}-${dayOfMonth}`;
            const indicatorApiResult = await axios.get(indicatorSummary.url);
            fetchedData.push({ date, csv: indicatorApiResult.data });
        } catch (error) {
            logger.error({ productName, indicator: indicatorName, message: error as string });
        }
    }
    return fetchedData;
}

export { demarchesSimplifieesAdaptator };
