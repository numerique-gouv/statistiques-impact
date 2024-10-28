import { tchapAdaptator } from './tchap.adaptator';

describe('tchapAdaptator', () => {
    it('should fetch the tchap output', () => {
        expect(tchapAdaptator.fetch()).rejects.toThrow();
    });
});
