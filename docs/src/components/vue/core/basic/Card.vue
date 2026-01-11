<template>
  <div
    :class="[
      cardClasses,
      borderClass,
      radiusClass,
      elevationClass,
      sizeClass,
      'text-text-dim transition-all duration-200 motion-reduce:transition-none',
      hoverable && 'hover:border-primary/50 hover:shadow-glow cursor-pointer'
    ]"
  >
    <div
      v-if="$slots.image"
      :class="['overflow-hidden -m-6 mb-0', imageRadiusClass]"
    >
      <slot name="image" />
    </div>
    <div
      v-if="$slots.header"
      :class="headerClasses"
    >
      <slot name="header" />
    </div>
    <div
      v-if="$slots.title"
      :class="titleClasses"
    >
      <slot name="title" />
    </div>
    <div :class="contentClasses">
      <slot />
    </div>
    <div
      v-if="$slots.actions"
      :class="actionsClasses"
    >
      <slot name="actions" />
    </div>
    <div
      v-if="$slots.footer"
      :class="footerClasses"
    >
      <slot name="footer" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import type { Variant, Tone, Size, Radius, Elevation } from '../design-system/tokens'

export interface CardProps {
  /**
   * Visual style variant from design system tokens
   * When provided, overrides background prop with variant-specific styling
   * @default 'primary'
   */
  variant?: Variant

  /**
   * Semantic tone (status color)
   */
  tone?: Tone

  /**
   * Card size (affects padding)
   * @default 'md'
   */
  size?: Size

  /**
   * Border radius
   * @default 'lg'
   */
  radius?: Radius

  /**
   * Shadow elevation level
   * @default 'sm'
   */
  elevation?: Elevation

  /**
   * Whether to add hover effect
   * @default false
   */
  hoverable?: boolean

}

const props = withDefaults(defineProps<CardProps>(), {
  variant: 'primary',
  size: 'md',
  radius: 'lg',
  elevation: 'sm',
  hoverable: false,
})

const cardClasses = computed(() => {
  // Tone takes precedence over variant for background
  if (props.tone) {
    switch (props.tone) {
      case 'info':
        return 'bg-info-faint'
      case 'success':
        return 'bg-success-dark/10'
      case 'warning':
        return 'bg-warning-dark/10'
      case 'danger':
        return 'bg-danger-dark/10'
    }
  }

  // Variant-based backgrounds
  switch (props.variant) {
    case 'secondary':
      return 'bg-surface-lighter'
    case 'outline':
      return 'bg-transparent'
    case 'ghost':
      return 'bg-surface-dark/50'
    default: // primary
      return 'bg-surface-dark'
  }
})

const borderClass = computed(() => {
  if (props.tone) {
    switch (props.tone) {
      case 'info':
        return 'border border-info/30'
      case 'success':
        return 'border border-success/30'
      case 'warning':
        return 'border border-warning/30'
      case 'danger':
        return 'border border-danger/30'
    }
  }

  if (props.variant === 'outline') {
    return 'border-2 border-border-dark'
  }

  return 'border border-border-dark'
})

const radiusClass = computed(() => {
  switch (props.radius) {
    case 'md':
      return 'rounded-md'
    case 'xl':
      return 'rounded-xl'
    case '2xl':
      return 'rounded-2xl'
    default: // lg
      return 'rounded-lg'
  }
})

const imageRadiusClass = computed(() => {
  // Image should match top radius of card
  switch (props.radius) {
    case 'md':
      return 'rounded-t-md'
    case 'xl':
      return 'rounded-t-xl'
    case '2xl':
      return 'rounded-t-2xl'
    default: // lg
      return 'rounded-t-lg'
  }
})

const elevationClass = computed(() => {
  switch (props.elevation) {
    case 'none':
      return ''
    case 'md':
      return 'shadow-lg'
    case 'lg':
      return 'shadow-xl'
    default: // sm
      return 'shadow'
  }
})

const sizeClass = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'p-4'
    case 'lg':
      return 'p-8'
    default: // md
      return 'p-6'
  }
})

const headerClasses = computed(() => {
  const spacing = props.size === 'sm' ? 'mb-2' : 'mb-4'
  return spacing
})

const titleClasses = computed(() => {
  const spacing = props.size === 'sm' ? 'mb-1' : 'mb-2'
  const fontSize = props.size === 'lg' ? 'text-xl' : 'text-lg'
  return `${spacing} ${fontSize} font-bold text-white`
})

const contentClasses = computed(() => {
  const spacing = props.size === 'sm' ? 'mb-2' : 'mb-4'
  return `${spacing} text-white`
})

const actionsClasses = computed(() => {
  const spacing = props.size === 'sm' ? 'mt-2' : 'mt-4'
  return spacing
})

const footerClasses = computed(() => {
  const spacing = props.size === 'sm' ? 'mt-2' : 'mt-4'
  return `${spacing} text-text-dim`
})
</script>
