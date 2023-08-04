import axios from 'axios';
import { PRODUCTS } from '../../constants';
import { extractMetabaseVersion } from './extractMetabaseVersion';
import { dataSource } from '../../dataSource';
import { buildProductService } from '../../modules/product';
import { logger } from '../../lib/logger';

async function importMetabaseVersions() {
    await dataSource.initialize();
    const productInfoService = buildProductService(dataSource);

    for (const [_, product] of Object.entries(PRODUCTS)) {
        if (product.metabaseUrl) {
            try {
                const { data } = await axios.get(product.metabaseUrl);
                const metabaseVersion = await extractMetabaseVersion(data);
                await productInfoService.upsertProduct({
                    nom_service_public_numerique: product.name,
                    metabaseVersion,
                });
            } catch (error) {
                logger.error({ productName: product.name, message: error as string });
            }
        }
    }
}

importMetabaseVersions();
