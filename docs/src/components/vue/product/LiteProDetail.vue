<template>
  <div class="min-h-screen bg-background-dark">
    <div class="mx-auto max-w-7xl px-6 lg:px-24 py-20">
      <nav class="mb-12 flex items-center gap-2 text-sm text-text-dim">
        <a href="/products" class="hover:text-primary transition-colors">PRODUCTS</a>
        <span>/</span>
        <span class="text-white">LITE PRO</span>
      </nav>

      <div class="flex flex-col lg:flex-row gap-16 mb-24">
        <div class="flex-1">
          <div class="mb-8 inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary/10 border border-primary/20">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
            </span>
            <span class="text-primary text-xs font-black uppercase tracking-widest">Production Ready (4B Parameters)</span>
          </div>

          <h1 class="text-5xl lg:text-7xl font-black text-white mb-6 leading-tight">
            Tagging AI<br />
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-cyan-glow">Lite Pro.</span>
          </h1>

          <p class="text-text-dim text-xl leading-relaxed mb-10">
            Our flagship medium-weight model. Precision-tuned for routing, SLA assignment, and management reporting with professional accuracy.
          </p>

          <div class="flex flex-wrap gap-4">
            <Button variant="primary" size="lg" class="uppercase tracking-widest">
              Buy License (2.500€)
            </Button>
            <Button variant="outline" size="lg">
              Calculate ROI
            </Button>
          </div>
        </div>

        <div class="flex-1">
          <div class="bg-surface-dark border border-surface-lighter rounded-3xl p-8 relative overflow-hidden">
            <div class="absolute -top-20 -right-20 w-64 h-64 bg-primary/10 blur-[80px]"></div>
            
            <h3 class="text-white text-lg font-bold mb-8 relative z-10">Enterprise Specifications</h3>
            
            <div class="space-y-6 relative z-10">
              <MetricBlock 
                label="MODEL COMPLEXITY"
                value="4.2B Parameters"
                sub="LARGE TRANSFORMER"
              />
              
              <MetricBlock 
                label="INFERENCE SPEED"
                value="< 150ms"
                sub="ON TESLA P100"
              />
              
              <MetricBlock 
                label="ACCURACY TARGET"
                value="~90.2%"
                sub="VERIFIED ON SME DATASETS"
              />
              
              <MetricBlock 
                label="MAINTENANCE"
                value="Included"
                sub="MONTHLY UPDATES"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-24">
        <div class="bg-surface-dark border border-surface-lighter rounded-2xl p-8 hover:border-primary/30 transition-all">
          <div class="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center mb-6">
            <ChartBarIcon class="w-6 h-6 text-primary" />
          </div>
          <h3 class="text-white text-xl font-bold mb-3">Management Reporting</h3>
          <p class="text-text-dim text-sm leading-relaxed">
            Hierarchical tags enable deep-dive analysis of root causes and help desk performance trends.
          </p>
        </div>

        <div class="bg-surface-dark border border-surface-lighter rounded-2xl p-8 hover:border-primary/30 transition-all">
          <div class="w-12 h-12 rounded-xl bg-cyan-glow/20 flex items-center justify-center mb-6">
            <BoltIcon class="w-6 h-6 text-cyan-glow" />
          </div>
          <h3 class="text-white text-xl font-bold mb-3">Intelligent Routing</h3>
          <p class="text-text-dim text-sm leading-relaxed">
            Instantly assign tickets to specialized teams based on fine-grained intent detection.
          </p>
        </div>

        <div class="bg-surface-dark border border-surface-lighter rounded-2xl p-8 hover:border-primary/30 transition-all">
          <div class="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center mb-6">
            <ShieldCheckIcon class="w-6 h-6 text-primary" />
          </div>
          <h3 class="text-white text-xl font-bold mb-3">Air-Gapped Privacy</h3>
          <p class="text-text-dim text-sm leading-relaxed">
            Designed for banking, healthcare and government use-cases. No cloud needed.
          </p>
        </div>
      </div>

      <div class="bg-surface-dark border border-surface-lighter rounded-3xl p-12 mb-24 relative overflow-hidden">
        <div class="absolute -bottom-20 -left-20 w-96 h-96 bg-cyan-glow/10 blur-[100px]"></div>
        
        <h2 class="text-4xl font-black text-white mb-12 text-center relative z-10">
          LITE VS PRO
        </h2>

        <div class="relative z-10">
          <div class="grid grid-cols-3 gap-6 mb-6 pb-6 border-b border-surface-lighter">
            <div class="text-text-dim text-sm font-bold uppercase tracking-wider"></div>
            <div class="text-center">
              <div class="text-white text-lg font-bold">Lite Free</div>
              <div class="text-text-dim text-xs mt-1">Evaluation</div>
            </div>
            <div class="text-center">
              <div class="text-primary text-lg font-bold">Lite Pro</div>
              <div class="text-primary-light text-xs mt-1">Production</div>
            </div>
          </div>

          <div class="space-y-3">
            <ComparisonRow 
              label="Model Size"
              free="0.5B Parameters"
              pro="4.2B Parameters"
            />
            <ComparisonRow 
              label="Tag Taxonomy"
              free="150+ Tags"
              pro="150+ Tags"
            />
            <ComparisonRow 
              label="Expected Accuracy"
              free="~82%"
              pro="~90%"
            />
            <ComparisonRow 
              label="Inference Speed"
              free="~300ms"
              pro="< 150ms"
            />
            <ComparisonRow 
              label="Hardware Requirements"
              free="8GB RAM, CPU-only"
              pro="16GB RAM, GPU recommended"
            />
            <ComparisonRow 
              label="Use Case"
              free="Testing & PoC"
              pro="Production routing & analytics"
            />
            <ComparisonRow 
              label="Support & Updates"
              free="Community"
              pro="Professional (Included)"
            />
            <ComparisonRow 
              label="Price"
              free="0€"
              pro="2,500€ (one-time)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ChartBarIcon, BoltIcon, ShieldCheckIcon } from '@heroicons/vue/24/outline';
import Button from '../core/basic/Button.vue';

const MetricBlock = defineComponent({
  props: {
    label: { type: String, required: true },
    value: { type: String, required: true },
    sub: { type: String, required: true }
  },
  template: `
    <div class="border-l-2 border-primary/30 pl-4">
      <div class="text-text-dim text-xs font-bold uppercase tracking-wider mb-1">{{ label }}</div>
      <div class="text-white text-2xl font-black mb-1">{{ value }}</div>
      <div class="text-primary-light text-xs uppercase tracking-wide">{{ sub }}</div>
    </div>
  `
});

const ComparisonRow = defineComponent({
  props: {
    label: { type: String, required: true },
    free: { type: String, required: true },
    pro: { type: String, required: true }
  },
  template: `
    <div class="grid grid-cols-3 gap-6 py-4 border-b border-surface-lighter/30 hover:bg-surface-lighter/20 transition-colors rounded-lg px-4">
      <div class="text-white font-medium text-sm">{{ label }}</div>
      <div class="text-text-dim text-sm text-center">{{ free }}</div>
      <div class="text-white text-sm text-center font-medium">{{ pro }}</div>
    </div>
  `
});
</script>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'LiteProDetail'
});
</script>
