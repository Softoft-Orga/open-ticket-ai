<template>
  <span :class="[baseClass, variantClass, sizeClass, radiusClass, elevationClass]"><slot/></span>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import type { Tone, Size, Radius, Elevation } from '../design-system/tokens'

// Badge supports brand colors (primary, secondary) plus semantic tones
type BadgeType = 'primary' | 'secondary' | Tone

interface Props {
  type?: BadgeType
  size?: Size
  radius?: Radius
  elevation?: Elevation
}

const props = withDefaults(defineProps<Props>(), {
  type: 'secondary',
  size: 'md',
  radius: 'xl',
  elevation: 'sm'
})

const baseClass =
  'inline-flex items-center gap-1 font-semibold leading-tight ring-1 ring-inset transition-all duration-150'

const variantClass = computed(() => {
  switch (props.type) {
    case 'primary':
      return 'bg-primary text-white ring-primary/50 hover:bg-primary-dark hover:ring-primary/70'
    case 'info':
      return 'bg-info text-white ring-info/50 hover:bg-info/90 hover:ring-info/70'
    case 'success':
      return 'bg-success text-white ring-success/50 hover:bg-success-dark hover:ring-success/70'
    case 'warning':
      return 'bg-warning text-background-dark ring-warning/50 hover:bg-warning-dark hover:ring-warning/70'
    case 'danger':
      return 'bg-danger text-white ring-danger/50 hover:bg-danger-dark hover:ring-danger/70'
    default: // secondary
      return 'bg-secondary text-background-dark ring-secondary/50 hover:bg-secondary-dark hover:ring-secondary/70'
  }
})

const sizeClass = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'px-2 py-0.5 text-xs'
    case 'lg':
      return 'px-4 py-1.5 text-sm'
    default: // md
      return 'px-3 py-1 text-xs'
  }
})

const radiusClass = computed(() => {
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

const elevationClass = computed(() => {
  switch (props.elevation) {
    case 'none':
      return ''
    case 'md':
      return 'shadow-md'
    case 'lg':
      return 'shadow-lg'
    default: // sm
      return 'shadow-sm'
  }
})
</script>
