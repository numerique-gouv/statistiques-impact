import { Indicator } from './Indicator.entity';
import { dataSource } from '../../dataSource';

export { buildIndicatorService };

function buildIndicatorService() {
    const indicatorRepository = dataSource.getRepository(Indicator);
    const indicatorService = {
        getIndicators,
    };

    return indicatorService;

    async function getIndicators() {
        return indicatorRepository.find();
    }
}
