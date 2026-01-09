
import React from 'react';
import { PricingCard, IntegrationPackageCard, ExtensionItem } from '../components/ServiceElements';

const Services: React.FC = () => {
  return (
    <div className="min-h-screen bg-background-dark pb-32">
      {/* Hero */}
      <section className="relative pt-24 pb-20 text-center">
        <div className="mx-auto max-w-7xl px-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-xs font-bold text-primary mb-8">
            <span className="flex h-2 w-2 rounded-full bg-green-500"></span>
            German Engineering Precision
          </div>
          <h1 className="mx-auto max-w-4xl text-6xl font-black text-white sm:text-7xl lg:text-8xl tracking-tighter mb-8 leading-[0.9]">
            We Don't Just Build AI. <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-cyan-400">We Integrate It.</span>
          </h1>
          <p className="mx-auto max-w-2xl text-xl text-slate-400 leading-relaxed font-medium">
            Transparent, fixed-price packages for enterprise-grade helpdesk automation. 
            From self-hosted AI models to full workflow automation.
          </p>
        </div>
      </section>

      {/* Ticket Tagging AI Model Section */}
      <section className="max-w-7xl mx-auto px-6 mb-32">
        <div className="bg-[#120818] border border-white/5 rounded-3xl p-10 flex flex-col lg:flex-row gap-16">
          <div className="lg:w-2/3">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-lg bg-primary/10 text-primary">
                <span className="material-symbols-outlined text-3xl">hub</span>
              </div>
              <h2 className="text-3xl font-bold text-white">Ticket Tagging AI Model</h2>
            </div>
            <p className="text-slate-400 text-lg mb-10 max-w-2xl leading-relaxed">
              Our core AI model designed for the automatic classification and tagging of helpdesk tickets. 
              It processes incoming requests to instantly identify critical metadata before a human even sees the ticket.
            </p>
            <div className="grid grid-cols-2 gap-6">
              <div className="flex items-center gap-3 text-slate-300">
                <div className="size-2 rounded-full bg-primary"></div>
                <span className="font-bold">Category & Topic</span>
              </div>
              <div className="flex items-center gap-3 text-slate-300">
                <div className="size-2 rounded-full bg-primary"></div>
                <span className="font-bold">Intent Recognition</span>
              </div>
              <div className="flex items-center gap-3 text-slate-300">
                <div className="size-2 rounded-full bg-primary"></div>
                <span className="font-bold">Impact, Urgency & Priority</span>
              </div>
              <div className="flex items-center gap-3 text-slate-300">
                <div className="size-2 rounded-full bg-primary"></div>
                <span className="font-bold">Routing Hints</span>
              </div>
            </div>
          </div>
          <div className="lg:w-1/3 flex flex-col gap-4">
            <div className="text-slate-500 text-xs font-bold uppercase tracking-widest mb-2">Deployment & Integration</div>
            <div className="bg-[#1a101f] border border-white/5 rounded-xl p-4 flex gap-4 items-start">
              <span className="material-symbols-outlined text-primary">dns</span>
              <div>
                <h4 className="text-white text-sm font-bold">Self-Hosted</h4>
                <p className="text-slate-500 text-[11px] leading-tight">Full on-premise deployment. No data leaves your secure infrastructure.</p>
              </div>
            </div>
            <div className="bg-[#1a101f] border border-white/5 rounded-xl p-4 flex gap-4 items-start">
              <span className="material-symbols-outlined text-primary">sync_alt</span>
              <div>
                <h4 className="text-white text-sm font-bold">Auto Write-Back</h4>
                <p className="text-slate-500 text-[11px] leading-tight">Deep integration with ticket systems to automatically write back tags and fields.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Synthetic Data Generation */}
      <section className="max-w-7xl mx-auto px-6 mb-32">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full bg-cyan-400/10 border border-cyan-400/20 px-3 py-1 text-[10px] font-black uppercase text-cyan-400 mb-6">
            <span className="material-symbols-outlined text-xs">database</span>
            Data Generation
          </div>
          <h2 className="text-5xl font-black text-white mb-6 tracking-tight">Synthetic Data Generation</h2>
          <p className="text-slate-400 text-lg max-w-3xl mx-auto leading-relaxed">
            Custom, realistic, multilingual support-ticket datasets for AI training, evaluation, and benchmarking. 
            No sensitive customer data exposed.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
          <PricingCard 
            title="Evaluation Dataset"
            subtitle="Benchmarking & Testing"
            price="3.000 €"
            features={[
              "Up to 20,000 synthetic tickets",
              "Weighted multilingual generation",
              "Core ticket fields (subject, body, queue)",
              "Realistic distributions",
              "JSONL or CSV delivery"
            ]}
          />
          <PricingCard 
            title="Training Dataset"
            subtitle="High Volume Training"
            price="7.500 €"
            highlighted
            buttonText="Get Demo"
            features={[
              "50k–100k+ tickets",
              "Custom schema (queues, priorities, SLAs)",
              "Controlled label distributions",
              "Multilingual expansion",
              "Train / validation split, 1 revision round"
            ]}
          />
          <PricingCard 
            title="Enterprise Dataset"
            subtitle="Complex Use Cases"
            price="15.000 €"
            features={[
              "100k–500k+ tickets",
              "Strict balancing & constraints",
              "Realistic noise (typos, phrasing variance)",
              "Optional agent replies or conversations",
              "Train / dev / test splits & documentation"
            ]}
          />
        </div>

        {/* Common Extensions */}
        <div className="bg-[#0a060d] border border-white/5 rounded-2xl p-8">
          <div className="flex items-center gap-3 mb-8">
            <span className="material-symbols-outlined text-slate-500">inventory_2</span>
            <h3 className="text-slate-400 text-sm font-bold uppercase tracking-widest">Common Extensions <span className="text-slate-600 font-normal">(Add-ons)</span></h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
            <ExtensionItem icon="tune" title="Fine-tuned Model" desc="Deliver a tagging model specifically fine-tuned on the generated dataset." />
            <ExtensionItem icon="analytics" title="Evaluation Report" desc="Comprehensive metrics report on model performance using the dataset." />
            <ExtensionItem icon="integration_instructions" title="System Tuning" desc="Specific format tuning for import into OTOBO, Znuny, or Zammad systems." />
            <ExtensionItem icon="update" title="Ongoing Updates" desc="Periodic dataset refreshes to match evolving business logic." />
          </div>
        </div>
      </section>

      {/* Integration Services */}
      <section className="max-w-7xl mx-auto px-6 mb-32">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-black text-white mb-6">Integration Services</h2>
          <p className="text-slate-400 text-lg">Fixed-price packages to connect Open Ticket AI with your existing ecosystem.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <IntegrationPackageCard 
            title="Integration Package"
            subtitle="Standard Stack"
            price="2.000 €"
            systems="OTOBO, Znuny (OTRS stack), Zammad"
            buttonText="Contact Sales"
            features={[
              "Technical setup of Tagging AI service",
              "Connection to 1 ticket system instance",
              "Mapping tags to technical field logic",
              "One trigger setup (e.g. on creation)",
              "Basic testing + handover"
            ]}
          />
          <IntegrationPackageCard 
            title="Integration Package"
            subtitle="Enterprise / Custom"
            price="5.000 €"
            highlighted
            systems="Jira Service Management, Zendesk, Freshdesk, ServiceNow, Custom"
            buttonText="Get Demo"
            features={[
              "Everything in Standard Package",
              "Additional adapter work for non-standard APIs",
              "Extended testing for proprietary environments"
            ]}
          />
        </div>
        <div className="mt-8 text-center bg-red-500/5 border border-red-500/10 rounded-xl py-3">
          <p className="text-xs font-bold uppercase tracking-widest text-red-500/60">
            Out of Scope <span className="text-red-500">(Billed Hourly):</span> Multi-instance rollouts, complex field transformations, custom UI work, deep customization, and bespoke workflows.
          </p>
        </div>
      </section>

      {/* Automation Services (OTA) */}
      <section className="max-w-7xl mx-auto px-6 mb-32">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-5">
            <div className="inline-flex items-center gap-2 rounded-lg bg-purple-500/10 border border-purple-500/20 px-3 py-1 text-[10px] font-black uppercase text-purple-400 mb-6">
              <span className="material-symbols-outlined text-xs">auto_fix</span>
              Automation Engine
            </div>
            <h2 className="text-5xl font-black text-white mb-6">Automation Services</h2>
            <h3 className="text-xl font-bold text-slate-200 mb-6">Open Ticket Automation (OTA)</h3>
            <p className="text-slate-400 text-lg leading-relaxed mb-8">
              OTA is our open-source layer that translates AI tags into concrete actions. It bridges the gap between intelligence and resolution.
            </p>
            <ul className="space-y-4">
              {['Routing & Assignments', 'Priority & SLA Updates', 'Auto-replies & Notes', 'Triggering Tasks'].map((item, i) => (
                <li key={i} className="flex items-center gap-3 text-slate-300 font-bold">
                  <span className="material-symbols-outlined text-primary">arrow_forward</span>
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div className="lg:col-span-7">
            <div className="bg-[#1a101f] border border-primary/20 rounded-2xl p-8">
              <div className="flex justify-between items-start mb-10 pb-6 border-b border-white/5">
                <div>
                  <h4 className="text-white text-xl font-bold">OTA Automation Pack</h4>
                  <p className="text-slate-500 text-xs mt-1">Implementation of 3 core automations</p>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-white">3.000 €</div>
                  <div className="text-[10px] text-slate-500 uppercase">One-time</div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                <div>
                  <div className="text-[10px] text-white uppercase font-black mb-4">What's included</div>
                  <ul className="space-y-3">
                    {['Config of 3 automations based on your rules', 'Testing with real ticket examples', 'Handover documentation'].map((item, i) => (
                      <li key={i} className="flex items-start gap-2.5 text-xs text-slate-400">
                        <span className="material-symbols-outlined text-primary text-base">check</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="bg-black/20 rounded-xl p-6 border border-white/5">
                  <div className="text-[10px] text-white uppercase font-black mb-4">Need more?</div>
                  <p className="text-xs text-slate-400 mb-6">Additional rules after go-live.</p>
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-slate-300">Additional Automation</span>
                    <span className="font-bold text-white">500 € <span className="text-[10px] text-slate-500 font-normal">/each</span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Model Development */}
      <section className="max-w-7xl mx-auto px-6 mb-32">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full bg-purple-500/10 border border-purple-500/20 px-3 py-1 text-[10px] font-black uppercase text-purple-400 mb-6">
            <span className="material-symbols-outlined text-xs">psychology</span>
            Intelligence Layer
          </div>
          <h2 className="text-5xl font-black text-white mb-6">Model Development <span className="text-slate-500 font-medium">(Custom Tagging Models)</span></h2>
          <p className="text-slate-400 text-lg">Custom training and architecture for specialized tagging requirements.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
          <PricingCard 
            title="Custom Tags Model"
            subtitle="Synthetic Training Focus"
            price="20.000 €"
            priceSuffix="Base price"
            features={[
              "Custom tag definition (or yours + our additions)",
              "Trained primarily via our synthetic data generator",
              "Can be optionally hybridized with limited customer samples"
            ]}
          />
          <PricingCard 
            title="Custom Tag Model"
            subtitle="Start Data Training"
            price="30.000 €"
            highlighted
            buttonText="Get Demo"
            priceSuffix="Base price"
            features={[
              "Training primarily on your historical ticket data",
              "Requires 10k-50k+ labeled examples",
              "Includes comprehensive dataset preparation and evaluation"
            ]}
          />
          <div className="flex flex-col rounded-2xl p-8 bg-[#150c19] border border-white/5 hover:border-white/20 transition-all h-full">
            <div className="mb-6">
              <h4 className="text-white text-xl font-bold font-display">Custom Development</h4>
              <p className="text-primary text-xs font-bold uppercase mt-1">Special Requirements</p>
            </div>
            <div className="mb-8">
              <div className="text-3xl font-bold text-white font-display">On Request</div>
              <div className="text-[10px] text-slate-500 uppercase mt-1">Custom Quote</div>
            </div>
            <p className="text-sm text-slate-400 mb-10 flex-grow leading-relaxed">
              Anything beyond tag-model creation: special architectures, constraints, on-prem performance targets, multilingual requirements, advanced-evaluation, long-term training programs.
            </p>
            <button className="w-full rounded-lg py-3.5 text-sm font-bold border border-white/20 text-white hover:bg-white/5">
              Contact Sales
            </button>
          </div>
        </div>

        {/* Typical Scope */}
        <div className="bg-[#0a060d] border border-white/5 rounded-2xl p-8">
          <div className="flex items-center gap-3 mb-10">
            <span className="material-symbols-outlined text-slate-500">list_alt</span>
            <h3 className="text-slate-400 text-sm font-bold uppercase tracking-widest">Typical Scope <span className="text-slate-600 font-normal">(Included in fixed-price options)</span></h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
            <ExtensionItem icon="psychology" title="Tag Definition" desc="Taxonomy design, custom tag definitions, or mapping your structure with our standard ontology." />
            <ExtensionItem icon="hub" title="Dataset Strategy" desc="Balancing synthetic vs real data, handling multiple languages, and covering edge cases." />
            <ExtensionItem icon="verified" title="Training & Evaluation" desc="Full model training cycles with rigorous acceptance tests and performance validation." />
            <ExtensionItem icon="rocket_launch" title="Packaging & Deployment" desc="Guidance for self-hosted inference setup, containerization, and update strategies." />
          </div>
        </div>
      </section>

      {/* Hourly / Subscription */}
      <section className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-8 mb-32">
        <div className="rounded-3xl border border-white/10 bg-card-dark/50 p-10 flex flex-col hover:border-primary/40 transition-all">
          <div className="flex items-center gap-4 mb-6">
            <div className="p-3 rounded-2xl bg-blue-500/10 text-blue-400">
              <span className="material-symbols-outlined text-3xl">schedule</span>
            </div>
            <h3 className="text-2xl font-bold text-white">Hourly Services</h3>
          </div>
          <p className="text-slate-400 text-lg mb-10 flex-grow">
            For extra changes beyond package-scope, custom features/workflows, troubleshooting, performance tuning, additional systems, or migrations.
          </p>
          <div className="border-t border-white/5 pt-8 flex justify-between items-center">
            <span className="text-slate-400 font-medium">Remote Rate</span>
            <span className="text-3xl font-bold text-white">200 € <span className="text-base font-normal text-slate-500">/hour</span></span>
          </div>
        </div>
        
        <div className="rounded-3xl border border-white/10 bg-card-dark/50 p-10 flex flex-col hover:border-green-500/40 transition-all">
          <div className="flex items-center gap-4 mb-6">
            <div className="p-3 rounded-2xl bg-green-500/10 text-green-400">
              <span className="material-symbols-outlined text-3xl">support_agent</span>
            </div>
            <h3 className="text-2xl font-bold text-white">Ongoing Support</h3>
          </div>
          <p className="text-slate-400 text-lg mb-4 flex-grow">
            Best-effort subscription for reliable coverage. Includes async support via ticket/email, minor fixes, maintenance help, and updates.
          </p>
          <div className="flex flex-col gap-2 mb-10">
            <div className="flex items-center gap-2 text-xs text-green-400 font-bold">
              <span className="material-symbols-outlined text-sm">check_circle</span>
              Target response within 2 business days
            </div>
            <p className="text-[10px] text-slate-500 italic">* Unused hours/time will not carry over. Available for integration/OSS customers.</p>
          </div>
          <div className="border-t border-white/5 pt-8 flex justify-between items-center">
            <span className="text-slate-400 font-medium">Subscription</span>
            <span className="text-3xl font-bold text-white">400 € <span className="text-base font-normal text-slate-500">/month</span></span>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-6">
        <div className="bg-gradient-to-r from-[#1a1033] to-[#0f0814] border border-white/10 rounded-3xl p-20 text-center relative overflow-hidden">
          <div className="absolute inset-0 bg-glow-radial opacity-30"></div>
          <div className="relative z-10">
            <h2 className="text-5xl font-black text-white mb-6">Ready to automate your helpdesk?</h2>
            <p className="text-xl text-slate-400 mb-12 max-w-2xl mx-auto">
              Schedule a technical consultation with our German engineering team to discuss your specific infrastructure needs.
            </p>
            <div className="flex flex-wrap justify-center gap-6">
              <button className="h-14 px-10 rounded-lg bg-cyan-400 text-background-dark font-black text-lg hover:bg-cyan-300 transition-colors shadow-xl shadow-cyan-400/20">
                Get Demo
              </button>
              <button className="h-14 px-10 rounded-lg border border-white/20 text-white font-bold text-lg hover:bg-white/5 transition-colors flex items-center gap-2">
                Contact Sales <span className="material-symbols-outlined">arrow_forward</span>
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Services;
