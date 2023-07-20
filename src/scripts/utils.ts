function parseCsv(csv: string, lineDelimitator = '\n'): Array<string[]> {
    return csv
        .trim()
        .split(lineDelimitator)
        .map((line) => line.split(','));
}

const dateHandler = {
    addMonth,
    substractMonth,
    parseDate,
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

function parseDate(date: string) {
    const DATE_REGEX = /^(\d{4})-(\d{2})-(\d{2})$/;
    const result = date.match(DATE_REGEX);
    if (!result || result.length !== 4) {
        throw new Error(`date "${date}" does not match the format YYYY-MM-DD`);
    }
    return { year: Number(result[1]), month: Number(result[2]), dayOfMonth: Number(result[3]) };
}

export { parseCsv, dateHandler, parseDate };
