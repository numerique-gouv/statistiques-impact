import axios from 'axios';
import { dateHandler } from '../utils';
import { PRODUCTS } from '../../../constants';
import { indicatorDtoType } from '../../../modules/indicator';

const hubeeAdaptator = { fetch };

const productName = PRODUCTS.HUBEE.name;

type hubeeApiOutputType = {
    getNumberTDByStatus: Array<{ DONE: number; REFUSED: number; ADD_AWAITING: number }>;
};

async function fetch() {
    const url = 'https://hubee-prod.osc-fr1.scalingo.io/statistiquesJSON';
    const result = await axios.get(url);
    const hubeeApiOutput: hubeeApiOutputType = result.data;
    assertOutputRightFormat(hubeeApiOutput);

    const indicatorDtos: indicatorDtoType[] = [];
    const now = new Date();

    const parsedNow = dateHandler.parseDate(now);
    const beginningOfMonthDate = { ...parsedNow, dayOfMonth: 1 };
    let date_fin = beginningOfMonthDate;
    let date_debut = dateHandler.substractMonth(beginningOfMonthDate);

    const indicatorName =
        'dossiers traités (avis favorable, avis défavorable, en attente de complément)';
    for (
        let length = hubeeApiOutput.getNumberTDByStatus.length, index = length - 1;
        index >= 0;
        index--
    ) {
        const monthIndicator = hubeeApiOutput.getNumberTDByStatus[index];
        const value =
            Number(monthIndicator.DONE) +
            Number(monthIndicator.REFUSED) +
            Number(monthIndicator.ADD_AWAITING);
        indicatorDtos.push({
            date_debut: dateHandler.stringifyParsedDate(date_debut),
            date: dateHandler.stringifyParsedDate(date_fin),
            indicateur: indicatorName,
            unite_mesure: 'unité',
            nom_service_public_numerique: productName,
            frequence_monitoring: 'mensuelle',
            est_automatise: true,
            est_periode: true,
            valeur: value,
        });

        date_fin = date_debut;
        date_debut = dateHandler.substractMonth(date_fin);
    }

    return indicatorDtos;
}

function assertOutputRightFormat(hubeeApiOutput: hubeeApiOutputType) {
    const STATUSES = ['DONE', 'REFUSED', 'ADD_AWAITING'];
    if (!hubeeApiOutput.getNumberTDByStatus) {
        throw new Error(`getNumberTDByStatus not defined`);
    }

    for (const monthIndicator of hubeeApiOutput.getNumberTDByStatus) {
        const missingStatus = STATUSES.find(
            (status) => !Object.keys(monthIndicator).includes(status),
        );
        if (!!missingStatus) {
            throw new Error(`Missing status: ${missingStatus}`);
        }
        if (Object.values(monthIndicator).some((value) => isNaN(Number(value)))) {
            throw new Error(
                `Error parsing values of monthIndicator: [${Object.values(monthIndicator).join(
                    ', ',
                )}]`,
            );
        }
    }
}
export { hubeeAdaptator, assertOutputRightFormat };
