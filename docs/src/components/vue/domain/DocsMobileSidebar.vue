<template>
  <div>
    <!-- Mobile Sidebar Toggle Button - Only visible on mobile/tablet -->
    <!-- eslint-disable-next-line vue/no-restricted-syntax -->
    <button
      class="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-primary shadow-lg transition-transform hover:scale-110 active:scale-95 lg:hidden"
      aria-label="Open sidebar menu"
      @click="isOpen = true"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="2"
        stroke="currentColor"
        class="h-6 w-6 text-white"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
        />
      </svg>
    </button>

    <!-- Mobile Sidebar Dialog -->
    <TransitionRoot :show="isOpen" as="template">
      <Dialog class="relative z-50 lg:hidden" @close="isOpen = false">
        <!-- Backdrop -->
        <TransitionChild
          as="template"
          enter="transition-opacity duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="transition-opacity duration-200"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/80 backdrop-blur-sm" aria-hidden="true" />
        </TransitionChild>

        <!-- Sidebar Panel -->
        <div class="fixed inset-0 flex justify-end">
          <TransitionChild
            as="template"
            enter="transform transition duration-300 ease-out"
            enter-from="translate-x-full"
            enter-to="translate-x-0"
            leave="transform transition duration-200 ease-in"
            leave-from="translate-x-0"
            leave-to="translate-x-full"
          >
            <DialogPanel
              class="relative flex h-full w-full max-w-sm flex-col bg-[#0f0814] shadow-xl"
            >
              <!-- Header -->
              <div class="flex items-center justify-between border-b border-white/5 px-6 py-4">
                <DialogTitle class="text-lg font-bold text-white">Documentation</DialogTitle>
                <!-- eslint-disable-next-line vue/no-restricted-syntax -->
                <button
                  class="rounded-md p-2 text-slate-400 transition-colors hover:bg-white/5 hover:text-white"
                  aria-label="Close sidebar"
                  @click="isOpen = false"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="2"
                    stroke="currentColor"
                    class="h-6 w-6"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <!-- Scrollable Navigation -->
              <nav
                class="flex-1 overflow-y-auto px-4 py-6"
                style="scrollbar-width: thin; scrollbar-color: #374151 transparent"
              >
                <div v-for="section in sidebarSections" :key="section.label" class="mb-6">
                  <h3
                    class="mb-2 px-3 text-[11px] font-black uppercase tracking-widest text-slate-500"
                  >
                    {{ section.label }}
                  </h3>
                  <ul class="space-y-1">
                    <li v-for="item in section.items" :key="item.link">
                      <a
                        :href="item.link"
                        :class="[
                          'block rounded-md px-3 py-2 text-sm transition-all',
                          item.active
                            ? 'bg-white/10 font-semibold text-white'
                            : 'text-slate-400 hover:bg-white/5 hover:text-white',
                        ]"
                        @click="isOpen = false"
                      >
                        {{ item.label }}
                      </a>
                    </li>
                  </ul>
                </div>
              </nav>

              <!-- Footer - Optional GitHub Link -->
              <div class="border-t border-white/5 px-6 py-4">
                <a
                  href="https://github.com/Softoft-Orga/open-ticket-ai"
                  target="_blank"
                  class="flex items-center gap-2 text-sm text-slate-400 hover:text-white"
                >
                  <span class="text-base">⚡</span>
                  GitHub
                </a>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionRoot, TransitionChild } from '@headlessui/vue';

interface SidebarItem {
  label: string;
  link: string;
  active: boolean;
}

interface SidebarSection {
  label: string;
  items: SidebarItem[];
}

defineProps<{
  sidebarSections: SidebarSection[];
}>();

const isOpen = ref(false);
</script>
