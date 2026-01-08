<template>
  <nav class="sticky top-0 z-50 border-b border-slate-800 bg-slate-950/90 backdrop-blur text-slate-200">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 items-center justify-between">
        <!-- Brand / Logo -->
        <div class="flex items-center gap-3">
          <a :href="withLocale('/')" class="flex items-center gap-3 focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-400 rounded">
            <img 
              v-if="brand.logoSrc" 
              :alt="brand.name + ' logo'" 
              :src="brand.logoSrc"
              class="h-8 w-8 rounded-xl"
            />
            <div v-if="brand.showName !== false">
              <p class="font-semibold leading-tight text-slate-100">{{ brand.name }}</p>
              <p v-if="brand.tagline" class="text-xs text-slate-400 leading-tight">{{ brand.tagline }}</p>
            </div>
          </a>
        </div>

        <!-- Navigation Links -->
        <div v-if="navLinks.length > 0" class="hidden md:flex items-center gap-1">
          <a
            v-for="link in navLinks"
            :key="link.label"
            :href="withLocale(link.href)"
            :aria-label="link.label"
            class="px-3 py-2 text-sm text-slate-300 hover:text-slate-100 hover:bg-slate-900 rounded-lg transition focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-400"
          >
            {{ link.label }}
          </a>
        </div>

        <!-- CTA Button -->
        <div v-if="cta" class="flex items-center gap-2">
          <a
            :href="withLocale(cta.href)"
            :aria-label="cta.label"
            class="inline-flex items-center px-4 py-2 text-sm font-semibold rounded-lg bg-blue-500 text-white hover:bg-blue-600 transition focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-400"
          >
            {{ cta.label }}
          </a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script lang="ts" setup>
import {computed} from 'vue'
import {useI18n} from 'vue-i18n'

interface LinkItem {
  label: string
  href: string
}

interface Props {
  brand?: {
    name?: string
    tagline?: string
    logoSrc?: string | null
    showName?: boolean
  }
  links?: LinkItem[]
  cta?: LinkItem | null
}

const props = defineProps<Props>()

const {locale} = useI18n()
const langCode = computed(() => locale.value.split('-')[0])

const brand = computed(() => ({
  name: 'Open Ticket AI',
  tagline: null,
  logoSrc: null,
  showName: true,
  ...(props.brand ?? {})
}))

const defaultLinks: LinkItem[] = [
  {label: 'Documentation', href: '/docs/'},
  {label: 'Demo', href: '/demo/'},
  {label: 'Pricing', href: '/pricing/'},
  {label: 'About', href: '/about/'},
]

const navLinks = computed(() => props.links ?? defaultLinks)

const withLocale = (path: string) => `/${langCode.value}${path}`.replace('//', '/')
</script>
