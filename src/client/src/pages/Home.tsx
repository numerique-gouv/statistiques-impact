import { Link } from 'react-router-dom';
import { Table } from '@codegouvfr/react-dsfr/Table';
import { Badge } from '@codegouvfr/react-dsfr/Badge';

import { Page } from '../components/Page';
import { useQuery } from 'react-query';
import { api } from '../lib/api';

type productsType = Array<{ id: string; nom_service_public_numerique: string }>;

function Home() {
    const headers = ['Produit', 'Phase', 'Sécurité', 'Accessibilité'];
    const query = useQuery<productsType>(['products'], api.getProducts);
    console.log(query.data);

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
                        <div />,
                        <div />,
                    ])}
                    caption="Produits référencés"
                ></Table>
            )}
        </Page>
    );
}

export { Home };
