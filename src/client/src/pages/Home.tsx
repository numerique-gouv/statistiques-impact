import { Link } from 'react-router-dom';
import { Table } from '@codegouvfr/react-dsfr/Table';
import { Badge } from '@codegouvfr/react-dsfr/Badge';

import { Page } from '../components/Page';

function Home() {
    const headers = ['Produit', 'Phase', 'Sécurité', 'Accessibilité'];
    const tableData = buildData();

    return (
        <Page>
            <Table headers={headers} data={tableData} caption="Produits référencés"></Table>
        </Page>
    );
}

function buildData() {
    return [
        'Agent Connect',
        'audioconf',
        'api.gouv',
        'calendso',
        'DVF',
        'France Connect',
        'code.gouv',
        'datapass',
        'API Entreprises',
        'API Géo',
        'Mon France Connect',
        'Mon Compte Pro',
        'Osmose',
        'Pad',
        'Resana',
        'Rizomo',
    ]
        .sort()
        .map((name) => [
            <Link to={`/indicators/${name}`}>{name}</Link>,
            <Badge severity="info">-</Badge>,
            <div />,
            <div />,
        ]);
}

export { Home };
