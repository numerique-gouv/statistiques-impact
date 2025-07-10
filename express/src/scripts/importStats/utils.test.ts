import { dateHandler, parseCsv } from './utils';

describe('utils', () => {
    describe('parseCsv', () => {
        it('should parse the csv', () => {
            const csv = 'mois,nb_procedures_creees_par_mois\nJune,1378\n';

            const parsedCsv = parseCsv(csv);

            expect(parsedCsv).toEqual({
                header: ['mois', 'nb_procedures_creees_par_mois'],
                values: [['June', '1378']],
            });
        });
    });
    describe('dateHandler', () => {
        describe('compareDates', () => {
            it('returns 0 when dates are equal', () => {
                const dateA = { year: 2023, month: 2, dayOfMonth: 3 };
                const dateB = { year: 2023, month: 2, dayOfMonth: 3 };

                const result = dateHandler.compareDates(dateA, dateB);

                expect(result).toBe(0);
            });

            it('returns 1 when date A is older than date B', () => {
                const dateA = { year: 2019, month: 3, dayOfMonth: 3 };
                const dateB = { year: 2023, month: 2, dayOfMonth: 3 };

                const result = dateHandler.compareDates(dateA, dateB);

                expect(result).toBe(1);
            });

            it('returns -1 when date B is older than date A', () => {
                const dateA = { year: 2023, month: 3, dayOfMonth: 3 };
                const dateB = { year: 2023, month: 2, dayOfMonth: 3 };

                const result = dateHandler.compareDates(dateA, dateB);

                expect(result).toBe(-1);
            });
        });

        describe('parseReadableDate', () => {
            it('parses the date within a year', () => {
                const humanReadableDate = 'août 2022';

                const { date_debut, date } = dateHandler.parseReadableDate(humanReadableDate);

                expect(date_debut).toBe('2022-08-01');
                expect(date).toBe('2022-09-01');
            });

            it('parses the date between two years', () => {
                const humanReadableDate = 'décembre 2022';

                const { date_debut, date } = dateHandler.parseReadableDate(humanReadableDate);

                expect(date_debut).toBe('2022-12-01');
                expect(date).toBe('2023-01-01');
            });
        });

        describe('parseStringDate', () => {
            it('parsed the date', () => {
                const date = '2023-08-01';

                const parsedDate = dateHandler.parseStringDate(date);

                expect(parsedDate).toEqual({ year: 2023, month: 8, dayOfMonth: 1 });
            });
        });

        describe('formatDate', () => {
            it('formats the date', () => {
                const date = '2023-06-27 00:00:00';

                const formattedDate = dateHandler.formatDate(date);

                expect(formattedDate).toEqual('2023-06-27');
            });

            it('throw an error if not well formatted', () => {
                const date = '2023-067-27 00:00:00';

                expect(() => dateHandler.formatDate(date)).toThrow();
            });
        });
        describe('addMonth', () => {
            it('should add a month at the beginning of the year', () => {
                const date = '2023-01-01';

                const newDate = dateHandler.addMonth(date);

                expect(newDate).toBe('2023-02-01');
            });

            it('should add a month at the end of the year', () => {
                const date = '2023-12-01';

                const newDate = dateHandler.addMonth(date);

                expect(newDate).toBe('2024-01-01');
            });
        });

        describe('substractMonth', () => {
            it('should substract a month at the beginning of the year', () => {
                const date = '2023-01-01';

                const newDate = dateHandler.substractMonth(date);

                expect(newDate).toBe('2022-12-01');
            });

            it('should substract a month at the end of the year', () => {
                const date = '2023-12-01';

                const newDate = dateHandler.substractMonth(date);

                expect(newDate).toBe('2023-11-01');
            });
        });
    });
});
