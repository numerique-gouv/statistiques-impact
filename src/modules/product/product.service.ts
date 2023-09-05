import { DataSource } from 'typeorm';
import { Product } from './Product.entity';

function buildProductService(dataSource: DataSource) {
    const productRepository = dataSource.getRepository(Product);
    return {
        getProducts,
        upsertProduct,
    };

    async function getProducts() {
        const products = await productRepository.find({
            relations: ['indicators'],
            select: { indicators: { date: true } },
        });
        return products.map((product) => ({
            id: product.id,
            nom_service_public_numerique: product.nom_service_public_numerique,
            lastStatisticDate: product.indicators.length
                ? product.indicators.sort()[product.indicators.length - 1].date
                : undefined,
        }));
    }

    async function upsertProduct(productDto: Partial<Product>) {
        return productRepository.upsert(productDto, ['nom_service_public_numerique']);
    }
}

export { buildProductService };
