type productType = { name: string };

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
    | 'FRANCE_TRANSFERT'
    | 'GRIST'
    | 'HUBEE'
    | 'DOCS'
    | 'VISIO'
    | 'MON_COMPTE_PRO'
    | 'OOTS'
    | 'OSMOSE'
    | 'PAD'
    | 'PLANKA'
    | 'REGIE'
    | 'RESANA'
    | 'RIZOMO'
    | 'TCHAP'
    | 'WEBCONF'
    | 'WEBINAIRE';

const PRODUCTS: Record<PRODUCT_ID, productType> = {
    AGENT_CONNECT: {
        name: 'proconnect',
    },
    ANNUAIRE_DES_ENTREPRISES: {
        name: 'annuaire-des-entreprises',
    },
    API_PARTICULIER: {
        name: 'api-particulier',
    },
    API_ENTREPRISE: {
        name: 'api-entreprise',
    },
    AUDIOCONF: {
        name: 'audioconf',
    },
    AUTHENTIFICATION: {
        name: 'authentification',
    },
    CODE_GOUV: {
        name: 'code-gouv',
    },
    DATA_GOUV: {
        name: 'data-gouv',
    },
    DATAPASS: {
        name: 'datapass',
    },
    DEMARCHES_SIMPLIFIEES: {
        name: 'demarches-simplifiees',
    },
    DOCUMENTATION: {
        name: 'documentation',
    },
    DVF: {
        name: 'dvf',
    },
    FRANCE_CONNECT: {
        name: 'france-connect',
    },
    FRANCE_TRANSFERT: {
        name: 'france-transfert',
    },
    GRIST: {
        name: 'grist',
    },
    HUBEE: { name: 'hubee' },
    DOCS: { name: 'docs' },
    VISIO: { name: 'visio' },
    MON_COMPTE_PRO: {
        name: 'mon-compte-pro',
    },
    OOTS: { name: 'oots' },
    OSMOSE: { name: 'osmose' },
    PAD: { name: 'pad' },
    PLANKA: { name: 'planka' },
    REGIE: { name: 'regie' },
    RESANA: { name: 'resana' },
    RIZOMO: { name: 'rizomo' },
    TCHAP: {
        name: 'tchap',
    },
    WEBCONF: {
        name: 'webconf',
    },
    WEBINAIRE: {
        name: 'webinaire',
    },
};

export { PRODUCTS };
export type { PRODUCT_ID };
