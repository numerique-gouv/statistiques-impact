import { Link } from 'react-router-dom';
import { Table } from '@codegouvfr/react-dsfr/Table';
import { Badge } from '@codegouvfr/react-dsfr/Badge';

import { Page } from '../components/Page';
import { useQuery } from 'react-query';
import { api } from '../lib/api';

function Home() {
    const headers = [
        'Produit',
        'Phase',
        'Date dernière stat.',
        'Dernière stat.',
        'Récupération automatique ?',
    ];
    const query = useQuery(['products'], api.getProducts);

    if (!query.data) {
        return <Page>Chargement en cours...</Page>;
    }

    const formattedData = query.data
        .sort((a, b) =>
            a.nom_service_public_numerique.localeCompare(b.nom_service_public_numerique),
        )
        .map((product) => [
            <Link to={`/indicators/${product.nom_service_public_numerique}`}>
                {product.nom_service_public_numerique}
            </Link>,
            <Badge severity="info">-</Badge>,
            <div>{product.lastIndicatorDate || '-'}</div>,
            <div>
                {product.lastIndicators.length > 0 ? (
                    <ul>
                        {product.lastIndicators.map((indicator) => (
                            <li>{indicator}</li>
                        ))}
                    </ul>
                ) : (
                    '-'
                )}
            </div>,
            <div>{product.est_automatise && 'X'}</div>,
        ]);

    return (
        <Page>
            <Table headers={headers} data={formattedData} caption="Produits référencés"></Table>
        </Page>
    );
}

export { Home };
