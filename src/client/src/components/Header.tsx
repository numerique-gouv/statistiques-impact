import { Header as DSFRHeader } from '@codegouvfr/react-dsfr/Header';

function Header() {
    return (
        <DSFRHeader
            brandTop={<>DASHLORD</>}
            homeLinkProps={{
                to: '/',
                title: 'Accueil',
            }}
        />
    );
}

export { Header };
