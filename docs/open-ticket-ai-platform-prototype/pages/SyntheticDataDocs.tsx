
import React from 'react';
import DocsLayout from '../components/DocsLayout';

const SyntheticDataDocs: React.FC = () => {
  const toc = [
    { label: "Introduction", id: "introduction" },
    { label: "Data Privacy", id: "privacy" },
    { label: "Generation Process", id: "generation" },
    { label: "Custom Schemas", id: "customization" },
    { label: "Export Formats", id: "formats" }
  ];

  const breadcrumbs = [
    { label: "Documentation", to: "/docs" },
    { label: "Synthetic Data Generator" }
  ];

  return (
    <DocsLayout toc={toc} breadcrumbs={breadcrumbs}>
      <section id="introduction" className="mb-20">
        <div className="inline-flex items-center gap-2 rounded-lg bg-cyan-400/10 border border-cyan-400/20 px-3 py-1 text-[10px] font-black uppercase text-cyan-400 mb-6">
          <span className="material-symbols-outlined text-xs">database</span>
          Data Generation Layer
        </div>
        <h1 className="text-4xl md:text-5xl font-black text-white mb-6 font-display">Synthetic Data Generator</h1>
        <p className="text-xl text-slate-400 leading-relaxed mb-8">
          Generate realistic, high-quality ticket datasets without exposing sensitive PII. Perfect for training LLMs.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-6 rounded-xl bg-[#0c151a] border border-cyan-400/10">
            <span className="material-symbols-outlined text-cyan-400 mb-3">verified_user</span>
            <h3 className="text-white font-bold mb-2">100% Privacy</h3>
            <p className="text-xs text-slate-500 leading-relaxed">No real customer data is ever used. Models are seeded with ontologies.</p>
          </div>
          <div className="p-6 rounded-xl bg-[#0c151a] border border-cyan-400/10">
            <span className="material-symbols-outlined text-cyan-400 mb-3">language</span>
            <h3 className="text-white font-bold mb-2">Multilingual</h3>
            <p className="text-xs text-slate-500 leading-relaxed">Supports German, English, French, and Spanish natively.</p>
          </div>
        </div>
      </section>

      <section id="privacy" className="mb-20 pt-16 border-t border-white/5">
        <h2 className="text-3xl font-bold text-white mb-6 font-display">Data Privacy</h2>
        <p className="text-slate-400 mb-6 leading-relaxed">
          Our generator operates on a "Zero-PII" principle. Compliant with GDPR, HIPAA, and industry-specific standards.
        </p>
      </section>

      <section id="generation" className="mb-20 pt-16 border-t border-white/5">
        <h2 className="text-3xl font-bold text-white mb-6 font-display">Generation Process</h2>
        <div className="space-y-6">
          {[
            { step: 1, title: "Taxonomy Ingestion", desc: "Load categories and priority levels." },
            { step: 2, title: "Semantic Sampling", desc: "Create diverse subject lines and bodies." },
            { step: 3, title: "Validation & Export", desc: "Validate against schema and export." }
          ].map((item, i) => (
            <div key={i} className="flex gap-6">
              <div className="flex-shrink-0 size-8 rounded-full bg-cyan-400/20 text-cyan-400 flex items-center justify-center font-bold text-xs">{item.step}</div>
              <div>
                <h4 className="text-white font-bold mb-1 text-sm">{item.title}</h4>
                <p className="text-xs text-slate-500">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section id="customization" className="mb-20 pt-16 border-t border-white/5">
        <h2 className="text-3xl font-bold text-white mb-6 font-display">Custom Schemas</h2>
        <div className="bg-[#0c0d15] rounded-xl p-6 border border-slate-800 shadow-2xl">
           <pre className="text-xs text-cyan-400 font-mono leading-relaxed overflow-x-auto cyber-scrollbar">
{`schema:
  fields:
    - name: "product_version"
      type: "enum"
      values: ["v2.1", "v2.4-beta", "v3.0"]
    - name: "sentiment"
      type: "weight"
      distribution: 
        frustrated: 0.2
        neutral: 0.7`}
           </pre>
        </div>
      </section>

      <section id="formats" className="mb-32 pt-16 border-t border-white/5">
        <h2 className="text-3xl font-bold text-white mb-6 font-display">Export Formats</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {['JSONL', 'CSV', 'XML', 'SQL'].map((fmt, i) => (
            <div key={i} className="p-4 rounded-xl bg-surface-dark border border-white/5 text-center">
              <span className="text-[10px] font-black text-slate-500 mb-2 block uppercase tracking-widest">Format</span>
              <span className="text-base font-bold text-white">{fmt}</span>
            </div>
          ))}
        </div>
      </section>
    </DocsLayout>
  );
};

export default SyntheticDataDocs;
