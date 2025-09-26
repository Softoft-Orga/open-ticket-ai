<template>
  <div :class="['my-4 p-4 border-l-4 rounded', colorClasses]">
    <div class="flex items-start gap-2">
      <span>{{ icon }}</span>
      <div class="flex-1">
        <slot />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

interface Props {
  type?: 'info' | 'success' | 'warning' | 'danger'
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info'
})

const colorClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'bg-green-800/20 border-green-400 text-green-300'
    case 'warning':
      return 'bg-yellow-800/20 border-yellow-500 text-yellow-400'
    case 'danger':
      return 'bg-pink-800/20 border-pink-500 text-pink-400'
    default:
      return 'bg-vp-brand/10 border-vp-brand text-vp-brand'
  }
})

const icon = computed(() => {
  switch (props.type) {
    case 'success':
      return '✔'
    case 'warning':
      return '⚠'
    case 'danger':
      return '✖'
    default:
      return 'ℹ'
  }
})
</script>
