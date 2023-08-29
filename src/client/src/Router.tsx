import { Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home';
import { Product } from './pages/Product';
import { Measures } from './pages/Measures';
import { Measure } from './pages/Measure';

function Router() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/products/:productId" element={<Product />} />
            <Route path="/products/:productId/:sub1" element={<Product />} />
            <Route path="/products/:productId/:sub1/:sub2" element={<Product />} />
            <Route path="/measures/:measureId" element={<Measure />} />
            <Route path="/measures" element={<Measures />} />
        </Routes>
    );
}

export { Router };
