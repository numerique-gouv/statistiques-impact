import axios from 'axios';
import { logger } from '../../../lib/logger';
import { dateHandler } from '../utils';
import { PRODUCTS } from '../../../constants';
import { config } from '../../../config';

const documentationAdaptator = { fetch };

type outlineApiOutputType = {
    pagination: {
        limit: number;
        offset: number;
        total: number;
    };
    data: Array<outlineUserApiType>;
};

type outlineUserApiType = { id: string; lastActiveAt: string };

const productName = PRODUCTS.DOCUMENTATION.name;
const indicatorName = 'utilisateurs actifs';

function getLastMonthIndicator(outlineUsers: Array<outlineUserApiType>, now: Date) {
    const date = dateHandler.formatDate(now.toISOString());
    const date_debut = dateHandler.substractMonth(date);
    const activeUsersCount = outlineUsers.filter((outlineUser) => {
        const parsedLastActiveAtDate = dateHandler.parseStringDate(outlineUser.lastActiveAt);
        const parsedDateDebut = dateHandler.parseStringDate(date_debut);
        return dateHandler.compareDates(parsedDateDebut, parsedLastActiveAtDate) >= 0;
    }).length;
    return { activeUsersCount, date, date_debut };
}

async function fetch() {
    const url = `https://documentation.beta.numerique.gouv.fr/api/users.list`;
    const headers = {
        Accept: 'application/json',
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${config.DOCUMENTATION_API_KEY}`,
    };
    let outlineUsers: Array<outlineUserApiType> = [];
    let offset = 0;
    const limit = 100;
    let total = -1;

    try {
        do {
            const body = {
                offset: `${offset}`,
                limit: `${limit}`,
                sort: 'lastActiveAt',
                direction: 'DESC',
                query: '',
                filter: 'all',
            };
            const { data } = await axios.post<outlineApiOutputType>(url, body, {
                headers,
            });
            outlineUsers.push(
                ...data.data
                    .map(({ id, lastActiveAt }) => ({ id, lastActiveAt }))
                    .filter(({ lastActiveAt }) => !!lastActiveAt),
            );
            total = data.pagination.total;
            offset += limit;
        } while (offset < total);
    } catch (error) {
        logger.error({
            productName,
            indicator: indicatorName,
            message: error as string,
        });
    }

    let indicatorDtos: any[] = [];
    const { date, date_debut, activeUsersCount } = getLastMonthIndicator(outlineUsers, new Date());

    indicatorDtos.push({
        date,
        date_debut,
        valeur: activeUsersCount,
        indicateur: indicatorName,
        nom_service_public_numerique: productName,
        unite_mesure: 'unité',
        frequence_monitoring: 'mensuelle',
        est_automatise: true,
        est_periode: true,
    });

    return indicatorDtos;
}

export { documentationAdaptator, getLastMonthIndicator };
