const padAdaptator = { format };

type padApiOutputType = {
    dateInf: string;
    dateSup: string;
    activeUsers: number;
};

function format(padApiOutput: padApiOutputType) {
    const DATE_REGEX = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/;
    let castPadApiOutput = {
        dateInf: padApiOutput.dateInf || '',
        dateSup: padApiOutput.dateSup || '',
        activeUsers: Number(padApiOutput.activeUsers),
    };
    if (
        !castPadApiOutput.dateInf.match(DATE_REGEX) ||
        !castPadApiOutput.dateSup.match(DATE_REGEX) ||
        isNaN(castPadApiOutput.activeUsers)
    ) {
        throw new Error('The pad API did not return the right format');
    }

    return [
        {
            date: castPadApiOutput.dateSup.slice(0, 10),
            date_debut: castPadApiOutput.dateInf.slice(0, 10),
            valeur: castPadApiOutput.activeUsers,
            indicateur: 'utilisateurs actifs',
            unite_mesure: 'unité',
            frequence_calcul: 'mensuelle',
            est_periode: true,
        },
    ];
}

export { padAdaptator };
