import axios from 'axios';
import { dataSource } from '../dataSource';
import { buildIndicatorService } from '../modules/indicator';
import { padApiAdaptator } from './padApi.adaptator';

async function updatePadStats() {
    await dataSource.initialize();

    const indicatorService = buildIndicatorService(dataSource);

    const URL = `https://pad.numerique.gouv.fr/stats/users/lastMonth`;
    const result = await axios.get(URL);
    const formattedApiOutput = padApiAdaptator.format(result.data);

    const indicatorDto = {
        nom_service_public_numerique: 'pad',
        indicateur: 'utilisateurs actifs',
        valeur: formattedApiOutput.value,
        unite_mesure: 'unité',
        frequence_calcul: 'mensuelle',
        date: formattedApiOutput.date,
        date_debut: formattedApiOutput.date_debut,
        est_periode: true,
    };

    return indicatorService.upsertIndicators([indicatorDto]);
}

updatePadStats();
