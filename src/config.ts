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
    PORT: process.env.PORT || 3000,
    DATABASE_HOST: process.env.DATABASE_HOST || '',
    DATABASE_PASSWORD: process.env.DATABASE_PASSWORD || '',
    DATABASE_USER: process.env.DATABASE_USER || '',
    DATABASE_NAME: process.env.DATABASE_NAME || '',
    DATABASE_PORT: process.env.DATABASE_PORT ? Number(process.env.DATABASE_PORT) : 5432,
    ...databaseConfig,
};

export { config };
