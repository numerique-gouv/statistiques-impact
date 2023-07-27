import { indicatorDtoType } from '../../modules/indicator';

type adaptatorType<apiOutputT> = {
    fetch: () => apiOutputT;
    map: (apiOutput: apiOutputT) => Array<indicatorDtoType>;
};

export type { adaptatorType };
