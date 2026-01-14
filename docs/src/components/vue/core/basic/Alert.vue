<template>
  <div :class="alertClasses">
    <div
      v-if="!hideIcon"
      class="mt-0.5 flex-shrink-0"
    >
      <component
        :is="iconComponent"
        :class="iconClasses"
        aria-hidden="true"
      />
    </div>
    <div class="flex-1">
      <h4
        v-if="title"
        class="mb-1 font-semibold"
      >
        {{ title }}
      </h4>
      <div class="text-sm">
        <slot />
      </div>
      <div
        v-if="$slots.footer"
        class="mt-3 border-t pt-3"
        :class="footerBorderClasses"
      >
        <slot name="footer" />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  LightBulbIcon,
  InformationCircleIcon,
} from '@heroicons/vue/24/outline';
import { alert } from '../design-system/recipes';
import type { Variant, Tone } from '../design-system/tokens.ts';

type AlertType = 'info' | 'success' | 'warning' | 'danger' | 'tip';

interface Props {
  type?: AlertType;
  title?: string;
  hideIcon?: boolean;
  variant?: Variant;
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info',
  hideIcon: false,
  variant: 'subtle',
  title: undefined,
});

// Map legacy 'tip' type to 'primary' tone
const tone = computed((): Tone => {
  if (props.type === 'tip') return 'primary';
  return props.type as Tone;
});

const alertClasses = computed(() => {
  return alert({
    variant: props.variant,
    tone: tone.value,
  });
});

const iconComponent = computed(() => {
  switch (props.type) {
    case 'success':
      return CheckCircleIcon;
    case 'warning':
      return ExclamationTriangleIcon;
    case 'danger':
      return XCircleIcon;
    case 'tip':
      return LightBulbIcon;
    default:
      return InformationCircleIcon;
  }
});

const iconClasses = computed(() => {
  const sizeClass = 'w-6 h-6';
  let colorClass = '';

  switch (props.type) {
    case 'success':
      colorClass = 'text-success';
      break;
    case 'warning':
      colorClass = 'text-warning';
      break;
    case 'danger':
      colorClass = 'text-danger';
      break;
    case 'tip':
      colorClass = 'text-primary-light';
      break;
    default:
      colorClass = 'text-info';
  }

  return `${sizeClass} ${colorClass}`;
});

const footerBorderClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'border-success/20';
    case 'warning':
      return 'border-warning/20';
    case 'danger':
      return 'border-danger/20';
    case 'tip':
      return 'border-primary/20';
    default:
      return 'border-info/20';
  }
});
</script>
