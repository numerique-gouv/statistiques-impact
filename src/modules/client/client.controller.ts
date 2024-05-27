import { DataSource } from 'typeorm';
import { buildClientService } from './client.service';

export { buildClientController };

function buildClientController(dataSource: DataSource) {
    const clientService = buildClientService(dataSource);
    const clientController = {};

    return clientController;
}
