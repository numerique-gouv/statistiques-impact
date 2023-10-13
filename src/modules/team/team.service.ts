import { DataSource } from 'typeorm';
import { Team } from './Team.entity';
import { mapEntities } from '../../lib/mapEntities';

function buildTeamService(dataSource: DataSource) {
    const teamRepository = dataSource.getRepository(Team);
    return {
        getAllTeams,
        upsertTeam,
    };

    async function getAllTeams() {
        const teams = await teamRepository.find();
        return mapEntities(teams);
    }

    async function upsertTeam(name: string) {
        return teamRepository.upsert({ name }, ['name']);
    }
}

export { buildTeamService };
