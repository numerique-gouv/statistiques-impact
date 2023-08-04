import { computeBeginningDateToWatch } from './computeBeginningDateToWatch';

describe('computeBeginningDateToWatch', () => {
    it('should compute the date since which you want to fetch data', async () => {
        const now = new Date('2023-08-04T11:19:28.874Z');
        const monthsToWatch = 3;
        const beginningDateToWatch = computeBeginningDateToWatch(now, monthsToWatch);

        expect(beginningDateToWatch).toBe('2023-05-06T11:19:28.874Z');
    });
});
