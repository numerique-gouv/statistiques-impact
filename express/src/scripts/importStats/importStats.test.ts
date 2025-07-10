import { indicatorsToUpdate } from './adaptators';
test.concurrent.each(Object.entries(indicatorsToUpdate))(
    "indicator '%s'",
    async (_productName, adaptator) => {
        await expect(adaptator.fetch()).resolves.not.toThrowError();
    },
    10000,
);
