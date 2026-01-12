<template>
  <div :class="cardClasses">
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
import { card } from '../../../../design-system/recipes'
import type { Variant, Tone, Size, Radius, Elevation } from '../../../../design-system/tokens'

export interface CardProps {
  /**
   * Visual style variant from design system tokens
   * @default 'surface'
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
   * @default 'xl'
   */
  radius?: Radius

  /**
   * Shadow elevation level
   * @default 'none'
   */
  elevation?: Elevation

  /**
   * Whether to add hover effect
   * @default false
   */
  hoverable?: boolean
}

const props = withDefaults(defineProps<CardProps>(), {
  variant: 'surface',
  size: 'md',
  radius: 'xl',
  elevation: 'none',
  hoverable: false,
  tone: undefined
})

const cardClasses = computed(() => {
  return card({
    variant: props.variant,
    tone: props.tone,
    size: props.size,
    radius: props.radius,
    elevation: props.elevation,
    hoverable: props.hoverable
  })
})

const imageRadiusClass = computed(() => {
  // Image should match top radius of card
  switch (props.radius) {
    case 'lg':
      return 'rounded-t-lg'
    case '2xl':
      return 'rounded-t-2xl'
    default: // xl
      return 'rounded-t-xl'
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
