
import React from 'react';

export const PricingCard: React.FC<{ 
  title: string; 
  subtitle?: string;
  price: string; 
  features: string[]; 
  badge?: string; 
  highlighted?: boolean;
  buttonText?: string;
  priceSuffix?: string;
}> = ({ title, subtitle, price, features, badge, highlighted, buttonText = "Contact Sales", priceSuffix = "" }) => (
  <div className={`flex flex-col rounded-2xl p-8 transition-all h-full ${highlighted ? 'bg-[#1a1033] border-2 border-primary shadow-[0_0_30px_rgba(166,13,242,0.2)]' : 'bg-[#150c19] border border-white/5 hover:border-white/20'}`}>
    <div className="mb-6">
      <h4 className="text-white text-xl font-bold font-display">{title}</h4>
      {subtitle && <p className="text-primary text-xs font-bold uppercase mt-1">{subtitle}</p>}
    </div>
    <div className="mb-8">
      <div className="text-slate-400 text-sm mb-1 uppercase tracking-widest font-bold">from</div>
      <div className="text-3xl font-bold text-white font-display">{price} <span className="text-sm font-normal text-slate-500">{priceSuffix}</span></div>
    </div>
    <ul className="space-y-3 mb-10 flex-grow">
      {features.map((f, i) => (
        <li key={i} className="flex items-start gap-2.5 text-sm text-slate-300">
          <span className="material-symbols-outlined text-primary text-lg flex-shrink-0">check</span>
          <span>{f}</span>
        </li>
      ))}
    </ul>
    <button className={`w-full rounded-lg py-3.5 text-sm font-bold transition-all ${highlighted ? 'bg-primary hover:bg-primary-dark text-white' : 'bg-transparent border border-white/20 text-white hover:bg-white/5'}`}>
      {buttonText}
    </button>
  </div>
);

export const IntegrationPackageCard: React.FC<{
  title: string;
  subtitle: string;
  price: string;
  systems: string;
  features: string[];
  buttonText: string;
  highlighted?: boolean;
}> = ({ title, subtitle, price, systems, features, buttonText, highlighted }) => (
  <div className={`rounded-2xl p-8 flex flex-col h-full ${highlighted ? 'bg-[#1d1023] border border-primary/30' : 'bg-[#120818] border border-white/5'}`}>
    <div className="flex justify-between items-start mb-6">
      <div>
        <h4 className="text-white text-xl font-bold">{title}</h4>
        <p className="text-primary text-xs font-bold uppercase tracking-widest mt-1">{subtitle}</p>
      </div>
      <div className="text-right">
        <div className="text-2xl font-bold text-white">{price}</div>
        <div className="text-[10px] text-slate-500 uppercase">One-time fee</div>
      </div>
    </div>
    
    <div className="mb-6">
      <div className="text-[10px] text-slate-500 uppercase font-bold tracking-widest mb-2">Supported Systems</div>
      <div className="text-slate-200 text-sm font-medium">{systems}</div>
    </div>

    <ul className="space-y-2.5 mb-8 flex-grow">
      {features.map((f, i) => (
        <li key={i} className="flex items-start gap-2 text-sm text-slate-400">
          <span className="material-symbols-outlined text-primary text-lg flex-shrink-0">check</span>
          <span>{f}</span>
        </li>
      ))}
    </ul>

    <button className={`w-full rounded-lg py-3 text-sm font-bold transition-all ${highlighted ? 'bg-primary text-white hover:bg-primary-dark' : 'bg-transparent border border-white/20 text-white hover:bg-white/5'}`}>
      {buttonText}
    </button>
  </div>
);

export const ExtensionItem: React.FC<{ icon: string; title: string; desc: string }> = ({ icon, title, desc }) => (
  <div className="flex items-start gap-4">
    <div className="text-primary mt-0.5">
      <span className="material-symbols-outlined text-2xl">{icon}</span>
    </div>
    <div>
      <h5 className="text-white text-sm font-bold mb-1">{title}</h5>
      <p className="text-slate-500 text-xs leading-relaxed">{desc}</p>
    </div>
  </div>
);
