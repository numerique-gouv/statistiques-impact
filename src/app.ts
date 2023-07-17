import Express from 'express';
import { config } from './config';
import { router } from '../router';

async function runApp() {
    const app = Express();

    app.use('/', router);

    app.listen(config.PORT, async () => {
        console.log(`Server is running on port ${config.PORT}`);
    });
}

export { runApp };
