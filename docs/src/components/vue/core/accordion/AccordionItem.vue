<template>
  <Disclosure v-slot="{ open }" :default-open="defaultOpen" as="div" :class="surfaceClasses">
    <DisclosureButton :disabled="disabled" :class="buttonClasses">
      <slot name="title" :open="open">
        <span class="text-lg font-semibold text-white">{{ title }}</span>
      </slot>
      <svg
        :class="[
          'h-5 w-5 flex-shrink-0 transition-transform duration-300',
          open ? 'rotate-180' : 'rotate-0',
          iconClasses,
        ]"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        aria-hidden="true"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </DisclosureButton>
    <transition
      enter-active-class="transition-all duration-300 ease-out overflow-hidden motion-reduce:transition-none"
      enter-from-class="opacity-0 max-h-0"
      enter-to-class="opacity-100 max-h-screen"
      leave-active-class="transition-all duration-300 ease-in overflow-hidden motion-reduce:transition-none"
      leave-from-class="opacity-100 max-h-screen"
      leave-to-class="opacity-0 max-h-0"
    >
      <DisclosurePanel class="overflow-hidden">
        <div :class="contentClasses">
          <slot :open="open" />
        </div>
      </DisclosurePanel>
    </transition>
  </Disclosure>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue';
import { surface, button } from '../design-system/recipes';

type Variant = 'default' | 'ghost' | 'bordered' | 'gradient';

interface Props {
  id?: string;
  title?: string;
  defaultOpen?: boolean;
  variant?: Variant;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  id: () => `accordion-item-${Math.random().toString(36).substr(2, 9)}`,
  title: '',
  defaultOpen: false,
  variant: 'default',
  disabled: false,
});

// Surface styling using design-system recipes
const surfaceClasses = computed(() => {
  const base = 'transition-all duration-200';

  const variants = {
    default: 'border-b border-border-dark',
    ghost: '',
    bordered: surface({ variant: 'surface', radius: 'lg' }) + ' mb-2 overflow-hidden',
    gradient:
      surface({ variant: 'surface', tone: 'primary', intensity: 'soft', radius: 'lg' }) +
      ' mb-2 overflow-hidden',
  };

  return `${base} ${variants[props.variant]}`;
});

// Button styling using design-system button recipe
const buttonClasses = computed(() => {
  const baseButton = button({
    variant: 'subtle',
    tone: 'neutral',
    radius: 'lg',
    disabled: props.disabled,
  });

  const variants = {
    default: 'py-4 px-0',
    ghost: 'py-3 px-0',
    bordered: 'py-4 px-5',
    gradient: 'py-4 px-5 backdrop-blur-sm',
  };

  return `${baseButton} w-full justify-between items-center text-left ${variants[props.variant]}`;
});

const iconClasses = computed(() => {
  const variants = {
    default: 'text-text-dim',
    ghost: 'text-text-dim',
    bordered: 'text-primary',
    gradient: 'text-primary',
  };

  return variants[props.variant];
});

const contentClasses = computed(() => {
  const variants = {
    default: 'pt-2 pb-4 px-0 text-text-dim',
    ghost: 'pt-2 pb-3 px-0 text-text-dim',
    bordered: 'px-5 pb-4 text-text-dim',
    gradient: 'px-5 pb-4 text-text-dim',
  };

  return variants[props.variant];
});
</script>
