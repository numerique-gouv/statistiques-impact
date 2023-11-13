import { dataSource } from '../../dataSource';
import { buildProductService } from '../../modules/product';
import { api, teamRecordType } from '../../lib/api';
import { buildTeamService } from '../../modules/team';

async function importProducts() {
    await dataSource.initialize();
    const productService = buildProductService(dataSource);
    const teamService = buildTeamService(dataSource);
    const teams = await api.fetchTeams();
    const mappedTeams: Record<string, { bddId: string; teamRecord: teamRecordType }> = {};

    for (const team of teams) {
        const result = await teamService.upsertTeam(team.fields.Equipe);
        const bddId = result.identifiers[0].id as string;
        mappedTeams[team.id] = { bddId, teamRecord: team };
    }

    const products = await api.fetchProducts();
    for (const product of products) {
        const teamId = mappedTeams[`${product.fields.Equipe}`].bddId;
        await productService.upsertProduct(
            {
                nom_service_public_numerique: product.fields.slug,
            },
            teamId,
        );
    }
    return;
}

importProducts();
