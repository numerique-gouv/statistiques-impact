import { documentationAdaptator, getLastMonthIndicator } from './documentation.adaptator';

describe('documentation', () => {
    it('should fetch the data', async () => {
        const data = await documentationAdaptator.fetch();

        expect(data.length).toBeGreaterThan(0);
    });

    it('should get the last month indicator', () => {
        const outlineUsers = [
            {
                id: 'b154',
                lastActiveAt: '2023-11-15T13:52:10.543Z',
            },
            {
                id: '04df',
                lastActiveAt: '2023-11-10T13:39:25.638Z',
            },
            {
                id: '9a1f',
                lastActiveAt: '2023-10-20T11:47:09.792Z',
            },
            {
                id: 'b959',
                lastActiveAt: '2023-10-10T11:24:20.903Z',
            },
            {
                id: 'c005',
                lastActiveAt: '2023-09-15T10:16:41.310Z',
            },
        ];
        const now = new Date('2023-11-15T14:27:50.625Z');

        const { activeUsersCount, date, date_debut } = getLastMonthIndicator(outlineUsers, now);

        expect(activeUsersCount).toEqual(3);
        expect(date).toEqual('2023-11-15');
        expect(date_debut).toEqual('2023-10-15');
    });
});
