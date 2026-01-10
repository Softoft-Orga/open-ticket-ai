<!-- Cell.vue -->
<template>
  <component :is="tag"
             :class="cellClasses">
    <slot/>
  </component>
</template>

<script lang="ts" setup>
import {computed, inject, withDefaults} from 'vue'
import type {TableVariant} from './Table.vue'

type Align = 'left' | 'center' | 'right'

const props = withDefaults(defineProps<{ header?: boolean; align?: Align }>(), {
  header: false,
  align: 'left'
})

const dense = inject('tableDense', false) as boolean
const variant = inject('tableVariant', 'default') as TableVariant

const tag = computed(() => (props.header ? 'th' : 'td'))

const alignClass = computed(() => {
  if (props.align === 'center') return 'text-center'
  if (props.align === 'right') return 'text-right'
  return 'text-left'
})

const cellClasses = computed(() => {
  const classes: string[] = []
  
  // Padding based on variant and density
  if (variant === 'compact' || dense) {
    classes.push('px-3 py-2')
  } else {
    classes.push('px-4 py-3')
  }
  
  // Alignment
  classes.push(alignClass.value)
  
  // Text styling for headers
  if (props.header) {
    switch (variant) {
      case 'glassy':
        classes.push('text-white font-bold tracking-wide')
        break
      case 'bordered':
        classes.push('text-primary-light font-semibold')
        break
      case 'compact':
        classes.push('text-slate-200 font-semibold text-xs uppercase tracking-wider')
        break
      default:
        classes.push('text-slate-200 font-semibold')
    }
  } else {
    // Regular cell text color
    switch (variant) {
      case 'glassy':
        classes.push('text-slate-300')
        break
      default:
        classes.push('text-slate-300')
    }
  }
  
  return classes
})
</script>
