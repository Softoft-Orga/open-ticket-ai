<!-- Table.vue -->
<template>
  <div :class="['overflow-x-auto', containerClasses, widthClass]">
    <table :class="['!m-0 !p-0 text-sm', tableWidthClass, textColorClass]">
      <tbody :class="bodyDividerClass">
        <slot />
      </tbody>
    </table>
  </div>
</template>

<script lang="ts" setup>
import { computed, provide, toRef, withDefaults } from 'vue';
import { card } from '../design-system/recipes/card';
import type { Radius, Elevation } from '../design-system/tokens.ts';

export type TableWidth = 'stretch' | 'auto' | 'full';

const props = withDefaults(
  defineProps<{
    bordered?: boolean;
    striped?: boolean;
    dense?: boolean;
    width?: TableWidth;
    hoverEffect?: boolean;
    radius?: Radius;
    elevation?: Elevation;
  }>(),
  {
    bordered: true,
    striped: true,
    dense: false,
    width: 'full',
    hoverEffect: true,
    radius: 'xl',
    elevation: 'sm',
  }
);

// Provide props for child components
provide('tableStriped', toRef(props, 'striped'));
provide('tableDense', toRef(props, 'dense'));
provide('tableBordered', toRef(props, 'bordered'));
provide('tableHoverEffect', toRef(props, 'hoverEffect'));

// Width classes
const widthClass = computed(() => {
  switch (props.width) {
    case 'stretch':
      return 'w-full';
    case 'auto':
      return 'w-auto inline-block';
    case 'full':
    default:
      return 'w-full';
  }
});

const tableWidthClass = computed(() => {
  return props.width === 'auto' ? 'w-auto' : 'min-w-full';
});

// Container styling using card recipe
const containerClasses = computed(() => {
  if (!props.bordered) {
    return '';
  }

  return card({
    variant: 'surface',
    radius: props.radius,
    elevation: props.elevation,
  });
});

// Text color - using design tokens
const textColorClass = computed(() => {
  return 'text-text-dim';
});

// Body divider classes - using fixed token classes
const bodyDividerClass = computed(() => {
  if (!props.bordered) {
    return '';
  }
  return 'divide-y divide-border-dark';
});
</script>
