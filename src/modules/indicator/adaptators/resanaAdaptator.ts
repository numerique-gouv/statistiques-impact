import { dateHandler, parsedDateType } from '../../../scripts/importStats/utils';
import { Product } from '../../product';
import { Indicator } from '../Indicator.entity';

function resanaAdaptator(
    csv: Array<Record<string, string | undefined>>,
    product: Product,
): Indicator {
    const indicator = new Indicator();
    let activeUsersCount = 0;
    const now = dateHandler.parseDate(new Date());
    const ONE_MONTH_AGO = dateHandler.substractMonth(now);

    for (let i = 0; i < csv.length; i++) {
        try {
            const row = csv[i];
            if (!row['derniere_connexion']) {
                console.warn(`No derniere_connexion for line ${i}`);
                continue;
            }
            const lastLoginDate = parseCsvDate(row['derniere_connexion']);

            if (dateHandler.compareDates(ONE_MONTH_AGO, lastLoginDate) >= 0) {
                activeUsersCount++;
            }
        } catch (error) {
            console.error(error);
        }
    }

    indicator.date = dateHandler.stringifyParsedDate(now);
    indicator.date_debut = dateHandler.stringifyParsedDate(ONE_MONTH_AGO);
    indicator.est_automatise = true;
    indicator.est_periode = true;
    indicator.frequence_monitoring = 'mensuelle';
    indicator.indicateur = 'utilisateurs actifs';
    indicator.unite_mesure = 'unité';
    indicator.valeur = activeUsersCount;
    indicator.product = product;

    return indicator;
}

function parseCsvDate(date: string): parsedDateType {
    const REGEX = /^(\d{4})(\d{2})(\d{2})/;
    const match = date.match(REGEX);
    if (!match) {
        throw new Error(`Wrongly formatted date: ${date}`);
    }
    const [_, year, month, dayOfMonth] = match;
    return dateHandler.parseStringDate(`${year}-${month}-${dayOfMonth}`);
}

export { resanaAdaptator };
