<template>
  <footer class="border-t border-white/5 bg-background-dark py-24">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
        <div class="md:col-span-1">
          <div class="flex items-center gap-2 mb-6">
            <div class="flex size-8 items-center justify-center rounded bg-primary/20 text-primary">
              <TicketIcon class="w-5 h-5" />
            </div>
            <span class="font-display text-lg font-bold text-white tracking-tight">Open Ticket AI</span>
          </div>
          <p class="text-slate-500 text-sm leading-relaxed max-w-xs">
            Intelligent automation for OTRS, Znuny, and Zammad. German Engineering.
          </p>
        </div>
        
        <div>
          <h4 class="text-white font-bold text-sm mb-6 uppercase tracking-widest">Product</h4>
          <ul class="space-y-4 text-slate-500 text-sm">
            <li><a href="/products" class="hover:text-primary transition-colors">Features</a></li>
            <li><a href="/services" class="hover:text-primary transition-colors">Integrations</a></li>
            <li><a href="/docs" class="hover:text-primary transition-colors">Security</a></li>
          </ul>
        </div>

        <div>
          <h4 class="text-white font-bold text-sm mb-6 uppercase tracking-widest">Company</h4>
          <ul class="space-y-4 text-slate-500 text-sm">
            <li><a href="#" class="hover:text-primary transition-colors">About Us</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Careers</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Legal</a></li>
          </ul>
        </div>

        <div>
          <h4 class="text-white font-bold text-sm mb-6 uppercase tracking-widest">Connect</h4>
          <div class="flex gap-4 text-slate-500">
            <a href="https://github.com/openticketai" class="hover:text-primary transition-colors" aria-label="GitHub">
              <CodeBracketSquareIcon class="w-6 h-6" />
            </a>
            <a href="https://www.linkedin.com/company/open-ticket-ai" class="hover:text-primary transition-colors" aria-label="LinkedIn">
              <LinkIcon class="w-6 h-6" />
            </a>
          </div>
        </div>
      </div>
      
      <div class="pt-8 border-t border-white/5 flex flex-col md:flex-row items-center justify-between gap-6">
        <div class="text-xs text-slate-600">
          © {{ year }} Open Ticket AI GmbH. All rights reserved.
        </div>
        <div class="flex gap-8 text-xs text-slate-600">
          <a class="hover:text-white transition-colors" href="#">Privacy Policy</a>
          <a class="hover:text-white transition-colors" href="#">Imprint</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { TicketIcon, CodeBracketSquareIcon, LinkIcon } from '@heroicons/vue/24/outline'

const year = computed(() => new Date().getFullYear())
</script>
