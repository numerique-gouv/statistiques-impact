import { DataSource } from 'typeorm';
import { config } from './config';
import { Indicator } from './modules/indicator/Indicator.entity';
import { LogEntry } from './modules/logEntry/LogEntry.entity';
import { Product } from './modules/product/Product.entity';
import { Team } from './modules/team';
import { Client } from './modules/client';

const dataSource = new DataSource({
    type: 'postgres',
    ssl: config.DATABASE_CONNECTION_IS_SSL,
    host: config.DATABASE_HOST,
    port: config.DATABASE_PORT,
    username: config.DATABASE_USER,
    password: config.DATABASE_PASSWORD,
    database: config.DATABASE_NAME,
    logging: ['warn', 'error'],
    entities: [Indicator, LogEntry, Product, Team, Client],
    subscribers: [],
    migrations: ['**/migrations/*.js'],
});

export { dataSource };
