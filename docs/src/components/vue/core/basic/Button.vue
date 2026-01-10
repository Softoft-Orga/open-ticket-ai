<template>
  <button
      :class="[
      'inline-flex items-center justify-center font-bold transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/50',
      sizeClasses,
      variantClasses,
      toneClasses,
      radiusClasses,
      elevationClasses,
      disabled && 'opacity-50 cursor-not-allowed'
    ]"
      :disabled="disabled"
  >
    <slot/>
  </button>
</template>

<script lang="ts" setup>
import {computed} from 'vue'
import type {Variant, Size, Tone, Radius, Elevation} from '../design-system/tokens'

interface Props {
  variant?: Variant
  size?: Size
  tone?: Tone
  radius?: Radius
  elevation?: Elevation
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  tone: undefined,
  radius: 'xl',
  elevation: 'none',
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
  if (props.tone) {
    return ''
  }
  
  switch (props.variant) {
    case 'secondary':
      return 'bg-white text-background-dark hover:bg-gray-200'
    case 'outline':
      return 'bg-transparent border border-border-dark hover:border-primary/50 text-white hover:bg-white/5'
    case 'ghost':
      return 'bg-transparent text-white hover:bg-white/10'
    default: // primary
      return 'bg-primary text-white hover:bg-primary-dark shadow-[0_0_20px_rgba(166,13,242,0.3)] hover:shadow-[0_0_30px_rgba(166,13,242,0.4)]'
  }
})

const toneClasses = computed(() => {
  if (!props.tone) return ''
  
  switch (props.tone) {
    case 'info':
      return 'bg-info text-white hover:bg-info/90'
    case 'success':
      return 'bg-success text-white hover:bg-success-dark'
    case 'warning':
      return 'bg-warning text-white hover:bg-warning-dark'
    case 'danger':
      return 'bg-danger text-white hover:bg-danger-dark'
    default:
      return ''
  }
})

const radiusClasses = computed(() => {
  switch (props.radius) {
    case 'md':
      return 'rounded-md'
    case 'lg':
      return 'rounded-lg'
    case '2xl':
      return 'rounded-2xl'
    default: // xl
      return 'rounded-xl'
  }
})

const elevationClasses = computed(() => {
  switch (props.elevation) {
    case 'sm':
      return 'shadow-sm'
    case 'md':
      return 'shadow-md'
    case 'lg':
      return 'shadow-lg'
    default: // none
      return ''
  }
})
</script>
