import axios from 'axios';
import { PRODUCTS } from '../../constants';
import { extractMetabaseVersion } from './extractMetabaseVersion';
import { dataSource } from '../../dataSource';
import { buildProductInfoService } from '../../modules/productInfo';
import { logger } from '../../lib/logger';

async function importMetabaseVersions() {
    await dataSource.initialize();
    const productInfoService = buildProductInfoService(dataSource);

    for (const [_, product] of Object.entries(PRODUCTS)) {
        if (product.metabaseUrl) {
            try {
                const { data } = await axios.get(product.metabaseUrl);
                const metabaseVersion = await extractMetabaseVersion(data);
                await productInfoService.insertProductInfo({
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
