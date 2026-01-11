<template>
  <footer class="border-t border-white/5 bg-background-dark py-24">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
        <div class="md:col-span-1">
          <div class="flex items-center gap-2 mb-6">
            <div class="flex size-8 items-center justify-center rounded bg-link/20 text-link">
              <TicketIcon class="w-5 h-5" />
            </div>
            <span class="font-display text-lg font-bold text-white tracking-tight">Open Ticket AI</span>
          </div>
          <p class="text-slate-500 text-sm leading-relaxed max-w-xs">
            Intelligent automation for OTRS, Znuny, and Zammad. German Engineering.
          </p>
        </div>
        
        <div
          v-for="(section, index) in sections"
          :key="index"
        >
          <h4 class="text-white font-bold text-sm mb-6 uppercase tracking-widest">
            {{ section.title }}
          </h4>
          <ul class="space-y-4 text-slate-500 text-sm">
            <li
              v-for="(link, linkIndex) in section.links"
              :key="linkIndex"
            >
              <a
                :href="link.url"
                class="text-primary hover:text-primary-light transition-colors"
              >{{ link.label }}</a>
            </li>
          </ul>
        </div>

        <div v-if="social.length > 0">
          <h4 class="text-white font-bold text-sm mb-6 uppercase tracking-widest">
            Connect
          </h4>
          <div class="flex gap-4 text-primary">
            <a
              v-for="(socialLink, index) in social"
              :key="index"
              :href="socialLink.url"
              :aria-label="socialLink.ariaLabel"
              class="hover:text-primary-light transition-colors"
            >
              <CodeBracketSquareIcon
                v-if="socialLink.platform === 'github'"
                class="w-6 h-6"
              />
              <LinkIcon
                v-else-if="socialLink.platform === 'linkedin'"
                class="w-6 h-6"
              />
            </a>
          </div>
        </div>
      </div>
      
      <div class="pt-8 border-t border-white/5 flex flex-col md:flex-row items-center justify-between gap-6">
        <div class="text-xs text-slate-600">
          © {{ year }} {{ copyright }}
        </div>
        <div
          v-if="legal.length > 0"
          class="flex gap-8 text-xs text-primary"
        >
          <a
            v-for="(legalLink, index) in legal"
            :key="index"
            :href="legalLink.url"
            class="hover:text-primary-light transition-colors"
          >{{ legalLink.label }}</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { TicketIcon, CodeBracketSquareIcon, LinkIcon } from '@heroicons/vue/24/outline'

type FooterLink = {
  label: string
  url: string
}

type FooterSection = {
  title: string
  links: FooterLink[]
}

type SocialLink = {
  platform: string
  url: string
  ariaLabel: string
}

type FooterData = {
  sections: FooterSection[]
  social: SocialLink[]
  legal: FooterLink[]
  copyright: string
}

type Props = {
  footerData?: FooterData
}

const props = defineProps<Props>()

const sections = computed(() => props.footerData?.sections || [])
const social = computed(() => props.footerData?.social || [])
const legal = computed(() => props.footerData?.legal || [])
const copyright = computed(() => props.footerData?.copyright || 'Open Ticket AI UG. All rights reserved.')
const year = computed(() => new Date().getFullYear())
</script>
