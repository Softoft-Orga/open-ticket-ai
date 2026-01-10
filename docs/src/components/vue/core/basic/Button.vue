<template>
  <button
      :class="[
      'inline-flex items-center justify-center font-bold rounded-xl transition-all focus:outline-none focus:ring-2 focus:ring-primary/50',
      sizeClasses,
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
import type {Variant, Size} from '../design-system/tokens'

interface Props {
  variant?: Variant
  size?: Size
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'h-10 px-6 text-sm'
    case 'lg':
      return 'h-14 px-10 text-lg'
    default: // md
      return 'h-12 px-8 text-base'
  }
})

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'secondary':
      return 'bg-white text-background-dark hover:bg-gray-200 transition-colors'
    case 'outline':
      return 'bg-transparent border border-border-dark hover:border-primary/50 text-white hover:bg-white/5 transition-all'
    case 'ghost':
      return 'bg-transparent text-white hover:bg-white/10 transition-colors'
    default: // primary
      return 'bg-primary text-white hover:bg-primary-dark shadow-[0_0_20px_rgba(166,13,242,0.3)] hover:shadow-[0_0_30px_rgba(166,13,242,0.4)] transition-all'
  }
})
</script>
