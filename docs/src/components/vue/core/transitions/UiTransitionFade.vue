<template>
  <TransitionChild
    :as="as"
    :appear="appear"
    v-bind="fade"
  >
    <slot />
  </TransitionChild>
</template>

<script lang="ts" setup>
import { TransitionChild } from '@headlessui/vue'
import { fade } from './presets'

withDefaults(defineProps<{
  appear?: boolean
  as?: string
}>(), {
  appear: false,
  as: 'template'
})
</script>
