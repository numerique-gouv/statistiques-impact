import { DataSource } from 'typeorm';
import { Product } from './Product.entity';
import { Team, buildTeamService } from '../team';

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
        getProducts,
        upsertProduct,
    };

    async function getProducts() {
        const teamService = buildTeamService(dataSource);
        const products = await productRepository.find({
            relations: ['indicators', 'team'],
            select: {
                indicators: { date: true, est_automatise: true, valeur: true, indicateur: true },
                team: { id: true },
            },
        });
        const teams = await teamService.getAllTeams();
        const results: Record<
            string,
            {
                id: string;
                name: string;
                products: Array<formattedProductType>;
            }
        > = {};
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

            results[product.team.id] = results[product.team.id]
                ? {
                      ...results[product.team.id],
                      products: [...results[product.team.id].products, formattedProduct],
                  }
                : {
                      id: product.team.id,
                      name: teams[product.team.id].name,
                      products: [formattedProduct],
                  };
        }

        return results;
    }

    async function upsertProduct(productDto: Partial<Product>, teamId?: Team['id']) {
        return productRepository.upsert({ ...productDto, team: { id: teamId } }, [
            'nom_service_public_numerique',
        ]);
    }
}

export { buildProductService };
