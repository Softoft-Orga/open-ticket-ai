<!-- Table.vue -->
<template>
  <div :class="[
    'overflow-x-auto',
    roundedClass,
    wrapperBorderClass,
    widthClass
  ]">
    <table :class="[
      'text-sm !m-0 !p-0',
      tableWidthClass,
      textColorClass
    ]">
      <tbody :class="bodyDividerClass">
        <slot/>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts" setup>
import {computed, provide, toRef, withDefaults} from 'vue'

export type TableVariant = 'default' | 'bordered' | 'borderless' | 'glassy' | 'compact'
export type TableWidth = 'stretch' | 'auto' | 'full'

const props = withDefaults(defineProps<{
  variant?: TableVariant
  striped?: boolean
  dense?: boolean
  width?: TableWidth
  borderColor?: string
  hoverEffect?: boolean
}>(), {
  variant: 'default',
  striped: true,
  dense: false,
  width: 'full',
  borderColor: '',
  hoverEffect: true
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

// Rounded corners based on variant
const roundedClass = computed(() => {
  if (props.variant === 'borderless') return ''
  return 'rounded-2xl'
})

// Text color based on variant
const textColorClass = computed(() => {
  switch (props.variant) {
    case 'glassy':
      return 'text-slate-200'
    case 'compact':
      return 'text-slate-300'
    default:
      return 'text-slate-300'
  }
})

// Wrapper border styling based on variant
const wrapperBorderClass = computed(() => {
  const borderColor = props.borderColor || 'border-dark'
  
  switch (props.variant) {
    case 'bordered':
      return `border-2 border-${borderColor} shadow-lg`
    case 'borderless':
      return ''
    case 'glassy':
      return `border border-${borderColor} bg-glass-gradient backdrop-blur-sm shadow-card`
    case 'compact':
      return `border border-${borderColor}`
    case 'default':
    default:
      return `border border-${borderColor}`
  }
})

// Body divider classes
const bodyDividerClass = computed(() => {
  const borderColor = props.borderColor || 'border-dark'
  
  if (props.variant === 'borderless') {
    return ''
  }
  return `divide-y divide-${borderColor}`
})
</script>
