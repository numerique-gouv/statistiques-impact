import { webinaireAdaptator } from './webinaire.adaptator';

describe('webinaireAdaptator', () => {
    it('should format the webinaire output', () => {
        const webinaireOutputRows = [
            { 'Created At': '2021-06-01T00:00:00Z', 'Nombre de lignes': 295 },
        ];

        const formatted = webinaireAdaptator.map(webinaireOutputRows);

        expect(formatted).toEqual([
            {
                date: '2021-07-01',
                date_debut: '2021-06-01',
                valeur: 295,
                est_periode: true,
                nom_service_public_numerique: 'webinaire',
                frequence_calcul: 'mensuelle',
                est_automatise: true,
                indicateur: 'conférences',
                unite_mesure: 'unité',
            },
        ]);
    });
});
