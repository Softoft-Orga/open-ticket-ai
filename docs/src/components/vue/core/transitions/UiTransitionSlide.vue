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
import { slideDownSm, slideUpSm, slideLeftSm, slideRightSm } from './presets'

const props = withDefaults(defineProps<{
  appear?: boolean
  as?: string
  direction: 'up' | 'down' | 'left' | 'right'
}>(), {
  appear: false,
  as: 'template'
})

const preset = computed(() => {
  switch (props.direction) {
    case 'down':
      return slideDownSm
    case 'up':
      return slideUpSm
    case 'left':
      return slideLeftSm
    case 'right':
      return slideRightSm
  }
})
</script>
