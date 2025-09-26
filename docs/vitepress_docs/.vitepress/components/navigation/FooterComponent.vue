<template>
  <footer class="border-t border-slate-800 bg-slate-950/80 backdrop-blur text-slate-200">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <!-- Top: brand + social -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-6 pb-10 border-b border-slate-800/70">
        <div class="flex items-center gap-3">
          <img v-if="brand.logoSrc" :src="brand.logoSrc" :alt="brand.name + ' logo'" class="h-8 w-8 rounded-xl" />
          <div>
            <p class="font-semibold leading-tight text-slate-100">{{ brand.name }}</p>
            <p class="text-sm text-slate-400 leading-tight">{{ brand.tagline }}</p>
          </div>
        </div>

        <nav aria-label="Social" class="flex items-center gap-2">
          <a
            v-for="s in social"
            :key="s.label"
            :href="s.href"
            class="inline-flex items-center justify-center rounded-xl p-2 hover:bg-slate-900 focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-400"
            target="_blank"
            rel="noopener noreferrer"
            :aria-label="s.label"
          >
            <component :is="s.icon" class="h-5 w-5 text-slate-300" />
          </a>
        </nav>
      </div>

      <!-- Links -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 py-10">
        <Section v-for="group in linkGroups" :key="group.title" :title="group.title">
          <ul class="mt-3 space-y-2">
            <li v-for="item in group.items" :key="item.label">
              <a
                :href="withLocale(item.href)"
                class="text-sm text-slate-400 hover:text-slate-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-400 rounded"
                :aria-label="item.label"
              >
                {{ item.label }}
              </a>
            </li>
          </ul>
        </Section>
      </div>

      <!-- Bottom: legal row -->
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-t border-slate-800/70 pt-6">
        <p class="text-xs text-slate-400">© {{ year }} {{ brand.name }} · {{ brand.footerNote }}</p>
        <div class="flex flex-wrap gap-x-4 gap-y-2 text-xs text-slate-400">
          <a v-for="l in legalLinks" :key="l.label" :href="withLocale(l.href)" class="hover:text-slate-200">{{ l.label }}</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed, defineComponent } from 'vue'
import { useI18n } from 'vue-i18n'
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
import { MarkGithubIcon } from '@heroicons/vue/24/outline'
import { AcademicCapIcon } from '@heroicons/vue/24/outline'
import { LinkIcon } from '@heroicons/vue/24/outline'

interface LinkItem { label: string; href: string }
interface LinkGroup { title: string; items: LinkItem[] }

const props = defineProps<{ brand?: { name?: string; tagline?: string; logoSrc?: string | null; footerNote?: string }; links?: { product?: LinkItem[]; solutions?: LinkItem[]; company?: LinkItem[]; resources?: LinkItem[]; legal?: LinkItem[] }; social?: { label: string; href: string; icon?: any }[] }>()

const { locale } = useI18n()
const year = new Date().getFullYear()
const langCode = computed(() => locale.value.split('-')[0])

const brand = computed(() => ({ name: 'Open Ticket AI', tagline: 'AI Ticket Classification · Open Source', logoSrc: null, footerNote: 'Built with ❤️ and Open Source', ...(props.brand ?? {}) }))

const defaultLinks = computed(() => ({
  product: [
    { label: 'Documentation', href: '/docs/' },
    { label: 'Getting Started', href: '/getting-started/' },
    { label: 'Live Demo', href: '/demo/' },
    { label: 'Pricing', href: '/pricing/' },
  ],
  solutions: [
    { label: 'OTOBO / Znuny / OTRS', href: '/solutions/otobo-znuny-otrs/' },
    { label: 'Model Fine‑Tuning', href: '/services/fine-tuning/' },
    { label: 'Synthetic Data', href: '/services/synthetic-data/' },
    { label: 'Installation & Setup', href: '/services/installation/' },
  ],
  company: [
    { label: 'About', href: '/about/' },
    { label: 'Blog', href: '/blog/' },
    { label: 'Contact', href: '/contact/' },
  ],
  resources: [
    { label: 'API', href: '/api/' },
    { label: 'Ticket Dataset', href: '/dataset/' },
    { label: 'Guides', href: '/guides/' },
  ],
  legal: [
    { label: 'Imprint', href: '/imprint/' },
    { label: 'Privacy', href: '/privacy/' },
    { label: 'Cookie Policy', href: '/cookies/' },
  ],
}))

const linkGroups = computed<LinkGroup[]>(() => [
  { title: 'Product', items: props.links?.product ?? defaultLinks.value.product },
  { title: 'Solutions', items: props.links?.solutions ?? defaultLinks.value.solutions },
  { title: 'Company', items: props.links?.company ?? defaultLinks.value.company },
  { title: 'Resources', items: props.links?.resources ?? defaultLinks.value.resources },
])

const legalLinks = computed(() => props.links?.legal ?? defaultLinks.value.legal)

const withLocale = (path: string) => `/${langCode.value}${path}`.replace('//', '/')

const social = computed(() => (props.social ?? [
  { label: 'GitHub', href: 'https://github.com/openticketai', icon: MarkGithubIcon },
  { label: 'Hugging Face', href: 'https://huggingface.co/openticketai', icon: AcademicCapIcon },
  { label: 'LinkedIn', href: 'https://www.linkedin.com/company/open-ticket-ai', icon: LinkIcon },
]).filter(s => !/instagram/i.test(s.label)))

const Section = defineComponent<{ title: string }>({
  name: 'FooterSection',
  props: { title: { type: String, required: true } },
  setup(p, { slots }) {
    return () => (
      <Disclosure as="section" class="sm:contents">
        {() => (
          <>
            <div class="sm:hidden">
              <DisclosureButton class="w-full flex items-center justify-between rounded-xl bg-slate-900/70 px-4 py-3 text-left font-medium text-slate-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-400">
                <span>{p.title}</span>
                <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M10 3a1 1 0 0 1 1 1v5h5a1 1 0 1 1 0 2h-5v5a1 1 0 1 1-2 0v-5H4a1 1 0 0 1 0-2h5V4a1 1 0 0 1 1-1Z" clip-rule="evenodd"/></svg>
              </DisclosureButton>
              <DisclosurePanel class="px-4 pt-1 pb-4">
                {slots.default?.()}
              </DisclosurePanel>
            </div>
            <div class="hidden sm:block">
              <h3 class="text-sm font-semibold text-slate-200">{p.title}</h3>
              {slots.default?.()}
            </div>
          </>
        )}
      </Disclosure>
    )
  },
})
</script>
