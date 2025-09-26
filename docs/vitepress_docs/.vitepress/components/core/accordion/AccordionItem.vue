<template>
  <Disclosure :default-open="defaultOpen" as="div" class="py-3">
    <template #default="{ open }">
      <DisclosureButton class="flex w-full justify-between font-semibold text-left">
        <span class="font-bold text-lg">{{ title }}</span>
        <span>{{ open ? '–' : '+' }}</span>
      </DisclosureButton>
      <DisclosurePanel class="pt-2 text-vp-text-2">
        <slot />
      </DisclosurePanel>
    </template>
  </Disclosure>
</template>

<script setup lang="ts">
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'

defineProps<{
  title: string
  defaultOpen?: boolean
}>()
</script>
