function computeBeginningDateToWatch(now: Date, months: number) {
    const MONTH_IN_MILLISECONDS = 30 * 24 * 60 * 60 * 1000;
    const DURATION_TO_WATCH = months * MONTH_IN_MILLISECONDS;
    const beginningDateToWatch = new Date();
    beginningDateToWatch.setTime(now.getTime() - DURATION_TO_WATCH);
    return beginningDateToWatch.toISOString();
}

export { computeBeginningDateToWatch };
