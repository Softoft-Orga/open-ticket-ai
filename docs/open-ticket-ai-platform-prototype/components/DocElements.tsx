
import React from 'react';
import { Link } from 'react-router-dom';

export const DocCard: React.FC<{ icon: string; title: string; desc: string; link: string; to?: string }> = ({ icon, title, desc, link, to = "#" }) => (
  <Link
    to={to}
    className="group relative flex flex-col p-10 rounded-2xl bg-card-dark border border-slate-800 hover:border-primary/50 transition-all duration-300 hover:-translate-y-2 shadow-glow"
  >
    <div className="h-16 w-16 rounded-xl bg-slate-800 flex items-center justify-center text-white mb-10 group-hover:bg-primary group-hover:text-background-dark transition-colors duration-300">
      <span className="material-symbols-outlined text-4xl">{icon}</span>
    </div>
    <h3 className="text-2xl font-bold mb-4 text-white group-hover:text-primary transition-colors">{title}</h3>
    <p className="text-slate-400 text-lg leading-relaxed mb-8 flex-grow">{desc}</p>
    <div className="flex items-center text-primary text-sm font-bold uppercase tracking-widest">
      {link} <span className="material-symbols-outlined text-lg ml-2 group-hover:translate-x-1 transition-transform">arrow_forward</span>
    </div>
  </Link>
);

export const QuickLink: React.FC<{ icon: string; label: string; to?: string }> = ({ icon, label, to = "#" }) => (
  <Link
    to={to}
    className="group flex flex-col items-center justify-center p-8 rounded-xl bg-card-dark border border-slate-800 hover:border-primary/40 hover:bg-slate-800/50 transition-all duration-300"
  >
    <span className="material-symbols-outlined text-slate-500 group-hover:text-primary mb-3 text-3xl transition-colors">{icon}</span>
    <span className="text-sm font-bold text-slate-400 group-hover:text-white transition-colors">{label}</span>
  </Link>
);
