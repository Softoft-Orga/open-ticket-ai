<template>
  <div 
    :class="[
      cardClasses,
      'border border-border-dark rounded-lg shadow text-text-dim',
      paddingClass
    ]"
  >
    <div v-if="$slots.image" class="overflow-hidden rounded-t-lg -m-6 mb-0">
      <slot name="image"/>
    </div>
    <div v-if="$slots.header" :class="headerClasses">
      <slot name="header"/>
    </div>
    <div v-if="$slots.title" :class="titleClasses">
      <slot name="title"/>
    </div>
    <div :class="contentClasses">
      <slot/>
    </div>
    <div v-if="$slots.actions" :class="actionsClasses">
      <slot name="actions"/>
    </div>
    <div v-if="$slots.footer" :class="footerClasses">
      <slot name="footer"/>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

export interface CardProps {
  /**
   * Background color variant
   * @default 'default'
   */
  background?: 'default' | 'surface-dark' | 'surface-lighter' | 'primary' | 'gradient' | 'transparent' | 'custom'
  
  /**
   * Custom background class when background is 'custom'
   */
  customBg?: string
  
  /**
   * Padding size
   * @default 'default'
   */
  padding?: 'none' | 'sm' | 'default' | 'lg'
  
  /**
   * Whether to add hover effect
   * @default false
   */
  hoverable?: boolean
}

const props = withDefaults(defineProps<CardProps>(), {
  background: 'default',
  customBg: '',
  padding: 'default',
  hoverable: false,
})

const backgroundClasses: Record<string, string> = {
  'default': 'bg-surface-dark',
  'surface-dark': 'bg-surface-dark',
  'surface-lighter': 'bg-surface-lighter',
  'primary': 'bg-primary/10',
  'gradient': 'bg-cyber-gradient',
  'transparent': 'bg-transparent',
  'custom': props.customBg || 'bg-surface-dark',
}

const paddingClasses: Record<string, string> = {
  'none': 'p-0',
  'sm': 'p-4',
  'default': 'p-6',
  'lg': 'p-8',
}

const cardClasses = computed(() => {
  const classes = [
    backgroundClasses[props.background],
  ]
  
  if (props.hoverable) {
    classes.push('transition-all duration-300 hover:border-primary/50 hover:shadow-glow cursor-pointer')
  }
  
  return classes.join(' ')
})

const paddingClass = computed(() => paddingClasses[props.padding])

const headerClasses = computed(() => {
  const spacing = props.padding === 'none' ? 'px-6 pt-6 pb-4' : 'mb-4'
  return spacing
})

const titleClasses = computed(() => {
  const spacing = props.padding === 'none' ? 'px-6 pb-2' : 'mb-2'
  return `${spacing} text-lg font-bold text-white`
})

const contentClasses = computed(() => {
  const spacing = props.padding === 'none' ? 'px-6 py-4' : 'mb-4'
  return `${spacing} text-white`
})

const actionsClasses = computed(() => {
  const spacing = props.padding === 'none' ? 'px-6 py-4' : 'mt-4'
  return spacing
})

const footerClasses = computed(() => {
  const spacing = props.padding === 'none' ? 'px-6 pb-6 pt-4' : 'mt-4'
  return `${spacing} text-text-dim`
})
</script>
