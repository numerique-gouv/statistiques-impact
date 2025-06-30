import { Request, Response } from 'express';
import httpStatus from 'http-status';
import { extractBearerToken } from './extractBearerToken';
import { crypto } from '../crypto';
import { AppError } from '../../error';
import { extractAdminApiKey } from './extractAdminApiKey';
import { config } from '../../config';

export { buildAdminAuthenticatedController };

function buildAdminAuthenticatedController<
    paramsT extends Record<string, string>,
    queryT extends Record<string, string>,
    bodyT,
>(
    controller: (params: {
        query: queryT;
        urlParams: paramsT;
        body: bodyT;
        fileBuffer?: Buffer;
    }) => any | Promise<any>,
) {
    return async (req: Request, res: Response) => {
        console.log(`${req.method} ${req.originalUrl}`);

        try {
            const adminApiKey = extractAdminApiKey(req);
            if (adminApiKey !== config.ADMIN_API_KEY) {
                throw new Error('Invalid API key');
            }
        } catch (error) {
            console.error(error);
            res.sendStatus(httpStatus.UNAUTHORIZED);
            return;
        }

        try {
            const result = await controller({
                query: req.query as queryT,
                urlParams: req.params as paramsT,
                body: req.body,
                fileBuffer: req.file ? req.file.buffer : undefined,
            });
            res.setHeader('Content-Type', 'application/json');
            res.send(result);
        } catch (error) {
            console.error(error);
            if (error instanceof AppError) {
                res.status(error.statusCode).send(error.message);
            } else {
                res.sendStatus(httpStatus.INTERNAL_SERVER_ERROR);
            }
        }
    };
}
