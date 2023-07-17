import Express from 'express';
import 'reflect-metadata';
import { config } from './config';
import { router } from './router';
import { dataSource } from './dataSource';
import bodyParser from 'body-parser';

async function runApp() {
    await dataSource.initialize();
    console.log(`Data source has been initialized`);
    const app = Express();

    app.use('/', bodyParser.json(), router);

    app.listen(config.PORT, async () => {
        console.log(`Server is running on port ${config.PORT}`);
    });
}

export { runApp };
