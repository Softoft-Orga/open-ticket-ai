<!-- Table.vue -->
<template>
  <div
    :class="[
      'overflow-x-auto',
      containerClasses,
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
import { card } from '../../../../design-system/recipes/card'
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

// Container styling using card recipe
const containerClasses = computed(() => {
  if (props.variant === 'borderless') {
    return ''
  }
  
  if (props.variant === 'glassy') {
    return card({
      variant: 'outline',
      radius: props.radius,
      elevation: props.elevation
    }) + ' backdrop-blur-sm'
  }
  
  return card({
    variant: 'surface',
    radius: props.radius,
    elevation: props.elevation
  })
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

// Body divider classes - using fixed token classes
const bodyDividerClass = computed(() => {
  if (props.variant === 'borderless') {
    return ''
  }
  return 'divide-y divide-border-dark'
})
</script>
