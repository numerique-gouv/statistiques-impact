import { DataSource } from 'typeorm';
import { ProductInfo } from './ProductInfo.entity';

function buildProductInfoService(dataSource: DataSource) {
    const productInfoRepository = dataSource.getRepository(ProductInfo);
    return {
        insertProductInfo,
    };

    async function insertProductInfo(productInfoDto: Partial<ProductInfo>) {
        const productInfo = await productInfoRepository.findOneBy({
            nom_service_public_numerique: productInfoDto.nom_service_public_numerique,
        });
        if (productInfo) {
            return productInfoRepository.update({ id: productInfo.id }, productInfoDto);
        } else {
            return productInfoRepository.insert(productInfoDto);
        }
    }
}

export { buildProductInfoService };
