import React, { ReactElement } from 'react';
import { fr } from '@codegouvfr/react-dsfr';
import { Header } from './Header';
import { Footer } from './Footer';

function Page(props: { children: ReactElement }) {
    return (
        <>
            <Header />
            <div className={fr.cx('fr-m-8v')}>{props.children}</div>
            <Footer />
        </>
    );
}

export { Page };
