import { DataSource } from 'typeorm';
import { Team } from './Team.entity';

function buildTeamService(dataSource: DataSource) {
    const teamRepository = dataSource.getRepository(Team);
    return {
        upsertTeam,
    };

    async function upsertTeam(name: string) {
        return teamRepository.upsert({ name }, ['name']);
    }
}

export { buildTeamService };
