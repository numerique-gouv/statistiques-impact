import { Request } from 'express';

function extractAdminApiKey(req: Request) {
    const apiKey = req.headers['x-api-key'];
    if (!apiKey) {
        throw new Error('API key is missing');
    }
    return apiKey;
}

export { extractAdminApiKey };
