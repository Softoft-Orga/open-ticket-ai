<template>
  <TransitionChild
    :as="as"
    :appear="appear"
    v-bind="preset"
  >
    <slot />
  </TransitionChild>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { TransitionChild } from '@headlessui/vue'
import { fadeScaleSm, fadeScaleMd } from './presets'

const props = withDefaults(defineProps<{
  appear?: boolean
  as?: string
  strength?: 'sm' | 'md'
}>(), {
  appear: false,
  as: 'template',
  strength: 'sm'
})

const preset = computed(() => {
  return props.strength === 'md' ? fadeScaleMd : fadeScaleSm
})
</script>
