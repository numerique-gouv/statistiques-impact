import { metabaseAdaptator } from './metabase.adaptator';

describe('metabaseAdaptator', () => {
    it('should format the metabase output', () => {
        const metabaseOutputRows = [
            { 'Date Begin': '2022-12-01T00:00:00Z', Count: 1234 },
            { 'Date Begin': '2023-01-01T00:00:00Z', Count: 9577 },
            { 'Date Begin': '2023-02-01T00:00:00Z', Count: 8550 },
            { 'Date Begin': '2023-03-01T00:00:00Z', Count: 10364 },
            { 'Date Begin': '2023-04-01T00:00:00Z', Count: 7751 },
            { 'Date Begin': '2023-05-01T00:00:00Z', Count: 7178 },
            { 'Date Begin': '2023-06-01T00:00:00Z', Count: 8336 },
            { 'Date Begin': '2023-07-01T00:00:00Z', Count: 3543 },
        ];

        const formatted = metabaseAdaptator.format(metabaseOutputRows, 'month');

        expect(formatted).toEqual([
            { date: '2023-01-01', date_debut: '2022-12-01', value: 1234 },
            { date: '2023-02-01', date_debut: '2023-01-01', value: 9577 },
            { date: '2023-03-01', date_debut: '2023-02-01', value: 8550 },
            { date: '2023-04-01', date_debut: '2023-03-01', value: 10364 },
            { date: '2023-05-01', date_debut: '2023-04-01', value: 7751 },
            { date: '2023-06-01', date_debut: '2023-05-01', value: 7178 },
            { date: '2023-07-01', date_debut: '2023-06-01', value: 8336 },
        ]);
    });
});
