import { DataSource } from 'typeorm';
import { buildClientService } from './client.service';

export { buildClientController };

function buildClientController(dataSource: DataSource) {
    const clientService = buildClientService(dataSource);
    const clientController = {
        updateClientSecret,
        createToken,
        createClient,
    };

    async function createToken(params: { body: { clientId: string; clientSecret: string } }) {
        return clientService.createToken(params.body.clientId, params.body.clientSecret);
    }

    async function updateClientSecret(params: {
        body: { previousClientSecret: string };
        urlParams: { clientId: string };
    }) {
        return clientService.updateClientSecret(
            params.urlParams.clientId,
            params.body.previousClientSecret,
        );
    }

    async function createClient(params: { urlParams: { productName: string } }) {
        return clientService.createClient(params.urlParams.productName);
    }

    return clientController;
}
