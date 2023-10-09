import { Link } from 'react-router-dom';
import { Table } from '@codegouvfr/react-dsfr/Table';
import { Badge } from '@codegouvfr/react-dsfr/Badge';

import { Page } from '../components/Page';
import { useQuery } from 'react-query';
import { api } from '../lib/api';

type productsType = Array<{
    id: string;
    nom_service_public_numerique: string;
    lastStatisticDate: string | undefined;
    est_automatise: boolean;
}>;

function Home() {
    const headers = ['Produit', 'Phase', 'Dernière stat publiée', 'Récupération automatique ?'];
    const query = useQuery<productsType>(['products'], api.getProducts);

    return (
        <Page>
            {!!query.data && (
                <Table
                    headers={headers}
                    data={query.data.map((product) => [
                        <Link to={`/indicators/${product.nom_service_public_numerique}`}>
                            {product.nom_service_public_numerique}
                        </Link>,
                        <Badge severity="info">-</Badge>,
                        <div>{product.lastStatisticDate || '-'}</div>,
                        <div>{product.est_automatise && 'X'}</div>,
                    ])}
                    caption="Produits référencés"
                ></Table>
            )}
        </Page>
    );
}

export { Home };
