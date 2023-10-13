import { config } from '../config';

const api = { getIndicatorsByProduct, getProducts };

const BASE_URL = `${config.API_URL}/api`;

type grouppedProductByTeamType = Record<
    string,
    {
        id: string;
        name: string;
        products: Array<formattedProductType>;
    }
>;

type formattedProductType = {
    id: string;
    nom_service_public_numerique: string;
    lastIndicatorDate: string | undefined;
    lastIndicators: string[];
    est_automatise: boolean;
};

function getIndicatorsByProduct(productId: string) {
    const url = `${BASE_URL}/indicators/${productId}`;
    return performApiCall(url);
}

function getProducts(): Promise<grouppedProductByTeamType> {
    const url = `${BASE_URL}/products`;
    return performApiCall(url);
}

async function performApiCall(url: string) {
    const response = await fetch(url, { method: 'GET' });
    return response.json();
}

export { api };
