import { Product } from '../product';
import { Indicator } from './Indicator.entity';
import { DataSource } from 'typeorm';
import { adaptators } from './adaptators';

export { buildIndicatorService };

export type { indicatorDtoType };

type indicatorDtoType = {
    nom_service_public_numerique: string;
    indicateur: string;
    valeur: number;
    unite_mesure: string;
    frequence_monitoring: string;
    date: string;
    date_debut?: string;
    est_periode: boolean;
    est_automatise: boolean;
};

function buildIndicatorService(dataSource: DataSource) {
    const indicatorRepository = dataSource.getRepository(Indicator);
    const productRepository = dataSource.getRepository(Product);
    const indicatorService = {
        getIndicators,
        getIndicatorsByProductName,
        deleteIndicator,
        upsertIndicators,
        insertRawIndicators,
    };

    return indicatorService;

    async function getIndicators() {
        return indicatorRepository.find({
            relations: ['product'],
            select: { product: { nom_service_public_numerique: true } },
        });
    }

    async function getIndicatorsByProductName(nom_service_public_numerique: string) {
        const indicators = await indicatorRepository.find({
            where: { product: { nom_service_public_numerique } },
            order: { date: 'ASC' },
        });

        const grouppedIndicators = indicators.reduce((acc, indicator) => {
            return {
                ...acc,
                [indicator.indicateur]: acc[indicator.indicateur]
                    ? [...acc[indicator.indicateur], indicator]
                    : [indicator],
            };
        }, {} as Record<string, Indicator[]>);

        return grouppedIndicators;
    }

    async function deleteIndicator(indicatorId: string) {
        const result = await indicatorRepository.delete({ id: indicatorId });
        return result.affected === 1;
    }

    async function insertRawIndicators(csv: Array<Record<string, string>>, productName: string) {
        const adaptator = adaptators[productName];
        if (!adaptator) {
            throw new Error(`No adaptator available for productName "${productName}"`);
        }
        const product = await productRepository.findOneByOrFail({
            nom_service_public_numerique: productName,
        });
        const indicator = adaptator(csv, product);
        return indicatorRepository.insert(indicator);
    }

    async function upsertIndicators(
        nom_service_public_numerique: string,
        indicatorDtos: indicatorDtoType[],
    ) {
        const product = await productRepository.findOneByOrFail({
            nom_service_public_numerique,
        });

        const indicators = indicatorDtos.map((indicatorDto) => {
            const indicator = new Indicator();

            indicator.product = product;
            indicator.indicateur = indicatorDto.indicateur;
            indicator.valeur = indicatorDto.valeur;
            indicator.unite_mesure = indicatorDto.unite_mesure;
            indicator.frequence_monitoring = indicatorDto.frequence_monitoring;
            indicator.date = indicatorDto.date;
            if (indicatorDto.date_debut) {
                indicator.date_debut = indicatorDto.date_debut;
            }
            indicator.est_periode = indicatorDto.est_periode;
            indicator.est_automatise = indicatorDto.est_automatise;

            return indicator;
        });
        return Promise.all(
            indicators.map((indicator) =>
                indicatorRepository.upsert(indicator, {
                    upsertType: 'on-conflict-do-update',
                    skipUpdateIfNoValuesChanged: true,
                    conflictPaths: ['product', 'indicateur', 'frequence_monitoring', 'date'],
                }),
            ),
        );
    }
}
