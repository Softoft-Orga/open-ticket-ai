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
        <template v-for="link in navLinks" :key="link.url">
          <!-- Nav item with dropdown -->
          <Menu
            v-if="link.children && link.children.length > 0"
            v-slot="{ open }"
            as="div"
            class="relative"
          >
            <MenuButton
              :class="[
                'flex items-center gap-1 rounded-lg px-2 py-1 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60',
                isActive(link.url) || isAnyChildActive(link.children)
                  ? 'text-text-1'
                  : 'text-text-2 hover:text-text-1',
              ]"
            >
              {{ link.label }}
              <ChevronDownIcon
                :class="['h-4 w-4 transition-transform duration-200', open ? 'rotate-180' : '']"
              />
            </MenuButton>
            <Transition
              enter-active-class="transition duration-100 ease-out"
              enter-from-class="transform scale-95 opacity-0"
              enter-to-class="transform scale-100 opacity-100"
              leave-active-class="transition duration-75 ease-in"
              leave-from-class="transform scale-100 opacity-100"
              leave-to-class="transform scale-95 opacity-0"
            >
              <MenuItems
                class="absolute left-0 mt-2 w-56 origin-top-left rounded-lg border border-border-dark bg-surface-dark shadow-lg ring-1 ring-black/5 focus:outline-none"
              >
                <div class="p-1">
                  <MenuItem v-for="child in link.children" :key="child.url" v-slot="{ active }">
                    <a
                      :href="child.url"
                      :class="[
                        'group flex w-full items-center rounded-lg px-3 py-2 text-sm transition-colors',
                        isActive(child.url)
                          ? 'bg-primary/20 text-text-1'
                          : active
                            ? 'bg-surface-lighter text-text-1'
                            : 'text-text-2',
                      ]"
                    >
                      {{ child.label }}
                    </a>
                  </MenuItem>
                </div>
              </MenuItems>
            </Transition>
          </Menu>
          <!-- Regular nav item without dropdown -->
          <a
            v-else
            :class="isActive(link.url) ? 'text-text-1' : 'text-text-2 hover:text-text-1'"
            :href="link.url"
            class="rounded-lg px-2 py-1 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60"
          >
            {{ link.label }}
          </a>
        </template>
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
                <template v-for="link in navLinks" :key="link.url">
                  <!-- Mobile nav item with children -->
                  <div v-if="link.children && link.children.length > 0" class="flex flex-col gap-1">
                    <button
                      :class="[
                        'flex items-center justify-between rounded-xl px-5 py-4 text-lg font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60',
                        isActive(link.url) || isAnyChildActive(link.children)
                          ? 'bg-primary/20 text-text-1'
                          : 'text-text-2 hover:bg-surface-lighter hover:text-text-1',
                      ]"
                      @click="toggleMobileDropdown(link.url)"
                    >
                      <span>{{ link.label }}</span>
                      <ChevronDownIcon
                        :class="[
                          'h-5 w-5 transition-transform duration-200',
                          mobileDropdownOpen[link.url] ? 'rotate-180' : '',
                        ]"
                      />
                    </button>
                    <Transition
                      enter-active-class="transition duration-200 ease-out"
                      enter-from-class="transform -translate-y-2 opacity-0"
                      enter-to-class="transform translate-y-0 opacity-100"
                      leave-active-class="transition duration-150 ease-in"
                      leave-from-class="transform translate-y-0 opacity-100"
                      leave-to-class="transform -translate-y-2 opacity-0"
                    >
                      <div
                        v-if="mobileDropdownOpen[link.url]"
                        class="ml-4 flex flex-col gap-1 border-l-2 border-primary/30 pl-4"
                      >
                        <a
                          v-for="child in link.children"
                          :key="child.url"
                          :href="child.url"
                          :class="[
                            'rounded-lg px-4 py-3 text-base font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60',
                            isActive(child.url)
                              ? 'bg-primary/20 text-text-1'
                              : 'text-text-2 hover:bg-surface-lighter hover:text-text-1',
                          ]"
                          @click="closeMobileMenu"
                        >
                          {{ child.label }}
                        </a>
                      </div>
                    </Transition>
                  </div>
                  <!-- Mobile nav item without children -->
                  <a
                    v-else
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
                </template>
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
import { Bars3Icon, XMarkIcon, ChevronDownIcon } from '@heroicons/vue/24/outline';
import {
  TransitionChild,
  TransitionRoot,
  Menu,
  MenuButton,
  MenuItems,
  MenuItem,
} from '@headlessui/vue';
import Button from '../basic/Button.vue';
import { fade, slideLeft } from '../transitions/presets';

type NavLink = {
  label: string;
  url: string;
  children?: { label: string; url: string }[];
};

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
  // Close all dropdowns when closing mobile menu
  mobileDropdownOpen.value = {};
};

const mobileDropdownOpen = ref<Record<string, boolean>>({});
const toggleMobileDropdown = (url: string) => {
  mobileDropdownOpen.value[url] = !mobileDropdownOpen.value[url];
};

const isActive = (url: string) => activePath.value === url || activePath.value.startsWith(url);

const isAnyChildActive = (children?: { label: string; url: string }[]) => {
  if (!children) return false;
  return children.some(child => isActive(child.url));
};
</script>
