import React from 'react';
import ReactDOM from 'react-dom/client';
import reportWebVitals from './reportWebVitals';
import { startReactDsfr } from '@codegouvfr/react-dsfr/spa';
import { BrowserRouter, Link } from 'react-router-dom';
import { Router } from './Router';

startReactDsfr({ defaultColorScheme: 'system', Link });

//Only in TypeScript projects
declare module '@codegouvfr/react-dsfr/spa' {
    interface RegisterLink {
        Link: typeof Link;
    }
}

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
    <React.StrictMode>
        <BrowserRouter>
            <Router />
        </BrowserRouter>
    </React.StrictMode>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
