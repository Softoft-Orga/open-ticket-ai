<template>
  <header class="sticky top-0 z-50 w-full border-b border-surface-lighter bg-background-dark/80 backdrop-blur-md">
    <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
      <a
        class="flex items-center gap-2 text-white group focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/70 rounded-lg"
        href="/docs/public"
      >
        <div class="flex size-8 items-center justify-center rounded-lg bg-primary/20 text-primary transition-all group-hover:shadow-[0_0_15px_rgba(166,13,242,0.5)]">
          <TicketIcon
            aria-hidden="true"
            class="w-5 h-5"
          />
        </div>
        <h2 class="font-display text-lg font-bold tracking-tight">Open Ticket AI</h2>
      </a>

      <nav class="hidden md:flex flex-1 justify-center gap-8 text-sm font-medium">
        <a
          v-for="item in navItems"
          :key="item.href"
          :aria-current="isActive(item.href) ? 'page' : undefined"
          :class="isActive(item.href) ? 'text-white' : 'text-gray-400 hover:text-white'"
          :href="item.href"
          class="transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 rounded-lg px-2 py-1"
        >
          {{ item.label }}
        </a>

        <div
          class="relative"
          @mouseenter="openDocs"
          @mouseleave="closeDocs"
        >
          <button
            ref="docsTriggerRef"
            :aria-expanded="docsOpen"
            aria-haspopup="true"
            class="flex items-center gap-1 text-gray-400 hover:text-white transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 rounded-lg px-2 py-1"
            type="button"
            @click="toggleDocs"
          >
            Docs
            <ChevronDownIcon
              :class="docsOpen ? 'rotate-180 text-white' : 'text-gray-400'"
              class="h-4 w-4 transition-transform"
            />
          </button>

          <Transition name="fade-scale">
            <div
              v-if="docsOpen"
              ref="docsMenuRef"
              aria-label="Docs menu"
              class="absolute right-0 mt-3 w-72 rounded-2xl border border-surface-lighter bg-[#11011c] shadow-2xl backdrop-blur-xl p-4"
              role="menu"
            >
              <div class="space-y-4">
                <div>
                  <p class="text-xs uppercase tracking-[0.2em] text-slate-400">
                    Resources
                  </p>
                  <a
                    :href="docsHub.href"
                    class="mt-3 flex gap-3 rounded-xl border border-surface-lighter/60 bg-slate-900/60 px-3 py-2 text-left text-white transition-colors hover:border-surface-lighter hover:bg-surface-dark focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/40"
                    role="menuitem"
                  >
                    <BookOpenIcon class="mt-1 h-5 w-5 text-primary" />
                    <div>
                      <p class="text-sm font-semibold">{{ docsHub.label }}</p>
                      <p class="text-xs text-slate-400">Documentation Home</p>
                    </div>
                  </a>
                </div>

                <div>
                  <p class="text-xs uppercase tracking-[0.2em] text-slate-400">
                    Products & Guides
                  </p>
                  <a
                    v-for="link in docsProductLinks"
                    :key="link.href"
                    :href="link.href"
                    class="mt-3 flex gap-3 rounded-xl border border-surface-lighter/60 bg-slate-900/60 px-3 py-2 text-left text-white transition-colors hover:border-surface-lighter hover:bg-surface-dark focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/40"
                    role="menuitem"
                  >
                    <component
                      :is="link.icon"
                      class="mt-1 h-5 w-5 text-cyan-glow"
                    />
                    <div>
                      <p class="text-sm font-semibold">{{ link.label }}</p>
                      <p class="text-xs text-slate-400">{{ link.description }}</p>
                    </div>
                  </a>
                </div>
              </div>
            </div>
          </Transition>
        </div>
      </nav>

      <div class="hidden md:flex items-center gap-3">
        <Button variant="secondary" size="sm">Contact Sales</Button>
        <Button variant="primary" size="sm">See Demo</Button>
      </div>

      <button
        class="md:hidden flex items-center justify-center p-2 text-gray-400 hover:text-white transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 rounded-lg"
        @click="openMobileMenu"
        aria-label="Open menu"
      >
        <Bars3Icon class="h-6 w-6" />
      </button>
    </div>

    <TransitionRoot :show="mobileMenuOpen" as="template">
      <Dialog @close="closeMobileMenu" class="relative z-50 md:hidden">
        <UiTransitionFade>
          <div class="fixed inset-0 bg-black/80 backdrop-blur-sm" />
        </UiTransitionFade>

        <div class="fixed inset-0 flex items-start justify-end">
          <UiTransitionSlide direction="right">
            <DialogPanel class="w-full max-w-sm h-full bg-background-dark border-l border-surface-lighter p-6 shadow-2xl">
              <div class="flex items-center justify-between mb-8">
                <DialogTitle class="text-lg font-bold text-white">Menu</DialogTitle>
                <button
                  @click="closeMobileMenu"
                  class="p-2 text-gray-400 hover:text-white transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 rounded-lg"
                  aria-label="Close menu"
                >
                  <XMarkIcon class="h-6 w-6" />
                </button>
              </div>

              <nav class="flex flex-col gap-4">
                <a
                  v-for="item in navItems"
                  :key="item.href"
                  :href="item.href"
                  :class="[
                    'px-4 py-3 rounded-xl text-base font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60',
                    isActive(item.href) 
                      ? 'bg-primary/20 text-white border border-primary/40' 
                      : 'text-gray-400 hover:text-white hover:bg-surface-lighter'
                  ]"
                  @click="closeMobileMenu"
                >
                  {{ item.label }}
                </a>

                <Disclosure v-slot="{ open }">
                  <DisclosureButton
                    :class="[
                      'flex items-center justify-between px-4 py-3 rounded-xl text-base font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60',
                      open ? 'bg-primary/20 text-white border border-primary/40' : 'text-gray-400 hover:text-white hover:bg-surface-lighter'
                    ]"
                  >
                    <span>Docs</span>
                    <ChevronDownIcon :class="['h-5 w-5 transition-transform', open && 'rotate-180']" />
                  </DisclosureButton>
                  
                  <TransitionRoot>
                    <UiTransitionSlide direction="down">
                      <DisclosurePanel class="mt-2 ml-4 space-y-2">
                        <a
                          :href="docsHub.href"
                          class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm text-white bg-slate-900/60 border border-surface-lighter/60 hover:bg-surface-dark hover:border-surface-lighter transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/40"
                          @click="closeMobileMenu"
                        >
                          <BookOpenIcon class="h-5 w-5 text-primary" />
                          <div>
                            <p class="font-semibold">{{ docsHub.label }}</p>
                            <p class="text-xs text-slate-400">Documentation Home</p>
                          </div>
                        </a>
                        <a
                          v-for="link in docsProductLinks"
                          :key="link.href"
                          :href="link.href"
                          class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm text-white bg-slate-900/60 border border-surface-lighter/60 hover:bg-surface-dark hover:border-surface-lighter transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/40"
                          @click="closeMobileMenu"
                        >
                          <component :is="link.icon" class="h-5 w-5 text-cyan-glow" />
                          <div>
                            <p class="font-semibold">{{ link.label }}</p>
                            <p class="text-xs text-slate-400">{{ link.description }}</p>
                          </div>
                        </a>
                      </DisclosurePanel>
                    </UiTransitionSlide>
                  </TransitionRoot>
                </Disclosure>

                <div class="mt-6 pt-6 border-t border-surface-lighter space-y-3">
                  <Button variant="secondary" size="md" class="w-full">Contact Sales</Button>
                  <Button variant="primary" size="md" class="w-full">See Demo</Button>
                </div>
              </nav>
            </DialogPanel>
          </UiTransitionSlide>
        </div>
      </Dialog>
    </TransitionRoot>
  </header>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'
import {
  Menu,
  MenuButton,
  MenuItems,
  MenuItem,
  Dialog,
  DialogPanel,
  DialogTitle,
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
  TransitionRoot
} from '@headlessui/vue'
import {
  TicketIcon,
  ChevronDownIcon,
  BookOpenIcon,
  SparklesIcon,
  AdjustmentsHorizontalIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import Button from '../basic/Button.vue'
import UiTransitionFade from '../transitions/UiTransitionFade.vue'
import UiTransitionSlide from '../transitions/UiTransitionSlide.vue'

type NavItem = { href: string; label: string }

type Props = {
  navItems?: NavItem[]
  currentPath?: string
}

const props = defineProps<Props>()

const defaultNavItems: NavItem[] = [
  { href: '/products/', label: 'Products' },
  { href: '/services/', label: 'Services' },
  { href: '/pricing/', label: 'Pricing' }
]

const navItems = computed(() => props.navItems ?? defaultNavItems)

const activePath = ref(props.currentPath ?? '/')
const updateActivePath = () => {
  if (typeof window !== 'undefined') {
    activePath.value = props.currentPath ?? window.location.pathname
  }
}

onMounted(() => {
  updateActivePath()
})

const docsHub = { href: '/docs/', label: 'Docs Hub' }
const docsProductLinks = [
  { href: '/docs/ticket-tagging/', label: 'Ticket Tagging AI', description: 'Classification Engine', icon: AdjustmentsHorizontalIcon },
  { href: '/docs/open-ticket-automation/', label: 'Open Ticket Automation', description: 'Workflow Layer', icon: SparklesIcon }
]

const mobileMenuOpen = ref(false)
const openMobileMenu = () => {
  mobileMenuOpen.value = true
}
const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

const isActive = (href: string) => activePath.value === href || activePath.value.startsWith(href)
</script>
