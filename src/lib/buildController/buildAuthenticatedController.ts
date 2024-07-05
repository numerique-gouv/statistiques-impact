import { Request, Response } from 'express';
import httpStatus from 'http-status';
// import Joi from 'joi';
// import { User } from '../../modules/user';
import { dataSource } from '../../dataSource';
import { extractBearerToken } from './extractBearerToken';
import { crypto } from '../crypto';
// import { extractUserIdFromHeader } from './extractUserIdFromHeader';

export { buildAuthenticatedController };

function buildAuthenticatedController<
    paramsT extends Record<string, string>,
    queryT extends Record<string, string>,
    bodyT,
>(
    controller: (
        params: { query: queryT; urlParams: paramsT; body: bodyT; fileBuffer?: Buffer },
        clientId: string,
    ) => any | Promise<any>,
    options?: {
        // schema?: Joi.Schema;
        // checkAuthorization?: (params: paramsT, user: User) => void | Promise<void>;
    },
) {
    console.log('BUILD');
    return async (req: Request, res: Response) => {
        console.log('RUN');

        console.log(`${req.method} ${req.originalUrl}`);

        let payload: any;
        try {
            const token = extractBearerToken(req);
            payload = crypto.jwtVerify(token);
            if (!payload.clientId) {
                throw new Error(`No clientId specified`);
            }
        } catch (error) {
            console.error(error);
            res.sendStatus(httpStatus.UNAUTHORIZED);
            return;
        }

        const fileBuffer = req.file ? req.file.buffer : undefined;

        try {
            const result = await controller(
                {
                    query: req.query as queryT,
                    urlParams: req.params as paramsT,
                    body: req.body,
                    fileBuffer,
                },
                payload.clientId,
            );
            res.setHeader('Content-Type', 'application/json');
            res.send(result);
        } catch (error) {
            console.error(error);
            res.sendStatus(httpStatus.INTERNAL_SERVER_ERROR);
        }
    };
}
