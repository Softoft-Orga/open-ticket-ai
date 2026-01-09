
import React from 'react';

export const Badge: React.FC<{ label: string; color: string }> = ({ label, color }) => (
  <span className={`inline-flex items-center rounded-full px-4 py-1.5 text-xs font-bold border ${color}`}>
    {label}
  </span>
);

export const CapabilityCard: React.FC<{ icon: string; title: string; desc: string }> = ({ icon, title, desc }) => (
  <div className="group p-8 rounded-2xl bg-surface-dark border border-border-dark hover:border-primary/50 transition-all duration-500 hover:shadow-[0_0_40px_rgba(166,13,242,0.15)]">
    <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center text-primary mb-8 group-hover:scale-110 transition-transform duration-500 group-hover:bg-primary/20">
      <span className="material-symbols-outlined text-4xl">{icon}</span>
    </div>
    <h3 className="font-display text-2xl font-bold text-white mb-4 group-hover:text-primary transition-colors">{title}</h3>
    <p className="text-gray-400 text-base leading-relaxed">{desc}</p>
  </div>
);
