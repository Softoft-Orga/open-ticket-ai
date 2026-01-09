
import React from 'react';
import { CapabilityCard } from '../components/CommonElements';

const Home: React.FC = () => {
  return (
    <div className="w-full">
      {/* Hero Section */}
      <section className="relative w-full px-4 md:px-10 lg:px-20 xl:px-40 py-20 flex justify-center bg-glow-radial">
        <div className="w-full max-w-7xl flex flex-col lg:flex-row gap-16 items-center">
          <div className="flex flex-col gap-8 lg:w-1/2">
            <div className="flex items-center gap-2 w-fit px-3 py-1 rounded-full border border-primary/30 bg-primary/10 text-primary text-xs font-bold uppercase tracking-wider">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
              </span>
              Live Classification Engine v2.0
            </div>
            <h1 className="font-display text-5xl md:text-6xl lg:text-7xl font-bold leading-tight tracking-tight text-white">
              Automated, Consistent Ticket Classification <br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-cyan-400">In Real Time.</span>
            </h1>
            <p className="text-gray-400 text-xl leading-relaxed max-w-xl">
              Analyze incoming tickets and assign structured, hierarchical tags instantly. No rules to maintain. No manual effort. Fully automated.
            </p>
            <div className="flex flex-wrap gap-4 pt-4">
              <button className="h-14 px-10 rounded-lg bg-white text-background-dark text-lg font-bold hover:bg-gray-100 transition-colors">
                Start Free Trial
              </button>
              <button className="h-14 px-10 rounded-lg border border-border-dark hover:border-primary/50 text-white text-lg font-medium transition-colors bg-surface-dark/50">
                View Demo
              </button>
            </div>
          </div>

          {/* Hero Visual: Processor Mockup */}
          <div className="w-full lg:w-1/2 relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-primary to-cyan-500 rounded-xl blur opacity-20 group-hover:opacity-40 transition duration-1000"></div>
            <div className="relative w-full aspect-video bg-surface-dark border border-border-dark rounded-xl overflow-hidden shadow-2xl flex flex-col">
              <div className="h-10 bg-[#150c19] border-b border-border-dark flex items-center px-4 gap-2">
                <div className="flex gap-2">
                  <div className="size-3 rounded-full bg-red-500/50"></div>
                  <div className="size-3 rounded-full bg-yellow-500/50"></div>
                  <div className="size-3 rounded-full bg-green-500/50"></div>
                </div>
                <div className="ml-4 text-[11px] text-gray-500 font-mono tracking-wider">processor_v2.exe</div>
              </div>
              <div className="flex flex-1 overflow-hidden">
                <div className="w-1/2 border-r border-border-dark p-6 flex flex-col gap-4 bg-[#1a0f20]">
                  <div className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Raw Input</div>
                  <div className="flex flex-col gap-3 font-mono text-[13px] text-gray-400">
                    <div className="bg-white/5 p-3 rounded">
                      <span className="text-gray-500">Subject:</span> <span className="text-gray-300">Login failed again?</span>
                    </div>
                    <div className="bg-white/5 p-3 rounded flex-1">
                      <span className="text-gray-500">Body:</span><br/>
                      <span className="text-gray-300 leading-relaxed block mt-1">
                        Hi support, I'm trying to access the dashboard but getting error 503. This is blocking the payroll run. Please fix ASAP!
                      </span>
                    </div>
                  </div>
                </div>
                <div className="w-1/2 p-6 flex flex-col gap-4 bg-[#150c19]">
                  <div className="text-[10px] font-bold text-primary uppercase tracking-widest">AI Structured Output</div>
                  <div className="flex flex-col gap-4 font-mono text-[13px]">
                    <div className="flex flex-col gap-1.5">
                      <span className="text-gray-500 text-[11px]">Intent</span>
                      <span className="px-3 py-1.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30 w-fit">access_issue</span>
                    </div>
                    <div className="flex flex-col gap-1.5">
                      <span className="text-gray-500 text-[11px]">System</span>
                      <span className="px-3 py-1.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30 w-fit">dashboard_main</span>
                    </div>
                    <div className="flex flex-col gap-1.5">
                      <span className="text-gray-500 text-[11px]">Urgency</span>
                      <span className="px-3 py-1.5 rounded bg-red-500/20 text-red-300 border border-red-500/30 w-fit animate-pulse">critical</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Core Capabilities */}
      <section className="w-full px-4 md:px-10 lg:px-20 xl:px-40 py-24 bg-background-dark relative overflow-hidden">
        <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-primary/5 rounded-full blur-[120px] pointer-events-none"></div>
        <div className="w-full max-w-7xl mx-auto">
          <div className="mb-16">
            <h2 className="font-display text-4xl font-bold text-white mb-4">Core Capabilities</h2>
            <p className="text-gray-400 text-lg">Built for enterprise scale and precision.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <CapabilityCard 
              icon="psychology" 
              title="Fully Automated Classification" 
              desc="Assigns tags for Intent, Urgency, Impact, User Role, and Sentiment. Works seamlessly on new tickets and historical backlogs without human intervention."
            />
            <CapabilityCard 
              icon="account_tree" 
              title="Hierarchical, Not Flat" 
              desc="A real taxonomy tree. Parent nodes for high-level aggregation, leaf tags for operational precision. Enables deep, multi-level analytics."
            />
            <CapabilityCard 
              icon="hub" 
              title="10 Quadrillion Combinations" 
              desc="Map our fixed high-quality taxonomy to your custom fields. Over 10 quadrillion possible combinations to fit any specific workflow or industry."
            />
          </div>
        </div>
      </section>

      {/* Terminal Visual */}
      <section className="w-full px-4 md:px-10 lg:px-20 xl:px-40 py-24 bg-[#160b1b]">
        <div className="w-full max-w-7xl mx-auto flex flex-col lg:flex-row gap-16 items-center rounded-3xl bg-[#1d1023] border border-border-dark p-12 relative overflow-hidden shadow-2xl">
          <div className="absolute -right-20 -top-20 w-96 h-96 bg-cyan-500/10 rounded-full blur-[100px]"></div>
          
          <div className="w-full lg:w-3/5 order-2 lg:order-1">
            <div className="rounded-xl bg-[#0d0710] border border-[#3c2249] p-6 font-mono text-sm shadow-inner relative z-10">
              <div className="flex items-center justify-between mb-6 border-b border-[#3c2249] pb-3">
                <div className="text-gray-500 text-xs">bash</div>
                <div className="flex gap-1.5">
                  <div className="size-2 rounded-full bg-white/10"></div>
                </div>
              </div>
              <div className="flex flex-col gap-4">
                <div className="text-green-400 flex gap-2">
                  <span>$</span>
                  <span className="text-white">query analytics --group-by intent --metric resolution_time</span>
                </div>
                <div className="text-gray-500 italic text-xs">Processing 14,203 tickets...</div>
                <div className="flex flex-col gap-2 mt-2">
                  <div className="flex justify-between items-center bg-[#2b1834] p-3 rounded border-l-4 border-green-500">
                    <span className="text-blue-300">intent/service_request/access_request</span>
                    <span className="text-white font-bold">9 min <span className="text-gray-500 font-normal ml-1">avg</span></span>
                  </div>
                  <div className="flex justify-between items-center bg-[#2b1834] p-3 rounded border-l-4 border-red-500">
                    <span className="text-blue-300">intent/incident/security_incident</span>
                    <span className="text-white font-bold">3.1h <span className="text-gray-500 font-normal ml-1">avg</span></span>
                  </div>
                  <div className="flex justify-between items-center bg-[#2b1834] p-3 rounded border-l-4 border-yellow-500">
                    <span className="text-blue-300">intent/billing/dispute</span>
                    <span className="text-white font-bold">4.2d <span className="text-gray-500 font-normal ml-1">avg</span></span>
                  </div>
                </div>
                <div className="text-green-400 mt-4 flex gap-2">
                  <span>$</span>
                  <span className="animate-pulse bg-white w-2 h-5 inline-block"></span>
                </div>
              </div>
            </div>
          </div>

          <div className="w-full lg:w-2/5 flex flex-col gap-6 order-1 lg:order-2 z-10">
            <h2 className="font-display text-4xl font-bold text-white leading-tight">Actionable Reporting for Management.</h2>
            <p className="text-gray-400 text-xl leading-relaxed">
              See exactly where time and risk come from. Detect bottlenecks immediately with granular, AI-assigned tags that reveal the truth behind your support metrics.
            </p>
            <div className="flex items-center gap-2 text-primary font-bold text-lg cursor-pointer group hover:text-white transition-colors">
              <span>Explore Analytics Dashboard</span>
              <span className="material-symbols-outlined transition-transform group-hover:translate-x-1">arrow_forward</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
