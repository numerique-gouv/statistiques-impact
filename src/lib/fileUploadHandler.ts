import csvParser from 'csv-parser';
import multer from 'multer';
import { Readable } from 'stream';
import { pipeline } from 'stream/promises';

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

const uploadSingleFileMiddleware = upload.single('file');

async function parseCsv(fileBuffer: Buffer) {
    const results: any[] = [];
    try {
        await pipeline(Readable.from(fileBuffer.toString()), csvParser(), async function* (source) {
            for await (const chunk of source) {
                results.push(chunk);
            }
        });

        return results;
    } catch (error: any) {
        throw new Error(`Could not parse CSV file : ${error.message}`);
    }
}

const fileUploadHandler = {
    uploadSingleFileMiddleware,
    parseCsv,
};

export { fileUploadHandler };
