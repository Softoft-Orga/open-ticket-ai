<template>
  <div :class="['rounded-xl p-4', containerClasses]">
    <div class="flex gap-3">
      <div v-if="!hideIcon" class="flex-shrink-0 mt-0.5">
        <component :is="iconComponent" :class="iconClasses" aria-hidden="true" />
      </div>
      <div class="flex-1">
        <h4 v-if="title" class="mb-1 font-semibold">{{ title }}</h4>
        <div class="text-sm">
          <slot />
        </div>
        <div v-if="$slots.footer" class="mt-3 pt-3 border-t" :class="footerBorderClasses">
          <slot name="footer" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  LightBulbIcon,
  InformationCircleIcon
} from '@heroicons/vue/24/outline'

interface Props {
  type?: 'info' | 'success' | 'warning' | 'danger' | 'tip'
  title?: string
  hideIcon?: boolean
  variant?: 'default' | 'inline'
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info',
  hideIcon: false,
  variant: 'default'
})

const iconComponent = computed(() => {
  switch (props.type) {
    case 'success':
      return CheckCircleIcon
    case 'warning':
      return ExclamationTriangleIcon
    case 'danger':
      return XCircleIcon
    case 'tip':
      return LightBulbIcon
    default:
      return InformationCircleIcon
  }
})

const iconClasses = computed(() => {
  const sizeClass = 'w-6 h-6'
  let colorClass = ''
  
  switch (props.type) {
    case 'success':
      colorClass = 'text-success'
      break
    case 'warning':
      colorClass = 'text-warning'
      break
    case 'danger':
      colorClass = 'text-danger'
      break
    case 'tip':
      colorClass = 'text-primary-light'
      break
    default:
      colorClass = 'text-info'
  }
  
  return `${sizeClass} ${colorClass}`
})

const containerClasses = computed(() => {
  const isInline = props.variant === 'inline'
  let classes = ''
  
  // Border and background classes
  if (isInline) {
    // Inline variant: no border, subtle background
    switch (props.type) {
      case 'success':
        classes = 'bg-success/5 text-gray-200'
        break
      case 'warning':
        classes = 'bg-warning/5 text-gray-200'
        break
      case 'danger':
        classes = 'bg-danger/5 text-gray-200'
        break
      case 'tip':
        classes = 'bg-primary/5 text-gray-200'
        break
      default:
        classes = 'bg-info/5 text-gray-200'
    }
  } else {
    // Default variant: with border and stronger background
    switch (props.type) {
      case 'success':
        classes = 'border border-success/30 bg-success/10 text-gray-100 shadow-sm'
        break
      case 'warning':
        classes = 'border border-warning/30 bg-warning/10 text-gray-100 shadow-sm'
        break
      case 'danger':
        classes = 'border border-danger/30 bg-danger/10 text-gray-100 shadow-sm'
        break
      case 'tip':
        classes = 'border border-primary/30 bg-primary/10 text-gray-100 shadow-sm'
        break
      default:
        classes = 'border border-info/30 bg-info/10 text-gray-100 shadow-sm'
    }
  }
  
  return classes
})

const footerBorderClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'border-success/20'
    case 'warning':
      return 'border-warning/20'
    case 'danger':
      return 'border-danger/20'
    case 'tip':
      return 'border-primary/20'
    default:
      return 'border-info/20'
  }
})
</script>
