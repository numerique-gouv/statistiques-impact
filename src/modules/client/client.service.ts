import { Client } from './Client';
import { DataSource } from 'typeorm';

export { buildClientService };

function buildClientService(dataSource: DataSource) {
    const clientRepository = dataSource.getRepository(Client);
    const clientService = {};

    return clientService;
}
