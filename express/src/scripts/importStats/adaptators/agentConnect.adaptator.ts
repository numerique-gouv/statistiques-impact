import axios from 'axios';
import { dateHandler } from '../utils';
import { logger } from '../../../lib/logger';
import { PRODUCTS } from '../../../constants';

const agentConnectAdaptator = { fetch };

const productName = PRODUCTS.AGENT_CONNECT.name;
const CONNEXIONS = ['Initiée', 'Réussie'] as const;

type agentConnectApiOutputType = Array<{
    Time: string;
    Connexion: (typeof CONNEXIONS)[number];
    Count: number;
}>;

function map(agentConnectOutputRows: agentConnectApiOutputType) {}

async function fetch() {
    const url =
        'https://stats.proconnect.gouv.fr/model/112-monthly-active-users-over-time';
    const result = await axios.get<agentConnectApiOutputType>(url);

    const agentConnectOutputRows = result.data;

    const indicatorDtos = [];
    const grouppedIndicatorsByDate: Record<
        string,
        Record<(typeof CONNEXIONS)[number], number>
    > = {};
    try {
        agentConnectOutputRows.forEach((agentConnectOutputRow) => {
            const date = dateHandler.formatDate(agentConnectOutputRow.Time);
            if (!CONNEXIONS.includes(agentConnectOutputRow.Connexion)) {
                throw new Error(
                    `agentConnectOutputRow.Connexion "${
                        agentConnectOutputRow.Connexion
                    }" does not belong to [${CONNEXIONS.join(', ')}] `,
                );
            }
            const count = Number(agentConnectOutputRow.Count);
            if (isNaN(count)) {
                throw new Error(
                    `agentConnectOutputRow.Connexion ${agentConnectOutputRow.Connexion} is NaN`,
                );
            }

            grouppedIndicatorsByDate[date] = {
                ...grouppedIndicatorsByDate[date],
                [agentConnectOutputRow.Connexion]: count,
            };
        });
    } catch (error) {
        logger.error({
            productName,
            indicator: 'connexions réussies',
            message: error as string,
        });
    }
    const dates_debut = Object.keys(grouppedIndicatorsByDate);
    for (const date_debut of dates_debut) {
        try {
            const date = dateHandler.addMonth(date_debut);
            if (!grouppedIndicatorsByDate[date_debut]['Réussie']) {
                throw new Error(`No value for Connexions réussies`);
            }

            indicatorDtos.push({
                date_debut,
                date,
                indicateur: 'connexions réussies',
                unite_mesure: 'unité',
                nom_service_public_numerique: productName,
                frequence_monitoring: 'mensuelle',
                est_automatise: true,
                est_periode: true,
                valeur: grouppedIndicatorsByDate[date_debut]['Réussie'],
            });

            if (!grouppedIndicatorsByDate[date_debut]['Initiée']) {
                throw new Error(`No value for Connexions initiées`);
            }

            const percentage =
                grouppedIndicatorsByDate[date_debut]['Initiée'] /
                (grouppedIndicatorsByDate[date_debut]['Initiée'] +
                    grouppedIndicatorsByDate[date_debut]['Réussie']);

            indicatorDtos.push({
                date_debut,
                date,
                indicateur: '% de connexions réussies',
                unite_mesure: '%',
                nom_service_public_numerique: productName,
                frequence_monitoring: 'mensuelle',
                est_automatise: true,
                est_periode: true,
                valeur: Number(percentage.toFixed(2)),
            });
        } catch (error) {
            logger.error({
                productName,
                indicator: 'pourcentage de connexions réussies',
                message: error as string,
            });
        }
    }

    return indicatorDtos;
}

export { agentConnectAdaptator };
