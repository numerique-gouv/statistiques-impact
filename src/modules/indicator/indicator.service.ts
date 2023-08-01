import { Indicator } from './Indicator.entity';
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
    const indicatorService = {
        getIndicators,
        getIndicatorsByProductName,
        deleteIndicator,
        upsertIndicators,
    };

    return indicatorService;

    async function getIndicators() {
        return indicatorRepository.find();
    }

    async function getIndicatorsByProductName(nom_service_public_numerique: string) {
        return indicatorRepository.find({
            where: { nom_service_public_numerique },
        });
    }

    async function deleteIndicator(indicatorId: string) {
        const result = await indicatorRepository.delete({ id: indicatorId });
        return result.affected === 1;
    }

    async function upsertIndicators(indicatorDtos: indicatorDtoType[]) {
        const indicators = indicatorDtos.map((indicatorDto) => {
            const indicator = new Indicator();

            indicator.nom_service_public_numerique = indicatorDto.nom_service_public_numerique;
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
            'nom_service_public_numerique',
            'indicateur',
            'frequence_calcul',
            'date',
        ]);
    }
}
