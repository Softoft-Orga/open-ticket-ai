<template>
  <div :class="cardClasses">
    <div v-if="$slots.image" :class="['-m-6 mb-0 overflow-hidden', imageRadiusClass]">
      <slot name="image" />
    </div>

    <div v-if="$slots.header" :class="headerClasses">
      <slot name="header" />
    </div>

    <div v-if="$slots.title" :class="titleClasses">
      <slot name="title" />
    </div>

    <div :class="contentClasses">
      <slot />
    </div>

    <template v-if="actionsSticky">
      <div v-if="$slots.actions || $slots.footer" :class="bottomClasses">
        <div v-if="$slots.actions" :class="actionsClasses">
          <slot name="actions" />
        </div>
        <div v-if="$slots.footer" :class="footerClasses">
          <slot name="footer" />
        </div>
      </div>
    </template>

    <template v-else>
      <div v-if="$slots.actions" :class="actionsClasses">
        <slot name="actions" />
      </div>
      <div v-if="$slots.footer" :class="footerClasses">
        <slot name="footer" />
      </div>
    </template>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { card } from '../design-system/recipes';
import type { Variant, Tone, Size, Radius, Elevation } from '../design-system/tokens.ts';

export interface CardProps {
  variant?: Variant;
  tone?: Tone;
  size?: Size;
  radius?: Radius;
  elevation?: Elevation;
  hoverable?: boolean;
  actionsSticky?: boolean;
}

const props = withDefaults(defineProps<CardProps>(), {
  variant: 'surface',
  size: 'md',
  radius: 'xl',
  elevation: 'none',
  hoverable: false,
  tone: undefined,
  actionsSticky: false,
});

const cardClasses = computed(() => {
  const base = card({
    variant: props.variant,
    tone: props.tone,
    size: props.size,
    radius: props.radius,
    elevation: props.elevation,
    hoverable: props.hoverable,
  });

  return props.actionsSticky ? `${base} h-full flex flex-col` : base;
});

const imageRadiusClass = computed(() => {
  switch (props.radius) {
    case 'lg':
      return 'rounded-t-lg';
    case '2xl':
      return 'rounded-t-2xl';
    default:
      return 'rounded-t-xl';
  }
});

const headerClasses = computed(() => (props.size === 'sm' ? 'mb-2' : 'mb-4'));

const titleClasses = computed(() => {
  const spacing = props.size === 'sm' ? 'mb-1' : 'mb-2';
  const fontSize = props.size === 'lg' ? 'text-xl' : 'text-lg';
  return `${spacing} ${fontSize} font-bold text-white`;
});

const contentClasses = computed(() => {
  const spacing = props.size === 'sm' ? 'mb-2' : 'mb-4';
  return `${spacing} text-white`;
});

const actionsClasses = computed(() => (props.size === 'sm' ? 'mt-2' : 'mt-4'));

const footerClasses = computed(() => {
  const spacing = props.size === 'sm' ? 'mt-2' : 'mt-4';
  return `${spacing} text-text-dim`;
});

const bottomClasses = computed(() => {
  const spacing = props.size === 'sm' ? 'mt-2' : 'mt-4';
  return `mt-auto ${spacing}`;
});
</script>
