
import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar: React.FC = () => {
  const location = useLocation();
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
        <nav className="hidden md:flex flex-1 justify-center gap-6">
          <Link to="/products" className={`text-sm font-medium transition-colors ${isActive('/products') ? 'text-white' : 'text-gray-400 hover:text-white'}`}>Products</Link>
          <Link to="/services" className={`text-sm font-medium transition-colors ${isActive('/services') ? 'text-white' : 'text-gray-400 hover:text-white'}`}>Services</Link>
          <Link to="/media-lab" className={`text-sm font-medium transition-colors ${isActive('/media-lab') ? 'text-white' : 'text-gray-400 hover:text-white'}`}>Media Lab</Link>
          <Link to="/docs/ota" className={`text-sm font-medium transition-colors ${isActive('/docs/ota') ? 'text-white' : 'text-gray-400 hover:text-white'}`}>OTA Docs</Link>
          <Link to="/blog" className={`text-sm font-medium transition-colors ${isActive('/blog') ? 'text-white' : 'text-gray-400 hover:text-white'}`}>Blog</Link>
          <Link to="/docs" className={`text-sm font-medium transition-colors ${isActive('/docs') ? 'text-white' : 'text-gray-400 hover:text-white'}`}>Docs Hub</Link>
        </nav>
        <div className="flex items-center gap-4">
          <button className="hidden sm:flex h-9 items-center justify-center rounded-lg bg-surface-lighter px-4 text-sm font-bold text-white transition-colors hover:bg-surface-lighter/80 border border-primary/20">
            Login
          </button>
          <button className="flex h-9 items-center justify-center rounded-lg bg-primary px-4 text-sm font-bold text-white shadow-[0_0_15px_rgba(166,13,242,0.3)] transition-all hover:bg-primary-dark">
            Get Demo
          </button>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
