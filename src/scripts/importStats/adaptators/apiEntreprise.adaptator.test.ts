import { apiEntrepriseAdaptator } from './apiEntreprise.adaptator';

describe('apiEntrepriseAdaptator', () => {
    it('should format the apiEntreprise output', () => {
        const apiEntrepriseOutput = {
            "Nombre d'appels pour une unité légale sur les 2 derniers mois": [
                { timestamp: '2023-05-01T00:00:00+02:00', count: 407125 },
            ],
            "Nombre d'appels totaux sur les 2 derniers mois": [
                { timestamp: '2023-06-01T00:00:00+02:00', count: 7997423 },
            ],
        };

        const formatted = apiEntrepriseAdaptator.map(apiEntrepriseOutput);

        expect(formatted).toEqual([
            {
                date: '2023-06-01',
                date_debut: '2023-05-01',
                valeur: 407125,
                est_periode: true,
                nom_service_public_numerique: 'api-entreprise',
                frequence_monitoring: 'mensuelle',
                est_automatise: true,
                indicateur: "Nombre d'appels pour une unité légale sur les 2 derniers mois",
                unite_mesure: 'unité',
            },
            {
                date: '2023-07-01',
                date_debut: '2023-06-01',
                valeur: 7997423,
                est_periode: true,
                nom_service_public_numerique: 'api-entreprise',
                frequence_monitoring: 'mensuelle',
                est_automatise: true,
                indicateur: "Nombre d'appels totaux sur les 2 derniers mois",
                unite_mesure: 'unité',
            },
        ]);
    });
});
