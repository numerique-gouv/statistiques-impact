import { Link } from 'react-router-dom';
import { Table } from '@codegouvfr/react-dsfr/Table';
import { Badge } from '@codegouvfr/react-dsfr/Badge';

import { Page } from '../components/Page';
import { useQuery } from 'react-query';
import { api } from '../lib/api';

function Home() {
    const headers = [
        'Équipe',
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

    return (
        <Page>
            <Table
                headers={headers}
                data={Object.values(query.data)
                    .sort((a, b) => a.name.localeCompare(b.name))
                    .reduce((acc, team) => {
                        return [
                            ...acc,
                            ...team.products.map((product) => [
                                <div>{team.name}</div>,
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
                            ]),
                        ];
                    }, [] as React.ReactNode[][])}
                caption="Produits référencés"
            ></Table>
        </Page>
    );
}

export { Home };
