import { PRODUCTS } from '../../constants';
import { dataSource } from '../../dataSource';
import { buildProductService } from '../../modules/product';
import { logger } from '../../lib/logger';
import { fetchCommitVerificationList } from './fetchCommitVerificationList';
import { computePercentageSignedCommits } from './computePercentageSignedCommits';

async function importSignedCommitsPercentage() {
    await dataSource.initialize();
    const productInfoService = buildProductService(dataSource);
    for (const [_, product] of Object.entries(PRODUCTS)) {
        if (product.repositoriesUrl.length === 0) {
            continue;
        }
        try {
            const verificationStatuses = await fetchCommitVerificationList(product.repositoriesUrl);
            const percentageSignedCommits = computePercentageSignedCommits(verificationStatuses);
            await productInfoService.upsertProduct({
                nom_service_public_numerique: product.name,
                percentageSignedCommits,
            });
        } catch (error) {
            logger.error({ productName: product.name, message: error as string });
        }
    }
}

importSignedCommitsPercentage();
