
import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => (
  <footer className="border-t border-white/5 bg-background-dark py-24">
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
        <div className="md:col-span-1">
          <div className="flex items-center gap-2 mb-6">
            <div className="flex size-8 items-center justify-center rounded bg-primary/20 text-primary">
              <span className="material-symbols-outlined text-xl">confirmation_number</span>
            </div>
            <span className="font-display text-lg font-bold text-white tracking-tight">Open Ticket AI</span>
          </div>
          <p className="text-slate-500 text-sm leading-relaxed max-w-xs">
            Intelligent automation for OTRS, Znuny, and Zammad. German Engineering.
          </p>
        </div>
        
        <div>
          <h4 className="text-white font-bold text-sm mb-6 uppercase tracking-widest">Product</h4>
          <ul className="space-y-4 text-slate-500 text-sm">
            <li><Link to="/products" className="hover:text-primary transition-colors">Features</Link></li>
            <li><Link to="/services" className="hover:text-primary transition-colors">Integrations</Link></li>
            <li><Link to="/docs" className="hover:text-primary transition-colors">Security</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="text-white font-bold text-sm mb-6 uppercase tracking-widest">Company</h4>
          <ul className="space-y-4 text-slate-500 text-sm">
            <li><a href="#" className="hover:text-primary transition-colors">About Us</a></li>
            <li><a href="#" className="hover:text-primary transition-colors">Careers</a></li>
            <li><a href="#" className="hover:text-primary transition-colors">Legal</a></li>
          </ul>
        </div>

        <div>
          <h4 className="text-white font-bold text-sm mb-6 uppercase tracking-widest">Connect</h4>
          <div className="flex gap-4 text-slate-500">
            <a href="#" className="hover:text-primary transition-colors">
              <span className="material-symbols-outlined">link</span>
            </a>
            <a href="#" className="hover:text-primary transition-colors">
              <span className="material-symbols-outlined">campaign</span>
            </a>
          </div>
        </div>
      </div>
      
      <div className="pt-8 border-t border-white/5 flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="text-xs text-slate-600">
          © 2024 Open Ticket AI GmbH. All rights reserved.
        </div>
        <div className="flex gap-8 text-xs text-slate-600">
          <a className="hover:text-white" href="#">Privacy Policy</a>
          <a className="hover:text-white" href="#">Imprint</a>
        </div>
      </div>
    </div>
  </footer>
);

export default Footer;
