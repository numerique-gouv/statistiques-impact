import { PRODUCTS } from '../../constants';
import { dataSource } from '../../dataSource';
import { buildProductService } from '../../modules/product';

async function importProducts() {
    await dataSource.initialize();
    const productService = buildProductService(dataSource);

    for (const [_, product] of Object.entries(PRODUCTS)) {
        await productService.upsertProduct({ nom_service_public_numerique: product.name });
    }
}

importProducts();
