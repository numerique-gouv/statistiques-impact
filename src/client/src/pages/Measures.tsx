import React from 'react';
import { Link } from 'react-router-dom';
import Table from '@codegouvfr/react-dsfr/Table';
import { Badge } from '@codegouvfr/react-dsfr/Badge';

import { Page } from '../components/Page';

function Measures() {
    const data = computeData();
    return (
        <Page>
            <Table data={data} caption="Mesures"></Table>
        </Page>
    );

    function computeData() {
        return [
            {
                label: 'Scan des dépendances',
                measureId: 'DEPENDENCY_SCAN',
                value: Math.floor(Math.random() * 100),
            },
            {
                label: 'Scan du code source',
                measureId: 'SOURCE_CODE_SCAN',
                value: Math.floor(Math.random() * 100),
            },
            {
                label: 'Détection de fuite de secrets',
                measureId: 'SECRET_LEAK_DETECTION',
                value: Math.floor(Math.random() * 100),
            },
            {
                label: 'Certificat HTTPS',
                measureId: 'HTTPS_CONNECTION',
                value: Math.floor(Math.random() * 100),
            },
            {
                label: 'Scan anti-malware automatique',
                measureId: 'MALWARE_SCAN',
                value: Math.floor(Math.random() * 100),
            },
            {
                label: "Implémentation d'une Content-Security-Policy",
                measureId: 'CSP_HEADER_IMPLEMENTED',
                value: Math.floor(Math.random() * 100),
            },
            {
                label: 'Inscription à programme Bug Bounty',
                measureId: 'BUG_BOUNTY',
                value: Math.floor(Math.random() * 100),
            },
            {
                label: 'Implémentation de X-Frame-Option',
                measureId: 'X_FRAME_OPTION_HEADER_IMPLEMENTED',
                value: Math.floor(Math.random() * 100),
            },
        ].map(({ label, measureId, value }) => {
            return [
                <Link to={`/measures/${measureId}`}>{label}</Link>,
                <Badge severity={value > 50 ? 'success' : 'warning'}>
                    {value > 50 ? 'OK' : 'En cours'}
                </Badge>,
            ];
        });
    }
}

export { Measures };
