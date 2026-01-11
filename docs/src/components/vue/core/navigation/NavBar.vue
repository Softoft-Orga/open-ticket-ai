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
          class="transition-colors"
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

      <div class="flex items-center gap-4">
        <button class="hidden sm:flex h-9 items-center justify-center rounded-lg bg-surface-lighter px-4 text-sm font-bold text-white transition-colors hover:bg-surface-lighter/80 border border-primary/20">
          Login
        </button>
        <button class="flex h-9 items-center justify-center rounded-lg bg-primary px-4 text-sm font-bold text-white shadow-[0_0_15px_rgba(166,13,242,0.3)] transition-all hover:bg-primary-dark">
          Get Demo
        </button>
      </div>
    </div>
  </header>
</template>

<script lang="ts" setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { TicketIcon, ChevronDownIcon, BookOpenIcon, SparklesIcon, AdjustmentsHorizontalIcon } from '@heroicons/vue/24/outline'

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
  document.addEventListener('click', handleGlobalClick, true)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleGlobalClick, true)
})

const docsHub = { href: '/docs/', label: 'Docs Hub' }
const docsProductLinks = [
  { href: '/docs/ticket-tagging/', label: 'Ticket Tagging AI', description: 'Classification Engine', icon: AdjustmentsHorizontalIcon },
  { href: '/docs/open-ticket-automation/', label: 'Open Ticket Automation', description: 'Workflow Layer', icon: SparklesIcon }
]

const docsOpen = ref(false)
const docsTriggerRef = ref<HTMLElement | null>(null)
const docsMenuRef = ref<HTMLElement | null>(null)

const toggleDocs = () => (docsOpen.value = !docsOpen.value)
const openDocs = () => (docsOpen.value = true)
const closeDocs = () => (docsOpen.value = false)

const handleGlobalClick = (event: MouseEvent) => {
  if (!docsOpen.value) return
  const target = event.target as Node | null
  if (!target) return
  if (docsMenuRef.value?.contains(target) || docsTriggerRef.value?.contains(target)) return
  closeDocs()
}

const isActive = (href: string) => activePath.value === href || activePath.value.startsWith(href)
</script>

<style scoped>
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: translateY(-4px) scale(0.98);
}
.fade-scale-enter-to,
.fade-scale-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}
</style>
