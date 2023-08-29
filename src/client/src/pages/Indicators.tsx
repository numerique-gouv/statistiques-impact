import { Table } from '@codegouvfr/react-dsfr/Table';
import { Link, useParams } from 'react-router-dom';
import { Page } from '../components/Page';

function Indicators() {
    const params = useParams();
    const { productId } = params;
    return (
        <Page>
            <div />
        </Page>
    );
}

export { Indicators };
