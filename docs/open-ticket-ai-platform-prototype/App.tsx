
import React from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Blog from './pages/Blog';
import Products from './pages/Products';
import Docs from './pages/Docs';
import Services from './pages/Services';
import OtaDocs from './pages/OtaDocs';
import SyntheticDataDocs from './pages/SyntheticDataDocs';
import MediaLab from './pages/MediaLab';

const App: React.FC = () => {
  return (
    <HashRouter>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/blog" element={<Blog />} />
            <Route path="/products" element={<Products />} />
            <Route path="/docs" element={<Docs />} />
            <Route path="/docs/ota" element={<OtaDocs />} />
            <Route path="/docs/synthetic-data" element={<SyntheticDataDocs />} />
            <Route path="/services" element={<Services />} />
            <Route path="/media-lab" element={<MediaLab />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </HashRouter>
  );
};

export default App;
