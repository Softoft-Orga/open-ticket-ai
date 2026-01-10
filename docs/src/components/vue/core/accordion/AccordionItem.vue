<template>
  <div :class="containerClasses">
    <button
      :id="`accordion-header-${uid}`"
      type="button"
      :class="headerClasses"
      :aria-expanded="computedOpen"
      :aria-controls="`accordion-panel-${uid}`"
      @click="handleToggle"
    >
      <span :class="titleClasses">{{ title }}</span>
      <svg 
        :class="iconClasses"
        class="w-5 h-5 transition-transform duration-300"
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
    </button>
    <transition
      name="accordion"
      @enter="onEnter"
      @after-enter="onAfterEnter"
      @leave="onLeave"
    >
      <div
        v-show="computedOpen"
        :id="`accordion-panel-${uid}`"
        :class="contentClasses"
        role="region"
        :aria-labelledby="`accordion-header-${uid}`"
      >
        <div :class="contentInnerClasses">
          <slot/>
        </div>
      </div>
    </transition>
  </div>
</template>

<script lang="ts" setup>
import {ref, computed, watch} from 'vue'

type Variant = 'default' | 'ghost' | 'bordered' | 'gradient'

interface Props {
  title: string
  defaultOpen?: boolean
  isOpen?: boolean
  variant?: Variant
}

const props = withDefaults(defineProps<Props>(), {
  defaultOpen: false,
  isOpen: undefined,
  variant: 'default'
})

const emit = defineEmits<{
  (e: 'toggle'): void
}>()

const uid = Math.random().toString(36).substr(2, 9)
const internalOpen = ref(props.defaultOpen)

const computedOpen = computed(() => {
  return props.isOpen !== undefined ? props.isOpen : internalOpen.value
})

watch(() => props.isOpen, (newVal) => {
  if (newVal !== undefined) {
    internalOpen.value = newVal
  }
})

const handleToggle = () => {
  if (props.isOpen === undefined) {
    internalOpen.value = !internalOpen.value
  }
  emit('toggle')
}

// Animation handlers
const onEnter = (el: Element) => {
  const element = el as HTMLElement
  element.style.height = '0'
  element.offsetHeight // Force reflow
  element.style.height = element.scrollHeight + 'px'
}

const onAfterEnter = (el: Element) => {
  const element = el as HTMLElement
  element.style.height = 'auto'
}

const onLeave = (el: Element) => {
  const element = el as HTMLElement
  element.style.height = element.scrollHeight + 'px'
  element.offsetHeight // Force reflow
  element.style.height = '0'
}

// Variant-based styling
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

const iconClasses = computed(() => {
  const rotation = computedOpen.value ? 'rotate-180' : 'rotate-0'
  
  const variants = {
    default: 'text-text-dim',
    ghost: 'text-text-dim',
    bordered: 'text-primary',
    gradient: 'text-primary'
  }
  
  return `${rotation} ${variants[props.variant]}`
})

const contentClasses = computed(() => {
  return 'overflow-hidden transition-all duration-300 ease-in-out'
})

const contentInnerClasses = computed(() => {
  const variants = {
    default: 'pt-2 pb-4 px-0 text-gray-400',
    ghost: 'pt-2 pb-3 px-0 text-gray-400',
    bordered: 'px-5 pb-4 text-gray-400',
    gradient: 'px-5 pb-4 text-gray-400'
  }
  
  return variants[props.variant]
})
</script>

<style scoped>
.accordion-enter-active,
.accordion-leave-active {
  transition: height 0.3s ease-in-out;
}

.accordion-enter-from,
.accordion-leave-to {
  height: 0;
}
</style>
