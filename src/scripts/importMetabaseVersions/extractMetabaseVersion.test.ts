import { extractMetabaseVersion } from './extractMetabaseVersion';
import { promises as fs } from 'fs';

describe('extractMetabaseVersion', () => {
    it('should return the right version', async () => {
        const pathname = __dirname + '/audioconfMetabase.html';
        const html = await fs.readFile(pathname);

        const metabaseVersion = await extractMetabaseVersion(html.toString());

        expect(metabaseVersion).not.toBe(undefined);
    });
});
