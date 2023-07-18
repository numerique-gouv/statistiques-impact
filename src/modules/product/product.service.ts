import { Product } from './Product.entity';
import { dataSource } from '../../dataSource';

export { buildProductService };

function buildProductService() {
    const productRepository = dataSource.getRepository(Product);
    const productService = {
        getProducts,
        createProduct,
    };

    return productService;

    async function getProducts() {
        return productRepository.find();
    }

    async function createProduct(name: string) {
        const product = new Product();
        product.name = name;

        return productRepository.save(product);
    }
}
