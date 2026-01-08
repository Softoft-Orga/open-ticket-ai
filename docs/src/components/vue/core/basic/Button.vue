<template>
  <button
      :class="[
      'inline-flex items-center font-semibold rounded transition focus:outline-none px-4 py-2',
      variantClasses,
      disabled && 'opacity-50 cursor-not-allowed'
    ]"
      :disabled="disabled"
  >
    <slot/>
  </button>
</template>

<script lang="ts" setup>
import {computed} from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'info' | 'success' | 'warning' | 'danger'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  disabled: false
})

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'secondary':
      return 'border border-border-dark bg-surface-dark text-text-dim hover:bg-surface-lighter'
    case 'info':
      return 'bg-cyan-glow text-background-dark hover:brightness-110'
    case 'success':
      return 'bg-primary-light text-background-dark hover:bg-primary'
    case 'warning':
      return 'bg-amber-500 text-white hover:bg-amber-600'
    case 'danger':
      return 'bg-rose-600 text-white hover:bg-rose-700'
    default: // primary
      return 'bg-primary text-white hover:bg-primary-dark'
  }
})
</script>
