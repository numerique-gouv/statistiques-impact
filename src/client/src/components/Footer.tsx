import { Footer as DSFRFooter } from '@codegouvfr/react-dsfr/Footer';

function Footer() {
    return (
        <DSFRFooter
            brandTop={
                <>
                    <div>République</div>
                    <div>Française</div>
                </>
            }
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
