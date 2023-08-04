import { DataSource } from 'typeorm';
import { config } from './config';
import { Indicator } from './modules/indicator/Indicator.entity';
import { LogEntry } from './modules/logEntry/LogEntry.entity';
import { Product } from './modules/product/Product.entity';

const dataSource = new DataSource({
    type: 'postgres',
    host: config.DATABASE_HOST,
    port: config.DATABASE_PORT,
    username: config.DATABASE_USER,
    password: config.DATABASE_PASSWORD,
    database: config.DATABASE_NAME,
    logging: true,
    entities: [Indicator, LogEntry, Product],
    subscribers: [],
    migrations: ['**/migrations/*.js'],
});

export { dataSource };
