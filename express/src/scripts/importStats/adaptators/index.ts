import { PRODUCTS } from '../../../constants';
import { audioconfAdaptator } from './audioconf.adaptator';
import { demarchesSimplifieesAdaptator } from './demarchesSimplifiees.adaptator';
import { datapassAdaptator } from './datapass.adaptator';
import { annuaireDesEntreprisesAdaptator } from './annuaireDesEntreprises.adaptator';
import { webinaireAdaptator } from './webinaire.adaptator';
import { apiParticulierAdaptator } from './apiParticulier.adaptator';
import { apiEntrepriseAdaptator } from './apiEntreprise.adaptator';
import { agentConnectAdaptator } from './agentConnect.adaptator';
import { documentationAdaptator } from './documentation.adaptator';
import { hubeeAdaptator } from './hubee.adaptator';
import { regieAdaptator } from './regie.adaptator';
import {
    resanaAdaptator,
    franceTransfertAdaptator,
    gristAdaptator,
    docsAdaptator,
    visioAdaptator,
    plankaAdaptator,
    padAdaptator,
} from './suite.adaptator';
import { indicatorDtoType } from '../../../modules/indicator';

type adaptatorType = {
    fetch: () => Promise<Array<indicatorDtoType>>;
};

const indicatorsToUpdate: Record<string, adaptatorType> = {
    [PRODUCTS.HUBEE.name]: hubeeAdaptator,
    [PRODUCTS.AUDIOCONF.name]: audioconfAdaptator,
    [PRODUCTS.PAD.name]: padAdaptator,
    [PRODUCTS.DEMARCHES_SIMPLIFIEES.name]: demarchesSimplifieesAdaptator,
    [PRODUCTS.DATAPASS.name]: datapassAdaptator,
    [PRODUCTS.ANNUAIRE_DES_ENTREPRISES.name]: annuaireDesEntreprisesAdaptator,
    [PRODUCTS.WEBINAIRE.name]: webinaireAdaptator,
    [PRODUCTS.AGENT_CONNECT.name]: agentConnectAdaptator,
    [PRODUCTS.DOCUMENTATION.name]: documentationAdaptator,
    // [PRODUCTS.API_PARTICULIER.name]: apiParticulierAdaptator,
    // [PRODUCTS.API_ENTREPRISE.name]: apiEntrepriseAdaptator,
    [PRODUCTS.RESANA.name]: resanaAdaptator,
    [PRODUCTS.DOCS.name]: docsAdaptator,
    [PRODUCTS.FRANCE_TRANSFERT.name]: franceTransfertAdaptator,
    [PRODUCTS.VISIO.name]: visioAdaptator,
    [PRODUCTS.PLANKA.name]: plankaAdaptator,
    [PRODUCTS.GRIST.name]: gristAdaptator,
    [PRODUCTS.REGIE.name]: regieAdaptator,
};

export { indicatorsToUpdate };
export type { adaptatorType };
