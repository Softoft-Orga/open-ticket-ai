<template>
  <TransitionChild
    as="template"
    enter="ease-out duration-300 motion-reduce:transition-none"
    enter-from="opacity-0"
    enter-to="opacity-100"
    leave="ease-in duration-200 motion-reduce:transition-none"
    leave-from="opacity-100"
    leave-to="opacity-0"
  >
    <slot />
  </TransitionChild>
</template>

<script setup lang="ts">
import { TransitionChild } from '@headlessui/vue'
</script>
