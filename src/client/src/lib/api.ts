const api = { getIndicatorsByProduct, getProducts };

const BASE_URL = `http://localhost:3001/api`;

function getIndicatorsByProduct(productId: string) {
    const url = `${BASE_URL}/indicators/${productId}`;
    return performApiCall(url);
}

function getProducts() {
    const url = `${BASE_URL}/products`;
    return performApiCall(url);
}

async function performApiCall(url: string) {
    const response = await fetch(url, { method: 'GET' });
    return response.json();
}

export { api };
