import { padApiAdaptator } from './padApi.adaptator';

describe('', () => {
    it('should raise an error if the pad does not return the right format', () => {
        const padApiOutput = {};

        expect(() => padApiAdaptator.format(padApiOutput as any)).toThrowError(
            'The pad API did not return the right format',
        );
    });

    it('should return the right format', () => {
        const padApiOutput = {
            dateInf: '2023-06-19 00:00:00',
            dateSup: '2023-07-19 00:00:00',
            activeUsers: 333,
        };

        const formattedOutput = padApiAdaptator.format(padApiOutput);

        expect(formattedOutput).toEqual({
            date_debut: '2023-06-19',
            date: '2023-07-19',
            value: 333,
        });
    });
});
