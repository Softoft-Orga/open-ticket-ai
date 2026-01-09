<template>
  <div :class="['rounded-xl border p-4 shadow-sm', variantClasses]">
    <div class="flex gap-3">
      <div v-if="!hideIcon" class="flex-shrink-0">
        <component :is="iconComponent" class="w-5 h-5" aria-hidden="true" />
      </div>
      <div class="flex-1">
        <h4 v-if="title" class="mb-1 font-semibold">{{ title }}</h4>
        <div class="text-sm">
          <slot />
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
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info',
  hideIcon: false
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

const variantClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'border-emerald-500/30 bg-emerald-500/10 text-emerald-100'
    case 'warning':
      return 'border-amber-500/30 bg-amber-500/10 text-amber-100'
    case 'danger':
      return 'border-rose-500/30 bg-rose-500/10 text-rose-100'
    case 'tip':
      return 'border-primary/30 bg-primary/10 text-primary-light'
    default:
      return 'border-blue-500/30 bg-blue-500/10 text-blue-100'
  }
})
</script>
