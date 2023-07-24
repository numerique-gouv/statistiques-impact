import { audioconfAdaptator } from './audioconf.adaptator';

describe('audioconfAdaptator', () => {
    it('should format the audioconf output', () => {
        const audioconfOutputRows = [{ 'Date Begin': '2022-12-01T00:00:00Z', Count: 1234 }];

        const formatted = audioconfAdaptator.map(audioconfOutputRows);

        expect(formatted).toEqual([
            {
                date: '2023-01-01',
                date_debut: '2022-12-01',
                valeur: 1234,
                est_periode: true,
                frequence_calcul: 'mensuelle',
                indicateur: 'conférences de plus de deux minutes',
                unite_mesure: 'unité',
            },
        ]);
    });
});
