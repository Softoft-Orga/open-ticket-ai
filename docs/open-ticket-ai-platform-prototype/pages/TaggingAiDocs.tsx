
import React from 'react';
import DocsLayout from '../components/DocsLayout';

const TaggingAiDocs: React.FC = () => {
  const toc = [
    { label: "Engine Overview", id: "overview" },
    { label: "Hierarchical Taxonomies", id: "taxonomies" },
    { label: "Privacy & On-Prem", id: "privacy-onprem" },
    { label: "Multilingual Logic", id: "multilingual" },
    { label: "Hardware Sizing", id: "hardware" }
  ];

  const breadcrumbs = [
    { label: "Documentation", to: "/docs" },
    { label: "Ticket Tagging AI" }
  ];

  return (
    <DocsLayout toc={toc} breadcrumbs={breadcrumbs}>
      <section id="overview" className="mb-20">
        <div className="inline-flex items-center gap-2 rounded-lg bg-primary/10 border border-primary/20 px-3 py-1 text-[10px] font-black uppercase text-primary-light mb-6">
          <span className="material-symbols-outlined text-xs">psychology</span>
          Core Intelligence Layer
        </div>
        <h1 className="text-4xl md:text-5xl font-black text-white mb-6 font-display leading-tight">Ticket Tagging AI</h1>
        <p className="text-xl text-slate-400 leading-relaxed mb-8">
          The high-performance classification engine that powers the Open Ticket AI platform. Designed to read, understand, and categorize support tickets at scale with human-level accuracy.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-6 rounded-xl bg-surface-dark border border-white/5">
            <span className="material-symbols-outlined text-primary mb-3">account_tree</span>
            <h3 className="text-white font-bold mb-2">Tree-Based Logic</h3>
            <p className="text-xs text-slate-500 leading-relaxed">Unlike flat taggers, our engine understands the parent-child relationship between categories.</p>
          </div>
          <div className="p-6 rounded-xl bg-surface-dark border border-white/5">
            <span className="material-symbols-outlined text-primary mb-3">speed</span>
            <h3 className="text-white font-bold mb-2">Sub-Second Latency</h3>
            <p className="text-xs text-slate-500 leading-relaxed">Average classification time for a 500-word ticket is under 400ms on optimized hardware.</p>
          </div>
        </div>
      </section>

      <section id="taxonomies" className="mb-20 pt-16 border-t border-white/5">
        <h2 className="text-3xl font-bold text-white mb-6 font-display">Hierarchical Taxonomies</h2>
        <p className="text-slate-400 mb-6 leading-relaxed">
          We move beyond simple "keyword matching." Our engine uses a 4-level deep ontology to provide actionable context for your agents.
        </p>
        <div className="bg-[#0f0814] border border-white/5 rounded-xl overflow-hidden mb-8 shadow-2xl">
          <div className="p-4 bg-white/5 border-b border-white/5 flex items-center gap-2">
            <span className="material-symbols-outlined text-xs text-primary">schema</span>
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Example Output Structure</span>
          </div>
          <div className="p-6 font-mono text-xs text-slate-300">
            <div className="text-primary-light">"classification": &#123;</div>
            <div className="pl-6">"intent": "incident/technical/access_issue",</div>
            <div className="pl-6">"system": "erp/finance/sap_gui",</div>
            <div className="pl-6">"urgency": "high",</div>
            <div className="pl-6">"sentiment": "frustrated",</div>
            <div className="pl-6">"is_blocking": true</div>
            <div className="text-primary-light">&#125;</div>
          </div>
        </div>
      </section>

      <section id="privacy-onprem" className="mb-20 pt-16 border-t border-white/5">
        <h2 className="text-3xl font-bold text-white mb-6 font-display">Privacy & On-Premise</h2>
        <p className="text-slate-400 mb-8 leading-relaxed">
          Data privacy is our "first-class citizen." Our engine is optimized to run on local infrastructure.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <h4 className="text-white font-bold flex items-center gap-2 text-sm">
              <span className="material-symbols-outlined text-green-400 text-sm">check_circle</span>
              GDPR & HIPAA
            </h4>
            <p className="text-xs text-slate-500 leading-relaxed">Zero data retention by default. Models are loaded in VRAM and cleared after inference.</p>
          </div>
          <div className="space-y-4">
            <h4 className="text-white font-bold flex items-center gap-2 text-sm">
              <span className="material-symbols-outlined text-green-400 text-sm">check_circle</span>
              Air-Gapped Ready
            </h4>
            <p className="text-xs text-slate-500 leading-relaxed">Our containers can run without external dependencies or internet access.</p>
          </div>
        </div>
      </section>

      <section id="multilingual" className="mb-20 pt-16 border-t border-white/5">
        <h2 className="text-3xl font-bold text-white mb-6 font-display">Multilingual Logic</h2>
        <p className="text-slate-400 mb-8 leading-relaxed">
          Built with German engineering at heart, we have specialized models for the DACH market.
        </p>
        <div className="flex flex-wrap gap-3">
          {['German (Native)', 'English', 'French', 'Spanish', 'Italian'].map((lang, i) => (
            <div key={i} className="px-4 py-2 rounded-lg bg-surface-dark border border-white/5 text-xs text-slate-300">
              {lang}
            </div>
          ))}
        </div>
      </section>

      <section id="hardware" className="mb-32 pt-16 border-t border-white/5">
        <h2 className="text-3xl font-bold text-white mb-6 font-display">Hardware Sizing</h2>
        <p className="text-slate-400 mb-8 leading-relaxed text-sm">
          Recommended specs for on-premise deployments based on daily ticket volume.
        </p>
        <div className="overflow-x-auto rounded-xl border border-white/5">
          <table className="w-full text-left text-xs bg-surface-dark">
            <thead>
              <tr className="border-b border-white/10 text-slate-500 bg-white/5">
                <th className="p-4 font-black uppercase tracking-widest">Volume / Day</th>
                <th className="p-4 font-black uppercase tracking-widest">CPU Threads</th>
                <th className="p-4 font-black uppercase tracking-widest">VRAM (NVIDIA)</th>
              </tr>
            </thead>
            <tbody className="text-slate-300">
              <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td className="p-4">Up to 1,000</td>
                <td className="p-4">4 Cores</td>
                <td className="p-4 font-mono">8 GB</td>
              </tr>
              <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td className="p-4">1,000 - 10,000</td>
                <td className="p-4">8 Cores</td>
                <td className="p-4 font-mono">16 GB</td>
              </tr>
              <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td className="p-4">10,000+</td>
                <td className="p-4">16+ Cores</td>
                <td className="p-4 font-mono">24+ GB (A10/L40)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </DocsLayout>
  );
};

export default TaggingAiDocs;
