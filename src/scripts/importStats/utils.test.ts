import { dateHandler } from './utils';

describe('utils', () => {
    describe('dateHandler', () => {
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

        describe('parseDate', () => {
            it('parsed the date', () => {
                const date = '2023-08-01';

                const parsedDate = dateHandler.parseDate(date);

                expect(parsedDate).toEqual({ year: 2023, month: 8, dayOfMonth: 1 });
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