import { dataSource } from '../../dataSource';
import { buildIndicatorService, indicatorDtoType } from '../../modules/indicator';
import { logger } from '../../lib/logger';
import { dateHandler, parsedDateType } from './utils';

import { indicatorsToUpdate } from './adaptators';

async function importStats() {
    console.log('IMPORT STATS');
    console.log('===');
    console.log(`Initializing database...`);
    await dataSource.initialize();
    console.log(`Database initialized...`);

    const indicatorService = buildIndicatorService(dataSource);

    for (const [productName, adaptator] of Object.entries(indicatorsToUpdate)) {
        console.log(`Fetching indicators for "${productName}"...`);
        try {
            const result = await adaptator.fetch();
            const now = new Date();
            const parsedNowDate = {
                year: now.getFullYear(),
                month: now.getMonth() + 1,
                dayOfMonth: now.getDate(),
            };
            const indicatorDtos = result.filter((indicatorDto) =>
                filterUncompletedMonth(indicatorDto, parsedNowDate),
            );
            console.log(`${indicatorDtos.length} found! Inserting in database...`);
            await indicatorService.upsertIndicators(productName, indicatorDtos);
            console.log(`Indicators inserted!`);
        } catch (error) {
            logger.error({ productName: productName, message: error as string });
        }
    }
}

function filterUncompletedMonth(
    indicatorDto: indicatorDtoType,
    parsedNowDate: parsedDateType,
): boolean {
    const parsedIndicatorDate = dateHandler.parseStringDate(indicatorDto.date);
    const result = dateHandler.compareDates(parsedIndicatorDate, parsedNowDate) !== -1;
    return result;
}

importStats();
