import { indicatorDtoType } from '../modules/indicator';

type adaptatorType<apiOutputT> = {
    fetch: () => apiOutputT;
    map: (apiOutput: apiOutputT) => Array<Omit<indicatorDtoType, 'nom_service_public_numerique'>>;
};

export type { adaptatorType };
