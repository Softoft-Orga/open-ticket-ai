<template>
  <TransitionChild
    as="template"
    :enter="enterClass"
    :enter-from="enterFromClass"
    :enter-to="enterToClass"
    :leave="leaveClass"
    :leave-from="leaveFromClass"
    :leave-to="leaveToClass"
  >
    <slot />
  </TransitionChild>
</template>

<script setup lang="ts">
import { TransitionChild } from '@headlessui/vue'
import { computed } from 'vue'

interface Props {
  direction?: 'up' | 'down' | 'left' | 'right'
}

const props = withDefaults(defineProps<Props>(), {
  direction: 'down'
})

const baseTransition = 'ease-out duration-300 motion-reduce:transition-none'
const baseTransitionLeave = 'ease-in duration-200 motion-reduce:transition-none'

const enterClass = computed(() => baseTransition)
const leaveClass = computed(() => baseTransitionLeave)

const enterFromClass = computed(() => {
  switch (props.direction) {
    case 'up':
      return 'opacity-0 translate-y-4'
    case 'down':
      return 'opacity-0 -translate-y-4'
    case 'left':
      return 'opacity-0 translate-x-4'
    case 'right':
      return 'opacity-0 -translate-x-4'
    default:
      return 'opacity-0'
  }
})

const enterToClass = computed(() => 'opacity-100 translate-x-0 translate-y-0')

const leaveFromClass = computed(() => 'opacity-100 translate-x-0 translate-y-0')

const leaveToClass = computed(() => {
  switch (props.direction) {
    case 'up':
      return 'opacity-0 translate-y-4'
    case 'down':
      return 'opacity-0 -translate-y-4'
    case 'left':
      return 'opacity-0 translate-x-4'
    case 'right':
      return 'opacity-0 -translate-x-4'
    default:
      return 'opacity-0'
  }
})
</script>
