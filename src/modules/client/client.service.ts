import { Client } from './Client.entity';
import { DataSource } from 'typeorm';

export { buildClientService };

function buildClientService(dataSource: DataSource) {
    const clientRepository = dataSource.getRepository(Client);
    const clientService = {};

    return clientService;
}
