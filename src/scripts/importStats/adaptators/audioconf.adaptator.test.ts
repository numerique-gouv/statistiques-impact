import { audioconfAdaptator } from './audioconf.adaptator';

describe('audioconfAdaptator', () => {
    it('should format the audioconf output', () => {
        const audioconfOutputRows = [
            { 'Date Begin': '2022-12-01T00:00:00Z', 'Nombre de lignes': 1234 },
        ];

        const formatted = audioconfAdaptator.map(audioconfOutputRows);

        expect(formatted).toEqual([
            {
                date: '2023-01-01',
                date_debut: '2022-12-01',
                valeur: 1234,
                est_periode: true,
                nom_service_public_numerique: 'audioconf',
                frequence_monitoring: 'mensuelle',
                est_automatise: true,
                indicateur: 'conférences de plus de deux minutes',
                unite_mesure: 'unité',
            },
        ]);
    });
});
