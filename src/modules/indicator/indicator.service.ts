import { Indicator } from './Indicator.entity';
import { dataSource } from '../../dataSource';

export { buildIndicatorService };

export type { indicatorDto };

type indicatorDto = {
    nom_service_public_numerique: string;
    indicateur: string;
    valeur: number;
    unite_mesure: string;
    frequence_calcul: string;
    date: number;
    est_periode: boolean;
};

function buildIndicatorService() {
    const indicatorRepository = dataSource.getRepository(Indicator);
    const indicatorService = {
        getIndicators,
        createIndicator,
        deleteIndicator,
    };

    return indicatorService;

    async function getIndicators() {
        return indicatorRepository.find();
    }

    async function deleteIndicator(indicatorId: string) {
        const result = await indicatorRepository.delete({ id: indicatorId });
        return result.affected === 1;
    }

    async function createIndicator(body: indicatorDto) {
        const indicator = new Indicator();
        indicator.nom_service_public_numerique = body.nom_service_public_numerique;
        indicator.indicateur = body.indicateur;
        indicator.valeur = body.valeur;
        indicator.unite_mesure = body.unite_mesure;
        indicator.frequence_calcul = body.frequence_calcul;
        const date = new Date();
        date.setTime(body.date);
        indicator.date = date.toISOString();
        indicator.est_periode = body.est_periode;

        return indicatorRepository.save(indicator);
    }
}
