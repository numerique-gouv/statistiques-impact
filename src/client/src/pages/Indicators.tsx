import { useParams } from 'react-router-dom';
import { useQuery } from 'react-query';
import { Line } from 'react-chartjs-2';
import { CategoryScale, Chart, LineElement, LinearScale, PointElement } from 'chart.js';

import { Page } from '../components/Page';
import { api } from '../lib/api';

type indicatorType = { date: string; indicateur: string; date_debut?: string; valeur: number };

type apiOutputType = Record<string, indicatorType[]>;

Chart.register(CategoryScale, LinearScale, PointElement, LineElement);

function Indicators() {
    const params = useParams();
    const productId = params.productId || '';
    const query = useQuery<apiOutputType>(['indicators', productId], () =>
        api.getIndicatorsByProduct(productId),
    );

    const charts = formatChartData(query.data);

    return <Page>{charts}</Page>;

    function formatChartData(rawData?: apiOutputType) {
        if (!rawData) {
            return [];
        }
        return Object.entries(rawData).map(([indicatorName, indicators]) => {
            const data = {
                type: 'line',
                labels: indicators.map(({ date }) => date),
                datasets: [
                    {
                        label: indicatorName,
                        data: indicators.map(({ valeur }) => valeur),
                    },
                ],
            };

            return (
                <>
                    <Line data={data} />
                    {indicatorName}
                </>
            );
        });
    }
}

export { Indicators };
