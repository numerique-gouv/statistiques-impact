import React from 'react';
import { Footer as DSFRFooter } from '@codegouvfr/react-dsfr/Footer';

function Footer() {
    return (
        <DSFRFooter
            brandTop={<>Statistiques</>}
            accessibility="non compliant"
            homeLinkProps={{
                to: '/',
                title: 'Accueil - ',
            }}
            personalDataLinkProps={{
                to: '#',
            }}
            termsLinkProps={{
                to: '#',
            }}
            websiteMapLinkProps={{
                to: '#',
            }}
        />
    );
}
export { Footer };
