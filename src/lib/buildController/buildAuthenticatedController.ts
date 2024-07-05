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
        params: { query: queryT; urlParams: paramsT; body: bodyT },
        clientId: string,
    ) => any | Promise<any>,
    options?: {
        // schema?: Joi.Schema;
        // checkAuthorization?: (params: paramsT, user: User) => void | Promise<void>;
    },
) {
    return async (req: Request, res: Response) => {
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

        try {
            const result = await controller(
                {
                    query: req.query as queryT,
                    urlParams: req.params as paramsT,
                    body: req.body,
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
