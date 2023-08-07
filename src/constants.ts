type productType = { name: string; metabaseUrl?: string; repositoriesUrl: string[] };

const PRODUCTS: Record<string, productType> = {
    AGENT_CONNECT: {
        name: 'agent-connect',
        metabaseUrl: 'https://stats.agentconnect.gouv.fr',
        repositoriesUrl: [],
    },
    ANNUAIRE_DES_ENTREPRISES: {
        name: 'annuaire-des-entreprises',
        repositoriesUrl: ['https://github.com/etalab/annuaire-entreprises-site'],
    },
    API_GOUV: {
        name: 'api-gouv',
        metabaseUrl: 'https://metabase.entreprise.api.gouv.fr',
        repositoriesUrl: [],
    },
    AUDIOCONF: {
        name: 'audioconf',
        metabaseUrl: 'https://stats.audioconf.numerique.gouv.fr/',
        repositoriesUrl: ['https://github.com/betagouv/audioconf'],
    },
    AUTHENTIFICATION: {
        name: 'authentification',
        repositoriesUrl: [],
    },
    CODE_GOUV: {
        name: 'code-gouv',
        repositoriesUrl: [],
    },
    DATAPASS: {
        name: 'datapass',
        repositoriesUrl: [],
    },
    DEMARCHES_SIMPLIFIEES: {
        name: 'demarches-simplifiees',
        repositoriesUrl: [],
    },
    FRANCE_CONNECT: {
        name: 'france-connect',
        repositoriesUrl: [],
    },
    HUBEE: { name: 'hubee', repositoriesUrl: [] },
    MON_COMPTE_PRO: {
        name: 'mon-compte-pro',
        repositoriesUrl: ['https://github.com/betagouv/moncomptepro'],
        metabaseUrl: 'https://stats.moncomptepro.beta.gouv.fr/',
    },
    OSMOSE: { name: 'osmose', repositoriesUrl: [] },
    PAD: { name: 'pad', repositoriesUrl: ['https://github.com/betagouv/pad.numerique.gouv.fr'] },
    RESANA: { name: 'resana', repositoriesUrl: [] },
    RIZOMO: { name: 'rizomo', repositoriesUrl: [] },
    TCHAP: {
        name: 'tchap',
        metabaseUrl: 'https://stats.tchap.incubateur.net/',
        repositoriesUrl: [],
    },
    WEBCONF: {
        name: 'webconf',
        repositoriesUrl: [],
    },
    WEBINAIRE: {
        name: 'webinaire',
        repositoriesUrl: [],
        metabaseUrl: 'https://webinaire-metabase.osc-secnum-fr1.scalingo.io/',
    },
};

export { PRODUCTS };
