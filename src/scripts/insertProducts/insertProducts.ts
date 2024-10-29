import { PRODUCTS } from '../../constants';
import { dataSource } from '../../dataSource';
import { buildProductService } from '../../modules/product';

async function insertProducts() {
    console.log('INSERT PRODUCTS');
    console.log('===');
    console.log(`Initializing database...`);
    await dataSource.initialize();
    console.log(`Database initialized...`);
    console.log(`Inserting ${Object.keys(PRODUCTS).length} products...`);

    const productService = buildProductService(dataSource);

    await Promise.all(
        Object.values(PRODUCTS).map((PRODUCT) =>
            productService.upsertProduct({
                nom_service_public_numerique: PRODUCT.name,
            }),
        ),
    );
    console.log('INSERT PRODUCTS DONE!');
}

insertProducts();
