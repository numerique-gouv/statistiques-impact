import { Request } from 'express';

function extractBearerToken(req: Request) {
    const authorization = req.headers['authorization'];
    if (!authorization) {
        throw new Error(`No header "Authorization" present`);
    }

    const splitBearerToken = authorization.split(' ');
    if (splitBearerToken.length !== 2 || splitBearerToken[0] !== 'Bearer') {
        throw new Error(`Wrong format for Bearer token`);
    }
    const token = splitBearerToken[1];
    return token;
}

export { extractBearerToken };
