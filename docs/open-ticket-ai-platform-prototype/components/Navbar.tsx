
import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar: React.FC = () => {
  const location = useLocation();
  const [isDocsOpen, setIsDocsOpen] = useState(false);

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="sticky top-0 z-50 w-full border-b border-surface-lighter bg-background-dark/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-2 text-white group">
          <div className="flex size-8 items-center justify-center rounded-lg bg-primary/20 text-primary transition-all group-hover:shadow-[0_0_15px_rgba(166,13,242,0.5)]">
            <span className="material-symbols-outlined text-2xl">confirmation_number</span>
          </div>
          <h2 className="font-display text-lg font-bold tracking-tight">Open Ticket AI</h2>
        </Link>

        <nav className="hidden md:flex flex-1 justify-center gap-8">
          <Link to="/products" className={`text-sm font-medium transition-colors ${isActive('/products') ? 'text-white' : 'text-gray-400 hover:text-white'}`}>Product</Link>
          <Link to="/services" className={`text-sm font-medium transition-colors ${isActive('/services') ? 'text-white' : 'text-gray-400 hover:text-white'}`}>Solutions</Link>
          <Link to="/services" className={`text-sm font-medium transition-colors ${location.pathname === '/services' ? 'text-white' : 'text-gray-400 hover:text-white'}`}>Pricing</Link>
          
          {/* Documentation Dropdown */}
          <div 
            className="relative group py-4"
            onMouseEnter={() => setIsDocsOpen(true)}
            onMouseLeave={() => setIsDocsOpen(false)}
          >
            <button className={`flex items-center gap-1 text-sm font-medium transition-colors ${location.pathname.startsWith('/docs') ? 'text-white' : 'text-gray-400 hover:text-white'}`}>
              Docs
              <span className={`material-symbols-outlined text-sm transition-transform duration-200 ${isDocsOpen ? 'rotate-180' : ''}`}>expand_more</span>
            </button>
            
            {/* Dropdown Menu */}
            <div className={`absolute top-full left-1/2 -translate-x-1/2 w-80 p-3 bg-surface-dark border border-white/10 rounded-2xl shadow-2xl transition-all duration-200 origin-top ${isDocsOpen ? 'opacity-100 scale-100' : 'opacity-0 scale-95 pointer-events-none'}`}>
              <div className="flex flex-col gap-2">
                <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest px-3 pt-2">Resources</div>
                <Link to="/docs" className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors group">
                  <div className="size-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                    <span className="material-symbols-outlined text-xl font-bold">hub</span>
                  </div>
                  <div>
                    <div className="text-white text-xs font-bold">Docs Hub</div>
                    <div className="text-slate-500 text-[10px]">Documentation Home</div>
                  </div>
                </Link>
                <div className="h-px bg-white/5 my-1 mx-3"></div>
                <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest px-3">Products & Guides</div>
                <Link to="/docs/tagging-ai" className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors group">
                  <span className="material-symbols-outlined text-primary text-xl px-2">psychology</span>
                  <div>
                    <div className="text-white text-xs font-bold">Ticket Tagging AI</div>
                    <div className="text-slate-500 text-[10px]">Classification Engine</div>
                  </div>
                </Link>
                <Link to="/docs/ota" className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors group">
                  <span className="material-symbols-outlined text-primary text-xl px-2">settings_suggest</span>
                  <div>
                    <div className="text-white text-xs font-bold">Open Ticket Automation</div>
                    <div className="text-slate-500 text-[10px]">Workflow Layer</div>
                  </div>
                </Link>
                <Link to="/docs/synthetic-data" className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors group">
                  <span className="material-symbols-outlined text-primary text-xl px-2">database</span>
                  <div>
                    <div className="text-white text-xs font-bold">Synthetic Data</div>
                    <div className="text-slate-500 text-[10px]">Privacy-Safe Datasets</div>
                  </div>
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <div className="flex items-center gap-4">
          <button className="flex h-9 items-center justify-center rounded-lg bg-primary px-4 text-xs font-bold text-white shadow-[0_0_15px_rgba(166,13,242,0.3)] transition-all hover:bg-primary-dark uppercase tracking-widest">
            Get Lite Free
          </button>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
