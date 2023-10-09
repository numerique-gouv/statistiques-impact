import { padAdaptator } from './pad.adaptator';

describe('pad', () => {
    it('should raise an error if the pad does not return the right format', () => {
        const padApiOutput = {};

        expect(() => padAdaptator.map(padApiOutput as any)).toThrowError(
            'The pad API did not return the right format',
        );
    });

    it('should return the right format', () => {
        const padApiOutput = {
            dateInf: '2023-06-19 00:00:00',
            dateSup: '2023-07-19 00:00:00',
            activeUsers: 333,
        };

        const formattedOutput = padAdaptator.map(padApiOutput);

        expect(formattedOutput).toEqual([
            {
                date: '2023-07-19',
                date_debut: '2023-06-19',
                est_periode: true,
                frequence_monitoring: 'mensuelle',
                est_automatise: true,
                nom_service_public_numerique: 'pad',
                indicateur: 'utilisateurs actifs',
                unite_mesure: 'unité',
                valeur: 333,
            },
        ]);
    });
});
