import { DataSource } from 'typeorm';
import { Product } from './Product.entity';

type formattedProductType = {
    id: string;
    nom_service_public_numerique: string;
    lastIndicatorDate: string | undefined;
    lastIndicators: string[];
    est_automatise: boolean;
};

function buildProductService(dataSource: DataSource) {
    const productRepository = dataSource.getRepository(Product);
    return {
        getProductByName,
        getProducts,
        upsertProduct,
    };

    async function getProductByName(productName: Product['nom_service_public_numerique']) {
        return productRepository.findOneByOrFail({ nom_service_public_numerique: productName });
    }

    async function getProducts() {
        const products = await productRepository.find({
            relations: ['indicators'],
            select: {
                indicators: { date: true, est_automatise: true, valeur: true, indicateur: true },
            },
        });
        const formattedProducts: Array<formattedProductType> = [];
        for (const product of products) {
            let est_automatise = false;
            let lastIndicators: string[] = [];
            let lastIndicatorDate: string | undefined = undefined;

            if (product.indicators.length > 0) {
                lastIndicatorDate = product.indicators.sort((b, a) =>
                    a.date.localeCompare(b.date),
                )[0].date;
                lastIndicators = product.indicators
                    .filter((indicator) => indicator.date === lastIndicatorDate)
                    .map((indicator) => `${indicator.valeur} ${indicator.indicateur}`);
                est_automatise = product.indicators.every((indicator) => indicator.est_automatise);
            }
            const formattedProduct: formattedProductType = {
                id: product.id,
                nom_service_public_numerique: product.nom_service_public_numerique,
                lastIndicators,
                lastIndicatorDate,
                est_automatise,
            };
            formattedProducts.push(formattedProduct);
        }

        return formattedProducts;
    }

    async function upsertProduct(productDto: Partial<Product>) {
        return productRepository.upsert({ ...productDto }, ['nom_service_public_numerique']);
    }
}

export { buildProductService };
