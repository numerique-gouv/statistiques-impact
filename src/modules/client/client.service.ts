import { Client } from './Client.entity';
import { crypto } from '../../lib/crypto';
import { Product, buildProductService } from '../product';
import { DataSource } from 'typeorm';

export { buildClientService };

function buildClientService(dataSource: DataSource) {
    const productService = buildProductService(dataSource);
    const clientRepository = dataSource.getRepository(Client);
    const clientService = {
        createToken,
        createClient,
    };

    async function createToken(clientId: string, clientSecret: string) {
        const client = await clientRepository.findOneByOrFail({ id: clientId });

        if (client.secret === clientSecret) {
            throw new Error(`Wrong secret for clientId ${clientId}`);
        }

        const payload = {
            clientId,
        };

        const jwtToken = crypto.jwtSign(payload);

        return jwtToken;
    }

    async function createClient(productName: Product['nom_service_public_numerique']) {
        const product = await productService.getProductByName(productName);

        const client = new Client();
        client.product = product;
        client.secret = crypto.generateSecret();

        const result = await clientRepository.insert(client);
        const id = result.identifiers[0]['id'];

        return clientRepository.findOneByOrFail({ id });
    }

    return clientService;
}
