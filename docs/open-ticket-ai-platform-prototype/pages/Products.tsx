
import React from 'react';

const Products: React.FC = () => {
  return (
    <div className="min-h-screen bg-background-dark font-body">
      {/* Hero Section */}
      <section className="relative px-6 lg:px-24 py-20 lg:py-32 overflow-hidden">
        <div className="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-16">
          <div className="flex-1 space-y-8">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-[10px] font-black uppercase tracking-widest">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
              </span>
              Live Classification Engine v2.0
            </div>
            <h1 className="text-5xl lg:text-7xl font-black text-white leading-[0.9] font-display tracking-tighter">
              Automated, <br />
              Consistent Ticket <br />
              Classification <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-cyan-400">In Real Time.</span>
            </h1>
            <p className="text-slate-400 text-lg lg:text-xl max-w-xl leading-relaxed">
              Analyze incoming tickets and assign structured, hierarchical tags instantly. No rules to maintain. No manual effort. Fully automated.
            </p>
            <div className="flex flex-wrap gap-4">
              <button className="px-8 h-12 bg-white text-black font-bold rounded-md hover:bg-slate-200 transition-colors">
                Start Free Trial
              </button>
              <button className="px-8 h-12 bg-transparent border border-white/20 text-white font-bold rounded-md hover:bg-white/5 transition-colors">
                View Demo
              </button>
            </div>
          </div>

          {/* Processor Mockup */}
          <div className="flex-1 w-full relative">
            <div className="absolute -inset-4 bg-primary/20 blur-3xl rounded-full opacity-30"></div>
            <div className="relative bg-[#1d1023] border border-white/5 rounded-xl shadow-2xl overflow-hidden flex flex-col h-[400px]">
              <div className="h-10 bg-[#0f0814] flex items-center px-4 gap-1.5 border-b border-white/5">
                <div className="flex gap-1.5">
                  <div className="size-2.5 rounded-full bg-red-500/50"></div>
                  <div className="size-2.5 rounded-full bg-yellow-500/50"></div>
                  <div className="size-2.5 rounded-full bg-green-500/50"></div>
                </div>
                <div className="ml-4 text-[10px] text-slate-500 font-mono italic">processor_v2.exe</div>
              </div>
              <div className="flex flex-1">
                <div className="w-1/2 p-6 bg-[#1a0f20] border-r border-white/5 flex flex-col gap-4">
                  <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Raw Input</div>
                  <div className="space-y-4 font-mono text-[11px]">
                    <div className="bg-black/20 p-3 rounded text-slate-400">
                      <span className="text-slate-600">Subject:</span> Login failed again?
                    </div>
                    <div className="bg-black/20 p-3 rounded text-slate-400 h-32">
                      <span className="text-slate-600">Body:</span><br />
                      Hi support, I'm trying to access the dashboard but getting error 503. This is blocking the payroll run. Please fix
                    </div>
                  </div>
                </div>
                <div className="w-1/2 p-6 bg-[#0f0814] flex flex-col gap-4">
                  <div className="text-[10px] font-black text-primary uppercase tracking-widest">AI Structured Output</div>
                  <div className="space-y-6 font-mono text-[11px]">
                    <div>
                      <div className="text-slate-600 mb-1.5 uppercase text-[9px]">Intent</div>
                      <span className="px-3 py-1 bg-blue-500/20 text-blue-300 border border-blue-500/20 rounded">access_issue</span>
                    </div>
                    <div>
                      <div className="text-slate-600 mb-1.5 uppercase text-[9px]">System</div>
                      <span className="px-3 py-1 bg-purple-500/20 text-purple-300 border border-purple-500/20 rounded">dashboard_main</span>
                    </div>
                    <div>
                      <div className="text-slate-600 mb-1.5 uppercase text-[9px]">Urgency</div>
                      <span className="px-3 py-1 bg-red-500/20 text-red-300 border border-red-500/20 rounded">critical</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Core Capabilities */}
      <section className="px-6 lg:px-24 py-24 bg-background-dark">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-white mb-2 font-display">Core Capabilities</h2>
          <p className="text-slate-500 text-sm mb-12">Built for enterprise scale and precision.</p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-8 bg-[#1d1023]/40 border border-white/5 rounded-xl hover:border-primary/30 transition-all">
              <span className="material-symbols-outlined text-primary text-3xl mb-6">psychology</span>
              <h3 className="text-xl font-bold text-white mb-4">Fully Automated Classification</h3>
              <p className="text-slate-400 text-sm leading-relaxed">Assigns tags for Intent, Urgency, Impact, User Role, and Sentiment. Works seamlessly on new tickets and historical backlogs without human intervention.</p>
            </div>
            <div className="p-8 bg-[#1d1023]/40 border border-white/5 rounded-xl hover:border-primary/30 transition-all">
              <span className="material-symbols-outlined text-primary text-3xl mb-6">account_tree</span>
              <h3 className="text-xl font-bold text-white mb-4">Hierarchical, Not Flat</h3>
              <p className="text-slate-400 text-sm leading-relaxed">A real taxonomy tree. Parent nodes for high-level aggregation, leaf tags for operational precision. Enables deep, multi-level analytics.</p>
            </div>
            <div className="p-8 bg-[#1d1023]/40 border border-white/5 rounded-xl hover:border-primary/30 transition-all">
              <span className="material-symbols-outlined text-primary text-3xl mb-6">hub</span>
              <h3 className="text-xl font-bold text-white mb-4">10 Quadrillion Combinations</h3>
              <p className="text-slate-400 text-sm leading-relaxed">Map our fixed high-quality taxonomy to your custom fields. Over 10 quadrillion possible combinations to fit any specific workflow or industry.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Actionable Reporting */}
      <section className="px-6 lg:px-24 py-24 bg-background-dark">
        <div className="max-w-7xl mx-auto flex flex-col lg:flex-row gap-16 items-center bg-[#1d1023]/50 border border-white/5 rounded-3xl p-12 overflow-hidden relative">
          <div className="absolute right-0 top-0 w-96 h-96 bg-primary/10 blur-[100px] pointer-events-none"></div>
          
          {/* Analytics Terminal */}
          <div className="flex-1 w-full">
            <div className="bg-[#0f0814] border border-white/10 rounded-xl overflow-hidden shadow-2xl">
              <div className="bg-[#1a0f20] px-4 py-2 flex items-center justify-between border-b border-white/5">
                <span className="text-[10px] font-mono text-slate-500">bash</span>
                <div className="size-2 rounded-full bg-white/10"></div>
              </div>
              <div className="p-6 font-mono text-[12px] space-y-4">
                <div className="flex gap-2">
                  <span className="text-green-400">$</span>
                  <span className="text-white">query analytics --group-by intent --metric resolution_time</span>
                </div>
                <div className="text-slate-600 italic text-[11px]">Processing 14,203 tickets...</div>
                <div className="space-y-2">
                  <div className="flex justify-between items-center bg-[#2d1b36] p-3 rounded-lg border-l-2 border-purple-500">
                    <span className="text-primary-light">intent/service_request/access_request</span>
                    <span className="text-white font-bold">9 min <span className="text-slate-500 font-normal">avg</span></span>
                  </div>
                  <div className="flex justify-between items-center bg-[#2d1b36] p-3 rounded-lg border-l-2 border-pink-500">
                    <span className="text-primary-light">intent/incident/security_incident</span>
                    <span className="text-white font-bold">3.1h <span className="text-slate-500 font-normal">avg</span></span>
                  </div>
                  <div className="flex justify-between items-center bg-[#2d1b36] p-3 rounded-lg border-l-2 border-primary">
                    <span className="text-primary-light">intent/billing/dispute</span>
                    <span className="text-white font-bold">4.2d <span className="text-slate-500 font-normal">avg</span></span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <span className="text-green-400">$</span>
                  <span className="w-2 h-4 bg-white animate-pulse"></span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex-1 space-y-6 relative z-10">
            <h2 className="text-4xl font-bold text-white font-display leading-tight">Actionable Reporting for Management.</h2>
            <p className="text-slate-400 text-lg leading-relaxed">
              See exactly where time and risk come from. Detect bottlenecks immediately with granular, AI-assigned tags that reveal the truth behind your support metrics.
            </p>
            <a href="#" className="inline-flex items-center gap-2 text-primary font-bold hover:text-primary-light transition-colors group">
              Explore Analytics Dashboard
              <span className="material-symbols-outlined transition-transform group-hover:translate-x-1">arrow_forward</span>
            </a>
          </div>
        </div>
      </section>

      {/* Flexible Editions */}
      <section className="px-6 lg:px-24 py-24 bg-background-dark">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4 font-display">Flexible Editions</h2>
            <p className="text-slate-500 text-sm">Choose the model complexity that fits your operational needs.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-stretch">
            {/* Lite Free */}
            <div className="flex flex-col bg-[#1d1023]/40 border border-white/5 rounded-2xl p-10 hover:border-white/20 transition-all">
              <div className="mb-8">
                <h3 className="text-xl font-bold text-white">Lite Free</h3>
                <p className="text-slate-500 text-xs mt-1">Evaluation & Testing</p>
              </div>
              <div className="mb-8">
                <span className="text-4xl font-black text-white">0 €</span>
                <span className="text-slate-600 text-sm ml-2">/ one-time</span>
              </div>
              <ul className="space-y-4 mb-12 flex-grow">
                {[
                  "Model: 0.5B Parameters",
                  "150+ Tags",
                  "Accuracy: ~0.82",
                  "ROI from 15 tickets/day"
                ].map((f, i) => (
                  <li key={i} className="flex items-center gap-3 text-xs text-slate-300">
                    <span className="material-symbols-outlined text-green-500 text-sm">check_circle</span>
                    {f}
                  </li>
                ))}
              </ul>
              <div className="text-[10px] text-slate-600 text-center mb-4 italic">Available 16.01</div>
              <button className="w-full py-3 bg-white/5 border border-white/10 rounded-lg text-white font-bold text-sm hover:bg-white/10 transition-colors">
                Download Lite
              </button>
            </div>

            {/* Lite Pro */}
            <div className="flex flex-col bg-[#2d1b36] border-2 border-primary rounded-2xl p-10 shadow-[0_0_40px_rgba(166,13,242,0.2)] relative scale-105 z-10">
              <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-primary text-white text-[10px] font-black uppercase tracking-widest px-4 py-1.5 rounded-full">Best Value</div>
              <div className="mb-8">
                <h3 className="text-xl font-bold text-white">Lite Pro</h3>
                <p className="text-primary-light text-xs mt-1 font-medium">Production Ready</p>
              </div>
              <div className="mb-8">
                <span className="text-4xl font-black text-white">2,500 €</span>
                <span className="text-slate-500 text-sm ml-2">/ one-time</span>
              </div>
              <ul className="space-y-4 mb-12 flex-grow">
                {[
                  "Model: 4B Parameters",
                  "150+ Tags",
                  "Accuracy: ~0.90",
                  "Focus: Routing & Reporting"
                ].map((f, i) => (
                  <li key={i} className="flex items-center gap-3 text-xs text-slate-200">
                    <span className="material-symbols-outlined text-primary-light text-sm">check_circle</span>
                    {f}
                  </li>
                ))}
              </ul>
              <div className="text-[10px] text-slate-400 text-center mb-4 italic">Available 16.01</div>
              <button className="w-full py-4 bg-primary text-white rounded-lg font-black text-sm hover:bg-primary-dark transition-all shadow-glow">
                Pre-order Lite Pro
              </button>
            </div>

            {/* Full Pro */}
            <div className="flex flex-col bg-[#1d1023]/40 border border-white/5 rounded-2xl p-10 hover:border-white/20 transition-all opacity-80">
              <div className="mb-8">
                <h3 className="text-xl font-bold text-white">Full Pro</h3>
                <p className="text-slate-500 text-xs mt-1">Advanced Enterprise</p>
              </div>
              <div className="mb-8">
                <span className="text-4xl font-black text-white">6,000 €</span>
                <span className="text-slate-600 text-sm ml-2">/ one-time</span>
              </div>
              <ul className="space-y-4 mb-12 flex-grow">
                {[
                  "Model: 8B Parameters",
                  "250+ Tags",
                  "Accuracy: ~0.92",
                  "Focus: Maximum Detail"
                ].map((f, i) => (
                  <li key={i} className="flex items-center gap-3 text-xs text-slate-300">
                    <span className="material-symbols-outlined text-green-500 text-sm">check_circle</span>
                    {f}
                  </li>
                ))}
              </ul>
              <div className="text-[10px] text-slate-600 text-center mb-4 italic uppercase font-black">In Development</div>
              <button className="w-full py-3 bg-white/5 border border-white/10 rounded-lg text-slate-500 font-bold text-sm cursor-not-allowed">
                Coming Soon
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Deployment Flexibility */}
      <section className="px-6 lg:px-24 py-24 bg-[#0a060d]">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-12">
          <div className="flex-1">
            <h2 className="text-3xl font-bold text-white mb-4 font-display">Deployment & Hardware Flexibility</h2>
            <p className="text-slate-500">Secure by design. Optimized for your infrastructure.</p>
          </div>
          <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 gap-8">
            <div className="flex items-center gap-4">
              <div className="p-2 bg-primary/10 rounded-lg">
                <span className="material-symbols-outlined text-primary">dns</span>
              </div>
              <span className="text-xs font-bold text-slate-300 uppercase tracking-widest">On-Premise or Private Cloud</span>
            </div>
            <div className="flex items-center gap-4">
              <div className="p-2 bg-primary/10 rounded-lg">
                <span className="material-symbols-outlined text-primary">shield_lock</span>
              </div>
              <span className="text-xs font-bold text-slate-300 uppercase tracking-widest">No data leaves infrastructure</span>
            </div>
            <div className="flex items-center gap-4">
              <div className="p-2 bg-primary/10 rounded-lg">
                <span className="material-symbols-outlined text-primary">memory</span>
              </div>
              <span className="text-xs font-bold text-slate-300 uppercase tracking-widest">IMT8, BF16, FP16 quantizations</span>
            </div>
            <div className="flex items-center gap-4">
              <div className="p-2 bg-primary/10 rounded-lg">
                <span className="material-symbols-outlined text-primary">settings_suggest</span>
              </div>
              <span className="text-xs font-bold text-slate-300 uppercase tracking-widest">Optimized for CPU & GPU</span>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="px-6 lg:px-24 py-32 bg-background-dark">
        <div className="max-w-4xl mx-auto text-center space-y-12">
          <div className="flex justify-center">
            <div className="size-20 bg-primary rounded-3xl flex items-center justify-center shadow-[0_0_50px_rgba(166,13,242,0.4)] animate-bounce-slow">
              <span className="material-symbols-outlined text-white text-5xl">rocket_launch</span>
            </div>
          </div>
          <h2 className="text-5xl lg:text-6xl font-black text-white leading-tight font-display tracking-tight">
            Turn Raw Tickets into <br />
            Operational Intelligence.
          </h2>
          <p className="text-slate-500 text-lg lg:text-xl font-medium">
            Join forward-thinking support teams automating their workflow today.
          </p>
          <div className="flex flex-wrap justify-center gap-6 pt-4">
            <button className="h-14 px-10 bg-primary text-white font-black uppercase tracking-widest rounded-xl hover:bg-primary-dark transition-all shadow-glow">
              Get Lite Free Version
            </button>
            <button className="h-14 px-10 bg-[#1d1023] border border-white/10 text-white font-bold rounded-xl hover:bg-white/5 transition-all">
              View Architecture
            </button>
          </div>
        </div>
      </section>

      {/* Mini Footer */}
      <footer className="px-6 lg:px-24 py-12 border-t border-white/5 bg-background-dark">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-xl">confirmation_number</span>
            <span className="font-bold text-white text-sm">Open Ticket AI</span>
          </div>
          <div className="text-[10px] text-slate-700 font-medium uppercase tracking-widest">
            © 2024 Open Ticket AI GmbH. German Engineering.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Products;
