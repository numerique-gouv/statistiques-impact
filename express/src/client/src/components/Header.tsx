import { Header as DSFRHeader } from '@codegouvfr/react-dsfr/Header';

function Header() {
    return (
        <DSFRHeader
            brandTop={
                <>
                    <div>République</div>
                    <div>Française</div>
                </>
            }
            serviceTitle="Statistiques d'usage"
            homeLinkProps={{
                to: '/',
                title: 'Accueil',
            }}
        />
    );
}

export { Header };
