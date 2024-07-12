import { Request, Response } from 'express';
import httpStatus from 'http-status';

export { buildController };

function buildController<paramsT extends Record<string, string>, bodyT>(
    controller: ({ urlParams, body }: { urlParams: paramsT; body: bodyT }) => any | Promise<any>,
) {
    return async (req: Request, res: Response) => {
        console.log(`${req.method} ${req.originalUrl}`);
        try {
            const result = await controller({ urlParams: req.params as paramsT, body: req.body });
            res.send(result);
        } catch (error) {
            console.error(error);
            res.sendStatus(httpStatus.INTERNAL_SERVER_ERROR);
        }
    };
}
