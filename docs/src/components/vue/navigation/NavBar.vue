<template>
  <nav class="border-b border-slate-800 bg-slate-950/80 backdrop-blur text-slate-200 sticky top-0 z-50">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 items-center justify-between">
        <!-- Brand/Logo -->
        <div class="flex items-center gap-3">
          <a 
            :href="withLocale(brand.href || '/')" 
            class="flex items-center gap-3 hover:opacity-80 transition-opacity"
          >
            <img 
              v-if="brand.logoSrc" 
              :alt="brand.name + ' logo'" 
              :src="brand.logoSrc"
              class="h-8 w-8 rounded-xl"
            />
            <span class="font-semibold text-lg text-slate-100">{{ brand.name }}</span>
          </a>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex md:items-center md:gap-8">
          <nav v-if="navLinks.length > 0" aria-label="Main navigation" class="flex items-center gap-6">
            <a
              v-for="link in navLinks"
              :key="link.label"
              :href="withLocale(link.href)"
              class="text-sm text-slate-300 hover:text-slate-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-400 rounded px-1 transition-colors"
            >
              {{ link.label }}
            </a>
          </nav>

          <!-- CTA Button -->
          <a
            v-if="ctaButton"
            :href="withLocale(ctaButton.href)"
            class="inline-flex items-center px-4 py-2 bg-blue-500 text-white font-semibold rounded hover:bg-blue-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-400 transition-colors"
          >
            {{ ctaButton.label }}
          </a>
        </div>

        <!-- Mobile Menu Button -->
        <button
          class="md:hidden inline-flex items-center justify-center p-2 rounded-md text-slate-300 hover:text-slate-100 hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-400"
          :aria-expanded="mobileMenuOpen"
          aria-label="Toggle navigation menu"
          @click="mobileMenuOpen = !mobileMenuOpen"
        >
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path 
              v-if="!mobileMenuOpen"
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2" 
              d="M4 6h16M4 12h16M4 18h16"
            />
            <path 
              v-else
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2" 
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <!-- Mobile Menu -->
      <div 
        v-if="mobileMenuOpen"
        class="md:hidden border-t border-slate-800 py-4"
      >
        <nav class="flex flex-col gap-3">
          <a
            v-for="link in navLinks"
            :key="link.label"
            :href="withLocale(link.href)"
            class="text-sm text-slate-300 hover:text-slate-100 px-3 py-2 rounded hover:bg-slate-800 transition-colors"
            @click="mobileMenuOpen = false"
          >
            {{ link.label }}
          </a>
          <a
            v-if="ctaButton"
            :href="withLocale(ctaButton.href)"
            class="inline-flex items-center justify-center px-4 py-2 mt-2 bg-blue-500 text-white font-semibold rounded hover:bg-blue-600 transition-colors"
            @click="mobileMenuOpen = false"
          >
            {{ ctaButton.label }}
          </a>
        </nav>
      </div>
    </div>
  </nav>
</template>

<script lang="ts" setup>
import {ref, computed} from 'vue'
import {useI18n} from 'vue-i18n'

interface LinkItem {
  label: string
  href: string
}

interface BrandConfig {
  name?: string
  logoSrc?: string | null
  href?: string
}

interface CtaButton {
  label: string
  href: string
}

interface Props {
  brand?: BrandConfig
  links?: LinkItem[]
  ctaButton?: CtaButton | null
}

const props = withDefaults(defineProps<Props>(), {
  brand: () => ({name: 'Open Ticket AI', logoSrc: null, href: '/'}),
  links: () => [],
  ctaButton: null
})

const {locale} = useI18n({useScope: 'global'})
const mobileMenuOpen = ref(false)

const brand = computed(() => ({
  name: 'Open Ticket AI',
  logoSrc: null,
  href: '/',
  ...(props.brand ?? {})
}))

const navLinks = computed(() => 
  props.links ?? [
    {label: 'Documentation', href: '/docs/'},
    {label: 'Demo', href: '/demo/'},
    {label: 'Pricing', href: '/pricing/'},
    {label: 'About', href: '/about/'}
  ]
)

const langCode = computed(() => locale.value.split('-')[0])

function withLocale(path: string) {
  return `/${langCode.value}${path}`.replace('//', '/')
}
</script>
