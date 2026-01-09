
import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import DocsSidebar from './DocsSidebar';

interface DocsLayoutProps {
  children: React.ReactNode;
  toc?: { label: string; id: string }[];
  breadcrumbs: { label: string; to?: string }[];
}

const DocsLayout: React.FC<DocsLayoutProps> = ({ children, toc, breadcrumbs }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  // Close mobile menu on route change
  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location]);

  return (
    <div className="min-h-screen bg-background-dark">
      {/* Sub-Header / Breadcrumbs */}
      <div className="border-b border-white/5 bg-[#0f0814]/50 sticky top-16 z-40 backdrop-blur-sm shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-12 flex items-center justify-between">
          <div className="flex items-center text-[10px] gap-2 overflow-hidden">
            <button 
              onClick={() => setIsMobileMenuOpen(true)}
              className="lg:hidden p-1.5 rounded-md bg-white/5 text-slate-400 hover:text-white mr-2"
            >
              <span className="material-symbols-outlined text-lg">menu_open</span>
            </button>
            {breadcrumbs.map((crumb, i) => (
              <React.Fragment key={i}>
                {crumb.to ? (
                  <Link to={crumb.to} className="text-slate-500 hover:text-white transition-colors whitespace-nowrap">{crumb.label}</Link>
                ) : (
                  <span className="text-primary-light font-bold truncate">{crumb.label}</span>
                )}
                {i < breadcrumbs.length - 1 && (
                  <span className="material-symbols-outlined text-xs text-slate-700">chevron_right</span>
                )}
              </React.Fragment>
            ))}
          </div>

          <div className="hidden sm:flex items-center gap-4">
             <a href="https://github.com/open-ticket-ai" target="_blank" className="text-slate-500 hover:text-white flex items-center gap-1.5 text-[10px] font-bold">
               <span className="material-symbols-outlined text-sm">terminal</span>
               GitHub
             </a>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12 flex flex-col lg:flex-row gap-12">
        {/* Desktop Sidebar - Left */}
        <aside className="hidden lg:block w-72 flex-shrink-0 sticky top-32 h-[calc(100vh-160px)] overflow-y-auto cyber-scrollbar pr-4">
          <DocsSidebar />
        </aside>

        {/* Mobile Sidebar Overlay */}
        {isMobileMenuOpen && (
          <div className="fixed inset-0 z-[60] lg:hidden">
            <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setIsMobileMenuOpen(false)}></div>
            <div className="absolute inset-y-0 left-0 w-72 bg-background-dark border-r border-white/10 p-6 flex flex-col animate-in slide-in-from-left duration-300">
              <div className="flex items-center justify-between mb-8">
                <span className="text-xs font-black uppercase tracking-widest text-primary">Documentation</span>
                <button onClick={() => setIsMobileMenuOpen(false)} className="text-slate-500">
                  <span className="material-symbols-outlined">close</span>
                </button>
              </div>
              <div className="flex-1 overflow-y-auto cyber-scrollbar">
                <DocsSidebar onClose={() => setIsMobileMenuOpen(false)} />
              </div>
            </div>
          </div>
        )}

        {/* Main Content Area */}
        <main className="flex-1 min-w-0">
          <div className="max-w-4xl mx-auto">
            <div className="animate-in fade-in slide-in-from-bottom-2 duration-700">
              {children}
            </div>
          </div>
        </main>

        {/* Local Table of Contents - Right */}
        {toc && toc.length > 0 && (
          <aside className="hidden xl:block w-56 flex-shrink-0 sticky top-32 h-fit">
            <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-6 px-4">On this page</h4>
            <nav className="flex flex-col gap-1 border-l border-white/5">
              {toc.map((item, i) => (
                <a
                  key={i}
                  href={`#${item.id}`}
                  className="px-4 py-1.5 text-slate-400 hover:text-white border-l-2 border-transparent hover:border-primary transition-all text-[11px] font-medium"
                >
                  {item.label}
                </a>
              ))}
            </nav>
            
            <div className="mt-12 px-4">
              <div className="p-4 rounded-xl bg-gradient-to-br from-primary/10 to-surface-dark border border-white/5 relative overflow-hidden group">
                <div className="relative z-10">
                  <span className="material-symbols-outlined text-primary mb-2 text-xl">forum</span>
                  <div className="text-[10px] font-black text-white uppercase mb-1">Support Discord</div>
                  <p className="text-[9px] text-slate-500 leading-tight mb-3">Get help from the community.</p>
                  <button className="w-full py-1.5 bg-white/5 rounded text-[9px] font-bold text-slate-300 hover:bg-white/10 transition-colors">Join Server</button>
                </div>
              </div>
            </div>
          </aside>
        )}
      </div>
    </div>
  );
};

export default DocsLayout;
