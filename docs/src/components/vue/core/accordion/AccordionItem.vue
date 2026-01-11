<template>
  <Disclosure
    v-slot="{ open }"
    :default-open="defaultOpen"
    as="div"
    :class="containerClasses"
  >
    <DisclosureButton
      :class="headerClasses"
    >
      <span :class="titleClasses">{{ title }}</span>
      <svg 
        :class="[
          'w-5 h-5 transition-transform duration-300',
          open ? 'rotate-180' : 'rotate-0',
          iconColorClasses
        ]"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        aria-hidden="true"
      >
        <path 
          stroke-linecap="round" 
          stroke-linejoin="round" 
          stroke-width="2" 
          d="M19 9l-7 7-7-7"
        />
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
      <DisclosurePanel
        :class="contentClasses"
      >
        <div :class="contentInnerClasses">
          <slot />
        </div>
      </DisclosurePanel>
    </transition>
  </Disclosure>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'

type Variant = 'default' | 'ghost' | 'bordered' | 'gradient'

interface Props {
  title: string
  defaultOpen?: boolean
  variant?: Variant
}

const props = withDefaults(defineProps<Props>(), {
  defaultOpen: false,
  variant: 'default'
})


// Variant-based styling using Tailwind tokens
const containerClasses = computed(() => {
  const base = 'transition-all duration-200'
  
  const variants = {
    default: 'border-b border-border-dark',
    ghost: '',
    bordered: 'border border-border-dark rounded-lg mb-2 overflow-hidden',
    gradient: 'border border-primary/30 rounded-lg mb-2 overflow-hidden bg-gradient-to-r from-primary/5 to-transparent'
  }
  
  return `${base} ${variants[props.variant]}`
})

const headerClasses = computed(() => {
  const base = 'flex w-full justify-between items-center text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-primary transition-all duration-200'
  
  const variants = {
    default: 'py-4 px-0 hover:text-primary',
    ghost: 'py-3 px-0 hover:text-primary',
    bordered: 'py-4 px-5 bg-surface-dark hover:bg-surface-lighter',
    gradient: 'py-4 px-5 bg-surface-dark/50 hover:bg-surface-dark backdrop-blur-sm'
  }
  
  return `${base} ${variants[props.variant]}`
})

const titleClasses = computed(() => {
  const base = 'font-semibold transition-colors duration-200'
  
  const variants = {
    default: 'text-lg text-white',
    ghost: 'text-base text-white',
    bordered: 'text-lg text-white',
    gradient: 'text-lg text-white'
  }
  
  return `${base} ${variants[props.variant]}`
})

const iconColorClasses = computed(() => {
  const variants = {
    default: 'text-text-dim',
    ghost: 'text-text-dim',
    bordered: 'text-primary',
    gradient: 'text-primary'
  }
  
  return variants[props.variant]
})

const contentClasses = computed(() => {
  return 'overflow-hidden'
})

const contentInnerClasses = computed(() => {
  const variants = {
    default: 'pt-2 pb-4 px-0 text-text-dim',
    ghost: 'pt-2 pb-3 px-0 text-text-dim',
    bordered: 'px-5 pb-4 text-text-dim',
    gradient: 'px-5 pb-4 text-text-dim'
  }
  
  return variants[props.variant]
})
</script>
