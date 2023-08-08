import { DataSource } from 'typeorm';
import { Product } from './Product.entity';

function buildProductService(dataSource: DataSource) {
    const productRepository = dataSource.getRepository(Product);
    return {
        getProducts,
        upsertProduct,
    };

    async function getProducts() {
        return productRepository.find();
    }

    async function upsertProduct(productDto: Partial<Product>) {
        return productRepository.upsert(productDto, ['nom_service_public_numerique']);
    }
}

export { buildProductService };
