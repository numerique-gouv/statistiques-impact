import { PRODUCTS } from '../../../constants';
import { audioconfAdaptator } from './audioconf.adaptator';
import { padAdaptator } from './pad.adaptator';
import { demarchesSimplifieesAdaptator } from './demarchesSimplifiees.adaptator';
import { datapassAdaptator } from './datapass.adaptator';
import { annuaireDesEntreprisesAdaptator } from './annuaireDesEntreprises.adaptator';
import { webinaireAdaptator } from './webinaire.adaptator';
import { apiParticulierAdaptator } from './apiParticulier.adaptator';
import { apiEntrepriseAdaptator } from './apiEntreprise.adaptator';
import { agentConnectAdaptator } from './agentConnect.adaptator';
import { tchapAdaptator } from './tchap.adaptator';
import { documentationAdaptator } from './documentation.adaptator';
import { hubeeAdaptator } from './hubee.adaptator';
import {
    resanaAdaptator,
    franceTransfertAdaptator,
    impressAdaptator,
    meetAdaptator,
    plankaAdaptator,
    rizomoAdaptator,
    regieAdaptator,
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
    [PRODUCTS.TCHAP.name]: tchapAdaptator,
    [PRODUCTS.DOCUMENTATION.name]: documentationAdaptator,
    [PRODUCTS.API_PARTICULIER.name]: apiParticulierAdaptator,
    [PRODUCTS.API_ENTREPRISE.name]: apiEntrepriseAdaptator,
    [PRODUCTS.RESANA.name]: resanaAdaptator,
    [PRODUCTS.IMPRESS.name]: impressAdaptator,
    [PRODUCTS.FRANCE_TRANSFERT.name]: franceTransfertAdaptator,
    [PRODUCTS.MEET.name]: meetAdaptator,
    [PRODUCTS.PLANKA.name]: plankaAdaptator,
    [PRODUCTS.REGIE.name]: regieAdaptator,
    [PRODUCTS.RIZOMO.name]: rizomoAdaptator,
};

export { indicatorsToUpdate };
export type { adaptatorType };
