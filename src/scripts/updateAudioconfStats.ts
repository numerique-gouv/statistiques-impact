import axios from 'axios';
import { dataSource } from '../dataSource';
import { buildIndicatorService } from '../modules/indicator';
import { metabaseAdaptator } from './metabase.adaptator';

async function updateAudioconfStats() {
    await dataSource.initialize();

    const indicatorService = buildIndicatorService(dataSource);
    const URL =
        'https://stats.audioconf.numerique.gouv.fr/public/question/f98281a7-5bd6-4f09-8ec6-a278975adfb9.json';

    const result = await axios.get(URL);

    const formattedRows = metabaseAdaptator.format(result.data, 'month');
    const indicatorDtos = formattedRows.map((formattedRow) => ({
        nom_service_public_numerique: 'audioconf',
        indicateur: 'Conférences créées',
        valeur: formattedRow.value,
        unite_mesure: 'unité',
        frequence_calcul: 'mensuelle',
        date: formattedRow.date,
        date_debut: formattedRow.date_debut,
        est_periode: true,
    }));

    return indicatorService.upsertIndicators(indicatorDtos);
}

updateAudioconfStats();
