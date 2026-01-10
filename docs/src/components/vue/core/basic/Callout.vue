<template>
  <div :class="['my-4 p-4 rounded', borderClasses, colorClasses]">
    <div class="flex items-start gap-2">
      <component :is="iconComponent" class="w-5 h-5 flex-shrink-0 mt-0.5" aria-hidden="true" />
      <div class="flex-1">
        <slot/>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {computed} from 'vue'
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  InformationCircleIcon
} from '@heroicons/vue/24/outline'
import type {Tone} from '../design-system/tokens'

interface Props {
  type?: Tone
  variant?: 'left-border' | 'bordered' | 'filled'
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info',
  variant: 'left-border'
})

const borderClasses = computed(() => {
  switch (props.variant) {
    case 'bordered':
      return 'border-2'
    case 'filled':
      return ''
    default:
      return 'border-l-4'
  }
})

const colorClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'bg-emerald-500/15 border-emerald-500 text-emerald-300'
    case 'warning':
      return 'bg-amber-500/15 border-amber-400 text-amber-300'
    case 'danger':
      return 'bg-rose-500/15 border-rose-500 text-rose-300'
    default:
      return 'bg-primary/10 border-primary text-primary'
  }
})

const iconComponent = computed(() => {
  switch (props.type) {
    case 'success':
      return CheckCircleIcon
    case 'warning':
      return ExclamationTriangleIcon
    case 'danger':
      return XCircleIcon
    default:
      return InformationCircleIcon
  }
})
</script>
