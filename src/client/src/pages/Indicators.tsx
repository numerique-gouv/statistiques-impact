import { Table } from '@codegouvfr/react-dsfr/Table';
import { useParams } from 'react-router-dom';
import { useQuery } from 'react-query';
import { Page } from '../components/Page';
import { api } from '../lib/api';

type indicatorType = { date: string; indicateur: string; date_debut?: string; valeur: number };

function Indicators() {
    const params = useParams();
    const productId = params.productId || '';
    const query = useQuery<Array<indicatorType>>(['indicators', productId], () =>
        api.getIndicatorsByProduct(productId),
    );

    const headers = ['Indicateur', 'Valeur', 'Date de début', 'Date de fin'];
    const tableData = formatTableData(query.data);

    return (
        <Page>
            <Table headers={headers} caption={productId} data={tableData}></Table>
        </Page>
    );

    function formatTableData(rawData: Array<indicatorType> | undefined) {
        return (
            rawData?.map(({ date, indicateur, valeur, date_debut }) => [
                indicateur,
                valeur,
                date_debut || '-',
                date,
            ]) || []
        );
    }
}

export { Indicators };
