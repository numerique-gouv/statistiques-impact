const metabaseAdaptator = { format };

type metabaseOutputRowType = { 'Date Begin': string; Count: number };

type formattedRowType = { date: string; date_debut: string; value: number };

function format(metabaseOutputRows: Array<metabaseOutputRowType>, frequency: 'month') {
    const output: Array<formattedRowType> = [];
    switch (frequency) {
        case 'month':
            for (const metabaseOutputRow of metabaseOutputRows) {
                const dateInf = new Date(metabaseOutputRow['Date Begin']);
                const dateSup = new Date(dateInf);
                if (dateInf.getMonth() === 11) {
                    dateSup.setMonth(0);
                    dateSup.setFullYear(dateInf.getFullYear() + 1);
                } else {
                    dateSup.setMonth(dateInf.getMonth() + 1);
                }
                const now = new Date();

                if (dateSup.getTime() > now.getTime()) {
                    continue;
                }
                const formattedSupYear = `${dateSup.getFullYear()}`;
                const formattedSupMonth =
                    dateSup.getMonth() + 1 < 10
                        ? `0${dateSup.getMonth() + 1}`
                        : `${dateSup.getMonth() + 1}`;
                const formattedSupDayOfMonth =
                    dateSup.getDate() < 10 ? `0${dateSup.getDate()}` : `${dateSup.getDate()}`;
                const date = `${formattedSupYear}-${formattedSupMonth}-${formattedSupDayOfMonth}`;
                const date_debut = metabaseOutputRow['Date Begin'].slice(0, 10);
                const value = metabaseOutputRow.Count;
                output.push({ date_debut, value, date });
            }
            break;
    }

    return output;
}

export { metabaseAdaptator };
