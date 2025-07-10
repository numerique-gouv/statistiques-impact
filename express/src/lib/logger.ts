const logger = buildLogger();

function buildLogger() {
    return { error };

    async function error({
        productName,
        indicator,
        message,
    }: {
        productName: string;
        indicator?: string;
        message: string;
    }) {
        const description = `${productName} - ${indicator || ''} - ${message}`;
        console.warn(description);
    }
}

export { logger };
