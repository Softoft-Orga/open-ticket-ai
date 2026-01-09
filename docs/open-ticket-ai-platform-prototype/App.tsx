
import React from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Blog from './pages/Blog';
import BlogAdvantagesTaggingAi from './pages/BlogAdvantagesTaggingAi';
import Products from './pages/Products';
import Docs from './pages/Docs';
import Services from './pages/Services';
import OtaDocs from './pages/OtaDocs';
import OtaGettingStarted from './pages/OtaGettingStarted';
import SyntheticDataDocs from './pages/SyntheticDataDocs';
import TaggingAiDocs from './pages/TaggingAiDocs';
import MediaLab from './pages/MediaLab';

// Placeholder components for new documentation routes
const DocsPlaceholder = ({ title }: { title: string }) => (
  <div className="min-h-[60vh] flex flex-col items-center justify-center text-center p-10">
    <span className="material-symbols-outlined text-6xl text-slate-800 mb-4">construction</span>
    <h1 className="text-3xl font-bold text-white mb-4">{title}</h1>
    <p className="text-slate-500 max-w-md">This documentation page is currently being updated to reflect the latest platform changes in v2.4.</p>
  </div>
);

const App: React.FC = () => {
  return (
    <HashRouter>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/blog" element={<Blog />} />
            <Route path="/blog/advantages-of-ticket-tagging-ai" element={<BlogAdvantagesTaggingAi />} />
            <Route path="/products" element={<Products />} />
            <Route path="/docs" element={<Docs />} />
            <Route path="/docs/ota" element={<OtaDocs />} />
            <Route path="/docs/ota/getting-started" element={<OtaGettingStarted />} />
            <Route path="/docs/ota/rules" element={<DocsPlaceholder title="Rule Engine Reference" />} />
            <Route path="/docs/ota/connectors" element={<DocsPlaceholder title="Connector Setup" />} />
            <Route path="/docs/tagging-ai" element={<TaggingAiDocs />} />
            <Route path="/docs/tagging-ai/taxonomy" element={<DocsPlaceholder title="Taxonomy Design" />} />
            <Route path="/docs/tagging-ai/training" element={<DocsPlaceholder title="Model Training" />} />
            <Route path="/docs/synthetic-data" element={<SyntheticDataDocs />} />
            <Route path="/services" element={<Services />} />
            <Route path="/media-lab" element={<MediaLab />} />
            <Route path="/docs/*" element={<DocsPlaceholder title="Documentation Page" />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </HashRouter>
  );
};

export default App;
