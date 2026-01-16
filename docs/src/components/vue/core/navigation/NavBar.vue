<template>
  <header
    class="sticky top-0 z-50 w-full border-b border-border-dark bg-background-dark/80 backdrop-blur-md"
  >
    <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
      <a
        class="flex items-center gap-3 rounded-lg text-text-1 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/70"
        href="/"
      >
        <img :src="logoSrc" alt="Company logo" class="size-10 object-contain" />
        <span
          class="font-display bg-gradient-to-r from-primary to-cyan-400 bg-clip-text text-lg font-bold tracking-tight text-transparent"
        >
          Open Ticket AI
        </span>
      </a>

      <nav class="hidden flex-1 justify-center gap-8 text-sm font-medium md:flex">
        <a
          v-for="link in navLinks"
          :key="link.url"
          :class="isActive(link.url) ? 'text-text-1' : 'text-text-2 hover:text-text-1'"
          :href="link.url"
          class="rounded-lg px-2 py-1 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60"
        >
          {{ link.label }}
        </a>
      </nav>

      <div class="hidden items-center gap-4 md:flex">
        <Button v-if="ctaLabel" :href="ctaUrl" size="md" tone="primary" variant="subtle">
          {{ ctaLabel }}
        </Button>
        <slot v-else />
      </div>

      <button
        aria-label="Open menu"
        class="flex items-center justify-center rounded-lg p-2 text-text-2 transition-colors hover:text-text-1 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 md:hidden"
        @click="openMobileMenu"
      >
        <Bars3Icon class="h-6 w-6" />
      </button>
    </div>
  </header>

  <Teleport to="body">
    <TransitionRoot :show="mobileMenuOpen" as="template">
      <div class="fixed inset-0 z-50 md:hidden">
        <TransitionChild as="template" v-bind="fade">
          <div
            class="fixed inset-0 bg-background-dark/95 backdrop-blur-md"
            @click="closeMobileMenu"
          />
        </TransitionChild>
        <TransitionChild as="template" v-bind="slideLeft">
          <div class="fixed inset-0 z-10 flex">
            <div
              class="flex h-full w-full flex-col border-4 border-primary/30 bg-surface-dark shadow-[0_0_40px_rgba(166,13,242,0.3)]"
            >
              <div
                class="flex h-16 items-center justify-between border-b border-primary/20 bg-surface-lighter px-4"
              >
                <div class="flex items-center gap-3">
                  <img :src="logoSrc" alt="Company logo" class="size-10 object-contain" />
                  <span
                    class="font-display bg-gradient-to-r from-primary to-cyan-400 bg-clip-text text-lg font-bold tracking-tight text-transparent"
                  >
                    Open Ticket AI
                  </span>
                </div>
                <button
                  aria-label="Close menu"
                  class="rounded-lg p-2 text-text-2 transition-colors hover:text-text-1 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60"
                  @click="closeMobileMenu"
                >
                  <XMarkIcon class="h-6 w-6" />
                </button>
              </div>

              <nav class="flex flex-1 flex-col gap-1 overflow-y-auto p-4">
                <a
                  v-for="link in navLinks"
                  :key="link.url"
                  :class="[
                    'rounded-xl px-5 py-4 text-lg font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60',
                    isActive(link.url)
                      ? 'bg-primary/20 text-text-1'
                      : 'text-text-2 hover:bg-surface-lighter hover:text-text-1',
                  ]"
                  :href="link.url"
                  @click="closeMobileMenu"
                >
                  {{ link.label }}
                </a>
              </nav>

              <div v-if="ctaLabel" class="border-t border-primary/20 p-4">
                <Button :href="ctaUrl" block size="lg" tone="primary" variant="subtle">
                  {{ ctaLabel }}
                </Button>
              </div>
              <slot v-else></slot>
            </div>
          </div>
        </TransitionChild>
      </div>
    </TransitionRoot>
  </Teleport>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { Bars3Icon, XMarkIcon } from '@heroicons/vue/24/outline';
import { TransitionChild, TransitionRoot } from '@headlessui/vue';
import Button from '../basic/Button.vue';
import { fade, slideLeft } from '../transitions/presets';

type NavLink = { label: string; url: string };

type Props = {
  logoUrl?: string;
  links?: NavLink[];
  ctaLabel?: string;
  ctaUrl?: string;
};

const props = defineProps<Props>();

const navLinks = computed(() => props.links || []);
const logoSrc = computed(() => props.logoUrl);

const activePath = ref('/');
const syncActivePath = () => {
  if (typeof window !== 'undefined') {
    activePath.value = window.location.pathname;
  }
};

onMounted(syncActivePath);

const mobileMenuOpen = ref(false);
const openMobileMenu = () => {
  mobileMenuOpen.value = true;
};
const closeMobileMenu = () => {
  mobileMenuOpen.value = false;
};

const isActive = (url: string) => activePath.value === url || activePath.value.startsWith(url);
</script>
