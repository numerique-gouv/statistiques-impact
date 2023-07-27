const logger = { error };

function error({
    productName,
    indicator,
    message,
}: {
    productName: string;
    indicator: string;
    message: string;
}) {
    console.warn(`${productName} - ${indicator} - ${message}`);
}

export { logger };
