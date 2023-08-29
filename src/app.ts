import Express, { Response } from 'express';
import cors from 'cors';
import 'reflect-metadata';
import { config } from './config';
import { buildRouter } from './router';
import { dataSource } from './dataSource';
import bodyParser from 'body-parser';
import path from 'path';

async function runApp() {
    await dataSource.initialize();
    console.log(`Data source has been initialized`);
    const app = Express();
    const router = buildRouter(dataSource);

    app.use('/api', cors({ origin: 'http://localhost:3000' }), bodyParser.json(), router);

    app.use(Express.static(path.join(__dirname, '..', 'src', 'client', 'build')));

    app.get('/*', (_, res: Response) => {
        res.sendFile(path.join(__dirname, '..', 'src', 'client', 'build', 'index.html'));
    });

    app.listen(config.PORT, async () => {
        console.log(`Server is running on port ${config.PORT}`);
    });
}

export { runApp };
