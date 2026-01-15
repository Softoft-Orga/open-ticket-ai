<!-- Row.vue -->
<template>
  <tr :class="rowClasses">
    <slot />
  </tr>
</template>

<script lang="ts" setup>
import { computed, inject } from 'vue';
import type { TableVariant } from './Table.vue';

const striped = inject('tableStriped', false) as boolean;
const variant = inject('tableVariant', 'default') as TableVariant;
const hoverEffect = inject('tableHoverEffect', true) as boolean;

const rowClasses = computed(() => {
  const classes: string[] = [];

  // Striped background - using semantic utilities with Tailwind design tokens
  if (striped) {
    if (variant === 'borderless') {
      classes.push('odd:bg-transparent even:bg-surface-dark/30');
    } else {
      classes.push('odd:bg-surface-dark even:bg-surface-lighter');
    }
  }

  // Hover effect - simplified
  if (hoverEffect) {
    classes.push('hover:bg-primary/15 hover:shadow-sm');
  }

  // Smooth transition
  classes.push('transition-all duration-200 ease-in-out');

  return classes;
});
</script>
