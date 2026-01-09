
import React from 'react';
import { Link } from 'react-router-dom';
import DocsLayout from '../components/DocsLayout';

const OtaGettingStarted: React.FC = () => {
  const toc = [
    { label: "Prerequisites", id: "prerequisites" },
    { label: "1. Installation", id: "installation" },
    { label: "2. Configuration", id: "configuration" },
    { label: "3. Connector Setup", id: "connector-setup" },
    { label: "4. Your First Rule", id: "first-rule" },
    { label: "5. Verification", id: "verification" }
  ];

  const breadcrumbs = [
    { label: "Documentation", to: "/docs" },
    { label: "Open Ticket Automation", to: "/docs/ota" },
    { label: "Getting Started" }
  ];

  return (
    <DocsLayout toc={toc} breadcrumbs={breadcrumbs}>
      <header className="mb-16">
        <h1 className="text-5xl font-black text-white mb-6 font-display tracking-tight leading-tight">Getting Started with <span className="text-primary">OTA</span></h1>
        <p className="text-xl text-slate-400 leading-relaxed">
          This guide will walk you through deploying Open Ticket Automation (OTA) on your local infrastructure.
        </p>
      </header>

      <section id="prerequisites" className="mb-16">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
          <span className="material-symbols-outlined text-primary">inventory</span>
          Prerequisites
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { title: "Docker", desc: "Docker & Compose installed locally.", icon: "check_circle" },
            { title: "API Access", desc: "Admin API token for OTRS/Znuny.", icon: "check_circle" },
            { title: "AI Endpoint", desc: "Tagging AI URL accessible.", icon: "check_circle" }
          ].map((item, i) => (
            <div key={i} className="p-5 rounded-xl bg-surface-dark border border-white/5 text-center">
              <span className="material-symbols-outlined text-green-500 mb-2">{item.icon}</span>
              <h4 className="text-xs font-bold text-white mb-1">{item.title}</h4>
              <p className="text-[10px] text-slate-500">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="installation" className="mb-16 pt-8 border-t border-white/5">
        <div className="text-xs font-black text-primary uppercase tracking-[0.2em] mb-3">Step One</div>
        <h2 className="text-3xl font-bold text-white mb-6">Installation</h2>
        <div className="bg-black rounded-xl overflow-hidden border border-slate-800 shadow-2xl">
          <div className="flex items-center justify-between px-4 py-2 bg-slate-900 border-b border-slate-800">
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Terminal</span>
            <span className="material-symbols-outlined text-slate-600 text-sm cursor-pointer hover:text-white">content_copy</span>
          </div>
          <div className="p-6 font-mono text-[11px] leading-relaxed cyber-scrollbar overflow-x-auto">
            <div className="text-slate-500 italic mb-2"># Pull and run the container</div>
            <div className="text-white"><span className="text-primary">$</span> docker run -d \</div>
            <div className="text-white pl-6">--name ota-core \</div>
            <div className="text-white pl-6">-p 8080:8080 \</div>
            <div className="text-white pl-6">-v $(pwd)/config.yaml:/app/config.yaml \</div>
            <div className="text-white pl-6">ghcr.io/open-ticket-ai/ota:latest</div>
          </div>
        </div>
      </section>

      <section id="configuration" className="mb-16 pt-8 border-t border-white/5">
        <div className="text-xs font-black text-primary uppercase tracking-[0.2em] mb-3">Step Two</div>
        <h2 className="text-3xl font-bold text-white mb-6">Configuration</h2>
        <div className="bg-[#0f1117] rounded-xl overflow-hidden border border-slate-800 shadow-2xl">
          <div className="px-4 py-2 bg-slate-900 border-b border-slate-800 flex justify-between items-center">
            <span className="text-[10px] font-bold text-slate-500">config.yaml</span>
          </div>
          <div className="p-6 font-mono text-[11px] text-slate-300 leading-relaxed overflow-x-auto cyber-scrollbar">
{`server:
  port: 8080
  api_key: "your-internal-ota-secret"

ai_service:
  endpoint: "http://tagging-ai.local:5000/v1/tag"
  timeout_ms: 2000`}
          </div>
        </div>
      </section>

      <div className="mt-20 p-12 rounded-3xl bg-gradient-to-br from-primary/20 to-surface-dark border border-white/10 text-center">
        <h3 className="text-2xl font-bold text-white mb-4">Installation Complete</h3>
        <p className="text-slate-400 mb-8 max-w-md mx-auto text-sm">
          Ready to explore complex workflows and custom data mappings?
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link to="/docs/ota" className="h-12 px-8 rounded-lg bg-primary text-white font-bold flex items-center justify-center hover:bg-primary-dark transition-all text-sm">
            Configuration Reference
          </Link>
          <Link to="/services" className="h-12 px-8 rounded-lg border border-white/10 text-white font-bold flex items-center justify-center hover:bg-white/5 transition-all text-sm">
            Contact Support
          </Link>
        </div>
      </div>
    </DocsLayout>
  );
};

export default OtaGettingStarted;
