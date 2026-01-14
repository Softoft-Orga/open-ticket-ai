<template>
  <header
    class="sticky top-0 z-50 w-full border-b border-border-dark bg-background-dark/80 backdrop-blur-md"
  >
    <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
      <a
        class="flex items-center gap-3 rounded-lg text-text-1 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/70"
        href="/"
      >
        <img
          :src="logoSrc"
          alt="Company logo"
          class="size-10 rounded-lg border border-border-dark object-cover"
        >
        <span class="font-display text-lg font-bold tracking-tight">Open Ticket AI</span>
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
        <Button
          v-if="ctaLabel"
          :href="ctaUrl"
          variant="subtle"
          tone="primary"
          size="md"
        >
          {{ ctaLabel }}
        </Button>
      </div>

      <button
        class="flex items-center justify-center rounded-lg p-2 text-text-2 transition-colors hover:text-text-1 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 md:hidden"
        aria-label="Open menu"
        @click="openMobileMenu"
      >
        <Bars3Icon class="h-6 w-6" />
      </button>
    </div>

    <TransitionRoot
      :show="mobileMenuOpen"
      as="template"
    >
      <div class="md:hidden">
        <TransitionChild
          v-bind="fade"
          as="template"
        >
          <div
            class="fixed inset-0 bg-background-dark/80 backdrop-blur-sm"
            @click="closeMobileMenu"
          />
        </TransitionChild>
        <TransitionChild
          v-bind="slideLeft"
          as="template"
        >
          <div class="fixed inset-y-0 right-0 flex w-full max-w-sm">
            <div class="h-full w-full border-l border-border-dark bg-surface-dark p-6 shadow-2xl">
              <div class="mb-8 flex items-center justify-between">
                <p class="text-lg font-bold text-text-1">
                  Menu
                </p>
                <button
                  class="rounded-lg p-2 text-text-2 transition-colors hover:text-text-1 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60"
                  aria-label="Close menu"
                  @click="closeMobileMenu"
                >
                  <XMarkIcon class="h-6 w-6" />
                </button>
              </div>

              <nav class="flex flex-col gap-3">
                <a
                  v-for="link in navLinks"
                  :key="link.url"
                  :class="[
                    'rounded-xl px-4 py-3 text-base font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60',
                    isActive(link.url)
                      ? 'border border-primary/40 bg-primary/20 text-text-1'
                      : 'text-text-2 hover:bg-surface-lighter',
                  ]"
                  :href="link.url"
                  @click="closeMobileMenu"
                >
                  {{ link.label }}
                </a>
              </nav>

              <div
                v-if="ctaLabel"
                class="mt-8 border-t border-border-dark pt-6"
              >
                <Button
                  :href="ctaUrl"
                  variant="subtle"
                  tone="primary"
                  size="md"
                  block
                >
                  {{ ctaLabel }}
                </Button>
              </div>
            </div>
          </div>
        </TransitionChild>
      </div>
    </TransitionRoot>
  </header>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { Bars3Icon, XMarkIcon } from '@heroicons/vue/24/outline';
import { TransitionRoot, TransitionChild } from '@headlessui/vue';
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
const logoSrc = computed(() => props.logoUrl ?? '/public/open-ticket-logo.png');

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
