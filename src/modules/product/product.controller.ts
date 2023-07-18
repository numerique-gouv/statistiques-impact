import { buildProductService } from './product.service';

export { buildProductController };

function buildProductController() {
    const productService = buildProductService();
    const productController = {
        getProducts,
        createProduct,
    };

    return productController;

    async function getProducts() {
        return productService.getProducts();
    }

    async function createProduct(params: { body: { name: string } }) {
        return productService.createProduct(params.body.name);
    }
}
