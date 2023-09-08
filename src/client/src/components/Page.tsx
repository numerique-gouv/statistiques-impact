import React from 'react';
import { fr } from '@codegouvfr/react-dsfr';
import { Header } from './Header';
import { Footer } from './Footer';

function Page(props: { children: JSX.Element | JSX.Element[] | boolean }) {
    return (
        <>
            <Header />
            <div className={fr.cx('fr-m-8v')}>{props.children}</div>
            <Footer />
        </>
    );
}

export { Page };
