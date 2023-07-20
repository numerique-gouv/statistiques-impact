import axios from 'axios';
import { dateHandler, parseCsv } from './utils';

const demarchesSimplifieesAdaptator = { map, fetch };

type indicatorSummaryType = {
    data: Array<{
        id: string;
        title: string;
        url: string;
    }>;
};

function map(indicators: Array<{ date: string; csv: string }>) {
    const indicatorDtos = [];
    for (const indicator of indicators) {
        const parsedCsv = parseCsv(indicator.csv);
        if (parsedCsv.length !== 2) {
            console.warn(
                `parsedCsv: [${parsedCsv.join(
                    ';',
                )}] does not have two lines ; its content cannot be interpreted`,
            );
            continue;
        }
        const row = parsedCsv[1];
        if (row.length !== 2) {
            console.warn(
                `row [${row.join(
                    ',',
                )}] does not have two cells ; its content cannot be interpreted`,
            );
            continue;
        }
        const value = Number(row[1]);
        if (isNaN(value)) {
            console.warn(`value ${row[1]} is not a number ; it cannot be interpreted`);
            continue;
        }

        const indicatorDto = {
            date: indicator.date,
            date_debut: dateHandler.substractMonth(indicator.date),
            valeur: value,
            indicateur: 'procédures créées',
            unite_mesure: 'unité',
            frequence_calcul: 'mensuelle',
            est_periode: true,
        };
        indicatorDtos.push(indicatorDto);
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
    }
    return fetchedData;
}

export { demarchesSimplifieesAdaptator };
