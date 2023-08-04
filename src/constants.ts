type productType = { name: string; metabaseUrl?: string; repositoriesUrl: string[] };

const PRODUCTS: Record<string, productType> = {
    ANNUAIRE_DES_ENTREPRISES: {
        name: 'annuaire-des-entreprises',
        repositoriesUrl: ['https://github.com/etalab/annuaire-entreprises-site'],
    },
    AGENT_CONNECT: {
        name: 'agent-connect',
        metabaseUrl: 'https://stats.agentconnect.gouv.fr',
        repositoriesUrl: [],
    },
    API_PARTICULIER: {
        name: 'api-particulier',
        metabaseUrl: 'https://metabase.entreprise.api.gouv.fr',
        repositoriesUrl: [],
    },
    API_ENTREPRISE: {
        name: 'api-entreprise',
        metabaseUrl: 'https://metabase.entreprise.api.gouv.fr',
        repositoriesUrl: [],
    },
    AUDIOCONF: {
        name: 'audioconf',
        metabaseUrl: 'https://stats.audioconf.numerique.gouv.fr/',
        repositoriesUrl: ['https://github.com/betagouv/audioconf'],
    },
    DATAPASS: {
        name: 'datapass',
        repositoriesUrl: [],
    },
    DEMARCHES_SIMPLIFIEES: {
        name: 'demarches-simplifiees',
        repositoriesUrl: [],
    },
    PAD: { name: 'pad', repositoriesUrl: ['https://github.com/betagouv/pad.numerique.gouv.fr'] },
    TCHAP: {
        name: 'tchap',
        metabaseUrl: 'https://stats.tchap.incubateur.net/',
        repositoriesUrl: [],
    },
    WEBINAIRE: {
        name: 'webinaire',
        repositoriesUrl: [],
        metabaseUrl: 'https://webinaire-metabase.osc-secnum-fr1.scalingo.io/',
    },
    MON_COMPTE_PRO: {
        name: 'mon-compte-pro',
        repositoriesUrl: ['https://github.com/betagouv/moncomptepro'],
        metabaseUrl: 'https://stats.moncomptepro.beta.gouv.fr/',
    },
};

export { PRODUCTS };
