import { apiParticulierAdaptator } from './apiParticulier.adaptator';

describe('apiParticulierAdaptator', () => {
    it('should format the apiParticulier output', () => {
        const apiParticulierOutput = {
            'Nombre de pièces justificatives transmises sur les 2 derniers mois': [
                { timestamp: '2023-05-01T00:00:00+02:00', 'Nb appels': 647205 },
            ],
            'Nombre de quotients familiaux transmis sur les 2 derniers mois': [
                { timestamp: '2023-06-01T00:00:00+02:00', 'Nb appels': 543321 },
            ],
        };

        const formatted = apiParticulierAdaptator.map(apiParticulierOutput);

        expect(formatted).toEqual([
            {
                date: '2023-06-01',
                date_debut: '2023-05-01',
                valeur: 647205,
                est_periode: true,
                nom_service_public_numerique: 'api-particulier',
                frequence_calcul: 'mensuelle',
                est_automatise: true,
                indicateur: 'Nombre de pièces justificatives transmises sur les 2 derniers mois',
                unite_mesure: 'unité',
            },
            {
                date: '2023-07-01',
                date_debut: '2023-06-01',
                valeur: 543321,
                est_periode: true,
                nom_service_public_numerique: 'api-particulier',
                frequence_calcul: 'mensuelle',
                est_automatise: true,
                indicateur: 'Nombre de quotients familiaux transmis sur les 2 derniers mois',
                unite_mesure: 'unité',
            },
        ]);
    });
});
