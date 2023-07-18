import { DataSource } from 'typeorm';
import { config } from './config';
import { Indicator } from './modules/indicator';
import { Product } from './modules/product';

const dataSource = new DataSource({
    type: 'postgres',
    host: config.DATABASE_HOST,
    port: config.DATABASE_PORT,
    username: config.DATABASE_USER,
    password: config.DATABASE_PASSWORD,
    database: config.DATABASE_NAME,
    logging: true,
    entities: [Indicator, Product],
    subscribers: [],
    migrations: ['**/migrations/*.js'],
});

export { dataSource };
