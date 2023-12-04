import { indicatorDtoType } from '../../modules/indicator';

type adaptatorType = {
    fetch: () => Promise<Array<indicatorDtoType>>;
};

export type { adaptatorType };
