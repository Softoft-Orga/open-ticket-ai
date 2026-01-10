<!-- Row.vue -->
<template>
  <tr :class="rowClasses">
    <slot/>
  </tr>
</template>

<script lang="ts" setup>
import {computed, inject} from 'vue'
import type {TableVariant} from './Table.vue'

const striped = inject('tableStriped', false) as boolean
const variant = inject('tableVariant', 'default') as TableVariant
const hoverEffect = inject('tableHoverEffect', true) as boolean

const rowClasses = computed(() => {
  const classes: string[] = []
  
  // Striped background based on variant
  if (striped) {
    switch (variant) {
      case 'glassy':
        classes.push('odd:bg-surface-dark/50 even:bg-surface-lighter/30')
        break
      case 'bordered':
        classes.push('odd:bg-surface-dark even:bg-surface-lighter')
        break
      case 'compact':
        classes.push('odd:bg-slate-900/50 even:bg-slate-800/50')
        break
      case 'borderless':
        classes.push('odd:bg-transparent even:bg-surface-dark/30')
        break
      case 'default':
      default:
        classes.push('odd:bg-surface-dark even:bg-surface-lighter')
    }
  }
  
  // Hover effect based on variant
  if (hoverEffect) {
    switch (variant) {
      case 'glassy':
        classes.push('hover:bg-primary/10 hover:backdrop-blur-md')
        break
      case 'bordered':
        classes.push('hover:bg-primary/5')
        break
      case 'compact':
        classes.push('hover:bg-slate-700/30')
        break
      case 'borderless':
        classes.push('hover:bg-surface-dark/50')
        break
      case 'default':
      default:
        classes.push('hover:bg-primary/5')
    }
  }
  
  // Transition for smooth hover
  classes.push('transition-colors duration-200')
  
  return classes
})
</script>
