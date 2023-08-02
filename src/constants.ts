type productType = { name: string; metabaseUrl?: string };

const PRODUCTS: Record<string, productType> = {
    ANNUAIRE_DES_ENTREPRISES: { name: 'annuaire-des-entreprises' },
    AGENT_CONNECT: { name: 'agent-connect', metabaseUrl: 'https://stats.agentconnect.gouv.fr' },
    API_PARTICULIER: {
        name: 'api-particulier',
        metabaseUrl: 'https://metabase.entreprise.api.gouv.fr',
    },
    API_ENTREPRISE: {
        name: 'api-entreprise',
        metabaseUrl: 'https://metabase.entreprise.api.gouv.fr',
    },
    AUDIOCONF: { name: 'audioconf', metabaseUrl: 'https://stats.audioconf.numerique.gouv.fr/' },
    DATAPASS: { name: 'datapass' },
    DEMARCHES_SIMPLIFIEES: { name: 'demarches-simplifiees' },
    PAD: { name: 'pad' },
    TCHAP: { name: 'tchap', metabaseUrl: 'https://stats.tchap.incubateur.net/' },
    WEBINAIRE: {
        name: 'webinaire',
        metabaseUrl: 'https://webinaire-metabase.osc-secnum-fr1.scalingo.io/',
    },
    MON_COMPTE_PRO: {
        name: 'mon-compte-pro',
        metabaseUrl: 'https://stats.moncomptepro.beta.gouv.fr/',
    },
};

export { PRODUCTS };
