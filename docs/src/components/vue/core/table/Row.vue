<!-- Row.vue -->
<template>
  <tr :class="rowClasses">
    <slot />
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
  
  // Striped background based on variant - using design tokens
  if (striped) {
    switch (variant) {
      case 'glassy':
        classes.push('odd:bg-surface-dark/50 even:bg-surface-lighter/30')
        break
      case 'bordered':
        classes.push('odd:bg-surface-dark even:bg-surface-lighter')
        break
      case 'compact':
        classes.push('odd:bg-surface-dark/70 even:bg-surface-lighter/50')
        break
      case 'borderless':
        classes.push('odd:bg-transparent even:bg-surface-dark/30')
        break
      case 'default':
      default:
        classes.push('odd:bg-surface-dark even:bg-surface-lighter')
    }
  }
  
  // Hover effect - stronger but tasteful with smooth transitions
  if (hoverEffect) {
    switch (variant) {
      case 'glassy':
        classes.push('hover:bg-primary/20 hover:backdrop-blur-md hover:shadow-md')
        break
      case 'bordered':
        classes.push('hover:bg-primary/15 hover:shadow-sm')
        break
      case 'compact':
        classes.push('hover:bg-primary/10 hover:ring-1 hover:ring-primary/30')
        break
      case 'borderless':
        classes.push('hover:bg-surface-lighter/60')
        break
      case 'default':
      default:
        classes.push('hover:bg-primary/15 hover:shadow-sm')
    }
  }
  
  // Smooth transition for colors and shadows
  classes.push('transition-all duration-200 ease-in-out')
  
  return classes
})
</script>
