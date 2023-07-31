import { agentConnectAdaptator } from './agentConnect.adaptator';

describe('agentConnectAdaptator', () => {
    it('should format the agentConnect output', () => {
        const agentConnectOutputRows = [
            { Time: '2023-01-01', Connexion: 'Initiée' as const, Count: 31413 },
            { Time: '2023-01-01', Connexion: 'Réussie' as const, Count: 6770 },
        ];

        const formatted = agentConnectAdaptator.map(agentConnectOutputRows);

        expect(formatted).toEqual([
            {
                date: '2023-02-01',
                date_debut: '2023-01-01',
                valeur: 6770,
                est_periode: true,
                nom_service_public_numerique: 'agent-connect',
                frequence_calcul: 'mensuelle',
                indicateur: 'nombre de connexions réussies',
                unite_mesure: 'unité',
            },
            {
                date: '2023-02-01',
                date_debut: '2023-01-01',
                valeur: 0.82,
                est_periode: true,
                nom_service_public_numerique: 'agent-connect',
                frequence_calcul: 'mensuelle',
                indicateur: 'pourcentage de connexions réussies',
                unite_mesure: '%',
            },
        ]);
    });
});
