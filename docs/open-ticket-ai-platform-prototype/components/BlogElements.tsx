
import React from 'react';

export const TopicLink: React.FC<{ icon: string; label: string; count?: number; active?: boolean }> = ({ icon, label, count, active }) => (
  <a className={`flex items-center justify-between rounded-xl px-4 py-3.5 text-sm font-medium transition-all ${active ? 'bg-surface-dark border border-primary/40 text-white shadow-glow' : 'text-text-dim hover:bg-surface-dark hover:text-white'}`} href="#">
    <span className="flex items-center gap-3">
      <span className={`material-symbols-outlined text-xl ${active ? 'text-primary' : 'group-hover:text-primary transition-colors'}`}>{icon}</span>
      {label}
    </span>
    {count && <span className="text-xs text-text-dim bg-surface-lighter px-2.5 py-1 rounded-full">{count}</span>}
  </a>
);

export const ArticleCard: React.FC<{ category: string; title: string; date: string; img: string; desc: string; tagColor?: string; bgColor?: string }> = ({ category, title, date, img, desc, tagColor = "text-primary-light", bgColor = "bg-primary/10" }) => (
  <article className="group flex flex-col overflow-hidden rounded-2xl border border-surface-lighter bg-surface-dark transition-all hover:border-primary/50 hover:shadow-glow hover:-translate-y-2">
    <div className="relative aspect-video w-full overflow-hidden bg-surface-lighter">
      <img src={img} alt={title} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110 opacity-70" />
    </div>
    <div className="flex flex-1 flex-col p-8">
      <div className="mb-4 flex items-center justify-between">
        <span className={`rounded-md px-3 py-1 text-xs font-bold ${bgColor} ${tagColor} uppercase tracking-wide`}>{category}</span>
        <span className="text-xs text-text-dim">{date}</span>
      </div>
      <h3 className="mb-3 font-display text-2xl font-bold leading-tight text-white group-hover:text-primary-light transition-colors">{title}</h3>
      <p className="mb-6 line-clamp-2 text-base text-text-dim leading-relaxed">{desc}</p>
      <div className="mt-auto flex items-center text-sm font-bold text-white group-hover:text-primary transition-colors">
        Read Article <span className="material-symbols-outlined ml-2 text-xl transition-transform group-hover:translate-x-1">arrow_forward</span>
      </div>
    </div>
  </article>
);
