import nodeCrypto from 'crypto';
import jwt from 'jsonwebtoken';
import { config } from '../config';

const crypto = { generateSecret, jwtSign, jwtVerify };

function generateSecret() {
    return nodeCrypto.randomBytes(64).toString('hex');
}

function jwtSign(payload: Object) {
    return jwt.sign(payload, config.JWT_SECRET, { expiresIn: '1d' });
}

function jwtVerify(token: string) {
    return jwt.verify(token, config.JWT_SECRET) as any;
}
export { crypto };
