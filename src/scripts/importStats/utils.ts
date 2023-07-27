function parseCsv(
    csv: string,
    options?: { lineDelimitator?: string; columnsCount?: number; rowsCount?: number },
): { header: string[]; values: string[][] } {
    const rows = csv
        .trim()
        .split(options?.lineDelimitator || '\n')
        .map((line) => line.split(','));

    if (rows.length === 0) {
        throw new Error(`csv ${csv} has 0 rows and cannot be parsed`);
    }
    const header = rows[0];
    const values = rows.slice(1);

    if (
        !!options?.columnsCount &&
        (header.length !== options.columnsCount ||
            values.some((row) => row.length !== options.columnsCount))
    ) {
        throw new Error(
            `csv ${csv} does not match the expected columns count (${options.columnsCount})`,
        );
    }

    if (!!options?.rowsCount && options.rowsCount !== values.length) {
        throw new Error(`csv ${csv} does not match the expected rows count (${options.rowsCount})`);
    }

    return { header, values };
}

const dateHandler = {
    addMonth,
    substractMonth,
    parseDate,
    formatDate,
    parseReadableDate,
};

function addMonth(date: string) {
    const parsedDate = parseDate(date);
    let newYear: number;
    let newMonth: number;
    if (parsedDate.month === 12) {
        newYear = parsedDate.year + 1;
        newMonth = 1;
    } else {
        newYear = parsedDate.year;
        newMonth = parsedDate.month + 1;
    }
    return `${newYear}-${formatValue(newMonth)}-${formatValue(parsedDate.dayOfMonth)}`;
}

function formatValue(value: number) {
    return value < 10 ? `0${value}` : `${value}`;
}
function substractMonth(date: string) {
    const parsedDate = parseDate(date);
    let newYear: number;
    let newMonth: number;
    if (parsedDate.month === 1) {
        newYear = parsedDate.year - 1;
        newMonth = 12;
    } else {
        newYear = parsedDate.year;
        newMonth = parsedDate.month - 1;
    }
    return `${newYear}-${formatValue(newMonth)}-${formatValue(parsedDate.dayOfMonth)}`;
}

const DATE_REGEX = /^(\d{4})-(\d{2})-(\d{2})$/;

function parseDate(date: string) {
    const result = date.match(DATE_REGEX);
    if (!result || result.length !== 4) {
        throw new Error(`date "${date}" does not match the format YYYY-MM-DD`);
    }
    return { year: Number(result[1]), month: Number(result[2]), dayOfMonth: Number(result[3]) };
}

function formatDate(date: string): string {
    const slicedDate = date.slice(0, 10);
    if (!slicedDate.match(DATE_REGEX)) {
        throw new Error(`date "${date}" does not match the format YYYY-MM-DD`);
    }
    return slicedDate;
}

function parseReadableDate(humanReadableDate: string) {
    const humanReadableMonthMapping: Record<string, number> = {
        janvier: 1,
        février: 2,
        mars: 3,
        avril: 4,
        mai: 5,
        juin: 6,
        juillet: 7,
        août: 8,
        septembre: 9,
        octobre: 10,
        novembre: 11,
        décembre: 12,
    };
    const HUMAN_READABLE_DATE_REGEX = /^([a-zéû]+) (\d{4})$/;
    const result = humanReadableDate.match(HUMAN_READABLE_DATE_REGEX);
    if (!result || result.length !== 3) {
        throw new Error(`humanReadableDate "${humanReadableDate}" could not be parsed`);
    }
    const humanReadableMonth = result[1];
    const yearInf = result[2];
    const monthInf = humanReadableMonthMapping[humanReadableMonth];
    if (!monthInf) {
        throw new Error(`month "${humanReadableMonth}" could not be parsed`);
    }
    const formattedMonthInf = formatValue(monthInf);

    const date_debut = `${yearInf}-${formattedMonthInf}-01`;
    const date = addMonth(date_debut);

    return { date, date_debut };
}

export { parseCsv, dateHandler };
