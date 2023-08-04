import { parseGithubUrl } from './parseGithubUrl';

describe('parseGithubUrl', () => {
    it('should return the repository owner and name', async () => {
        const { owner, name } = parseGithubUrl('https://github.com/betagouv/pad.numerique.gouv.fr');

        expect(owner).toBe('betagouv');
        expect(name).toBe('pad.numerique.gouv.fr');
    });
});
