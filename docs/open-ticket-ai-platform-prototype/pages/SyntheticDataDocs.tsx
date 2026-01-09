
import React from 'react';
import { Link } from 'react-router-dom';

const SyntheticDataDocs: React.FC = () => {
  return (
    <div className="min-h-screen bg-background-dark">
      {/* Sub-Header / Breadcrumbs */}
      <div className="border-b border-white/5 bg-[#0f0814]/50 sticky top-16 z-40 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 h-12 flex items-center text-xs gap-2">
          <Link to="/docs" className="text-slate-500 hover:text-white transition-colors">Documentation Hub</Link>
          <span className="material-symbols-outlined text-sm text-slate-700">chevron_right</span>
          <span className="text-cyan-400 font-bold">Synthetic Data Generator</span>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-16 lg:flex gap-16">
        {/* Table of Contents - Sidebar */}
        <aside className="hidden lg:block w-64 flex-shrink-0 sticky top-32 h-fit">
          <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-6">On this page</h4>
          <nav className="flex flex-col gap-4 text-sm">
            <a href="#introduction" className="text-white font-bold border-l-2 border-cyan-400 pl-4">Introduction</a>
            <a href="#privacy" className="text-slate-400 hover:text-white transition-colors pl-4 border-l-2 border-transparent hover:border-white/10">Data Privacy</a>
            <a href="#generation" className="text-slate-400 hover:text-white transition-colors pl-4 border-l-2 border-transparent hover:border-white/10">Generation Process</a>
            <a href="#customization" className="text-slate-400 hover:text-white transition-colors pl-4 border-l-2 border-transparent hover:border-white/10">Custom Schemas</a>
            <a href="#formats" className="text-slate-400 hover:text-white transition-colors pl-4 border-l-2 border-transparent hover:border-white/10">Export Formats</a>
          </nav>

          <div className="mt-12 p-6 rounded-2xl bg-cyan-400/5 border border-cyan-400/10">
            <h5 className="text-xs font-bold text-cyan-400 mb-2">Dataset Pricing</h5>
            <p className="text-[11px] text-slate-400 mb-4">We offer fixed-price packs for high-volume datasets.</p>
            <Link to="/services" className="text-[11px] font-bold text-white flex items-center gap-1 group">
              View Pricing Packages
              <span className="material-symbols-outlined text-xs group-hover:translate-x-1 transition-transform">arrow_forward</span>
            </Link>
          </div>
        </aside>

        {/* Main Content */}
        <div className="flex-1 max-w-3xl">
          <section id="introduction" className="mb-20">
            <div className="inline-flex items-center gap-2 rounded-lg bg-cyan-400/10 border border-cyan-400/20 px-3 py-1 text-[10px] font-black uppercase text-cyan-400 mb-6">
              <span className="material-symbols-outlined text-xs">database</span>
              Data Generation Layer
            </div>
            <h1 className="text-4xl md:text-5xl font-black text-white mb-6 font-display">Synthetic Data Generator</h1>
            <p className="text-xl text-slate-400 leading-relaxed mb-8">
              Generate realistic, high-quality ticket datasets without exposing sensitive PII (Personally Identifiable Information). Perfect for training LLMs, benchmarking support teams, or testing automation rules in staging.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-6 rounded-xl bg-[#0c151a] border border-cyan-400/10">
                <span className="material-symbols-outlined text-cyan-400 mb-3">verified_user</span>
                <h3 className="text-white font-bold mb-2">100% Privacy</h3>
                <p className="text-xs text-slate-500 leading-relaxed">No real customer data is ever used. Models are seeded with ontologies, not private records.</p>
              </div>
              <div className="p-6 rounded-xl bg-[#0c151a] border border-cyan-400/10">
                <span className="material-symbols-outlined text-cyan-400 mb-3">language</span>
                <h3 className="text-white font-bold mb-2">Multilingual</h3>
                <p className="text-xs text-slate-500 leading-relaxed">Supports German, English, French, and Spanish with native-level nuances and technical jargon.</p>
              </div>
            </div>
          </section>

          <section id="privacy" className="mb-20 pt-16 border-t border-white/5">
            <h2 className="text-3xl font-bold text-white mb-6 font-display">Data Privacy</h2>
            <p className="text-slate-400 mb-6 leading-relaxed">
              Our generator operates on a "Zero-PII" principle. Instead of obfuscating existing data, we construct tickets from the ground up using a sophisticated semantic engine.
            </p>
            <ul className="space-y-4">
              <li className="flex items-start gap-3">
                <span className="material-symbols-outlined text-cyan-400 text-sm mt-1">shield</span>
                <span className="text-slate-300 text-sm">Compliant with GDPR, HIPAA, and industry-specific privacy standards.</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="material-symbols-outlined text-cyan-400 text-sm mt-1">block</span>
                <span className="text-slate-300 text-sm">Eliminates the risk of "data leakage" in model training.</span>
              </li>
            </ul>
          </section>

          <section id="generation" className="mb-20 pt-16 border-t border-white/5">
            <h2 className="text-3xl font-bold text-white mb-6 font-display">Generation Process</h2>
            <p className="text-slate-400 mb-8 leading-relaxed">
              We use a hierarchical approach to ensure the generated data follows your actual business logic.
            </p>
            <div className="space-y-6">
              <div className="flex gap-6">
                <div className="flex-shrink-0 size-8 rounded-full bg-cyan-400/20 text-cyan-400 flex items-center justify-center font-bold text-xs">1</div>
                <div>
                  <h4 className="text-white font-bold mb-1">Taxonomy Ingestion</h4>
                  <p className="text-xs text-slate-500">We load your categories, queues, and priority levels.</p>
                </div>
              </div>
              <div className="flex gap-6">
                <div className="flex-shrink-0 size-8 rounded-full bg-cyan-400/20 text-cyan-400 flex items-center justify-center font-bold text-xs">2</div>
                <div>
                  <h4 className="text-white font-bold mb-1">Semantic Sampling</h4>
                  <p className="text-xs text-slate-500">The engine creates diverse subject lines and bodies based on typical user personas.</p>
                </div>
              </div>
              <div className="flex gap-6">
                <div className="flex-shrink-0 size-8 rounded-full bg-cyan-400/20 text-cyan-400 flex items-center justify-center font-bold text-xs">3</div>
                <div>
                  <h4 className="text-white font-bold mb-1">Validation & Export</h4>
                  <p className="text-xs text-slate-500">Data is validated against your schema constraints and exported.</p>
                </div>
              </div>
            </div>
          </section>

          <section id="customization" className="mb-20 pt-16 border-t border-white/5">
            <h2 className="text-3xl font-bold text-white mb-6 font-display">Custom Schemas</h2>
            <p className="text-slate-400 mb-8 leading-relaxed">
              Define the structure of your tickets in a simple JSON format to match your helpdesk's custom fields.
            </p>
            <div className="bg-[#0c0d15] rounded-xl p-6 border border-slate-800">
               <pre className="text-xs text-cyan-400 font-mono leading-relaxed overflow-x-auto">
{`schema:
  fields:
    - name: "customer_id"
      type: "pattern"
      value: "CUST-[0-9]{5}"
    - name: "product_version"
      type: "enum"
      values: ["v2.1", "v2.4-beta", "v3.0"]
    - name: "sentiment"
      type: "weight"
      distribution:
        frustrated: 0.2
        neutral: 0.7
        happy: 0.1`}
               </pre>
            </div>
          </section>

          <section id="formats" className="mb-32 pt-16 border-t border-white/5">
            <h2 className="text-3xl font-bold text-white mb-6 font-display">Export Formats</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {['JSONL', 'CSV', 'XML', 'SQL'].map((fmt, i) => (
                <div key={i} className="p-4 rounded-xl bg-surface-dark border border-white/5 text-center">
                  <span className="text-xs font-black text-slate-500 mb-2 block">FORMAT</span>
                  <span className="text-lg font-bold text-white">{fmt}</span>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default SyntheticDataDocs;
