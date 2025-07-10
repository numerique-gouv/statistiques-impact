import { Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home';
import { Indicators } from './pages/Indicators';

function Router() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/indicators/:productId" element={<Indicators />} />
        </Routes>
    );
}

export { Router };
