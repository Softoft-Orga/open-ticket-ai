<!-- Table.vue -->
<template>
  <div
    :class="[
      'overflow-x-auto',
      roundedClass,
      elevationClass,
      wrapperBorderClass,
      widthClass
    ]"
  >
    <table
      :class="[
        'text-sm !m-0 !p-0',
        tableWidthClass,
        textColorClass
      ]"
    >
      <tbody :class="bodyDividerClass">
        <slot />
      </tbody>
    </table>
  </div>
</template>

<script lang="ts" setup>
import {computed, provide, toRef, withDefaults} from 'vue'
import type {Radius, Elevation} from '../design-system/tokens'

export type TableVariant = 'default' | 'bordered' | 'borderless' | 'glassy' | 'compact'
export type TableWidth = 'stretch' | 'auto' | 'full'

const props = withDefaults(defineProps<{
  variant?: TableVariant
  striped?: boolean
  dense?: boolean
  width?: TableWidth
  hoverEffect?: boolean
  radius?: Radius
  elevation?: Elevation
}>(), {
  variant: 'default',
  striped: true,
  dense: false,
  width: 'full',
  hoverEffect: true,
  radius: 'xl',
  elevation: 'sm'
})

// Provide props for child components
provide('tableStriped', toRef(props, 'striped'))
provide('tableDense', toRef(props, 'dense'))
provide('tableVariant', toRef(props, 'variant'))
provide('tableHoverEffect', toRef(props, 'hoverEffect'))

// Width classes
const widthClass = computed(() => {
  switch (props.width) {
    case 'stretch':
      return 'w-full'
    case 'auto':
      return 'w-auto inline-block'
    case 'full':
    default:
      return 'w-full'
  }
})

const tableWidthClass = computed(() => {
  return props.width === 'auto' ? 'w-auto' : 'min-w-full'
})

// Rounded corners based on variant and radius prop
const roundedClass = computed(() => {
  if (props.variant === 'borderless') return ''
  
  // Map radius prop to Tailwind classes
  const radiusMap: Record<Radius, string> = {
    'md': 'rounded-md',
    'lg': 'rounded-lg',
    'xl': 'rounded-xl',
    '2xl': 'rounded-2xl'
  }
  
  return radiusMap[props.radius]
})

// Elevation (shadow) based on variant and elevation prop
const elevationClass = computed(() => {
  if (props.variant === 'borderless') return ''
  
  // Map elevation prop to Tailwind shadow classes
  const elevationMap: Record<Elevation, string> = {
    'none': '',
    'sm': 'shadow-sm',
    'md': 'shadow-md',
    'lg': 'shadow-lg'
  }
  
  return elevationMap[props.elevation]
})

// Text color based on variant - using design tokens
const textColorClass = computed(() => {
  switch (props.variant) {
    case 'glassy':
      return 'text-slate-200'
    case 'compact':
      return 'text-text-dim'
    default:
      return 'text-text-dim'
  }
})

// Wrapper border styling based on variant - using fixed token classes
const wrapperBorderClass = computed(() => {
  switch (props.variant) {
    case 'bordered':
      return 'border-2 border-border-dark'
    case 'borderless':
      return ''
    case 'glassy':
      return 'border border-border-dark bg-glass-gradient backdrop-blur-sm'
    case 'compact':
      return 'border border-border-dark bg-surface-dark'
    case 'default':
    default:
      return 'border border-border-dark bg-surface-dark'
  }
})

// Body divider classes - using fixed token classes
const bodyDividerClass = computed(() => {
  if (props.variant === 'borderless') {
    return ''
  }
  return 'divide-y divide-border-dark'
})
</script>
