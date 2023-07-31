import { tchapAdaptator } from './tchap.adaptator';

describe('tchapAdaptator', () => {
    it('should format the tchap output', () => {
        const tchapOutputRows = [
            {
                Month: '2023-03-01T00:00:00+01:00',
                'Valeurs distinctes de User ID': 149550,
            },
        ];

        const formatted = tchapAdaptator.map(tchapOutputRows);

        expect(formatted).toEqual([
            {
                date: '2023-04-01',
                date_debut: '2023-03-01',
                valeur: 149550,
                est_periode: true,
                nom_service_public_numerique: 'tchap',
                frequence_calcul: 'mensuelle',
                indicateur: 'utilisateurs actifs',
                unite_mesure: 'unité',
            },
        ]);
    });
});
