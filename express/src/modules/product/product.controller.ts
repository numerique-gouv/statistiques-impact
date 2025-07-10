import { DataSource } from 'typeorm';
import { buildProductService } from './product.service';

export { buildProductController };

function buildProductController(dataSource: DataSource) {
    const productService = buildProductService(dataSource);
    const productController = {
        getProducts,
    };

    return productController;

    async function getProducts() {
        return productService.getProducts();
    }
}
