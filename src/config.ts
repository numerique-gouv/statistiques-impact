import dotenv from 'dotenv';
import pgConnectionString from 'pg-connection-string';

dotenv.config();

let databaseConfig: Record<string, string> = {};

if (process.env.DATABASE_URL) {
    const infos = pgConnectionString.parse(process.env.DATABASE_URL);
    databaseConfig.DATABASE_PORT = infos.port || '';
    databaseConfig.DATABASE_HOST = infos.host || '';
    databaseConfig.DATABASE_NAME = infos.database || '';
    databaseConfig.DATABASE_USER = infos.user || '';
    databaseConfig.DATABASE_PASSWORD = infos.password || '';
}

const config = {
    DATABASE_CONNECTION_IS_SSL: process.env.DATABASE_CONNECTION_IS_SSL === 'true',
    PORT: process.env.PORT || 3000,
    DATABASE_HOST: process.env.DATABASE_HOST || '',
    DATABASE_PASSWORD: process.env.DATABASE_PASSWORD || '',
    DATABASE_USER: process.env.DATABASE_USER || '',
    DATABASE_NAME: process.env.DATABASE_NAME || '',
    DATABASE_PORT: process.env.DATABASE_PORT ? Number(process.env.DATABASE_PORT) : 5432,
    ALLOWED_ORIGIN: process.env.ALLOWED_ORIGIN || '',
    GRIST_API_KEY: process.env.GRIST_API_KEY,
    GRIST_DOCUMENT_ID: process.env.GRIST_DOCUMENT_ID,
    GRIST_URL: process.env.GRIST_URL,
    DOCUMENTATION_API_KEY: process.env.DOCUMENTATION_API_KEY,
    ...databaseConfig,
};

export { config };
