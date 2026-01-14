<!-- Cell.vue -->
<template>
  <component :is="tag" :class="cellClasses">
    <slot />
  </component>
</template>

<script lang="ts" setup>
import { computed, inject, withDefaults } from 'vue';
import type { TableVariant } from './Table.vue';

type Align = 'left' | 'center' | 'right';

const props = withDefaults(defineProps<{ header?: boolean; align?: Align }>(), {
  header: false,
  align: 'left',
});

const dense = inject('tableDense', false) as boolean;
const variant = inject('tableVariant', 'default') as TableVariant;

const tag = computed(() => (props.header ? 'th' : 'td'));

const cellClasses = computed(() => {
  const classes: string[] = [];

  // Padding - simplified to semantic sizes
  if (variant === 'compact' || dense) {
    classes.push('px-3 py-2');
  } else {
    classes.push('px-4 py-3');
  }

  // Alignment - semantic utility classes
  if (props.align === 'center') classes.push('text-center');
  else if (props.align === 'right') classes.push('text-right');
  else classes.push('text-left');

  // Text styling - simplified, relies on parent context
  if (props.header) {
    classes.push('text-slate-200 font-semibold');
    if (variant === 'compact') {
      classes.push('text-xs uppercase tracking-wider');
    }
  } else {
    classes.push('text-text-dim');
  }

  return classes;
});
</script>
