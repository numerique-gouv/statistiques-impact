import { Indicator } from './Indicator.entity';
import { Product } from '../product';
import { DataSource } from 'typeorm';

export { buildIndicatorService };

export type { indicatorDtoType };

type indicatorDtoType = {
    nom_service_public_numerique: string;
    indicateur: string;
    valeur: number;
    unite_mesure: string;
    frequence_calcul: string;
    date: string;
    date_debut?: string;
    est_periode: boolean;
};

function buildIndicatorService(dataSource: DataSource) {
    const indicatorRepository = dataSource.getRepository(Indicator);
    const productRepository = dataSource.getRepository(Product);
    const indicatorService = {
        getIndicators,
        upsertIndicator,
        deleteIndicator,
        upsertIndicators,
    };

    return indicatorService;

    async function getIndicators() {
        return indicatorRepository.find();
    }

    async function deleteIndicator(indicatorId: string) {
        const result = await indicatorRepository.delete({ id: indicatorId });
        return result.affected === 1;
    }

    async function upsertIndicator(body: indicatorDtoType) {
        const indicator = new Indicator();

        const product = await productRepository.findOneOrFail({
            where: { name: body.nom_service_public_numerique },
        });

        indicator.product = product;
        indicator.indicateur = body.indicateur;
        indicator.valeur = body.valeur;
        indicator.unite_mesure = body.unite_mesure;
        indicator.frequence_calcul = body.frequence_calcul;
        indicator.date = body.date;
        indicator.est_periode = body.est_periode;

        return indicatorRepository.upsert(indicator, [
            'product',
            'indicateur',
            'frequence_calcul',
            'date',
        ]);
    }

    async function upsertIndicators(indicatorDtos: indicatorDtoType[]) {
        const products: Record<string, Product> = {};

        for (const indicatorDto of indicatorDtos) {
            if (!Object.keys(products).includes(indicatorDto.nom_service_public_numerique)) {
                const product = await productRepository.findOneOrFail({
                    where: { name: indicatorDto.nom_service_public_numerique },
                });
                products[indicatorDto.nom_service_public_numerique] = product;
            }
        }

        const indicators = indicatorDtos.map((indicatorDto) => {
            const indicator = new Indicator();

            indicator.product = products[indicatorDto.nom_service_public_numerique];
            indicator.indicateur = indicatorDto.indicateur;
            indicator.valeur = indicatorDto.valeur;
            indicator.unite_mesure = indicatorDto.unite_mesure;
            indicator.frequence_calcul = indicatorDto.frequence_calcul;
            indicator.date = indicatorDto.date;
            if (indicatorDto.date_debut) {
                indicator.date_debut = indicatorDto.date_debut;
            }
            indicator.est_periode = indicatorDto.est_periode;
            return indicator;
        });
        return indicatorRepository.upsert(indicators, [
            'product',
            'indicateur',
            'frequence_calcul',
            'date',
        ]);
    }
}
