type productType = { name: string; metabaseUrl?: string; repositoriesUrl: string[] };

type PRODUCT_ID =
    | 'AGENT_CONNECT'
    | 'ANNUAIRE_DES_ENTREPRISES'
    | 'API_PARTICULIER'
    | 'API_ENTREPRISE'
    | 'AUDIOCONF'
    | 'AUTHENTIFICATION'
    | 'CODE_GOUV'
    | 'DATA_GOUV'
    | 'DATAPASS'
    | 'DEMARCHES_SIMPLIFIEES'
    | 'DOCUMENTATION'
    | 'DVF'
    | 'FRANCE_CONNECT'
    | 'HUBEE'
    | 'MON_COMPTE_PRO'
    | 'OOTS'
    | 'OSMOSE'
    | 'PAD'
    | 'RESANA'
    | 'RIZOMO'
    | 'TCHAP'
    | 'WEBCONF'
    | 'WEBINAIRE';

const PRODUCTS: Record<PRODUCT_ID, productType> = {
    AGENT_CONNECT: {
        name: 'agent-connect',
        metabaseUrl: 'https://stats.agentconnect.gouv.fr',
        repositoriesUrl: [],
    },
    ANNUAIRE_DES_ENTREPRISES: {
        name: 'annuaire-des-entreprises',
        repositoriesUrl: [
            'https://github.com/etalab/annuaire-entreprises-site',
            'https://github.com/etalab/annuaire-entreprises-search-api',
            'https://github.com/etalab/annuaire-entreprises-search-infra',
            'https://github.com/etalab/annuaire-entreprises-api-proxy',
            'https://github.com/etalab/annuaire-entreprises-search-testing',
        ],
    },

    API_PARTICULIER: {
        name: 'api-particulier',
        metabaseUrl: 'https://metabase.entreprise.api.gouv.fr',
        repositoriesUrl: [],
    },
    API_ENTREPRISE: {
        name: 'api-entreprise',
        metabaseUrl: 'https://metabase.entreprise.api.gouv.fr',
        repositoriesUrl: [
            'https://github.com/etalab/admin_api_entreprise',
            'https://github.com/etalab/calendrier.api.gouv.fr',
            'https://github.com/etalab/rncs_worker_api_entreprise',
            'https://github.com/etalab/watchdoge_apientreprise',
        ],
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
    DATA_GOUV: {
        name: 'data-gouv',
        repositoriesUrl: [
            'https://github.com/etalab/ouverture.data.gouv.fr',
            'https://github.com/etalab/schema.data.gouv.fr',
            'https://github.com/etalab/guides.data.gouv.fr',
            'https://github.com/etalab/catalogage-donnees',
            'https://github.com/etalab/cadastre.data.gouv.fr',
            'https://github.com/etalab/explore.data.gouv.fr',
            'https://github.com/etalab/datagouvfr-pages',
            'https://github.com/etalab/doc.data.gouv.fr',
            'https://github.com/etalab/support.data.gouv.fr',
        ],
    },
    DATAPASS: {
        name: 'datapass',
        repositoriesUrl: ['https://github.com/betagouv/datapass'],
    },
    DEMARCHES_SIMPLIFIEES: {
        name: 'demarches-simplifiees',
        repositoriesUrl: ['https://github.com/betagouv/doc.demarches-simplifiees.fr'],
    },
    DOCUMENTATION: {
        name: 'documentation',
        repositoriesUrl: ['https://github.com/numerique-gouv/outline'],
    },
    DVF: {
        name: 'dvf',
        repositoriesUrl: [
            'https://github.com/etalab/DVF-app',
            'https://github.com/etalab/api-dvf',
            'https://github.com/etalab/dvf',
        ],
    },
    FRANCE_CONNECT: {
        name: 'france-connect',
        repositoriesUrl: [],
    },
    HUBEE: { name: 'hubee', repositoriesUrl: [] },
    MON_COMPTE_PRO: {
        name: 'mon-compte-pro',
        repositoriesUrl: [
            'https://github.com/betagouv/moncomptepro',
            'https://github.com/betagouv/moncomptepro-landing-page',
            'https://github.com/betagouv/moncomptepro-infrastructure',
        ],
        metabaseUrl: 'https://stats.moncomptepro.beta.gouv.fr/',
    },
    OOTS: { name: 'oots', repositoriesUrl: ['https://github.com/betagouv/oots-france'] },
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
        repositoriesUrl: ['https://github.com/betagouv/visio-bbb/'],
        metabaseUrl: 'https://webinaire-metabase.osc-secnum-fr1.scalingo.io/',
    },
};

export { PRODUCTS };
