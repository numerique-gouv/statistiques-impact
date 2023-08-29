import { Table } from '@codegouvfr/react-dsfr/Table';
import { Link, useParams } from 'react-router-dom';
import { ProgressBar } from '../components/ProgressBar';
import { Page } from '../components/Page';

function Product() {
    const params = useParams();
    const rawData = computeRawData();
    const tableData = formatTableData(rawData);
    return (
        <Page>
            <Table data={tableData}></Table>
        </Page>
    );

    function computeRawData() {
        const { sub1 } = params;
        if (sub1) {
            switch (sub1) {
                case 'security':
                    return [
                        {
                            title: 'Sécurité du processus de développement',
                            path: `/measures`,
                            value: 21,
                        },
                        {
                            title: "Sécurité de l'application",
                            path: `/measures`,
                            value: 33,
                        },
                    ];
                case 'accessibility':
                    return [];
                default:
                    throw new Error(`La sous-catégorie 1 ${sub1} n'existe pas`);
            }
        }
        return [
            { title: 'Sécurité', path: `security`, value: 90 },
            { title: 'Accessibilité', path: `accessibility`, value: 20 },
        ];
    }

    function formatTableData(rawData: Array<{ title: string; path?: string; value: number }>) {
        return rawData.map((row) => {
            const element = row.path ? <Link to={row.path}>{row.title}</Link> : row.title;
            return [element, <ProgressBar progress={row.value} />];
        });
    }
}

export { Product };
