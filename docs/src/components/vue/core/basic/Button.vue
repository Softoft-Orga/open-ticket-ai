<template>
  <component
    :is="componentType"
    :class="buttonClasses"
    :disabled="disabled || loading"
    :to="to"
    :href="href"
  >
    <slot />
  </component>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { button } from '../design-system/recipes';
import type { Variant, Tone, Size, Radius } from '../design-system/tokens.ts';

interface Props {
  variant?: Variant;
  size?: Size;
  tone?: Tone;
  radius?: Radius;
  disabled?: boolean;
  loading?: boolean;
  block?: boolean;
  to?: string;
  href?: string;
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'surface',
  size: 'md',
  tone: 'primary',
  radius: 'xl',
  disabled: false,
  loading: false,
  block: false,
  to: undefined,
  href: undefined,
});

const componentType = computed(() => {
  if (props.to) return 'router-link';
  if (props.href) return 'a';
  return 'button';
});

const buttonClasses = computed(() => {
  return button({
    variant: props.variant,
    tone: props.tone,
    size: props.size,
    radius: props.radius,
    loading: props.loading,
    disabled: props.disabled,
    block: props.block,
  });
});
</script>
