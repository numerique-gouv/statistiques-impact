import { dataSource } from '../../dataSource';
import { buildProductService } from '../../modules/product';
import { api } from '../../lib/api';

async function importProducts() {
    await dataSource.initialize();
    const productService = buildProductService(dataSource);

    const products = await api.fetchProducts();
    for (const product of products) {
        await productService.upsertProduct({
            nom_service_public_numerique: product.fields.slug,
        });
    }
    return;
}

importProducts();
