import { DataSource } from 'typeorm';
import { Product } from './Product.entity';
import { Team } from '../team';

function buildProductService(dataSource: DataSource) {
    const productRepository = dataSource.getRepository(Product);
    return {
        getProducts,
        upsertProduct,
    };

    async function getProducts() {
        const products = await productRepository.find({
            relations: ['indicators'],
            select: { indicators: { date: true, isAutomatic: true } },
        });
        return products.map((product) => ({
            id: product.id,
            nom_service_public_numerique: product.nom_service_public_numerique,
            lastStatisticDate: product.indicators.length
                ? product.indicators.sort()[product.indicators.length - 1].date
                : undefined,
            isAutomatic: product.indicators.every((indicator) => indicator.isAutomatic),
        }));
    }

    async function upsertProduct(productDto: Partial<Product>, teamId?: Team['id']) {
        return productRepository.upsert({ ...productDto, team: { id: teamId } }, [
            'nom_service_public_numerique',
        ]);
    }
}

export { buildProductService };
