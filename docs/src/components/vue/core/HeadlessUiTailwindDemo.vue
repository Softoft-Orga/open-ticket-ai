<script lang="ts" setup>
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
</script>

<template>
  <Disclosure v-slot="{ open }" as="div" class="w-[320px]">
    <DisclosureButton
      class="flex w-full items-center justify-between rounded-xl bg-surface-lighter px-4 py-3 text-left text-white shadow-card ring-1 ring-border-dark transition ui-open:bg-primary ui-open:ring-primary-dark ui-open:shadow-neon-cyan hover:bg-surface-lighter/80 focus:outline-none focus:ring-2 focus:ring-secondary focus:ring-offset-2 focus:ring-offset-background-dark"
    >
      <span class="font-semibold">Headless UI Tailwind plugin is active</span>
      <span class="text-sm text-text-dim">{{ open ? 'Hide' : 'Show' }}</span>
    </DisclosureButton>

    <DisclosurePanel class="mt-3 rounded-xl border border-border-dark bg-surface-lighter/80 p-4 text-sm text-text-dim shadow-card backdrop-blur ui-open:animate-fade-in ui-closed:animate-fade-out">
      You can now target Headless UI states with <code class="rounded bg-surface-dark px-1 py-0.5 text-primary">ui-open</code> and
      <code class="rounded bg-surface-dark px-1 py-0.5 text-primary">ui-closed</code> variants.
    </DisclosurePanel>
  </Disclosure>
</template>

