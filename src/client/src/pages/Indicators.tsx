import { Table } from '@codegouvfr/react-dsfr/Table';
import { Link, useParams } from 'react-router-dom';
import { useQuery } from 'react-query';
import { Page } from '../components/Page';
import {} from '../';
import { api } from '../lib/api';

function Indicators() {
    const params = useParams();
    const productId = params.productId || '';
    const query = useQuery(['indicators', productId], () => api.getIndicatorsByProduct(productId));
    console.log(query.data);

    return (
        <Page>
            <div />
        </Page>
    );
}

export { Indicators };
